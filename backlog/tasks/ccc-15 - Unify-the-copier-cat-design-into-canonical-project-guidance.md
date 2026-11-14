---
id: CCC-15
title: Unify the copier-cat design into canonical project guidance
status: To Do
created_date: 2026-11-14 05:57
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The recent stack, compatibility, agent-adaptation, and conversational-creation discussion added CCC-5 through CCC-14 and a session handoff, but the canonical spec, glossary, and roadmap do not yet express the expanded product coherently. Some records contain superseded recommendations, unapproved schema proposals, or overlapping implementation scopes.

Ship:

- An extraction audit mapping the session's substantive conclusions to the correct canonical home: GLOSSARY.md for domain language, spec.md for requirements, backlog decisions for settled tradeoffs, drafts for unresolved questions with safe defaults and owners, ROADMAP.md for sequencing, and implementation tasks for buildable units.
- A grill-with-docs design process that resolves the decision frontier with the maintainer, records settled vocabulary immediately, and distinguishes verified facts from decisions still requiring answers.
- A unified requirements model connecting template composition, stack recipes, independent template updates, structural compatibility, agent-assisted adaptation, conversational creation, and template generation without redefining Copier or requiring agentic overlays to depend on Python.
- A reconciled task graph and implementation sequence that removes duplicate scope and gives each task one clear deliverable boundary.
- A final review of all modified canonical documents and tasks against PRINCIPLES.md and the maintainer's approved decisions before implementation begins.

Constraints:

