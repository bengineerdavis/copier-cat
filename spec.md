# copier-cat (cc) — requirements

Derives from PRINCIPLES.md (the constitution). This file carries
requirements only: what each capability must do and the open gates
blocking it. Decisions live in the backlog store (`backlog/decisions/`
and the decision log in `backlog/docs/`); evidence in
`backlog/docs/prior-art.md`; current work in native Backlog tasks; open
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

## C2 — contribute

Detect changes in stamped projects that belong in the template, present
them for review, and prepare PRs to the template repo so every
inheriting project receives them on its next `copier update`.

Contribute MUST:

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

## C8 — stack assembly

Create one project from one or more ordinary Copier project templates without
introducing template inheritance. A single template is a valid one-template
stack. The agentic overlay remains independent of Python and reusable with
TypeScript, Rust, and other bases.

Assembly MUST:

- discover templates through a small local catalog and resolve a self-contained
  stack definition containing ordered template identities, Copier-compatible
  sources, optional refs, roles, answers or answer-input references, and explicit
  requirements;
- expose first-class stack creation, inspection, and editing. The user-facing
  noun is `stack`, matching the artifact being modified; a stack definition is
  reusable input, stored with application state in one project-local stack
  artifact;
- render each ordinary template through Copier in an isolated preview, extract
  structured contributions with deterministic format adapters, and serialize one
  valid shared result. Explicit pre-render contribution contracts may optimize
  this later but are not a prerequisite;
- compose disjoint paths, shared TOML, and shared `.gitignore` in the first
  assembly milestone. Identify chunks by stable keys, paths, or explicit regions;
  never concatenate completed structured files or silently select a winner for
  unsupported overlaps;
- require a declared precedence rule or review for same-key conflicts. A role,
  shared file path, or semantic similarity alone is not a collision;
- use isolated, cc-owned previews with cleanup after success, failure, or
  cancellation unless explicitly retained. Approval of an assembly authorizes
  only the displayed new destination; existing-project changes, source-template
  changes, and publication each require separate consent;
- write independent native answers files and one disposable
  `<stack name>.stack.yml` artifact containing the stack definition and its
  application state, not a separate stamp file. Removing cc or that artifact
  must not impair any template's native `copier update -a` lifecycle;
- always validate rendered structure, assembly invariants and attribution, and
  the generated project's own tests, without asking whether to validate. Guided
  mode presents the validation results so the user can see how choices affect
  the result. Structural compatibility alone does not prove semantic fitness
  or a working project;
- support concise default output, additional `-v` context, stderr `--debug`
  diagnostics, and one versioned `--json` result. Output format is distinct from
  verbosity. JSON alone produces a read-only preview and requires no `--yes`;
  `--yes` approves only the displayed write scope, never a different operation,
  template download, publication, or telemetry;
- offer a concise end-to-end path and an explicit `--guided` path that engages
  the user in reviewing resolved templates, answers, composition, validation,
  and final assembly. Ordinary assembly must not require five commands or
  decorative approval prompts;
- require an explicit stack for JSON and other noninteractive assembly. An
  interactive request without a stack opens a fuzzy-search selector; if no
  suitable stack exists, guided setup may propose a Copier-compatible source,
  with separate approval before downloading it for isolated inspection. Never
  infer a default stack from a project name;
- provide `ccc init` and offer initialization on an interactive first invocation
  without persisted user config. Built-in defaults support ordinary use without
  that config; declining setup must not block the requested workflow. Init must
  review preferences and obtain explicit approval before writing, preserve
  existing valid config, and distinguish missing from corrupt config. Help,
  version, JSON, and other noninteractive paths never launch an interview.
  Initialization MAY offer a separate, explicit agent-skill setup through
  dotagents, displaying source, skill, user/project scope, exact command, and
  refresh/removal behavior before executing it. It must be idempotent and leave
  plain CLI use intact when declined. It must not silently modify global agent
  configuration or force-reset existing declarations. MCP setup is a separate
  later opt-in after CCC-17 reviews the agent surface; telemetry consent is
  independent of both;
