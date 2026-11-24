---
id: CCC-34
title: Specify reset with restorable backup and quarantine
status: To Do
created_date: 2026-11-22 17:09
updated_date: 2026-11-22 17:10
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PRINCIPLES.md principle 7 (decision-10) requires that cc never destroys a project's working state without a restorable backup, that quarantine is the only staging area for removed content, and that restore is a first-class operation. spec.md has no reset capability at all, so the principle currently has no requirements home. The 2026-11-08 prototype on branch prototype/cc-composition-cli modeled this: reset --scope <scope> --backup takes a backup before applying, quarantines removed content under .migration/, and restore is a separate verb. Ship: requirements for reset and restore in spec.md covering backup-before-write, quarantine layout, restore as a separate explicit operation, and the practical exceptions the constitution deliberately leaves to spec.md. Constraints: do not implement reset in this task; keep it requirements-only like the rest of spec.md. Preserve independent native copier updates and explicit consent boundaries.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 spec.md carries reset and restore requirements with backup-before-write, quarantine layout, and restore as a separate explicit operation
- [ ] #2 Practical exceptions to principle 7 are stated per capability in spec.md, not in PRINCIPLES.md
- [ ] #3 No reset implementation is added; the change is requirements-only
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Derives from decision-10. Pairs with CCC-35, which tests principle 6.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
