# copier-cat (cc) — draft spec

## Intent

cc is a template manager for copier. Copier renders and updates projects
from one template; cc manages the *lifecycle around* that: bringing
existing projects under a template (adopt), carrying project-side fixes
back to the template so every inheriting project benefits (contribute /
phone home), and operating a collection of templates as one monorepo with
shared data and a chooser for selecting between them.

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

### C3 — monorepo of templates + chooser

One repository hosts a collection of templates; users choose among them;
a chooser flow (cc-native, or delegating through a template) helps choose;
data shared across the templates is defined once.

Design questions:

- Layout: `templates/<name>/{copier.yml,template/}` and how copier's
  `_subdirectory` maps onto it (each template is its own copier root) —
  every template must remain a plain, standalone-usable copier template
  regardless of monorepo hosting.
- The choosing flow: a cc-native interactive picker vs a choosing flow
  that delegates to a template — what the template renders in that case
  (a stub? nothing? answers only)?
- DRY shared data: copier has `!include` in `copier.yml` (glob-capable,
  documented merge semantics) and `_external_data` for reading another
  template's answers file — but conditional/variable-driven includes are
  an unresolved ask (#1076), base-template inheritance is open (#934),
  and no mechanism shares data across repos without vendoring (the
  shared-config-as-submodule practice is workaround, not mechanism).
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
- **Operates on regular copier templates.** cc acts on copier templates as
  their own units — any conforming copier template works with cc without
  cc-specific structure. cc's conveniences (monorepo hosting, shared data,
  automation) are additive layers on top, never prerequisites: a template
  that never touches cc's extras must remain fully usable by plain copier
  and by cc alike.

## Open questions

Each open question carries a safe default until resolved. Resolved
questions move to the decision record.

- ~~**Language/stack.**~~ Resolved 2026-10-13: Python, uv-managed.
- ~~**cc vs agentic-project-template CLI.**~~ Resolved 2026-10-13, revised
  same session: agentic-project-template is just a regular copier
  template for now — a managed member of cc's future template collection,
  not a special engine owner or consumer. Its adopt-shaped CLI is the
  prototype cc's C1 engine ports from; absorb/consume questions for its
  CLI are moot for now (apt backlog APT-16).
- ~~**Binary name.**~~ Resolved 2026-10-13: `copier-cat`; `cc` remains a
  personal alias.
- ~~**Upstream posture for adopt.**~~ Resolved 2026-10-13: prototype in
  cc, keep it donatable.

## Decision record

| Decision | Choice |
| --- | --- |
| Name | copier-cat (cc); free on PyPI/npm/crates, unclaimed under bengineerdavis on GitHub (checked 2026-10-12) |
| Origin | Spun out of the agentic-project-template session (2026-10-12); its CLI is the prototype of C1/C2 mechanics |
| Seed scope | Docs only — no code or harness; the next session chooses the stack and seeds it |
| Language/stack | Python, uv-managed (2026-10-13) — matches the maintainer's tooling and the apt merge-engine prototype that C1 ports; copier itself is Python, so C2 diff-reuse is direct library use |
| cc ↔ apt | agentic-project-template is a regular copier template for now — not an engine owner or special consumer. Its CLI is the prototype cc's C1 engine ports from (2026-10-13, revised from an earlier full-absorb decision the same session) |
| Binary name | `copier-cat` (2026-10-13) |
| Upstream posture | Prototype adopt in cc, shaped to stay donatable upstream (copier#2486); no PR-first engagement (2026-10-13) |

## References

Prior-art findings recorded 2026-10-13 (research session). These are
evidence and direction, not decisions; each C1/C2/C3 design question
resolves against them explicitly.

### cruft — the closest analogue for update/adopt state and diff flow

- State is a pointer file: `.cruft.json` holds template URL, pinned
  commit, prompt answers (frozen at create time), skip globs. No diff
  content is persisted.
- Update = double render (old at recorded commit with old answers, new
  at HEAD) + `git diff --no-index` patch + `git apply -3`, falling back
  to `git apply --reject` (`*.rej` files).
- Adoption exists minimally as `cruft link` (since 1.1.0): re-prompts
  for variables to reconstruct context, verifies nothing, and the
  community flow (`link` then `diff | git apply`) misses files the
  project lacks (#256).
- Complaint cluster maps 1:1 onto cc's design requirements: #49 (top
  ask: better `.rej` UX), #206 (render-in-repo + editable diff), #287
  (conflict markers harder than `.rej`), #53/#67/#181 (false success
  after partial application), #181 (`git apply -3` needs blobs shallow
  clones lack — breaks CI update bots), #142 (stored branch ignored),
  #232 (new template parameters silently skipped), #256 (project-only
  files invisible to diff; locally-deleted template files not reported).
