---
id: decision-13
title: Reconcile decision-10 remediation with decision-11 convergence semantics
date: 2026-11-23 07:26
status: accepted
---

## Context

decision-10 (accepted 2026-11-22) added principles 6 and 7 to the
constitution and asserted that C1 adopt already satisfies them and that
C8 assembly satisfies them. That assertion is factually false: measured
2026-11-22 (review 746), repeated adopt re-renders, re-merges, and
re-stamps — two identical runs against a conflicted project produced
nested conflict markers — and overwrites (accepted conflicts, binary
replacements, answers-file stamping) carry no restorable backup;
assembly refuses an existing destination outright. decision-11
(accepted 2026-11-22, on main) independently ruled the verb semantics:
adopt stamps once, refuses a second stamp, and points at upgrade; the
new-project surface (assemble today, copy after CCC-37) refuses an
existing destination and points at adopt. Reviews 753 and 755 flagged
that remediation tasks written as "no-op or reviewed reconciliation"
would reverse decision-11, and review 758 required the correction live
in a superseding record rather than as an edit to decision-10's
accepted body.

## Decision

Both decisions stand. decision-10's compliance claim is factually
corrected here rather than edited in place: adopt and assembly do NOT
yet satisfy principles 6 and 7. Refusal-with-pointer IS the convergence
principle 6 requires — same inputs, same refusal, zero state change.

1. **Adopt converges by refusing.** The second-stamp guard implementing
   decision-11's stamp-once rule satisfies principle 6; no
   reconciliation path is added. The backup gap remains real: the first
   stamp takes a restorable backup before overwriting project content.
2. **Assembly converges by refusing.** The existing-destination refusal
   implements decision-11 item 2 and satisfies principle 6 once it is
   explicit and machine-readable with an adopt pointer — never a bare
   error, never a write into the existing tree.
3. **Task ownership.** CCC-39 owns the adopt remediation and its own
   regression tests; CCC-40 owns the assembly remediation and its own
   regression tests; CCC-35 owns the cross-operation coverage
   (partial-failure resumability, repeated-run final verification) and
   depends on both. Each remediation task is self-contained.

## Consequences

decision-10 is restored verbatim to its accepted body, so it carries no
forward link to this record; a reader of decision-10's original
compliance claims finds the correction here by date (this record is the
only later decision addressing principles 6 and 7 remediation). This
record supersedes only the remediation interpretation — neither accepted
ruling is reversed. CCC-39/CCC-40 acceptance criteria cite this record
for their convergence semantics.
