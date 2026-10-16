# AGENTS.md

Repository router for copier-cat: a copier template manager. Read first,
escalate conflicts, and never let a diff carry a governance change.

## Read first

- `HANDOFF.md` — session provenance, read order, first-session suggestions
- `PRINCIPLES.md` — the constitution: intent, principles, constraints,
  and the amendment rule
- `spec.md` — draft spec; derives from the principles; capability map
  C1–C7 with gating design questions
- `ROADMAP.md` — phases

## Rules

- `PRINCIPLES.md` is the constitution: read it before designing anything.
  Conflicts with it are surfaced for a deliberate decision — never
  silently reinterpreted, and never edited as a side effect of
  implementation or session work.
- `spec.md` derives from the principles and governs capability design;
  ambiguous behavior stays an open question there (safe default + owner);
  resolved questions move to its decision record.
- The harness is seeded (mise + prek.toml + uv + backlog-md-py store);
  C1 work starts from the merger-registry extraction (task CC-1), not
  from new scaffolding.
- Grounding links live in HANDOFF.md; read the copier issues before
  designing adopt/contribute mechanics.
