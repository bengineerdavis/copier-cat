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

Grill round 1 (2026-11-08; A1-A6 accepted, Q2-Q5 accepted, Q1 re-opened — see below):

Partially resolved questions:

- Extension: repeated `adopt` is the extension primitive; no separate
  `extend`/`add` command. Re-adopting an already-adopted template is a no-op.

  QUALIFIED by bdavis same session: uncertain whether repeating `adopt`
  dilutes the verb's meaning once it covers base install + overlay add +
  stack expansion together. Grill round 2 follow-up (bdavis 2026-11-08):
- Q1a: YES to one verb, BUT research copier's feature request first and
  disambiguate what `adopt` was asked to do: (i) converting an existing repo
  into a template we didn't have before vs (ii) applying a template to a repo
  that wasn't previously using it. Research pending; not settled until the two
  readings are distinguished against upstream intent.
- Q1b: yes — idempotent act if state is resolved or has no new diff the
  command would be responsible for.
- Q1c: ok — report carries the role (`base:`/`overlay:`), not the verb choice.
- Q1d: ok — reject the split verbs. CAVEAT: must document the full template
  lifecycle clearly, including stamped child projects and how they update
  themselves and their parent project templates via the CLI. Open item.
- Q1e: ok — `--stack` stays a flag on the same verb.

Resolved questions:

- Stack / answers files / composition record: the composition record *is* the
  per-template `.copier-answers.<template>.yml` files (copier-native
  provenance, per C1). Stack membership is recorded only in cc's local state
  dir, keyed by project — no separate in-project composition file.
- Migrate/reset genericity: `migrate` and `reset` keep generic names and
  generic shapes (quarantine → review → apply; scope → backup → quarantine →
  apply). The store-specific mapping in `migrate tasks.json --into backlog` is
  not hardcoded — it comes from the base's task-operation contract (T3), with
  a backlog adapter shipped by cc. `reset` is fully generic.
- Phone-home CLI surface: two commands — `prepare` (classify + select
  destination + validate) and `publish` (per-proposal, user's own `gh` auth).
  Approval is the publish act itself; no separate `approve` command (mirrors
  C1's "accept is the consent moment"). Maintainer acceptance is upstream PR
  review, outside cc.
- Trust policy: future automatic PR creation is permitted only for change
  classes the destination template's operation contract declares safe, opted
  into per-project via cc config. Automatic merging is permanently out.
  Declared by the template, enabled by the user — never by cc.

Prototype behaviors accepted (grill round 1, 2026-11-08):

- Overlay adoption requires a base first — hard refusal ("refused: choose an
  agnostic base first"), not a warning. Overlays are adjectives over the
  base's noun.
- Migrate is rerun-safe: backup precedes `--apply`; the quarantine report
  survives unresolved conflicts; rerun imports nothing twice. Idempotent
  apply; quarantine is the only staging area.
- Reset requires a restorable backup before apply; restore is a separate
  verb (`reset --restore <backup>` illustrative; exact syntax deferred to
  implementation).
- Phone-home refuses without provenance: `prepare` with local changes but no
  adopted base is refused ("needs provenance: adopt a base first");
  project-specific files are excluded, never proposed.
- Publish is per-proposal: `publish --proposal python/001` touches only that
  proposal; others stay unpublished. No batch publish.
- Stack adoption expands to adopt operations: `adopt --stack python-agentic`
  resolves to the three per-template adopts and requires review of the
  proposed file changes — it is not a fourth composition mechanism.

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
