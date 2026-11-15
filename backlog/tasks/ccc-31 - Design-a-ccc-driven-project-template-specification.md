---
id: CCC-31
title: Design a ccc-driven project template specification
status: To Do
created_date: 2026-11-15 16:16
references:
- backlog/docs/cc-assembly-mvp-spec.md
- GLOSSARY.md
- https://github.com/bengineerdavis/agentic-project-template/tree/main
- https://github.com/bengineerdavis/agentic-project-template/blob/main/backlog/tasks/apt-53%20-%20Refactor-the-agentic-template-into-readable-project-template-artifacts.md
updated_date: 2026-11-15 16:29
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The maintainer’s project templates produce inconsistent stamped outputs, and agentic-project-template’s rendering and merge intent is difficult to understand from its Python injection scripts. A ccc-driven template specification could make project templates and their compositions more consistent and understandable to humans and agents.

Ship:

- A standalone research project charter and cited community-evidence report covering established project-template tools, declarative specifications, composition and overlay patterns, compatibility and interface contracts, and practices reported by their maintainers and users.
- A reviewed project-template specification defining what template types should exist, their behavior and composition rules, their human- and agent-readable interfaces, and the canonical vocabulary shared with copier-cat.
- An evidence-based migration and adoption plan for agentic-project-template and the Python base, including traceable case studies of unreadable merge intent and the observed .alint.yml difference between copier-cat and copier-testkit.

Constraints:

- Begin with deep-research and review-best-practices: inspect primary sources, established tools and specifications, and practitioner reports; verify load-bearing claims against installed artifacts and record rejected options with reasons. Prefer complementary community conventions over a new ccc-specific mechanism.
- Follow research with grill-with-docs and domain-modeling to challenge the maintainer’s opinions and settle terminology before to-spec and to-tickets. Keep these design phases in one unbroken context where practical.
- Evaluate declarative representations against imperative injection and merging code; do not assume all template behavior can or should be declarative.
- Treat agentic-project-template as a case study, not a foregone defect: determine which intent belongs in Copier templates, manifests, composition data, scripts, or documented interfaces.
- Trace stamped provenance and the actual stamp matrix before assigning ownership of missing files. Verified case-study evidence: .alint.yml is absent in copier-cat and present in copier-testkit; agentic-project-template contains template/.alint.yml. copier-cat’s recorded Python-base provenance does not by itself establish an agentic-stamp defect.
- The research project should ultimately be creatable through ccc, but do not block CCC-24 through CCC-29 or expand their MVP scopes. Creating the research repository is a later approved action.
- Any new skill reference is declared in agents.toml in the same implementation change. Research and specification work creates no template, project, or upstream modifications without separate approval.

Agreed with the maintainer 2026-11-15: capture the research project now so the next fresh session can focus on the ccc assembly MVP.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A standalone research charter and cited report evaluate community tools, specifications, composition patterns, interface contracts, and practitioner experience with rejected options recorded
- [ ] #2 The reviewed specification defines template types, behavior, composition rules, human- and agent-readable interfaces, and canonical shared vocabulary
- [ ] #3 The adoption plan addresses agentic-project-template and the Python base and traces the unreadable merge-intent and alint case studies to verified provenance and ownership evidence
- [ ] #4 backlog-py board shows the research project with its full description and acceptance criteria
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Research routing: use deep-research and review-best-practices for evidence, then grill-with-docs and domain-modeling for maintainer decisions and vocabulary. The eventual specification may lead to a declarative ccc manifest, generation/validation conventions, or a hybrid; that representation is an open design decision. Safe research default: define required behavior and interfaces independently of representation before selecting a mechanism. Owner: maintainer through the documented grilling workflow.

Origin evidence: copier-cat main through c16c279de6a4d1a4d4bd40f97bb2671897c048a8. This research is deliberately independent of CCC-24 through CCC-29 and must not delay their first usable assembly workflow.
Research inputs added 2026-11-15: agentic-template artifact ownership belongs in a fresh refactor discussion, not silently in the assembly MVP. APT-53 captures that discussion and the imperative-template/alint investigation: https://github.com/bengineerdavis/agentic-project-template/blob/main/backlog/tasks/apt-53%20-%20Refactor-the-agentic-template-into-readable-project-template-artifacts.md. The research should give that discussion shared vocabulary and evidence, not prescribe its result.

Reusable case-study resources: copier-cat DOC-9; prototype/cc-assembly-ux at bf924fd; prototype/cc-composition-evidence at 5d0d5ad; the original stamping/readability observations through c16c279de6a4d1a4d4bd40f97bb2671897c048a8. APL-26 also records a worktree-claim reconciliation lesson from this project for the agentic backlog-workflow adapter.

Glossary review inputs: compare artifact ownership, stamped artifact, provenance, rendering runner, composition runner, template interface, declarative specification, composition data, imperative composition, merge intent, and compatibility contract against existing terms. Reuse established community vocabulary where it fits. Do not introduce a term merely to rename an existing one; the grilling and domain-modeling phase owns final definitions.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
