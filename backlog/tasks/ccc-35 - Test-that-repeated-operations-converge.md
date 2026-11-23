---
id: CCC-35
title: Test that repeated operations converge
status: To Do
created_date: 2026-11-22 17:09
updated_date: 2026-11-22 17:10
dependencies:
- CCC-39
- CCC-40
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PRINCIPLES.md principle 6 (decision-10) requires that repeating an operation with unchanged inputs converges on the same state without duplicating effects. Merger-level coverage already exists on main: tests/test_mergers.py test_toml_merge_is_idempotent performs a second merge and asserts identical output with no warnings — this task does not duplicate that coverage. Scope after review 753: the per-operation remediation and its own regression tests live with the owning tasks — CCC-39 (adopt convergence + restorable backup) and CCC-40 (assembly convergence). This task owns the REMAINING cross-operation coverage: partial-failure resumability (an interrupted operation leaves the project resumable rather than half-applied) and the repeated-conflict scenario as final verification of both remediated behaviors. Dependencies: CCC-39 and CCC-40 land first; this task's repeated-run assertions verify remediated behavior, never pin current defects. Constraints: test behavior at public seams, not implementation details; do not assert tautologies. Keep the tests independent of the unfinished CCC-25 branch. Verified 2026-11-22: 94 tests pass on main; the only idempotency coverage is the merger-level test named above.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A second identical adopt run is a no-op or produces only new work
- [ ] #2 Re-running a validated composition does not duplicate contributions
- [ ] #3 Partial failure leaves the operation resumable rather than half-applied
- [ ] #4 uv run pytest -q passes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Derives from decision-10 (idempotent operations and non-destructive change). Pairs with CCC-34, which gives principle 7 its reset requirements home.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
