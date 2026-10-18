"""The CLI contract: stable commands, exit codes, JSON output (spec C5)."""

import json

import pytest
from typer.testing import CliRunner

from copier_cat.cli import app

runner = CliRunner()


@pytest.fixture
def sides(tmp_path):
    ours = tmp_path / "project.toml"
    theirs = tmp_path / "render.toml"
    base = tmp_path / "base.toml"
    return ours, theirs, base


def test_merge_clean_exit_0_and_json(sides) -> None:
    ours, theirs, _ = sides
    ours.write_text('[tools]\npython = "3.13"\n', encoding="utf-8")
    theirs.write_text('[tools]\nroborev = "latest"\n', encoding="utf-8")
    result = runner.invoke(
        app, ["merge", "--ours", str(ours), "--theirs", str(theirs), "--json"]
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["merger"] == "toml"
    assert payload["conflicted"] is False
    assert payload["warnings"] == []
    assert "python" in payload["text"] and "roborev" in payload["text"]


def test_merge_conflicted_exit_1(tmp_path) -> None:
    ours = tmp_path / "project.txt"
    theirs = tmp_path / "render.txt"
    ours.write_text("ours line\n", encoding="utf-8")
    theirs.write_text("theirs line\n", encoding="utf-8")
    result = runner.invoke(
        app, ["merge", "--ours", str(ours), "--theirs", str(theirs), "--json"]
    )
    # A format no merger accepts falls to git merge-file: an add/add
    # conflict surfaced for review (decision-2).
    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["conflicted"] is True
    assert payload["merger"] == "git-merge-file"
    assert "<<<<<<<" in payload["text"]


def test_merge_kept_value_warns_on_stderr_in_human_mode(sides) -> None:
    ours, theirs, _ = sides
    ours.write_text('[tools]\npython = "3.13"\n', encoding="utf-8")
    theirs.write_text('[tools]\npython = "3.12"\n', encoding="utf-8")
    result = runner.invoke(app, ["merge", "--ours", str(ours), "--theirs", str(theirs)])
    assert result.exit_code == 0
    assert "warning:" in result.stderr
    assert "python" in result.stderr


def test_merge_output_file_writes_merged_text(sides, tmp_path) -> None:
    ours, theirs, _ = sides
    ours.write_text("[a]\nx = 1\n", encoding="utf-8")
    theirs.write_text("[a]\ny = 2\n", encoding="utf-8")
    out = tmp_path / "merged.toml"
    result = runner.invoke(
        app,
        ["merge", "--ours", str(ours), "--theirs", str(theirs), "--output", str(out)],
    )
    assert result.exit_code == 0
    assert "x = 1" in out.read_text(encoding="utf-8")
    assert "y = 2" in out.read_text(encoding="utf-8")


def test_merge_with_explicit_base_reaches_the_fallback(sides) -> None:
    ours, theirs, base = sides
    base.write_text("[a]\nx = 0\n\nz = 9\n", encoding="utf-8")
    ours.write_text("[a]\nx = 1\n\nz = 9\n", encoding="utf-8")
    theirs.write_text("[a]\nx = 0\n\ny = 2\nz = 9\n", encoding="utf-8")
    result = runner.invoke(
        app,
        [
            "merge",
            "--ours",
            str(ours),
            "--theirs",
            str(theirs),
            "--base",
            str(base),
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["merger"] == "git-merge-file"
    assert payload["conflicted"] is False
    assert "y = 2" in payload["text"]


def test_merge_path_key_routes_selection(sides, tmp_path) -> None:
    ours = tmp_path / "project.txt"
    theirs = tmp_path / "render.txt"
    ours.write_text("k = 1\n", encoding="utf-8")
    theirs.write_text("k = 2\n", encoding="utf-8")
    result = runner.invoke(
        app,
        [
            "merge",
            "--ours",
            str(ours),
            "--theirs",
            str(theirs),
            "--path",
            "mise.toml",
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["merger"] == "toml"
    assert payload["path"] == "mise.toml"


def test_merge_missing_input_is_exit_2(sides, tmp_path) -> None:
    _, theirs, _ = sides
    result = runner.invoke(
        app, ["merge", "--ours", str(tmp_path / "nope"), "--theirs", str(theirs)]
    )
    assert result.exit_code == 2
    assert "error:" in result.stderr


def test_mergers_lists_registry_json() -> None:
    result = runner.invoke(app, ["mergers", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload == {"mergers": ["toml", "yaml"], "fallback": "git-merge-file"}


def test_mergers_human_output() -> None:
    result = runner.invoke(app, ["mergers"])
    assert result.exit_code == 0
    assert "toml" in result.output and "fallback: git-merge-file" in result.output
