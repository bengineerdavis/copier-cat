---
id: CCC-6
title: Record a cross-layer resolution report when templates overlap
status: To Do
created_date: 2026-11-14 03:42
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
During the research repo stamp on 2026-11-12 the maintainer asked which templates had been used, and the answer could not be recovered from the repo. The base and agentic layers both own mise.toml, the merge resolved correctly (python and uv survived beside roborev and dotagents), and no record of that resolution exists anywhere.

The mechanism worked; the evidence was discarded. That is why a correct stamp still needed a teardown and restamp to explain.

Ship:

- A machine-readable resolution report for every adopt or merge run: per file, per chunk, which side won and why (accept, keep, conflict).
- The same unified diff _review_one already renders to stdout, emitted as data rather than only inside the interactive prompt loop.
- JSON mode writes the report even under --accept-all, which today applies changes with no prompt and therefore no diff at all.
- The chunk identity is the merger provider's own unit: TOML/YAML key path, marked-section name, or text span.

Constraints:

- Reuse the existing merger registry (decision-1); this is reporting over merges that already happen, not a new engine.
- Blocked by draft-2: name-bearing markers and region orientation. A chunk that cannot be named cannot be reported on.
- No new marker convention in project files (decision-5).
- The report is an artifact the maintainer can commit or discard; cc does not require it to be committed (graduation principle, spec C6).

Agreed with the maintainer 2026-11-13: the smallest useful version first, then increment. A report that names what won is more valuable than a general compatibility model that arrives later.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A merge or adopt run emits a per-file, per-chunk resolution report naming which side won and why
- [ ] #2 The report is emitted in JSON mode under --accept-all, where no interactive prompt and therefore no diff exists today
- [ ] #3 Chunk identity comes from the merger provider (TOML/YAML key path, marked-section name, text span), not a parallel naming scheme
- [ ] #4 A stack whose layers both own mise.toml produces a report showing which keys each layer contributed
- [ ] #5 Nothing the report produces is required for a template to keep working with plain copier
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
