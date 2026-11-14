---
id: CCC-16
title: Design deterministic gitignore generation and composition
status: To Do
created_date: 2026-11-14 14:59
dependencies:
- CCC-7
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Design and scenario-test generation of `.gitignore` from ordered, deduplicated technology patterns and template contributions, informed by https://github.com/toptal/gitignore.io.

Ship:

- Research of the current primary sources: pattern-data ownership, API/tool availability, offline/vendored operation, maintenance model, license implications, and suitability as a cc adapter.
- A recommended reuse-versus-own decision with rejected alternatives and a smallest viable design.
- Scenario coverage for ordered patterns, exact deduplication, negation semantics, conflicts, cache/offline behavior, and reproducibility across Python and non-Python stacks.
- An interface sketch connecting technology-pattern generation to stack assembly without network access in ordinary tests or every assembly.

Constraints:

- Prefer a maintained existing tool or pattern dataset when it fits cc's deterministic, no-lock-in model; do not invent a universal text merger.
- Remote availability must not make ordinary assembly or tests flaky. Pin/cache any data and make its source visible.
- Project-local additions survive composition. Never silently remove negations or reorder patterns whose meaning depends on order.
- This is a design/scenario task; implementation follows the approved adapter choice.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The research report covers primary-source evidence for pattern data, tools, licensing, offline operation, maintenance, and reuse versus own implementation
- [ ] #2 The scenario design covers ordering, exact deduplication, negation semantics, conflicts, project-local additions, and reproducible offline composition
- [ ] #3 The proposed adapter interface connects generated patterns to stack assembly without network-dependent ordinary assembly or tests
- [ ] #4 The recommendation identifies a smallest viable design and explicitly rejected alternatives
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Primary-source research completed 2026-11-14. Artifact: backlog/docs/gitignore-generation.md (verified on disk after background delegation returned no artifact; research was then performed in-session).
Recommendation: reuse GitHub official CC0 gitignore template collection as pinned/cached pattern data, with a small deterministic offline adapter. Do not call gitignore.io during ordinary assembly; its JSON list API is an optional online acquisition alternative. The toptal/gitignore.io service is Swift/Vapor and its referenced toptal/gitignore data URL returns 404. Git documents last matching pattern wins; plain set union or last-pattern-wins dedup is rejected. Preserve first exact occurrence and negation order; test with git check-ignore fixtures. This is evidence for implementation, not an approved schema or performance claim.
Implementation evidence boundary: reuse pinned CC0 data, not gitignore.io at runtime. The report records primary sources, rejected options, safe dedup/order behavior, and git check-ignore scenarios. Keep this task design/research only until CCC-15 converts approved requirements into implementation tickets.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
