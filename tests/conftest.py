"""Shared fixtures: real git-backed copier templates for adopt tests.

Adopt renders through copier itself, so the fixtures build real
templates — a git repo with a copier.yml, the answers-file jinja
convention, and content files — rather than mocking the render.
"""

import subprocess
from collections.abc import Mapping
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


def git_template(root: Path, files: Mapping[str, str | bytes]) -> Path:
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
    files: dict[str, str | bytes] = dict(TEMPLATE_FILES)
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
def jinja_answers_template(tmp_path: Path) -> Path:
    """A template whose _answers_file is jinja'd under custom envops
    (copier-template-copier-template's shape)."""
    return git_template(
        tmp_path / "tpl-jinja-answers",
        {
            "copier.yml": (
                "_answers_file: .copier-answers.<< project_name >>.yml\n"
                "_envops:\n"
                "  block_end_string: '%>'\n"
                "  block_start_string: '<%'\n"
                "  variable_end_string: '>>'\n"
                "  variable_start_string: '<<'\n"
                "_templates_suffix: .tmpl\n"
                "project_name:\n  type: str\n  default: demo\n"
            ),
            "<< _copier_conf.answers_file >>.tmpl": (
                "# Changes here will be overwritten by Copier\n"
                "<< _copier_answers|to_nice_yaml >>\n"
            ),
            "README.md.tmpl": "# << project_name >>\n",
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


@pytest.fixture(autouse=True)
def _isolate_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Keep every test's writes out of the shared worktree.

    Tests that run a failing CLI (or a CLI with a path bug) must not drop
    generated projects into the repository checkout. A traversal-shaped input
    once did exactly that.
    """
    monkeypatch.chdir(tmp_path)
    yield


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
            "mise.toml.jinja": '[tools]\npython = "3.12"\n',
            ".gitignore": ".python-version\n.shared-cache/\n",
        },
    )
