---
id: CCC-10
title: Design agent-assisted template adaptation and progressive shrinkage
status: To Do
created_date: 2026-11-14 05:46
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Open-ended template goals such as "make these templates compatible" or "combine Python and TypeScript into a polyglot template" require intent, domain judgment, and changes that a deterministic merger cannot infer. cc currently has deterministic merging, adopt, and a requirements-level agent-skill surface, but no workflow that turns those goals into reviewable compatibility changes.

Ship:

- A research and design note defining the agent-assisted adaptation loop: clarify intent, inspect templates with cc, classify the desired outcome, propose an adapter or template changeset, validate it in isolated fixtures, and present the resulting diffs and evidence for human review.
- A question and interaction policy for open-ended commands, including which facts the agent must establish (target project or generated template, required sources and answers, shared-file semantics, standalone expectations), when it may proceed with stated defaults, and how it escalates unresolved ambiguity without repeatedly interviewing the user.
- A compatibility-proposal record and contract connecting the agent's proposed edits to cc's deterministic inspection, rendering, merging, validation, and report surfaces; include reuse of an accepted proposal by later stacks.
- A shrinkage policy that starts generously with agent skills and workflows when the problem is unclear, observes repeated successful adaptations, and graduates stable behavior into deterministic adapters, CLI functions, tests, and documented native Copier equivalents. Include how recurrence is measured and when deterministic behavior replaces rather than merely supplements the agent.
- Two worked design scenarios: making a Python base and language-independent agentic overlay compose, and producing a polyglot Python-plus-TypeScript project template. Identify what the agent may infer, what requires user answers, and what can become deterministic after the first successful case.

Constraints:

- Follow PRINCIPLES.md: deterministic machinery first; AI may classify and propose but is never the merge engine; all output is reviewable; no project modification, overwrite, publication, or source-template patch lands without explicit human consent at the action.
- The agent uses cc's CLI and structured evidence rather than implementing a second composition engine. Copier remains responsible for rendering and updating each template.
- Ordinary, already-known composition must not require an LLM or an agent interview. Agent assistance is an opt-in adaptation path for unknowns, and remains available even after common paths become deterministic.
- Distinguish structural compatibility (valid files, known chunk identities, reproducible renders) from semantic fitness (the resulting project or template serves its intended purpose). Parsing and tests provide evidence, not a universal compatibility guarantee.
- The agentic overlay remains an independent Copier project template and must not require or inherit from the Python base. The same overlay must be reusable with TypeScript, Rust, and other bases.
- Preserve no lock-in: each source template remains independently renderable and updatable with plain Copier, with its own answers file. A stack may produce a project, a reusable stack definition, or a standalone generated Copier template; generated templates must not pretend Copier provides inheritance.
- Agent-proposed arbitrary merge code is not an MVP requirement. Prefer declarative mappings and existing adapters; new deterministic code requires tests and human review.
- This task defines policy, interaction contracts, and validation evidence. It does not implement the adaptation loop, create an MCP server, or change PRINCIPLES.md, spec.md, GLOSSARY.md, or ROADMAP.md.
- Reconcile CCC-7's current ordered-layer-only stack.yml premise with the newer requirement that a fresh stack contains every source, ref, and answer needed to render. Record that conflict for explicit CCC-7 revision rather than silently treating both as settled.
- Any skill introduced by implementation must be declared in agents.toml in the same change; the existing optional consult-llm template component is not evidence that cc already has an adaptation implementation.

Agreed with the maintainer 2026-11-14: models are fluid collaborators whose useful output can be shaped by evidence, questions, deterministic tools, and feedback; begin generously with agent assistance for unclear work and progressively shrink its surface into deterministic layers.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The adaptation design note defines the clarify, inspect, propose, validate, review, and reuse loop with deterministic cc ownership at every stage
- [ ] #2 The interaction policy defines required intent and template facts, safe defaults, and escalation for unresolved ambiguity without forcing agent interviews on known compositions
- [ ] #3 The compatibility-proposal contract links proposed changes to deterministic validation, reviewable diffs, and reuse in later stacks
- [ ] #4 The shrinkage policy defines recurrence evidence and criteria for graduating agent behavior into deterministic adapters, functions, tests, and native Copier equivalents while retaining opt-in agent assistance
- [ ] #5 The Python-plus-agentic and polyglot-template scenarios distinguish agent inference, required user answers, and future deterministic behavior without coupling the agentic overlay to Python
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Maintainer roadmap clarification 2026-11-14 — natural-language project creation:

- Roadmap goal: from MCP or any agent session, the user can describe a desired project and have cc abstract the complete creation process using templates it already knows. The user should not need to remember template sources, flags, answer variable names, or command order.
- Near-term goal: an ordinary agent session can ask cc to build a project through an installable skill and the deterministic CLI. MCP is another transport to the same capability, not a separate product or composition engine.
- Agent responsibilities: understand the requested outcome, discover and select candidate templates, identify missing intent or answers, ask focused user questions, invoke cc, and explain the resulting plan and validation evidence.
- cc responsibilities: template discovery, machine-readable metadata, plan construction, source/ref/answer resolution, compatibility inspection, Copier invocation, validation, and reporting. Do not put deterministic planning or rendering into a skill prompt.
- Open interfaces: use dotagents-installable agent skills and SKILL.md/AGENTS.md conventions, plugins where the host requires them, and MCP for tool access. Keep the CLI usable without any of those wrappers; preserve the graduation principle.
- Consent boundary: planning, inspection, and preview may be automatic. Creating or modifying project files, applying source-template patches, publishing contributions, or other consequential actions require explicit review and consent at the action. A conversational request is not blanket permission for unrelated writes or publication.
- Roadmap sequencing candidate: CCC-5 exposes the current CLI; the CCC-7 stack surface supplies composition; CCC-10 defines natural-language planning and adaptation; a later implementation task ships the installable project-creation skill and its end-to-end scenario. Do not block the near-term skill on full autonomous project creation.
- First conversational proof: "Create a Python project named research with my agentic overlay" discovers the Python base and agentic template, asks only for missing required answers, previews the plan, creates the project after approval, verifies both templates' configuration, and leaves independent native Copier update paths.
- Later proof: a request for a Python-plus-TypeScript polyglot template can use the adaptation workflow to clarify intent, propose necessary template changes, validate them, and produce a standalone Copier template rather than merely concatenating two renders.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
