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
    grouped: dict[str, set[str]] = defaultdict(set)
    for item in items:
        if item["title"] is not None:
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--refs", action="store_true", help="Audit all Git refs")
    args = parser.parse_args()
    root = args.root.resolve()
    items = checkout_records(root)
    if args.refs:
        items = git_records(root)
    problems = collisions(items) + duplicate_ids(items)
    print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
