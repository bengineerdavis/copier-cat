---
id: CCC-17
title: Review the CLI against human and agent workflows
status: To Do
created_date: 2026-11-14 15:56
dependencies:
- CCC-14
- CCC-5
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Why: the CLI should be learned by real use before settling agent workflows, skills, and MCP. Preserve an MVP review map rather than freeze a broad command surface.

Ship:
- Walk the proposed human workflows through the current CLI prototype.
- Mark accepted behavior, tentative grammar, and gaps for first-use feedback.
- Derive agent workflows from the same deterministic operations.
- Use the findings to revise skills and CCC-5 MCP parity.

Constraints:
- MVP only; expect changes after maintainer use.
- CLI owns actions/workflow; skills guide invocation; MCP is transport.
- No hidden agent-only composition or implicit project writes.
- Prototype is not production code; verify before relying on it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A current CLI-to-workflow map covers init, discovery, stack editing, preview/guided assembly, validation, output, and errors
- [ ] #2 The maintainer has a concise human walkthrough and records friction or corrections from real use
- [ ] #3 Agent workflows and skill requirements are derived from reviewed deterministic CLI operations
- [ ] #4 CCC-5 is revised from existing-command parity to cover the reviewed assembly surface and explicit approval/error semantics
- [ ] #5 The review identifies what remains deferred rather than expanding the MVP
- [ ] #6 Human and agent help are first-class: operands, effects, examples, and approval boundaries are clear and testable
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Review entry: backlog/docs/cli-workflow-review.md. Prototype: /Users/ben.davis/code/personal/cc-assembly-ux-prototype/prototype.py.
Maintainer direction: come back later, walk through CLI against desired human workflows, tune it through real use, then derive agent workflows/skills/MCP inspired by backlog-py/backlog.md.
Do not treat the prototype as production. Before init work 15 simulated interaction cases passed; current first-run/config edits have not completed a final verification. Prototype does not inspect real config existence.
Proposed init behavior: ccc init; interactive first-run setup when no config; built-in defaults work after skipping; JSON/--yes never prompt; no implicit stack; existing/corrupt config must not be overwritten. These are requirements for review, not verified implementation.
Review should settle the smallest useful MVP rather than freeze every proposed shorthand.
First-use feedback 2026-11-14: user accepted case-insensitive confirmations as a class of input-behavior requirements; simulated init success must produce observable state and not repeat on the next invocation. Prototype now writes only the explicit CCC_CONFIG_FILE review marker after consent, preserves existing content, and shares tolerant y/yes/n/no parsing. 17 cases passed. Without CCC_CONFIG_FILE, init is dry-run only; no real preferences/config are stored.
Guided steps are in the right direction, but raw JSON answers are not the final UX. During implementation derive dynamic, human-readable questions from template metadata with defaults/types/validation/explanations. Ask Python version/include_backlog/etc individually or via a well-formatted interactive form; do not hard-code a Python questionnaire. Maintainer wants a bullet-proof intuitive interface and will work through remaining specifics in-session during implementation. Preserve this as acceptance feedback, not scope for indefinite prototype tuning.
Additional product boundaries accepted 2026-11-14: validation is presumed and always runs, including guided; it is not a permission question. Guided must show results so choices yield useful user/maintainer debugging feedback.
JSON preview should not require --yes. Prototype now returns status=preview, destination=null, approved=false for --json alone (exit 0); --json --yes is explicit approval of the new-destination write. 15 focused cases passed.
CCC-18 owns first-class bug reporting separate from general telemetry: human-friendly action/failure/next-step explanations; transparent exact payload/recipient/destination/purpose/redactions; opt-in init and later preferences; bounded deduplicated unique-issue offers; local report without Sentry; optional consent-gated Sentry adapter; never auto-submit or couple assembly approval to sharing. Those features are later design/implementation work, not prototype telemetry.
Remaining interaction details should be resolved with maintainer feedback during implementation rather than more throwaway tuning.
Maintainer first-class concern 2026-11-14: help usability for humans and machines. Decision-6 extended: help remains the teaching surface, now with named operands, effects, copy-safe examples, and versioned help --json / COMMAND --help --json discovery. The contract must distinguish DESTINATION from STACK and read-only preview from explicit write approval.
Proposed example: copier-cat assemble example-project --stack example-stack --dry-run means plan creation of new project directory ./example-project using named stack example-stack; no files written. --json alone is read-only; --json --yes approves only the displayed new-destination write. Help never triggers init or project/config writes.
Prototype help updated to use these terms and examples. Proposed illustrative schema: cc-assembly-ux-prototype/help_contract.py. Production help --json remains unimplemented; tests must enforce behavior/schema, not just prose. CCC-11 MVP should include this help contract for assemble, stack list/show, init, and top-level help rather than postpone operand clarity.
Prototype help surfaces now exist: human ccc --help and ccc assemble --help; machine ccc help --json and ccc assemble --help --json. Focused checks verify no config/init/writes, single DESTINATION operand, --stack STACK, example-project/example-stack copy-safe examples, read-only --dry-run/--json behavior, and JSON destination=null/approved=false. Machine schema is illustrative only. CCC-11 owns production schema and test coverage for the MVP commands; CCC-17 should test whether humans and agents can actually use them.
Research spike authorized 2026-11-14 before implementation. Requirement 1: agents must discover copier-cat operations, operands, options, descriptions, examples, side effects, errors, and approval scope without parsing terminal-formatted prose; a machine-help candidate that cannot carry examples/descriptions in a stable versioned structure is disqualified. Requirement 2: ccc init should enable the maintainer's agent workflows with minimal explicit reversible setup while CLI-only use remains intact and MCP stays optional; an approach requiring hidden global changes or non-idempotent installation is disqualified.
Use two focused primary-source research spikes rather than a broad deep-research program. Reports: backlog/docs/machine-readable-help-research.md and backlog/docs/agentic-init-research.md. Each must recommend one MVP path, cite primary sources, verify relevant installed surfaces, record rejected options, and separate MVP from later work. Prototype changes may follow only where they clarify the existing help example; no production implementation or global agent configuration changes.
Two focused research reports completed in-session after delegated spikes returned session summaries without artifacts:
- backlog/docs/machine-readable-help-research.md: recommend one shared versioned command-description model for human/JSON help, using Typer/Click metadata for ordinary parameters plus explicit examples/effects/consent. No MCP dependency or terminal-prose parsing.
- backlog/docs/agentic-init-research.md: init offers separate explicit dotagents skill installation with visible scope/source/command; MCP later and separately. No direct global OpenCode edits.
Prototype now returns catalog from help --json and focused contract from assemble --help --json. Both contain descriptions, usage, per-option effects, and structured examples. Focused checks verify catalog/focused parity and no initialization.
Research verification complete. Reports saved and prototype focused checks passed. Evidence boundary: backlog-py support is its installed CLI surfaces (2.2.0), not an asserted internal architecture. dotagents 3.4.0 installed help and official README support skills/MCP/scope/install/remove surfaces; OpenCode official docs support skill discovery and explicit MCP setup. No configuration changes or production implementation. Next: finish CCC-15 consolidation, then to-spec/to-tickets for the single usable assemble workflow.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
