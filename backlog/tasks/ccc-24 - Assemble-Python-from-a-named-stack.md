---
id: CCC-24
title: Assemble Python from a named stack
status: To Do
created_date: 2026-11-15 06:09
labels:
- ready-for-agent
parent_task_id: CCC-11
references:
- backlog/docs/assembly-original-implementation-tickets.md
updated_date: 2026-11-15 06:42
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A developer needs to create a real Python project from a named stack without memorizing template sources or CLI flags. This is the first usable vertical slice of the deterministic assembly MVP.

Ship:

- A real CLI that assembles Python from a named local stack into an explicitly named new destination, resolving template identity, source, optional ref, answers, and role from a small catalog.
- Read-only previews, focused metadata-driven questions, explicit destination-write approval, and clear noninteractive missing-answer failures.
- Native Copier update evidence, disposable assembly provenance, native update instructions, and automatic or explicitly retained isolated previews.
- Validation of rendered output, assembly invariants, and the generated project’s own tests, plus real CLI acceptance tests at the approved seams.

Constraints:

- Preserve DOC-9, decisions 3 through 8, and CCC-11 as the requirement sources; Copier owns rendering and updates.
- JSON alone is a safe preview; --yes approves only the displayed new-destination write. Cancellation leaves no approved destination.
- Do not introduce the conversational skill, stack-wide update orchestration, or a second composition implementation.

Agreed with the maintainer 2026-11-14: convert the approved first DOC-10 original ticket into the native Backlog implementation queue.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A real CLI assembles Python from a named local stack into an explicitly named destination
- [ ] #2 The local catalog resolves template identity, source, optional ref, answers, and role without another project answers file
- [ ] #3 Defaults and focused metadata-driven questions work, and missing noninteractive answers fail clearly
- [ ] #4 Dry-run and JSON previews validate without writing or a bypass; approval covers only the displayed destination
- [ ] #5 Native update evidence, disposable provenance, update instructions, and preview cleanup or retention are verified
- [ ] #6 Validation and CLI acceptance tests prove rendered output, assembly invariants, generated tests, and failure reporting
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Original approved ticket text is preserved verbatim in DOC-10 (backlog/docs/assembly-original-implementation-tickets.md). This native task is the active implementation queue; the archived ticket is audit evidence, not a second queue.
DOC-10 also records the original .scratch-to-native task mapping. The external .scratch queue was retired after the archive and native tasks were published.
Composition experiment evidence preserved on prototype/cc-composition-evidence at 5d0d5ad: https://github.com/bengineerdavis/copier-cat/tree/prototype/cc-composition-evidence/prototype/cc-composition-evidence. It records measured Copier behavior for source resolution, structured data, --data replacement, and rejected update hunks. This is experimental evidence, not implementation.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
