# copier-cat vs copier

Start here if you are deciding whether you need `ccc`, or trying to work out
which tool owns a task. This document is derived from the
[stack specification](stack-specification.md) and
[stack protocol](stack-protocol.md); if it disagrees with them, they are
right and this file is stale.

`copier-cat` is the package and full executable name. `ccc` is its built-in
alias. `cc` is never used — that is the system C compiler.

> **Read this first: what exists today.** This document describes the target
> design, and some commands below are **not built yet**. Shipped today:
> `adopt`, `assemble`, `merge`, `mergers`, `stack list`, `stack show`.
> **Designed, not built:** `copy`, `upgrade`, `stack new`, `stack edit`.
> The shipped new-project command is still `ccc assemble`; `copy` is its
> planned replacement ([decision-11](../backlog/decisions/decision-11%20-%20Copy-names-new-project-creation-assemble-is-retired-as-a-CLI-verb.md)).
> [ROADMAP.md](../ROADMAP.md) is the authoritative shipped-versus-planned
> surface, and the migration is tracked in
> [Migrate the CLI verb from assemble to copy](../backlog/tasks/ccc-37%20-%20Migrate-the-CLI-verb-from-assemble-to-copy.md).
> The promises in "What still works if you stop using `ccc`" are requirements
> under test, not yet demonstrated — that evidence is
> [Prove the no-lock-in boundary on dummy projects](../backlog/tasks/ccc-38%20-%20Prove-the-no-lock-in-boundary-on-dummy-projects.md).

## The one-paragraph version

Copier renders a project from one template and updates it afterwards.
`ccc` manages the lifecycle *around* that: adopting a project that was never
stamped, composing several templates into one project, and carrying your
improvements back to the source template. `ccc` never renders anything itself
— it orchestrates Copier's renders.

## Who owns what

| Capability | Owner |
| --- | --- |
| Render one template | **Copier** |
| Update one stamped template | **Copier** |
| Three-way merge with a known baseline | **Copier** |
| Adopt with no baseline (empty tree as merge base) | **`ccc`** |
| Compose several templates deterministically | **`ccc`** |
| Backup, quarantine, and restore | **`ccc`** |
| Prepare and publish changes back to a template | **`ccc`** |
| Commit, push, or merge a pull request | **Neither — always you** |

Two boundaries are worth memorizing:

- **Copier never knows what a stack is.** It sees one template and one answers
  file at a time.
- **`ccc` never renders.** It resolves, composes, validates, and reports;
  Copier does the rendering and the native per-template updating.

## Which command do I want?

| You want to… | With Copier | With `ccc` |
| --- | --- | --- |
| Apply template(s) to a **new** directory | `copier copy SRC DEST` | `ccc copy DEST (--template SRC \| --stack STACK)` |
| Bring an **existing** project under a template, without losing your work | Not available upstream (copier#2486) | `ccc adopt [PROJECT] (--template SRC \| --stack STACK)` |
| Move to a newer template version, keeping your changes | `copier update -a ANSWERS_FILE` | `ccc upgrade [PROJECT] [--stack STACK]` |
| Throw away your changes and re-render | `copier recopy` | Not offered — `ccc` will not destroy state without a backup |
| Check whether you are behind | `copier check-update` | `ccc upgrade --dry-run` |
| See or edit a reusable stack | No equivalent | `ccc stack show/new/edit/list` |

`ccc copy` refuses an existing destination and points you at `adopt`. That is
deliberate: `copier copy` writing into an existing project is exactly the
data-loss trap described in copier#2486, and `ccc` exists partly to close it.

`ccc adopt` stamps a template once. Asking it to adopt the same template again
refuses and points at `upgrade`.

## What a stack buys you

A stack is an ordered composition of ordinary templates. One template is a
valid stack and needs no extra configuration, so you do not have to think
about stacks to use a single template — `ccc` builds a trivial one internally.

You would name and keep a stack when you want to:

- apply the same set of templates to more than one project;
- pin versions and move them deliberately, with a reviewable diff;
- see which template contributed what when two of them touch the same file.

A stack definition is **reusable input**, not something your project must
carry around. It is not template inheritance, and your project does not become
a hybrid template.

## What still works if you stop using `ccc`

This is the promise that matters most, so it is stated as a table rather than
a reassurance. Everything in the "yes" rows is covered by observable tests,
not just intent.

After `ccc` has applied a stack, with `ccc` removed:

| You want to… | Plain Copier |
| --- | --- |
| Update one stamped template via its answers file | **Yes** |
| Update several stamped templates | **Yes**, as separate commands you run yourself |
| Update a template added by a later stack extension | **Yes**, once that extension was applied and stamped |
| Discover and apply a *new* stack extension | **No** — needs `ccc`, or a manual native equivalent |
| Reproduce whole-stack composition or attribution reports | **No** |
| Resume an interrupted multi-template application as one step | **No** |
| Remove a template and everything it contributed | **No** — `copier update` does not do this |
| Resolve new cross-template conflicts automatically | **No** — conflicts stop for your review, in either tool |

**`ccc` adds orchestration. Removing it costs you orchestration, never the
per-template lifecycle.** If you ever find a case where deleting `ccc` and its
provenance breaks `copier update -a ...` on a stamped template, that is a bug
against this promise, not a limitation to accept.

Note the timing distinction: extending a stack *with* `ccc` and then leaving
is fully supported. Extending a stack *after* leaving is a manual per-template
Copier workflow, because Copier has no stack membership to extend.

## What `ccc` will never do

- Push, merge, or commit without your explicit yes at the moment of action.
- Modify your project or publish anything without reviewable consent.
- Silently overwrite your work, or destroy it without a restorable backup.
- Silently choose a winner when two templates disagree.
- Rewrite an accepted record in place; corrections supersede.
- Ask a template to cooperate in order to classify your files.
- Publish automatically. `contribute prepare` and `contribute publish` are two
  separate commands, and publishing uses your own `gh` auth.

`ccc` uses deterministic machinery for merges, diffs, and classification. An
agent may *suggest*, but never acts as the merge engine, and its suggestions
are always reviewable.

## Terminology worth learning

- **Stamped project** — a project with a valid answers file and a recorded
  baseline, so plain `copier update` works on it.
- **Adopt** — bringing an existing project under a template without data loss.
- **Baseline** — the recorded template state your future updates merge against.
- **Stack** — an ordered composition of project templates.
- **Composition** — combining identified contributions into valid shared
  files, deterministically, with explicit precedence or review.
- **Contribute** — preparing, and only after approval publishing, a
  template-worthy change back to its source template.

The full vocabulary lives in `GLOSSARY.md`.
