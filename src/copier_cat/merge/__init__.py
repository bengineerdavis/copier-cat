"""The merger registry library (spec C1/C5).

A stable, tested API usable independently of any CLI (PRINCIPLES
constraint). The git-merge-driver shape and the empty-base adopt contract
are decision-1 and decision-2 in backlog/decisions/.
"""

from .fallback import GitMergeFileMerger, MergeToolError, git_merge_file
from .marked_section import MarkedSectionMerger, Markers
from .registry import Registry, default_registry
from .struct_merge import deep_merge
from .toml_merger import TomlMerger
from .types import Merger, MergeResult
from .yaml_merger import YamlMerger

__all__ = [
    "GitMergeFileMerger",
    "MarkedSectionMerger",
    "Markers",
    "MergeResult",
    "MergeToolError",
    "Merger",
    "Registry",
    "TomlMerger",
    "YamlMerger",
    "deep_merge",
    "default_registry",
    "git_merge_file",
]
