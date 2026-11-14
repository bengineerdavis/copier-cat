---
id: decision-7
title: Abstract project assembly over rendering runners
date: 2026-11-14 06:08
status: accepted
---

## Context

Copier renders and updates projects from individual templates. cc needs to abstract those commands for CLI and agent users, compose multiple templates into one subproject, and eventually offer conversational creation from known templates. The composition discussion had not yet separated rendering, assembly, shared-file composition, and adaptation.

## Decision

Accepted with the maintainer 2026-11-14:

1. cc manages the lifecycle around project templates: adopt existing projects, assemble subprojects from one or more templates, update templates independently, contribute improvements upstream, author templates and overlays, and expose these operations through CLI and agent sessions. It does not become a template-independent application generator.
2. **Assemble** names the single- or multi-template subproject-creation workflow. A one-template stack is valid and requires no composition-specific configuration. cc resolves sources, refs, answers, destination, ordering, preview, validation, and reporting; a rendering runner performs the actual render.
3. Copier is the initial rendering runner. The assembly boundary may accommodate other runners in the distant future, including conversion of Cookiecutter templates, but multi-runner support and conversion are not current commitments.
4. The first user-visible milestone is an ordinary agent session that can assemble Python plus the language-independent agentic overlay: discover known templates, obtain missing answers, preview a plan, receive approval, invoke deterministic cc operations, validate the result, and report independent native Copier update paths. MCP is a later transport, not a prerequisite.
5. A stack produces one subproject rendered from multiple independent templates, not an inherited hybrid template. Every template retains its own answers file and native Copier update lifecycle. Separately generating a standalone template is an authoring capability, not the default assembly output.
6. cc may propose explicit, reviewed changes to the real Python and agentic templates so they compose cleanly, while preserving standalone rendering. Arbitrary-template adaptation is not an MVP guarantee.
7. Forward updates use native per-template Copier updates in declared order and surface `.rej` or inline conflicts. Initial assembly and forward updating are separate problems. Humans or agents may address residual conflicts; cc must not claim automatic semantic resolution.
8. Deterministic failure produces a review-required compatibility report. An agent may separately propose a compatibility adapter or template patch, with validation and approval. Ordinary assembly never silently modifies source templates to make a plan succeed.
9. Every abstracted operation remains explainable and reproducible with native runner commands. The CLI is usable without agents, MCP, or host-specific plugins.

The exact shared-file composition stage remains open pending the Q6 design discussion; this decision does not mandate pre-render-only or post-render-only merging.

Accepted with the maintainer 2026-11-14 (Q9–Q12):

10. Shared-file composition operates on structured contributions with stable identities: TOML keys, YAML paths, named marked regions, or explicit text spans. A shared file path is never permission to concatenate completed configuration.
11. Native-render extraction is the initial source of structured contributions. Optional explicit pre-render contribution contracts may later optimize this path, but both use the same structured composer. Rendering independently and composing structured data afterward does not mean textual concatenation.
12. Each template retains its native answers file. cc separately records per-chunk contributor attribution in a reviewable, disposable resolution report. The report is not required for plain Copier use.
13. Different contribution identities compose additively. A same-identity collision requires a declared precedence rule or review; cc never silently chooses a winner. The report identifies contributors, identities, selected rules, and unresolved outcomes.
14. **Contribute** is the canonical capability and CLI command-group name for preparing and publishing template-worthy changes. **Publish** is the explicit PR action. **Phone home** is retained only as historical language; historical records need not be rewritten.

## Consequences

- spec.md needs assembly, composition, compatibility, and adaptation requirements rather than treating agent skills as the sole new capability.
- CCC-7 and CCC-11 must be reconciled into one deterministic assembly implementation path. CCC-14 supplies conversational access after that path exists.
- Templates must not be redesigned around a hypothetical second rendering runner. The abstraction is a seam, not a requirement for templates to know about runners.
- The agentic overlay remains independent of Python and reusable with TypeScript, Rust, and other bases.
