"""The git merge-file fallback: format-blind three-way merge."""

import subprocess

import pytest

from copier_cat.merge.fallback import GitMergeFileMerger, MergeToolError, git_merge_file


def test_clean_three_way_merge() -> None:
    # Edits on adjacent lines conflict in git (xdiff adjacency), so the
    # two sides' changes are separated by unchanged lines.
    base = "a\nb\nc\nd\ne\nf\n"
    ours = "a\nOURS\nc\nd\ne\nf\n"
    theirs = "a\nb\nc\nd\nTHEIRS\nf\n"
    text, conflicted = git_merge_file(base, ours, theirs)
    assert not conflicted
    assert "OURS" in text and "THEIRS" in text


def test_conflict_produces_markers() -> None:
    text, conflicted = git_merge_file("", "ours line\n", "theirs line\n")
    assert conflicted
    assert "<<<<<<<" in text and ">>>>>>>" in text and "=======" in text


def test_labels_appear_in_markers() -> None:
    text, _ = git_merge_file("", "a\n", "b\n", labels=("base", "project", "render"))
    assert "<<<<<<< project" in text
    assert ">>>>>>> render" in text


def test_empty_theirs_leaves_ours_standing() -> None:
    text, conflicted = git_merge_file("", "ours content\n", "")
    assert not conflicted
    assert text == "ours content\n"


def test_identical_additions_merge_clean() -> None:
    text, conflicted = git_merge_file("", "same\n", "same\n")
    assert not conflicted
    assert text.strip() == "same"


def test_fallback_merger_accepts_everything_and_reports_name() -> None:
    merger = GitMergeFileMerger()
    assert merger.accepts("anything.bin", "", "a\n", "b\n")
    result = merger.merge("notes.md", "", "a\n", "b\n")
    assert result.conflicted
    assert "<<<<<<< ours" in result.text


def test_missing_git_binary_raises_merge_tool_error(monkeypatch) -> None:
    def boom(*args, **kwargs):
        raise FileNotFoundError("git not found")

    monkeypatch.setattr(subprocess, "run", boom)
    with pytest.raises(MergeToolError, match="could not run"):
        git_merge_file("", "a\n", "b\n")


def test_exit_code_above_conflict_range_raises_merge_tool_error(monkeypatch) -> None:
    # Conflict counts truncate at 127; beyond that the tool failed.
    proc = subprocess.CompletedProcess(
        args=[], returncode=200, stdout="", stderr="boom"
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: proc)
    with pytest.raises(MergeToolError, match="failed"):
        git_merge_file("", "a\n", "b\n")
