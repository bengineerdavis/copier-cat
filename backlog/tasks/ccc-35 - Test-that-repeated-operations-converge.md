---
id: CCC-35
title: Test that repeated operations converge
status: To Do
created_date: 2026-11-22 17:09
updated_date: 2026-11-22 17:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PRINCIPLES.md principle 6 (decision-10) requires that repeating an operation with unchanged inputs converges on the same state without duplicating effects. Merger-level coverage already exists on main: tests/test_mergers.py test_toml_merge_is_idempotent performs a second merge and asserts identical output with no warnings — this task does not duplicate that coverage. No test on main asserts idempotent re-runs as a property of the PUBLIC operations (adopt, assemble). The 2026-11-08 prototype demonstrated the failure mode: its walkthrough apply() lacked the free-play hasOverlay guard, so Previous then Run re-applied and produced a duplicate agentic overlay. Measured 2026-11-22 (review 746): repeating an identical `adopt --defaults --accept-all --json` run against a conflicted project produced nested conflict markers rather than converging — re-adopt is the primary uncovered case. Ship: tests at the public seams of adopt and assemble proving that a second identical run is a no-op or produces only new work, and that partial failure leaves the operation resumable rather than half-applied. Cover re-adopt of an already-adopted template (including the repeated-conflict scenario, whose current behavior is the non-convergence defect decision-10 now records) and re-running a validated composition against the existing new-destination guard. Constraints: test behavior at public seams, not implementation details; do not assert tautologies. Keep the tests independent of the unfinished CCC-25 branch. Verified 2026-11-22: 94 tests pass on main; the only idempotency coverage is the merger-level test named above.
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
