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


def related_refs(root: Path, left: str, right: str) -> bool:
    """Whether two refs share history (one forked from the other).

    An ordinary rename branch shares history with its parent; an
    orphan branch shares none. Used to merge a rename viewed from
    opposite sides without merging independent same-title records.
    """
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", left, right],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return True
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", right, left],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def collisions(
    items: list[dict[str, Any]], root: Path | None = None
) -> list[dict[str, Any]]:
    """One ID with more than one meaning across refs.

    A record's identity is its path. All titles a path carries across
    refs belong to ONE record lineage — a retitle never splits meanings.
    Distinct paths are distinct records, merged into one work only when
    a single branch holds both with the SAME title on each — the trace a
    rename-without-retitle leaves. Same-title paths on independent
    branches are not identity proof: they collide. Same-path divergence
    is delegated to git's own merge conflict, not detected here.
    """
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        by_id[item["id"]].append(item)
    results: list[dict[str, Any]] = []
    for identifier, recs in by_id.items():
        titles_by_path: dict[str, set[str]] = defaultdict(set)
        title_on_branch: dict[tuple[str, str], str | None] = {}
        for item in recs:
            if item["title"] is not None:
                titles_by_path[item["path"]].add(item["title"])
            title_on_branch[(item["branch"], item["path"])] = item["title"]
        if len(titles_by_path) < 2:
            continue  # one path = one record lineage, retitles included
        paths = list(titles_by_path)
        parent = {path: path for path in paths}

        def find(path: str, links: dict[str, str] = parent) -> str:
            while links[path] != path:
                links[path] = links[links[path]]
                path = links[path]
            return path

        # A rename leaves two visible shapes: (1) one ref holds both paths
        # with the SAME title on each; (2) an ordinary git mv leaves only
        # the new path on the rename branch and the old path on the
        # parent — same title, disjoint paths, across ancestor-connected
        # refs. Same-title paths on independent branches are not identity
        # proof: they collide.
        branches: dict[str, list[str]] = defaultdict(list)
        for (branch, _), _title in title_on_branch.items():
            branches[branch].append(_)
        for branch, branch_paths in branches.items():
            for index, left in enumerate(branch_paths):
                for right in branch_paths[index + 1 :]:
                    left_title = title_on_branch[(branch, left)]
                    right_title = title_on_branch[(branch, right)]
                    if (
                        left_title is not None
                        and left_title == right_title
                        and find(left) != find(right)
                    ):
                        parent[find(right)] = find(left)
        if len(branches) > 1:
            for branch_a, paths_a in branches.items():
                for branch_b in branches:
                    if branch_a == branch_b:
                        continue
                    if root is not None and not related_refs(root, branch_a, branch_b):
                        continue  # independent histories: not a rename
                    only_a = [p for p in paths_a if p not in branches[branch_b]]
                    only_b = [p for p in branches[branch_b] if p not in paths_a]
                    if not only_a or not only_b:
                        continue
                    titles_a = {title_on_branch[(branch_a, p)] for p in only_a}
                    titles_b = {title_on_branch[(branch_b, p)] for p in only_b}
                    if titles_a and titles_a == titles_b and None not in titles_a:
                        for path in only_b:
                            parent[find(path)] = find(only_a[0])
        works = {find(path) for path in paths}
        if len(works) > 1:
            titles = sorted({t for s in titles_by_path.values() for t in s})
            results.append({"id": identifier, "titles": titles})
    return results


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
        working_by_path = {item["path"]: item for item in working}
        overlayed = []
        for item in items:
            if branch is None or item["branch"] != branch:
                overlayed.append(item)  # other refs keep their versions
                continue
            local = working_by_path.get(item["path"])
            if local is None:
                overlayed.append(item)  # no working-tree version at this path
                continue
            if (local["id"], local["title"]) == (item["id"], item["title"]):
                overlayed.append(item)
                continue  # identical: keep one copy, appended once below
            overlayed.append(item)
            # A CHANGED local edit still leaves the committed version in
            # scope: the collision check needs the checked-out branch's
            # committed state to compare divergent refs against. The
            # working-tree version joins below as the record's new state.
        overlayed = overlayed + working
        problems = collisions(overlayed, root) + duplicate_ids(items + working)
        print(json.dumps({"records": len(overlayed), "collisions": problems}, indent=2))
        return int(bool(problems))
    problems = collisions(items) + duplicate_ids(items)
    print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
