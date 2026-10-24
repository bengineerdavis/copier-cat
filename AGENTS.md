# AGENTS.md

Repository router for copier-cat: a copier template manager. Read first,
escalate conflicts, and never let a diff carry a governance change.

## Read first

- `HANDOFF.md` — session provenance, read order, first-session suggestions
- `PRINCIPLES.md` — the constitution: intent, principles, constraints,
  and the amendment rule
- `spec.md` — requirements only: capabilities, MUSTs, and open gates
- `backlog/` — the working memory: tasks (requirements + acceptance
  criteria), drafts (open questions), decisions/, docs/
- `ROADMAP.md` — phases

## Rules

- `PRINCIPLES.md` is the constitution: read it before designing anything.
  Conflicts with it are surfaced for a deliberate decision — never
  silently reinterpreted, and never edited as a side effect of
  implementation or session work.
- `spec.md` is requirements only. Decisions live in
  `backlog/decisions/` and the decision log (`backlog/docs/`);
  evidence in `backlog/docs/prior-art.md`; open questions as backlog
  drafts carrying a safe default and an owner. Anything else
  accumulating in spec.md is a bug, not an addition.
- The backlog store is the workflow: drive its lifecycle through the
  `backlog-py` CLI (create/list/board/promote/cleanup), never by
  hand-editing store frontmatter; prose edits fill the files the CLI
  writes. Archiving a single completed task is the established
  exception — a pure `git mv` of the task file into `backlog/completed/`
  (frontmatter untouched — that is the invariant this rule protects);
  `backlog-py cleanup` remains the batch path when every Done task
  should move at once.
- The harness is seeded (mise + prek.toml + uv + backlog-md-py store);
  CC-1..3 are completed and archived — Phase 1's remainder is the first
  cc skill (adopt/update, C6) and the dogfood adopt, per ROADMAP.md and
  HANDOFF.md.
- Grounding links live in HANDOFF.md; read the copier issues before
  designing adopt/contribute mechanics.
