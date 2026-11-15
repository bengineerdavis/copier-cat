---
id: CCC-14
title: Ship conversational project creation through an installable cc skill
status: To Do
created_date: 2026-11-14 05:55
dependencies:
- CCC-11
updated_date: 2026-11-15 06:22
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The maintainer's near-term goal is to ask copier-cat to build projects from an ordinary agent session; the roadmap goal is to describe the desired project from MCP or any session and have cc abstract creation using known templates. The deterministic stack MVP does not itself provide the installable interaction surface.

Ship:

- A dotagents-installable cc project-creation skill using SKILL.md, with AGENTS.md guidance only where needed, that interprets a natural-language request, discovers candidate templates, asks focused intent questions, invokes cc's deterministic CLI, and explains the plan and validation evidence.
- An end-to-end scenario for "Create a Python project named research with my agentic overlay" that discovers templates, obtains only missing required answers, previews the plan, creates the project after approval, and reports independent native Copier update paths.
- An adapter boundary allowing MCP and host-specific plugins to expose the same CLI operations without duplicating workflow or composition logic.
- Documentation of the conversational consent boundary and the handoff from known composition to CCC-10's adaptation workflow when templates are missing or incompatible.

Constraints:

- The skill is workflow guidance, not a second renderer, planner, or merge engine. Deterministic discovery, planning, rendering, merging, validation, and reporting remain in cc's CLI/library surfaces.
- Planning, inspection, and non-destructive previews may be automatic. Creating/modifying project files, patching templates, publishing contributions, and unrelated writes require explicit consent at the action.
- Open standards are preferred: SKILL.md, AGENTS.md, dotagents packaging, host plugins as needed, and MCP as transport. No host-specific lock-in.
- Known composition must not require an unnecessary agent interview; unknown intent or compatibility may use focused questions and CCC-10 adaptation.
- Any new skill must be declared in agents.toml in the same implementation change. Follow the applicable skill-authoring and publication conventions when implementing.
- Do not block this near-term skill on fully autonomous project creation, arbitrary template generation, or universal semantic compatibility.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The installable SKILL.md workflow discovers templates, asks focused questions, invokes the deterministic cc CLI, and explains the plan and validation
- [ ] #2 The Python-plus-agentic conversational scenario creates an approved project and reports independent native update paths
- [ ] #3 MCP and host-plugin adapters reuse the same CLI operations without duplicating planning or composition logic
- [ ] #4 Documentation defines consent boundaries and the handoff to CCC-10 adaptation, and the implementation declares every new skill in agents.toml
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Interaction direction confirmed 2026-11-14 through Q29 and the CLI feedback:
- `stack new/edit/show` inspects and modifies the reusable stack definition. Prefer `stack` over `recipe` so the command noun matches the artifact 1:1. `--stack NAME use TEMPLATE|SOURCE` is the mise-inspired composition operation.
- `assemble` creates a project. Direct saved-stack invocation (`STACK PROJECT`) and the terse default-stack form (`PROJECT`) are shorthand, not a second workflow.
- One-command assembly is the ordinary path. `--guided` explicitly walks resolve, answers, compose, validate, and assemble with real answers/review; it is not decorative staging. `--staged` is only a prototype compatibility alias, not the preferred public name.
- Unknown commands fail without writes and suggest rather than execute corrections. `ccc recipie` must not become an unconfirmed ./recipie project. `assemble NAME` is the explicit literal-name escape.
- Default output is concise; -v adds resolved plan/composition/validation evidence; --debug logs diagnostics to stderr; --json emits one machine-readable result on stdout with prompts separate.
- Synthetic UX prototype preserved on `prototype/cc-assembly-ux` at `bf924fd`. Twelve routing/output/guidance cases passed in the original exploratory run, including typo rejection and JSON fail-closed behavior. It is not production code and did not run Copier or project validation.
- Naming settled: `ccc` is the local CLI alias; `copier-cat` is the product/package/registry identity. Evidence in backlog/docs/cli-short-name.md. No name transfer is needed.
- No implicit default stack. Bare interactive assembly opens fuzzy stack selection. JSON, --yes, and other noninteractive paths require an explicit stack. Ambiguous matches require confirmation and can cancel without writes.
- If no suitable stack exists, guided setup accepts a Copier-compatible source and requests separate approval before downloading for isolated inspection. The prototype simulates, never performs, that download.
- Use prompt_toolkit's fuzzy completion for interactive selection, with a plain numbered-menu fallback; fzf is not a required dependency.
- Revised synthetic prototype passed 15 interaction cases: direct/named stack selection, mise-style use, typo rejection, guided completion/cancellation/editing, JSON success/fail-closed behavior, ambiguous-selection cancellation, and source-download cancellation. No real writes, downloads, Copier execution, or project validation occurred.
- Open before implementation: exact stack-definition/catalog schema, source-to-stack naming and inspection policy, and JSON schema/versioning.
Later review: CCC-17, mapped in backlog/docs/cli-workflow-review.md. Maintainer wants to use and tune the human CLI MVP before settling agent workflows and skills. This task must consume those findings rather than freezing prototype shorthand. Init is proposed: explicit ccc init plus optional interactive first-run setup with built-in defaults; automation never prompts and missing config never selects a default stack. Current init prototype changes are not finally verified and do not inspect real config.
Guided UX requirement from first-use feedback (CCC-17): dynamic human-readable questions sourced from template metadata, not raw JSON answer maps or hard-coded Python-specific prompts. Individual values or a well-formatted form are both acceptable; validate inputs and provide defaults/explanations. Ordinary assembly stays concise and does not impose an unnecessary interview. The installable skill must use the same deterministic answer metadata/validation and consent operations as the CLI.
Research complete: backlog/docs/agentic-init-research.md. Recommendation: ccc init layers preferences plus separate opt-in dotagents skill installation. For maintainer OpenCode, user/global scope is useful default but never implicit; dotagents defaults global so cc must show scope/source/skill/exact command and refresh/removal before approval. Use --project for repo-local evaluation. Never force-reset or directly edit managed OpenCode config. Actual shipped skill/source remains implementation prerequisite; local path source may dogfood.
MCP setup is separate later opt-in after CCC-17/CCC-5, not bundled with skill or telemetry consent. Init/help must be idempotent and plain CLI works when declined. Primary evidence: installed dotagents 3.4.0 help + official README; official OpenCode skills/MCP docs; backlog-py 2.2.0 integration/help precedent. No installation/config changes made.
Assembly UX evidence preserved on prototype/cc-assembly-ux at bf924fd: https://github.com/bengineerdavis/copier-cat/tree/prototype/cc-assembly-ux/prototype/cc-assembly-ux. Its README records the simulated boundary and the two annotation-only corrections required by pyrefly. The evidence branch adds read-only smoke checks; the historical interaction-run claims above remain historical rather than a claim that the original tests were recovered.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
