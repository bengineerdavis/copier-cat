---
id: DOC-13
title: Prove the no-lock-in lifecycle on dummy projects
---

## Scope

Partial evidence for CCC-38, not completion of the full scenario matrix. The durable source is the public CLI test `test_extended_stack_native_updates_survive_stack_artifact_removal` on `feature/ccc-25-evidence`; no scratch checkout is required.

## Reproduce

From the feature worktree:

```sh
uv run pytest tests/test_assemble_composition.py::test_extended_stack_native_updates_survive_stack_artifact_removal -o addopts=
```

The test creates synthetic, local, Git-backed templates and an isolated dummy subproject. It never uses the network or another project checkout.

## Verified behavior

1. Assemble the Python base stack into a new destination.
2. Extend that existing project with the real single-template `adopt` command. Adoption reports a `.gitignore` conflict; the test resolves it explicitly rather than treating conflict exit 1 as success.
3. Add and commit `project-owned.txt` as local work.
4. Delete `python.stack.yml` and commit its removal.
5. Change both source templates and tag each `v1.1.0`.
6. Run plain `copier update` independently against `.agentic-answers.yml` and `.copier-answers.yml`. No copier-cat command or library participates in either update.
7. Assert both upgraded outputs contain `Agentic template v2` or `Python template v2`, `project-owned.txt` survives, repeated unchanged updates leave Git clean, and both native answers files record `v1.1.0`.

Copier refuses a dirty Git tree. After each real version upgrade, the test commits the changed answers and output before updating the next member. Removing copier-cat does not remove that Git consent boundary.

## Naming and safety

Assembly writes one `<stack name>.stack.yml` with `definition` and `application` sections. There is no separate stamp file. Native per-template answers files remain Copier-owned update baselines. Adopt preserves those rendered answers byte-for-byte. Unsafe stack names that could escape the destination are rejected.

## Human observation

The maintainer ran both native updates in the retained dummy project before its cleanup. Both reported `Keeping template version 1.1.0`; `git status --short` remained empty. That demonstrates that plain Copier discovered both baselines without the stack artifact and that repeated unchanged updates did no writes. The actual tagged upgrades had already been performed by the test.

## Unproven boundaries

This is not `adopt --stack`: extension uses the shipped single-template adopt path. Adoption does not yet update the existing stack artifact application state. Backup/restore, interrupted-run recovery, stack discovery, member removal, and the remaining CCC-38 matrix are not proven by this scenario.

## Collision reconciliation

`uv run python scripts/audit_backlog.py --refs` audits native Backlog frontmatter across local and remote refs. The audit on 2026-11-22 covered 769 records and found zero ID/title collisions. Its public CLI tests include a deliberately colliding two-branch fixture, so the zero result is not merely an empty scan.
