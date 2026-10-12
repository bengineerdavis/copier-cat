# Roadmap

> Seed phase. Nothing here is committed; phases re-order as design answers
> land. Current priorities live in the spec's open questions until a task
> store is adopted.

## Phase 0 — Ground and design (current)

- Read and digest copier#2486, #955, #2005, #1738, and the closed PR #2487.
- Survey prior art: cruft's update story, existing monorepo template
  collections, any copier contribute-back tooling.
- Resolve the spec's open questions that gate C1 (merger registry shape,
  adopt UX, baseline establishment).
- Choose stack, seed harness, adopt a task store.

## Phase 1 — adopt MVP (C1)

- Merge-engine library extracted and generalized from the
  agentic-project-template prototype: per-format mergers (TOML, YAML,
  marked sections) + conflict-marker fallback for unknown formats.
- `adopt` flow: render → classify per file (add / identical / conflict) →
  apply with review → write answers with a valid baseline.
- Dogfood: adopt a real template into a real existing personal repo.

## Phase 2 — contribute / phone home MVP (C2)

- Diff-reuse of copier's update computation.
- Deterministic classification (template-bug vs project-specific) with an
  explainable report.
- Review flow and human-triggered PR creation against the template repo.

## Phase 3 — monorepo + meta-template (C3)

- Monorepo layout with per-template copier roots.
- Choosing flow (picker or meta-template), DRY shared-data mechanism.
- Migrate the maintainer's existing templates (copier-mise-sandbox,
  python-cli-template, dotfile-topic-copier, agentic-project-template) as
  the first collection.

## Phase 4 — templating templates (C4)

- `new-template` scaffolding with house conventions pre-wired.
