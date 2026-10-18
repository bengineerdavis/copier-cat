---
id: CC-1
title: Extract the merger registry from the agentic-project-template prototype
status: In Progress
created_date: 2026-10-16 21:06
updated_date: 2026-10-18 02:33
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Port the merge engine behind the git-merge-driver-shaped registry per backlog/decisions/decision-1 (TOML deep-merge, YAML, marked sections; git merge-file fallback).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Registry of git-merge-driver-shaped mergers: each merger receives base/ours/theirs texts and returns merged text, a conflicted flag, and warnings (decision-1)
- [ ] #2 TOML merger ports the prototype deep-merge: project values win conflicts, template fills gaps, named lists merge by name, plain lists union without duplicates, kept values surface as warnings, idempotent
- [ ] #3 YAML merger with the same deep-merge semantics
- [ ] #4 Marked-section merger: marker pair is a constructor parameter (no cc marker convention), template-owned regions replace matching regions byte-for-byte or insert when absent, non-region divergence surfaces as a conflict, provider-open for CC-2
- [ ] #5 git merge-file fallback for formats no merger accepts; format mergers decline unparseable input and non-empty merge bases so the fallback takes over
- [ ] #6 The merge base is caller-supplied — adopt passes the empty tree (decision-2); the registry never invents one
- [ ] #7 Stable public library API exported from copier_cat.merge, usable independently of any CLI (PRINCIPLES constraint; spec C5)
- [ ] #8 CLI exposes the same operations: copier-cat merge and copier-cat mergers, stable exit codes (0 clean, 1 conflicted, 2 error), JSON output (spec C5)
- [ ] #9 Test suite covers ported prototype semantics plus registry selection, fallback, and the CLI contract; mise run lint and mise run test pass
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Format mergers decline a non-empty merge base (git merge-file takes over): cc's registry fires only at adopt time where the base is the empty tree (decision-2), and updates run through copier's own machinery, so a structure-aware three-way with non-empty base is deliberately not built here.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
