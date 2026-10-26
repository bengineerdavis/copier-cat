---
id: draft-3
title: 'TOML merger array semantics: dedupe and dependency-aware merge'
status: Draft
created_date: 2026-10-26 15:56
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Dogfood evidence (2026-10-26 python-project-template adopt): the TOML merger concatenates arrays, so the template's typer constraint was appended alongside cc's existing one (typer>=0.27.3 and typer>=0.12 in one dependencies array). An earlier CTCT adopt showed the same class (duplicate copier/pytest requirements, split [tool.pytest] tables). Real adopts need manual cleanup before commit.

Open questions: should arrays dedupe by requirement identity (PEP 508 name) rather than append? Should table merging prefer cc's existing table over the template's when both configure the same tool? Safe default until decided: review every TOML merge by hand on adopt; do not change merger semantics without fixtures from these adopts. Owner: bdavis.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
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
