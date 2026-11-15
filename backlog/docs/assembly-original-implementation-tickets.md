---
type: evidence
tags:
- assembly
- history
- implementation-queue
id: DOC-10
title: Original deterministic-assembly implementation tickets
---

# Original deterministic-assembly implementation tickets

This document preserves the six approved `.scratch` implementation tickets
verbatim. The active queue is native Backlog tasks **CCC-24 through CCC-29**;
this is an audit record, not a second implementation queue.

DOC-9 supplies the feature requirements. The native tasks own current scope,
acceptance criteria, dependencies, labels, and orchestration. Their condensed
wording does not supersede the requirements in DOC-9 or the design decisions it
references.

| Original ticket | Native Backlog task |
| --- | --- |
| `01-assemble-python-from-named-stack.md` | CCC-24 |
| `02-compose-independent-agentic-overlay.md` | CCC-25 |
| `03-share-human-and-agent-command-discovery.md` | CCC-26 |
| `04-install-optional-conversational-workflow.md` | CCC-27 |
| `05-review-first-use-without-expanding-mvp.md` | CCC-28 |
| `06-design-reusable-workflow-distribution.md` | CCC-29 |

## Dependency graph

- CCC-24 blocks CCC-25 and CCC-26.
- CCC-25 and CCC-26 block CCC-27.
- CCC-25 blocks CCC-28.
- CCC-29 is independent and deliberately outside the assembly MVP.

## Original ticket text

The following sections reproduce the six original Markdown files exactly,
including their original headings, references, and acceptance lists.


---

# 01: Assemble Python from a named stack

**What to build:** A developer can name a new project directory and the Python stack, inspect a read-only plan, and approve creation through the real CLI. The command discovers the known template, resolves only necessary answers, renders through Copier, validates the result, and leaves native update evidence. The destination is independent of the stack name.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

**Parent:** CCC-11; requirements in DOC-9 and decisions 3 through 8.

- [ ] The first command assembles a real Python project from a named local stack into an explicitly named new destination.
- [ ] A small local catalog resolves the template's identity, source, optional ref, answers, and role without another project's answers file.
- [ ] Ordinary defaults and focused metadata-driven questions produce a useful project; noninteractive missing answers fail clearly.
- [ ] Dry-run and JSON previews render and validate without writing the destination or requiring a special bypass flag.
- [ ] Explicit approval authorizes only the displayed new-destination write; cancellation leaves no approved project.
- [ ] The generated project has native Copier update state, disposable assembly provenance, and reported native update instructions.
- [ ] Validation covers rendered output, assembly invariants, and the generated project's own tests; failure cannot be reported as success.
- [ ] Isolated previews clean up automatically unless explicitly retained; retained previews report their location and cleanup action.
- [ ] CLI acceptance tests exercise real commands in isolated destinations; composition behavior uses the existing public engine seam.


---

# 02: Compose the independent agentic overlay

**What to build:** A developer can assemble Python with the independent agentic overlay and receive both templates' contributions in one valid project. Each template remains independently renderable and updatable with ordinary Copier.

**Blocked by:** 01 — Assemble Python from a named stack.

**Status:** ready-for-agent

**Parent:** CCC-7 and CCC-11; requirements in DOC-9 and decisions 5 through 7.

- [ ] The named Python-plus-agentic stack renders each ordinary template in isolation and preserves all disjoint files.
- [ ] Structured TOML contributions retain both templates' settings and produce valid, deterministic output through the existing composition engine.
- [ ] Ordered, deduplicated `.gitignore` composition retains both templates' rules.
- [ ] Same-key collisions require a declared deterministic rule or visible review; unsupported shared formats fail explicitly rather than concatenating text.
- [ ] The agentic overlay declares overlay capabilities rather than requiring or inheriting from Python.
- [ ] Both native answers files work independently; native update commands are reported and verified.
- [ ] Real local template fixtures and synthetic conflict fixtures cover composition, validation, and failure reporting.
- [ ] Automatic stack-wide update orchestration is not introduced.


---

# 03: Share human and agent command discovery

**What to build:** A developer or agent can discover assembly operands, examples, effects, errors, and consent boundaries without parsing terminal prose or invoking the workflow. Human and machine help describe the same commands.

**Blocked by:** 01 — Assemble Python from a named stack.

**Status:** ready-for-agent

**Parent:** CCC-17 and decision-8; supporting research in `backlog/docs/machine-readable-help-research.md` and `backlog/docs/cli-workflow-review.md`.

