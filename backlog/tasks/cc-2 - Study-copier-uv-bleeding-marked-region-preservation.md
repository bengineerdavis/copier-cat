---
id: CC-2
title: Study copier-uv-bleeding marked-region preservation
status: To Do
created_date: 2026-10-16 21:06
updated_date: 2026-10-18 17:01
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Phase 1 study task (grill round 2): evaluate marked-region mechanism as another merger provider against the registry interface.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Mechanism read from source at pinned commits (PR #329, merge 9a80874, v0.41.2), not assumed: skip-if-exists plus _tasks regeneration of mixed files, template-preserve:<name>:start/:end markers, by-name matching, snapshot-splice semantics, tool-owned scalar pass, legacy bootstrap, and the documented trade-off that unmarked project content is dropped on update
- [ ] #2 Evaluated against the merger-registry interface (decision-1): how the mechanism enters as a composed provider like MarkedSectionMerger, where its semantics differ (named markers, region-body precedence), and what a port would generalize — recorded in this task's implementation notes
- [ ] #3 Upstream signal assessed: copier#2762 ({% ignore %} tag, preview-leaning) — update-time region preservation stays copier's; cc's registry stays adopt-time; deference posture recorded
- [ ] #4 Verdict recorded as a backlog decision with pinned evidence in backlog/docs/prior-art.md and a review trigger
- [ ] #5 C1 gate closes: spec.md's marked-region gate is removed in the same commit as the decision, per the gate's own wording
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 All acceptance criteria checked
- [ ] #2 Evidence section in prior-art.md carries pinned commits and a review trigger
<!-- DOD:END -->
