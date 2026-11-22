# copier-cat glossary

The language copier-cat uses. Three groups, by where a term is owned:

1. **[Borrowed from Copier](#borrowed-from-copier)** — cited, unmodified.
   These follow upstream; if Copier redefines one, we follow.
2. **[Stack vocabulary](#stack-vocabulary)** — owned by the
   [stack specification](docs/stack-specification.md) and portable with it.
   Definitions live there; this file gists and links rather than restating.
3. **[copier-cat application vocabulary](#copier-cat-application-vocabulary)**
   — specific to `copier-cat`, not portable with the stack spec.

`copier-cat` is the package and full executable name; `ccc` is its built-in
alias. `cc` is never used — that is the system C compiler.

### Provenance note

The member/role/layer split was decided by the maintainer on 2026-11-14 and
recorded in the implementation notes of
[Research stack vocabulary and answers-file naming conventions](backlog/tasks/ccc-9%20-%20Research-stack-vocabulary-and-answers-file-naming-conventions.md).
That ruling was never written into this glossary, which is why later drafts
contradicted it. Adopted here 2026-11-22: **member** names a stack entry,
**layer** is reserved for internal organization within one template, and
**subproject** names the generated result. Parent/child language is avoided
for stack relationships because it suggests inheritance.

---

## Borrowed from Copier

Source: [Copier documentation, Basic concepts](https://copier.readthedocs.io/en/stable/#basic-concepts),
verified against Copier 9.19.1 on 2026-11-22.

**Project template** (Copier: *template*):
The reusable source that lays out how to generate a subproject. "Template"
alone is fine when no disambiguation is needed. Distinguished from the Jinja
templates a project template contains.

**Subproject** (Copier: *subproject*):
The result of rendering a project template — where the real, source-managed
program lives. Also simply "project". The template repository is a project in
the everyday sense too, so **subproject** is the disambiguating form when the
two could be confused.

**Questionnaire**:
The questions configured in a project template. Answers are used to generate
and update subprojects.

**Answers file**:
The per-subproject, per-template YAML file Copier writes recording the
template version and answers. The unit of coexistence when multiple templates
manage one subproject.

**Rendering**:
Generating a subproject from a project template. Copier owns this; copier-cat
orchestrates it and never renders itself.

**Template creator / template consumer**:
Copier's two audiences — maintainers of project templates, and the people who
apply them.

**Code scaffolding / code lifecycle management**:
Copier's two stated goals for project templates. copier-cat extends the
second, not the first: it does not become a template-independent application
generator.

### Related upstream terms we rely on

**Composition vs inheritance**:
[Copier#934](https://github.com/copier-org/copier/issues/934) distinguishes
composition — several templates render into one subproject — from inheritance,
where a child template extends a parent, and rejects treating them as one
mechanism. This is the upstream basis for the stack model.

**Template composition**:
[Copier's configuring documentation](https://copier.readthedocs.io/en/stable/configuring/#applying-multiple-templates-to-the-same-subproject)
names applying multiple templates to the same subproject, and requires a
different answers file per independently updated template. copier-cat builds
on that requirement rather than replacing it.

---

## Stack vocabulary

A **stack** is structure for applying one or more project templates, ordered
and composed. Either a project template or a stack produces a subproject; a
single project template is a valid one-member stack.

Full definitions and field schemas:
[docs/stack-specification.md](docs/stack-specification.md). Terms below are
gists with links to the defining sections.

**Stack**:
An ordered composition of project templates that can produce a subproject.
Not template inheritance.

**Stack definition**:
The reusable, ordered input — what was *asked for*. Lives in the catalog, not
in the subproject.
→ [definition](docs/stack-specification.md#stack-definition)

**Member**:
One entry in a stack: an ordered reference to a project template, with its
ref, role, and answers. **Not** "layer" — see the provenance note above.

**Anonymous stack**:
A stack definition with no name and no catalog entry, constructed at the
point of use. Same data type as a named stack; anonymity affects reusability,
not persistence. Single-template use needs no named stack.

**Role**:
A project template's intended contribution: `base`, `specialization`, or
`overlay`. Metadata about intent, not a different template technology, and
never by itself evidence of incompatibility.

**Base** / **Specialization** / **Overlay**:
The foundation; a project shape that may presuppose a foundation; and an
additive, cross-cutting concern independent of a particular language base.

**Stamp record**:
The per-subproject record of what was *actually applied* — resolved sources,
refs or content digests, answers, composition rules, and native update paths.
One definition yields many stamp records. Lives in the subproject at
`.copier-cat-stack.yml`, disposable without impairing native updates.
→ [stamp record](docs/stack-specification.md#stamp-record)

**Composition**:
Combining identified contributions from independently rendered templates into
valid shared files, using deterministic format adapters and explicit
precedence or review.

**Contribution**:
A structured fragment a template supplies to a shared file, identified by a
stable key, path, named region, or explicit text span. Distinct from an
upstream contribution prepared through `contribute`.

**Resolution report**:
Reviewable evidence of which member contributed each composed chunk, the
precedence rules applied, and any unresolved overlaps.
→ [resolution report](docs/stack-specification.md#resolution-report)

**Catalog**:
A small, user-level collection of named project templates and reusable stack
definitions. Enables discovery and reuse without hard-coding template paths
in agent prompts.

**Rendering runner**:
The engine copier-cat invokes to render a project template. Copier is the
only implemented runner; the abstraction is a seam, not a commitment to more.

### Reserved for internal template organization

**Layer**:
Internal organization *within one project template*, distinct from Jinja
templates and macros. **Not** a stack position — use **member**.

**Component**:
An internal concern within one project template, such as environment setup or
task management. Not an independently rendered stack member.

---

## copier-cat application vocabulary

Specific to copier-cat. These stay behind if the stack specification is ever
extracted.

**Stamped project**:
A subproject with a valid answers file and a recorded baseline, so plain
`copier update` works on it. A stamp record is what makes a project stamped.
_Avoid_: managed project, template-ed project

**Adopt**:
Bringing an existing subproject under a project template so it becomes a
stamped project, without data loss and with every change reviewable. Stamps
a template once; a second stamp of the same template points at **upgrade**.
_Avoid_: onboard, import, migrate

**Upgrade**:
Moving a stamped subproject to the versions its stack resolves, with no-op
detection and reviewable changes. Native equivalent:
`copier update -a ANSWERS_FILE`.

**Copy**:
Creating a new subproject from a project template or stack. Refuses an
existing destination and points at **adopt**. Native equivalent:
`copier copy`.

**Assemble**:
Retired as a CLI verb ([decision-11](backlog/decisions/decision-11%20-%20Copy-names-new-project-creation-assemble-is-retired-as-a-CLI-verb.md)).
Survives only as the internal capability name for the composition stage
(spec C8). Use **copy** for the command.

**Baseline**:
The recorded template state a stamped subproject's future updates merge
against.
_Avoid_: snapshot, seed commit

**Merger registry**:
The structure-aware, deterministic per-format mergers copier-cat uses to
combine subproject files with template output, with a fallback for unknown
formats.
_Avoid_: merge engine, merge driver

**Per-file review**:
The unit of consent in adopt: every rendered file is accepted, rejected, or
edited individually before it lands.

**Ownership map**:
copier-cat's record of which paths a template owns, derived from what the
render produces — never from template cooperation.
_Avoid_: file ownership config, template manifest

**Quarantine**:
The only staging area for content copier-cat removes. Nothing is destroyed
without a restorable backup, and restore is a first-class operation.

**Template-worthy change**:
A change made in a stamped subproject that belongs in the project template
rather than staying project-local.
_Avoid_: upstreamable change, template fix

**Changeset**:
A per-file unit of template-worthy change prepared for contribution.
_Avoid_: patch bundle, contribution set

**Contribute**:
Preparing, and only after explicit approval publishing, a template-worthy
change to its source project template. The commands are
`contribute prepare` and `contribute publish`.
_Avoid_: phone home except as historical language, contribute back, reverse sync

**Marked region**:
A named, byte-stable section inside a generated file that the project
template owns; a candidate for preservation across regenerations.
_Note_: the template owns the region *boundary*; who owns the region *body*
is an explicit orientation choice. copier-uv-bleeding's regions are
user-owned, copier-cat's are template-owned — same marker shape, opposite
precedence.

**Adaptation**:
A separately approved workflow proposing and validating a cohesive template
or compatibility change when existing templates cannot express the user's
intent.

**Compatibility proposal**:
A reviewable adapter or template changeset intended to resolve an identified
composition incompatibility, with validation evidence.
_Avoid_: agent merge

**Contribution candidate**:
A portable, paste-ready handoff describing a template-worthy change, its
target local template project, current evidence, and validation instructions.
_Avoid_: automatic upstream patch

**Consultation**:
Agent-assisted discovery of the intended application, constraints, and
appropriate templates before creation. Uses evidence and focused questions,
not a fixed questionnaire.
_Avoid_: requirements interview as a mandatory step

**Structural compatibility**:
Evidence that contributions can be identified, composed reproducibly, and
serialized into valid files. Does not by itself establish semantic fitness.
_Avoid_: automatic compatibility

**Preview**:
An isolated, copier-cat-owned assembly produced for inspection without
modifying the requested destination. Cleaned up after success or failure
unless explicitly retained.

**User config**:
Optional user-level preferences. Built-in defaults work without it;
declining setup never blocks a workflow. Never selects an implicit default
stack.
_Avoid_: mandatory setup

### Collections

**Collection**:
A repository hosting several project templates, each remaining a plain,
standalone-usable Copier template.
_Avoid_: template monorepo, template family

**Chooser**:
The flow helping a user select which project template in a collection to
apply.
_Avoid_: picker, meta-template (that term means a template that generates
templates)
