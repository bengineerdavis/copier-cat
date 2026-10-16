# Roadmap

> Seed phase. Nothing here is committed; phases re-order as design answers
> land. Current priorities live in the spec's open questions until a task
> store is adopted.

## Phase 0 — Ground and design (current)

- Read and digest copier#2486, #955, #2005, #1738, and the closed PR #2487.
- Survey prior art: cruft's update story, existing monorepo template
  collections, any copier contribute-back tooling.
- ~~Resolve the spec's open questions that gate C1 (merger registry shape,
  adopt UX, baseline establishment).~~ Resolved 2026-10-15 (spec decision
  record; docs/adr/0001-0002; grill rounds 1-2 for per-file review and the
  apply flow), with the marked-region evaluation and multi-template
  answers-file coexistence (#1738) still open.
- ~~Choose stack~~ (2026-10-13); seed the harness and adopt the task store
  (backlog-md-py, grill round 2 2026-10-15) — the next action.

## Phase 1 — adopt MVP (C1, C5, C6)

- Merger-registry library extracted and generalized from the
  agentic-project-template prototype: per-format mergers (TOML, YAML,
  marked sections) + conflict-marker fallback for unknown formats —
  shipped as a tested library API and a CLI with stable commands, exit
  codes, and JSON output.
- Study task: evaluate copier-uv-bleeding's marked-region preservation
  against the merger-registry interface (grill round 2); the interface is
  being built so a marked-region provider is another merger, not a rival.
- `adopt` flow: render → classify per file (add / identical / conflict) →
  apply with review → write answers with a valid baseline.
- First cc skill shipped alongside (adopt/update), carrying its teaching
  sections — the graduation principle is exercised from the first release,
  not deferred.
- Dogfood: adopt a real template into a real existing personal repo.

## Phase 2 — contribute / phone home MVP (C2)

- Diff-reuse of copier's update computation.
- Deterministic classification (template-bug vs project-specific) with an
  explainable report.
- Review flow and human-triggered PR creation against the template repo.

## Phase 3 — monorepo + chooser (C3)

- Monorepo layout with per-template copier roots.
- Choosing flow (the chooser: cc-native picker or a delegated flow),
  DRY shared-data mechanism.
- Template-authoring skill (C6): walks an agent or human through building
  a template with house conventions — questions, jinja, answers files,
  stamp tests — teaching copier concepts throughout.
- Migrate the maintainer's existing templates (copier-mise-sandbox,
  python-cli-template, dotfile-topic-copier, agentic-project-template) as
  the first collection.

## Phase 4 — templating templates (C4)

- `new-template` scaffolding with house conventions pre-wired.
