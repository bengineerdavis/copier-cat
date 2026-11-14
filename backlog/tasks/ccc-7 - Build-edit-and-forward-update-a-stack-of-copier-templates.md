---
id: CCC-7
title: Build, edit and forward-update a stack of copier templates
status: To Do
created_date: 2026-11-14 03:42
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Copier templates stamp and update projects independently, but Copier has no native recipe for composing several templates into one destination. The maintainer's current Python-plus-agentic project needs a reusable composition recipe and a way to forward-update both templates without hiding conflicts.

Ship:

- A stack recipe containing the ordered template applications and everything needed for a fresh render: stable template identity, source usable by copier copy, optional ref, role, answers or referenced answer inputs, and explicit requirements. Do not reduce this to an ordering-only file.
- Stack creation, inspection, and editing operations that resolve those inputs into a reviewable plan and invoke Copier for every render; sources and answers remain inspectable rather than hidden in a session or agent prompt.
- Data-shaped composition for shared structured files: render each ordinary Copier template in an isolated preview, extract structured contributions, merge by stable identity, and serialize one valid result. Report overrides and unsupported overlaps; never concatenate completed structured files or silently discard a template's contribution.
- Native per-template update verification in the first milestone. A later forward runner uses each template's native answers file and copier update -a in declared order, detects .rej files or inline conflict markers, and stops rather than claiming success with unresolved conflicts.
- Independent per-template answers files and a no-lock-in guarantee: removing the recipe or cc leaves every template independently renderable and updatable with plain Copier.
- A first dogfood covering python-project-template alone and python-project-template plus agentic-project-template, with valid shared mise.toml containing both templates' entries and independent native update paths.

Constraints:

- Copier remains the rendering and update engine. cc orchestrates applications and composes known structured contributions; it does not implement a competing renderer or inheritance model.
- The agentic overlay is an independent Copier project template. It must not require or inherit from the Python base, and must remain reusable with TypeScript, Rust, and other bases.
- Initial roles are base, specialization, and overlay. Require at least one base, but do not infer incompatibility from matching roles or apparent semantic similarity. Slots and stack-definition constraints are roadmap material, not required for direct composition.
- Native-render extraction is the initial composition path; an explicit pre-render contribution contract is an optional later optimization. Same-key conflicts need an explicit deterministic rule or review, with the resolution reported. Unsupported file types fail visibly or require review; never invent a universal merge.
- First-milestone shared-file support is TOML and .gitignore, alongside disjoint paths. Use the gitignore reuse evidence in backlog/docs/gitignore-generation.md rather than making assembly depend on a network service.
- Scenario B native Copier conflicts are acceptable initially if surfaced honestly. Safe update ordering remains unverified until the real dogfood test runs.
- Defer agent-assisted compatibility changes to CCC-10; this task's deterministic composition path must work without an LLM or interview.
- Rejected stack cardinality syntax includes exactly-one/optional-one/any and min/max fields. Do not implement either pending stack-format exploration.

Supersedes the earlier ordering-only stack.yml premise, which conflicted with the maintainer's 2026-11-14 requirement that a fresh stack carry all render inputs. Per-template answers files still own Copier's _src_path, _commit, and update state after stamping; the stack recipe owns the initial composition inputs.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A fresh stack recipe contains every render input: template identity, Copier-compatible source, optional ref, role, answers or referenced answer inputs, order, and explicit requirements
- [ ] #2 Stack creation, inspection, and editing produce a reviewable plan and invoke Copier for every render without hiding inputs in an agent session
- [ ] #3 Native-render extraction yields data-shaped contributions that merge per stable identity; the two-table test emits one [tools] table and all contributed tasks, while same-key input follows an explicit rule or review with a reported outcome
- [ ] #4 Scenario A produces no .rej files on the data-shaped path; Scenario B surfaces native Copier .rej or inline conflicts without claiming success
- [ ] #5 Each template keeps an independent answers file and native Copier update lifecycle
- [ ] #6 A compatibility report names shared files and whether the format adapter can resolve them; unsupported overlaps do not silently choose a winner
- [ ] #7 Python alone and Python plus the language-independent agentic overlay produce valid shared mise.toml retaining both templates' entries and native update paths
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Current maintainer decisions 2026-11-14 (CCC-15 / decision-7):
- Assemble names single- and multi-template creation. The first milestone includes deterministic assembly plus its installable conversational skill.
- Initial composition renders each ordinary Copier template in an isolated preview, extracts structured contributions with format adapters, composes by stable key/path/region, and serializes valid shared files. Explicit pre-render contribution contracts are an optional later optimization, not required by this task.
- Rendering after extraction is not textual concatenation. Reuse the existing structure-aware merger behavior where its conflict policy matches composition; do not assume its adopt-time base-wins scalar rule is sufficient for stack precedence.
- Same-key scalar conflicts require a declared precedence policy or review. Stack order alone is not permission to silently override. Existing TOML deep_merge currently retains earlier scalar values with warnings; any later-wins behavior requires an explicit tested decision.
- The reusable stack recipe lives with its catalog/stack definition and is not required project residue. Generated projects retain native answers files and update commands.
- Initial previews are cc-owned and automatically cleaned up after success/failure unless explicitly retained; retained previews report their path and cleanup command.
- Stack-wide forward-update orchestration is the next increment after the first assembly milestone. Each individual template must still have a verified native copier update -a path.
- CCC-11 no longer owns settling these product decisions; CCC-15 and decision-7 carry them. Reconcile CCC-7 and CCC-11 into one assembly implementation path during /to-spec and /to-tickets.

Superseded notes from the earlier pre-render-only exploration are retained below as evidence, not current requirements.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
