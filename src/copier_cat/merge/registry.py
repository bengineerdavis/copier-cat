"""The merger registry (decision-1): ordered mergers with a fallback.

Selection is content- and path-aware: the first merger whose `accepts`
returns True takes the merge; when none do, the git merge-file fallback
does. The registry never invents a merge base — adopt supplies the empty
tree (decision-2) and callers pass it through.

Two registry-level fast paths keep "fresh addition" merges trivial and
identical for every format: an empty project file takes the template
render; an empty render leaves the project file standing.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from .fallback import GitMergeFileMerger
from .toml_merger import TomlMerger
from .types import Merger, MergeResult
from .yaml_merger import YamlMerger


@dataclass(frozen=True)
class Registry:
    mergers: tuple[Merger, ...] = ()
    fallback: Merger = field(default_factory=GitMergeFileMerger)

    def merger_for(self, path: str, base: str, ours: str, theirs: str) -> Merger:
        for merger in self.mergers:
            if merger.accepts(path, base, ours, theirs):
                return merger
        return self.fallback

    def merge(self, path: str, base: str, ours: str, theirs: str) -> MergeResult:
        # Fast paths fire only on the adopt shape (empty base). With a
        # non-empty base, an empty side means a modify/delete-style
        # divergence that must reach merger selection and the fallback —
        # not a silent resurrection of one side.
        empty_base = not base.strip()
        if empty_base and not ours.strip():
            return MergeResult(text=theirs, conflicted=False)
        if empty_base and not theirs.strip():
            return MergeResult(text=ours, conflicted=False)
        merger = self.merger_for(path, base, ours, theirs)
        return replace(merger.merge(path, base, ours, theirs), merger=merger.name)


def default_registry() -> Registry:
    """The shipped registry: format mergers plus the git merge-file fallback.

    No marked-section merger by default — markers are a template-side
    convention cc does not impose (spec C1). Flows that adopt a template
    using marked regions compose one:

        Registry(
            mergers=(TomlMerger(), YamlMerger(), MarkedSectionMerger(markers)),
            fallback=GitMergeFileMerger(),
        )
    """
    return Registry(mergers=(TomlMerger(), YamlMerger()))
