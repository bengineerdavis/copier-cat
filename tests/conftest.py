"""Shared fixtures: real git-backed copier templates for adopt tests.

Adopt renders through copier itself, so the fixtures build real
templates — a git repo with a copier.yml, the answers-file jinja
convention, and content files — rather than mocking the render.
"""

import subprocess
from pathlib import Path

import pytest

TEMPLATE_FILES = {
    "copier.yml": "project_name:\n  type: str\n  default: demo\n",
    "{{ _copier_conf.answers_file }}.jinja": (
        "# Changes here will be overwritten by Copier\n"
        "{{ _copier_answers|to_nice_yaml }}\n"
    ),
    "README.md.jinja": "# {{ project_name }}\n",
    "mise.toml.jinja": '[tools]\npython = "{{ project_name }}"\n',
    "extra.toml.jinja": '[template]\nkey = "value"\n',
    "notes.txt.jinja": "template note\n",
}


def git_template(root: Path, files: dict[str, str]) -> Path:
    """Build a real git-backed copier template with one commit."""
    for rel, text in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", "."], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "template",
        ],
        cwd=root,
        check=True,
    )
    return root


@pytest.fixture
def template(tmp_path: Path) -> Path:
    """A git-backed template rendering add/identical/merge/conflict shapes."""
    return git_template(tmp_path / "tpl", TEMPLATE_FILES)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """An existing project: identical, mergeable, and conflicting twins
    of the render's files, plus a project-only file adopt must not touch."""
    root = tmp_path / "project"
    root.mkdir()
    (root / "mise.toml").write_text('[tools]\npython = "demo"\n')
    (root / "extra.toml").write_text('[project]\nown = "keep"\n')
    (root / "notes.txt").write_text("project note\n")
    (root / "keep.txt").write_text("project only\n")
    return root
