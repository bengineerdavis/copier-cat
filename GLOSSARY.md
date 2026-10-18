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
A per-file unit of template-worthy change prepared for phone home.
_Avoid_: patch bundle, contribution set

**Marked region**:
A named, byte-stable section inside a generated file that the template owns; candidates for preservation across regenerations.
_Avoid_: preserve markers, template-preserve (that name belongs to copier-uv-bleeding's mechanism)
_Note (CC-2)_: the template owns the region boundary (the markers); who owns the region _body_ is an explicit orientation choice — copier-uv-bleeding's regions are user-owned, cc's are template-owned. Same marker shape, opposite precedence.

**Template-worthy change**:
A change made in a stamped project that belongs in the template rather than staying project-local.
_Avoid_: upstreamable change, template fix

**Phone home**:
Routing a template-worthy change from a stamped project back to the template repository as a reviewable, human-triggered contribution.
_Avoid_: contribute back, reverse sync

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
