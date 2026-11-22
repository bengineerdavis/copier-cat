# Stack protocol

Status: draft, version 0.1. Owner: bdavis. Last reviewed 2026-11-22.

The operations over the artifacts in the
[stack specification](stack-specification.md). Read that document first; this
one defines behavior, consent scope, and failure semantics. The user-facing
[copier-cat vs copier](copier-cat-vs-copier.md) derives from both.

Nothing here is implemented unless the [command surface](#command-surface)
marks it shipped. The verified baseline: `adopt`, `assemble`, `merge`,
`mergers`, `stack list`, and `stack show` exist; `copy`, `upgrade`,
`stack new`, and `stack edit` are designed, not built.

## Operations

Seven operations, all available to humans and agents with identical
semantics. None of them commits, pushes, or opens a pull request.

| Operation | Reads | Writes | Consent |
| --- | --- | --- | --- |
| `resolve` | Stack definition, catalog, runner metadata | Nothing | None; may require separate approval to download an unknown source |
| `validate` | Resolved plan, rendered preview | Preview only | None beyond preview creation |
| `preview` | Same as validate, plus composition | Preview only | Never writes the destination |
| `apply` | Approved plan | Exactly the approved write scope | Explicit, at the moment of the write |
| `diff` | Stamp record, current resolved inputs | Nothing | None |
| `upgrade` | Stamp record, stack definition | One subproject | Explicit, project scope only |
| `inspect` | Definitions, records, reports | Nothing | None |

`resolve`, `validate`, `preview`, `diff`, and `inspect` are read-only with
respect to the user's project. They must never prompt for project writes,
initialize user configuration, or download a source without separate
approval.

## Command surface

`copier-cat` is the package and unambiguous executable; `ccc` is the built-in
local alias. `cc` is never used — it is the system C compiler.

| Command | Target | Native equivalent | Status |
| --- | --- | --- | --- |
| `ccc copy DESTINATION (--template SOURCE \| --stack STACK)` | A **new** project | `copier copy` | Designed |
| `ccc adopt [PROJECT] (--template SOURCE \| --stack STACK)` | Existing project, first stamp | copier#2486 (does not exist upstream) | `adopt` shipped; `--stack` designed |
| `ccc upgrade [PROJECT] [--stack STACK]` | One already-stamped subproject | `copier update -a ANSWERS_FILE` | Designed |
| `ccc stack new/edit/show/list` | Reusable definitions and catalog | None; Copier has no stack concept | `show`/`list` shipped |

Three verbs, three different acts, and the native equivalents are the
teaching surface required by decision-6. `copy` creates, `adopt` brings an
existing project under a template, `upgrade` moves versions. `assemble` is
retired as a CLI verb (Q17, 2026-11-22) and survives only as the internal
capability name for the composition stage.

`ccc stack assemble` is rejected: assembly creates a project, so it belongs
to `copy`, while `stack` operations modify definitions. Two commands for one
act would be a second engine by another name.

### `copy` refuses existing destinations

`copier copy` writes into an existing directory, which is precisely the
data-loss trap copier#2486 describes. `ccc copy` refuses an existing
destination and points at `adopt` (Q18, 2026-11-22). The sharp edge stays on
Copier's side, and `adopt` retains a distinct purpose.

### Target discovery

`PROJECT` is optional. When omitted, `ccc` selects the nearest unambiguous
stamped project at or above the current directory (Q15, 2026-11-22).

A `.git` entry is **not** sufficient evidence: linked worktrees carry a
`.git` file rather than a directory, the command may run in a subdirectory,
one repository may hold several independently stamped projects, and an
ordinary repository may hold none. Ambiguous discovery is an error, never a
guess and never an implicit batch.

One subproject per invocation. Batch upgrades, if added later, orchestrate
that primitive with separate previews, approvals, backups, and failure
reports — they do not widen a single command's consent scope.

## Two-stage conflict resolution

Adopt and upgrade into an existing project resolve conflicts in two separate,
separately reviewable stages (Q13, 2026-11-22).

1. **Template compatibility.** Render each member in an isolated preview and
   compose contributions. Report shared-file collisions, precedence choices,
   unsupported overlaps, and the questions needed to settle them.
2. **Project application.** Only after template composition is resolved,
   show the changes against the existing project, including local drift and
   the backup and restore scope.

Neither stage writes. Unsupported overlaps stop for review; `ccc` never
claims automatic semantic resolution, and never concatenates completed
structured files or silently picks a winner.

Both `adopt` and `copy` call the **same composition library**. They differ in
apply target, not in composition engine. This corrects the earlier framing
that adopt used live merge while assembly used isolated composition: both
already render in isolation.

## Idempotency and recovery

Principles 6 and 7 (`decision-10`) bind every operation here.

- Repeating an operation with unchanged resolved inputs performs **zero
  writes**, including no rewrite of native answers files. No-op detection
  follows the two tiers in the specification.
- Version detection is *conditional* idempotency: a new resolved ref is new
  work, not a no-op. `upgrade` exists for exactly that case.
- `adopt` stamps a template only once. Re-invoking it for an already-stamped
  member refuses and points at `upgrade`.
- Partial failure records `partial` and which members were applied, so the
  next run resumes rather than re-applies.
- Before any destructive project write, `ccc` takes a restorable backup.
  Removed content goes to quarantine, the only staging area, and restore is a
  first-class operation. Reset and restore requirements are owned by CCC-34 on
   `docs/idempotency-immutability-principle`;
  this protocol does not invent them here.

## Combined stack-and-project operations

Stack changes and project changes have different consent scopes, so they stay
separate by default. A combined form is allowed only as explicit opt-in
orchestration (Q10, 2026-11-22):

- the stack-definition diff and the project diff are shown separately;
- preview performs no writes;
- approval names **both** write scopes, and approves nothing else;
- the implementation runs the existing stack-edit and upgrade operations, not
  a third path;
- partial failure is reported as such and leaves a resumable plan.

Plain `ccc upgrade PROJECT --stack STACK` never modifies the stack
definition. Exact flag spelling for the combined form is an implementation
detail, deliberately not settled in this document.

## Human, scripted, and agent use

One versioned result schema per command, shared by human help and
`--json`. JSON without an approval flag is a read-only preview. Help and
discovery never initialize configuration, download, render, or write.

The maintainer requires observable user testing on dummy projects before this
workflow is treated as settled (Q12–Q13, 2026-11-22), covering human,
scripted, and agent-driven paths. Evidence to capture per scenario: commands,
output, exit status, before/after file hashes, diffs, native answers files,
and native update results. Test classes at minimum: unchanged inputs with
clean and locally modified projects; changed versions, answers, ordering, and
composition rules; mutable refs whose contents moved; stack extension
followed by `ccc` removal; independent native updates afterward; interruption
part-way through; duplicate runs; backup and restore; unsupported conflicts;
and nested projects, subdirectories, worktrees, and ambiguous discovery.

## Runner neutrality

Operations are defined against the abstract runner seam in the specification.
A runner that cannot express an operation reports it unsupported; the
protocol never silently narrows what the user asked for. Copier is the only
implemented runner, and templates are never redesigned around a hypothetical
second one (decision-7 item 3).
