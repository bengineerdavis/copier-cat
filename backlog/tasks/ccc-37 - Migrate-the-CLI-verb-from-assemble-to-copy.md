---
id: CCC-37
title: Migrate the CLI verb from assemble to copy
status: To Do
created_date: 2026-11-22 21:25
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
decision-11 (accepted with maintainer 2026-11-22, Q17/Q18) reverses decision-7 item 2: copy names new-project creation and assemble is retired as a CLI verb, surviving only as the internal capability name for the composition stage (spec C8) and a glossary term. Ship: rename the CLI command and its help epilog, make ccc copy refuse an existing destination and point at adopt, and update spec.md C8, ROADMAP.md Phase 2, GLOSSARY.md, backlog/docs/cc-assembly-mvp-spec.md, and backlog/docs/cli-workflow-review.md so the documented surface matches the code. Keep the copier-native teaching table enforced by decision-6 passing: copy -> copier copy, adopt -> copier#2486, upgrade -> copier update -a ANSWERS_FILE. Constraints: keep behavior identical apart from the new refusal of existing destinations. Until this lands the shipped verb is still ccc assemble, and docs/stack-protocol.md marks copy as designed rather than built. Verified 2026-11-22: copier 9.19.1 ships copy, recopy, update, check-update; no copy or upgrade command exists in src/copier_cat/cli.py. Numbered 37 because CCC-34/35/36 are allocated on branch docs/idempotency-immutability-principle.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
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