- [ ] One versioned command-description model supplies human help and JSON help, with shared descriptions and structured examples.
- [ ] Discovery distinguishes the new project destination from the named stack and explains read-only previews versus approved writes.
- [ ] Catalog-wide discovery can narrow to a single command without exposing unrelated internal machinery.
- [ ] Help is read-only, initialization-free, and does not download, render, or write project files.
- [ ] JSON alone is a safe assembly preview; JSON with explicit approval authorizes only the displayed new-destination write.
- [ ] Diagnostics and prompts remain separate from machine-readable results.
- [ ] CLI acceptance tests prove parity, schema versioning, side-effect boundaries, and readable failures.
- [ ] MCP and terminal-prose parsing are not prerequisites.


---

# 04: Install the optional conversational workflow

**What to build:** An agent user can request a known stack in ordinary language and have a portable skill invoke the deterministic CLI, explain its plan, and respect the same approval boundary. Installation works with dotagents or a documented open-standards path without it.

**Blocked by:** 02 — Compose the independent agentic overlay; 03 — Share human and agent command discovery.

**Status:** ready-for-agent

**Parent:** CCC-14 and decision-9; supporting research in `backlog/docs/agentic-init-research.md` and `backlog/docs/cli-workflow-review.md`.

- [ ] A portable SKILL.md interprets intent, asks only materially necessary questions, invokes CLI discovery and assembly, and explains validation evidence.
- [ ] The skill does not implement planning, rendering, merging, or update logic itself.
- [ ] A conversational Python-plus-agentic scenario creates an approved project and reports independent native update paths.
- [ ] Every new skill is declared in `agents.toml` in the same implementation change.
- [ ] Optional dotagents setup uses supported dependency operations; a standards-based installation path works without dotagents.
- [ ] Setup shows source, selected skill, scope, exact command or destination, and refresh/removal behavior before changing anything.
- [ ] Setup is idempotent, preserves unrelated configuration, and never implicitly selects global scope or resets existing declarations.
- [ ] Isolated tests cover dotagents present and absent; declining setup leaves the CLI fully functional.
- [ ] MCP, telemetry, hosted bug reporting, and source-template changes require separate later consent and are not bundled.


---

# 05: Review first use without expanding the MVP

**What to build:** A maintainer can use the real Python-plus-agentic workflow, distinguish defects that block ordinary use from later ideas, and turn only the necessary corrections into a small follow-up plan.

**Blocked by:** 02 — Compose the independent agentic overlay.

**Status:** ready-for-agent

**Parent:** CCC-17 and CCC-15; supporting review in `backlog/docs/cli-workflow-review.md`.

- [ ] A real first-use walkthrough covers the ordinary assembly workflow and records observable friction and outcomes.
- [ ] Usage-blocking defects are separated from optional workflow polish, integrations, and future capabilities.
- [ ] Corrections are limited to the demonstrated workflow; prototype behavior alone is not treated as production evidence.
- [ ] Findings identify whether later skills, host plugins, or MCP should consume existing CLI operations rather than duplicate them.
- [ ] Deferred ideas remain visible in their existing follow-up records without reopening the whole design.
- [ ] The review reports commands exercised, evidence gathered, decisions made, and remaining non-goals.


---

# 06: Design reusable workflow distribution

**What to build:** A distribution plan identifies which copier-cat workflow guidance, optional host plugins, and agent declarations should later be merged into the maintainer's existing project templates, with installation paths suitable for maintained and newly stamped projects.

**Blocked by:** None (can start immediately; not part of the assembly MVP).

**Status:** ready-for-agent

**Parent:** CCC-14 and decision-9; coordinate with the maintainer's separate template repositories.

- [ ] Inventory reusable workflow skills, optional host plugins, `.agents` declarations, and `agents.toml` entries, distinguishing their roles rather than treating them as interchangeable packaging.
- [ ] Define portable SKILL.md guidance over the deterministic CLI; plugins and MCP remain optional adapters, not separate workflow engines.
- [ ] Define installation with and without dotagents, including visible source, scope, command or destination, refresh/removal behavior, and consent boundaries.
- [ ] Address both adoption into maintained existing projects and inclusion in newly stamped projects.
- [ ] Identify which existing maintainer templates should receive which artifacts and the order of reviewed migrations.
- [ ] Preserve open skill standards and avoid host-specific runtime lock-in.
- [ ] Do not modify any source-template repository or global agent configuration as part of this planning ticket.
- [ ] Produce separately actionable follow-up work only after the maintainer approves the distribution plan.
