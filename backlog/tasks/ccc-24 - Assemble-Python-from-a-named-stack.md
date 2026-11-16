---
id: CCC-24
title: Assemble Python from a named stack
status: Done
created_date: 2026-11-15 06:09
labels:
- ready-for-agent
parent_task_id: CCC-11
references:
- backlog/docs/assembly-original-implementation-tickets.md
updated_date: 2026-11-16 06:13
orchestration:
  status_key: inprogress
  lease_owner: opencode-ccc-24
  lease_expires_at: '2026-11-16T06:49:42.319281Z'
  version: 1
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
- [x] #1 A real CLI assembles Python from a named local stack into an explicitly named destination
- [x] #2 The local catalog resolves template identity, source, optional ref, answers, and role without another project answers file
- [x] #3 Defaults and focused metadata-driven questions work, and missing noninteractive answers fail clearly
- [x] #4 Dry-run and JSON previews validate without writing or a bypass; approval covers only the displayed destination
- [x] #5 Native update evidence, disposable provenance, update instructions, and preview cleanup or retention are verified
- [x] #6 Validation and CLI acceptance tests prove rendered output, assembly invariants, generated tests, and failure reporting
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Original approved ticket text is preserved verbatim in DOC-10 (backlog/docs/assembly-original-implementation-tickets.md). This native task is the active implementation queue; the archived ticket is audit evidence, not a second queue.
DOC-10 also records the original .scratch-to-native task mapping. The external .scratch queue was retired after the archive and native tasks were published.
Composition experiment evidence preserved on prototype/cc-composition-evidence at 5d0d5ad: https://github.com/bengineerdavis/copier-cat/tree/prototype/cc-composition-evidence/prototype/cc-composition-evidence. It records measured Copier behavior for source resolution, structured data, --data replacement, and rejected update hunks. This is experimental evidence, not implementation.
Implemented the Python-only vertical slice: local YAML catalog; assemble DESTINATION --stack STACK with --dry-run, --json, --guided, --retain-preview, and --yes; stack list/show. Copier owns rendering and updates. Preview initializes a clean Git baseline solely in an isolated preview to validate native updates; it does not publish or mutate source templates. Native answers and disposable .copier-cat-stack.yml provenance are retained. Generated tests use an external environment so they do not dirty the update baseline. Explicit catalog refs are passed to Copier; the preview update uses the selected ref rather than upgrading pinned assemblies. Test findings: local Copier templates include dirty content, so ref tests use a cloned source; Copier diagnostics redirect to stderr for a single JSON stdout result. Multi-template composition remains CCC-25; machine-readable help remains CCC-26.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Shipped real Python assembly from a named local stack with read-only previews, metadata-driven questions, explicit new-destination approval, isolated validation, native Copier answers/update instructions, disposable provenance, preview cleanup/retention, and structured errors. Added stack list/show. Verification: 94 tests pass, ruff check/format and pyrefly pass, scoped pre-commit passes. Generated tests and independent native updates are exercised by CLI acceptance tests; failure and existing-destination cases cannot write the destination.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->

## Run History
<!-- SECTION:RUN_HISTORY:BEGIN -->
<!-- RUN_HISTORY_ENTRY:BEGIN -->
```yaml
event_id: run-4269cb2737234144aee82c6a079ff68e
type: claim_task
actor: opencode-ccc-24
timestamp: '2026-11-16T05:49:42.319337Z'
result: succeeded
task_id: CCC-24
from_status: todo
to_status: inprogress
metadata:
  lease_ttl_seconds: '3600'
```
Implement the Python-only named-stack assembly vertical slice
<!-- RUN_HISTORY_ENTRY:END -->
<!-- SECTION:RUN_HISTORY:END -->
