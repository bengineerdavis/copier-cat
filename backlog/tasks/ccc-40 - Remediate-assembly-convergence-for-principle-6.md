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
Decision-10 (principles 6 and 7) records a measured assembly gap: repeated assembly against an existing destination fails without a clean convergence story. This task owns the implementation AND its own regression tests (review 753 scope), RECONCILED with accepted decision-11 item 2: the new-project surface (assemble today, copy after CCC-37) REFUSES an existing destination and points at adopt. Refusal-with-pointer IS the convergence principle 6 requires — same inputs, same refusal, zero state change — so the remediation is making the refusal explicit, machine-readable, and upgrade/adopt-pointing, never a bare error and never a silent write into the existing tree. The first-run path is untouched: it already converges (isolated preview, approval-gated write). Self-contained by design: this task never depends on unfinished CCC-35 to verify its own work. CCC-35 owns the remaining cross-operation coverage (partial-failure resumability, repeated-scenario final verification) and runs after this task and CCC-39.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A second identical assemble run against an existing destination converges per decision-11: it refuses before any write with an explicit, machine-readable pointer to adopt — never a bare error, never a write into the existing tree
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
