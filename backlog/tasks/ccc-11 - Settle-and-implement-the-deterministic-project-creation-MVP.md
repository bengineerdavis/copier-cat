---
id: CCC-11
title: Settle and implement the deterministic project-creation MVP
status: To Do
created_date: 2026-11-14 05:55
dependencies:
- CCC-7
updated_date: 2026-11-15 06:22
documentation:
- DOC-9
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The stack and agent discussions produced several partially overlapping tasks but no single MVP decision. The next session needs to review the design against the existing cc codebase, settle the smallest buildable project-creation workflow, and implement it with tests.

Ship:

- A concise MVP decision covering the initial stack recipe shape, supported composition cases, explicit non-goals, and the exact first end-to-end command sequence. Resolve the CCC-7 fresh-render inputs, CCC-9 vocabulary, and CCC-10 agent-boundary decisions into one buildable scope.
- A template catalog and discovery contract sufficient for an agent or user to find the known Python base and agentic overlay, inspect their required answers and roles, and construct a fresh-render plan without memorized sources or flags.
- The deterministic project-creation path for python-project-template alone and Python plus agentic-project-template, reusing CCC-7's composition and native-update requirements rather than creating a second implementation.
- An executable Python-alone and Python-plus-agentic dogfood in an isolated destination, with shared mise.toml retaining both templates' contributions and independent answers files.
- A short implementation report naming the settled decisions, files changed, tests run, and deferred roadmap work.

Constraints:

- Review before building: read PRINCIPLES.md, spec.md, GLOSSARY.md, HANDOFF.md, ROADMAP.md, the existing src/tests, and CCC-5 through CCC-10. Run the existing test suite and inspect the current repository state before editing.
- The MVP is deterministic composition plus an agent-callable CLI. Do not block it on autonomous natural-language planning, MCP, meta-template slots, universal semantic compatibility, or generating arbitrary new templates.
- Copier owns rendering and updates. cc owns the recipe, plan, discovery, structured composition, and reporting. Templates remain independently renderable and updatable.
- The agentic overlay must not require or inherit from Python; test at least one language-independent contribution contract that can later serve TypeScript or Rust.
- Start with TOML structured contributions and disjoint file paths. Same-key collisions require an explicit rule or review; unsupported overlaps must surface rather than silently choose a winner.
- Do not modify the research repository or any template source repository as a side effect. Use synthetic or explicitly approved local fixtures.
- The recipe must carry source, optional ref, answers or answer-input references, identity, role, order, and requirements for fresh rendering. Post-render answers files carry Copier update state.
- Existing CCC-7 acceptance IDs require cleanup during implementation planning; the CLI's sequential --remove-ac behavior renumbered rather than replacing the intended old criteria.
- Do not commit, push, create a worktree, or change branches without the maintainer's explicit approval for that Git action.
- Keep the first slice small enough for fast feedback. If the recipe schema or composition implementation expands beyond the Python-plus-agentic path, split the remaining work rather than hiding roadmap scope in the MVP.

Agreed with the maintainer 2026-11-14: move review, MVP settlement, and implementation to a fresh copier-cat session after this design session captures the conclusions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The MVP decision records the initial recipe, supported cases, non-goals, and exact first end-to-end commands after reviewing the existing code and CCC-5 through CCC-10
- [ ] #2 Template catalog and discovery expose known template identity, source, role, and required answers for fresh-render planning
- [ ] #3 The deterministic CLI creates Python-alone and Python-plus-agentic projects using Copier and CCC-7 composition without an LLM
- [ ] #4 Isolated dogfood validates shared mise.toml, independent answers files, and the generated projects' own tests
- [ ] #5 The implementation report lists changed files, executed tests, settled decisions, and deferred roadmap work
- [ ] #6 The first CLI includes human and agent help for top-level, assemble, stack list/show, and init: named operands/effects, copy-safe examples, and versioned discovery without writes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
MVP scope from CCC-17: operand clarity and help are usage-blocking, not optional polish. Implement top-level and core-command human help plus versioned help --json / COMMAND --help --json as discovery-only surfaces. Use DESTINATION for a new project directory and STACK for a named composition; examples use harmless example-project/example-stack placeholders and state read-only versus approved-write effects. --json alone previews; --json --yes approves only the displayed new-destination write. Help must work without config/TTY/init and must not write. Broader help polish and other workflow conveniences remain reviewable after use. Existing decision-6 and test_cli.py gate extended accordingly.
Research inputs ready: backlog/docs/machine-readable-help-research.md and backlog/docs/agentic-init-research.md. Machine help uses shared versioned command descriptions for human and JSON, with descriptions/examples/effects/consent. Agent init MVP is optional dotagents skill setup, not MCP configuration. Prototype demonstrates catalog/focused parity and examples shared with human help.
Next flow after CCC-15: to-spec/to-tickets for one usable deterministic assemble vertical slice; then fresh implementation sessions per ticket. Do not expand the prototype into the production CLI in this design session. Agent-init and MCP remain downstream of core workflow, with their explicit scope/consent contracts preserved.
Spec complete and published as DOC-9 (backlog/docs/cc-assembly-mvp-spec.md). Approved test seams: real CLI acceptance + existing composition-engine interface. Agent skill must be portable/open-standards-compatible with or without dotagents; dotagents optional installer, no requirement.
Tracker triage label `ready-for-agent` is NOT applied: CCC-15 documents that backlog-py has labels/priorities but no defined triage vocabulary. Resolve that vocabulary rather than inventing a tag. Spec content itself is complete and ready for /to-tickets.
Prototype preserved on `prototype/cc-assembly-ux` at `bf924fd` as behavioral evidence only. Real production MVP has not been implemented. Start at CCC-24 from DOC-9 and the native implementation queue.
Storage correction after maintainer review: DOC-9 is a feature spec, not the durable decision store. Added decision-8 (shared human/JSON command-description contract) and decision-9 (optional open-standards-compatible agent skill installation, with or without dotagents). Durable composition/assembly choices remain decision-3..7; research docs supply evidence; implementation tickets supply actionable slices. DOC-9 now points to this decision layer.
Tracker correction 2026-11-14: the approved six implementation tickets currently live under .scratch/deterministic-project-assembly/issues/. Before implementation, reconcile them into the configured backlog-py tracker using native tasks, dependencies, labels, and orchestration claims; preserve their content and blocking edges. .scratch is not the intended Backlog adapter output. APL-26 owns the reusable reconcile/routing component. Findings and retro follow-ups are captured as native tasks rather than remaining conversation-only.
Native implementation queue created 2026-11-14: CCC-24 (Python assembly), CCC-25 (independent overlay; depends on CCC-24), CCC-26 (shared discovery; depends on CCC-24), CCC-27 (optional conversational skill; depends on CCC-25 and CCC-26), CCC-28 (first-use review; depends on CCC-25), and CCC-29 (workflow distribution; outside the assembly MVP). All six carry the ready-for-agent triage label. The immediate frontier is CCC-24 and CCC-29.

The approved .scratch/deterministic-project-assembly/issues/ files are superseded as the implementation queue. Preserve them as uncommitted local history until their six native tasks are merged, then remove the duplicate queue through a separately approved cleanup. Do not implement from both systems.
Assembly UX evidence preserved on prototype/cc-assembly-ux at bf924fd: https://github.com/bengineerdavis/copier-cat/tree/prototype/cc-assembly-ux/prototype/cc-assembly-ux. It is synthetic, not production implementation. Production starts at CCC-24; shared discovery belongs to CCC-26 and the optional skill to CCC-27. The external workspace directory is no longer required.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
