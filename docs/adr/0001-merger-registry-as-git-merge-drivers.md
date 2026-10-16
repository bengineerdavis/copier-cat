# Merger registry shaped as git merge drivers

cc's C1 adopt engine uses a registry of structure-aware mergers (TOML
deep-merge, YAML, marked sections) as its core, but each merger is shaped
like a git merge driver and the fallback is plain `git merge-file`, so the
file-level adopt flow reads as a git three-way merge. Decided over a pure
custom engine (the agentic-project-template prototype's shape) and a pure
git-merge design (no format awareness) to keep both determinism and the
upstream posture: copier#2376 proposes rebuilding `copier update` on
`git merge`, so a merge-shaped adopt interfaces with that direction
instead of fighting it.

## Considered options

- Port apt's engine as-is: rejected — a bespoke merge plumbing would not
  donate into a git-merge-based copier (#2376 is open and maintainer-
  reviewed).
- Conflict markers alone (copier#2486 MVP): rejected — cruft's `.rej` and
  marker-only complaint history (#49, #287) shows format-blind resolution
  is exactly the UX users suffer.
- mergiraf-style structural merging as a dependency: noted as composable
  with the driver shape (fohte/copier-update-action pairs it already);
  not adopted for cc's core while the registry can express the same
  contracts.