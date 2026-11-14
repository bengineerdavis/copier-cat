---
id: CCC-9
title: Research stack vocabulary and answers-file naming conventions
status: To Do
created_date: 2026-11-14 04:49
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The emerging stack model needs stable names for any template used as a stack member, its composition role, and its per-project answers file. "Template" already names the reusable source in copier, while "layer" and "template type" currently conflate role, internal sub-layer, and specialization.

Ship:

- Research copier's canonical composition terminology, relevant composition standards or specifications, and practitioner vocabulary for stack members and roles.
- Recommend glossary entries for a generic stack member, foundation, specialization, cross-cutting overlay, internal sub-layer, and the distinction between source templates and their instances in a project.
- Recommend one deterministic answers-file naming convention, including parsing and migration rules, that works for template names containing hyphens.
- Record rejected vocabulary and filename patterns with reasons, and identify compatibility consequences for existing projects.

Constraints:

- Reuse copier's "template", "subproject", "answers file", and composition vocabulary where it fits; do not invent a competing term merely to avoid the ordinary noun "template".
- A role describes how a template participates in one stack, not a different kind of copier template or an inheritance relationship.
- Internal sub-layers remain separate from independently renderable stack members.
- Renaming answers files is deferred until the maintainer approves it; do not rename existing project files as part of this research.
- Verify load-bearing claims against the installed copier version or its maintained source and documentation.
- The filename convention must leave each native copier update -a command usable and preserve independent per-template update state.

Decision inputs from the maintainer 2026-11-14: "cross-cutting layer" should use a more intuitive single-word role; .copier-answers.<template>-<template type>.yml is an acceptable direction, but alternatives should be researched before locking it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A cited research note compares copier terminology, standards or specifications, and practitioner vocabulary for stack membership and roles
- [ ] #2 The note recommends glossary entries distinguishing source templates, stack members, composition roles, and internal sub-layers
- [ ] #3 The note recommends one unambiguous answers-file convention with parsing and migration rules for hyphenated template names
- [ ] #4 Rejected vocabulary and filename patterns are recorded with reasons and existing-project compatibility consequences
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Research snapshot 2026-11-14 (read-only research; no glossary decision recorded yet).

Requirement: one intuitive name for any stack member, separate names for composition roles, no confusion with Jinja templates or internal template components, and deterministic per-template answers filenames.

Evidence searched:

- Copier's maintained configuring documentation calls the reusable source a "template", calls "applying multiple templates to the same subproject" template composition, and requires a different answers file per independently updated template. Its parent/child example uses _external_data for one template's answers to inform another; it does not implement template inheritance. https://copier.readthedocs.io/en/stable/configuring/#applying-multiple-templates-to-the-same-subproject
- Copier issue #934 distinguishes composition (several templates render into one project) from inheritance (a child template extends a parent template); the maintainer comments reject treating these as the same mechanism. It also documents the reusable-source versus Jinja-template ambiguity. https://github.com/copier-org/copier/issues/934
- The Compose specification uses base and override files, ordered merging, and adding or overriding values. This supports ordered composition semantics, but "override" does not fit additive agent concerns as well as "overlay". https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/
- Practitioner systems commonly use "layer" for an ordered stack member and base/framework/addon for roles. Examples: createjsstack documents base, framework, database, and addon layers; TriStack uses base, framework, and addons; project-starter-template uses base plus overlays. https://www.createjsstack.dev/docs/how-it-works/ and https://tristack.space/docs/project-structure

Recommendation:

1. Keep "copier template" for the reusable source. Do not invent "unit", "module", "artifact", or "archetype" as a replacement; each either collides with existing software vocabulary or hides copier compatibility.
2. Define "layer" as one ordered application of a copier template in a particular stack, with its answers file and composition role. A template is source; a layer is its configured participation in one stack. This is the generic stack-member term.
3. Use "base" for the foundation role, "overlay" for a cross-cutting additive role such as agentic-project-template, and "specialization" for a project shape that presupposes a foundation, such as a Python web application. Role names describe relationships in a stack, not different copier template technologies.
4. Reserve "component" for an internal concern within one template, such as environment, review loops, or task management inside agentic-project-template. Components are not independently rendered stack members. This replaces the ambiguous "sub-layer" term.
5. Do not use parent/child for the general stack relationship; it suggests inheritance and obscures ordering. Do not use addon as the generic term: it implies optional features and does not cover foundations or specializations. Do not use module as the generic term: it collides with source modules and lacks ordering semantics.

Answers-file recommendation:

