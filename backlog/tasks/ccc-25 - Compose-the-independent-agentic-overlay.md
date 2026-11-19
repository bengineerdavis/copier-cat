---
id: CCC-25
title: Compose the independent agentic overlay
status: To Do
created_date: 2026-11-15 06:09
dependencies:
- CCC-24
labels:
- ready-for-agent
parent_task_id: CCC-11
references:
- backlog/docs/session-2026-11-19-lore-self-heal-retro.md
updated_date: 2026-11-19 21:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The assembly MVP must combine Python with an independent agentic overlay while preserving each template’s native update lifecycle.

Ship:

- Isolated ordinary-template rendering with disjoint files preserved, structured TOML merged through the existing engine, and ordered deduplicated .gitignore composition.
- Explicit collision and unsupported-format handling that never silently chooses a winner or concatenates text.
- An overlay capability contract independent of Python, two working native answers files, and verified independent update commands.
- Real local template fixtures and synthetic conflict fixtures covering composition, validation, and failure reporting.

Constraints:

- Preserve DOC-9 and decisions 5 through 7. Do not require or inherit from Python for the agentic overlay.
- Do not introduce automatic stack-wide update orchestration.

Agreed with the maintainer 2026-11-14: convert the approved second DOC-10 original ticket into the native Backlog implementation queue.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Isolated rendering preserves all disjoint files from both ordinary templates
- [ ] #2 Structured TOML and ordered deduplicated .gitignore composition retain both templates contributions deterministically
- [ ] #3 Same-key collisions require a declared rule or visible review, and unsupported shared formats fail explicitly
- [ ] #4 The agentic overlay declares capabilities without requiring or inheriting from Python
- [ ] #5 Both native answers files and reported update commands work independently
- [ ] #6 Real local and synthetic conflict fixtures cover composition, validation, and failure reporting without stack-wide update orchestration
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Original approved ticket text is preserved verbatim in DOC-10 (backlog/docs/assembly-original-implementation-tickets.md). This native task is the active implementation queue; the archived ticket is audit evidence, not a second queue.
DOC-10 also records the original .scratch-to-native task mapping. The external .scratch queue was retired after the archive and native tasks were published.
Composition experiment evidence preserved on prototype/cc-composition-evidence at 5d0d5ad: https://github.com/bengineerdavis/copier-cat/tree/prototype/cc-composition-evidence/prototype/cc-composition-evidence. Its combined5 fixture demonstrates structured TOML composition and its rejected-hunk artifact demonstrates why update conflicts must remain visible. Use the existing composition engine for production behavior.
Session wrap-up 2026-11-19: implementation is WIP, not Done. Branch feature/ccc-25-agentic-overlay, worktree .worktrees/ccc-25-agentic-overlay, WIP commit 776f27d. Main has since merged CCC-24; rebase or merge deliberately before review. Tests on the WIP tree: 101 passed via .venv/bin/python -m pytest -q. The pytest console script has a stale interpreter from the superseded checkout; recreate the worktree venv before using uv run pytest. Remaining acceptance criteria: all six are unchecked and must be reviewed against the implementation, especially native answers/update independence and collision/unsupported-format behavior. Do not infer completion from the passing suite. GLOSSARY.md and spec.md on main are another session edits and are excluded.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
