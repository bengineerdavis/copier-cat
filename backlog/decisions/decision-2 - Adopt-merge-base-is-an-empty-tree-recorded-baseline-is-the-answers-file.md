---
id: decision-2
title: Adopt merge base is an empty tree; recorded baseline is the answers file
date: 2026-10-17 05:29
status: accepted
---

## Context

These are two decisions often fused into one phrase, and keeping them
distinct is the point. copier#2486's MVP presents the empty base as one
of two adopt-time merge formulations and closes adopt by writing answers
that make updates work. The first committed version of this decision
(ADR 0002, 2026-10-15) conflated them — roborev review #5.1 caught it —
and was restated the same day. Migrated from docs/adr/0002 in the
backlog-workflow switch (2026-10-17).

## Decision

Adopt-time merge base: an empty tree — template files arrive as fresh
additions resolved against the project's current content, each
resolution reviewed per-file. Rejected: template initial version
(arbitrary vintage; re-stamped and fresh projects would diverge in
mechanics) and a synthetic snapshot base (tells the adopt-time merge
that project content is template content).

The recorded baseline for later updates: the copier answers file,
pointing at the adopted template's current version, so plain
`copier update` works as the #2486 MVP describes. Rejected: recording a
snapshot of the merged render (would tell every future update that
conflict-resolved project content is template content, poisoning the
three-way merge and the user-modifications diff C2's classification is
seeded from).

## Consequences

The empty merge base avoids project-to-template misattribution; its cost
— template files contradicting project content surface as add/add-style
merges — is paid once, in the review flow, not at every update.
