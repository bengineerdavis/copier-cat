---
id: CCC-30
title: Ship the adopt and native-update teaching skill
status: To Do
created_date: 2026-11-15 15:36
parent_task_id: CCC-11
references:
- backlog/docs/cc-assembly-mvp-spec.md
- backlog/docs/seed-and-implementation-session-handoff.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A user of the completed adopt flow needs an installable skill that teaches adoption and native Copier updates through the graduation principle. This is the remaining skill deliverable from the original Phase 1 roadmap, distinct from the later conversational project-creation skill.

Ship:

- A portable adopt/update skill that invokes the shipped copier-cat CLI and explains rendering, per-file review, the answers-file baseline, and native Copier update behavior.
- The curated references required by C6: the project’s real foundational templates and tooling, not generic advice.
- An installation path compatible with the repository’s declared agent workflow, with the skill declared in agents.toml in the same implementation change.

Constraints:

- Do not implement another renderer, planner, or merge engine in the skill.
- Preserve independent native Copier updates and the project’s explicit consent boundaries.
- Keep conversational Python-plus-agentic creation in CCC-14 and the assembly implementation in CCC-24–CCC-29.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The adopt/update skill invokes the shipped CLI and teaches per-file review, answers-file baselines, and native Copier updates
- [ ] #2 The skill includes the C6 curated references to the project’s real foundational templates and tooling
- [ ] #3 agents.toml declares the new skill in the same implementation change
- [ ] #4 The adopt/update workflow remains distinct from the later conversational project-creation skill
- [ ] #5 backlog-py board shows the teaching-skill task with its full description and acceptance criteria
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
