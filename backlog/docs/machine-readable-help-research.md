---
id: DOC-7
title: Machine-readable help research for copier-cat
---

# Machine-readable help research

## Requirement

Agents must discover copier-cat operations, operands, options, command
descriptions, examples, side effects, errors, and approval scope without parsing
terminal-formatted prose. A candidate that cannot expose descriptions/examples
and consent/write semantics in a stable, versioned machine-readable form is
disqualified.

## Recommendation

Use **one versioned command-description model as the source for both human help
and `help --json`**. Populate ordinary names and parameter help from Typer/Click
metadata; add structured examples, effects, consent scope, native Copier
equivalents, and output/error descriptions that the framework does not model.

Keep human `COMMAND --help` and machine `COMMAND --help --json` as two renderings
of the same description. `help --json` returns the catalog; command-specific help
returns one command. Both are read-only and bypass initialization. JSON Schema
may document the output, but is not itself the command-discovery vocabulary.

This is a small domain model, not a new CLI framework. The existing prototype's
custom schema is justified by approval semantics and structured examples, not by
JSON being fashionable.

## Evidence

### Installed framework capabilities

On 2026-11-14 the copier-cat environment had Click 8.5.0 and Typer 0.27.3. An
in-session check of `typer.main.get_command(copier_cat.cli.app)` returned a
`TyperGroup`; each command exposes `help`, `epilog`, and typed parameter objects
with `name` and `help`. Current `merge`, `mergers`, and `adopt` expose their
human help and argument descriptions through this API. Typer's official command
help documentation describes docstrings, argument/option help, epilogs, and
panels: [Typer command help](https://typer.tiangolo.com/tutorial/commands/help/).

Click's official API exposes `Command.get_help`, parameter objects, and context
objects: [Click API](https://click.palletsprojects.com/en/stable/api/). These
objects are useful metadata, but there is no installed `COMMAND --help --json`
contract, schema version, structured example model, or consent model. Do not
assert that Click has native JSON help based on this metadata alone.

The existing `src/copier_cat/cli.py` and `tests/test_cli.py` already treat help
as enforceable behavior: command help must carry `Copier equivalent:` and
`Exit codes:`. Decision-6 is the local governing precedent.

### Structured descriptions and examples

JSON Schema's meta-data vocabulary explicitly includes `title`, `description`,
`default`, and `examples` annotations for documentation and UI hints:
[JSON Schema meta-data](https://json-schema.org/draft/2020-12/json-schema-validation#name-a-vocabulary-for-basic-meta-data).
Its core vocabulary provides `$schema` and `$id` for identifying schemas:
[JSON Schema core](https://json-schema.org/draft/2020-12/json-schema-core).

These annotations support the recommendation to expose command and option
descriptions and structured examples. They do not define CLI invocation,
filesystem effects, or approval. cc must define those domain fields and test
their meaning rather than overload `readOnly` to mean CLI safety.

MCP's official 2025-11-25 schema similarly gives tools names, descriptions,
input/output JSON Schemas, and read-only/destructive/idempotent/open-world
annotations: [MCP schema](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts).
Those annotations are hints, not consent. This supports explicit effect fields
and separating discovery from invocation. MCP tool annotations do not replace
CLI help or automatically convey destination approval.

### Practitioner surfaces

Installed `backlog-py 2.2.0` exposes a conventional command tree through
`--help`, with separate `completion` and opt-in `integration` commands. Its
actual help was inspected on 2026-11-14. No general CLI-help JSON surface was
asserted from its CLI alone. backlog-py is useful as a CLI/skills/MCP ownership
example, not as evidence that terminal prose is machine-parseable.

The preserved copier-cat prototype's
[`help_contract.py`](https://github.com/bengineerdavis/copier-cat/blob/bf924fd/prototype/cc-assembly-ux/help_contract.py)
contains a command, named destination, option effects, structured examples,
exit codes, and approval scope. It is synthetic and not a production contract.

## Options ranked

1. **Shared command model + two renderers (recommended).** Meets descriptions,
   examples, effects, consent, and human parity. Costs a small explicit model
   and consistency tests. Use framework metadata for ordinary parameters;
   duplicate nothing that can be safely extracted.
2. **Serialize Typer/Click objects directly.** Good starting metadata but fails
   structured examples, stable public schema, native equivalents, and consent.
   Keep as an input, not the contract.
3. **MCP-only discovery.** Fails CLI-only agents, adds a server dependency, and
   does not provide a standard CLI usage/example contract. Optional transport
   later; not the source of truth.
4. **Parse terminal help.** Fails the requirement: formatting is not a stable
   semantic API. Rejected.
5. **OpenAPI for CLI.** Models network operations, not terminal operands,
   approval flags, or native Copier equivalents. Rejected for this purpose.

## Prototype changes justified

Add command description, usage, per-option descriptions, structured examples,
`read_only`, `writes`, and explicit approval scope to the machine response.
`help --json` must return the command catalog rather than one command. Keep
schema versioning and a native Copier equivalent field. Do not put unbounded
human prose, terminal markup, or an entire composition engine in help.

## Tests for implementation

- Human and JSON help share the same descriptions and structured examples.
- Every command and option has a description; every example has a command,
  effect, and explicit write/approval scope.
- Help never initializes config, prompts, downloads, renders, or writes.
- JSON parse and schema-version checks pass; unknown versions fail clearly.
- New commands fail tests until descriptions, examples, effects, and native
  equivalents are supplied.
- `help --json` contains the command catalog; command help narrows it.

## Scope boundary

MVP needs top-level discovery and help for the real core commands. Do not build
an interactive help browser, generic CLI-description standard, MCP server, or
full execution planner to satisfy this requirement.

Research completed in-session after two delegated spikes returned session
summaries without writing the requested artifacts. No external files or
configuration were changed by the research.
