---
id: CC-3
title: Adopt CLI flow MVP
status: To Do
created_date: 2026-10-16 21:06
updated_date: 2026-10-18 17:01
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Render, classify per file, per-file review, apply to working tree, write answers file per backlog/decisions/decision-2 and the round-2 decisions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 adopt renders the template and classifies every rendered file add / identical / conflict, with classification derived from the render — no template cooperation, no cc marker conventions (decision log: Classification ownership)
- [ ] #2 Conflicts resolve through the merger registry with the empty tree as the merge base (decisions 1-2)
- [ ] #3 Per-file review is the consent moment: every file is accepted, rejected, or edited individually; accepted merges land in the working tree and cc never commits (grill round 2)
- [ ] #4 The answers file is written in copier's per-template naming — plain .copier-answers.yml for a first template — with the adopted template's current version as the recorded update baseline (decision-2, grill round 2)
- [ ] #5 Single-template scope: the flow works for one template per project; N-template coexistence stays on draft-1's safe default
- [ ] #6 Stable CLI contract: copier-cat adopt with stable exit codes (0 clean, 1 conflicted, 2 error) and a --json output mode (spec C5; same contract as CC-1)
- [ ] #7 Tests cover render, classify, review, apply, and answers end to end plus the CLI contract; mise run lint and mise run test pass
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
- [ ] #2 No adopt-specific merge logic outside the registry; flows compose mergers the way CC-1's docstring prescribes
<!-- DOD:END -->
