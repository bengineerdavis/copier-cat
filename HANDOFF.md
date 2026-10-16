# HANDOFF — copier-cat seed (2026-10-12)

Handoff for the next agent/human session. Read top to bottom.

## Read order

1. This file.
2. `PRINCIPLES.md` — the constitution: intent, principles, constraints,
   the amendment rule. Conflicts with it escalate; it is never edited as
   a side effect of other work.
3. `spec.md` — the draft spec, derived from the principles: capability
   map, design questions, decision record, references. It is deliberately
   *not* a full normative spec yet; inventing behaviors before design
   would violate the ambiguity rule.
4. `GLOSSARY.md` — cc's canonical domain language; avoid-words there are
   active rulings, not style notes.
5. `docs/adr/` — capability-level decisions that carry hard-to-reverse
   tradeoffs; currently ADR 0001 (merger registry shape) and ADR 0002
   (adopt merge base + recorded baseline).
6. `ROADMAP.md` — phases.
7. Grounding: [copier#2486](https://github.com/copier-org/copier/issues/2486)
   (`copier adopt` feature request — the core gap cc addresses), plus the
   related issues it cites: #955 (rebase existing project), #2005 (conflict
   markers on copy), #1738 (merge across templates). PR #2487 was an
   implementation attempt that was closed; worth reading before designing.

## What exists here

Documentation only, on purpose: README, spec draft, roadmap, this handoff,
license, gitignore. No code, no harness. The next session chooses the
language/stack (Python is the working assumption — see spec open questions)
and seeds its own harness; the house harness pattern (mise + prek + backlog)
is demonstrated in agentic-project-template and can be copied when wanted,
not before the shape settles.

## The relationship to agentic-project-template

`~/code/projects/personal/agentic-project-template` (GitHub:
bengineerdavis/agentic-project-template) is the **prototype** of cc's
hardest concepts:

- Its CLI (`src/agentic_project_template/`) already implements an
  adopt-shaped flow: render to temp, apply clean paths with a
  marker-guarded overwrite rule, and **deterministic shared-file merges**
  (TOML deep-merge base-wins, prek repo-signature dedupe, gitignore append,
  marked markdown section). That merge engine is the seed of cc's
  structure-aware merge registry.
- Its spec (Behavior: Composition; ARCHITECTURE.md merge table) documents
  the "two answers files" pattern — one answer to the multi-template
  problem (#1738) for a two-layer case. cc generalizes to N templates.
- cc treats it as a regular copier template (2026-10-13 session): it will
  join cc's Phase 3 collection like any other template. Its CLI stays the
  prototype cc's C1 engine ports from; no absorb/consume mechanics for
  now.
- cc is seeded at `~/code/projects/personal/templates/copier-cat` (the
  template family moved under `templates/` on 2026-10-13).

## Session 2026-10-15 — grill round 1 + roborev

Grill-with-docs round 1 resolved the C1 shape (git-merge-driver-shaped
merger registry — ADR 0001; per-file review; empty-tree adopt-time merge
base with the answers file as the recorded update baseline — ADR 0002,
its text corrected after roborev caught the conflation), the C3 approach
(chooser as the chosen flow — see the superseded meta-template wording),
shared data via copier's sanctioned primitives, and harness seeding
(now; task-store evaluation for backlog-md-py: parity is **partial** —
CLI/MCP/file-format parity is documented and tested against upstream
backlog.md 1.50.1, upstream is now 1.53.0 and the Python port lags only
recent upstream conveniences (cycle-rejection in dependency graphs,
`task list --watch`, list pagination; gaps documented in that repo's
`docs/upstream-feature-parity.md`); caveats are single maintainer
(rmusser01) and a GPL-3.0 tool licence. Adoption therefore stays the
task-store decision's call, re-checking the parity doc before relying on
upstream features). Recorded as GLOSSARY.md, docs/adr/0001-0002, and the
spec decision record rows. roborev is wired in (.roborev.toml, hooks,
agent opencode); its first reviews produced the two Low findings that
closed the chooser wording and this read-order wiring.

## Session 2026-10-15 — grill round 2

All six frontier questions resolved with recommended answers:

- **Apply flow**: accepted merges land in the working tree; the accept
  is the consent moment, committing stays the user's act (spec decision
  record).
- **Answers-file naming**: copier-native per-template pattern (decision
  record) — plain `.copier-answers.yml` first, `.copier-answers.<template>.yml`
  as more coexist.
- **Adopt MVP scope**: single-template runs; #1738 N-coexistence stays a
  flow-level open question on shared primitives.
- **Marked regions**: registry interface built provider-open; evaluation
  of copier-uv-bleeding's mechanism is a Phase 1 study task, not a blind
  pick (ROADMAP Phase 1).
