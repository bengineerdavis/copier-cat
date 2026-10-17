# copier-cat principles (cc)

The governing layer. `spec.md` derives from this file and carries the
capability design the principles produce; this file carries why. The
layering is deliberate: capability design churns every session — these
do not, and changes here are decisions, not edits.

## What cc is

cc is a template manager for copier. Copier renders and updates projects
from one template; cc manages the *lifecycle around* that: bringing
existing projects under a template (adopt), carrying project-side fixes
back to the template so every inheriting project benefits (contribute /
phone home), and operating a collection of templates as one monorepo with
shared data and a chooser for selecting between them.

The test for every capability in spec.md: it extends the maintainer, it prefers
deterministic machinery over AI, and it never silently destroys or
silently publishes anything. These are principles, not firm rules; when
they conflict, the conflict is recorded and resolved deliberately.

## Principles

1. **Extend the human.** cc reviews and proposes; it never pushes,
   merges, or overwrites without an explicit human yes.
2. **Deterministic first.** Merges, diffs, and classifications are
   deterministic code where possible. AI is acceptable for classification
   suggestions, never as the merge engine, and its output is always
   reviewable.
3. **Upstream-friendly.** Where a capability belongs in copier itself
   (adopt is the live example — copier#2486), cc prototypes it in a form
   that could be donated upstream rather than forked forever.
4. **Layered governance.** This file is the constitution; spec.md derives
   from it. Ambiguity is marked, not resolved: open questions carry a
   safe default and an owner, and resolved questions move to the
   backlog store's decisions.
5. **Operates on regular copier templates.** cc acts on copier templates
   as their own units — any conforming copier template works with cc
   without cc-specific structure. cc's conveniences (monorepo hosting,
   shared data, automation) are additive layers on top, never
   prerequisites. A template that never touches cc's extras must remain
   fully usable by plain copier and by cc alike.

## Constraints

- cc never modifies a project or pushes to a remote without explicit,
  reviewable human consent at the moment of the action.
- The merge/diff engines are libraries with tests, usable independently
  of any CLI flow — the CLI is a surface over them, not the definition
  of them (spec C5).
- **No lock-in.** Anything cc produces or changes in a project is
  understandable and continuable with plain copier; every flow documents
  its copier-native equivalent (the graduation principle).
- cc stays tool-agnostic about which template is "in charge"; multi-template
  coexistence is a first-class state, not an edge case.

## Amending this document

- A principle or constraint changes only by an explicit, recorded
  decision in the backlog store — `backlog/decisions/` or a
  decision-log row naming the change and its owner — never as an
  implementation side effect.
- When a proposed change conflicts with this file, the conflict is
  surfaced and resolved deliberately; silent reinterpretation is a
  governance failure, not a shortcut.
- Agents never edit this file while implementing or designing; they
  surface the conflict and ask. This rule is the custody arrangement the
  advisory discussion produced: the file's editor must not be whoever
  happens to hold the working tree.
