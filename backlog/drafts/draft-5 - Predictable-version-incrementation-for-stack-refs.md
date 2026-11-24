---
id: draft-5
title: Predictable version incrementation for stack refs
status: Draft
created_date: 2026-11-22 21:25
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Raised by the maintainer 2026-11-22 (Q19 follow-up): we need a way to automate versioning incrementation, or update versioning predictably, as a stack changes through ccc stack options. decision-11 item 4 settles only that upgrade takes no ad-hoc per-template version override and that version changes are stack edits with a reviewable definition diff. It deliberately does not settle when a stack edit should move a ref at all. Open questions: does a ref advance only on explicit request, or can ccc stack resolve latest-matching within a declared range; how are pre-releases handled (Copier makes them opt-in); what happens to refs pinned to a commit versus a mutable ref; how is a version bump presented in the definition diff versus the project diff it later causes; and how does this interact with no-op detection when a mutable ref moved but no one edited the stack. Safe default: refs change only by explicit stack edit, and ccc stack reports the available newer versions rather than applying them. Owner: bdavis. Evidence to build on: Copier 9.19.1 orders git tags by PEP 440, uses latest tag by default, and offers copier check-update.
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
