---
id: decision-10
title: Idempotent operations and non-destructive, append-only change
date: 2026-11-22 17:09
status: accepted
---

## Context

The maintainer declared on 2026-11-22, verbatim:

> Agreed that idempotency is one of the guiding principles for this project
> and the tool it produces. Immutability must be a first class feature; minus
> any practical exceptions.

`PRINCIPLES.md` carried no such principle. Idempotency appeared only in
scattered, capability-local places: `decision-9` for skill installation,
`spec.md` C6 for init, and `CCC-12` for composition validation. Nothing
governed operations generally.

The 2026-11-08 prototype already encoded both ideas as behavior rather than
principle: re-adopting an adopted template is a no-op, migrate backups before
`--apply` and imports nothing twice on rerun, reset requires a restorable
backup, quarantine is the only staging area for content it removes, and
publishing is per-proposal. Those behaviors were never promoted to the
constitution, and reset and migrate do not appear in `spec.md` at all.

The maintainer clarified on 2026-11-22 that backups and immutability are
qualities of the tool cc is building, alongside idempotency. These principles
govern what cc does to a user's project and to that project's own records —
its answers files, provenance, quarantine, and backups. They are not a rule
about how cc's own repository is edited.

Two senses of immutability matter for the tool and are kept distinct: the
project's working state is never destroyed without a way back, and the records
cc writes into a project are not silently rewritten in place.

The maintainer chose to keep practical exceptions out of the constitution: the
principles state the ideal, and each capability's requirements in `spec.md`
carry its own exceptions.

## Decision

Accepted with the maintainer 2026-11-22. Add two principles to `PRINCIPLES.md`:

6. **Idempotent operations.** Repeating an operation with unchanged inputs
   converges on the same state and does not duplicate its effects. Re-adopting
   an already-adopted template, re-preparing a changeset, and re-running a
   validated composition are no-ops or produce only new work. Partial failure
   leaves the operation resumable rather than half-applied.

7. **Non-destructive change with a way back.** cc never destroys a project's
   working state without a restorable backup taken before the write. Content cc
   removes goes to quarantine, which is the only staging area, and restore is a
   first-class operation. Records cc writes into a project — answers files,
   provenance, backups, quarantine manifests — are not silently rewritten in
   place; a corrected record supersedes the one it replaces.

Practical exceptions live in `spec.md` per capability, not in the constitution.
This follows principle 4: the constitution states the ideal, and ambiguity is
marked with a safe default and an owner rather than resolved silently.

## Consequences

Existing requirements are unaffected in text but now derive from a principle:
`decision-9` and `spec.md` C6's idempotent setup become instances of principle
6 rather than isolated requirements.

`spec.md` C1 adopt and `spec.md` C8 assembly do not yet satisfy these
principles, and this decision does not claim they do. Measured 2026-11-22
(review 746): repeating an identical `adopt --defaults --accept-all --json`
run against a conflicted project re-renders, re-merges, and re-stamps —
two identical runs produced nested conflict markers rather than
convergence, and accepted conflicts, binary replacements, and answers-file
stamping overwrite project content without a restorable backup. Assembly
previews converge for unchanged inputs but repeated assembly against an
existing destination is refused rather than reconciled. Adopting these
principles makes those behaviors spec gaps, not compliant baselines.
CCC-39 owns the adopt remediation: a second-stamp guard implementing
decision-11's stamp-once rule (refuse, change nothing, point at
upgrade), plus restorable backup before overwrites. CCC-40 owns the
assembly remediation: make the existing-destination refusal explicit
and adopt-pointing per decision-11 item 2 — refusal-with-pointer is the
convergence principle 6 requires, not a gap to remove. CCC-35 owns the
regression tests for both, verifying the remediated behaviors rather
than pinning the current defects. Until CCC-39 and CCC-40 land, adopt's
non-convergence and assembly's bare refusal are recorded gaps — not
exceptions, because no exception has been approved.

Two gaps are now visible against the principles and have their own tasks:

- **No reset capability exists in `spec.md`.** The prototype's reset, with its
  required restorable backup and separate restore verb, has no requirements
  home. Principle 7 makes that omission a spec gap rather than a design taste.
  CCC-34 owns the requirements.
- **Idempotency is untested as a property of the public operations.** The
  prototype's walkthrough `apply()` double-applied on Previous-then-Run,
  producing a duplicate overlay. Merger-level coverage exists on `main` —
  `tests/test_mergers.py` `test_toml_merge_is_idempotent` performs a second
  merge and asserts identical output with no warnings — but no test asserts
  that repeating a public operation (adopt, assemble) converges, so
  principle 6 currently has no enforcement at the operation level. CCC-35
  owns the tests, scoped to the uncovered public operations.

This decision does not govern cc's own repository housekeeping. How
`backlog/decisions/` and other project documents are corrected remains ordinary
maintainer practice, not a consequence of these principles.
