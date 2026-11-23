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


def base_paths_with_id(root: Path, base: str, identifier: str) -> set[str]:
    """Base-tree paths carrying the audited ID."""
    files = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", base, "--", "backlog"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if files.returncode != 0:
        return set()
    result: set[str] = set()
    for path in files.stdout.splitlines():
        if not path.endswith(".md"):
            continue
        text = subprocess.run(
            ["git", "show", f"{base}:{path}"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if text.returncode != 0:
            continue
        record = records(text.stdout, base, path)
        if record and record["id"] == identifier:
            result.add(path)
    return result


def related_refs(
    root: Path, left: str, right: str, identifier: str, old: str, new: str
) -> bool:
    """Whether a record moved between two related refs.

    True when the refs share a merge base whose tree carries the
    audited ID at exactly one of the two paths — the record existed at
    the old path before the fork and the new path appeared after it.
    Shared ancestry alone is not enough: independently added same-title
    records on sibling branches also share a base, and a base path
    carrying a different ID is not this record's history.
    """

    def rev(branch: str) -> str:
        return "HEAD" if branch == "working-tree" else branch

    result = subprocess.run(
        ["git", "merge-base", rev(left), rev(right)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return False
    base = result.stdout.strip()
    with_id = base_paths_with_id(root, base, identifier)
    return (old in with_id) != (new in with_id)


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

        # A rename leaves two visible shapes: (1) one ref holds both paths
        # with the SAME title on each; (2) an ordinary git mv leaves only
        # the new path on the rename branch and the old path on the
        # parent — same title, disjoint paths, across ancestor-connected
        # refs whose merge base carries the ID at the old path. Union
        # nodes are (branch, path) pairs: the same path on a different
        # branch is a different node, so a divergent branch's variant of
        # a path is never absorbed by another branch's rename.
        nodes: dict[tuple[str, str], tuple[str, str]] = {
            (branch, path): (branch, path) for (branch, path) in title_on_branch
        }

        def find(
            node: tuple[str, str],
            links: dict[tuple[str, str], tuple[str, str]] = nodes,
        ) -> tuple[str, str]:
            while links[node] != node:
                links[node] = links[links[node]]
                node = links[node]
            return node

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
                        and find((branch, left)) != find((branch, right))
                    ):
                        nodes[find((branch, right))] = find((branch, left))
        if len(branches) > 1:
            for branch_a, paths_a in branches.items():
                for branch_b in branches:
                    if branch_a == branch_b:
                        continue
                    only_a = [p for p in paths_a if p not in branches[branch_b]]
                    only_b = [p for p in branches[branch_b] if p not in paths_a]
                    if not only_a or not only_b:
                        continue
                    if root is not None and not related_refs(
                        root, branch_a, branch_b, identifier, only_a[0], only_b[0]
                    ):
                        continue  # independent additions, not a rename
                    titles_a = {title_on_branch[(branch_a, p)] for p in only_a}
                    titles_b = {title_on_branch[(branch_b, p)] for p in only_b}
                    if titles_a and titles_a == titles_b and None not in titles_a:
                        for path in only_b:
                            nodes[find((branch_b, path))] = find((branch_a, only_a[0]))
        # A work is a set of paths; project branch-scoped components down
        # to their path sets, then compare. A path counts as belonging to
        # a work only through the refs that were merged above — a path
        # shared by several branches contributes the branch-specific node
        # of each, so divergent variants stay separate unless git history
        # connected them.
        works: dict[tuple[str, str], set[str]] = defaultdict(set)
        for node in nodes:
            works[find(node)].add(node[1])
        distinct_works: list[set[str]] = []
        for component_paths in works.values():
            for existing in distinct_works:
                if component_paths & existing:
                    existing |= component_paths
                    break
            else:
                distinct_works.append(set(component_paths))
        if len(distinct_works) > 1:
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