- **Task store**: backlog-md-py adopted (partial parity accepted with
  eyes open — see the round-1 session entry's verdict).
- **Harness shape**: full house harness (mise + prek + uv + backlog) from
  apt — next action after this session.

GLOSSARY gained per-file review and marked region (avoid-words:
preserve markers / template-preserve). The frontier now points at C2
(classification, state, trust) once the engine exists.

## Session 2026-10-15 — grill round 3 (C2)

All seven C2 frontier questions resolved; two answers carried author
nuance worth preserving:

- **Diff sourcing**: reuse copier's own update computation (library
  import, one source of truth — inherits #2376 rather than drifting).
- **Ownership**: render-derived + cc config overrides, and the boundary
  is a rule, not a taste: cc computes classification from artifacts
  copier and the template already produce; nothing is pushed onto
  either. A mechanism that would require template cooperation is a
  scope error (author wording: "out of the scope of copier and a given
  template, anyway").
- **Render→source mapping**: reconstruct by re-rendering with recorded
  answers. Author's conditional on record: if reconstruction proves
  expensive, cc owns the render-map cache — a template-maintained map
  file is never the fallback shape.
- Per-file changesets, cc-local state dir keyed by (project, template),
  two-command prepare/publish with the user's own `gh` auth, and a
  template-root offset in the ownership map (subpath PRs deferred to
  Phase 3).

C2's design questions in the spec are struck with these resolutions;
round 4's frontier is C3's choosing flow and shared data, plus the
C4/C6/C7 ground.

## Session 2026-10-15 — harness seeded

Phase 0's last item landed. The harness follows the apt house pattern,
with one deliberate deviation the author specified: **prek's config is
`prek.toml`** (prek 0.5.5 defaults to TOML), not the legacy
`.pre-commit-config.yaml`. Stack: uv + Python 3.12, ruff + pyrefly via
uv-run local prek hooks (tool pins live in pyproject.toml only), tombi
for TOML lint, copier 9.18.2 as a real dependency (C2's diff-sourcing
decision exercised by the smoke test). Task store: backlog-md-py,
`backlog-py init --defaults --task-prefix cc`; seed tasks CC-1 (merger
registry extraction), CC-2 (marked-region study), CC-3 (adopt CLI MVP).
AGENTS.md's "nothing is implemented" routing rule is retired. Phase 1
starts at CC-1.

## Session 2026-10-13 — open questions resolved

All four spec open questions resolved (see spec decision record):

- Stack: **Python, uv-managed**. Phase 0's stack decision has landed; the
  "no scaffolding before stack decision" rule in AGENTS.md is satisfied —
  harness seeding may begin.
- cc ↔ apt: revised mid-session — **agentic-project-template is just a
  regular copier template for now**, not an engine owner or special
  consumer. Its CLI remains the prototype cc's C1 engine ports from
  (APT-16 settled this way).
- Binary: **copier-cat**. Upstream: **prototype in cc, donatable**.
- New hard constraint recorded: **cc operates on regular copier
  templates as their own units** — cc-native structure is always
  additive, never a prerequisite for a template to work with cc.
  This came from the session's cc↔apt resolution: apt is just a
  regular template, and that generalized.

## Session 2026-10-13 — prior-art research landed

Findings recorded as the spec's new **References** section (not
decisions). Headlines:

- **cruft** is the closest analogue; its complaint history (all-or-nothing
  apply, `.rej` UX, blind re-prompt adoption, `git apply -3` blob
  dependency) is cc's requirements list for adopt/update UX.
- **copier#2376** proposes a `git merge`-based update rewrite — C1's
  design must be merge-shaped to stay donatable; conflict markers-only
  would fight the direction of travel.
- **C2's gap is real and unclaimed**: zero contribute-back tooling
  exists anywhere found. copier's update already computes the
  user-modifications diff internally; that's the seed.
- **C3 correction recorded**: copier DOES have `!include` and
  `_external_data`; the missing pieces are cross-repo sharing,
  conditional includes (#1076), inheritance (#934). No chooser/
  meta-picker exists anywhere — multiple-template repos in the wild
  all paper over it with custom wrapper CLIs.
- **Upstream risk noted**: copier#2487 (adopt PR) was closed unmerged
  with no stated reason; revivals got silence. Donatability requires
  small, deference-shaped changes.

## Changes since seed (2026-10-13)

- **C7 added** (learnings routing — the virtuous knowledge cycle): harvest
  learnings from project surfaces and route them to where they will be
  acted on; recurring learnings promote into generated skills. Real
  motivating instances: the naming-skill watchlist handoff, handoff docs,
  and agentic-project-template's shrink-loop retro.
- **C1 gained close prior art**: copier-uv-bleeding implements the
  alternative architecture (skip-if-exists + migration script regenerating
  mixed files while preserving `template-preserve:<name>:start/:end`
  marked regions byte-for-byte). Evaluate against the merger registry
  before designing.
- **C6 gained a references design question**: skills must cite the real
  foundational catalog (monorepo templates, agentic-project-template,
  mise, dotagents, base project templates), not generic advice.
- **The sibling fork is now a concrete monorepo candidate**:
  copier-template-copier-template (bengineerdavis's fork of cbrown1234's)
  was customized — go-task replaced by mise everywhere (repo + generated
  template + CI + renovate), licensing expanded to 16 SPDX options
  including BlueOak-1.0.0 and the FSL Fair Source pair. Its own
  HANDOFF.md documents divergence and the upstream-sync question.
- agentic-project-template tracks the cc relationship as backlog task
  APT-16 (absorb / consume / coexist — spec open question).

## First-session suggestions (in rough order)

1. Read spec.md open questions; confirm or challenge them — the spec is a
   draft and the session should push back, not obey.
2. Research prior art before designing: `cruft` (update story for
   cookiecutter), copier's own discussions on contribute-back workflows,
   monorepo template collections (how others host N templates in one repo).
   Record findings as spec references, not as decisions.
3. Prototype `adopt` first (Roadmap Phase 1): it is the most grounded
   feature — port the apt merge engine behind a per-format merger registry
   (TOML/YAML/markdown-section first), dogfood by adopting a real template
   into a real personal repo.
4. Keep commits per commit-hygiene; keep the spec's ambiguity discipline
   (open questions with safe defaults and owners, never guesses).

## Environment notes

- `uv` is the Python toolchain on this machine (mise-managed); `copier`
  9.18.2 is pinned user-wide via pipx.
- GitHub CLI (`gh`) is authenticated as bengineerdavis.
- Backlog/backlog-md-py is the task-store convention in the sibling
  projects; **backlog-md-py is adopted here too** (grill round 2,
  2026-10-15 — partial parity accepted with the verdict recorded),
  seeding the harness/backlog store is the next action.
