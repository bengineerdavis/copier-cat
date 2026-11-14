# copier-cat (cc)

A template manager for copier: it brings existing projects under copier
templates, routes template-worthy changes back upstream, and hosts
collections of templates. This glossary defines the language cc uses for
its own domain; copier's own vocabulary is treated as given.

## Language

### Projects and templates

**Stamped project**:
A project that has a valid copier answers file and a recorded baseline, making plain `copier update` work on it.
_Avoid_: managed project, template-ed project

**Adopt**:
Bringing an existing project under a template such that it becomes a stamped project, without data loss and with every change reviewable.
_Avoid_: onboard, import, migrate

**Baseline**:
The recorded template state a stamped project's future updates merge against.
_Avoid_: snapshot, seed commit

### Merging

**Merger registry**:
The set of structure-aware, deterministic per-format mergers cc uses to combine project files with template output, with a fallback for unknown formats.
_Avoid_: merge engine, merge driver (as a cc term)

**Per-file review**:
The unit of consent in adopt: every rendered file is accepted, rejected, or edited individually before it lands.

**Ownership map**:
cc's record of which paths a template owns, derived from what the render produces — never from template cooperation or added template conventions.
_Avoid_: file ownership config, template manifest

**Changeset**:
A per-file unit of template-worthy change prepared for contribution.
_Avoid_: patch bundle, contribution set

**Marked region**:
A named, byte-stable section inside a generated file that the template owns; candidates for preservation across regenerations.
_Avoid_: preserve markers, template-preserve (that name belongs to copier-uv-bleeding's mechanism)
_Note (CCC-2)_: the template owns the region boundary (the markers); who owns the region _body_ is an explicit orientation choice — copier-uv-bleeding's regions are user-owned, cc's are template-owned. Same marker shape, opposite precedence.

**Template-worthy change**:
A change made in a stamped project that belongs in the template rather than staying project-local.
_Avoid_: upstreamable change, template fix

**Contribute**:
Preparing and, after explicit approval, publishing a template-worthy change to its source template as a reviewable contribution. The CLI command group is `contribute prepare` and `contribute publish`.
_Avoid_: phone home except as historical language, contribute back, reverse sync

### Assembly and composition

**Assemble**:
Creating a subproject from one or more project templates, including source, answer, composition, and validation orchestration.
_Avoid_: assemble a template, inherit a stack

**Project template**:
A reusable Copier template when distinguished from the Jinja templates it contains. Every project template remains independently renderable.
_Avoid_: template type as a synonym

**Stack**:
An ordered composition of project templates that can produce a subproject or another project template.
_Avoid_: template inheritance

**Role**:
A project template's intended contribution to a stack: base, specialization, or overlay. A role is not a different template technology or an inheritance relationship.

**Base**:
A project template that supplies a subproject's foundation.

**Specialization**:
A project template that supplies a particular project shape and may require a base.

**Overlay**:
A project template that supplies additive, cross-cutting concerns independently of a particular language base.
_Avoid_: agent layer as a generic role

**Stack definition**:
The complete, ordered input for assembling a fresh subproject or project template, including template sources, optional refs, answers or answer-input references, roles, and explicit requirements. It is the reusable artifact users inspect and modify through `stack` operations; it is not required residue in every stamped project.

**Catalog**:
A small, user-level collection of named project templates and reusable stack definitions, with sources, optional refs, roles, and answer aliases. It enables discovery and reuse of app-level configuration without hard-coding template paths in agent prompts.

**User config**:
Optional user-level preferences for cc. Built-in defaults work without it. `ccc init` reviews and, with explicit approval, persists it; interactive first use may offer initialization. It does not select an implicit default stack.
_Avoid_: mandatory setup, environment stamp as an assembly prerequisite

**Assembly plan**:
The reviewable resolution of a stack definition into template sources, answers, destination, expected contributions, composition decisions, validation steps, and preview-cleanup behavior.

**Composition**:
Combining identified contributions from independently rendered templates into valid shared files using deterministic format adapters and explicit precedence or review.

**Contribution**:
A structured fragment a template supplies to a shared file, identified by a stable key, path, named region, or explicit text span. Distinct from an upstream contribution prepared through `contribute`.

**Adaptation**:
A separately approved workflow that proposes and validates a cohesive template or compatibility change when existing templates cannot express the user's intended application.

**Resolution report**:
A reviewable record of which template contributed each composed chunk, any precedence rule applied, and unresolved overlaps requiring review.

**Preview**:
An isolated, cc-owned assembly produced for inspection without modifying the requested destination. cc removes it after success or failure unless the user explicitly retains it; failure preserves a concise report and the retained path when retention was requested.

**Rendering runner**:
The engine cc invokes to render a project template. Copier is the initial runner; the assembly interface does not preclude other runners in the distant future.
_Avoid_: cc rendering engine

**Structural compatibility**:
Evidence that contributions can be identified, composed reproducibly, and serialized into valid files. It does not by itself establish semantic fitness.
_Avoid_: automatic compatibility

**Compatibility proposal**:
A reviewable adapter or template changeset intended to resolve an identified composition incompatibility, accompanied by validation evidence.
_Avoid_: agent merge

**Contribution candidate**:
A portable, paste-ready handoff describing a template-worthy change, its target local template project, current evidence, and validation instructions. It transfers work to a fresh session without modifying the target project or creating a PR.
_Avoid_: automatic upstream patch

**Consultation**:
The agent-assisted discovery of the user's desired application, constraints, required answers, and appropriate templates before assembly. It uses evidence and focused questions rather than a fixed questionnaire or speculative architecture.
_Avoid_: requirements interview as a mandatory assembly step

### Collections

**Collection**:
A repository hosting several copier templates, each remaining a plain, standalone-usable copier template.
_Avoid_: template monorepo, template family

**Chooser**:
The flow that helps a user select which template in a collection to apply.
_Avoid_: picker, meta-template (that term means a template that generates templates)

### State files

**Answers file**:
The per-project, per-template YAML file copier writes recording the template version and answers; the unit of coexistence when multiple templates manage one project.
