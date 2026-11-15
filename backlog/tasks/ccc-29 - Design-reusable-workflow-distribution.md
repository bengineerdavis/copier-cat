---
id: CCC-29
title: Design reusable workflow distribution
status: To Do
created_date: 2026-11-15 06:09
labels:
- ready-for-agent
parent_task_id: CCC-14
references:
- backlog/docs/assembly-original-implementation-tickets.md
updated_date: 2026-11-15 06:29
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The maintainer needs a distribution plan for reusable workflow guidance, optional host plugins, and agent declarations across maintained and newly stamped projects. This is deliberately outside the assembly MVP.

Ship:

- An inventory distinguishing portable skills, optional host plugins, .agents declarations, and agents.toml entries rather than treating them as interchangeable packaging.
- A distribution design for portable SKILL.md guidance over the deterministic CLI, optional plugin and MCP adapters, and installation with or without dotagents.
- A reviewed migration plan identifying receiving maintainer templates and addressing both maintained existing projects and newly stamped projects.

Constraints:

- Preserve open skill standards and avoid host-specific runtime lock-in.
- Installation displays source, scope, command or destination, refresh/removal behavior, and consent.
- Do not modify source-template repositories or global agent configuration in this planning task.
- Produce separately actionable follow-up work only after the maintainer approves the plan.

Agreed with the maintainer 2026-11-14: convert the approved sixth DOC-10 original ticket into the native Backlog implementation queue.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The inventory distinguishes skills, optional host plugins, .agents declarations, and agents.toml entries
- [ ] #2 The design keeps portable skill guidance over the deterministic CLI and treats plugins and MCP as optional adapters
- [ ] #3 Installation works with and without dotagents and shows source, scope, command or destination, refresh/removal, and consent
- [ ] #4 The migration plan addresses maintained and newly stamped projects and identifies receiving templates and order
- [ ] #5 The plan preserves open standards and avoids host-specific runtime lock-in without modifying source templates or global agent configuration
- [ ] #6 Separately actionable follow-up work requires maintainer approval of the distribution plan
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Original approved ticket text is preserved verbatim in DOC-10 (backlog/docs/assembly-original-implementation-tickets.md). This native task is the active implementation queue; the archived ticket is audit evidence, not a second queue.
DOC-10 also records the original .scratch-to-native task mapping. The external .scratch queue was retired after the archive and native tasks were published.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
