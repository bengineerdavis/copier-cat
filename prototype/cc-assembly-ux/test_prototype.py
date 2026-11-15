"""Smoke checks for the preserved, synthetic assembly UX prototype."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROTOTYPE = Path(__file__).with_name("prototype.py")


def run_prototype(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROTOTYPE), *arguments],
        capture_output=True,
        check=False,
        text=True,
    )


@pytest.mark.parametrize("arguments", [("--help",), ("help",), ("assemble", "--help")])
def test_human_help_is_read_only(arguments: tuple[str, ...]) -> None:
    result = run_prototype(*arguments)

    assert result.returncode == 0
    assert "example-project" in result.stdout
    assert result.stderr == ""


def test_catalog_and_focused_help_share_the_command_contract() -> None:
    catalog_result = run_prototype("help", "--json")
    focused_result = run_prototype("assemble", "--help", "--json")

    assert catalog_result.returncode == 0
    assert focused_result.returncode == 0
    catalog = json.loads(catalog_result.stdout)
    focused = json.loads(focused_result.stdout)
    assert catalog["schema_version"] == 1
    assert catalog["commands"] == [focused]
    assert focused["arguments"][0]["name"] == "destination"
    assert focused["approval_scope"] == "displayed-new-destination-only"


def test_dry_run_preserves_the_named_destination_without_approval() -> None:
    result = run_prototype(
        "assemble",
        "example-project",
        "--stack",
        "example-stack",
        "--dry-run",
    )

    assert result.returncode == 0
    assert "Previewed plan for ./example-project" in result.stdout
    assert "no project writes" in result.stdout


def test_json_alone_is_a_safe_preview() -> None:
    result = run_prototype(
        "assemble",
        "example-project",
        "--stack",
        "example-stack",
        "--json",
    )

    assert result.returncode == 0
    result_json = json.loads(result.stdout)
    assert result_json["status"] == "preview"
    assert result_json["project"] == "example-project"
    assert result_json["stack"] == "example-stack"
    assert result_json["approved"] is False
    assert result_json["destination"] is None
    assert result_json["synthetic"] is True


def test_explicit_approval_is_scoped_to_the_simulated_destination() -> None:
    result = run_prototype(
        "assemble",
        "example-project",
        "--stack",
        "example-stack",
        "--json",
        "--yes",
    )

    assert result.returncode == 0
    result_json = json.loads(result.stdout)
    assert result_json["approved"] is True
    assert result_json["destination"] == "./example-project"
    assert result_json["synthetic"] is True


def test_guided_review_is_not_decorative() -> None:
    result = run_prototype(
        "assemble",
        "example-project",
        "--stack",
        "example-stack",
        "--guided",
        "--json",
        "--yes",
    )

    assert result.returncode == 0
    result_json = json.loads(result.stdout)
    assert result_json["reviews"] == [
        "validate:automatic",
        "resolve",
        "answers",
        "compose",
        "assemble",
    ]


def test_a_typo_fails_without_creating_a_simulated_destination() -> None:
    result = run_prototype("recipie", "--json")

    assert result.returncode == 2
    assert "Did you mean 'stack'?" in result.stderr
    assert "No writes." in result.stderr
    assert result.stdout == ""
