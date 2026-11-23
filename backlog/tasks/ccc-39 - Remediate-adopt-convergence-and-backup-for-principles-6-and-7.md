---
id: CCC-39
title: Remediate adopt convergence and backup for principles 6 and 7
status: To Do
created_date: 2026-11-23 06:53
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Decision-10 (principles 6 and 7) makes two measured adopt behaviors spec gaps, recorded in review 746: (1) repeating an identical adopt run re-renders, re-merges, and re-stamps — two identical runs against a conflicted project produced nested conflict markers instead of converging; (2) adopt overwrites project content — accepted conflicts, binary replacements, and answers-file stamping — without a restorable backup taken before the write. This task owns the implementation remediation and its own regression tests (review 753 scope), RECONCILED with accepted decision-11: adopt stamps once, then REFUSES a second stamp and points at upgrade. Refusal-with-pointer IS the convergence principle 6 requires — same inputs, same refusal, zero state change — so the remediation is a second-stamp guard, not reconciliation. Backup-before-overwrite remains: the first stamp must still take a restorable backup before overwriting project content. Self-contained by design: this task never depends on unfinished CCC-35 to verify its own work. CCC-35 owns the remaining cross-operation coverage (partial-failure resumability, repeated-run final verification) and depends on this task and CCC-40.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A second identical adopt run against an unchanged stamped project converges per decision-13 (refusal-with-pointer; implements decision-11's stamp-once rule): it refuses the second stamp, changes nothing, and points at upgrade — never nested conflict markers or duplicated effects
- [ ] #2 Adopt takes a restorable backup before overwriting project content (accepted conflicts, binary replacements, answers-file stamping) and can restore it
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
