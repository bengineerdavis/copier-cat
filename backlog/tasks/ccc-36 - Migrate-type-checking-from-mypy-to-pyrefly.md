---
id: CCC-36
title: Migrate type checking from mypy to pyrefly
status: To Do
created_date: 2026-11-22 17:09
updated_date: 2026-11-22 17:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
pyrefly already runs in the lint task, but it reads its settings from [tool.mypy] because no pyrefly.toml exists, and the dedicated type-check task still runs mypy. That is why CCC-33 is a mypy-only failure: uv run pyrefly check src tests reports 0 errors on the same code where mypy reports three attr-defined errors in assemble.py. Consolidating on pyrefly removes the duplicated checker and the config indirection. Follow the documented migration at https://pyrefly.org/en/docs/migrating-from-mypy/ rather than hand-writing config. Ship: run pyrefly init to convert [tool.mypy], read the generated config line by line before committing (the converter drops unrecognized settings and error codes without warning), confirm preset=legacy is written, run mypy src and pyrefly check on the same commit and classify every difference, then point the mise type-check task at pyrefly and remove mypy from dev dependencies and the [tool.mypy] section once pyrefly alone is green. Constraints: current mypy config is only python_version=3.12, warn_unused_configs=true, ignore_missing_imports=true, with no plugins and no strict=true, so the simple path applies. Do not blanket-suppress new errors to force a green run; classify them first. Coordinate with CCC-33, which fixes the three mypy os.sys errors in assemble.py — this task may supersede it, but decide that explicitly rather than letting the migration silently close it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pyrefly init output is reviewed line by line and the generated config committed
- [ ] #2 Differences between mypy src and pyrefly check on the same commit are classified, not blanket-suppressed
- [ ] #3 mise run type-check runs pyrefly and mise run quality passes
- [ ] #4 mypy is removed from dev dependencies and [tool.mypy] once pyrefly alone is green
- [ ] #5 CCC-33 is explicitly closed as superseded or kept, with the reason recorded
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
