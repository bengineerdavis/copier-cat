---
id: decision-5
title: Marked-region preservation is a merger provider, not a rival architecture
date: 2026-10-18 17:05
status: accepted
---

## Context

copier-uv-bleeding (detailobsessed, PR #329 at `9a80874`, v0.41.2)
implements the alternative C1 architecture HANDOFF flagged:
`_skip_if_exists` on mixed files plus a `_tasks` migration that
regenerates them fresh on every update while splicing
`# template-preserve:<name>:start/:end` regions back byte-for-byte.
copier upstream is also moving: PR #2762 (open, preview-leaning) adds a
Jinja `{% ignore %}` tag so developer-owned regions survive
`copier update` natively. CC-2 (2026-10-18) evaluated the mechanism
against the merger-registry interface; evidence in
backlog/docs/prior-art.md and the task's implementation notes.

## Decision

The mechanism is another merger provider, not a rival architecture —
decision-1's registry holds. cc does not adopt the
regenerate-and-splice architecture and does not port the template's
script: a uv-bleeding-style template enters the way
`MarkedSectionMerger` already does, as a composed provider with the
template's own markers (no cc marker conventions, no cc residue). Two
provider generalizations are required before such a template can be
served — name-bearing marker patterns (the current `Markers` is one
literal pair) and an explicit region-body orientation (uv-bleeding's
regions are user-owned; cc's marked regions are template-owned — same
marker shape, opposite precedence) — and they are deferred until cc
adopts a template that needs them (backlog draft, safe default: defer).
Update-time region preservation belongs to copier upstream: track #2762,
do not rival it; cc's registry stays adopt-time.

## Consequences

The spec's C1 marked-region gate closes with this decision: the
same-commit removal is this decision's own closure requirement,
executed on the decision log's constitution-ledger precedent — the
recorded decision is the closure, and the spec edit in the same commit
is its execution. cc's TOML merger already covers uv-bleeding's tool-owned
scalar problem structurally (project values win conflicts at adopt), so
no scalar pass is ported; the legacy bootstrap stays template-side. If
#2762 lands, marked-region templates get native update survival and cc's
provider matters at adopt only; if it stays open, cc's adopt-time
provider still leaves plain `copier update` working afterwards (C1's
stamped-project guarantee), which is the boundary cc promises.
