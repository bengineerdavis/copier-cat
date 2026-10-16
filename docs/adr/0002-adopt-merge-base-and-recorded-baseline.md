# Adopt uses an empty-tree merge base; the recorded baseline is the answers file

These are two decisions, and keeping them distinct is the point:

**Adopt-time merge base: an empty tree.** Template files that collide with
project files are merged with an empty tree as the merge base — they
arrive as fresh additions resolved against the project's current content,
each resolution reviewed per-file. The template initial version and a
synthetic snapshot are rejected for this role: a snapshot base tells the
adopt-time merge that project content is template content, and an initial
version is arbitrary vintage that makes a re-stamped project and a fresh
one diverge in mechanics.

**The recorded baseline for later updates: the copier answers file.**
Adopt closes by writing a valid answers file pointing at the adopted
template's current version, so plain `copier update` works exactly as the
copier#2486 MVP describes — the MVP presents the empty base as one of two
adopt-time merge formulations and closes adopt by writing answers that
make updates work. Recording a synthetic snapshot of the merged render as
the update baseline is rejected: it would tell every future update that
conflict-resolved project content is template content, poisoning the
three-way merge and the user-modifications diff C2's classification is
seeded from. The empty merge base avoids project→template misattribution;
its cost — template files contradicting project content surface as
add/add-style merges — is paid once, in the review flow, not at every
update.