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


def test_adopt_binary_asset_lands_verbatim(binary_template, project):
    # A template shipping a binary asset classifies as an add and lands
    # the render's bytes verbatim: the run never aborts on decoding.
    (project / "notes.txt").unlink()  # conflict-free project: exit 0
    result = invoke(binary_template, project, "--trust", "--accept-all", "--json")
    assert result.exit_code == 0
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    logo = by_path["logo.png"]
    assert logo["classification"] == "add"
    assert logo["applied"] is True
    assert any("binary" in warning for warning in logo["warnings"])
    assert logo["merger"] == ""  # the text merger never ran on binary content
    # Byte-identical to the render: no replacement characters, no corruption.
    assert (project / "logo.png").read_bytes() == bytes(range(256))


def test_adopt_binary_conflict_accept_lands_render_bytes(binary_template, project):
    # A differing binary file is a conflict; accept lands the render's
    # bytes verbatim — the project's bytes are replaced, not merged.
    (project / "logo.png").write_bytes(b"\x00\x01project-bytes")
    (project / "notes.txt").unlink()
    result = invoke(binary_template, project, "--trust", "--accept-all", "--json")
    assert result.exit_code == 1  # a conflict was presented
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    assert by_path["logo.png"]["classification"] == "conflict"
    assert by_path["logo.png"]["applied"] is True
    assert (project / "logo.png").read_bytes() == bytes(range(256))


def test_adopt_binary_conflict_reject_keeps_project_bytes(binary_template, project):
    # Reject keeps the project's bytes untouched.
    (project / "logo.png").write_bytes(b"\x00\x01project-bytes")
    (project / "notes.txt").unlink()
    result = invoke(binary_template, project, "--trust", "--reject-all", "--json")
    assert result.exit_code == 1
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    assert by_path["logo.png"]["applied"] is False
    assert (project / "logo.png").read_bytes() == b"\x00\x01project-bytes"


def test_adopt_binary_identical_classifies_identical(binary_template, project):
    # A project binary matching the render byte-for-byte is identical:
    # nothing to consent to, nothing lands.
    (project / "notes.txt").unlink()
    (project / "logo.png").write_bytes(bytes(range(256)))
    result = invoke(binary_template, project, "--trust", "--accept-all", "--json")
    assert result.exit_code == 0
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    assert by_path["logo.png"]["classification"] == "identical"


def test_adopt_json_implies_defaults_without_the_flag(template, project):
    # --json is non-interactive by construction: unanswered defaultable
    # questions take the template's defaults even without --defaults, so
    # the JSON contract holds without any prompt machinery (spec C5).
    (project / "notes.txt").unlink()  # conflict-free project: exit 0
    result = runner.invoke(
        app,
        ["adopt", str(template), str(project), "--trust", "--accept-all", "--json"],
    )
    # Note: no --defaults on this invocation.
    assert result.exit_code == 0
    payload = json.loads(result.output)
    by_path = {entry["path"]: entry for entry in payload["files"]}
    assert by_path["README.md"]["applied"] is True
    record = yaml.safe_load(
        (project / ".copier-answers.yml").read_text(encoding="utf-8")
    )
    assert record["project_name"] == "demo"


def test_adopt_json_required_question_is_clean_exit_2(required_template, project):
    # --json never prompts, and copier cannot default a required question
    # (no default): the render fails as a clean cc-contract exit-2 error
    # naming the question — never an interleaved prompt on the JSON
    # stream, and never copier's TTY-less session error.
    result = runner.invoke(
        app,
        [
            "adopt",
            str(required_template),
            str(project),
            "--trust",
            "--accept-all",
            "--json",
        ],
    )
    assert result.exit_code == 2
    assert 'Question "project_name" is required' in result.stderr
    # No JSON on the output stream for a failed render: the only content
    # is the error message (the runner mixes stdout and stderr).
    assert "{" not in result.output
    # Nothing landed, nothing stamped: the render never completed.
    assert not (project / "README.md").exists()
    assert not (project / ".copier-answers.yml").exists()
