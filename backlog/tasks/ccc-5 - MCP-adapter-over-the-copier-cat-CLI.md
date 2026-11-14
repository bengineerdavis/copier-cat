---
id: CCC-5
title: MCP adapter over the copier-cat CLI
status: To Do
created_date: 2026-11-12 19:26
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->

The `copier-cat` CLI ships `merge`, `mergers` and `adopt` with `--json`,
stable exit codes (0 clean, 1 conflicts presented, 2 error) and a
non-interactive JSON mode (CCC-3, CCC-4). Agent sessions cannot reach it
without a shell: there is no MCP server, so stamping a templated stack
from a session means hand-written shell invocations.

Ship:

- An MCP server exposing one tool per shipped CLI command (`merge`,
  `mergers`, `adopt`), each invoking the `copier-cat` CLI with `--json`.
- Tool schemas mapping parameters onto CLI flags, including `--accept-all`
  and `--reject-all` for the non-interactive adopt path.
- Exit-code translation: 0 returns the parsed JSON result, 1 returns the
  conflict set, 2 returns a tool error carrying the CLI's stderr.
- A documented `agents.toml` entry so the server installs through
  dotagents.
- CLI/MCP parity coverage: a test asserting the tool list matches the
  shipped command set.

Constraints:

- The MCP layer adds no merge, adopt or classification logic; it is a
  transport over the CLI, the same split backlog-md-py uses (deterministic
  actions and workflow in the CLI, MCP and skills as callers).
- The graduation principle (spec C5/C6) holds: nothing the MCP layer does
  may be unavailable to a plain CLI user.
- Interactive per-file review stays CLI-only; MCP tools are
  non-interactive by construction.

Decision record — agreed with the maintainer 2026-11-12: adapt over the
CLI rather than the library API, so the CLI stays the single source of
truth.

<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An MCP server exposes one tool per shipped CLI command (merge, mergers, adopt), each invoking the copier-cat CLI with --json
- [ ] #2 Tool schemas map parameters onto CLI flags, including --accept-all and --reject-all for the non-interactive adopt path
- [ ] #3 Exit code 0 returns the parsed JSON result, 1 returns the conflict set, 2 returns a tool error carrying the CLI's stderr
- [ ] #4 An agents.toml entry is documented so the server installs through dotagents
- [ ] #5 A test asserts the MCP tool list matches the shipped CLI command set
- [ ] #6 The MCP layer contains no merge, adopt or classification logic: review confirms every tool delegates to the CLI
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Future scope gate: CCC-17 (backlog/docs/cli-workflow-review.md) must review human CLI workflows and derive the agent surface before MCP assembly implementation. Existing CCC-5 acceptance criteria cover only shipped merge/mergers/adopt; they do not provide parity for proposed init/stack/assemble operations. Reconcile the tool list, JSON schema, explicit consent/error semantics, and tests after that review. MCP remains a CLI transport, not an independent workflow engine.
Consent/output clarification from CCC-17: --json alone is a read-only preview with no --yes requirement; --json --yes approves only the explicitly displayed new-destination write. MCP must expose separate inspect/preview and approved-write semantics, never treat a format flag as consent. Validation is always run, including guided, not a separate optional approval. CCC-18 separately governs diagnostic sharing and telemetry; MCP/agent invocation never implies either.
Agent-init research (backlog/docs/agentic-init-research.md) confirms MCP should be a separate opt-in setup after CCC-17 reviews CLI/agent operations and CCC-5 schema/consent contracts. ccc init must not silently enable MCP. Machine-help research (backlog/docs/machine-readable-help-research.md): share one versioned command-description model across human help and help --json; descriptions/examples/effects/consent belong in CLI contract, not MCP-only discovery. Typer/Click metadata supplies ordinary parameter help but not stable CLI help schema or approval semantics.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
