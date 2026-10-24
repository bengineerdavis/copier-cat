---
id: CC-2
title: Study copier-uv-bleeding marked-region preservation
status: Done
created_date: 2026-10-16 21:06
updated_date: 2026-10-18 17:07
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Phase 1 study task (grill round 2): evaluate marked-region mechanism as another merger provider against the registry interface.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Mechanism read from source at pinned commits (PR #329, merge 9a80874, v0.41.2), not assumed: skip-if-exists plus _tasks regeneration of mixed files, template-preserve:<name>:start/:end markers, by-name matching, snapshot-splice semantics, tool-owned scalar pass, legacy bootstrap, and the documented trade-off that unmarked project content is dropped on update
- [x] #2 Evaluated against the merger-registry interface (decision-1): how the mechanism enters as a composed provider like MarkedSectionMerger, where its semantics differ (named markers, region-body precedence), and what a port would generalize — recorded in this task's implementation notes
- [x] #3 Upstream signal assessed: copier#2762 ({% ignore %} tag, preview-leaning) — update-time region preservation stays copier's; cc's registry stays adopt-time; deference posture recorded
- [x] #4 Verdict recorded as a backlog decision with pinned evidence in backlog/docs/prior-art.md and a review trigger
- [x] #5 C1 gate closes: spec.md's marked-region gate is removed in the same commit as the decision — this task's own closure requirement, executed on the decision log's constitution-ledger precedent (the recorded decision is the closure; the spec edit in the same commit is its execution)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
MECHANISM (read at PR #329, merge 9a80874, v0.41.2 — not assumed): pyproject.toml and prek.toml sit in _skip_if_exists, so copier's patcher never touches them after first generation; a _tasks step (migrations/sync_marked_sections.py) regenerates each file fresh via copier.run_copy on every update, then splices preserved content back into the fresh render. Markers are '# template-preserve:<name>:start/:end' comments written in the .jinja source; regions match BY NAME (a deliberate fix over Templator's positional matching, which can splice into the wrong slot on reorder), the current file's region bodies are snapshotted and spliced byte-for-byte, and a region with no snapshot keeps the fresh render's default (never blanked — the second deliberate fix over Templator).

Two template-specific extras: tool-owned scalars (project.version, tool.semantic_release.tag_format) are preserved by TOML key path because markers cannot cover projects updating from marker-less versions; and a one-time, self-terminating legacy bootstrap regex-locates pre-marker content on the first update past the mechanism. Documented trade-off: anything outside a marked region always reflects the template — unmarked project additions are silently dropped (predictable, stricter than leave-unrecognized-alone). Motive: copier update is not a true 3-way merge; its fuzzy patch replay can silently overwrite hand-edits with no .rej (DOT-599).

FIT AGAINST THE REGISTRY INTERFACE (decision-1): the entry point is natural — sync_text(existing, fresh) has the same shape as merge(base='', ours=existing, theirs=fresh), so the mechanism ports as a composed provider exactly the way MarkedSectionMerger enters (never in the default registry; markers stay a template convention, no cc residue). Two generalizations are required before it could serve a uv-bleeding-style template: (a) NAMED MARKERS — cc's Markers is one literal begin/end pair, but template-preserve:<name>:start/:end is a marker family with a per-region name; the provider needs a name-bearing pattern and by-name region identity (cc's _Region carries no name today). (b) REGION-BODY PRECEDENCE — the ownership is inverted: uv-bleeding's regions are user-owned (the project body wins over the render's; the template owns everything outside regions), while cc's MarkedSectionMerger makes the render's region body replace ours' byte-for-byte (template-owned regions per GLOSSARY). Same marker shape, opposite semantics; a port must make region orientation explicit rather than silently pick one. The tool-owned scalar pass needs no port: cc's TomlMerger already gives project values conflict wins at adopt, structurally covering the DOT-620 case that forced uv-bleeding to hand-roll a key-path pass. The legacy bootstrap stays template-side — it is the template's migration concern and ships with the template.

UPSTREAM SIGNAL (copier#2762, closes #2184): the PR's own trajectory validates decision-1's shape — literal comment markers were rejected by the copier maintainer (hardcoded '#' cannot generalize across file formats) and reworked into a Jinja {% ignore %} tag: language-agnostic, nothing leaks into rendered files, region content survives by being omitted from both update-time merge sides, degrading to a normal conflict when the template edits lines adjacent to the block. sisp is leaning toward shipping it as an opt-in 'preview' feature. Posture: update-time region preservation is copier's problem to own; cc's registry stays adopt-time; if #2762 lands, marked-region templates get native update survival and cc's provider matters at adopt only. Track, do not rival.

VERDICT: another merger provider, not a rival architecture — ROADMAP's framing holds and decision-1 stays closed. The provider generalizations (named markers, explicit region orientation) are deferred until cc adopts a template that needs them; parked as a backlog draft with a safe default. Update-time preservation defers to copier upstream (#2762).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Studied at source (PR #329, 9a80874, v0.41.2): skip-if-exists + _tasks regeneration splicing by-name template-preserve regions; tool-owned scalar pass; legacy bootstrap; unmarked content dropped by design. Verdict (decision-5): another merger provider, not a rival — decision-1 holds; cc composes it like MarkedSectionMerger and never ships default markers. Two generalizations gate a port (named markers, explicit region orientation — inverted body precedence vs cc's template-owned regions); parked as draft-2. cc's TomlMerger already covers the tool-owned scalar case structurally. Update-time preservation belongs to copier upstream: #2762 moved from comment markers to a Jinja {% ignore %} tag, preview-leaning — cc tracks it, registry stays adopt-time. Evidence pinned in backlog/docs/prior-art.md; spec C1 gate closed with the decision. Next: CC-3.
<!-- SECTION:FINAL_SUMMARY:END -->
## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 All acceptance criteria checked
- [x] #2 Evidence section in prior-art.md carries pinned commits and a review trigger
<!-- DOD:END -->
