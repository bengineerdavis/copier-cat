---
id: DOC-3
title: Session 2026-11-14 — stack and agent design handoff
---

# Copier-cat design handoff — 2026-11-14

> **Historical design input, not an active instruction source.** CCC-15 and
> the maintainer's subsequent grilling decisions supersede this document
> where they differ. Accepted vocabulary and tradeoffs belong in
> GLOSSARY.md, spec.md, and backlog/decisions/; unresolved questions stay
> with their design task. In particular, native-render extraction followed
> by structured composition supersedes any implication here that initial
> shared-file composition must be pre-render-only.


## Entry point

Start with **CCC-11 — Settle and implement the deterministic project-creation MVP**. Review the current code and existing tests before editing. Read CCC-5 through CCC-10 for evidence and boundaries; use CCC-7 as the composition prerequisite.

This design session wrote backlog records only. No implementation, commits, pushes, worktrees, source-template changes, or research-repository changes were made. The task records are currently untracked under `backlog/tasks/`.

## Recommended execution sequence

1. **CCC-11**: review and settle the smallest deterministic MVP; reconcile the recipe, catalog/discovery, and test scope. Implement only the approved slice.
2. **CCC-7**: complete or refine the underlying composition/update engine as part of the approved CCC-11 implementation plan. Do not build two competing stack implementations.
3. **CCC-14**: after CCC-10's interaction policy is settled, ship the installable conversational project-creation skill. MCP via CCC-5 is a transport, not a prerequisite for the first skill.
4. **CCC-12**: derive language-independent overlays from stamped projects.
5. **CCC-13**: generate standalone Copier templates from stacks, including a polyglot fixture.

CCC-6 (resolution evidence), CCC-8 (isolated scenario testing), and CCC-9 (vocabulary/research) support the implementation; they are not excuses to expand the first slice indefinitely. CCC-10 defines the agent adaptation policy and progressive shrinkage, not an agent-owned merge engine.

## Settled direction

- Copier remains the renderer and updater. cc owns template discovery, stack recipes, plans, known structured composition, compatibility reports, and validation.
- Every source template remains a plain, independently renderable and updatable Copier template with its own answers file. The agentic overlay never requires or inherits from Python; it must work with TypeScript, Rust, and other bases.
- A fresh stack recipe carries each template's identity, source, optional ref, role, answers or answer-input reference, order, and requirements. It is not an ordering-only file. Post-render answers files carry `_src_path`, `_commit`, and native update state.
- Merge known structured mappings by key before one render. Copier `--data` replaces a whole mapping, so independent per-template `--data` calls cannot implement this merge. Same-key conflicts require a declared deterministic rule or review. Unknown formats and genuine semantic conflicts surface for review; never silently discard a contribution.
- Initial roles are base, specialization, and overlay. Require at least one base. Similar roles or apparent semantic similarity are not proof of collision. Explicit requirements/conflicts and concrete file/chunk conflicts are separate checks.
- Forward updates run native `copier update -a` per template in declared order. `.rej` or inline conflicts must fail loudly, never be reported as successful resolution.
- The first deterministic proof is Python alone and Python plus the agentic overlay, with valid shared `mise.toml`, retained base and overlay entries, independent update state, and tests of the rendered project's behavior.
- A stack may produce a project, a reusable stack definition, or a standalone generated Copier template. Template generation is not Copier inheritance. CCC-13 owns this beyond the first deterministic project-creation slice.
- Agents may clarify intent, inspect with cc, propose adapters or template patches, and validate isolated changes. They never become the merge engine, silently modify templates/projects, or publish contributions. Human consent is required at consequential actions.
- Start generously with agents for unclear adaptation, then graduate recurring successful behavior into deterministic adapters, functions, tests, and documented Copier-native equivalents. Keep opt-in agent assistance for unknowns; shrinkage is not agent removal.
- Near-term conversational creation uses installable skills and the CLI. The roadmap goal is natural-language creation from known templates in MCP or any session, with no need to remember sources, flags, answers, or command order. SKILL.md, AGENTS.md, dotagents packaging, host plugins, and MCP are open interface options, not separate engines.

## Decisions the next session still owns

- Exact stack filename and schema (`stack.yml` versus `stack.toml`, inline versus referenced answers). Do not revive rejected cardinality vocabularies (`exactly-one`/`optional-one`/`any` or `min`/`max`) without new evidence.
- Final answers-file convention. Recommendation is `.copier-answers.<template-name>.yml`; preserve existing `.agentic-answers.yml` until an explicit migration verifies `copier update -a`.
- How much catalog/discovery metadata is needed for the two known templates without inventing a general template registry prematurely.
- How data-shaped contributions are exposed by existing templates that currently render literal `mise.toml` fragments, and what isolated migration preserves standalone behavior.
- Exact safe ordering and real-divergence behavior for forward updates; the disposable probe did not prove this.
- Scope of CCC-6 reporting and CCC-8 scenario harness needed for the first slice.

## Vocabulary caution

Use **project template** when distinguishing the reusable Copier source from Jinja templates/macros. A role is a template's intended contribution. Basic direct composition needs no slots. Slots belong to optional reusable stack definitions and constrain candidate roles/identities and cardinality; they do not prove semantic compatibility. Internal template organization must not be confused with independently rendered stack members.

CCC-9's earlier recommendation to use "layer" as the generic stack member is superseded by its later maintainer alignment notes. Read the latest notes before editing GLOSSARY.md; no glossary change has been approved or made.

## Repository constraints

Read `PRINCIPLES.md` first. It requires deterministic machinery first, reviewable AI proposals, regular Copier templates, no lock-in, and explicit human consent for project modifications or publication. Do not edit it as an implementation side effect.

No Git mutation is authorized by this handoff. In particular, do not commit the untracked backlog records, create a branch/worktree, fetch, or push without the maintainer's explicit approval. Do not touch other repositories as a side effect of testing.
