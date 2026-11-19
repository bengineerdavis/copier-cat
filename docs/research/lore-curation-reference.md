# How lore curation actually works — a reference

Sources, read 2026-11-19 from the fork at `~/code/forks/loreai` (commit
`3b48e546`) and from the **installed binary v0.40.0** where behaviour differs.
Every claim is marked with where it comes from. Nothing below is inferred from
how a memory tool "usually" behaves.

Two facts about the machine matter throughout:

- **The binary is the released 0.40.0**; the fork source is *ahead* of it. Do
  not reason about behaviour from source alone.
- **`knowledge` is a versioned table.** `is_current=1 AND is_deleted=0` is the
  live set. `knowledge_current` is the view that means "the entries".

## 1. The two scopes, and what actually reaches a session

`architecture.md` (Tier 3 — Long-term knowledge):

> "The LTM table stores five categories of curated entries, each carrying a
> scope — **per-project** (the default, scoped to the working directory) or
> **cross-project** (`cross_project: true`, available across every project the
> gateway sees). Per-project knowledge is always in play; cross-project entries
> join the search only when the scope is `all`, fused in rather than consulted
> as a strict fallback."

Five categories: **decisions, patterns, preferences, architecture, gotchas.**

Third scope, from `db.ts` migration v38 — user-level/global:

> - `project_id IS NULL` → user-level / `scope:"global"` entries (kept cross)
> - `promotion_status = 'promoted'` → auto-promoted across >=3 projects
> - everything else that the curator defaulted to cross → **demoted back**

So: **project-scoped**, **cross-project** (`cross_project=1`), **global**
(`project_id IS NULL`). Global is the right home for behavioural rules.

## 2. Curation is automatic, and the cap is the mechanism

`configuration.md`, `curator.maxEntries`:

> "Per-project knowledge entry ceiling. A generous backstop, not a quality gate:
> injection is already token-budget-capped, and the confidence lifecycle (decay +
> reinforcement) governs what stays. When exceeded, the lowest-value entries are
> evicted. **Default: 200.**"

Measured on this machine (2026-11-19): every populated project sits at or just
under 200. The cap is enforced and working.

`curator.ts:982` — the soft cap exists *because* merging is unreliable:

> "This breaks the old ratchet (creates frozen at the cap → consolidation can't
> reduce a genuinely-unique set → knowledge base frozen) **without relying on an
> LLM merge that will never succeed.** Eviction ranks by decayed confidence, so a
> create weaker than every incumbent self-evicts."

So the answer to "why 200 lessons instead of 20" is: **lore evicts rather than
merges.** The design deliberately avoids LLM-driven combination.

Other `curator` fields (`configuration.md`): `enabled` (true), `onIdle` (true),
`inFlight` (false — cache-sensitive providers), `afterTurns` (3),
`contextTokenBudget` (20000).

## 3. The documented curation surfaces

### `.lore.md` — the reviewable one

`team-memory.md`:

> "When the curator records a durable fact, Lore exports it to a `.lore.md` file
> at your project root... reviewed in pull requests."

- **Hand edits are first-class.** "Edit `.lore.md` directly: fix a wrong fact,
  delete a stale one, or add a convention by hand. It's imported on the next
  run."
- Entries carry `<!-- lore:UUID -->` markers, sorted alphabetically by title
  within category, so diffs stay minimal and merges stay rare.
- "`git diff` shows exactly what the agent learned this session."

**This is the supported manual curation path.** Editing `.lore.md` and letting
the next session import it is a supported workflow, not a workaround.

### `lore data` CLI

From `lore data --help` on the installed binary:

| Subcommand                | Role                                               |
| ------------------------- | -------------------------------------------------- |
| `list`, `show`            | Inspect                                            |
| `clear`, `delete`         | Remove                                             |
| `move <type> <id..> --to` | Re-attribute sessions or knowledge                 |
| `split`                   | Auto-suggest moving mis-grouped sessions           |
| `merge`                   | Merge duplicate projects by git remote             |
| `consolidate`             | Merge `(unattributed)` buckets into real projects  |
| `export`                  | Regenerate `.lore.md` from the DB                  |
| `recover`                 | Re-import from `.lore.md` / `AGENTS.md`            |
| `dedup`                   | Find and remove duplicate knowledge (all projects) |
| `contradictions`          | List contradicting entries                         |
| `reindex`                 | Rebuild embedding vectors                          |
| `rerank`                  | Re-score preference confidence                     |
| `vacuum`                  | Full VACUUM                                        |

