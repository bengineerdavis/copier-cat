"""The TOML and YAML mergers behind the git-merge-driver shape."""

import tomllib

import pytest

from copier_cat.merge.registry import Registry
from copier_cat.merge.toml_merger import TomlMerger
from copier_cat.merge.yaml_merger import YamlMerger

# --- TOML merger (empty base = the adopt-time shape, decision-2) ---------


def test_toml_empty_base_project_wins_template_fills_gaps() -> None:
    ours = '[tools]\npython = "3.13"\n'
    theirs = '[tools]\npython = "3.12"\nroborev = "latest"\n'
    result = TomlMerger().merge("pyproject.toml", "", ours, theirs)
    assert not result.conflicted
    assert 'python = "3.13"' in result.text
    assert 'roborev = "latest"' in result.text
    assert any("python" in w for w in result.warnings)


def test_toml_merge_is_idempotent() -> None:
    ours = '[tools]\npython = "3.13"\n'
    theirs = '[tools]\nroborev = "latest"\n[tasks]\ntest = { run = "pytest" }\n'
    merger = TomlMerger()
    first = merger.merge("mise.toml", "", ours, theirs)
    second = merger.merge("mise.toml", "", first.text, theirs)
    assert not first.conflicted and not second.conflicted
    assert second.text == first.text
    assert second.warnings == ()


def test_toml_named_lists_merge_by_name() -> None:
    ours = '[[agents]]\nname = "a"\nsource = "x/a"\n'
    theirs = '[[agents]]\nname = "a"\nsource = "OTHER"\n\n[[agents]]\nname = "b"\n'
    result = TomlMerger().merge("config.toml", "", ours, theirs)
    doc = tomllib.loads(result.text)
    names = [agent["name"] for agent in doc["agents"]]
    assert names == ["a", "b"]
    assert doc["agents"][0]["source"] == "x/a"


def test_toml_merger_declines_non_empty_base() -> None:
    assert not TomlMerger().accepts(
        "a.toml", "[x]\ny = 1\n", "[x]\ny = 2\n", "[x]\ny = 3\n"
    )


def test_toml_merger_declines_unparseable_project_file() -> None:
    assert not TomlMerger().accepts("a.toml", "", "not [valid toml", "[x]\ny = 1\n")


def test_toml_merger_declines_other_paths() -> None:
    assert not TomlMerger().accepts("a.yaml", "", "[x]\ny = 1\n", "[x]\ny = 1\n")


def test_toml_merger_takes_both_empty_sides() -> None:
    result = TomlMerger().merge("a.toml", "", "", "")
    assert result.text == ""
    assert not result.conflicted


# --- YAML merger ----------------------------------------------------------


def test_yaml_empty_base_project_wins_template_fills_gaps() -> None:
    ours = "tools:\n  python: '3.13'\n"
    theirs = "tools:\n  python: '3.12'\n  roborev: latest\n"
    result = YamlMerger().merge("prek.yml", "", ours, theirs)
    assert not result.conflicted
    assert "python: '3.13'" in result.text
    assert "roborev: latest" in result.text
    assert any("python" in w for w in result.warnings)


def test_yaml_named_lists_merge_by_name() -> None:
    ours = "agents:\n  - name: a\n    source: x/a\n"
    theirs = "agents:\n  - name: b\n"
    result = YamlMerger().merge("agents.yml", "", ours, theirs)
    assert "name: a" in result.text and "name: b" in result.text
    assert "source: x/a" in result.text


def test_yaml_merger_declines_non_mapping_documents() -> None:
    # A bare scalar or a top-level sequence is not a mergeable document.
    assert not YamlMerger().accepts("a.yml", "", "- a\n- b\n", "key: v\n")
    assert not YamlMerger().accepts("a.yml", "", "just a string\n", "key: v\n")


def test_yaml_merger_declines_unparseable_input() -> None:
    assert not YamlMerger().accepts("a.yml", "", "key: [unclosed\n", "key: v\n")


def test_yaml_merger_declines_non_empty_base() -> None:
    assert not YamlMerger().accepts("a.yml", "k: 1\n", "k: 2\n", "k: 3\n")


# --- through the registry -------------------------------------------------


@pytest.mark.parametrize(
    ("path", "ours", "theirs", "expected"),
    [
        ("mise.toml", "k = [1]\n", "k = [2]\n", "toml"),
        ("prek.yaml", "k: [1]\n", "k: [2]\n", "yaml"),
        ("notes.md", "k: [1]\n", "k: [2]\n", "git-merge-file"),
    ],
)
def test_registry_routes_by_path(
    path: str, ours: str, theirs: str, expected: str
) -> None:
    registry = Registry(mergers=(TomlMerger(), YamlMerger()))
    result = registry.merge(path, "", ours, theirs)
    assert result.merger == expected
