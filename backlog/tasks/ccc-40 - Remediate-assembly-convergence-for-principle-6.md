---
id: CCC-40
title: Remediate assembly convergence for principle 6
status: To Do
created_date: 2026-11-23 07:06
dependencies:
- CCC-39
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Decision-10 (principles 6 and 7) records a measured assembly gap: repeated assembly against an existing destination is refused outright rather than converging or pointing at the right operation. Refusal is a safe default but not convergence — principle 6 requires that repeating an operation with unchanged inputs converge on the same state without duplicating effects. This task owns the implementation AND its own regression tests (review 753 scope): a second identical assembly run against an existing destination either no-ops with a clear pointer to adopt/upgrade, or performs a reviewed reconciliation — never bare refusal and never duplicated contributions — with tests landing WITH this task. Self-contained by design: this task never depends on unfinished CCC-35 to verify its own work. CCC-35 owns the remaining cross-operation coverage (partial-failure resumability, repeated-scenario final verification) and runs after this task and CCC-39.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A second identical assemble run against an existing destination converges: reports a no-op with a pointer to the right operation, or performs a reviewed reconciliation — never a bare refusal
- [ ] #2 The convergence path never duplicates contributions or writes outside the displayed destination
- [ ] #3 uv run pytest -q passes with this task's own regression tests asserting remediated behavior
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
