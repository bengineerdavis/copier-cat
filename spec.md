# copier-cat (cc) — draft spec

## Intent

cc is a template manager for copier. Copier renders and updates projects
from one template; cc manages the *lifecycle around* that: bringing
existing projects under a template (adopt), carrying project-side fixes
back to the template so every inheriting project benefits (contribute /
phone home), and operating a collection of templates as one monorepo with
shared data and a choosing meta-template.

The test for every capability below: it extends the maintainer, it prefers
deterministic machinery over AI, and it never silently destroys or
silently publishes anything. These are principles, not firm rules; when
they conflict, the conflict is recorded and resolved deliberately.

## Principles

1. **Extend the human.** cc reviews and proposes; it never pushes,
   merges, or overwrites without an explicit human yes.
2. **Deterministic first.** Merges, diffs, and classifications are
   deterministic code where possible. AI is acceptable for classification
   suggestions, never as the merge engine, and its output is always
   reviewable.
3. **Upstream-friendly.** Where a capability belongs in copier itself
   (adopt is the live example — copier#2486), cc prototypes it in a form
   that could be donated upstream rather than forked forever.
4. **Spec-driven.** This file governs; README describes; HANDOFF carries
   session provenance. Ambiguity is marked, not resolved: open questions
   carry a safe default and an owner.

## Capability map

Each capability states its direction and the design questions that must
be answered before implementation. Nothing here is normative until the
open questions resolve.

### C1 — adopt

Bring an existing project under a template without data loss, and leave
it in a state where plain `copier update` works afterwards (a valid
answers file with a recorded baseline).

Grounded in copier#2486: `copy --overwrite` destroys, `--skip`/`_skip_if_exists`
starves the project of template improvements, and `update` requires a
baseline that first-time adoption lacks. The issue's MVP proposes
conflict markers with the existing file as "ours" and template output as
"theirs" (or an empty-base three-way merge), then writing answers so
updates work.

Design questions:

- Conflict markers (issue's proposal) vs semantic merge, or both? The
  agentic-project-template merge engine argues for a **registry of
  structure-aware mergers** (TOML deep-merge, YAML list merge, marked
  sections) with conflict markers as the fallback for unknown formats.
- Prior art close to home: copier-uv-bleeding implements a different
  architecture for the same problem — `_skip_if_exists` on mixed
  template/user files plus a migration task that regenerates them while
  preserving `template-preserve:<name>:start/:end` marked regions
  byte-for-byte. Evaluate marked-region preservation as a mechanism cc
  can adopt or compose with the merger registry; it may be strictly
  better for files with stable named regions.
- Adopt of one template vs several into one project (#1738): how do
  per-template answers files coexist (the two-answers-files pattern
  generalizes to N)?
- Where does cc implement first — cc-native `adopt`, or a contributed
  upstream PR — and how does the prototype stay donatable?
- Baseline establishment: empty tree, template initial version, or a
  synthetic snapshot commit?

### C2 — contribute / phone home

Detect changes made in stamped projects that belong in the template,
present them for review, and push them as PRs to the template repo — so
that after merge, every inheriting project receives them on its next
`copier update`.

Direction: copier's update already computes the exact divergence between
a project and its template's current render; cc reuses that diff,
classifies hunks (template-bug fix vs project-specific intent), groups
them into candidate changesets, and walks the maintainer through review
before anything leaves the machine.

Design questions:

- Classification: deterministic heuristics first (file ownership paths,
  marker comments, answers-file knowledge), LLM-assisted suggestions as
  an opt-in layer — never the decider.
- State: where does "already proposed / already merged" live without
  polluting projects (cc-local state dir vs project marker)?
- Trust: PR creation is always human-triggered; scope tokens/permissions
  to the template repo only.
- Monorepo interplay: a template living at `templates/<name>/` inside a
  monorepo means PRs target a subpath — file ownership maps must handle
  that (ties into C3).

### C3 — monorepo of templates + meta-template

One repository hosts a collection of templates; users choose among them;
a meta-template (or cc-native flow) helps choose; data shared across the
templates is defined once.

Design questions:

- Layout: `templates/<name>/{copier.yml,template/}` and how copier's
  `_subdirectory` maps onto it (each template is its own copier root).
- The choosing flow: cc-native interactive picker vs a real meta-template
  that delegates — what does the meta-template actually render (a stub?
  nothing? answers only)?
- DRY shared data: copier has no include mechanism. Candidates: a shared
  answers file cc seeds via `--data`, a question/defaults library cc
  composes, or generation-time injection. This is cc's biggest design
  space; prototype before committing.
- Versioning: per-template tags vs monorepo-wide releases; how updates
  address a specific template inside the monorepo.

### C4 — templating templates

Scaffolding new templates from a template — the meta-template idea turned
inward: `cc new-template` (or a template in the monorepo) generates a new
template skeleton with the house conventions (spec, harness, stamp tests)
already wired.

Design questions: what the skeleton contains; how it links into the C3
monorepo; how much comes from agentic-project-template's governance
patterns vs being cc-specific.

### C5 — first-class CLI and API

cc is a library and a CLI, both first-class: the merge/diff/adopt engines
are importable with a stable, tested API, and the CLI exposes the same
operations with stable commands, stable exit codes, and machine-readable
output (JSON / agent formats) so that agents — not just humans — are
first-class users.

Design questions:

- API stability policy (what is public, semver from when).
- Output contracts: a JSON schema per command result; agent-consumable
  error and finding formats (the alint `agent` output format is prior art
  in the maintainer's toolchain).
- Whether skills call only the CLI (keeping one surface) or may use the
  library directly.

### C6 — agentic skills, with a graduation principle

cc ships dotagents-installable skills so agents can (a) author a copier
template well — questions, jinja gotchas, answers files, stamp testing —
and (b) drive cc directly for adopt/update/contribute flows.

**Graduation principle:** cc must leave users better at copier, not
dependent on cc. Every cc operation is explainable in copier terms; skills
teach the copier concepts they use; running cc's flows never produces a
state a user cannot understand or continue with plain copier. A user who
outgrows cc loses nothing. This is the "extend the human" principle made
testable.

Design questions:

- Skill inventory and granularity: template-authoring, adopt, update,
  contribute — one skill each or composed?
- Where skills live (cc repo, dotagents-installable) and how they stay in
  sync with CLI behavior (the referenced-skill-is-a-declared-dependency
  rule from the house spec style).
- How "explainable in copier terms" is enforced: per-command copier
  equivalents in docs/help, an `--explain` surface, or skill-authored
  teaching sections — pick a mechanism that can fail a review, not just an
  intention.
- Skill references to foundational templates and tooling: the authoring
  and usage skills should point at the real catalog (the cc monorepo
  templates, agentic-project-template, mise, dotagents, base project
  templates) rather than generic advice — a curated reference list the
  skills cite, kept in the repo where it can be reviewed and updated.

### C7 — learnings routing (the virtuous knowledge cycle)

Learnings made in one project routinely apply to others — the same
failure, the same convention, the same tool discovery. cc (or a cc-borne
skill) should close that loop: harvest learnings from a project's
existing surfaces (experiments logs, retro reports, handoff docs,
spec decisions), propose destinations for each (another project's spec or
context, a central learnings area, promotion into the cc monorepo's
shared data, or generation into a reusable skill), and act only with
human review.

Real instances that motivate this: the naming-skill watchlist handoff
(collisions learned during one session belong in a shared reference),
handoff documents written for one session that carry decisions other
repos need, and the agentic layer's shrink-loop retro, which already
produces findings that outlive their project.

Design questions:

- Harvest surfaces and formats: what counts as a learning, and what
  machine-readable shape does it take (a structured record vs prose)?
- Destination routing: per-learning destination rules, a central
  learnings store, or both — and how destinations consent.
- Skill generator: when a learning recurs across projects, promote it to
  a dotagents-installable skill rather than repeating it — cc's C6
  machinery is the natural home.
- Relationship to C2: C2 routes *code* changes upstream to templates;
  C7 routes *knowledge* sideways and upward. Same review discipline,
  different artifact type.

## Constraints

- cc never modifies a project or pushes to a remote without explicit,
  reviewable human consent at the moment of the action.
- The merge/diff engines are libraries with tests, usable independently
  of any CLI flow — the CLI is a surface over them, not the definition
  of them (C5).
- **No lock-in.** Anything cc produces or changes in a project is
  understandable and continuable with plain copier; every flow documents
  its copier-native equivalent (C6, graduation principle).
- cc stays tool-agnostic about which template is "in charge"; multi-template
  coexistence is a first-class state, not an edge case.

## Open questions

Each open question carries a safe default until resolved.

- **Language/stack.** Python (matches the maintainer's tooling and the
  prototype code). Default: Python, uv-managed. Owner: bdavis.
- **cc vs agentic-project-template CLI.** Absorb, consume, or coexist?
  Default: coexist until cc's adopt reaches parity; revisit then.
  Owner: bdavis.
- **Binary name.** `copier-cat`; `cc` is the C compiler and stays a
  personal alias. Default: confirmed. Owner: bdavis.
- **Upstream posture for adopt.** Prototype in cc vs contribute a PR to
  copier (a prior attempt, #2487, was closed). Default: prototype in cc,
  keep it donatable. Owner: bdavis.

## Decision record

| Decision | Choice |
| --- | --- |
| Name | copier-cat (cc); free on PyPI/npm/crates, unclaimed under bengineerdavis on GitHub (checked 2026-10-12) |
| Origin | Spun out of the agentic-project-template session (2026-10-12); its CLI is the prototype of C1/C2 mechanics |
| Seed scope | Docs only — no code or harness; the next session chooses the stack and seeds it |
