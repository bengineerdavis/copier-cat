"""The CLI contract: stable commands, exit codes, JSON output (spec C5)."""

import json

import pytest
from typer.testing import CliRunner

from copier_cat.cli import app

runner = CliRunner()


def test_every_command_documents_its_copier_equivalent() -> None:
    # The graduation principle (spec C6) made enforceable: each command's
    # help carries its copier-native equivalent and exit-code contract.
    # A commit adding a command without its teaching fails here.
    for command in app.registered_commands:
        # Typer leaves .name None when it derives the click name from the
        # callback; the click default is the function name with underscores
        # as dashes.
        assert command.callback is not None
        name = command.name or command.callback.__name__.replace("_", "-")
        result = runner.invoke(app, [name, "--help"])
        assert result.exit_code == 0, name
        assert "Copier equivalent:" in result.output, name
        assert "Exit codes:" in result.output, name


def test_top_level_help_carries_the_graduation_promise() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "leaves you with plain copier" in result.output


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


def test_json_and_output_combine(sides, tmp_path) -> None:
    ours, theirs, _ = sides
    ours.write_text("[a]\nx = 1\n", encoding="utf-8")
    theirs.write_text("[a]\ny = 2\n", encoding="utf-8")
    out = tmp_path / "merged.toml"
    result = runner.invoke(
        app,
        [
            "merge",
            "--ours",
            str(ours),
            "--theirs",
            str(theirs),
            "--output",
            str(out),
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert out.read_text(encoding="utf-8") == payload["text"]


def test_stdout_bytes_match_the_json_text_field(tmp_path) -> None:
    # Inputs without a trailing newline give a merged text without one:
    # the verbatim contract becomes visible.
    ours = tmp_path / "ours.txt"
    theirs = tmp_path / "theirs.txt"
    base = tmp_path / "base.txt"
    base.write_text("a\nb\nc")
    ours.write_text("A\nb\nc")
    theirs.write_text("a\nb\nc")
    plain = runner.invoke(
        app,
        ["merge", "--ours", str(ours), "--theirs", str(theirs), "--base", str(base)],
    )
    as_json = runner.invoke(
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
    assert plain.exit_code == 0
    payload = json.loads(as_json.output)
    assert not payload["text"].endswith("\n")
    assert plain.output == payload["text"]


def test_non_utf8_input_is_a_clean_exit_2(tmp_path) -> None:
    theirs = tmp_path / "render.txt"
    theirs.write_bytes(b"caf\xe9 latte\n")
    ours = tmp_path / "ours.txt"
    ours.write_text("ours\n", encoding="utf-8")
    result = runner.invoke(app, ["merge", "--ours", str(ours), "--theirs", str(theirs)])
    assert result.exit_code == 2
    assert "not valid UTF-8" in result.stderr
    assert "Traceback" not in result.stderr


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
