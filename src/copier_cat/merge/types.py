"""Core types for the merger registry (decision-1).

Every merger is shaped like a git merge driver: it receives the three
merge inputs (base, ours, theirs) as text and produces the merged text.
Adopt supplies an empty tree as the base (decision-2), so template files
arrive as fresh additions resolved against the project's current content;
the registry itself never invents a base.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class MergeResult:
    """Outcome of one file-level merge.

    `text` carries the merged content; when `conflicted` is True it
    contains conflict markers the per-file review flow resolves. Warnings
    report deterministic choices the merger made (kept project values,
    preserved regions) — the review signal for add/add-style merges.
    `merger` names the registry member that produced the result (empty
    for the registry's fast paths).
    """

    text: str
    conflicted: bool
    warnings: tuple[str, ...] = field(default=())
    merger: str = ""


class Merger(Protocol):
    """A git-merge-driver-shaped structure-aware merger.

    `accepts` decides whether the merger can handle a merge: it receives
    the target path (for format selection) and all three inputs (for
    content checks such as parseability). A merger that declines hands
    the merge to the next one, ultimately the registry's fallback.
    """

    name: str

    def accepts(self, path: str, base: str, ours: str, theirs: str) -> bool: ...

    def merge(self, path: str, base: str, ours: str, theirs: str) -> MergeResult: ...
