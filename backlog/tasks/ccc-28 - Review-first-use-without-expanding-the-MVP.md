---
id: CCC-28
title: Review first use without expanding the MVP
status: To Do
created_date: 2026-11-15 06:09
dependencies:
- CCC-25
labels:
- ready-for-agent
parent_task_id: CCC-17
references:
- backlog/docs/cli-workflow-review.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The maintainer needs to use the real Python-plus-agentic workflow and distinguish usage-blocking defects from later ideas before expanding its scope.

Ship:

- A real first-use walkthrough recording observable friction, outcomes, commands exercised, and evidence gathered.
- A small correction plan limited to demonstrated usage-blocking defects, with optional polish, integrations, and future capabilities kept in their existing follow-up records.
- Findings identifying whether later skills, host plugins, or MCP should consume existing CLI operations rather than duplicate them.

Constraints:

- Follow CCC-17 and CCC-15. Prototype behavior alone is not production evidence.
- Do not reopen the whole design or bundle deferred ideas into the MVP.

Agreed with the maintainer 2026-11-14: convert the approved fifth .scratch issue into the native Backlog implementation queue.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A real first-use walkthrough records the ordinary workflow, observable friction, commands, evidence, and outcomes
- [ ] #2 Usage-blocking defects are separated from optional polish, integrations, and future capabilities
- [ ] #3 Corrections are limited to demonstrated production workflow failures, not prototype behavior alone
- [ ] #4 Findings identify reuse of existing CLI operations by later skills, plugins, or MCP
- [ ] #5 Deferred ideas remain in existing records and the report states decisions and remaining non-goals
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
