---
id: decision-12
title: Store stack definition and application state in one project artifact
date: 2026-11-23 02:18
status: accepted
---

## Context

The stack specification selected one project-local artifact containing both
what was requested and what was applied. The implementation had already used
`.copier-cat-stack.yml` for assembly provenance, but its filename and schema
no longer described that coordinated model. The artifact model is distinct
from decision-11's CLI-verb decision and is recorded separately here.

The model was accepted by the maintainer on 2026-11-22: one
`<stack name>.stack.yml` file has a `definition` section and an `application`
section. Copier's native per-template answers files remain separate and
authoritative for native updates. The artifact is disposable: removing it must
not impair native per-template rendering or updating.

## Decision

Assembly writes one `<stack name>.stack.yml` containing the stack definition
and its application state, rather than `.copier-cat-stack.yml` and a separate
stamp file. The JSON result exposes its filename as `stack_artifact`.

Template contributions may not use the reserved artifact path. A contribution
that collides with it fails composition before a destination is written;
copier-cat never silently replaces that template-owned file.

Plain-directory templates remain supported for rendering and structural
validation. They have no Git commit baseline, so a versioned native Copier
update is unavailable and validation says so explicitly. No-ref Git templates
render their current working tree. When a local no-ref source is dirty,
native-update validation uses a clean committed copy of that source and its
real committed baseline; the source template is never modified.

## Consequences

- `spec.md` C8, the CLI help, and the stack artifact schema use the same
  filename and definition/application model.
- Native per-template answers files remain Copier-owned update baselines;
  assembly never makes the stack artifact a prerequisite for those updates.
- The artifact-model decision is recorded here rather than by editing the
  accepted decision-11 record.
- Full stack-aware extension, application-state updates after adoption,
  backup/restore, interrupted-run recovery, and the remaining CCC-38 scenario
  matrix remain unimplemented or unproven.
