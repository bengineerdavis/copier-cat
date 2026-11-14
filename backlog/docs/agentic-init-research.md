---
id: DOC-8
title: Agentic initialization research for copier-cat
---

# Agentic initialization research

## Requirement

`ccc init` should enable the maintainer's agent sessions to use copier-cat with
small, explicit, reversible setup. Plain CLI works without configuration and
MCP remains optional. Hidden global changes, silent downloads, or a second
composition engine are disqualified.

## Recommendation

Make init **layered and idempotent**:

1. Local preferences/catalog setup, with built-in defaults always available.
2. An **opt-in copier-cat skill installation through dotagents**, with a preview
   of source, selected skill, destination scope, and exact external command.
3. A separate, later **opt-in MCP setup** only after the CLI/agent surface is
   reviewed and CCC-5 is revised.

For the maintainer's primary OpenCode setup, user/global scope is the most useful
default for a reusable copier-cat skill, but it is never implicit: `dotagents`
defaults to global scope, so cc must display that scope before invoking it.
Project scope should be an explicit alternative for repo-only evaluation.

Do not make init write arbitrary OpenCode JSON itself. Let dotagents own its
supported projections and managed files. Keep installation, removal, and refresh
as ordinary visible commands. Declining agent setup leaves CLI use intact.

## Evidence

### dotagents, installed 3.4.0

`dotagents --help` on 2026-11-14 showed `init`, `install`, `add`, `remove`,
`sync`, `list`, `mcp`, `trust`, and `doctor`. No scope flag means global
`~/.agents/`; `--project` selects repository-local state. `add` discovers and
installs selected dependencies; `install` refreshes the declared dependencies;
`remove` removes dependencies. The official README documents `agents.toml` as
the source of truth for skills, MCP, hooks, subagents, and plugins across hosts:
[dotagents README](https://github.com/getsentry/dotagents#readme).

The installed `add --help` says re-adding an identical declaration refreshes its
installation successfully. `init --help` has `--agents` and `--force`; cc should
not need to run it when an existing scope is already configured. It should never
pass `--force` silently.

Illustrative setup commands, not an authorization to execute them:

```sh
# User-scope reusable skill; global is dotagents' default, shown explicitly.
dotagents add <copier-cat-skill-source> <skill-name>

# Project-scoped evaluation instead.
dotagents --project add <copier-cat-skill-source> <skill-name>

# Later refresh or removal through the same scope.
dotagents install
dotagents remove <skill-name>
```

The source and skill name must come from the actual shipped package/skill
layout, not guessed from this report. A local `path:` source can support
maintainer dogfooding, but a portable published source is needed for normal use.

### OpenCode's supported surfaces

The official [OpenCode skills documentation](https://opencode.ai/docs/skills/)
says skills are discovered from global and project `.opencode/skills`, with
compatibility discovery from `.claude/skills` and `.agents/skills`. Skills with
a description are advertised to the model and loaded on demand; HTTP catalogs
and explicit source directories are supported. dotagents can project skills to
OpenCode, so it is the appropriate owner of that projection for this maintainer.

The official [OpenCode MCP documentation](https://opencode.ai/docs/mcp-servers/)
says MCP tools consume model context and only needed servers should be added.
It documents explicit `opencode mcp add`, `--global`, `mcp list`, and disabling
servers. This supports keeping MCP optional and visible, not silently enabling
it during first-run setup.

The official [MCP 2025-11-25 schema](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts)
separates tool listing from tool calls. This is consistent with a safe
read-only discovery path and explicit invocation approval. It does not justify
configuring a server before its tools are settled.

### backlog-py/backlog.md precedent

Installed `backlog-py 2.2.0` exposes `agents --update-instructions` and an
`integration` command group whose `install-legacy-mcp-shim` is explicitly an
integration helper. Its top-level CLI owns task/workflow operations. This is a
useful precedent for making integration opt-in rather than mixing it into core
project assembly. It is not evidence that a new MCP server or generated global
agent config should be a prerequisite for cc.

The user-supplied `research` and `review-best-practices` skill bodies were read
on 2026-11-14. They direct research to primary sources and recommendation rather
than a survey; they are process inputs, not product evidence.

## Ranked approaches

1. **Preferences + optional dotagents skill setup (recommended).** Reuses the
   maintainer's declared agent dependency manager; OpenCode support is already
   documented; visible and reversible; no duplicate engine. MVP must still ship
   the actual skill before enabling the option.
2. **MCP setup later.** Useful for hosts where MCP is preferred or shell access
   is constrained. Defer until CCC-17's workflow review and CCC-5's tool/error/
   approval contract are settled. Offer separately, never bundle consent.
3. **Direct OpenCode config editing.** Rejected for the maintainer's setup:
   duplicates dotagents ownership and risks hand-editing managed/global files.
   A generic host adapter may be considered later for non-dotagents users.
4. **Copy a skill into `.opencode/skills` directly.** Possible for a controlled
   fixture but does not provide portable dependency refresh/removal across
   hosts. Reject as the normal init mechanism.
5. **Full plugin/daemon setup on first run.** Exceeds the MVP need and expands
   trust/network/global-state surface. Rejected.

## MVP user flow

1. Run `ccc init`; show existing config, preferences, and planned changes.
2. Ask separately: "Make the copier-cat skill available to your coding agents?"
3. If yes, show source, skill, user versus project scope, exact dotagents
   command, and whether refresh/removal changes existing declarations.
4. Execute only after explicit approval. Report success or preserve the old
   state on failure. Never claim a write that did not happen.
5. Explain that `dotagents install` refreshes dependencies, how to remove the
   skill, and that plain `copier-cat` needs none of this.
6. MCP is a separate later offer, not part of skill or telemetry consent.

Initialization should be safe to rerun: detect existing declarations, preserve
unrelated config, refresh identical declarations, and do not force-reset scope.
Help and JSON discovery must not run this flow.

## Open implementation questions

- Exact shipped skill name and source (local dogfood versus published repo).
- Default scope prompt wording and how agents are selected when dotagents has
  multiple targets. Do not infer or rewrite an existing `agents` list.
- Whether cc invokes dotagents or emits an approved command for the user; prefer
  subprocess with a displayed plan and no shell interpolation.
- Dotagents removal/rollback semantics for a previously existing declaration;
  verify in an isolated fixture before promising complete rollback.
- How the skill tells agents to call CLI help and obtain write approval.

## Scope boundary

MVP agent setup needs one usable skill through one supported dependency manager.
It does not need a universal host adapter, plugin marketplace, MCP server,
automatic telemetry, or autonomous template composition. Those follow actual
use and the CCC-5/CCC-14/CCC-17 reviews.

Research completed in-session after two delegated spikes returned session
summaries without writing the requested artifacts. No configuration, skill
installation, network download, or project generation was performed.
