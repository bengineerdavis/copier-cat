---
id: decision-11
title: Copy names new-project creation; assemble is retired as a CLI verb
date: 2026-11-22 21:24
status: accepted
---

## Context

decision-7 item 2 named **assemble** the single- or multi-template
project-creation workflow, and the shipped command is `ccc assemble
DESTINATION --stack STACK`.

While reviewing the command surface on 2026-11-22 the maintainer challenged
that name: `ccc` applying a stack to a new destination is the same act Copier
already calls `copy`, only with a wider input. Verification against the
installed Copier 9.19.1 confirmed its surface is `copy`, `recopy`, `update`,
and `check-update`, where `copier copy` is "Copy from a template source to a
destination."

The objection is not aesthetic. decision-6 requires every command's help to
teach its copier-native equivalent, enforced by a test. `ccc copy` →
`copier copy` is a one-word lesson; `ccc assemble` → `copier copy` needs a
paragraph explaining why two names exist for one act.

A second question followed from the same review: whether `ccc copy` should
accept an existing destination, as `copier copy` does.

## Decision

Accepted with the maintainer 2026-11-22 (Q17, Q18). This **reverses
decision-7 item 2** and is recorded as a new decision rather than an edit to
decision-7, whose accepted body is left intact.

1. **`copy` names new-project creation.** The command surface becomes
   `ccc copy DESTINATION (--template SOURCE | --stack STACK)`,
   `ccc adopt [PROJECT] (--template SOURCE | --stack STACK)`,
   `ccc upgrade [PROJECT] [--stack STACK]`, and
   `ccc stack new/edit/show/list`. `assemble` is retired as a CLI verb and
   survives only as the internal capability name for the composition stage
   (spec C8) and as a glossary term.
2. **`ccc copy` refuses an existing destination and points at `adopt`.**
   `copier copy` writing into an existing directory is the data-loss trap
   copier#2486 describes. Accepting existing destinations would force `copy`
   to become safe in exactly the way `adopt` already is, leaving `adopt` with
   no distinct purpose and erasing the difference between creating a project
   and changing one.
3. **`ccc stack assemble` is rejected.** Assembly creates a project, so it
   belongs to `copy`; `stack` operations modify reusable definitions.
4. **Version selection stays stack-pinned.** `upgrade` applies the versions a
   stack resolves and takes no ad-hoc per-template override, because that
   would diverge a project from its stack with no reviewable definition diff.
   Version changes are stack edits. Predictable version incrementation policy
   is an open question, not settled here.
5. **The specification is vendor-neutral by construction.** The stack
   specification defines sources, refs, answers, and application records
   against an abstract runner, confining runner-specific keys to a
   `runner` object. Copier is the only implemented runner; Cookiecutter,
   cruft, and other ecosystems' template libraries are motivations for the
   seam, not commitments. This extends decision-7 item 3 rather than adding
   multi-runner support.

## Consequences

`docs/stack-specification.md`, `docs/stack-protocol.md`, and
`docs/copier-cat-vs-copier.md` are the authoritative statements of the new
surface. The comparison document derives from the other two and must be
updated in the same change as either, so the two cannot drift.

Existing code and documents still say `assemble`: `src/copier_cat/cli.py`,
`spec.md` C8, `ROADMAP.md` Phase 2, `backlog/docs/cc-assembly-mvp-spec.md`,
`backlog/docs/cli-workflow-review.md`, and `GLOSSARY.md`. Migrating them is
implementation work with its own tasks, not part of this decision. Until then
the shipped command remains `ccc assemble`, and the protocol states plainly
which verbs are designed rather than built.

Renaming the CLI verb does not rename the capability. Composition,
contribution, attribution, and the two-stage conflict-resolution design are
unaffected.

The `upgrade` verb introduces a distinction adopt previously lacked: adopt
stamps a template once and refuses a second stamp, pointing at `upgrade`.
That matches copier#2486's meaning of adopt — a project with no baseline —
and keeps the upstream donation story intact, while `upgrade` owns the
native-equivalent story of `copier update`.

Two process notes from this session are worth keeping. decision numbering
collided across sibling branches: `decision-10` was created independently on
`docs/idempotency-immutability-principle` and on this branch. This record was
renumbered to 11, and its frontmatter id corrected by direct edit because
`backlog-py decision` offers only `create`. Decision ids therefore need
reconciliation when branches converge.
