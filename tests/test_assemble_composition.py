"""CLI acceptance tests for independently rendered template composition."""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import yaml
from conftest import git_template
from typer.testing import CliRunner

from copier_cat.cli import app

runner = CliRunner()


def answers_record(name: str) -> tuple[str, str]:
    return (
        name,
        "# Changes here will be overwritten by Copier\n"
        "{{ _copier_answers|to_nice_yaml }}\n",
    )


@pytest.fixture
def agentic_template(tmp_path: Path) -> Path:
    return git_template(
        tmp_path / "agentic-template",
        {
            "copier.yml": (
                "_answers_file: .agentic-answers.yml\n"
                "project_name:\n  type: str\n  default: Example project\n"
                "task_prefix:\n  type: str\n  default: demo\n"
            ),
            **dict([answers_record("{{ _copier_conf.answers_file }}.jinja")]),
            "AGENTS.md.jinja": (
                "# {{ project_name }}\nUse backlog prefix {{ task_prefix }}.\n"
            ),
            "mise.toml.jinja": '[tasks]\ncheck = "echo agentic"\n',
            ".gitignore": ".agents/\n.python-version\n.shared-cache/\n",
            "agents.toml.jinja": '[[skills]]\nname = "backlog-workflow"\n',
        },
    )


@pytest.fixture
def composed_catalog(
    tmp_path: Path, python_template: Path, agentic_template: Path
) -> Path:
    path = tmp_path / "composed-catalog.yml"
    path.write_text(
        "templates:\n"
        "  python:\n"
        "    role: base\n"
        f"    source: {python_template}\n"
        "    answers:\n      package_name: example_package\n"
        "  agentic:\n"
        "    role: overlay\n"
        "    capabilities: [agent-guidance, backlog-workflow]\n"
        f"    source: {agentic_template}\n"
        "stacks:\n"
        "  agentic-python:\n    templates: [python, agentic]\n"
        "  agentic-alone:\n    templates: [agentic]\n",
        encoding="utf-8",
    )
    return path


def assemble(
    catalog: Path, destination: Path, *extra: str, stack: str = "agentic-python"
):
    return runner.invoke(
        app,
        [
            "assemble",
            str(destination),
            "--stack",
            stack,
            "--catalog",
            str(catalog),
            *extra,
        ],
    )


def test_agentic_overlay_composes_and_updates_independently(
    composed_catalog: Path, destination: Path
):
    result = assemble(composed_catalog, destination, "--yes", "--json")
    assert result.exit_code == 0, result.output + result.stderr
    payload = json.loads(result.stdout_bytes)
    assert (destination / "README.md").read_text() == "# Example project\n"
    assert "Use backlog prefix demo." in (destination / "AGENTS.md").read_text()
    assert (destination / "agents.toml").is_file()
    config = tomllib.loads((destination / "mise.toml").read_text())
    assert config["tasks"]["check"] == "echo agentic"
    assert (destination / ".gitignore").read_text().splitlines() == [
        ".python-version",
        ".shared-cache/",
        ".agents/",
    ]
    subprocess.run(["git", "init", "-q", "."], cwd=destination, check=True)
    subprocess.run(["git", "add", "-A"], cwd=destination, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "composed project",
        ],
        cwd=destination,
        check=True,
    )
    for answers_file in [".copier-answers.yml", ".agentic-answers.yml"]:
        record = yaml.safe_load((destination / answers_file).read_text())
        assert record["_src_path"]
        update = subprocess.run(
            [
                sys.executable,
                "-m",
                "copier",
                "update",
                "--defaults",
                "--skip-tasks",
                "-a",
                answers_file,
            ],
            cwd=destination,
            capture_output=True,
            text=True,
            check=False,
        )
        assert update.returncode == 0, update.stdout + update.stderr
    assert len(payload["native_updates"]) == 2
    assert all(
        f"native Copier update succeeded: {name}" in payload["validation"]
        for name in ["python", "agentic"]
    )
    provenance = yaml.safe_load((destination / ".copier-cat-stack.yml").read_text())
    assert provenance["templates"][1]["capabilities"] == [
        "agent-guidance",
        "backlog-workflow",
    ]


def test_overlay_can_compose_without_python(composed_catalog: Path, destination: Path):
    result = assemble(
        composed_catalog, destination, "--yes", "--json", stack="agentic-alone"
    )
    assert result.exit_code == 0, result.output + result.stderr
    assert (destination / "AGENTS.md").is_file()
    assert not (destination / "pyproject.toml").exists()


def test_unsupported_shared_format_fails_without_destination(
    composed_catalog: Path, agentic_template: Path, destination: Path
):
    (agentic_template / "README.md.jinja").write_text("# Overlay version\n")
    subprocess.run(["git", "add", "-A"], cwd=agentic_template, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "shared markdown",
        ],
        cwd=agentic_template,
        check=True,
    )
    result = assemble(composed_catalog, destination, "--json")
    assert result.exit_code == 2
    payload = json.loads(result.stdout_bytes)
    assert payload["stage"] == "composition"
    assert "unsupported shared file README.md" in payload["error"]
    assert not destination.exists()


def test_identical_shared_text_is_not_silently_selected(
    composed_catalog: Path, agentic_template: Path, destination: Path
):
    (agentic_template / "README.md.jinja").write_text("# Example project\n")
    subprocess.run(["git", "add", "-A"], cwd=agentic_template, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "identical shared markdown",
        ],
        cwd=agentic_template,
        check=True,
    )
    result = assemble(composed_catalog, destination, "--json")
    assert result.exit_code == 2
    assert (
        "not concatenated or silently selected"
        in json.loads(result.stdout_bytes)["error"]
    )


def test_same_key_toml_collision_keeps_base_and_reports_warning(
    composed_catalog: Path, agentic_template: Path, destination: Path
):
    (agentic_template / "mise.toml.jinja").write_text(
        '[tools]\npython = "different"\n[tasks]\ncheck = "echo agentic"\n'
    )
    subprocess.run(["git", "add", "-A"], cwd=agentic_template, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "toml collision",
        ],
        cwd=agentic_template,
        check=True,
    )
    result = assemble(composed_catalog, destination, "--yes", "--json")
    assert result.exit_code == 0, result.output + result.stderr
    config = tomllib.loads((destination / "mise.toml").read_text())
    assert config["tools"]["python"] == "3.12"
    assert config["tasks"]["check"] == "echo agentic"


def test_overlay_requires_capabilities_without_python_dependency(
    composed_catalog: Path, destination: Path
):
    composed_catalog.write_text(
        composed_catalog.read_text().replace(
            "capabilities: [agent-guidance, backlog-workflow]", "capabilities: []"
        )
    )
    result = assemble(composed_catalog, destination, "--json")
    assert result.exit_code == 2
    assert "must declare capabilities" in json.loads(result.stdout_bytes)["error"]
    assert not destination.exists()


def test_composition_cleanup_does_not_retain_isolated_member_renders(
    composed_catalog: Path, destination: Path
):
    result = assemble(composed_catalog, destination, "--retain-preview", "--json")
    assert result.exit_code == 0, result.output + result.stderr
    payload = json.loads(result.stdout_bytes)
    preview = Path(payload["preview"])
    assert (preview / ".agentic-answers.yml").is_file()
    assert not list(preview.glob("render-*"))
    assert not destination.exists()