- Maintenance is slow (release ~annual; 2.16.0 Dec 2024).

Direction this gives cc: per-file/per-hunk review beats all-or-nothing
patch application; adopt must reconcile state with the real project
rather than re-prompt blind; the `git apply -3` blob dependency rules
out that mechanism for CI-targeted flows.

### copier upstream signals

- #2376 (open): proposal to rebuild `copier update` on `git merge`.
  Directly affects C1's donatable shape — a conflict-marker-based adopt
  would fight the direction of travel; a merge-shaped design composes.
- #2487 (PR, closed 2026-04-10 unmerged, no stated reason; review asked
  for rename to `onboard`, dropping `.rej` support because of #2376,
  and minimal scope). Community revival attempts got no response.
  Warning for the upstream posture: closure-without-explanation is a
  live risk; donatability also means small, deference-shaped changes.
- #2463 merged `copier check-update`; #2529 discussion spawned
  natescherer/copier-action. Downstream-update automation is where
  ecosystem energy goes.
- #2005 (conflict markers on copy) and #1738 (multi-template merge)
  remain open — cc's C1 generalizes both.
- Ecosystem update tooling: fohte/copier-update-action pairs copier
  update with mergiraf (an SMT-based merge tool — prior art for
  structural merge); natescherer/copier-action; KyleKing's
  copier-template-tester (stamp testing prior art for C6 skills).

### Contribute-back (C2): the gap is real and unclaimed

- No tool exists that detects template-worthy changes in a generated
  project and opens PRs to the template repo. Copier tracker, cruft
  tracker, GitHub-wide and web searches all return zero hits.
- cruft's `diff --exit-code` is framed as contribute-back *support*
  ("ensures any improvement to the template is always submitted
  upstream") but submission is entirely manual.
- copier's `update` already computes the user-modifications diff
  internally (fresh render at recorded commit vs current project);
  no command exports it as an artifact. That computation is the seed
  of C2's classification input.
- flexlate (multi-engine, git-native, 0.x) stores resolution history
  in internal branches; syncs manual changes into its own branches so
  they survive updates — mechanical prior art, but no upstream flow.

### Monorepo of templates (C3): what exists and what doesn't

- Copier's stated position: 1 template = 1 git repository (tags are
  repo-global; update machinery depends on them). Multi-template-repo
  requests #1078, #1279, #1571, #315 all closed pointing at docs; a
  maintainer notes a subdir-addressable src URL "could actually work"
  (unimplemented). #2300 (open) is destination-monorepos, a different
  problem. Remote URLs cannot address a subdirectory template.
- Verified multi-template repos in the wild
  (sdsc-ordes/repository-template, UABGH-Emerging-Technologies/Templates,
  WaylonWalker/devtainer, GoogleCloudPlatform/solutions-builder,
  mitodl/ol-infrastructure): all (a) clone-then-local-path, (b) use a
  custom wrapper CLI/script as the chooser, (c) give each template its
  own answers file, (d) accept degraded versioning (repo-global tags).
- Chosen patterns resembling cc's goals: sdsc-ordes hands template 1's
  answers to template 2 via `--data`; UABGH delegates via `_tasks`
  running `copier copy` on a `common/` template; worldworm layers
  `-ext` templates with separate answers files; SS-NES meta-template
  maintains a REGISTRY.md of derived templates (hand-maintained).
- No copier-native chooser/meta-picker exists anywhere found — one
  `copier.yml` asking "which stack?" then delegating onward is
  unclaimed. Choosers are always external tools (fzf scripts, just
  targets, bespoke CLIs). The one-template-with-toggles alternative
  (lincc-frameworks/python-project-template) trades per-stack
  repos/tags for a single questionnaire.

Direction this gives C3: cc's monorepo + chooser is the gap everyone
works around with custom wrappers; the price of admission is solving
subdir-addressable URLs/tags or wrapper-based local-path flows, and
`!include`/`_external_data` are the sanctioned sharing primitives any
shared-data design must build on rather than replace.

