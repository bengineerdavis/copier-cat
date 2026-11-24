---
id: CCC-33
title: Restore the full quality gate for assemble.py
status: Done
created_date: 2026-11-19 21:04
updated_date: 2026-11-23 02:42
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The main branch test, lint, and formatting checks pass, but the full quality task fails on three mypy errors inherited from the merged CCC-24 implementation. This blocks a clean quality verification for subsequent work.

Ship:

- Replace the three os.sys references in src/copier_cat/assemble.py with the appropriate explicitly imported module.
- Verify the complete quality task after the change.

Constraints:

- Keep this repair independent of the unfinished CCC-25 branch and preserve its behavior.

Measured 2026-11-19: the same os.sys calls exist in origin/main; this wrap-up did not introduce them.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The three mypy attr-defined errors in assemble.py are resolved without changing behavior
- [x] #2 uv run pytest -q passes
- [x] #3 mise run quality passes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Replaced os.sys.stderr with sys.stderr in assemble.py. mypy clean, 94 tests pass, mise run quality green on fix-ccc-33-quality-gate dae4f5d.
<!-- SECTION:FINAL_SUMMARY:END -->
## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
