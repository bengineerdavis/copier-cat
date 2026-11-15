---
id: CCC-26
title: Share human and agent command discovery
status: To Do
created_date: 2026-11-15 06:09
dependencies:
- CCC-24
labels:
- ready-for-agent
parent_task_id: CCC-17
references:
- backlog/docs/machine-readable-help-research.md
- backlog/docs/cli-workflow-review.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
People and agents need the same command descriptions, operands, examples, effects, errors, and consent boundaries without parsing terminal prose or invoking a workflow.

Ship:

- One versioned command-description model shared by human and JSON help, including focused command discovery and structured examples.
- Clear destination-versus-stack operands, read-only versus approved-write effects, separate diagnostics, and safe JSON preview semantics.
- CLI acceptance tests for parity, schema versioning, side-effect boundaries, and readable failures.

Constraints:

- Follow decision-8 and CCC-17. Help is read-only and initialization-free; it must not download, render, or write project files.
- JSON alone previews; JSON with explicit approval authorizes only the displayed new-destination write.
- MCP and terminal-prose parsing are not prerequisites.

Agreed with the maintainer 2026-11-14: convert the approved third .scratch issue into the native Backlog implementation queue.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 One versioned model supplies matching human and JSON descriptions and structured examples, including focused command discovery
- [ ] #2 Discovery distinguishes destination from stack and read-only previews from approved writes
- [ ] #3 Help performs no setup, download, rendering, or project writes
- [ ] #4 JSON alone previews and JSON with approval authorizes only the displayed destination write
- [ ] #5 Diagnostics stay separate from machine-readable results
- [ ] #6 CLI acceptance tests prove parity, schema versioning, side-effect boundaries, and readable failures without MCP or terminal parsing
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
