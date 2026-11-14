---
id: DOC-9
title: Deterministic project assembly MVP
---

# Deterministic project assembly MVP

## Problem Statement

A developer has ordinary Copier templates that should contribute to one project,
but Copier composes one template at a time. For Python plus the agentic overlay,
the developer must know template sources, answers, ordering, shared-file rules,
and the wrapper that currently performs those steps. There is no portable,
reviewable copier-cat operation that creates that project while preserving each
template's independent native update lifecycle.

Agents face the same problem without a safe discovery and consent contract.
Terminal-formatted help is not a stable API, JSON formatting is not write
approval, and installing agent integrations must not require a particular
agent dependency manager or silently change global configuration.

## Solution

A developer or agent asks copier-cat to assemble a named stack into a named new
project directory. A small local catalog resolves the stack into ordered,
independent Copier templates with their sources, refs, and answers. Copier
renders each template in isolation; copier-cat extracts and composes shared
structure deterministically; validation runs automatically; the user reviews
and approves the destination write.

The first dogfood stack combines the existing Python project template with the
independent agentic overlay. Both can still render standalone with Copier. The
result contains native per-template answers files, so native updates still work
without copier-cat. The overlay can also compose with non-Python foundations.

Human and machine interfaces expose the same command descriptions, structured
examples, effects, and approval boundaries. `--json` without `--yes` is a
read-only preview; `--json --yes` authorizes only the displayed new-destination
write. The CLI does not require dotagents or MCP.

A later explicit agent setup may install a portable, standards-compatible skill
through dotagents or an equivalent open-standards path. It must remain optional,
visible, reversible, and independent of telemetry and MCP consent.

## User Stories

1. As a project author, I want to assemble a Python project with the agentic
   overlay, so that I do not need to remember two rendering commands and merge
   their shared files manually.
2. As a project author, I want to name the destination independently of the
   stack, so that `assemble research --stack agentic-python` clearly creates
   a project called `research` rather than a template called `research`.
3. As a project author, I want a named stack, so that repeated compositions do
   not require remembering sources, refs, and ordering.
4. As a template author, I want each member to remain an ordinary Copier
   template, so that it is usable and testable without copier-cat.
5. As a template author, I want the agentic overlay to be independent of Python,
   so that the same overlay works with other foundations.
6. As a template author, I want explicit member sources and refs, so that a
   fresh composition does not depend on another project's answers files.
7. As a project author, I want a read-only plan, so that I can inspect the
   composition before any project files are created.
8. As a project author, I want an explicit approval step, so that invoking a
   preview or requesting JSON cannot create a project silently.
9. As a project author, I want human-readable answer questions, so that I do
   not have to edit raw JSON mappings to use the workflow.
10. As a project author, I want template defaults applied when appropriate, so
    that a small request can produce a useful project without unnecessary
    questions.
11. As a project author, I want to override specific answers, so that I can
    select a different Python version or optional features without editing the
    templates.
12. As a project author, I want unknown or missing required answers to be
    visible, so that the tool does not invent project policy.
13. As a project author, I want deterministic TOML composition, so that the
    Python and agentic contributions both survive in one valid file.
14. As a project author, I want deterministic ordered-line `.gitignore`
    composition, so that additive ignore rules are retained without duplicates.
15. As a project author, I want unsupported shared files reported clearly, so
    that the tool never concatenates arbitrary text or silently picks a winner.
16. As a project author, I want disjoint paths from each template preserved, so
    that the generated project contains both templates' independent files.
17. As a project author, I want automatic validation, so that invalid TOML,
    missing native answers, or failed project tests stop the workflow loudly.
18. As a project author, I want isolated previews cleaned automatically, so
    that inspection does not leave hidden working directories.
19. As a project author, I want explicit preview retention to report its path
    and cleanup command, so that I can inspect a failure without unsafe cleanup.
20. As a project author, I want native answers files for every template, so
    that I can run ordinary Copier updates without copier-cat.
21. As a project author, I want a small provenance record of the selected stack
    and answers, so that I can understand what was composed.
22. As a project author, I want that provenance to be disposable, so that
    deleting it does not break native updates or create a runtime dependency.
23. As a project author, I want a useful short success result, so that I know
    the destination, validation status, and next action without a wall of logs.
24. As a project author, I want verbose diagnostics on request, so that I can
    inspect resolved sources, answers, and composition decisions.
25. As an agent operator, I want command discovery as JSON, so that I do not
    have to parse terminal-formatted prose.
26. As an agent operator, I want command-specific discovery, so that I can
    inspect one operation without downloading an unrelated surface.
27. As an agent operator, I want descriptions and structured examples in both
    human and machine help, so that each operand and effect is unambiguous.
28. As an agent operator, I want a versioned machine schema, so that clients
    can detect an incompatible help contract.
29. As an agent operator, I want help to be read-only and initialization-free,
    so that discovery cannot modify my environment.
30. As an agent operator, I want JSON without `--yes` to be a safe preview, so
    that automation can inspect a plan without a special bypass flag.
31. As an agent operator, I want JSON with `--yes` to be the only noninteractive
    write authorization, so that approval is explicit and narrowly scoped.
