---
id: draft-4
title: Composition and phone-home CLI prototype
status: Draft
created_date: 2026-11-09 00:05
assignee:
- bdavis
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
How should copier-cat compose a base with multiple domain overlays and
prepare reviewable template feedback while preserving project-owned state?

Prototype: `prototype/cc-composition-cli.html` at the repository root, on
branch `prototype/cc-composition-cli`. Throwaway, in-memory browser
demonstration. It does not invoke copier, modify a project, access Git, or
implement a production CLI.

Inputs carried over from the template-stack map (T3 — Ownership split):

- `adopt TEMPLATE PROJECT` remains the primitive; additional overlays extend a
  project's composition rather than appearing as an `update` side effect.
- A named stack selects compatible base and overlay versions; it is a chooser,
  not a separate composition engine.
- Each project's composition record retains its chosen provenance.
- Task imports enter quarantine, preserve existing history, and require review
  before application.
- `reset` replaces workflow configuration after backup and preserves code,
  task history, and knowledge. Restore is a separate operation.
- Phone home classifies changes, selects destination templates, and prepares
  independent proposals. A delivery mechanism does not decide ownership.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Prototype: `prototype/cc-composition-cli.html` (open in a browser).
Behaviour check: `node prototype/cc-composition-cli.check.js`.

Evidence recorded 2026-11-09: the check drives all four guided walkthroughs and
every free-play operation under a DOM shim; 41/41 checks pass. It verifies the
model, not the visual design.

Questions to resolve in copier-cat:

- Does extending an existing composition use repeated `adopt` operations, or
  should a later command make that extension explicit?
- What is the relationship between a named stack, per-template answers files,
  and the composition record?
- Which migration and reset commands are genuinely generic copier-cat
  operations rather than domain-specific template operations?
- What CLI surface best distinguishes classification, preparation, approval,
  publication, and maintainer acceptance for phone home?
- Which trust policy permits future automatic PR creation without automatic
  merging?

Disposition: planning artifact only. Promote through copier-cat's own wayfinding
process after interactive review. The simulated output is not an accepted CLI
contract.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
