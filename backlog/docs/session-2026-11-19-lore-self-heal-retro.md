---
id: DOC-12
title: Session 2026-11-19 — Lore self-heal retrospective
---

# Session 2026-11-19 — Lore self-heal retrospective

This session began as copier-cat implementation work and became a Lore database
and export repair. It leaves durable research, a portable self-heal runbook,
and an explicitly unfinished CCC-25 handoff.

## What went well

- Re-attributed the three stray project buckets and imported knowledge from two
  repositories whose project rows were missing.
- Regenerated copier-cat's knowledge file and verified it by entry ID, not just
  entry count.
- Preserved other sessions' edits and kept CCC-25 on its own branch.
- Found the actual stale-export mechanism: the session path is re-resolved from
  the system prompt on every request, not from the process working directory.
- Rebuilt the main virtual environment after its scripts retained the superseded
  checkout path; the main test suite then ran successfully.

## What went wrong

- I asserted missing Lore capabilities after probing too little. A live
  structured-import probe disproved the claim that shared scope had no supported
  route.
- I counted the versioned knowledge table rather than its live view, producing
  inflated totals.
- I generalized one lossy export into a property of the export command. A later
  export was complete by ID; the correct rule is to verify each export, not to
  assume loss or completeness.
- I deleted a regenerated directory before establishing why it was being
  recreated. Deletion could not fix the session's pinned path.
- The committed curation reference still contains the disproved scope claim and
  an overbroad export-loss warning. That correction is queued as CCC-32 rather
  than silently expanding the wrap-up.
- The background-research subagent returned its session log instead of the
  requested file. The useful research was then produced inline and checked on
  disk.

## Lessons

1. Enumerate the actual interface before asserting that something is absent.
2. Verify knowledge repairs and exports by IDs; counts conceal substitutions.
3. Treat the curator as a recorder, not a fact-checker. Retractions need explicit
   corrective entries.
4. Diagnose a recurring artifact's writer before deleting the artifact.
5. When a checkout moves, inspect virtual-environment script interpreters before
   reporting that tests cannot run.
6. Deliverables from subagents need a filesystem check, not trust in their reply.

## Follow-ups and state

- CCC-25 carries the implementation handoff on its feature branch.
- CCC-32 owns the two reference-document corrections.
- The portable self-heal procedure and machine-specific handoff are in
  .worktrees/handoff-lore-self-heal.md and
  .worktrees/handoff-other-machine-lore-self-heal.md; both are intentionally
  gitignored.
- Main's tests, Ruff lint, and formatting pass. The full quality task remains
  blocked by three pre-existing mypy os.sys errors in origin/main's assemble.py.
  That defect predates this wrap-up and needs its own scoped repair, not an
  untested drive-by edit.
- The ghost export path regenerates while sessions retain it. Closing or moving
  those sessions remains the user's action, not a cleanup shortcut.
