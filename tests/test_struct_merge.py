"""Pure deep-merge semantics, ported from the agentic-project-template
prototype's test suite (tests/test_merge.py)."""

from copier_cat.merge.struct_merge import deep_merge


def test_deep_merge_fills_gaps_and_keeps_base() -> None:
    base = {"tools": {"python": "3.13", "uv": "latest"}, "tasks": {}}
    overlay = {"tools": {"roborev": "latest", "python": "3.12"}}
    merged, warnings = deep_merge(base, overlay)
    assert merged["tools"]["python"] == "3.13"
    assert merged["tools"]["uv"] == "latest"
    assert merged["tools"]["roborev"] == "latest"
    assert any("python" in w for w in warnings)


def test_deep_merge_named_lists_by_name() -> None:
    base = {"skills": [{"name": "a", "source": "x/a"}]}
    overlay = {
        "skills": [{"name": "a", "source": "OTHER"}, {"name": "b", "source": "x/b"}]
    }
    merged, _ = deep_merge(base, overlay)
    assert {s["name"] for s in merged["skills"]} == {"a", "b"}
    assert merged["skills"][0]["source"] == "x/a"


def test_deep_merge_allows_toml_types() -> None:
    merged, _ = deep_merge({"a": 1}, {"b": [1, 2], "c": {"d": True}})
    assert merged["a"] == 1 and merged["b"] == [1, 2] and merged["c"]["d"] is True


def test_deep_merge_unions_plain_lists_without_duplicates() -> None:
    base = {"deps": ["ruff", "pytest"]}
    overlay = {"deps": ["pytest", "copier"]}
    merged, _ = deep_merge(base, overlay)
    assert merged["deps"] == ["ruff", "pytest", "copier"]


def test_deep_merge_equal_values_warn_nothing() -> None:
    merged, warnings = deep_merge({"a": 1, "b": {"c": 2}}, {"a": 1, "b": {"c": 2}})
    assert merged == {"a": 1, "b": {"c": 2}}
    assert warnings == []
