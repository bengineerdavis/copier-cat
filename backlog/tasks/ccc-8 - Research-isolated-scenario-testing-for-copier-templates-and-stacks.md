---
id: CCC-8
title: Research isolated scenario testing for copier templates and stacks
status: To Do
created_date: 2026-11-14 04:31
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The existing suite has real git-backed template fixtures, but no reusable isolation model for testing rendered projects or copier-cat stacks. The Molecule role/playbook distinction suggests scenario-based coverage across copier templates and stacks without coupling every test to the host checkout.

Ship:

- Research a scenario harness that isolates template and stack renders in temporary destinations, runs commands inside those destinations, and cleans up after each scenario.
- Map the major scenarios: plain copier copy/update/recopy/check-update, data-shaped stack composition, forward-update conflicts, adopt on clean and hand-edited projects, contribute preparation, and free-text shared files. Binary composition is out of scope for this research.
- Compare pytest fixtures and existing copier testing helpers with a Molecule-like declarative scenario runner; choose the smallest reusable shape and name what is rejected.
- Specify reusable roles/fixtures for a standalone template, an ordered stack, a git-backed project, and a synthetic template version bump, with host state never shared between scenarios.

Constraints:

- Copier remains the render engine; the harness tests copier and cc behavior rather than replacing either.
- Regular copier templates need no cc-specific test files or structure (PRINCIPLES principle 5).
- Synthetic fixtures and local git repositories only; no network dependency, remote mutation, or access to another project's state.
- Scenario B may surface native copier .rej or inline conflicts for the first usable version, but the harness must detect them and distinguish expected conflict from unexpected success.
- Rendering correctness and rendered-project behavior are separate checks: valid TOML/JSON does not prove the resulting project's tests or commands work.
- This is research first; do not add a Molecule dependency or a bespoke runner without evidence that pytest plus copier primitives cannot carry the scenario matrix.
- Do not merge, transform, or synthesize binary files. Exploring where binary handling might be useful belongs to a separate project; it is not a near-term copier-cat capability.

Open questions:

- Which existing copier testing helpers are maintained and sufficient at the pinned version.
- Whether a scenario is declarative YAML, a Python fixture, or a small directory with setup/render/verify steps.
- Which scenarios belong in the default suite versus slower integration coverage.
- What artifact retention is useful on failure without leaving test state behind on success.

Agreed with the maintainer 2026-11-14: investigate Molecule-inspired isolation for copier projects and copier-cat stacks before building the next layer of composition machinery.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A research report compares pytest fixtures, existing copier testing helpers, and a Molecule-like scenario runner against the stated isolation requirements
- [ ] #2 The report specifies isolated scenario fixtures for standalone templates, ordered stacks, git-backed projects, and template version bumps
- [ ] #3 A scenario matrix covers plain copier operations, data-shaped composition, forward conflicts, adopt, contribute, and free-text files while explicitly excluding binary composition
- [ ] #4 The report separates rendering assertions from tests run inside the rendered project
- [ ] #5 The recommendation identifies the smallest reusable harness shape and rejected alternatives with reasons
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
