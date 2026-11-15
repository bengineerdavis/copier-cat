---
id: CCC-19
title: Track template and stack lineage for owned subprojects
status: To Do
created_date: 2026-11-14 18:44
updated_date: 2026-11-14 18:55
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Copier-cat can create or adopt projects from independent templates and stacks, but it does not yet maintain an informational map from those sources to the projects they produced. The maintainer wants to discover lineage across repositories they own or organizations they belong to, especially to support later change propagation and feedback.

Ship:

- A lineage design defining recorded template/stack identity, source, revision, answers-file evidence, optional provenance, and discovery scope for owned repositories and organizations.
- An informational inventory and search workflow that reports which known templates or stacks produced which subprojects, with confidence and missing-evidence states rather than inferred certainty.
- A forward-looking contract connecting lineage records to separately approved contribution, propagation, and feedback workflows without adding implementation to the assembly MVP.

Constraints:

- Start with informational discovery and reporting; do not automatically update, modify, or publish to a subproject.
- Use native per-template answers files and existing assembly provenance before introducing another mandatory project metadata file.
- Distinguish recorded lineage from guessed similarity; repositories without reliable evidence remain unknown or require review.
- Initial discovery is limited to explicitly configured local roots and maintainer-owned or maintainer-authorized organizations, with read-only access and no secret exposure.
- Preserve independent native Copier updates and language-independent overlays.
- Follow-up propagation, contribution, and feedback actions retain their own explicit consent boundaries.
- Any new skill introduced by implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: lineage is initially informational, with particular future value for pushing template changes and receiving subproject feedback.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The lineage design defines source identity, revisions, native answers evidence, optional provenance, and explicitly scoped owned/authorized repository discovery
- [ ] #2 An informational inventory and search workflow reports template/stack-to-subproject lineage with confidence and explicit unknown or review-required states
- [ ] #3 A later-work contract links lineage to separately approved propagation, contribution, and subproject feedback without expanding the assembly MVP
- [ ] #4 backlog-py board shows CCC-19 with its full description and acceptance criteria
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Upstream feedback convention: source-project findings remain in the configured local tracker. Any upstream issue, patch, pull request, or other submission follows the receiving project’s current contributor conventions and requires separate approval. See CCC-21 and APL-27.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
