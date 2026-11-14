---
id: DOC-6
title: CLI workflow review for human and agent use
---

# CLI workflow review

## Review question

Does the proposed `ccc` CLI map to the way the maintainer wants to work? Start
with the MVP, use it, and change the workflow from observed friction. Derive
agent workflows, skills, and MCP from that review rather than designing a
parallel agent-only product.

## Current status

The design and prototype are exploratory, not a released CLI. The prototype is
`/Users/ben.davis/code/personal/cc-assembly-ux-prototype/prototype.py`.
It simulates rendering, configuration writes, downloads, and project tests.

A 2026-11-14 smoke run passed 17 configured/automation cases, including init,
selection, direct assembly, stack listing/composition, typo rejection, JSON,
case-insensitive confirmation, and non-TTY/no-config paths. This is prototype
coverage only.

`CCC_CONFIG_FILE` selects a review-only marker whose file existence suppresses
first-run init. Explicit init consent creates only that marker; its comment
content is never parsed, and an existing marker is preserved. With no marker
environment variable, even explicit init is a dry run and cannot touch the real
default config. JSON, `--yes`, and non-TTY use never prompt. Optional
`prompt_toolkit` and `rapidfuzz` provide fuzzy selection, with a numbered menu
fallback. Real config parsing, schema, and preservation remain unimplemented.

A later focused run passed 15 cases covering the revised read-only JSON
preview boundary and existing configured workflows. These tests use synthetic
config markers and simulated operations; they are not production validation.

The earlier 15 cases covered direct stack invocation, selector behavior,
mise-style stack composition, typo rejection, guided stages, JSON approval
boundaries, ambiguous selection, and source-download cancellation.

## Help is a first-class human-and-agent interface

Every command's help must explain its purpose, named operands, effects,
write/approval scope, exit/error behavior, and native Copier equivalent.
Examples use harmless placeholders and say what each operand means. A user
must not need to guess that `example-project` is a new destination rather than
a stack, or that JSON formatting is not write approval.

Proposed assembly help:

```text
Usage: copier-cat assemble [OPTIONS] DESTINATION

DESTINATION  New project directory, for example ./example-project.
--stack STACK  Named template composition, for example example-stack.
--dry-run      Read-only plan; no project writes.
--json         Read-only machine plan; no --yes required.
--yes          Approve only the displayed new-destination write.
```

Copy-safe examples:

```sh
# Read-only human plan; no writes.
copier-cat assemble example-project --stack example-stack --dry-run

# Interactive assembly; review before writing ./example-project.
copier-cat assemble example-project --stack example-stack

# Agent discovery; never executes the operation or initializes config.
copier-cat help --json
copier-cat assemble --help --json

# Agent read-only plan; JSON is not consent.
copier-cat assemble example-project --stack example-stack --json

# Agent explicitly approves only the displayed new-destination write.
copier-cat assemble example-project --stack example-stack --json --yes
```

`help --json` and `COMMAND --help --json` are proposed machine-readable
discovery surfaces, not additional operations. Their versioned schema covers
operands, options, outputs, effects, errors, native equivalents, and consent.
Human help remains the teaching surface per decision-6; agent help must not
require parsing terminal-formatted prose. Tests must enforce both surfaces.

The prototype implements illustrative `help --json` and `assemble --help --json`
surfaces in `/Users/ben.davis/code/personal/cc-assembly-ux-prototype/help_contract.py`.
Its human help names `DESTINATION` and `STACK`, and its examples use
`example-project` and `example-stack`. Focused checks verified help without
config/init/writes and read-only `--dry-run`/`--json` previews. Production help
remains unimplemented; the schema and enforcement tests belong in CCC-11/CCC-17.

## Review map

| User intent | Proposed invocation | Expected behavior | Review focus |
| --- | --- | --- | --- |
| First interactive use | `ccc` followed by an interactive command | Offer init when no user config exists; resume the requested workflow after setup or skipping | Useful orientation versus setup fatigue |
| Initialize explicitly | `ccc init` | Preview preferences and confirm before writing user config | What belongs in user-level config? |
| Work without config | Any ordinary command | Built-in defaults work; no mandatory setup | Is declining setup frictionless? |
| Discover stacks/templates | `ccc stack list`; `ccc stack show NAME` | Inspect available reusable configurations and their sources/answers | Is the catalog easy to understand? |
| Create/edit a stack | `ccc stack new NAME`; `ccc stack edit NAME` | Modify the reusable stack, not the generated project | Does `stack` map 1:1 to the artifact? |
| Add a template | `ccc --stack NAME use TEMPLATE\|SOURCE` | Resolve and review an ordered template addition | Is this natural enough to remember? |
| Assemble a known stack | `ccc assemble DESTINATION --stack STACK` | Resolve, preview, obtain consent, render/compose/validate, report | DESTINATION is the new project directory; STACK is the composition |
| Preview a known stack | `ccc assemble example-project --stack example-stack --dry-run` | Show a read-only plan for `./example-project`; no `--yes` | Do users understand what each operand means? |
| Choose interactively | `ccc DESTINATION` | Fuzzy stack selector; no implicit default | Does selection help without guessing? |
| Use an unknown template | Interactive selector → guided source setup | Accept a Copier-compatible source; separate approval before isolated download | Does the empty-catalog path feel safe? |
| Review deliberately | `--guided` | Resolve, answers, compose, validate, assemble with real edit/review opportunities | Does the user learn or merely confirm? |
| Inspect detail | `-v`; `--debug` | Additional human context; diagnostic stderr respectively | Useful evidence versus noise |
| Inspect a plan as JSON | `--json` | One versioned read-only machine preview; no `--yes`, no interactive setup | Is the schema sufficient and stable? |
| Approve a write as JSON | `--json --yes` | Approve only the displayed new-destination write scope | Is approval still explicit without a terminal? |
| Understand an error | Ordinary command fails | Human-friendly explanation, local diagnostics, safe recovery | Can the maintainer understand the failure? |
| Report a bug | Later opt-in report flow | Preview exact payload, recipient, destination, purpose, and redactions | Can users report without telemetry or an account? |
| Configure diagnostics | `ccc init`, later preferences | Bug reporting and general telemetry are separate opt-ins | Are both easy to decline and disable? |
| Make a typo | e.g. `ccc recipie` | Suggest `stack`, make no writes, explain literal-name escape | Is a bare token a project or command? |
| Update a template | Native `copier update -a ANSWERS_FILE` | Independent template update lifecycle remains available | Is the no-lock-in path visible? |
| Improve a template | Later `contribute prepare/publish` | Prepare a portable candidate; separate explicit publication | Keep outside the first-use MVP |

