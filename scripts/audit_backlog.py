"""Audit native Backlog IDs across a checkout and its Git refs.

Read-only public script: no store files or Git refs are modified. Unlike a
single-tree lint, this catches the same ID assigned to different work on two
branches before those branches meet in a merge.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


def records(text: str, branch: str, path: str) -> dict[str, Any] | None:
    """Read the native store's YAML frontmatter, never rewrite it."""
    if not text.startswith("---\n"):
        return None
    frontmatter, marker, _ = text[4:].partition("\n---\n")
    if not marker:
        return None
    metadata = yaml.safe_load(frontmatter) or {}
    identifier = metadata.get("id")
    if not isinstance(identifier, str):
        return None
    title = metadata.get("title")
    return {
        "id": identifier,
        "title": str(title) if title is not None else None,
        "branch": branch,
        "path": path,
    }


def checkout_records(root: Path) -> list[dict[str, Any]]:
    result = []
    for path in (root / "backlog").rglob("*.md"):
        record = records(
            path.read_text(encoding="utf-8"),
            "working-tree",
            path.relative_to(root).as_posix(),
        )
        if record:
            result.append(record)
    return result


def git_records(root: Path) -> list[dict[str, Any]]:
    refs = subprocess.run(
        [
            "git",
            "for-each-ref",
            "--format=%(refname:short)",
            "refs/heads",
            "refs/remotes",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    result = []
    for ref in refs:
        if ref.endswith("/HEAD"):
            continue
        files = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref, "--", "backlog"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        for path in files:
            if not path.endswith(".md"):
                continue
            text = subprocess.run(
                ["git", "show", f"{ref}:{path}"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            record = records(text, ref, path)
            if record:
                result.append(record)
    return result


def collisions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One ID with more than one meaning across refs.

    A same-path retitle is one record, not two meanings: when two refs
    carry the same path for an ID, their titles describe the same record
    at different times, so only titles from records whose paths are NOT
    shared across refs count as distinct meanings.
    """
    grouped: dict[str, set[str]] = defaultdict(set)
    for item in items:
        if item["title"] is None:
            continue
        # Count a title as a distinct meaning only when this record's
        # path is not shared with another ref carrying the same ID.
        shared = sum(
            1
            for other in items
            if other["id"] == item["id"] and other["path"] == item["path"]
        )
        if shared > 1:
            continue
        grouped[item["id"]].add(item["title"])
    return [
        {"id": identifier, "titles": sorted(titles)}
        for identifier, titles in grouped.items()
        if len(titles) > 1
    ]


def duplicate_ids(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], set[str]] = defaultdict(set)
    for item in items:
        grouped[(item["branch"], item["id"])].add(item["path"])
    return [
        {"id": identifier, "paths": sorted(paths)}
        for (_, identifier), paths in grouped.items()
        if len(paths) > 1
    ]


def current_branch(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    branch = result.stdout.strip()
    return branch or None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--refs", action="store_true", help="Audit all Git refs")
    args = parser.parse_args()
    root = args.root.resolve()
    if not args.refs:
        items = checkout_records(root)
    else:
        items = git_records(root)
        # Overlay the working tree onto committed records for the same path
        # ONLY when the committed content matches the checked-out branch's
        # committed content — the record the working tree edits. A divergent
        # branch's own version of the path is different work and stays.
        # Collisions are judged on the overlayed set; duplicate IDs are judged
        # on the raw set, so a within-branch duplicate stays detectable even
        # when the overlay replaces one of its paths.
        branch = current_branch(root)
        working = checkout_records(root)
        committed_on_branch = {
            item["path"]: (item["id"], item["title"])
            for item in items
            if branch is not None and item["branch"] == branch
        }
        overlayed = []
        for item in items:
            same_as_branch = committed_on_branch.get(item["path"]) == (
                item["id"],
                item["title"],
            )
            if same_as_branch:
                continue  # replaced by the working-tree version below
            overlayed.append(item)
        overlayed = overlayed + working
        problems = collisions(overlayed) + duplicate_ids(items + working)
        print(json.dumps({"records": len(overlayed), "collisions": problems}, indent=2))
        return int(bool(problems))
    problems = collisions(items) + duplicate_ids(items)
    print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
