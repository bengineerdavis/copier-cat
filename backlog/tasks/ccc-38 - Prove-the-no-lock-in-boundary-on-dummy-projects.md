---
id: CCC-38
title: Prove the no-lock-in boundary on dummy projects
status: To Do
created_date: 2026-11-22 21:25
updated_date: 2026-11-22 23:38
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
2026-11-22 partial lifecycle evidence (not task completion): on feature/ccc-25-evidence, public CLI scenarios prove base stack application, single-template adopt extension with reviewed .gitignore conflict, removal of the project-local stack artifact, real tagged v1.1.0 upgrades for both templates using plain copier update, and repeated no-op updates. Project-owned.txt survives and Git ends clean. Full suite 105 passed; Ruff and pyrefly clean. Retained scenario: /home/bdavis/.cache/tmp/opencode/ccc-user-tests/lifecycle/test_extended_stack_native_upd0/example-project. Boundary: after each real version upgrade, commit or stash the changed answers/output before updating the next member; Copier refuses dirty Git trees. The current extension path uses single-template adopt, not adopt --stack. Full application-state updates after extension, stack discovery, atomic resume, backup/restore, and the remaining CCC-38 matrix are still unimplemented or unproven.
Durable evidence: DOC-13, Prove the no-lock-in lifecycle on dummy projects. It replaces the temporary scratch checkout with the reproducible public test test_extended_stack_native_updates_survive_stack_artifact_removal. The maintainer directly observed both plain Copier updates report Keeping template version 1.1.0 and leave git status empty. After committing the changes and rerunning the checks, the ccc-user-tests scratch directory was removed. Collision reconciliation: scripts/audit_backlog.py --refs checked 769 local/remote records with zero collisions; tests include a deliberately colliding two-branch fixture.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