## Human walkthrough

Use the prototype as a discussion aid, not as the production implementation.

1. Try `ccc init` and cancel. Does the remaining workflow still make sense?
2. Try a bare project request and select a stack. Try an ambiguous query and
   cancel. Confirm no implicit default is chosen.
3. Create a named stack and add a template using the mise-inspired `use` form.
4. Assemble a known stack with default output, then inspect `-v` and `--json`.
5. Repeat with `--guided`, editing answers and cancelling at each stage.
6. Try a nonexistent template source and decline its download.
7. Try misspelled commands and literal project names.
8. Record the point where the tool explains too much, asks too much, or hides
   a consequential decision. Prefer observed friction over hypothetical polish.

## Agent and MCP derivation

Keep the backlog-md/backlog-py split: the CLI owns deterministic actions and
workflow; skills guide selection and interpretation; MCP is a transport over
CLI operations. Skills do not reimplement planning, rendering, or composition.

Review these questions only after the human workflow:

- Which operations should be one-step workflow tools versus lower-level tools?
- How does an agent explicitly authorize a new destination, template download,
  existing-project change, or publication without interactive prompts?
- What JSON schema, exit/error model, and idempotency guarantees are required?
- How are ambiguous stack selection and missing templates handled without a TTY?
- Which preview, validation, and attribution evidence belongs in the tool result?
- How should `contribute` return a paste-ready candidate for a fresh session?
- How are the installable skill and `agents.toml` entry kept in sync with the CLI?

CCC-5 currently promises parity only for shipped `merge`, `mergers`, and `adopt`.
Do not treat that as coverage of the proposed assembly surface. Revise it after
this workflow review, including `init`, stack operations, assembly, approval,
errors, and machine-readable results.

## First-use feedback

The maintainer observed that accepting simulated config generation still caused
setup to repeat on the next invocation. The prototype now makes the simulated
state observable through its review marker and preserves an existing marker.
Shared confirmation parsing accepts case variants, reprompts invalid input,
and fails closed on interruption. Production must test this as a behavior class,
not a collection of unrelated prompts.

The guided direction is accepted, but the prototype's raw answer mapping is not
an acceptable final interface. Python version, backlog inclusion, and similar
values need approachable questions with individual defaults, types, validation,
and explanations. A well-formatted interactive form is acceptable if the user
can provide all answers at once. Derive the questions from template metadata;
do not hard-code a Python-specific questionnaire into the CLI.

The maintainer wants this interface to be bullet-proof and intuitive. Work on
the remaining interaction details during implementation, using in-session
feedback rather than expanding the prototype indefinitely.

## Open for the review session

- Minimal stack-definition and catalog schema, and where user config lives.
- First-run setup content, TTY/non-TTY detection, corrupt-config handling,
  config preservation, and an explicit `--no-init` policy if needed.
- Whether interactive init should run before every first command or only before
  workflow commands that benefit from it; help/version must remain immediate.
- Bare-token grammar and the balance between concise commands and discoverable
  explicit forms.
- Real Copier behavior, preview cleanup, generated-project validation, and
  performance; the synthetic prototype answers none of these.
- First-use feedback from the maintainer before freezing the agent surface.

## Help usability gate for implementation

The existing `Copier equivalent:` and `Exit codes:` checks remain necessary but
are not sufficient. Before shipping a new or changed command, test:

- Its human help names operands and explains their meanings and effects.
- Copy-safe examples use explicit placeholders and distinguish previews from
  writes; examples never imply that a destination is a template name.
- `help --json` and command-specific `--help --json` are discovery-only and
  return the same versioned operation/argument/effect/consent contract.
- Help works with no config, no TTY, no initialization, and no project writes.
- JSON assembly without `--yes` is read-only; `--yes` approves only the
  displayed new-destination write and never authorizes another operation.
- An agent can discover required inputs and approval scope without parsing
  terminal-formatted prose or guessing from examples.
