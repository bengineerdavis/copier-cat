---
id: CCC-38
title: Prove the no-lock-in boundary on dummy projects
status: To Do
created_date: 2026-11-22 21:25
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Maintainer requirement 2026-11-22 (Q11-Q15): the promises in docs/copier-cat-vs-copier.md must be demonstrated, not asserted, and the maintainer wants to try dummy projects while the agent observes, giving feedback from outcomes and from them directly. Ship: observable scenarios under the approved scratch area covering the whole no-lock-in table, each recording commands, output, exit status, before/after file hashes, diffs, native answers files, and native update results. Must include: a stack applied to an existing project, then extended or modified with ccc, then ccc removed, proving every stamped template still updates through plain copier update -a; the timing distinction that extending a stack AFTER ccc removal is a manual per-template Copier workflow; unchanged inputs with clean and locally modified projects; changed versions, answers, ordering, composition rules; mutable refs whose contents moved; interruption after only some members applied; duplicate runs; backup and restore; unsupported conflicts; nested projects, subdirectories, worktrees, and ambiguous discovery; human, scripted JSON, and agent-driven paths. Constraints: a couple of equality checks are explicitly insufficient per the maintainer. Cover the lost-capability rows too (no new stack extension discovery, no whole-stack composition reproduction, no atomic resume, no member removal) so the docs never over-promise. Bring in relevant ask-matt tasks for this build-out as the maintainer directed. Numbered 38 to avoid the id collision with the idempotency branch.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
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