32. As an agent operator, I want structured operation results and errors, so
    that a skill or later MCP adapter can use the CLI without duplicating its
    planning, rendering, or composition logic.
33. As an agent operator, I want explicit failure for unsupported composition,
    so that the agent does not mistake a partial render for success.
34. As a CLI user without dotagents, I want to use every assembly operation, so
    that agent tooling is not a prerequisite for project creation.
35. As an agent user without dotagents, I want a standards-compatible skill
    installation path, so that I can still use conversational assembly.
36. As a dotagents user, I want optional skill installation through it, so that
    dependency refresh and removal follow my existing agent setup.
37. As an agent user, I want the source, scope, and exact setup command shown
    before installation, so that I can consent to the actual change.
38. As an agent user, I want global and project scope to be explicit, so that
    initialization never silently changes shared configuration.
39. As an agent user, I want initialization to be safe to rerun, so that it can
    refresh an identical declaration without resetting unrelated settings.
40. As a CLI user, I want initialization to be optional, so that a missing or
    declined configuration never blocks an otherwise valid workflow.
41. As a CLI user, I want noninteractive commands to avoid setup interviews, so
    that automation does not hang waiting for an answer.
42. As a template maintainer, I want real fixture evidence from the Python and
    agentic templates, so that the MVP proves the actual composition rather than
    a synthetic example alone.
43. As a maintainer, I want CLI acceptance tests and existing composition-engine
    tests, so that user behavior and deterministic data composition are tested
    at their existing public boundaries.
44. As a maintainer, I want a compact first workflow, so that feedback comes
    from using a real command instead of reviewing more prototype commands.
45. As a maintainer, I want deferred agent transports and advanced composition
    formats tracked separately, so that the first usable project is not delayed.

## Implementation Decisions

This feature document records scope and requirements, not a substitute for ADRs.
Durable architectural decisions live in `backlog/decisions/`: decision-3 through
decision-7 govern composition and assembly; decision-8 governs shared human and
machine help; decision-9 governs optional open-standards agent installation.
Implementation tickets should reference the applicable ADRs explicitly.

### Product and ownership boundaries

- Copier owns template rendering and native per-template updates. It does not
  compose two templates into one project by itself.
- copier-cat owns the stack recipe, template discovery, answer planning,
  isolated rendering orchestration, structured composition, validation,
  reporting, and narrowly scoped write approval.
- The agent skill interprets intent, selects a proposed plan, asks focused
  questions, and invokes CLI operations. It does not reimplement the engine.
- The MVP creates one new project from a named stack. A one-template stack is
  valid, but a single ordinary template needs no copier-cat to render.
- Do not wrap `agentic-project-template new` as the implementation. That would
  preserve the current wrapper architecture instead of making the stack recipe
  and composition engine portable.

### Stack and answer resolution

- The initial catalog is local YAML and contains the Python foundation and
  independent agentic overlay as separately usable templates, plus the named
  `agentic-python` composition. Exact catalog schema is settled during the
  first implementation ticket, not expanded speculatively here.
- Each composition member declares a stable identity, role, Copier source, ref,
  and answer inputs. It does not depend on a different project's local answers
  file for a fresh render.
- The agentic template declares overlay capabilities, not a dependency on the
  Python template. Language-specific optional components remain internal to
  the template.
- Answers come from explicit overrides, named stack defaults, template
  metadata, and ordinary environment conventions. Show their resolution in the
  plan; never hide additional answers or project policy.
- A missing required answer produces a focused question or a structured error
  in noninteractive mode. It never launches a setup interview in help or JSON
  discovery.
- Keep native Copier answers files separate per template. Do not invent a
  single synthetic template that owns the resulting project's update history.

### Composition and validation

- Use isolated native renders, extract structured contributions, compose them
  deterministically, and serialize each supported format once.
- Different structured keys are additive. A same-key collision requires a
  declared rule or review; never silently select a winner.
- Initial shared-file support is TOML and ordered, deduplicated `.gitignore`
  lines. Disjoint paths pass through unchanged.
- Other shared formats produce an explicit unsupported-composition result;
  arbitrary text concatenation is not a fallback.
- Copier's `--data` behavior replaces a whole supplied mapping. Do not pass
  partial per-layer mappings and assume Copier merges them. Compose complete
  structured inputs before a combined render, or compose structured render
  results through the same engine.
- The composition engine is the existing test surface. Add behavior at that
  boundary rather than introducing a second internal adapter architecture.
- Validate rendered structured files, native answers and provenance,
  deterministic/idempotent composition, and the generated project's own tests.
  Validation always runs, including guided mode, without extra write consent.
- A failed preview or validation cannot be reported as an assembled project.
  Stop with the failed stage and inspectable evidence; do not auto-resolve
  semantic conflicts.
- Automatic forward-update orchestration is not part of this milestone. Native
  per-template update commands are reported and must work independently.

### CLI and machine contracts

- The first real workflow is `assemble DESTINATION --stack STACK`, with
  read-only `--dry-run` and `--json` previews, optional `--guided` answer
  review, and explicit `--yes` destination approval.
