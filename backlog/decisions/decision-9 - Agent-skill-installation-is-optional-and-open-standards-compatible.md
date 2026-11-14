---
id: decision-9
title: Agent skill installation is optional and open-standards-compatible
date: 2026-11-14 17:01
status: accepted
---

## Context

The maintainer wants conversational assembly in agent sessions without making
copier-cat depend on one agent dependency manager or silently modifying global
configuration. dotagents supports the maintainer's OpenCode setup, but must not
be a prerequisite for CLI use or for access to the skill.

The maintainer explicitly approved an open-standards-compatible installation path
with or without dotagents on 2026-11-14.

## Decision

Ship a portable skill made from Markdown instructions, discovery metadata, and
relative supporting files. Agent assistance is an optional consumer of the CLI;
plain assembly requires neither an agent integration nor MCP.

Initialization may offer dotagents installation when available. The same skill
must also be obtainable by copying its declared files into a compatible skill
directory when dotagents is absent. Show the source, selected skill, scope,
exact command or destination, and refresh/removal behavior before any change.

Setup is idempotent, preserves unrelated configuration, and never implicitly
selects global scope or resets existing declarations. Use dotagents' supported
operations rather than editing managed files. Skill installation, MCP setup,
and telemetry require separate consent.

## Consequences

Users without dotagents retain full CLI functionality and a documented skill
installation path. The implementation must test both installation routes in
isolated fixtures before promising refresh or rollback behavior. It must not
silently edit OpenCode configuration or bundle MCP setup into initialization.

Supporting evidence: backlog/docs/agentic-init-research.md. Feature requirements
and scope: DOC-9. Follow-up: CCC-14, CCC-17, and later CCC-5 transport design.
