"""Pure document merging shared by the TOML and YAML mergers.

Ported from the agentic-project-template prototype's merge engine
(agentic_project_template/merge.py) with semantics unchanged. Every merge
is pure, idempotent, and base-wins: the overlay fills gaps, it does not
overwrite choices the base already made. In the registry's adopt frame the
project document is the base (its choices win) and the template document
is the overlay (it fills gaps).
"""

from __future__ import annotations

from typing import Any


def deep_merge(base: dict, overlay: dict) -> tuple[dict, list[str]]:
    """Merge overlay into base; base wins on conflicts, gaps are filled.

    Lists of dicts that carry a `name` key merge by name (dotagents
    [[skills]]/[[mcp]], prek repos). Other lists: base's entries are kept
    and overlay's unseen entries are appended. Returns (merged, warnings);
    each warning names a kept base value the overlay tried to change.
    """
    warnings: list[str] = []
    merged = dict(base)

    for key, incoming in overlay.items():
        if key not in merged:
            merged[key] = incoming
            continue
        existing = merged[key]
        if isinstance(existing, dict) and isinstance(incoming, dict):
            merged[key], sub = deep_merge(existing, incoming)
            warnings.extend(sub)
        elif _is_named_list(existing) and _is_named_list(incoming):
            merged[key] = _merge_named_lists(existing, incoming)
        elif isinstance(existing, list) and isinstance(incoming, list):
            merged[key] = existing + [item for item in incoming if item not in existing]
        elif existing != incoming:
            warnings.append(f"kept existing value for {key!r}: {existing!r}")
    return merged, warnings


def _is_named_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, dict) and "name" in item for item in value)
    )


def _merge_named_lists(base: list, overlay: list) -> list:
    by_name = {item["name"]: dict(item) for item in base}
    for item in overlay:
        if item["name"] in by_name:
            continue
        by_name[item["name"]] = dict(item)
    return list(by_name.values())
