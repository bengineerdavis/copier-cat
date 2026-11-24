---
id: CCC-42
title: Stop assembling a tool-authored git commit into new projects
status: To Do
created_date: 2026-11-23 08:17
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Scope narrowed 2026-11-23 (review 793): main's assembly already creates the validation commit only inside _check_native_update's disposable update_root (assemble.py:679-720) and composes the approved destination from the non-Git preview/render (:837-850) — the original description's shared-preview .git leak no longer exists. What remains is locking the guarantee in: no public-CLI test asserts that an approved destination arrives without a .git directory or tool-authored commit, so a future refactor could silently reintroduce the leak. Ship that regression test through the public CLI.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An approved ccc assemble --yes produces a destination with no .git directory and no tool-authored commit
- [ ] #2 Native-update validation still proves a plain copier update succeeds against its own disposable baseline
- [ ] #3 uv run pytest -q passes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
