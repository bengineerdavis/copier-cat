---
id: decision-3
title: 'Chooser approach: cc invokes collection templates by local path'
date: 2026-10-17 14:00
status: accepted
---

## Context

copier's official position is 1 template = 1 git repository (tags are
repo-global; update machinery depends on them); remote URLs cannot
address a template inside a subdirectory. Prior art (backlog/docs/
prior-art.md, monorepo section): every verified multi-template repo in
the wild clones and invokes by local path, and a copier maintainer
floated subdir-addressable URLs as something that "could actually work"
— unimplemented. Decided grill round 1 (2026-10-15); recorded late
2026-10-17 when the thin spec cited the decision without a durable
store record.

## Decision

cc's chooser approach: clone the collection and invoke templates by
local path. No subdir-addressable remote URL requirements — that idea
stays open as a future option (it belongs to copier, and PRINCIPLES
principle 3 says cc prototypes in donatable shapes rather than
forking), not foreclosed by this decision.

## Consequences

cc is additive to copier: no new URL semantics are demanded of
templates or users. The cost every wild collection accepts: degraded
versioning (repo-global tags) and clone-then-local-path ergonomics,
which the chooser flow exists to smooth.
