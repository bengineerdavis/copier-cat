---
id: CCC-42
title: Stop assembling a tool-authored git commit into new projects
status: To Do
created_date: 2026-11-23 08:17
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
ccc assemble violates the no-commit consent contract: the assembly pipeline runs git init, git add -A, and a commit inside the isolated preview, then shutil.copytree copies the preview INCLUDING the .git directory into the approved destination — an ordinary ccc assemble --yes leaves a tool-authored 'Initial generated project' commit in the new project. Committing is always the user's action per the stack protocol's consent contract. Fix: either strip .git from the destination copy, or never commit inside the preview (keep the preview a plain directory and preserve the user's own git workflow). The preview commit currently exists to give copier a merge baseline for native-update validation; if the commit is removed, _check_native_update must create its baseline inside its own disposable copy instead of the shared preview.
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
