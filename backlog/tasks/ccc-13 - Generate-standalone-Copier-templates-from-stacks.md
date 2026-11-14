---
id: CCC-13
title: Generate standalone Copier templates from stacks
status: To Do
created_date: 2026-11-14 05:55
dependencies:
- CCC-11
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Stacks must be able to produce another independently usable Copier project template as well as an application project. The maintainer explicitly wants more reusable stack definitions and generated templates, including polyglot templates; this capability is not yet represented by the deterministic stack MVP task.

Ship:

- A stack-to-template generation path that emits a standalone Copier project template with copier.yml, Jinja sources, questions, answers-file template, and template tests.
- A reusable stack-definition artifact that can regenerate the template and record the sources, refs, answers, roles, and composition decisions used to create it.
- A worked polyglot Python-plus-TypeScript fixture demonstrating intentional shared configuration and independent language components, with tests for the generated template and the project it renders.
- Documentation distinguishing template generation from Copier inheritance and explaining which initial answers become questions, defaults, or fixed generated content.

Constraints:

- The generated template must be independently renderable and updatable using ordinary Copier; do not fabricate parent/child inheritance semantics.
- Preserve the independent identity and update lifecycle of source templates. Do not merge their version histories into a synthetic stack version.
- Use CCC-7's composition and CCC-8's isolated testing mechanisms. Unknown compatibility adaptations belong to CCC-10 and require reviewable proposals.
- Keep stack slots and candidate/cardinality constraints as roadmap exploration. Do not block basic template generation on a generalized meta-template schema.
- Do not claim semantic compatibility from parsing alone; test generated-template behavior and the rendered project's own commands.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Stack-to-template generation emits a complete standalone Copier project template with questions, Jinja sources, answers-file template, and tests
- [ ] #2 A reusable stack definition records all composition inputs and can regenerate the template
- [ ] #3 A Python-plus-TypeScript fixture validates the generated template and its rendered project without pretending Copier inheritance exists
- [ ] #4 Documentation defines how initial answers become questions, defaults, or fixed content and preserves source-template update lifecycles
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