- PRINCIPLES.md is not edited during this design work. Any conflict requiring amendment is surfaced with a proposed explicit decision for the maintainer.
- Do not treat a previous assistant recommendation or a session handoff as a maintainer-approved decision. Preserve rejected alternatives as history, but do not leave them reading as current requirements.
- Do not start implementation, commit, push, create branches/worktrees, or modify other repositories as part of this design task.
- Keep Copier responsible for rendering/updating, regular templates independently usable, and agentic overlays language-independent.
- Prefer the smallest coherent deterministic MVP; agent adaptation addresses unknowns and recurring behavior can later graduate to deterministic code.
- Use open agent interfaces without coupling the product to a single assistant or making MCP a prerequisite for a CLI/skill workflow.
- Consolidate rather than accrete: replace stale task requirements and link canonical sources instead of appending another layer of contradictory notes.
- Retain the original session handoff as read-only evidence until its accepted content has a canonical home; then label it as historical rather than an active instruction source.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An extraction audit assigns each substantive session conclusion to a canonical document, decision, draft, or implementation task
- [ ] #2 The grill-with-docs process records maintainer-approved vocabulary and separates resolved decisions from open questions with safe defaults and owners
- [ ] #3 The unified requirements model covers composition, compatibility, adaptation, conversational creation, and template generation while preserving Copier ownership and language-independent overlays
- [ ] #4 The reconciled task graph removes overlapping implementation scope and defines a coherent execution order
- [ ] #5 A final review checks every modified canonical document and task against PRINCIPLES.md and the maintainer's decisions
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Maintainer decisions 2026-11-14:
- Q1: cc abstracts Copier rendering commands in CLI and agent sessions; Copier remains the initial rendering runner.
- Q2: first user-visible milestone is conversational assembly of Python plus the agentic overlay through an ordinary agent session.
- Q3: adapt the two real templates through explicit reviewed patches while preserving standalone rendering; arbitrary-template compatibility is not an MVP guarantee.
- Q4: assembly produces one project rendered from multiple independent templates, not an inherited hybrid template.
- Q5: unified create/preview/update/inspect and discovery operate on stack recipes; one-template recipes are valid. Assemble names single/multi-template subproject creation; adopt remains first-class.
- Q7: native per-template updates and conflict detection are MVP; humans or agents resolve residual semantic conflicts.
- Q8: deterministic failures produce review-required reports; agent adaptation is separately approved.
- Q9-Q12: structured contributions have stable identities; native-render extraction is initial source; explicit pre-render contracts may optimize later; per-template answers files and per-chunk attribution reports are complementary; same-key collisions require declared precedence or review.
- Rendering runner is an optional future seam, with Copier first; Cookiecutter conversion is a distant possibility, not current scope.
- Canonical contribution terminology: contribute prepare and contribute publish; phone home is historical.
- GLOSSARY.md updated for assembly vocabulary. decision-7 records the accepted tradeoffs. spec.md and README.md use contribute; PRINCIPLES.md historical phone-home wording remains unamended and needs an explicit constitution decision only if desired.
- The earlier session handoff is now labeled historical input, not an active instruction source.
Q13-Q16 accepted 2026-11-14:
- Stack recipes live with reusable stack definitions, not as required residue in every generated project; optional project-local provenance is allowed but native updates must work without it.
- A small user-level catalog maps familiar template/stack names to sources, optional refs, roles, and answer aliases. It should make app-level configuration easy to capture, reuse, and eventually share.
- Agent creation approval covers only the explicitly approved new destination; existing-project changes, source-template edits, and publication need separate consent.
- Preview cleanup rules are required, including ownership of temporary destinations, cleanup after success/failure, and explicit user choice when retaining a preview for inspection.
- First milestone includes deterministic assembly and the installable conversational skill. Stack-wide update orchestration follows after real update-attribution and ordering evidence; every resulting template must retain a working native copier update -a path.
Q18-Q20 accepted 2026-11-14; Q17 remains unanswered:
- Previews are isolated and cc-owned, with automatic cleanup after success or failure unless the user explicitly retains one. A retained preview reports its path and cleanup instructions. Never delete unowned or user-modified directories.
- Consultant behavior: use the ask-matt main-flow lessons as design inputs. Grill intent, use facts rather than asking discoverable questions, prototype only when a runnable answer is needed, and hand off self-contained work to fresh sessions. cc does not invoke Matt skill names at runtime.
- Ask one focused question at a time only for material ambiguity or consent. Infer from request, catalog, template defaults, and context; surface inferred choices in the assembly preview.
- Template improvements become contribution candidates, not immediate source-template edits. The near-term workaround is a paste-ready handoff to a fresh agent session in a locally available or cloneable target project. Include target path or clone source, evidence, proposed changes, consent boundaries, and validation instructions; no target modification or PR until separately approved.
- Q14 app-level configuration capture/reuse/sharing requires careful separation of answers, recipes, and contributions. Q17 is intentionally left pending for that boundary.
- GLOSSARY.md now includes Consultation and Contribution candidate.
Q17 and Q21-Q23 accepted 2026-11-14:
- Reusable stack definitions may capture template selections, shared answers, and composition policy while templates remain independently renderable. Store catalog/configuration locally first; optionally backing it up to a dedicated Git repository is desirable later, not MVP.
- The consultant begins with intended application purpose, language/runtime needs, desired workflows, and delivery constraints. It may offer to produce missing templates or components, but proposals must be cohesive and as simple as possible without omitting necessary behavior; unknown work becomes a separate approved adaptation, not silent assembly.
- Contribution candidates are portable Markdown handoffs for a fresh session in a locally available or cloneable target project. Include all required context, evidence, proposed changes, open decisions, consent boundaries, and validation commands.
- When web access is available, research the target project's current contributing rules and conventions, as any contributor should. Fetch primary sources; do not guess project rules or automatically publish.
- After successful assembly, optionally save reusable configuration as a named local catalog entry, excluding secrets and project-local edits. Reuse or explicitly share its file; no automatic publication.
- Remaining design work: exact initial recipe/catalog persistence, minimal MVP decomposition, contribution-candidate workflow detail, adaptation boundaries, scenario coverage, and consolidating CCC-7/CCC-11 into one assembly path.
Q24-Q28 maintainer responses 2026-11-14:
- Q24 accepted: initial assembly supports disjoint paths, shared TOML, and .gitignore. Research/design gitignore generation informed by toptal/gitignore.io, preferably using an existing tool when it fits.
- Q25 provisional: local YAML catalog with referenced recipes needs a runnable prototype to understand use, invocation, and ergonomics.
- Q26 unresolved: the proposed CLI is too wordy; show a terser design.
- Q27 accepted: subprojects need user/cc-visible evidence of the stack that produced them, consistent with disposable provenance and native-update independence.
- Q28 accepted: validation must be strong and very fast.
- Prototype boundary: demonstrate CLI/catalog interaction, provenance, preview cleanup, and validation UX with synthetic data; do not implement a competing renderer or production composition engine.
Prototype evidence 2026-11-14:
- Location: /Users/ben.davis/code/personal/cc-assembly-ux-prototype/prototype.py (throwaway, outside cc production source; no Git branch or commit created).
- Run interactively: python3 /Users/ben.davis/code/personal/cc-assembly-ux-prototype/prototype.py
- Main flow without questions: python3 /Users/ben.davis/code/personal/cc-assembly-ux-prototype/prototype.py --demo cc
- Compares cc research, cc assemble research, and copier-cat assemble python-agentic research; shows a resolved plan, consent scope, simulated validation, disposable .copier-cat-stack.yml evidence, preview cleanup, and optional configuration capture.
- Verified all three --demo styles, cancellation with no destination writes and preview cleanup, and retained-preview state. It uses synthetic data only: no Copier execution, project writes, measured performance, or generated-project tests.
- CCC-16 created for deterministic gitignore generation/composition research informed by https://github.com/toptal/gitignore.io.
- Q25 and Q26 have since been revised through prototype feedback. The current interaction model is recorded in the final notes below and in spec.md; earlier recipe/alias/default-stack reservations here are historical, not current blockers.
Prototype feedback 2026-11-14:
- Direct recipe invocation is desirable for projects/templates stamped before.
- Assemble should offer one-command end-to-end creation AND an optional full-stage path; users must not have to invoke every stage for ordinary creation.
- Creating and modifying recipes is first-class, including designing a recipe before using it.
- Previous prototype output was too verbose/messy. Distinguish default output, verbose, debug, and JSON; do not dump state and documentation at every step.
- JSON is a first-class output contract for agents, with prompt/approval handled separately from stdout.
- Use an appropriate logging boundary (logging or loguru to be decided with the installed project conventions) for diagnostics; result serialization must not be interleaved with logs.
- Environment fact: `command -v cc` resolves to /usr/bin/cc (Apple clang 21.0.0); do not assume the short alias cc is available. Revisit the alias through the naming skill rather than silently claiming cc.
- Prototype is being revised around terse output and these workflows; recipe and output-schema decisions remain provisional until maintainer review.
Prototype verdict and interaction decisions 2026-11-14:
- Revised prototype: /Users/ben.davis/code/personal/cc-assembly-ux-prototype/prototype.py. It is synthetic UX code, not an implementation or measured validation.
- Default: three concise result lines. Verbose: resolved templates/answers/composition/evidence/update detail. Debug: logging diagnostics on stderr. JSON: one structured result on stdout. Prompt and diagnostics stay separate from JSON.
- Direct project form and direct recipe form accepted in principle: ccc research and ccc python-agentic research. Explicit assemble is also available: ccc assemble research. `ccc` is a prototype alias candidate only, not approved naming.
- One-command assembly covers all stages; --staged optionally exposes resolve/preview/compose/validate/assemble without making ordinary users invoke five commands.
- First-class recipe operations: recipe new/edit/show; creating or editing a recipe before assembly is valid. Successful assembly may optionally capture a reusable configuration with --save NAME.
- The prototype now uses `recipe` rather than suggesting an unrelated `save` command. It verifies default/verbose/debug/JSON, direct forms, staged and human cancellation, EOF fail-closed behavior, preview retention, JSON approval rejection, and capture/editing.
- Strong-but-fast validation remains a requirement: the prototype labels its validation synthetic; no performance claim was measured.
- Output contract: default=brief result; verbose=additional human-readable context; debug=diagnostic logging; JSON=machine result. They are not merely four increasing verbosity levels. Exact schema/versioning belongs in the CLI implementation spec.
- Logging choice (stdlib logging vs loguru) remains implementation detail; semantic output separation is the design requirement.
- `cc` is the C compiler on this machine. A short alias needs the naming workflow; ccc is only a candidate, with copier-cat assemble always available.
- Next canonical work: update spec.md and ROADMAP.md, consolidate CCC-7/CCC-11, revise CCC-14 conversational surface, and close/supersede CCC-9 where vocabulary is now settled. Preserve future overlay/template generation and adaptation work without placing it in MVP.
CLI feedback 2026-11-14 (prototype under revision):
- Future CLI tasking must handle misspelled commands or at least disambiguate unclear tokens. Example: `ccc recipie` must not offer to create ./recipie without clarification. Never fuzzy-execute a correction; suggest a command and give an explicit escape for literal project names.
- --staged remains useful only if it explicitly walks the user through each stage, engaging them for answers and review. It must not be an implicit opinionated automation path with decorative prompts.
- Prefer user-facing `stack` language over `recipe` so the noun matches the artifact being edited 1:1.
- Explore mise-inspired composition syntax: `ccc --stack agentic-python use flask-overlay` or a Copier-compatible source such as `gh:owner/template`, making stack construction/modification first-class.
- Prototype revision uses stack new/edit/show, --stack STACK use TEMPLATE, direct saved-stack invocation, and five explicit review stages (resolve, answers, compose, validate, assemble). These remain proposals pending maintainer review, not settled command grammar.
Q29 accepted; Q30 approved the naming workflow.
Stack-centered CLI: stack new/edit/show, --stack STACK use TEMPLATE|SOURCE, assemble for project creation, direct saved-stack invocation, terse default-stack form, and --guided for explicit five-stage user review. Unknown tokens fail without writes and suggest rather than auto-correct; explicit assemble handles literal project names.
Canonical spec.md now contains C8 stack assembly and conversational requirements; ROADMAP.md sequences deterministic assembly + skill ahead of contribution and later adaptation/template generation. CCC-7 composition corrected to native-render extraction followed by structured composition (not mandatory pre-render-only data); stack-wide update orchestration follows the first milestone. CCC-14 owns conversational surface and records prototype evidence.
Research artifacts: backlog/docs/gitignore-generation.md and backlog/docs/cli-short-name.md. Naming recommendation: tpls as candidate alias, not an adopted name. ktc rejected after direct discovery of a Kendo template precompiler; tstack has strong existing developer identities; ccc and most initials failed registry checks.
Remaining implementation-spec decisions: minimal stack schema/catalog persistence, default-stack ambiguity policy, alias selection, and a full final review before /to-spec and /to-tickets. No production code or Git mutations.
Q30 resolved by maintainer: use ccc as the local CLI alias and copier-cat as project/package/registry identity. PyPI CCC is Cloud Custom Connections, a Django CRM/marketing app for contacts, lead capture, and automated email/SMS/voice campaigns (only listed release 2.0.1, 2019-01-29). It is not a template manager or apparent executable collision; ccc is not installed locally. No PEP 541 transfer pursued. Evidence updated in backlog/docs/cli-short-name.md and spec.md. Fallback if needed: tpls. Default-stack ambiguity policy remains open.
Default-stack policy resolved by maintainer: no implicit default. A bare interactive project request opens a fuzzy-search selector of available stacks; JSON/--yes/noninteractive assembly requires an explicit stack. Ambiguous matches require confirmation and may cancel with no writes.
If no suitable stack exists, guided setup accepts a Copier-compatible template source and obtains separate approval before downloading it for isolated inspection. Source-to-stack naming/inspection remains an implementation-spec decision.
Use prompt_toolkit fuzzy completion when interactive, with a plain numbered-menu fallback; fzf is not required. Synthetic prototype now passes 15 cases covering direct forms, selection, typo safety, guided stages, JSON boundaries, ambiguous selection and download cancellation. It remains simulated; no production writes or real downloads.
Retro exploration requested by maintainer: how can we capture the instructions needed for the MVP of a design while still allowing open-ended exploration, then reliably reduce the design to the simplest next steps that get the maintainer using it?
Candidate pattern to examine, not a settled rule: maintain an exploration/option log separate from a small MVP contract containing the first real user outcome, one end-to-end workflow, minimum supported inputs, non-goals, and feedback criteria. Convert approved directions into that contract and schedule exploration notes for later review rather than implementing them as they arise.
Evidence from this session: prototype interactions generated many useful ideas (init, fuzzy selection, guided forms, validation, JSON approval, diagnostics, telemetry, MCP), but the maintainer repeatedly redirected toward a usable CLI. The proposed smallest next step is one real ccc assemble path with known stacks, metadata-driven answers, automatic validation, and explicit write approval; polish and integrations wait for actual use.
Retro questions: What artifact separates exploration from committed MVP behavior? Who or what declares that an idea is not usage-blocking? How do we preserve important future capabilities without repeatedly expanding the current implementation? How do we recognize the earliest genuinely usable vertical slice? How should CCC-17-style first-use feedback re-open deferred ideas? Do not treat this note as authorization to build another framework or expand the MVP.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
