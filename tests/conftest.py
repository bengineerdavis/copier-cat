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

# A payload that is not valid UTF-8 (NUL bytes and raw 0x80-0xff): the
# binary-asset fixture exercises the classification carve-out for
# content that must never enter the text merger.
BINARY_PAYLOAD = bytes(range(256))


def git_template(root: Path, files: dict[str, str | bytes]) -> Path:
    """Build a real git-backed copier template with one commit."""
    for rel, content in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
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
def binary_template(tmp_path: Path) -> Path:
    """The standard template plus a binary asset (a logo)."""
    files = dict(TEMPLATE_FILES)
    files["logo.png"] = BINARY_PAYLOAD
    return git_template(tmp_path / "tpl-bin", files)


@pytest.fixture
def required_template(tmp_path: Path) -> Path:
    """A template whose only question has no default (required)."""
    return git_template(
        tmp_path / "tpl-required",
        {
            "copier.yml": "project_name:\n  type: str\n",
            "{{ _copier_conf.answers_file }}.jinja": (
                "# Changes here will be overwritten by Copier\n"
                "{{ _copier_answers|to_nice_yaml }}\n"
            ),
            "README.md.jinja": "# {{ project_name }}\n",
        },
    )


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
