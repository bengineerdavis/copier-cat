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

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
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
    try:
        fields = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    if not isinstance(fields, dict):
        return {}
    identifier = fields.get("id")
    title = fields.get("title")
    return {
        "id": str(identifier).strip() if identifier is not None else None,
        "title": str(title).strip() if title is not None else None,
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


class AuditError(Exception):
    """A git command the audit depends on failed — report, never pass clean."""


def run_git_checked(root: Path, *args: str) -> str:
    result = run_git(root, *args)
    if result.returncode != 0:
        raise AuditError(
            f"git {' '.join(args)} failed (exit {result.returncode}): "
            f"{result.stderr.strip()[:200]}"
        )
    return result.stdout


def read_blobs(root: Path, oids: set[str]) -> dict[str, str]:
    """Read every blob in one ``git cat-file --batch`` process.

    A ``git show`` per file per ref forks a subprocess per record; a
    store spanning many refs never finishes that way (the same lesson
    backlog-py learned). Requesting object ids keeps the request stream
    free of any path bytes.
    """
    if not oids:
        return {}
    stdin = "".join(f"{oid}\n" for oid in sorted(oids)).encode("ascii")
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=root,
        input=stdin,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AuditError(f"git cat-file --batch failed: {result.stderr[:200]}")
    contents: dict[str, str] = {}
    output = result.stdout
    offset = 0
    while offset < len(output):
        end_of_header = output.find(b"\n", offset)
        if end_of_header == -1:
            break
        header = output[offset:end_of_header].decode("ascii", "replace").split()
        if len(header) < 3 or header[1] != "blob":
            break
        oid = header[0]
        size = int(header[2])
        body_start = end_of_header + 1
        contents[oid] = output[body_start : body_start + size].decode(
            "utf-8", "replace"
        )
        offset = body_start + size + 1
    return contents


def git_records(root: Path) -> list[dict[str, Any]]:
    """Read every record on every branch and remote ref."""
    items: list[dict[str, Any]] = []
    refs = run_git_checked(
        root, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes"
    )
    entries: list[tuple[str, str, str]] = []  # (ref, path, blob oid)
    oids: set[str] = set()
    for ref in refs.splitlines():
        if ref.endswith("/HEAD"):
            continue
        listing = run_git_checked(root, "ls-tree", "-r", ref, "--", "backlog")
        for line in listing.splitlines():
            # Default format: "<mode> <type> <oid>\t<path>".
            _meta, _kind, rest = line.split(" ", 2)
            oid, _, relpath = rest.partition("\t")
            entries.append((ref, relpath, oid))
            oids.add(oid)
    sources = read_blobs(root, oids)
    for ref, relpath, oid in entries:
        meta = parse_frontmatter(sources.get(oid, ""))
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


def _has_head(root: Path) -> bool:
    head = run_git(root, "rev-parse", "--verify", "HEAD")
    return head.returncode == 0


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
        if seed.returncode != 0 and _has_head(root):
            raise AuditError(
                f"git read-tree HEAD failed (exit {seed.returncode}): "
                f"{seed.stderr.decode('utf-8', 'replace')[:200]}"
            )
        refresh = subprocess.run(
            ["git", "add", "-A", "--", "backlog"],
            cwd=root,
            capture_output=True,
            env=env,
            check=False,
        )
        if refresh.returncode != 0:
            raise AuditError(
                f"git add failed (exit {refresh.returncode}): "
                f"{refresh.stderr.decode('utf-8', 'replace')[:200]}"
            )
        tree = subprocess.run(
            ["git", "write-tree"],
            cwd=root,
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        if tree.returncode != 0:
            raise AuditError(
                f"git write-tree failed (exit {tree.returncode}): {tree.stderr[:200]}"
            )
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
            raise AuditError(
                f"git commit-tree failed (exit {commit.returncode}): "
                f"{commit.stderr[:200]}"
            )
        return commit.stdout.strip()
    finally:
        index.unlink(missing_ok=True)


def merged_tree_ids(root: Path, tree: str) -> dict[str, list[str]]:
    """Map every ID in a merged tree to the paths carrying it.

    One batched read of the merged tree, shared by every ID verdict —
    merging per ID would re-run the same git merge-tree per pair.
    """
    listing = run_git_checked(root, "ls-tree", "-r", tree, "--", "backlog")
    oids: set[str] = set()
    entries: list[tuple[str, str]] = []
    for line in listing.splitlines():
        # Default format: "<mode> <type> <oid>\t<path>".
        _meta, _kind, rest = line.split(" ", 2)
        oid, _, relpath = rest.partition("\t")
        entries.append((relpath, oid))
        oids.add(oid)
    sources = read_blobs(root, oids)
    ids: dict[str, list[str]] = defaultdict(list)
    for relpath, oid in entries:
        meta = parse_frontmatter(sources.get(oid, ""))
        identifier = meta.get("id")
        if identifier is not None:
            ids[identifier].append(relpath)
    return ids


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

    # Merge each ref pair ONCE and read each merged tree once; every ID
    # verdict comes from that shared scan.
    refs_with_ids: dict[str, set[str]] = defaultdict(set)
    for item in items:
        refs_with_ids[item["branch"]].add(item["id"])
    ordered_refs = sorted(refs_with_ids)
    pair_scans: dict[tuple[str, str], dict[str, list[str]] | None] = {}
    for index, left in enumerate(ordered_refs):
        for right in ordered_refs[index + 1 :]:
            pair_scans[(left, right)] = None  # lazily merged below

    def scan(left: str, right: str) -> dict[str, list[str]] | None:
        """IDs to paths in git's merge of the pair; None = unrelated."""
        key = (left, right) if left < right else (right, left)
        if key not in pair_scans:
            return None
        if pair_scans[key] is None:
            if unrelated_refs(root, key[0], key[1]):
                pair_scans[key] = None
                return None
            merge = run_git(root, "merge-tree", "--write-tree", key[0], key[1])
            if merge.returncode not in (0, 1) or not merge.stdout.strip():
                raise AuditError(
                    f"git merge-tree {key[0]} {key[1]} failed "
                    f"(exit {merge.returncode}): {merge.stderr[:200]}"
                )
            tree = merge.stdout.splitlines()[0]
            pair_scans[key] = merged_tree_ids(root, tree)
        return pair_scans[key]

    for identifier, recs in by_id.items():
        refs = {item["branch"] for item in recs}
        if len(refs) < 2:
            continue
        titles = sorted({item["title"] for item in recs if item["title"] is not None})
        ordered = sorted(refs)
        collided = False
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                ids_map = scan(left, right)
                if ids_map is None:
                    # No merge possible (unrelated refs or no shared
                    # history): the ID reuse can never be reconciled.
                    collided = True
                    break
                if len(ids_map.get(identifier, [])) >= 2:
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
    try:
        if not args.refs:
            items = checkout_records(root)
            problems = collisions(items) + duplicate_ids(items)
            print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
            return int(bool(problems))

        committed = git_records(root)
        # No commits yet: the working tree is the whole audit — only
        # within-checkout duplicates can exist, and there is no ref to
        # merge against. This is the one genuinely optional state.
        if not _has_head(root):
            items = checkout_records(root)
            problems = duplicate_ids(items)
            print(json.dumps({"records": len(items), "collisions": problems}, indent=2))
            return int(bool(problems))
        working = working_tree_commit(root)
        if working is None:
            raise AuditError("working-state commit could not be built")
        items: list[dict[str, Any]] = list(committed)
        # The working state participates as its own ref (the throwaway commit)
        # for records the checked-out branch does not already carry — new or
        # edited-but-uncommitted records join; unchanged ones are already
        # represented by the checked-out ref.
        checked_out = run_git(root, "branch", "--show-current").stdout.strip() or None
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
    except AuditError as error:
        # A lint gate must never pass clean because a git call failed.
        print(
            json.dumps({"records": 0, "collisions": [], "error": str(error)}, indent=2),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
