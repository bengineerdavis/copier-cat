"""The marked-section merger: template-owned regions, parameterized markers.

The marker pair below is the agentic-project-template prototype's — used
here as a fixture. cc ships no default markers (spec C1: no cc residue).
"""

from copier_cat.merge.marked_section import MarkedSectionMerger, Markers
from copier_cat.merge.registry import Registry
from copier_cat.merge.toml_merger import TomlMerger

APT_MARKERS = Markers(
    begin="<!-- BEGIN managed: agentic-project-template -->",
    end="<!-- END managed: agentic-project-template -->",
)


def render(section: str) -> str:
    return f"{APT_MARKERS.begin}\n{section}\n{APT_MARKERS.end}\n"


def test_region_replaces_matching_project_region_byte_for_byte() -> None:
    ours = "# Title\n\nIntro.\n\n" + render("v1") + "\nOutro.\n"
    theirs = render("v2")
    result = MarkedSectionMerger(APT_MARKERS).merge("README.md", "", ours, theirs)
    assert not result.conflicted
    assert "v2" in result.text and "v1" not in result.text
    assert "# Title" in result.text and "Intro." in result.text
    assert "Outro." in result.text
    assert result.text.count(APT_MARKERS.begin) == 1


def test_region_inserts_when_project_file_lacks_it() -> None:
    ours = "# Title\n\nBody.\n"
    theirs = render("section v1")
    result = MarkedSectionMerger(APT_MARKERS).merge("README.md", "", ours, theirs)
    assert not result.conflicted
    assert "section v1" in result.text
    assert result.text.count(APT_MARKERS.begin) == 1
    # The template's region is appended; project content stands.
    assert result.text.startswith("# Title")


def test_project_region_missing_from_render_is_kept_with_warning() -> None:
    # The template no longer renders the region; the project's copy is
    # kept and the divergence is surfaced, not silently resolved.
    ours = "# Title\n\n" + render("kept section") + "\n"
    theirs = "fresh content\n"
    result = MarkedSectionMerger(APT_MARKERS).merge("README.md", "", ours, theirs)
    assert result.conflicted  # the render's other content contradicts ours
    assert any("kept marked region" in w for w in result.warnings)
    assert "kept section" in result.text
    assert "fresh content" in result.text


def test_accepts_when_only_the_project_carries_markers() -> None:
    assert MarkedSectionMerger(APT_MARKERS).accepts(
        "README.md", "", render("x"), "# no markers in the render\n"
    )


def test_declines_when_neither_side_carries_markers() -> None:
    assert not MarkedSectionMerger(APT_MARKERS).accepts(
        "README.md", "", "# ours\n", "# theirs\n"
    )


def test_non_region_divergence_conflicts_and_is_never_silently_resolved() -> None:
    ours = "body v1\n\n" + render("section v1")
    theirs = "body v2\n\n" + render("section v2")
    result = MarkedSectionMerger(APT_MARKERS).merge("README.md", "", ours, theirs)
    assert result.conflicted
    assert "<<<<<<<" in result.text
    # The region itself was resolved deterministically even amid the conflict.
    assert "section v2" in result.text and "section v1" not in result.text


def test_two_regions_splice_independently() -> None:
    ours = "intro\n\n" + render("first v1") + "\n\nmiddle\n"
    theirs = render("first v2") + "\n" + render("second v1")
    result = MarkedSectionMerger(APT_MARKERS).merge("README.md", "", ours, theirs)
    assert not result.conflicted
    assert "first v2" in result.text and "first v1" not in result.text
    assert "second v1" in result.text
    assert "middle" in result.text


def test_declines_when_render_carries_no_markers() -> None:
    assert not MarkedSectionMerger(APT_MARKERS).accepts(
        "README.md", "", "# project text\n", "# template text\n"
    )


def test_declines_non_empty_base() -> None:
    assert not MarkedSectionMerger(APT_MARKERS).accepts(
        "README.md", "base\n", "ours\n", render("x")
    )


def test_composes_as_another_registry_merger() -> None:
    """Provider-open interface: a marked-region provider is just a merger."""
    registry = Registry(mergers=(TomlMerger(), MarkedSectionMerger(APT_MARKERS)))
    result = registry.merge("README.md", "", "# ours\n", render("section"))
    assert result.merger == "marked-section"
    assert "section" in result.text