- `stack list` and `stack show NAME` are the only initial catalog inspection
  commands. `stack new`, `stack edit`, template switching, fuzzy shorthand,
  and stack-wide updates wait for actual usage feedback.
- One versioned command-description model supplies human help and JSON help.
  Extract ordinary parameter help from Typer/Click; add structured examples,
  effects, native Copier equivalents, errors, and consent scope.
- `help --json` returns a command catalog. `COMMAND --help --json` narrows the
  same catalog to one command. Neither initializes, downloads, renders, or
  writes.
- Help explicitly distinguishes the new project destination from the named
  stack and states what `--dry-run`, `--json`, and `--yes` do.
- Default output reports the destination, validation outcome, and next action.
  Verbose/debug modes add evidence. JSON emits one structured result.
- Cancellation leaves no approved project destination. Preview cleanup and
  retention behavior must be visible and testable.
- `--yes` approves only the displayed new-destination write. It does not
  authorize agent installation, source-template changes, publishing, telemetry,
  or updates to an existing project.

### Optional agent setup

- Agent assistance is an optional consumer of the CLI, not a runtime dependency.
- The shipped skill uses open skill standards: portable Markdown instructions,
  declared discovery metadata, and references relative to the skill directory.
  It must not require dotagents-specific runtime behavior.
- `init` may offer installation through dotagents when available. The same
  portable skill must be obtainable through a standards-based path when
  dotagents is absent; CLI-only use requires neither.
- The installer displays source, skill name, scope, exact command or copied
  destination, and refresh/removal behavior before changing anything. Project
  scope is available for isolated evaluation; global scope is never implicit.
- For dotagents, use its supported scope and dependency operations rather than
  editing its managed files. For a standards-based fallback, copy only the
  declared skill files to the selected compatible skill directory; never edit
  unrelated agent configuration.
- Setup is idempotent, preserves unrelated configuration, and never silently
  resets existing declarations. Declining leaves the CLI fully functional.
- MCP setup is separate and later. Skill installation, MCP configuration, and
  telemetry/bug reporting require independent consent.

## Testing Decisions

### Seam

The user approved two test seams:

1. **CLI acceptance boundary:** invoke the real command in isolated temporary
   directories and assert observable output, files, exit status, cleanup, and
   approval behavior. Use the highest existing CLI test seam.
2. **Existing composition-engine boundary:** exercise deterministic structured
   contributions, extraction, merging, serialization, and conflict reporting
   through the engine's public library surface.

Do not add a new UI, MCP, service, persistence, or adapter-test seam for the
MVP. Tests should not inspect private helper calls or duplicate the production
merge algorithm as their expected result.

### Behavior to cover

- Discover the named stack and resolve each member's source/ref/answers.
- Render Python alone and Python plus the independent agentic overlay using
  actual local template fixtures and synthetic edge-case fixtures.
- Preserve the complete destination name; distinguish it from the stack.
- Produce valid TOML with both contributions, deterministic `.gitignore`, and
  all disjoint files; reject unsupported shared text visibly.
- Verify native answers and independent Copier updates for each template.
- Run generated-project tests and prove that validation failure is not success.
- Verify preview cleanup, explicit retention, cancellation, and no unexpected
  destination writes.
- Prove that JSON without `--yes` is read-only and JSON with `--yes` authorizes
  only the displayed destination.
- Check help/catalog parity, required descriptions/examples/effects, schema
  version, no initialization, and readable errors.
- Exercise optional agent setup in an isolated fixture with dotagents available
  and absent. Confirm the same portable skill works through the standards-based
  fallback and that no unrelated configuration changes.

### Prior art

Use the existing CLI subprocess/help and merger unit tests, the existing TOML
fixture pattern, and Copier's own scenario-testing conventions researched for
CCC-8. The interactive prototype is behavioral evidence only, not production
code or a substitute for real Copier renders. Synthetic examples must use
harmless names such as `example-project` and `example-stack`.

## Out of Scope

- General-purpose application generation or replacing Copier's rendering.
- Arbitrary unmodified-template compatibility or semantic conflict resolution.
- YAML, JSON, Markdown, arbitrary text, or binary shared-file composition.
- Automatic stack-wide forward updates or silently handling Copier `.rej`
  files. Native per-template updates remain required.
- Publishing templates, contributing changes upstream, or editing source
  templates after an assembly.
- Stack-definition generation, slots/cardinality policy, template inheritance,
  fuzzy shorthand, or advanced catalog/registry discovery.
- MCP implementation or requiring MCP for help and agent workflows.
- Mandatory dotagents installation, global agent changes, telemetry, or hosted
  bug reporting.
- Interactive recipe editing, template switching, shell completion polish, or
  further expansion of the interaction-only prototype.

## Further Notes

This spec consolidates the approved design decisions and two focused research
spikes. It does not supersede the existing composition, rendering, or help
ADRs. The detailed research and review documents remain in the project backlog;
implementation should be split into small tickets and executed in fresh
sessions after `/to-tickets`.

The immediate proof is one real, usable `assemble` vertical slice using the
actual Python and agentic templates, with feedback gathered from that workflow
before broadening the command surface.
