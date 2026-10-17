---
id: decision-1
title: Merger registry shaped as git merge drivers
date: 2026-10-17 05:29
status: accepted
---

## Context

cc's C1 adopt engine needs a merge mechanism. Options: port the
agentic-project-template engine as-is (bespoke plumbing), pure git-merge
(conflict markers everywhere, format-blind), or a hybrid. copier#2376
(open) proposes rebuilding `copier update` on `git merge`; cruft's
complaint history (#49, #287) shows format-blind resolution is the UX
users suffer. Decided in grill round 1 (2026-10-15); migrated from
docs/adr/0001 in the backlog-workflow switch (2026-10-17).

## Decision

A registry of structure-aware mergers (TOML deep-merge, YAML, marked
sections) is the core, but each merger is shaped like a git merge driver
and the fallback is plain `git merge-file`, so the file-level adopt flow
reads as a git three-way merge. Mergiraf-style structural tools compose
with the driver shape; not adopted as a core dependency while the
registry can express the same contracts.

## Consequences

Adopt's design interfaces with #2376's direction instead of fighting it,
keeping the donatable posture (PRINCIPLES principle 3). A
marked-region provider is just another merger (evaluated as backlog
task CC-2), not a rival mechanism.
