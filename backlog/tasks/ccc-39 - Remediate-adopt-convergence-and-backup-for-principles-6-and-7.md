---
id: CCC-39
title: Remediate adopt convergence and backup for principles 6 and 7
status: To Do
created_date: 2026-11-23 06:53
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Decision-10 (principles 6 and 7) makes two measured adopt behaviors spec gaps, recorded in review 746: (1) repeating an identical adopt run does not converge — two identical runs against a conflicted project produced nested conflict markers rather than a no-op or reviewed reconciliation; (2) adopt overwrites project content — accepted conflicts, binary replacements, and answers-file stamping — without a restorable backup taken before the write. This task owns the implementation remediation. CCC-35 owns the regression tests and verifies the remediated behavior; this task must land before CCC-35's repeated-conflict acceptance criterion can pass.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A second identical adopt run against an unchanged project and template converges: no-op, or reviewed reconciliation — never nested conflict markers or duplicated effects
- [ ] #2 Adopt takes a restorable backup before overwriting project content (accepted conflicts, binary replacements, answers-file stamping) and can restore it
- [ ] #3 uv run pytest -q passes with the CCC-35 regression tests asserting remediated behavior
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