Measured traps in this surface (2026-11-19):

- **`move` takes only the FIRST id.** `data.ts:2347` is
  `const rawId = rawIds[0];` — a 310-id invocation moves one entry and silently
  drops the rest. Loop per id.
- **`recover` only scans existing project rows.** A repo with a `.lore.md` and
  no row is skipped entirely. Running `lore recall` there first creates the row.
- **Subcommands execute rather than showing help.** `lore data export --help`
  runs the export.
- **`export` is lossy** — it wrote 163 of 201 distinct titles in one observed
  run. Never "sync" a `.lore.md` by exporting over it.

### Config that affects curation

`configuration.md`:

- **`curator.maxEntries`** — per-project ceiling, default 200.
- **`crossProject`** — "Include cross-project knowledge in compaction summaries
  and auto-promote knowledge that recurs across 3+ projects." Default `true`.
- **`workspaces`** — "Workspace sub-project paths or globs (relative to
  `.lore.json`). Imported into the root knowledge base on startup. Supports
  literal paths and single-level globs (e.g. `packages/*`)."
- **`knowledge.architectureInjection`** (`guides/tune-knowledge-injection.md`) —
  `ranked` (default) vs `reserved` (architecture notes get a 20% first pass).

Note `workspaces` is one-way inward, root ← children, and
`curator.ts:1051` gates cross-project promotion on
`cfg.crossProject && embedding.isAvailable()`.

## 4. What is NOT in the released binary

Verified by `strings` on `/Users/ben.davis/.local/bin/lore` plus live probes
against port 3207, 2026-11-19:

- `PATCH /api/v1/knowledge/:id` with `scope: "shared"` — **absent**.
  `handlePatchKnowledge` → 0 hits; the whole `routes/knowledge.ts` module is
  unmounted. `GET /api/v1/knowledge/search` returns "Knowledge entry not found:
  search", i.e. `search` is parsed as an `:id`.
- In source (`knowledge-edit.ts:345`) `scope: "shared"` maps to
  `cross_project = 1` and runs a title-conflict check. That path exists in the
  fork source but not in the shipped artifact.

So **there is no supported way to promote an entry to cross-project or global
scope from the CLI or API in 0.40.0.** The only routes are:

1. **Let the curator do it** — automatic, and gated on embeddings plus 3+
   projects at high confidence.
1. **Edit `.lore.md`** — the documented manual curation surface, project-scoped.
1. **SQL** — what the v38 migration itself does. Documented as a workaround,
   bypassing the conflict check and versioned-row write.

## 5. What this means for curating template-work lessons

Stated as consequences of the above, not as a plan:

- The **supported manual move is `.lore.md` editing**, per-repo. That is how a
  human is meant to curate.
- **Cross-repo sharing has no manual control in 0.40.0.** Promotion is the
  curator's job, driven by embeddings and a 0.935 similarity threshold. You
  cannot declare "these template lessons are shared" through a supported path.
- **`workspaces` is the only declared aggregation mechanism**, and it is
  one-way inward to a root. It was ruled out for this layout by the author's
  2026-11-19 decision (no `~/code/.lore.json`), and separately by the
  foreign-project guard in `_importEntries` (`agents-file.ts:670-677`), which
  silently skips entries already attributed to their own project.
- A curation pass over the template repos therefore has three honest outcomes:
  **delete**, **rewrite in place**, or **leave alone** — all via `.lore.md`.
  "Make this shared" is not one of them by any supported route.

## 6. Open questions, not answers

- Whether the released 0.40.0 runs cross-project promotion at all. Measured on
  this machine: 208 entries are `cross_project=1` with `promoted_at IS NULL` for
  **every** row. That is consistent with promotion never having run, but also
  with the binary simply not stamping `promoted_at`. **Unverified.**
- Whether the 199 entries imported into the loreai fork worktree on 2026-11-19
  are current knowledge or stale. They exist and the worktree exists; content
  quality was not assessed.
- Whether a curation pass is better done by hand on `.lore.md` (supported, slow)
  or by an agent driving `lore data move`/`delete` (faster, more judgement per
  row). The docs describe the first; the second is how this session's heal ran.
