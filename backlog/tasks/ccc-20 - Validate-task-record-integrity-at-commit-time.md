---
id: CCC-20
title: Validate task-record integrity at commit time
status: To Do
created_date: 2026-11-14 18:54
updated_date: 2026-11-14 18:56
references:
- ../agentic-project-template/backlog/tasks/apt-49 - Adopt-upstream-conformant-workflow-feedback-in-stamped-projects.md
- backlog/tasks/ccc-21 - Make-contribution-candidates-follow-upstream-contributor-conventions.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The copier-cat CCC migration produced completed-task files with duplicate IDs because renaming the directory did not reliably stage or detect the old-ID deletions. The parent agentic template stamps the backlog workflow and commit harness used by copier-cat, so the missing mechanical guard belongs upstream.

Ship:

- Reconciliation of the copier-cat failure and the parent template’s existing commit harness, producing a scoped agentic-layer feedback task for a deterministic backlog task-record integrity check.
- A validation design covering filename/frontmatter ID agreement, duplicate IDs, resolvable dependencies, and path/status consistency, using the installed backlog-py diagnostics as evidence rather than assuming they cover these invariants.
- A reviewable handoff linking the upstream task to the concrete copier-cat migration evidence and the template tests that should fail before the guard is implemented.

Constraints:

- Reconcile current parent-template work before creating the task; preserve other sessions’ edits, worktrees, and unpushed commits.
- Keep this upstream of the copier-cat assembly MVP.
- Prefer the existing harness and a deterministic check; do not add a new workflow framework or silently change Git operations.
- Do not claim that backlog-py doctor covers an invariant without testing it against the installed version.
- Any new skill introduced by implementation must be declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: send the backlog integrity lesson to the parent agentic template so stamped projects inherit it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Reconciliation identifies the parent template’s current harness, established work, and a scoped agentic-layer feedback task
- [ ] #2 The integrity design covers ID/filename agreement, duplicates, resolvable dependencies, and path/status consistency with installed-tool evidence
- [ ] #3 A reviewable handoff links copier-cat migration evidence to upstream task and red-first template tests
- [ ] #4 backlog-py board shows CCC-20 with its full description and acceptance criteria
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
