# Empty-tree baseline for adopted projects

After `cc adopt`, the recorded baseline that later `copier update` calls
merge against is an empty tree — template files arrive as fresh additions
resolved against the project's current content. Decided over the
template's initial version and a synthetic snapshot commit of the render
at adoption time: a snapshot baseline tells copier that conflict-resolved
project content *is* template content, poisoning every future three-way
update against the project's own words; the empty tree is what the
adopt-MVP reasoning in copier#2486 converges on and is the only scheme
that cannot misattribute project-local edits to the template.

## Considered options

- Template initial version: rejected — arbitrary vintage, and adopting a
  re-stamped project would need a different answer than a fresh one.
- Synthetic snapshot commit: rejected — poisons update's user-diff
  classification (the C2 seed) by marking project content as baseline
  template content.