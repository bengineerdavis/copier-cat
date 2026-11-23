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


def merge_base_of(root: Path | None, left: str, right: str) -> str | None:
    """The merge base commit of two refs, if any."""
    if root is None:
        return None

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
        return None
    return result.stdout.strip()


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
    base = merge_base_of(root, left, right)
    if base is None:
        return False
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
        paths_seen: set[str] = set()
        title_on_branch: dict[tuple[str, str], str | None] = {}
        for item in recs:
            paths_seen.add(item["path"])
            if item["title"] is not None:
                titles_by_path[item["path"]].add(item["title"])
            title_on_branch[(item["branch"], item["path"])] = item["title"]
        if len(paths_seen) < 2:
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
            # Collect rename claims first, then resolve: a claim records
            # (source path, destination path, source branch, dest branch).
            # Two claims on one source diverge unless one continues the
            # other as a chain — the later claim's source equals the
            # earlier claim's destination AND its branch descends from
            # the earlier claim's branch. Iterating first and resolving
            # after avoids mid-loop poisoning between pair directions.
            claims: dict[tuple[str, str], tuple[str, str, str, str]] = {}
            checked_out = current_branch(root) if root is not None else None
            for branch_a, paths_a in branches.items():
                for branch_b in branches:
                    if branch_a == branch_b:
                        continue
                    # The working-tree node is the checked-out branch's
                    # current state; pairing it with that same branch
                    # would duplicate one real branch's view. Against any
                    # OTHER ref it carries real information (uncommitted
                    # renames), so it participates there.
                    if branch_a == "working-tree" and branch_b == checked_out:
                        continue
                    if branch_b == "working-tree" and branch_a == checked_out:
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
                    if not (titles_a and titles_a == titles_b and None not in titles_a):
                        continue
                    pair_key = (min(branch_a, branch_b), max(branch_a, branch_b))
                    if pair_key in claims:
                        continue  # same rename seen from the other side
                    # Canonical orientation: the pair's merge base
                    # carries the SOURCE path; the destination appeared
                    # after the fork.
                    assert root is not None
                    base = merge_base_of(root, branch_a, branch_b)
                    with_id = (
                        base_paths_with_id(root, base, identifier)
                        if base is not None
                        else set()
                    )
                    if only_b[0] in with_id:
                        claims[pair_key] = (
                            only_b[0],
                            only_a[0],
                            branch_b,
                            branch_a,
                        )
                    else:
                        claims[pair_key] = (only_a[0], only_b[0], branch_a, branch_b)
            accepted: list[tuple[str, str, str, str]] = []
            # Staged renames are a git-provided fact — union them, but
            # only for the audited ID: the destination must carry this
            # ID in the working tree, and the source must be the
            # checked-out branch's committed record for this ID.
            if root is not None:
                staged = subprocess.run(
                    ["git", "diff", "--cached", "--name-status", "-M"],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                checked_out = current_branch(root)
                if staged.returncode == 0 and checked_out is not None:
                    for line in staged.stdout.splitlines():
                        parts = line.split("\t")
                        if len(parts) != 3 or not parts[0].startswith("R"):
                            continue
                        old, new = parts[1], parts[2]
                        working_for_id = {
                            (item["branch"], item["path"])
                            for item in recs
                            if item["branch"] == "working-tree" and item["path"] == new
                        }
                        committed_for_id = {
                            (item["branch"], item["path"])
                            for item in recs
                            if item["branch"] == checked_out and item["path"] == old
                        }
                        if working_for_id and committed_for_id:
                            nodes[find(next(iter(working_for_id)))] = find(
                                next(iter(committed_for_id))
                            )
            for pair_key in sorted(claims):
                source, dest, src_branch, dest_branch = claims[pair_key]
                conflict = False
                for other in accepted:
                    o_src, o_dest, _o_src_branch, o_dest_branch = other
                    shares_path = bool({o_src, o_dest} & {source, dest})
                    same_pair = {o_src, o_dest} == {source, dest}
                    if shares_path and not same_pair:
                        # Claims compete for one path. They compose into a
                        # chain when the earlier claim's destination is
                        # this claim's source AND this claim's branch
                        # descends from the earlier claim's destination
                        # branch — the record moved along one lineage.
                        # Otherwise the histories are independent and
                        # git will report a rename/rename conflict.
                        composes = o_dest == source or o_src == dest
                        if not composes:
                            conflict = True
                            break
                        if root is None:
                            conflict = True
                            break
                        # The two claims must sit on ONE lineage: either
                        # claim's branches may descend from the other's
                        # (a chain read forward or backward through the
                        # sorted pair order). The working-tree pseudo-ref
                        # resolves to the checked-out branch.
                        later_nodes = {src_branch, dest_branch}
                        earlier_nodes = {
                            _o_src_branch,
                            o_dest_branch,
                        }

                        def real(b: str) -> str:
                            if b != "working-tree" or root is None:
                                return b
                            return current_branch(root) or b

                        related = False
                        for ln in later_nodes:
                            for en in earlier_nodes:
                                a, b = real(ln), real(en)
                                if a == b:
                                    related = True
                                else:
                                    ok1 = (
                                        subprocess.run(
                                            [
                                                "git",
                                                "merge-base",
                                                "--is-ancestor",
                                                a,
                                                b,
                                            ],
                                            cwd=root,
                                            capture_output=True,
                                            check=False,
                                        ).returncode
                                        == 0
                                    )
                                    ok2 = (
                                        subprocess.run(
                                            [
                                                "git",
                                                "merge-base",
                                                "--is-ancestor",
                                                b,
                                                a,
                                            ],
                                            cwd=root,
                                            capture_output=True,
                                            check=False,
                                        ).returncode
                                        == 0
                                    )
                                    related = related or ok1 or ok2
                            if related:
                                break
                        if not related:
                            conflict = True
                            break
                if conflict:
                    continue
                accepted.append((source, dest, src_branch, dest_branch))
            for source, dest, src_branch, dest_branch in accepted:
                nodes[find((dest_branch, dest))] = find((src_branch, source))
        # A work is a set of paths; project branch-scoped components down
        # to their path sets, then compare. Components sharing a path are
        # the same record ONLY when their refs are related — on related
        # refs, same-path divergence is git's own merge conflict; on
        # unrelated refs (an orphan branch), no git merge will ever
        # exist to catch the ID reuse, so the components stay apart and
        # the collision is reported here.
        works: dict[tuple[str, str], set[str]] = defaultdict(set)
        for node in nodes:
            works[find(node)].add(node[1])
        components: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
        for node in nodes:
            components[find(node)].add(node)
        distinct_works: list[set[str]] = []
        component_refs: list[set[str]] = []
        for _root_node, comp_nodes in components.items():
            comp_paths = {n[1] for n in comp_nodes}
            comp_branches = {n[0] for n in comp_nodes}
            merged = False
            for index, existing in enumerate(distinct_works):
                if comp_paths & existing:
                    prior_branches = component_refs[index]
                    if root is None or any(
                        merge_base_of(root, a, b) is not None
                        for a in comp_branches
                        for b in prior_branches
                    ):
                        existing |= comp_paths
                        component_refs[index] |= comp_branches
                        merged = True
                        break
            if not merged:
                distinct_works.append(comp_paths)
                component_refs.append(comp_branches)
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
