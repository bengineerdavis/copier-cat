#!/usr/bin/env python3
"""Cross-branch backlog ID audit.

Read the native store's YAML frontmatter, never rewrite it. Flag one
record ID assigned to different work on two branches BEFORE those
branches meet in a merge — the failure backlog-py cannot see, because
its ID allocation reads the current checkout only.

Lineage is git's job. For each pair of refs carrying an ID, git itself
merges them (``git merge-tree --write-tree``, a read-only merge in
memory) and the merged tree is inspected: if the ID survives at two or
more paths there, the two branches give the ID two meanings. Every
rename, retitle, chain, and conflict shape is resolved by git's own
machinery — this script never infers lineage.

Working-tree state participates as a throwaway commit built from the
index (``git write-tree`` + ``git commit-tree``, no HEAD is moved), so
uncommitted records and staged renames are audited like any ref.

Read-only public script: no store file and no Git ref is modified.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
ID_RE = re.compile(r"^id:\s*(.+?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
WORKING_TREE = "working-tree"


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def parse_frontmatter(source: str) -> dict[str, Any]:
    match = FRONTMATTER_RE.match(source)
    if match is None:
        return {}
    body = match.group(1)
    id_match = ID_RE.search(body)
    title_match = TITLE_RE.search(body)
    return {
        "id": id_match.group(1).strip() if id_match else None,
        "title": title_match.group(1).strip() if title_match else None,
    }


def checkout_records(root: Path) -> list[dict[str, Any]]:
    """Read every record in the current checkout."""
    items: list[dict[str, Any]] = []
    for path in sorted((root / "backlog").rglob("*.md")):
        if not path.is_file():
            continue
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if meta.get("id") is None:
            continue
        items.append(
            {
                "id": meta["id"],
                "title": meta["title"],
                "branch": WORKING_TREE,
                "path": path.relative_to(root).as_posix(),
            }
        )
    return items


def git_records(root: Path) -> list[dict[str, Any]]:
    """Read every record on every branch and remote ref."""
    items: list[dict[str, Any]] = []
    refs = run_git(
        root, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes"
    )
    if refs.returncode != 0:
        return items
    for ref in refs.stdout.splitlines():
        if ref.endswith("/HEAD"):
            continue
        listing = run_git(root, "ls-tree", "-r", "--name-only", ref, "--", "backlog")
        if listing.returncode != 0:
            continue
        for relpath in listing.stdout.splitlines():
            content = run_git(root, "show", f"{ref}:{relpath}")
            if content.returncode != 0:
                continue
            meta = parse_frontmatter(content.stdout)
            if meta.get("id") is None:
                continue
            items.append(
                {
                    "id": meta["id"],
                    "title": meta["title"],
                    "branch": ref,
                    "path": relpath,
                }
            )
    return items


def working_tree_commit(root: Path) -> str | None:
    """A throwaway commit of the full working state, parented on HEAD.

    A temporary index (``GIT_INDEX_FILE``) is seeded from HEAD and
    refreshed from disk, so staged, unstaged, and untracked records all
    participate. ``git write-tree`` turns that index into a tree and
    ``git commit-tree`` wraps it in a commit so ``git merge-tree`` can
    merge the working state like any ref. Everything writes only to the
    object database and the temp file — no ref moves, the real index is
    never touched.
    """
    import os
    import tempfile as _tempfile

    fd, index_path = _tempfile.mkstemp(prefix="backlog-audit-index-")
    os.close(fd)
    index = Path(index_path)
    env = {**os.environ, "GIT_INDEX_FILE": str(index)}
    try:
        seed = subprocess.run(
            ["git", "read-tree", "HEAD"],
            cwd=root,
            capture_output=True,
            env=env,
            check=False,
        )
        if seed.returncode != 0:
            return None
        refresh = subprocess.run(
            ["git", "add", "-A", "--", "backlog"],
            cwd=root,
            capture_output=True,
            env=env,
            check=False,
        )
        if refresh.returncode != 0:
            return None
        tree = subprocess.run(
            ["git", "write-tree"],
            cwd=root,
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        if tree.returncode != 0:
            return None
        head = run_git(root, "rev-parse", "HEAD")
        parent: list[str] = []
        if head.returncode == 0 and head.stdout.strip():
            parent = ["-p", head.stdout.strip()]
        commit = run_git(
            root,
            "commit-tree",
            *parent,
            "-m",
            "backlog-audit working state",
            tree.stdout.strip(),
        )
        if commit.returncode != 0:
            return None
        return commit.stdout.strip()
    finally:
        index.unlink(missing_ok=True)


def tree_id_paths(root: Path, tree: str, identifier: str) -> list[str]:
    """Paths in a merged tree whose record carries the audited ID."""
    listing = run_git(root, "ls-tree", "-r", "--name-only", tree, "--", "backlog")
    if listing.returncode != 0:
        return []
    hits: list[str] = []
    for relpath in listing.stdout.splitlines():
        content = run_git(root, "show", f"{tree}:{relpath}")
        if content.returncode != 0:
            continue
        meta = parse_frontmatter(content.stdout)
        if meta.get("id") == identifier:
            hits.append(relpath)
    return hits


def unrelated_refs(root: Path, left: str, right: str) -> bool:
    """True when two refs share no history — no merge will ever exist."""
    result = run_git(root, "merge-base", left, right)
    return result.returncode != 0 or not result.stdout.strip()


def collisions(
    items: list[dict[str, Any]], root: Path | None = None
) -> list[dict[str, Any]]:
    """One ID with more than one meaning, judged by git's own merges.

    For every pair of refs carrying the ID: unrelated refs mean the ID
    was reused with no shared history to reconcile it — a collision.
    Related refs are merged in memory; if the merged tree carries the
    ID at two or more paths, the branches give it two meanings. Content
    conflicts at a single path are git's own merge conflict and stay
    delegated to it.
    """
    if root is None:
        return []

    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        by_id[item["id"]].append(item)
    results: list[dict[str, Any]] = []

    for identifier, recs in by_id.items():
        refs = {item["branch"] for item in recs}
        if len(refs) < 2:
            continue
        titles = sorted({item["title"] for item in recs if item["title"] is not None})
        ordered = sorted(refs)
        collided = False
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                if unrelated_refs(root, left, right):
                    collided = True
                    break
                merge = run_git(root, "merge-tree", "--write-tree", left, right)
                tree = merge.stdout.splitlines()[0] if merge.stdout.strip() else None
                if tree is None:
                    # Refs merge cleanly but merge-tree produced no tree:
                    # treat as collided rather than silently passing.
                    collided = True
                    break
                if len(tree_id_paths(root, tree, identifier)) >= 2:
                    collided = True
                    break
            if collided:
                break
        if collided:
            results.append({"id": identifier, "titles": titles})
    return results


def duplicate_ids(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The same ID twice inside ONE ref — a within-branch duplicate."""
    grouped: dict[tuple[str, str], set[str]] = defaultdict(set)
    for item in items:
        grouped[(item["branch"], item["id"])].add(item["path"])
    return [
        {"id": identifier, "paths": sorted(paths)}
        for (branch, identifier), paths in grouped.items()
        if len(paths) > 1
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--refs", action="store_true", help="Audit all Git refs")
    args = parser.parse_args()
    root = args.root.resolve()
    if not args.refs:
        items = checkout_records(root)
        problems = collisions(items) + duplicate_ids(items)
        print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
        return int(bool(problems))

    committed = git_records(root)
    working = working_tree_commit(root)
    items: list[dict[str, Any]] = list(committed)
    # The working state participates as its own ref (the throwaway commit)
    # for records the checked-out branch does not already carry — new or
    # edited-but-uncommitted records join; unchanged ones are already
    # represented by the checked-out ref.
    checked_out = run_git(root, "branch", "--show-current").stdout.strip() or None
    if working is not None:
        carried: set[tuple[str, str]] = {
            (rec["path"], rec["id"])
            for rec in committed
            if checked_out is not None and rec["branch"] == checked_out
        }
        for item in checkout_records(root):
            if (item["path"], item["id"]) in carried:
                continue
            items.append(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "branch": working,
                    "path": item["path"],
                }
            )
    problems = collisions(items, root) + duplicate_ids(items)
    print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
