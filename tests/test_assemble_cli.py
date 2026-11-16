"""Real CLI acceptance tests for the Python-only named-stack assembly slice."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from conftest import git_template
from typer.testing import CliRunner

from copier_cat.cli import app

runner = CliRunner()


def json_payload(result) -> dict:
    """Read the CLI's separate stdout stream, not its human diagnostics."""
    return json.loads(result.stdout_bytes.decode())


@pytest.fixture
def destination(tmp_path: Path) -> Path:
    return tmp_path / "example-project"


@pytest.fixture
def python_template(tmp_path: Path) -> Path:
    return git_template(
        tmp_path / "python-template",
        {
            "copier.yml": (
                "project_name:\n"
                "  type: str\n"
                "  label: Project name\n"
                "  help: Human-readable project name\n"
                "  default: Example project\n"
                "package_name:\n"
                "  type: str\n"
                "  label: Python package\n"
                "  default: example_package\n"
            ),
            "{{ _copier_conf.answers_file }}.jinja": (
                "# Changes here will be overwritten by Copier\n"
                "{{ _copier_answers|to_nice_yaml }}\n"
            ),
            "README.md.jinja": "# {{ project_name }}\n",
            "pyproject.toml.jinja": (
                '[project]\nname = "{{ package_name }}"\nversion = "0.1.0"\n'
                'dependencies = []\n\n[dependency-groups]\ndev = ["pytest>=8"]\n'
            ),
            "tests/test_project.py.jinja": (
                "from pathlib import Path\n\n"
                "def test_project_readme():\n"
                "    assert Path('README.md').is_file()\n"
            ),
            "src/{{ package_name }}/__init__.py": '"""Example package."""\n',
        },
    )


@pytest.fixture
def catalog(tmp_path: Path, python_template: Path) -> Path:
    path = tmp_path / "catalog.yml"
    path.write_text(
        "templates:\n"
        "  python:\n"
        "    role: base\n"
        f"    source: {python_template}\n"
        "    answers:\n"
        "      package_name: example_package\n"
        "stacks:\n"
        "  python:\n"
        "    templates: [python]\n"
        "  agentic-python:\n"
        "    templates: [python, agentic]\n"
        "  missing:\n"
        "    templates: [missing]\n",
        encoding="utf-8",
    )
    return path


def invoke(catalog: Path, destination: Path, *extra: str, input: str | None = None):
    return runner.invoke(
        app,
        [
            "assemble",
            str(destination),
            "--stack",
            "python",
            "--catalog",
            str(catalog),
            *extra,
        ],
        input=input,
    )


def test_json_preview_is_real_read_only_render_and_native_update(
    catalog: Path, destination: Path
):
    result = invoke(catalog, destination, "--json")
    assert result.exit_code == 0, result.output + result.stderr
    payload = json_payload(result)
    assert payload["status"] == "preview"
    assert payload["destination"] == str(destination)
    assert payload["approved_write"] is None
    assert "native Copier update succeeded" in payload["validation"]
    assert "generated project tests passed" in payload["validation"]
    assert not destination.exists()
    assert payload["preview"] is None
    assert payload["preview_cleanup"] == "automatic"


def test_dry_run_without_yes_preserves_destination_name(catalog: Path, tmp_path: Path):
    destination = tmp_path / "example-project-with-a-long-name"
    result = invoke(catalog, destination, "--dry-run")
    assert result.exit_code == 0, result.output + result.stderr
    assert str(destination) in result.output
    assert not destination.exists()


def test_yes_writes_only_displayed_destination_with_native_evidence(
    catalog: Path, destination: Path
):
    result = invoke(catalog, destination, "--yes", "--json")
    assert result.exit_code == 0, result.output + result.stderr
    assert json_payload(result)["approved_write"] == str(destination)
    assert (destination / "README.md").read_text() == "# Example project\n"
    record = yaml.safe_load((destination / ".copier-answers.yml").read_text())
    assert record["_src_path"]
    assert record["_commit"]
    assert record["package_name"] == "example_package"
    provenance = yaml.safe_load((destination / ".copier-cat-stack.yml").read_text())
    assert provenance["stack"] == "python"
    assert provenance["templates"][0]["role"] == "base"
    update = subprocess.run(
        [
            sys.executable,
            "-m",
            "copier",
            "update",
            "-a",
            ".copier-answers.yml",
            "--defaults",
            "--skip-tasks",
        ],
        cwd=destination,
        capture_output=True,
        text=True,
        check=False,
    )
    assert update.returncode == 0, update.stdout + update.stderr
    clean = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=destination,
        capture_output=True,
        text=True,
        check=True,
    )
    assert clean.stdout == ""


