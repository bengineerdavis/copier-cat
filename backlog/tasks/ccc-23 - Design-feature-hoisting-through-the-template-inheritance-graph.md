---
id: CCC-23
title: Design feature hoisting through the template inheritance graph
status: To Do
created_date: 2026-11-15 02:40
updated_date: 2026-11-15 02:41
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Useful behavior often begins in the project that needs it, then becomes valuable to the template that maintains that project. Copier-cat should eventually help move such behavior through recorded template lineage instead of requiring a permanent new home to be chosen before the first useful implementation.

Ship:

- A design for feature hoisting that proposes each suitable parent in turn and stops when the feature no longer fits that template’s scope.
- A vocabulary and ownership model distinguishing the concrete project, its maintaining template, successive parent templates, and a possible root template that maintains shared workflow policy.
- A candidate and decision record that explains why a feature belongs at the proposed parent or remains local, using domain ownership and Matt Pocock’s tracer-bullet slicing to keep the move reviewable.
- A dogfood plan that implements and uses the capability in copier-cat first, then considers migrating the reusable mechanism or policy to a root template only after that boundary is justified.
- A relationship to bug fixes: reproduce a defect at successive source layers and fix the earliest layer that exhibits it; for a feature, propose the broadest parent whose scope actually fits.

Constraints:

- Do not delay a useful local implementation until a universal template taxonomy exists.
- Do not equate inheritance or similarity with ownership; evaluate the receiving template’s current scope and contributor conventions.
- Keep local implementation and parent contribution as separate reviewable changes, with explicit approval for target mutations or publication.
- Keep this design outside copier-cat’s first deterministic assembly workflow and do not implement root-template machinery yet.
- Use existing template lineage and provenance evidence rather than introducing another unverified hierarchy.

Agreed with the maintainer 2026-11-14: develop feature hoisting in copier-cat as a dogfooded capability, with a possible root-template policy as a later inheritance decision.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The hoisting design defines parent-by-parent scope checks and the stop condition for an unsuitable template
- [ ] #2 The vocabulary distinguishes maintaining templates, parent templates, and a possible root template without treating the taxonomy as settled
- [ ] #3 The candidate and decision records preserve provenance, scope rationale, local implementation boundaries, and approval gates
- [ ] #4 The dogfood plan starts in copier-cat and describes how the reusable policy can move later without duplicating it
- [ ] #5 The design distinguishes feature hoisting from root-cause defect repair and links the lineage evidence it requires
- [ ] #6 backlog-py board shows the feature-hoisting task with its full description and acceptance criteria
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Maintainer boundary 2026-11-14: apply judgment to self-hosting and propagation. Trace only the template layers that actually produce or consume the behavior; do not recursively chase dependencies of dependencies merely to optimize or centralize ownership. When evidence identifies a defect in a third-party project, prepare a scoped upstream issue or patch using that project’s conventions and submit it with explicit approval. Do not absorb third-party behavior into a local template just because it is upstream of a composed project.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
