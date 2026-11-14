---
id: decision-8
title: Human and agent help share a command-description contract
date: 2026-11-14 17:01
status: accepted
---

## Context

Agents need to discover cc commands, operands, examples, effects, errors, and
approval scope without parsing terminal-formatted help. Typer/Click expose useful
parameter metadata but not a versioned CLI JSON contract, structured examples, or
cc's consent semantics. Terminal prose parsing is brittle, and MCP would be an
unnecessary prerequisite for CLI discovery.

The maintainer approved this contract after reviewing the saved machine-help
research and prototype on 2026-11-14.

## Decision

Use one versioned command-description model for human and machine help. Populate
ordinary names and parameter help from Typer/Click; add structured examples,
effects, consent scope, native Copier equivalents, and errors that the framework
does not model. `help --json` returns the catalog and `COMMAND --help --json`
narrows it. Both views use the same descriptions and examples.

Help is read-only and never initializes configuration or invokes a workflow.
Machine-readable assembly without `--yes` is a preview. Only explicit `--yes`
approves the displayed destination write; JSON formatting is never consent.

## Consequences

CLI help is sufficient for agent discovery without MCP. Adding a command or
option requires descriptions, examples, effects, and tests for both views. The
small domain model must not become a second CLI framework. Later skills and MCP
adapters consume the same CLI contract and do not reimplement its semantics.

Supporting evidence: backlog/docs/machine-readable-help-research.md. Feature
requirements and scope: DOC-9.
