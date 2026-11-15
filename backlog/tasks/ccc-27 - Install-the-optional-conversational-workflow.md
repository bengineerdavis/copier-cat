---
id: CCC-27
title: Install the optional conversational workflow
status: To Do
created_date: 2026-11-15 06:09
dependencies:
- CCC-25
- CCC-26
labels:
- ready-for-agent
parent_task_id: CCC-14
references:
- backlog/docs/agentic-init-research.md
- backlog/docs/cli-workflow-review.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
An agent user needs a portable skill that invokes the deterministic CLI and respects the same approval boundary, with installation that works with or without dotagents.

Ship:

- A portable SKILL.md that interprets intent, asks only necessary questions, invokes CLI discovery and assembly, and explains validation evidence without implementing the workflow.
- A conversational Python-plus-agentic scenario that creates an approved project and reports independent native update paths.
- Optional dotagents setup and a standards-based alternative, with visible source, scope, command or destination, refresh/removal behavior, and consent.
- Isolated tests for dotagents present and absent, idempotence, preserved configuration, and a fully functional CLI when setup is declined.

Constraints:

- Follow decision-9 and CCC-14. Declare every new skill in agents.toml in the same implementation change.
- Never implicitly select global scope or reset existing declarations.
- MCP, telemetry, hosted bug reporting, and source-template changes require separate later consent.

Agreed with the maintainer 2026-11-14: convert the approved fourth .scratch issue into the native Backlog implementation queue.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A portable skill interprets intent, asks necessary questions, invokes CLI discovery and assembly, and explains evidence without implementing planning, rendering, merging, or updates
- [ ] #2 A conversational Python-plus-agentic scenario creates an approved project and reports independent native update paths
- [ ] #3 Every new skill is declared in agents.toml in the same implementation change
- [ ] #4 Setup works with and without dotagents and displays source, skill, scope, command or destination, refresh/removal, and consent
- [ ] #5 Isolated tests prove idempotence, preserved configuration, no implicit global scope or reset, and a functional CLI after declining setup
- [ ] #6 MCP, telemetry, hosted reporting, and source-template changes are not bundled
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
