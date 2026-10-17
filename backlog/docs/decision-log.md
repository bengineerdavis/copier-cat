---
type: archive
id: DOC-1
title: Decision log — spec ledger archive (2026-10-13..16)
---

The spec's decision record, archived verbatim when the backlog workflow
switch made the store the home for decisions (2026-10-17). Durable
design decisions live as individual files in `backlog/decisions/`; this
table is the historical ledger of everything resolved during the spec
era, including session-level and naming decisions that will not be
re-litigated as ADRs. New decisions are created with
`backlog-py decision create` and recorded here only if they need a
one-line index entry.

| Decision | Choice |
| --- | --- |
| Name | copier-cat (cc); free on PyPI/npm/crates, unclaimed under bengineerdavis on GitHub (checked 2026-10-12) |
| Origin | Spun out of the agentic-project-template session (2026-10-12); its CLI is the prototype of C1/C2 mechanics |
| Seed scope | Docs only — no code or harness; the next session chooses the stack and seeds it |
| Language/stack | Python, uv-managed (2026-10-13) — matches the maintainer's tooling and the apt merge-engine prototype that C1 ports; copier itself is Python, so C2 diff-reuse is direct library use |
| cc ↔ apt | agentic-project-template is a regular copier template for now — not an engine owner or special consumer. Its CLI is the prototype cc's C1 engine ports from (2026-10-13, revised from an earlier full-absorb decision the same session) |
| Binary name | `copier-cat` (2026-10-13) |
| Upstream posture | Prototype adopt in cc, shaped to stay donatable upstream (copier#2486); no PR-first engagement (2026-10-13) |
| Adopt merger registry (C1) | Merger registry shaped as git merge drivers with a `git merge-file` conflict-marker fallback — details and rejected options in backlog/decisions/decision-1 (2026-10-15) |
| Adopt merge base + baseline (C1) | Empty tree as the adopt-time merge base; the copier answers file as the recorded baseline for later updates — details and rejected options in backlog/decisions/decision-2 (2026-10-15) |
| Adopt apply flow (C1) | Per-file accepted merges land directly in the working tree; committing stays the user's act — the accept is the consent moment, `git diff` is the review surface (grill round 2, 2026-10-15) |
| Answers-file naming (C1) | Copier-native per-template pattern: plain `.copier-answers.yml` for a first template, `.copier-answers.<template>.yml` as more coexist (grill round 2, 2026-10-15) |
| Adopt MVP scope (C1) | Single-template runs; N-template coexistence is a later flow on the same engine/answers primitives (grill round 2, 2026-10-15) |
| Classification ownership (C2) | Render-derived, deterministic: template-rendered paths are template-owned, everything else project-owned; cc config overrides; the template is never asked to cooperate and no work is pushed onto copier (grill round 3, 2026-10-15) |
| Render→source mapping (C2) | Reconstructed deterministically by re-rendering with recorded answers; if that proves expensive, cc owns a cached render-map instead — never a template-maintained convention (grill round 3, 2026-10-15) |
| Changeset shape (C2) | One changeset per file; classification clustering is presentation, not engine (grill round 3, 2026-10-15) |
| Proposal state (C2) | cc-local state dir keyed by (project, template) identity; no in-project markers (grill round 3, 2026-10-15) |
| PR mechanics (C2) | Two explicit commands: prepare (branch + commits in a template checkout) and publish (user's own `gh` auth); no fork management in MVP (grill round 3, 2026-10-15) |
| Monorepo subpath (C2) | Ownership map carries a template-root offset from day one; subpath PRs deferred to Phase 3 (grill round 3, 2026-10-15) |
| Diff sourcing (C2) | Reuse copier's own update computation as a library import — one source of truth; tracks copier#2376's rewrite rather than drifting from it (grill round 3, 2026-10-15) |
| Governance split | PRINCIPLES.md is the constitution (intent, principles, constraints, amendment rule); spec.md derives from it. Advisory panel, deliberated; principle 4 reworded Spec-driven → Layered governance; the operate-on-regular-templates invariant promoted from constraint to principle 5. Owner: bdavis (2026-10-16) |
| Backlog workflow | Full Backlog.md-style store: requirements live as task acceptance criteria and the thin requirements spec; decisions as backlog/decisions/ + this log; evidence in backlog/docs/; open questions as drafts with safe default + owner. Owner: bdavis (2026-10-17) |
