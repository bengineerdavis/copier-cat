# How the community handles agent config across related repos

**Question:** with seven sibling git repos under `personal/templates/` — one of
which (`agentic-project-template`) stamps the others — should there be a
**parent-directory agent config**, or per-repo config kept uniform?

**Short answer:** every major agent tool resolves instruction files by walking
**up** from the working directory, and stops at the project/repo root or the
home directory. That makes a parent config work for **monorepo nesting**
(parent → child inside one repo) and **not** for coordinating **independent
sibling repos**, because a session inside repo B never consults a file that
"belongs" to the parent of repos A–G as a project config — it only arrives via
the generic walk-to-home, which is not scoped to the templates family at all.

There is **no community consensus endorsing a parent config for sibling
repos**, and the standards literature explicitly frames nesting as a monorepo
feature. The supported mechanism for template → instance propagation is the
template tool's own update path, which this repo already uses.

______________________________________________________________________

## 1. AGENTS.md — the cross-tool format

`https://agents.md` (stewarded by the Agentic AI Foundation under the Linux
Foundation; adopted by OpenAI Codex, Cursor, Amp, Jules, Factory, OpenCode,
Zed, Warp, VS Code, Devin, and others).

**REPORTED** — nesting is described only in monorepo terms:

> "Large monorepo? Use nested AGENTS.md files for subprojects. Place another
> AGENTS.md inside each package. Agents automatically read the nearest file in
> the directory tree, so the closest one takes precedence and every subproject
> can ship tailored instructions. For example, at time of writing the main
> OpenAI repo has 88 AGENTS.md files."

**REPORTED** — conflict semantics: "The closest AGENTS.md to the edited file
wins; explicit user chat prompts override everything." (Note: this is the
format's *stated* rule; the tools below are more specific and differ.)

**REPORTED** — scale claim: over 60k open-source repositories carry an
`AGENTS.md`.

The spec defines **no** mechanism for a file shared across sibling
repositories. Nesting is the only inheritance story, and it assumes one repo.

## 2. OpenCode

`https://opencode.ai/docs/rules` (MEASURED against this machine's sessions,
2026-11-19).

**REPORTED + MEASURED** — instruction resolution walks up and stops:

> "OpenCode loads the global file followed by every AGENTS.md from the current
> workspace directory toward the home directory. For workspaces outside the
> home directory, it stops at the project root."

MEASURED consequence in this session: cwd `copier-cat` loads
`copier-cat/AGENTS.md` → `templates/` (absent) → `personal/AGENTS.md` →
`~/code/AGENTS.md` → home. Three files actually arrived: copier-cat's real one
plus two 330-byte lore stubs. So `~/code/AGENTS.md` **is** an operative
cross-sibling channel today — but it is the home-walk, not a project config,
and it reaches `work/` too.

**REPORTED** — merge is additive, conflicts unresolved: "OpenCode combines the
files and does not resolve conflicts between them."

**REPORTED** — config resolution (different from instructions) searches cwd to
the **filesystem root**, "including directories above the detected project or
repository root", and **"every discovered `.opencode` config overrides every
discovered direct config"** regardless of depth. MEASURED in this repo: that
asymmetry is exactly why `copier-testkit` and `copier-template-copier-template`
(`.opencode/` form) would override a direct `templates/opencode.json` that
`copier-mise-sandbox` and `agentic-project-template` (root form) would inherit.

## 3. Claude Code

`https://code.claude.com/docs/en/memory` (REPORTED).

**REPORTED** — upward walk, additive, ordered root→cwd:

> "Claude Code loads CLAUDE.md and CLAUDE.local.md from your current working
> directory and every directory above it... All discovered files are
> concatenated into context rather than overriding each other."

**REPORTED** — monorepo escape hatch exists, and it *excludes* rather than
inherits: "If you work in a large monorepo where other teams' CLAUDE.md files
get picked up, use `claudeMdExcludes` to skip them." This is the community
telling you that upward-walking config **leaks in monorepos**, and the
sanctioned response is to prune, not to curate a parent.

**REPORTED** — size guidance: "target under 200 lines per CLAUDE.md file.
Longer files consume more context and reduce adherence." Path-scoped rules
(`.claude/rules/` with `paths:` frontmatter) are the documented way to avoid
inflating the always-loaded file.

**REPORTED** — conflict warning, directly relevant to a layered design: "if
two instructions contradict each other, Claude may pick one arbitrarily."

## 4. VS Code / GitHub Copilot

`https://code.visualstudio.com/docs/agent-customization/custom-instructions`
(REPORTED).

**REPORTED** — the most useful line found, and it is a refusal:
"Don't rely on a universal precedence order: combination rules differ by
harness."

**REPORTED** — activation scopes are *project-wide* and *file-pattern*
(`applyTo` in `.github/instructions/*.instructions.md`), not
*parent-directory*. Personal guidance is user-scope; org guidance is managed.

Implication: a design whose correctness depends on precedence across layers is
not portable across tools. Project + path-pattern is the portable subset.

## 5. Copier — template → instance propagation

`https://copier.readthedocs.io/en/stable/updating/` (REPORTED).

This is the case that actually matters here, because `agentic-project-template`
generates the siblings. Copier's answer is not "a parent config" — it is
**ship the file in the template and update by three-way merge**:

