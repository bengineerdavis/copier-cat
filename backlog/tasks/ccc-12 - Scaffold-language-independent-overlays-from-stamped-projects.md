---
id: CCC-12
title: Scaffold language-independent overlays from stamped projects
status: To Do
created_date: 2026-11-14 05:55
dependencies:
- CCC-11
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The maintainer wants to derive a new overlay from an existing stamped project's base structure, so the overlay has known structural composition points without becoming coupled to that base's language. CCC-7 defines composition; it does not yet define this authoring workflow.

Ship:

- An overlay-scaffolding design and implementation that inspects a stamped project's base source, revision, answers, rendered paths, and structured contributions, then generates a standalone Copier overlay template for review.
- A TOML-first contribution extraction path that separates base-owned structure, candidate overlay additions, and project-local edits instead of assuming every current project change belongs to the base.
- Isolated validation for base alone, overlay alone, base plus overlay, idempotent composition, and a second-language fixture demonstrating that the overlay does not require Python.
- Documentation of the structural-compatibility boundary: generated mappings and valid renders do not prove semantic fitness for every project.

Constraints:

- The overlay is an ordinary independently renderable Copier project template with its own answers file, not a child template or Python specialization.
- cc may deduce structure and propose candidate contributions; the maintainer reviews consequential template generation and edits. Agent assistance follows CCC-10 and is not required for known TOML extraction.
- Reuse the CCC-7 composition and CCC-8 scenario approaches. Do not create a separate renderer or universal merger.
- Do not silently copy project-local edits into the overlay or source template. Preserve no lock-in and independent native update paths.
- Defer arbitrary free-text inference and semantic compatibility claims. Unsupported overlaps become review items.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Overlay scaffolding derives base evidence and generates a standalone Copier overlay without assuming current project edits belong to the base
- [ ] #2 TOML-first extraction distinguishes base structure, candidate overlay contributions, and project-local edits for review
- [ ] #3 Isolated tests cover base alone, overlay alone, composition, idempotence, and reuse with a non-Python fixture
- [ ] #4 Documentation states structural versus semantic compatibility and preserves independent native update paths
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
