---
id: CCC-21
title: Make contribution candidates follow upstream contributor conventions
status: To Do
created_date: 2026-11-14 18:54
updated_date: 2026-11-14 18:56
references:
- ../personal/ai-prompt-library/backlog/tasks/apl-27 - Prepare-upstream-conformant-contribution-candidates.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Copier-cat can help prepare feedback or fixes for another project, but project-local findings must be communicated using the upstream project’s own contribution process rather than the agent’s preferred issue or patch format.

Ship:

- A contribution-candidate preparation contract that reads the target project’s contributor, agent, coding, security, support, and submission documentation before selecting the contribution artifact.
- A reviewable candidate containing the required local evidence, reproduction or validation commands, scope boundaries, provenance, and unresolved questions in the target project’s requested format.
- A separate approval gate for any target-project file write, issue creation, pull request, or other publication, followed by reporting the resulting target reference back to the source task.

Constraints:

- Fetch current primary-source contribution rules from the target project rather than relying on repository stereotypes or remembered conventions.
- A Backlog task, GitHub issue, pull request, patch, or Markdown handoff is selected only after the target’s process is known.
- Do not represent a local finding as already submitted, and do not invent a GitHub issue for every local task.
- Keep source-project tasks as the durable local record; link a target reference only when the target actually returns one.
- No target-project mutation or publication without explicit approval at that action.
- Any new skill introduced by implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: upstream submissions always follow the upstream project’s contributor conventions and documentation when communicating project-local findings.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The preparation contract requires current target-project contributor documentation before choosing a contribution artifact
- [ ] #2 The candidate contains relevant evidence, validation commands, provenance, scope, and unresolved questions in the target’s requested format
- [ ] #3 Target mutation and publication require separate explicit approval, with the resulting target reference reported to the source task
- [ ] #4 backlog-py board shows CCC-21 with its full description and acceptance criteria
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
