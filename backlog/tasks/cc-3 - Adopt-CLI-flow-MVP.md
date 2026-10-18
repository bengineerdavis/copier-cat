---
id: CC-3
title: Adopt CLI flow MVP
status: Done
created_date: 2026-10-16 21:06
updated_date: 2026-10-18 22:56
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Render, classify per file, per-file review, apply to working tree, write answers file per backlog/decisions/decision-2 and the round-2 decisions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 adopt renders the template and classifies every rendered file add / identical / conflict, with classification derived from the render — no template cooperation, no cc marker conventions (decision log: Classification ownership)
- [x] #2 Conflicts resolve through the merger registry with the empty tree as the merge base (decisions 1-2)
- [x] #3 Per-file review is the consent moment: every file is accepted, rejected, or edited individually; accepted merges land in the working tree and cc never commits (grill round 2)
- [x] #4 The answers file is written in copier's per-template naming — plain .copier-answers.yml for a first template — with the adopted template's current version as the recorded update baseline (decision-2, grill round 2)
- [x] #5 Single-template scope: the flow works for one template per project; N-template coexistence stays on draft-1's safe default
- [x] #6 Stable CLI contract: copier-cat adopt with stable exit codes (0 clean, 1 conflicted, 2 error) and a --json output mode (spec C5; same contract as CC-1)
- [x] #7 Tests cover render, classify, review, apply, and answers end to end plus the CLI contract; mise run lint and mise run test pass
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
DESIGN (probed against copier 9.18 source before implementing, not assumed): render goes through copier.run_copy itself at vcs_ref="HEAD" with skip_tasks=True — the template's current version is the baseline the answers file records, and adopt never runs the template's update-time tasks. copier's worker supplies the questions, the adopted answers, the template's configured answers filename (per-template naming, no cc convention), and the current commit; a plain directory template has no commit and the stamp records _src_path only. The answers filter replicates the worker's _answers_to_remember rather than importing it (underscore-private API across copier versions is not a dependency cc takes): only questions the template asks — the injected jinja helpers (now, make_secret) and _-prefixed internals never reach the stamp. Fixture lesson recorded: _copier_conf carries template config (answers_file, commit), NOT question answers — answers are top-level render context.

CLASSIFICATION is terminal over the registry's result over the empty base (decisions 1-2): a project file absent or empty is an add; a conflicged merge is a conflict whose proposal carries markers (decision-2's add/add cost paid once, in review); merged text equal to the project's is identical; anything else is a merge proposal. The clean-proposal fourth class is the AC trio's "conflicts resolve through the registry" made explicit. All merging goes through the registry — adopt carries no merge logic of its own (DOD #2).

CONSENT AND EXIT CODES (grill round 2): interactive review prompts per file — accept, reject, or edit (the edit replaces the proposal so markers never land from an edited conflict). --json refuses to apply ANYTHING without --accept-all/--reject-all: agent mode has no prompt to consent with, and the refusal leaves the project untouched (no files, no stamp). Exit 1 whenever any conflict was presented, resolved or not — the merge surface's contract. The stamp lands even on a full rejection: the answers file is adopt's own record of the baseline future updates merge against, not project content under review; it is also excluded from classify's plans (cc owns it, a template-shipped answers file is never a reviewed proposal).

TESTS: real git-backed template fixtures (conftest git_template), not mocked renders — covering render-at-HEAD (including a template change moving the baseline), classification of all four shapes, apply-with-edit, never-commits, the stamp convention (and its plain-directory variant), CLI accept-all/reject-all/consent-refusal/interactive review/error paths. 15 new tests, 74 total; mise lint and test clean.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented src/copier_cat/adopt.py (render at HEAD through copier itself, classify terminal over the registry's empty-base result — add/identical/merge/conflict, apply with edit, stamp) and the copier-cat adopt CLI (interactive y/n/e review, --accept-all/--reject-all for scripted consent, --json refusing to apply without consent, exit 0/1/2 with 1 whenever conflicts were presented, stamp lands even on full rejection). Answers filter replicates copier's _answers_to_remember without importing private API. 15 new tests over real git template fixtures; 74 total; lint and pyrefly clean. Next per ROADMAP Phase 1: the first cc skill (adopt/update teaching sections) and the dogfood adopt of a real template.
<!-- SECTION:FINAL_SUMMARY:END -->
## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 All acceptance criteria checked
- [x] #2 No adopt-specific merge logic outside the registry; flows compose mergers the way CC-1's docstring prescribes
<!-- DOD:END -->