def test_catalog_ref_selects_the_recorded_template_version(
    catalog: Path, python_template: Path, destination: Path
):
    first = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=python_template,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    (python_template / "README.md.jinja").write_text("# New version\n")
    subprocess.run(["git", "add", "-A"], cwd=python_template, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "new template version",
        ],
        cwd=python_template,
        check=True,
    )
    # A cloned Git source honors the selected historical ref; Copier's local
    # directory rendering deliberately includes current working-tree content.
    subprocess.run(
        [
            "git",
            "clone",
            "-q",
            str(python_template),
            str(python_template.parent / "clone"),
        ],
        check=True,
    )
    clone = python_template.parent / "clone"
    catalog.write_text(
        catalog.read_text().replace(
            f"source: {python_template}", f"source: git+{clone}\n    ref: {first}"
        )
    )
    result = invoke(catalog, destination, "--yes", "--json")
    assert result.exit_code == 0, result.output + result.stderr
    assert (destination / "README.md").read_text() == "# Example project\n"
    record = yaml.safe_load((destination / ".copier-answers.yml").read_text())
    assert record["_commit"] == first[:7]


def test_interactive_guided_questions_and_cancellation_leave_no_destination(
    catalog: Path, destination: Path
):
    result = invoke(catalog, destination, "--guided", input="\n\n\nn\n")
    assert result.exit_code == 0, result.output + result.stderr
    assert "Project name" in result.output
    assert "Human-readable project name" in result.output
    assert "Cancelled" in result.output
    assert not destination.exists()


def test_noninteractive_missing_required_answer_fails_clearly(
    tmp_path: Path, destination: Path
):
    template = git_template(
        tmp_path / "required",
        {
            "copier.yml": "project_name:\n  type: str\n  label: Project name\n",
            "README.md.jinja": "# {{ project_name }}\n",
            "{{ _copier_conf.answers_file }}.jinja": (
                "{{ _copier_answers|to_nice_yaml }}\n"
            ),
        },
    )
    catalog = tmp_path / "catalog.yml"
    catalog.write_text(
        f"templates:\n  python:\n    source: {template}\n"
        "stacks:\n  python:\n    templates: [python]\n"
    )
    result = invoke(catalog, destination, "--json")
    assert result.exit_code == 2
    payload = json_payload(result)
    assert payload["stage"] == "answers"
    assert "project_name" in payload["error"]
    assert not destination.exists()


def test_retained_preview_reports_cleanup(catalog: Path, destination: Path):
    result = invoke(catalog, destination, "--retain-preview", "--json")
    assert result.exit_code == 0, result.output + result.stderr
    payload = json_payload(result)
    preview = Path(payload["preview"])
    assert preview.is_dir()
    assert (preview / "README.md").is_file()
    assert not destination.exists()
    assert payload["preview_cleanup"].startswith("rm -rf ")


def test_existing_destination_is_never_overwritten(catalog: Path, destination: Path):
    destination.mkdir()
    marker = destination / "keep.txt"
    marker.write_text("keep\n")
    result = invoke(catalog, destination, "--yes", "--json")
    assert result.exit_code == 2
    assert json_payload(result)["stage"] == "approval"
    assert marker.read_text() == "keep\n"
    assert not (destination / ".copier-answers.yml").exists()


def test_generated_test_failure_is_not_success(
    catalog: Path, python_template: Path, destination: Path
):
    (python_template / "tests/test_project.py.jinja").write_text(
        "def test_failure():\n    assert False\n"
    )
    subprocess.run(["git", "add", "-A"], cwd=python_template, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "failing test",
        ],
        cwd=python_template,
        check=True,
    )
    result = invoke(catalog, destination, "--json")
    assert result.exit_code == 1
    payload = json_payload(result)
    assert payload["stage"] == "validation"
    assert "generated project tests failed" in payload["error"]
    assert not destination.exists()


def test_catalog_and_template_errors_are_structured(catalog: Path, destination: Path):
    unknown = runner.invoke(
        app,
        [
            "assemble",
            str(destination),
            "--stack",
            "unknown",
            "--catalog",
            str(catalog),
            "--json",
        ],
    )
    assert unknown.exit_code == 2
    assert json.loads(unknown.output)["stage"] == "catalog"
    multi = runner.invoke(
        app,
        [
            "assemble",
            str(destination),
            "--stack",
            "agentic-python",
            "--catalog",
            str(catalog),
            "--json",
        ],
    )
    assert multi.exit_code == 2
    assert "multi-template" in json.loads(multi.output)["error"]


def test_stack_inspection_uses_template_metadata(catalog: Path):
    listed = runner.invoke(app, ["stack", "list", "--catalog", str(catalog)])
    assert listed.exit_code == 0
    assert "python" in listed.output
    shown = runner.invoke(app, ["stack", "show", "python", "--catalog", str(catalog)])
    assert shown.exit_code == 0, shown.output + shown.stderr
    assert "Project name" in shown.output
    assert "Human-readable project name" in shown.output
