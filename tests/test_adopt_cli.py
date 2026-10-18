"""The adopt CLI contract: stable exit codes, consent, JSON output (spec C5).

Exit codes match the merge surface: 0 clean, 1 the run presented
conflicts (resolved or not), 2 error — including the refusal to apply
anything without per-file consent in --json mode.
"""

import json

import yaml
from typer.testing import CliRunner

from copier_cat.cli import app

runner = CliRunner()


def invoke(template, project, *extra):
    return runner.invoke(
        app,
        ["adopt", str(template), str(project), "--defaults", *extra],
    )


def test_adopt_accept_all_applies_and_stamps(template, project):
    result = invoke(template, project, "--trust", "--accept-all", "--json")
    # The run presented a conflict (notes.txt add/add) and the user
    # accepted it: exit 1 — resolved or not, conflicts were presented.
    assert result.exit_code == 1
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    assert by_path["README.md"]["classification"] == "add"
    assert by_path["README.md"]["applied"] is True
    assert by_path["mise.toml"]["classification"] == "identical"
    assert by_path["extra.toml"]["classification"] == "merge"
    assert by_path["extra.toml"]["merger"] == "toml"
    assert by_path["notes.txt"]["classification"] == "conflict"
    assert by_path["notes.txt"]["applied"] is True
    # The answers file never appears as a reviewed file: it is the stamp.
    assert ".copier-answers.yml" not in by_path
    # Everything accepted landed in the working tree, conflict markers and all.
    assert (project / "README.md").read_text(encoding="utf-8") == "# demo\n"
    assert "<<<<<<<" in (project / "notes.txt").read_text(encoding="utf-8")
    record = yaml.safe_load(
        (project / ".copier-answers.yml").read_text(encoding="utf-8")
    )
    assert record["project_name"] == "demo"


def test_adopt_accept_all_exit_0_on_a_conflict_free_project(template, project):
    # Without the conflicting twin, every file is add/merge/identical.
    (project / "notes.txt").unlink()
    result = invoke(template, project, "--trust", "--accept-all", "--json")
    assert result.exit_code == 0
    payload = json.loads(result.output)
    classifications = {
        entry["path"]: entry["classification"] for entry in payload["files"]
    }
    assert classifications == {
        "README.md": "add",
        "mise.toml": "identical",
        "extra.toml": "merge",
        "notes.txt": "add",
    }


def test_adopt_reject_all_skips_conflict_but_exit_1(template, project):
    result = invoke(template, project, "--trust", "--reject-all", "--json")
    # The run presented a conflict; rejecting it does not rewrite history.
    assert result.exit_code == 1
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    assert by_path["notes.txt"]["classification"] == "conflict"
    assert by_path["notes.txt"]["applied"] is False
    assert (project / "notes.txt").read_text(encoding="utf-8") == "project note\n"
    assert not (project / "README.md").exists()
    # The stamp is adopt's own record: it lands even on a full rejection.
    assert (project / ".copier-answers.yml").exists()


def test_adopt_json_without_consent_is_exit_2_and_touches_nothing(
    template,
    project,
):
    result = invoke(template, project, "--trust", "--json")
    assert result.exit_code == 2
    assert "--accept-all" in result.stderr
    # Nothing applied, nothing stamped: no consent, no changes.
    assert not (project / "README.md").exists()
    assert not (project / ".copier-answers.yml").exists()
    assert (project / "notes.txt").read_text(encoding="utf-8") == "project note\n"


def test_adopt_interactive_review_consents_per_file(template, project):
    # Reviewable order is path-sorted: README.md, extra.toml, notes.txt.
    result = runner.invoke(
        app,
        [
            "adopt",
            str(template),
            str(project),
            "--defaults",
            "--trust",
        ],
        input="y\nn\nn\n",
    )
    assert result.exit_code == 1  # conflict presented, rejected
    assert (project / "README.md").read_text(encoding="utf-8") == "# demo\n"
    assert (project / "extra.toml").read_text(encoding="utf-8") == (
        '[project]\nown = "keep"\n'
    )
    assert (project / "notes.txt").read_text(encoding="utf-8") == "project note\n"


def test_adopt_missing_dst_is_exit_2(template, tmp_path):
    result = runner.invoke(
        app,
        [
            "adopt",
            str(template),
            str(tmp_path / "nope"),
            "--defaults",
            "--accept-all",
        ],
    )
    assert result.exit_code == 2
    assert "existing project directory" in result.stderr


def test_adopt_bad_answers_option_is_exit_2(template, project):
    result = runner.invoke(
        app,
        [
            "adopt",
            str(template),
            str(project),
            "--defaults",
            "-a",
            "not-a-pair",
            "--accept-all",
        ],
    )
    assert result.exit_code == 2
    assert "QUESTION=ANSWER" in result.stderr


def test_adopt_mutually_exclusive_flags_are_exit_2(template, project):
    result = invoke(template, project, "--trust", "--accept-all", "--reject-all")
    assert result.exit_code == 2
    assert "mutually exclusive" in result.stderr


def test_adopt_human_mode_reports_every_file(template, project):
    result = invoke(template, project, "--trust", "--accept-all")
    assert result.exit_code == 1
    lines = result.output.splitlines()
    assert any(line == "add\tREADME.md\tapplied" for line in lines)
    assert any(line == "identical\tmise.toml\tidentical" for line in lines)
    assert any(line == "conflict\tnotes.txt\tapplied" for line in lines)
    assert "stamped: .copier-answers.yml" in lines