- treat input handling as a tested behavior class: accept case-insensitive
  `y`/`yes` and `n`/`no`, provide an explicit default and edit path, reprompt
  unrecognized text, and cancel safely on interruption or EOF. A reported config
  write must leave observable state and not repeat setup on the next invocation;
- derive guided questions from template metadata and present human-readable
  prompts with defaults, types, validation, and concise explanations. Never
  present a raw answer mapping as the primary question. Individual questions or
  a well-formatted interactive form are both acceptable; the CLI must not impose
  an unnecessary interview when answers are already known;
- reject unknown commands without executing a fuzzy correction. Suggest the
  closest command or stack and preserve an explicit `assemble` form for literal
  project names. Ambiguous input never becomes a destination by inference;
- treat help as a first-class human-and-agent interface. Every command MUST
  name its operands and effects (`DESTINATION` for a new project directory,
  `STACK` for a named composition), distinguish read-only previews from writes,
  explain consent scope, and provide copy-safe examples with placeholders and
  expected effects. Agent help MUST expose the same operation, arguments,
  options, outputs, exit/error semantics, and approval requirements in a
  versioned `help --json` catalog contract; command-specific
  `COMMAND --help --json` narrows the same contract. Use one shared
  command-description model for both views, including command/option
  descriptions, structured examples, effects, and consent scope. Populate
  ordinary parameter metadata from Typer/Click rather than duplicating it.
  Both forms are discovery-only. Help never requires project or config writes,
  and must not trigger first-run initialization.

Native per-template updates remain available in the first milestone. Stack-wide
forward-update orchestration follows only after real ordering and attribution
evidence; `.rej` or inline conflicts always stop for review.

Use `ccc` as the local CLI alias and `copier-cat` as the package/registry
identity. These are separate namespaces; the existing unrelated Django CRM
package `CCC` on PyPI does not prevent this alias choice.

Use `prompt_toolkit` for interactive fuzzy selection when available, with a
plain numbered-menu fallback; neither depends on `fzf` being installed.

Gates: minimal stack-definition schema, catalog persistence, safe shared-file
composition, and real dogfood evidence.

## C9 — opt-in diagnostics and error reporting

Errors MUST explain the attempted action, failure, and safe next step in
human-readable terms. Validation runs locally regardless of reporting choices.

Bug reporting and general usage telemetry are independent opt-in preferences.
Both default to no automatic sharing; enabling one never enables the other.
Initialization may ask about them separately, and either can be disabled without
impairing the CLI. Assembly consent never implies consent to share diagnostics.

Before sending a bug report, cc MUST show what will be shared, with whom, where,
and why, including redactions and exclusions. Newly identified issues may prompt
for a report on a bounded, deduplicated basis. Errors never auto-submit reports
or block recovery. A local report artifact works without Sentry or an account;
any Sentry integration is optional and consent-gated.

Gates: privacy and payload schema; offline/local export; unique-issue identity;
prompt limits; telemetry provider choice and dynamic-enrollment policy.

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
flows. The project-creation skill acts as a consultant: understand the intended
application before selecting templates, ask one focused question only when
intent or consent is materially unclear, and delegate discovery, planning,
composition, validation, and reporting to cc's deterministic CLI. It must not
become a second composition engine.

The first user-visible milestone includes conversational access to the
Python-plus-agentic assembly path; MCP is an optional transport, not a
prerequisite. Unknown needs become separately approved adaptation work.

The graduation principle is a requirement, not an aspiration:
every operation is explainable in copier terms, teaches the copier
concepts it uses, and leaves a user who outgrows cc with nothing lost.
Its enforcement mechanism must be able to fail a review. Gates: skill
inventory and granularity; skill/CLI sync rule; ~~the enforcement
mechanism~~ Done 2026-10-24 (decision-6: per-command copier equivalents
in --help, enforced by a test); the curated reference list of
foundational templates.

## C7 — learnings routing

Harvest learnings from project surfaces (experiments logs, retro
reports, handoff docs, decisions), propose destinations (another
project's context, a central learnings area, shared data in the
collection, or generation into a reusable skill via C6), and act only
with human review. C2 routes code upstream; C7 routes knowledge
sideways and upward — same review discipline, different artifact.
Gates: harvest surfaces and record shape; destination routing and
consent; the recurrence-to-skill promotion rule.
