# HANDOFF — copier-cat seed (2026-10-12)

Handoff for the next agent/human session. Read top to bottom.

## Read order

1. This file.
2. `spec.md` — the draft spec: intent, principles, capability map, open
   questions. It is deliberately *not* a full normative spec yet; inventing
   behaviors before design would violate the ambiguity rule recorded in it.
3. `ROADMAP.md` — phases.
4. Grounding: [copier#2486](https://github.com/copier-org/copier/issues/2486)
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
- cc does not replace it today. Whether cc eventually absorbs that CLI or
  apt consumes cc is an open question in the spec (do not decide casually).
  Tracked in apt's backlog as APT-16.
- cc is seeded at `~/code/projects/personal/templates/copier-cat` (the
  template family moved under `templates/` on 2026-10-13).

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
  projects; adopting it here is the new session's call.
