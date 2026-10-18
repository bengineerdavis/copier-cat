"""TOML merger: structure-aware deep-merge behind the driver shape.

Runs only on an empty merge base — the adopt-time shape (decision-2). A
non-empty base means genuinely divergent edits, which the format-blind
`git merge-file` fallback resolves instead (declined here, accepted
there). With the empty base, the project document wins conflicts and the
template document fills gaps: the prototype's base-wins deep-merge
(struct_merge.deep_merge).

Limitation carried from the prototype: the merged document is
re-serialized, so comments and formatting from either side do not
survive. Deterministic, not byte-preserving.
"""

from __future__ import annotations

import tomllib

import tomli_w

from .struct_merge import deep_merge
from .types import MergeResult


class TomlMerger:
    name = "toml"

    def accepts(self, path: str, base: str, ours: str, theirs: str) -> bool:
        if not path.endswith(".toml"):
            return False
        if base.strip():
            return False
        for text in (ours, theirs):
            if text.strip() and not isinstance(self._parse(text), dict):
                return False
        return True

    def merge(self, path: str, base: str, ours: str, theirs: str) -> MergeResult:
        ours_doc = self._parse(ours)
        theirs_doc = self._parse(theirs)
        merged, warnings = deep_merge(ours_doc or {}, theirs_doc or {})
        return MergeResult(
            text=tomli_w.dumps(merged),
            conflicted=False,
            warnings=tuple(warnings),
        )

    def _parse(self, text: str) -> dict | None:
        """Parse TOML text; None when empty or unparseable."""
        if not text.strip():
            return None
        try:
            return tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            return None
