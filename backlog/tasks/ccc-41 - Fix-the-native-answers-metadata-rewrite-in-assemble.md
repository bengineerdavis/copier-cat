---
id: CCC-41
title: Fix the native answers metadata rewrite in assemble
status: To Do
created_date: 2026-11-23 08:17
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The native-answers metadata rewrite in src/copier_cat/assemble.py (~782-809) replaces _src_path and _commit lines as raw text, but Copier's to_nice_yaml auto-quotes unsafe scalars while the raw replacement emits them unquoted. Verified failure modes: a template path containing ': ' produces invalid YAML (assembly exits 2); a path containing ' #' truncates the value as a comment and validation fails with 'native answers source does not match'; non-line-based answers formats raise StopIteration or an empty error. Plain non-git templates are never rewritten. Also a regression: native_answers.read_text runs before the _compose_members stamp fallback, so a valid Git template that renders no answers file now fails. Fix: serialize replacement scalars with YAML, preserve Copier's native layout byte-for-byte, stamp before rewriting when the answers file is absent, and apply the same handling in _check_native_update.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A template source path containing ': ' or ' #' still yields a valid, correct answers file after the metadata rewrite
- [ ] #2 A Git-backed template that renders no answers file still assembles via the stamp fallback
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
