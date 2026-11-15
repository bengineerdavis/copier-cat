# Roadmap

> Seed phase complete. Nothing here is committed forever; phases re-order
> as design answers land. Current priorities live in the backlog store
> (`backlog/tasks/`).
>
> The project currently uses FSL-1.1-MIT, a source-available license that
> converts each version to MIT after two years. Whether to adopt an
> open-source license immediately is a separate roadmap decision, not a
> commitment made by the current licensing choice.

## Phase 0 — Ground and design (complete)

- Read and digest copier#2486, #955, #2005, #1738, and the closed PR #2487.
- Survey prior art: cruft's update story, existing monorepo template
  collections, any copier contribute-back tooling.
- ~~Resolve the spec's open questions that gate C1 (merger registry shape,
  adopt UX, baseline establishment).~~ Resolved 2026-10-15 (spec decision
  record; backlog/decisions/decision-1 and decision-2 (formerly
  docs/adr/0001-0002); grill rounds 1-2 for per-file review and the
  apply flow), with the marked-region evaluation and multi-template
  answers-file coexistence (#1738) still open.
- ~~Choose stack~~ (2026-10-13); ~~seed the harness and adopt the task
  store (backlog-md-py)~~ (2026-10-15).

## Phase 1 — adopt MVP (C1, C5, C6) (current)

- ~~Merger-registry library extracted and generalized from the
  agentic-project-template prototype: per-format mergers (TOML, YAML,
  marked sections) + conflict-marker fallback for unknown formats —
  shipped as a tested library API and a CLI with stable commands, exit
  codes, and JSON output.~~ Done 2026-10-18 (CCC-1; decision-1's
  driver shape, decision-2's empty base).
- ~~Study task: evaluate copier-uv-bleeding's marked-region preservation
  against the merger-registry interface (grill round 2); the interface is
  being built so a marked-region provider is another merger, not a rival.~~
  Done 2026-10-18 (CCC-2; decision-5: another merger provider, not a rival;
  generalizations parked as draft-2).
- ~~`adopt` flow: render → classify per file (add / identical / conflict) →
  apply with review → write answers with a valid baseline.~~ Done
  2026-10-18 (CCC-3; classification is terminal over the registry's
  empty-base result — add / identical / merge / conflict — with the
  fourth class the clean-proposal case; the answers file is the stamp,
  written by cc even on full rejection).
- First cc skill shipped alongside (adopt/update), carrying its teaching
  sections — the graduation principle is exercised from the first release,
  not deferred. Tracked as CCC-30.
- ~~Dogfood: adopt a real template into a real existing personal repo.~~
  Done 2026-10-26: `python-project-template` adopted into cc itself
  (2 adds, 3 TOML merges, .gitignore union; cc's source, tests, docs,
  and store kept). Findings: jinja'd answers-filename expansion fixed
  (bdaf190), and the TOML merger's array-concatenation produced a
  duplicate requirement — recorded as a registry-semantics draft.

## Phase 2 — assemble and converse (C8, C5, C6)

- Settle the smallest stack-definition schema, local catalog, and CLI grammar.
  Use `stack` for reusable configuration and `assemble` for project creation.
- Deterministically assemble Python alone and Python plus the language-independent
  agentic overlay: isolated Copier renders, structured TOML and gitignore
  composition, disposable provenance, native answers files, and fast validation.
- Provide concise default, verbose, debug, and JSON output plus an explicit
  guided review path. Unknown commands suggest rather than auto-execute.
- Ship the installable conversational skill over the same CLI. MCP and other
  host adapters follow the CLI contract; they do not own composition.
- Verify independent native updates. Add stack-wide forward-update orchestration
  only after real ordering and attribution evidence.
- Later: language-independent overlay deduction, standalone template generation,
  agent-assisted adaptation, and template collections. These are not hidden in
  the first assembly slice.

## Phase 3 — contribute MVP (C2)

- Diff-reuse of copier's update computation.
- Per-chunk attribution for changes to files composed from multiple templates.
- Deterministic classification (template-bug vs project-specific) with an
  explainable report.
- Prepare portable contribution candidates; publish only with separate explicit
  approval through the user's own `gh` auth.

## Phase 4 — monorepo + chooser (C3)

- Monorepo layout with per-template copier roots.
- Choosing flow (the chooser: cc-native picker or a delegated flow),
  DRY shared-data mechanism.
- Template-authoring skill (C6): walks an agent or human through building
  a template with house conventions — questions, jinja, answers files,
  stamp tests — teaching copier concepts throughout.
- Migrate the maintainer's existing templates (copier-mise-sandbox,
  python-cli-template, dotfile-topic-copier, agentic-project-template) as
  the first collection.

## Phase 5 — templating templates (C4)

- `new-template` scaffolding with house conventions pre-wired.