- **REPORTED** — `copier update` regenerates a fresh project at the current
  template version, diffs it against the project, and applies that diff, so
  template changes reach instances without clobbering local work.
- **REPORTED** — "Template-based files/directories that were deleted in the
  generated project are automatically excluded from updates." Deleted means
  deliberately removed locally; Copier respects that.
- **REPORTED** — the exception that matters for presence-guaranteed files:
  paths matched by `skip_if_exists` have their presence "always ensured, even
  during an `update` operation."
- **REPORTED** — `.copier-answers.yml` must never be edited by hand; doing so
  breaks the smart-diff algorithm and is explicitly unsupported.
- **REPORTED** — `copier recopy` discards the smart update and behaves like a
  first-time application while keeping answers; the documented recovery path
  when an update breaks.

**Conclusion for this repo:** the propagation mechanism for agent config into
stamped projects is `copier update`, not a shared parent file. The template
already does this correctly — `template/.opencode/opencode.json.jinja` is
stamped, and `tests/test_stamp.py:76` asserts a fresh stamp contains
`.opencode/opencode.json` and `.opencode/agents/review-deep.md`.

## 6. Does anything support config across SIBLING repos?

**Nothing found.** Checked mechanisms, all upward from cwd:

| Tool                  | Walk                  | Stop condition              | Sibling support                         |
| --------------------- | --------------------- | --------------------------- | --------------------------------------- |
| AGENTS.md spec        | nearest file wins     | —                           | none defined; nesting = monorepo        |
| OpenCode instructions | up to home            | project root (outside home) | only via home-walk, unscoped            |
| OpenCode config       | up to filesystem root | —                           | none (not scoped to a family)           |
| Claude Code           | up to fs root         | —                           | none; `claudeMdExcludes` prunes leakage |
| VS Code               | project root          | —                           | none; project + globs only              |
| dotagents             | project or global     | `<repo>/agents.toml`        | none — project scope is per-repo        |

The honest answer to "how does the community handle sibling repos with a
relationship" is: **they don't do it with agent config.** They do it with the
generator (Copier update), or with a human-facing README, or by accepting a
shared org-level file that is deliberately not repo-shaped.

## Failure modes of parent/nested config (documented, not invented)

1. **Silent override inversion** — OpenCode: `.opencode/` beats direct
   `opencode.json` at any depth. A shallow `.opencode/` silently outranks a
   deeper direct file.
1. **Leakage into unrelated projects** — Claude Code documents
   `claudeMdExcludes` specifically because upward walking pulls in other
   teams' files. A `templates/` parent inherits into all seven repos,
   including ones with no agent config today.
1. **Arbitrary conflict resolution** — Claude Code: "Claude may pick one
   arbitrarily." OpenCode: "does not resolve conflicts between them."
1. **Generated-file clobbering** — Copier: hand-edited `.copier-answers.yml` is
   unsupported; deleted template paths are excluded from updates, so a file
   you delete locally stops receiving updates.
1. **Context inflation** — Claude Code's 200-line guidance per file; every
   extra always-loaded layer costs adherence.
1. **Non-portability** — VS Code: "combination rules differ by harness."

## Recommendation

**Do not add a parent-directory agent config at `templates/`.**

Ranked against the requirement — *"make agent config coherent across seven
related repos without duplicating it"* — leading with the disqualifying
capability (**does the mechanism actually reach a session working in a
sibling repo?**):

1. **Keep per-repo config, one form throughout** (recommended). Every repo
   uses `.opencode/opencode.json`. Already the template's stamped behaviour and
   test-pinned. Closes the drift that existed (`copier-mise-sandbox` was the
   only root-form repo). *Reaches sessions: yes, per repo. Duplication: only
   `$schema` + a per-repo `.context/` path list, which a parent cannot supply
   anyway.*
1. **`~/code/AGENTS.md` for genuinely shared prose** — already works, already
   loads into every session. Constraint: no employer-identifying content,
   since `~/code` also holds `work/`. *Reaches sessions: yes, all of them.*
1. **A parent `templates/opencode.json`** — rejected. It would be overridden by
   the two `.opencode/`-form repos and inherited by the root-form ones, i.e. it
   reproduces the exact split being fixed; and it silently reaches `copier-cat`,
   which has no config today. *Reaches sessions: inconsistently, which is worse
   than not at all.*
1. **dotagents project scope across all seven** — rejected as a coordination
   layer. Project scope is per-repo `<repo>/agents.toml` by design; there is no
   umbrella scope. Using it would mean seven declarations plus a sync story,
   which is more duplication, not less.

**For template → stamped-project propagation, use Copier.** That is the
documented, supported path and this repo already implements it. Anything else
(hand-editing stamped config, a shared parent, a sync script) competes with
`copier update` and will lose to it or corrupt the three-way merge.

## What remains unverified

- **REPORTED, not MEASURED:** whether OpenCode's home-walk reaches
  `~/code/AGENTS.md` for a session launched *outside* `~/code` (docs say the
  stop is the project root for workspaces outside home).
- **Not measured:** whether a `templates/opencode.json` in `.opencode/` form
  would actually reach all seven repos (the precedence rule implies yes; no
  probe was run, and the recommendation does not depend on it).
- **Not measured:** real-world sibling-repo setups. No public repo was found
  that explicitly documents coordinating agent config across independent
  sibling git roots — the absence is the finding, and it is an absence of
  evidence, not proof that nobody does it.
