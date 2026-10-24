---
id: CC-4
title: CLI reference and copier-equivalent help texts
status: Done
created_date: 2026-10-24 21:18
updated_date: 2026-10-24 22:35
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Spec C6's open question asks how 'explainable in copier terms' is enforced: per-command copier equivalents in docs/help, an --explain surface, or skill-authored teaching sections. This task answers it with the docs/help mechanism: each CLI command's --help carries a copier-native equivalent, usage examples, and its exit-code contract, and a test enforces the presence of the copier equivalent so the teaching cannot silently rot. A README CLI-reference section mirrors the same content for the repo surface.

Resolution of the C6 enforcement-mechanism gate rides with this task: the mechanism is per-command copier equivalents in --help, enforced by a test (recorded as a decision in the store, with the spec gate struck in the same commit as the decision, per the constitution-ledger precedent).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every CLI command's --help carries a copier-native equivalent line: what the command does in copier terms and why cc adds machinery around it
- [ ] #2 Every CLI command's --help shows usage examples and its exit-code contract (0 clean / 1 conflicts presented / 2 error)
- [ ] #3 A test asserts the copier-equivalent marker is present in every command's help output, so a commit adding a command without its teaching fails review
- [ ] #4 README gains a CLI reference section mirroring the help content: commands, flags, exit codes, JSON output shapes, human and agent examples
- [ ] #5 The C6 enforcement-mechanism decision is recorded in the store (decision file + decision-log row) and spec.md's C6 gate is struck in the same commit series
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Implemented 2026-10-24: copier equivalents + examples + exit contracts in every command's help epilog (ef53e86), enforcement test over the registered commands (ef53e86), README CLI reference (ec73ce2), decision-6 + decision-log row + spec C6 gate struck (1f283f8). 82/82 tests passing.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
