---
id: decision-6
title: C6's enforcement mechanism is per-command copier equivalents in --help, enforced
  by a test
date: 2026-10-24 21:24
status: accepted
---

## Context

Spec C6's graduation principle — every cc operation is explainable in
copier terms, and a user who outgrows cc loses nothing — carried an open
gate: which mechanism enforces the explainability. The candidates were
per-command copier equivalents in docs/help, an `--explain` surface, or
skill-authored teaching sections. The mechanism had to be able to fail a
review, not just be an intention.

## Decision

The mechanism is per-command copier equivalents in `--help`, enforced by
a test. Every CLI command's help epilog carries a `Copier equivalent:`
section (what the command does in copier terms and why cc adds machinery
around it), usage examples, and its exit-code contract; a test iterates
the registered commands and asserts both markers in every help output,
so a commit adding a command without its teaching fails review.

This also answers the surface question: the help text is the primary
teaching surface (it is where a user already is when invoking the
command), and the README CLI-reference section mirrors it for the repo
surface. No separate `--explain` surface is built — the help is the
explain surface.

## Consequences

The enforcement test (tests/test_cli.py) is the C6 gate's teeth: a new
command without its copier-equivalent teaching fails CI, and the
graduation principle stops being an aspiration. The cost is upkeep —
when a command's semantics change, its epilog must change in the same
commit (the same state-change-sweep discipline the reviews already
police). The skill-authored teaching sections (C6's other half) now
compose on top of a documented CLI rather than substituting for one.
