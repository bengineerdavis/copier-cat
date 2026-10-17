---
id: decision-4
title: Shared data builds on copier's sanctioned primitives
date: 2026-10-17 14:00
status: accepted
---

## Context

copier has `!include` in `copier.yml` (glob-capable, documented merge
semantics) and `_external_data` for reading another template's answers
file; what is missing is cross-repo sharing without vendoring,
conditional includes (#1076), and inheritance (#934). The
shared-config-as-submodule practice is workaround, not mechanism
(prior-art.md). Decided grill round 1 (2026-10-15); recorded late
2026-10-17 when the thin spec cited the decision without a durable
store record.

## Decision

Shared data across a collection builds on copier's sanctioned
primitives: a shared answers file seeded via `--data`, `!include` for
question reuse. cc composes with `!include`/`_external_data` rather
than replacing them; no cc-invented injection mechanism becomes a
prerequisite for a template to work (PRINCIPLES principle 5).

## Consequences

Templates that ignore cc's conveniences remain fully usable by plain
copier and cc alike; shared data rides on mechanisms copier documents
and maintains. The open upstream asks (#1076, #934) may later expand
what "sanctioned" covers — this decision composes with those rather
than racing them.
