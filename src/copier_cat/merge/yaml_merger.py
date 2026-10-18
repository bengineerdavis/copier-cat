"""YAML merger: structure-aware deep-merge behind the driver shape.

Same contract as the TOML merger (empty base only; project wins, template
fills gaps) over YAML documents parsed with safe_load. Only mapping
documents merge; sequences or scalars at the document root decline to the
fallback. Re-serialization with safe_dump drops comments and formatting,
and can also reflow quoted strings — deterministic, not byte-preserving.
"""

from __future__ import annotations

from typing import Any

import yaml

from .struct_merge import deep_merge
from .types import MergeResult


class YamlMerger:
    name = "yaml"

    def accepts(self, path: str, base: str, ours: str, theirs: str) -> bool:
        if path.rsplit(".", 1)[-1].lower() not in ("yml", "yaml"):
            return False
        if base.strip():
            return False
        for text in (ours, theirs):
            if text.strip() and not isinstance(self._parse(text), dict):
                return False
        return True

    def merge(self, path: str, base: str, ours: str, theirs: str) -> MergeResult:
        ours_doc = self._parse(ours) or {}
        theirs_doc = self._parse(theirs) or {}
        merged, warnings = deep_merge(ours_doc, theirs_doc)
        return MergeResult(
            text=yaml.safe_dump(merged, sort_keys=False),
            conflicted=False,
            warnings=tuple(warnings),
        )

    def _parse(self, text: str) -> dict[str, Any] | None:
        """Parse YAML text; None when empty, unparseable, or not a mapping."""
        if not text.strip():
            return None
        try:
            doc = yaml.safe_load(text)
        except yaml.YAMLError:
            return None
        return doc if isinstance(doc, dict) else None
