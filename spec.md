# copier-cat (cc) — requirements

Derives from PRINCIPLES.md (the constitution). This file carries
requirements only: what each capability must do and the open gates
blocking it. Decisions live in the backlog store (`backlog/decisions/`
and the decision log in `backlog/docs/`); evidence in
`backlog/docs/prior-art.md`; session state in HANDOFF.md; open
questions as backlog drafts carrying a safe default and an owner.
Decisions, session residue, and evidence accumulating here are a bug.

## C1 — adopt

Bring an existing project under a template without data loss, and leave
it a stamped project: a valid answers file with a recorded baseline, so
plain `copier update` works afterwards. Grounded in copier#2486.

Adopt MUST:

- render the template and classify every file (add / identical /
  conflict);
- resolve conflicts through the merger registry (git-merge-driver
  shaped, `git merge-file` fallback) with an empty tree as the
  adopt-time merge base;
- obtain per-file review as the consent moment — accepted merges land
  in the working tree, and cc never commits;
- write the answers file in copier's per-template naming pattern, with
  the adopted template's current version as the recorded update
  baseline;
- change nothing a template or project did not already produce: no
  marker conventions, no cc residue (decision log: Classification
  ownership, Proposal state).

Gates: N-template coexistence (draft-1).

## C2 — contribute / phone home

Detect changes in stamped projects that belong in the template, present
them for review, and prepare PRs to the template repo so every
inheriting project receives them on its next `copier update`.

Phone home MUST:

- reuse copier's own update computation as the diff source (library
  import; tracks copier#2376 rather than forking merge logic);
- derive ownership from the render (template-rendered paths are
  template-owned) with cc config overrides; never ask the template to
  cooperate;
- map rendered paths back to template source by re-rendering with the
  recorded answers (cc owns a cache if that proves expensive);
- shape changesets per file, clustering as presentation only;
- keep proposal state cc-local, keyed by (project, template) identity;
- publish only through the explicit two-command flow (prepare, then
  publish with the user's own `gh` auth) — never automatically;
- carry a template-root offset in the ownership map (subpath PRs
  deferred to Phase 3).

Gates: none — design is settled; implementation is Phase 2.

## C3 — collection of templates + chooser

One repository hosts a collection; a chooser flow helps users select;
shared data is defined once.

The collection MUST keep every template a plain, standalone-usable
copier template regardless of hosting (PRINCIPLES principle 5);
invoke templates by local path after cloning
(backlog/decisions/decision-3; subdir-addressable URLs stay open as a
future option); and build shared data on copier's sanctioned
primitives — a shared answers file seeded via `--data`, `!include`
for question reuse (backlog/decisions/decision-4) — composing with
`!include`/`_external_data` rather than replacing them.

Gates (drafts to open as Phase 3 approaches): layout
(`templates/<name>/{copier.yml,template/}` and the `_subdirectory`
mapping); choosing-flow mechanics and what a delegating template
renders; per-template vs collection-wide versioning.

## C4 — templating templates

`cc new-template` (or a template in the collection) generates a new
template skeleton with the house conventions (principles, harness, stamp tests)
already wired. Gates: skeleton contents; linkage into the C3
collection; how much derives from agentic-project-template's
governance patterns.

## C5 — first-class CLI and API

The merge/diff/adopt engines are importable libraries with a stable,
tested API; the CLI exposes the same operations with stable commands,
stable exit codes, and machine-readable output (JSON / agent formats)
so agents are first-class users. Gates: API stability policy; output
contracts (a JSON schema per command result); whether skills call only
the CLI or may use the library directly.

## C6 — agentic skills, with a graduation principle

cc ships dotagents-installable skills for template authoring (questions,
jinja gotchas, answers files, stamp testing) and for driving cc's
flows. The graduation principle is a requirement, not an aspiration:
every operation is explainable in copier terms, teaches the copier
concepts it uses, and leaves a user who outgrows cc with nothing lost.
Its enforcement mechanism must be able to fail a review. Gates: skill
inventory and granularity; skill/CLI sync rule; the enforcement
mechanism; the curated reference list of foundational templates.

## C7 — learnings routing

Harvest learnings from project surfaces (experiments logs, retro
reports, handoff docs, decisions), propose destinations (another
project's context, a central learnings area, shared data in the
collection, or generation into a reusable skill via C6), and act only
with human review. C2 routes code upstream; C7 routes knowledge
sideways and upward — same review discipline, different artifact.
Gates: harvest surfaces and record shape; destination routing and
consent; the recurrence-to-skill promotion rule.
