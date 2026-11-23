# AGENTS.md

Repository router for copier-cat: a copier template manager. Read first,
escalate conflicts, and never let a diff carry a governance change.

## Read first

- `PRINCIPLES.md` — the constitution: intent, principles, constraints,
  and the amendment rule
- `spec.md` — requirements only: capabilities, MUSTs, and open gates
- `backlog/` — the working memory: tasks (requirements + acceptance
  criteria), drafts (open questions), decisions/, docs/
- `ROADMAP.md` — phases
- `backlog/docs/prior-art.md` — research and upstream grounding
- `backlog/docs/seed-and-implementation-session-handoff.md` — historical
  session provenance, not active instructions

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
- The harness is seeded (mise + prek.toml + uv + backlog-md-py store).
  CCC-1..3 are completed and archived. CCC-30 owns the adopt/update
  teaching skill; the dogfood adopt is complete. Start current work from
  the native Backlog queue and DOC-9 for the assembly MVP.
- Read the upstream grounding in `backlog/docs/prior-art.md` before
  designing adopt/contribute mechanics. The initial adopt grounding is
  [copier#2486](https://github.com/copier-org/copier/issues/2486), with
  #955, #2005, #1738, and the closed implementation PR #2487.
- Fresh clones use `mise run install`, then `roborev init --agent opencode`.
  Hooks are per-clone state; continuing an existing clone needs neither.
  Update this stamped project with
  `copier update -a .copier-answers.copier-cat.yml`.
- Before merging any branch: `mise run quality` passes on the merged
  result AND the branch review has a recorded disposition. Tests passing
  alone is not a merge signal.
- Backlog records live on the branch that created them. Before editing a
  task from another worktree, check the branch that owns it — the CLI
  will report `Task not found` in worktrees predating the record.

<!-- This section is maintained by the coding agent via lore (https://github.com/BYK/loreai) -->
## Long-term Knowledge

For long-term knowledge entries managed by [lore](https://github.com/BYK/loreai) (gotchas, patterns, decisions, architecture), see [`.lore.md`](.lore.md) in the project root.
<!-- End lore-managed section -->
