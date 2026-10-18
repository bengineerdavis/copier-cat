"""Registry behavior: selection, fast paths, base pass-through."""

from copier_cat.merge.marked_section import MarkedSectionMerger, Markers
from copier_cat.merge.registry import Registry, default_registry
from copier_cat.merge.toml_merger import TomlMerger

APT_MARKERS = Markers(
    begin="<!-- BEGIN managed: agentic-project-template -->",
    end="<!-- END managed: agentic-project-template -->",
)


def test_default_registry_composition() -> None:
    registry = default_registry()
    assert [m.name for m in registry.mergers] == ["toml", "yaml"]
    assert registry.fallback.name == "git-merge-file"


def test_empty_project_file_takes_the_template_render() -> None:
    registry = default_registry()
    result = registry.merge("anything.txt", "", "", "template content\n")
    assert result.text == "template content\n"
    assert not result.conflicted


def test_empty_render_leaves_project_content_standing() -> None:
    registry = default_registry()
    result = registry.merge("anything.txt", "", "project content\n", "")
    assert result.text == "project content\n"
    assert not result.conflicted


def test_base_is_passed_through_unchanged() -> None:
    """The registry never invents a base; adopt passes the empty tree."""
    registry = default_registry()
    # Non-empty base on a .toml path: the TOML merger declines, the
    # fallback resolves it — proving the base reached merger selection.
    result = registry.merge("a.toml", "[k]\nv = 1\n", "[k]\nv = 2\n", "[k]\nv = 3\n")
    assert result.merger == "git-merge-file"
    assert result.conflicted


def test_non_empty_base_with_empty_side_reaches_the_fallback() -> None:
    """An empty side against a non-empty base is modify/delete-style
    divergence — surfaced as a conflict, never silently resurrected."""
    registry = default_registry()
    deleted_ours = registry.merge("a.toml", "[k]\nv = 1\n", "", "[k]\nv = 3\n")
    assert deleted_ours.conflicted
    assert deleted_ours.merger == "git-merge-file"
    dropped_theirs = registry.merge("a.toml", "[k]\nv = 1\n", "[k]\nv = 2\n", "")
    assert dropped_theirs.conflicted
    assert dropped_theirs.merger == "git-merge-file"


def test_marked_section_merger_joins_via_composition_not_default() -> None:
    registry = Registry(mergers=(TomlMerger(), MarkedSectionMerger(APT_MARKERS)))
    render = f"{APT_MARKERS.begin}\nsection\n{APT_MARKERS.end}\n"
    result = registry.merge("README.md", "", "# ours\n", render)
    assert result.merger == "marked-section"


def test_result_carries_the_merger_name() -> None:
    result = default_registry().merge("mise.toml", "", "k = 1\n", "j = 2\n")
    assert result.merger == "toml"