- Prefer .copier-answers.<template-name>.yml, where template-name is the stable unique template ID in the stack. This borrows copier's own examples and avoids renaming state when a template's role changes.
- If the maintainer requires the role in the filename, prefer .copier-answers.<template-name>.<role>.yml over a hyphen separator. A dot before a fixed role suffix parses unambiguously even when template-name contains hyphens. Example: .copier-answers.python-project-template.base.yml.
- Reject .copier-answers.<template>-<role>.yml as the canonical machine-parsed pattern: template names and role names both use hyphens, so the boundary is ambiguous without an external manifest.
- Role is not update identity. The answers file's _src_path and _commit identify the source template and version. A template should be usable in different stacks or roles without invalidating its update history.
- If one template may be applied more than once to the same project, template-name alone is insufficient; a distinct stack layer ID becomes necessary. Defer this case rather than encode duplicate occurrence numbers prematurely.
- Existing .agentic-answers.yml and other legacy names require an explicit migration with native copier update -a verification before renaming. No existing answers file was renamed during this research.

Pending maintainer decision: whether to keep the simpler template-only filename or require the visible role suffix. Glossary edits wait for that decision and confirmation of "component" for internal sub-layers.
Maintainer alignment 2026-11-14 — basic stack model and roadmap constraints:

- Drop slots from the basic model. A project template has an intended role; a stack orders project templates. Distinct application identities can be added later only if the same template needs multiple independent applications in one project.
- Do not use "layer" for a generic stack member. Reserve it for internal organization within one project template, so it remains distinct from Jinja templates and macros.
- Use base, specialization, and overlay as role names. A role is metadata describing the template's intended contribution, not a different kind of copier template.
- Recommended initial stack invariant: at least one base; any number of specializations and overlays. Do not add further cardinality rules before real composition cases require them.
- Do not infer a collision because two templates have the same role or appear similar. Semantic similarity is not deterministic enough to block a stack. Two different web specializations, for example, must not be rejected merely because both are web specializations.
- Roadmap validation may add explicit requirements and conflicts declared by template authors, plus warnings for competing capabilities. Actual unresolved file or chunk conflicts remain concrete composition results, separate from role compatibility.
- Keep this validation and similarity policy as roadmap material rather than near-term implementation.

These decisions supersede the earlier recommendation above to use layer as the generic stack-member term and the tentative discussion of slot-based identities.
Maintainer refinement 2026-11-14 — slots as meta-template constraints:

- Slots are useful for a reusable meta-template that describes a given stack type. They are not required merely to apply several templates to one project.
- A project template declares its intended role (base, specialization, overlay). A meta-template declares named slots and constrains which roles or template identities may fill each slot.
- A concrete stack binds selected project templates to those slots. A slot is the position and its selection constraints; a role remains the template's purpose; the project template remains the independently copier-renderable source.
- Example vocabulary: a web-application meta-template has a required base slot, an optional specialization slot, and repeatable overlay slots. Selecting templates checks their declared roles against slot requirements before rendering, catching incompatible combinations early.
- Slot constraints prevent incompatible combinations; they do not prove semantic compatibility and should not reject candidates merely for apparent similarity. Explicit conflicts and actual file/chunk conflicts remain separate checks.
- Treat meta-templates and slot-bound selection as roadmap material. Keep the basic direct-composition path independent of them.
Maintainer refinement 2026-11-14 — slot constraints and stack-level required templates:

- A slot can constrain accepted roles, candidate template identities, and cardinality. A base slot may accept exactly one template; that is a cardinality rule, not a general one-base-per-stack rule.
- A closed slot may allow exactly one template identity, for example a web-application stack definition with one specialization slot that accepts only flask-template. Do not assume every role accepts interchangeable alternatives.
- A stack definition may require a particular template identity, such as requiring the opencode overlay among otherwise repeatable overlays. Model this as a stack-level requirement rather than hiding it inside an unrelated slot or adding a new template role.
- Exact template identity does not mean pinning a git ref: keep the source/version in the concrete stack's answers file so the required template remains updatable.
- Pushback for the schema: separate slot cardinality (how many selections this position accepts), candidate constraints (which roles or identities can fill it), and stack requirements (which named slots or identities must be present). The OpenCode requirement must not accidentally limit a stack to exactly one overlay.
- Do not add an "opencode" role or make every overlay require OpenCode. Required identities belong in a particular stack definition, not in generic role semantics.
- Keep cardinality small and readable: exactly-one, optional-one, any; add bounded ranges only when a real stack needs them.
Maintainer refinement 2026-11-14 — cardinality and fresh-stack inputs:

- Reject exactly-one/optional-one/any and min/max as premature schema verbosity. A base slot may fit only one template, but defer cardinality syntax with the broader stack-format exploration.
- A stack recipe must contain all data needed to render every member on a fresh destination: template source usable with copier copy, ref where required, answers or referenced answer inputs, stable identity, role, order, and explicit requirements. Existing answers files provide update state after stamping; they are not sufficient inputs for a fresh composition.
- The stack recipe and the per-template answers files are complementary, not interchangeable. The recipe owns composition inputs; answers files own Copier's rendered answers, _src_path, _commit, and native update lifecycle.
- A stack may produce a project or another standalone Copier project template. Generating a template is not Copier inheritance.
- Slot candidates, exact-template requirements, and role constraints remain roadmap exploration. Do not turn an exact template requirement into a pinned version, and do not introduce template-specific roles such as "opencode".
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
