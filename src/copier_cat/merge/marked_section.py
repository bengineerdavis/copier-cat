"""Marked-section merger: template-owned regions inside a shared text file.

A marked region (GLOSSARY) is a named, byte-stable section inside a
generated file that the template owns. The marker pair is a constructor
parameter, not a cc convention: this merger only acts on files that
already carry markers, and cc ships no default markers (spec C1 — no cc
residue). Flows compose an instance configured for the template in play;
copier-uv-bleeding's mechanism would enter the same way (CC-2).

Semantics over an empty base (decision-2), ported from the prototype's
upsert behavior:

- the non-region content merges through `git merge-file` (divergent
  project/template text surfaces as conflict markers, never silently
  resolved);
- each region in the template render replaces the matching project
  region byte-for-byte, or is inserted when the project file lacks it;
- project regions the template no longer renders are kept, with a
  warning — the review flow decides.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .fallback import git_merge_file
from .types import MergeResult


@dataclass(frozen=True)
class Markers:
    """A literal begin/end marker pair identifying a template-owned region."""

    begin: str
    end: str


@dataclass(frozen=True)
class _Region:
    """One region block as it appears in the file, plus its identity."""

    begin_marker: str
    block: str  # the full matched text, begin..end, without a trailing newline


def _parse_regions(text: str, markers: Markers) -> list[_Region]:
    pattern = re.compile(
        re.escape(markers.begin) + r".*?" + re.escape(markers.end), re.DOTALL
    )
    return [_Region(markers.begin, match.group(0)) for match in pattern.finditer(text)]


class MarkedSectionMerger:
    name = "marked-section"

    def __init__(self, markers: Markers) -> None:
        self._markers = markers

    def accepts(self, path: str, base: str, ours: str, theirs: str) -> bool:
        if base.strip():
            return False
        # Either side carrying complete marker pairs makes this a
        # region-managed file: the render's regions splice in, and
        # project regions the render dropped are kept with a warning.
        return bool(
            _parse_regions(theirs, self._markers) or _parse_regions(ours, self._markers)
        )

    def merge(self, path: str, base: str, ours: str, theirs: str) -> MergeResult:
        regions = _parse_regions(theirs, self._markers)
        theirs_rest = _strip_regions(theirs, regions)
        warnings: list[str] = []
        # Ours' regions flow through the inner merge untouched (they are
        # ours-only lines), then get replaced below.
        text, conflicted = git_merge_file(base, ours, theirs_rest)

        ours_regions = _parse_regions(text, self._markers)
        theirs_begins = {region.begin_marker for region in regions}
        for region in regions:
            text = _splice_region(text, region, ours_regions)
        kept = [r for r in ours_regions if r.begin_marker not in theirs_begins]
        for region in kept:
            warnings.append(
                f"kept marked region {region.begin_marker!r}: not in the template render"
            )
        return MergeResult(text=text, conflicted=conflicted, warnings=tuple(warnings))


def _strip_regions(text: str, regions: list[_Region]) -> str:
    """Remove region blocks from the render, leaving the non-region content.

    A block carries its trailing newline (the template writes
    `begin\\nbody\\nend\\n`); removing the block alone would leave a
    stray blank line the inner merge would treat as content. A render
    that is only regions therefore strips to an empty string.
    """
    for region in regions:
        with_newline = region.block + "\n"
        if with_newline in text:
            text = text.replace(with_newline, "", 1)
        else:
            text = text.replace(region.block, "", 1)
    return text if text.strip() else ""


def _splice_region(text: str, region: _Region, ours_regions: list[_Region]) -> str:
    """Replace the matching project region byte-for-byte, or insert the block."""
    for ours_region in ours_regions:
        if (
            ours_region.begin_marker == region.begin_marker
            and ours_region.block in text
        ):
            return text.replace(ours_region.block, region.block, 1)
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + region.block + "\n"
