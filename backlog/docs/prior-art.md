---
type: reference
id: DOC-2
title: Prior-art findings (research session 2026-10-13)
---

Evidence and direction, not decisions (PRINCIPLES.md amendment logic applies: findings resolve against these explicitly, never silently). Recorded 2026-10-13; migrated from spec.md 2026-10-17.

### cruft — the closest analogue for update/adopt state and diff flow

- State is a pointer file: `.cruft.json` holds template URL, pinned
  commit, prompt answers (frozen at create time), skip globs. No diff
  content is persisted.
- Update = double render (old at recorded commit with old answers, new
  at HEAD) + `git diff --no-index` patch + `git apply -3`, falling back
  to `git apply --reject` (`*.rej` files).
- Adoption exists minimally as `cruft link` (since 1.1.0): re-prompts
  for variables to reconstruct context, verifies nothing, and the
  community flow (`link` then `diff | git apply`) misses files the
  project lacks (#256).
- Complaint cluster maps 1:1 onto cc's design requirements: #49 (top
  ask: better `.rej` UX), #206 (render-in-repo + editable diff), #287
  (conflict markers harder than `.rej`), #53/#67/#181 (false success
  after partial application), #181 (`git apply -3` needs blobs shallow
  clones lack — breaks CI update bots), #142 (stored branch ignored),
  #232 (new template parameters silently skipped), #256 (project-only
  files invisible to diff; locally-deleted template files not reported).
- Maintenance is slow (release ~annual; 2.16.0 Dec 2024).

Direction this gives cc: per-file/per-hunk review beats all-or-nothing
patch application; adopt must reconcile state with the real project
rather than re-prompt blind; the `git apply -3` blob dependency rules
out that mechanism for CI-targeted flows.

### copier upstream signals

- #2376 (open): proposal to rebuild `copier update` on `git merge`.
  Directly affects C1's donatable shape — a conflict-marker-based adopt
  would fight the direction of travel; a merge-shaped design composes.
- #2487 (PR, closed 2026-04-10 unmerged, no stated reason; review asked
  for rename to `onboard`, dropping `.rej` support because of #2376,
  and minimal scope). Community revival attempts got no response.
  Warning for the upstream posture: closure-without-explanation is a
  live risk; donatability also means small, deference-shaped changes.
- #2463 merged `copier check-update`; #2529 discussion spawned
  natescherer/copier-action. Downstream-update automation is where
  ecosystem energy goes.
- #2005 (conflict markers on copy) and #1738 (multi-template merge)
  remain open — cc's C1 generalizes both.
- Ecosystem update tooling: fohte/copier-update-action pairs copier
  update with mergiraf (an SMT-based merge tool — prior art for
  structural merge); natescherer/copier-action; KyleKing's
  copier-template-tester (stamp testing prior art for C6 skills).

### Contribute-back (C2): the gap is real and unclaimed

- No tool exists that detects template-worthy changes in a generated
  project and opens PRs to the template repo. Copier tracker, cruft
  tracker, GitHub-wide and web searches all return zero hits.
- cruft's `diff --exit-code` is framed as contribute-back *support*
  ("ensures any improvement to the template is always submitted
  upstream") but submission is entirely manual.
- copier's `update` already computes the user-modifications diff
  internally (fresh render at recorded commit vs current project);
  no command exports it as an artifact. That computation is the seed
  of C2's classification input.
- flexlate (multi-engine, git-native, 0.x) stores resolution history
  in internal branches; syncs manual changes into its own branches so
  they survive updates — mechanical prior art, but no upstream flow.

### Monorepo of templates (C3): what exists and what doesn't

- Copier's stated position: 1 template = 1 git repository (tags are
  repo-global; update machinery depends on them). Multi-template-repo
  requests #1078, #1279, #1571, #315 all closed pointing at docs; a
  maintainer notes a subdir-addressable src URL "could actually work"
  (unimplemented). #2300 (open) is destination-monorepos, a different
  problem. Remote URLs cannot address a subdirectory template.
- Verified multi-template repos in the wild
  (sdsc-ordes/repository-template, UABGH-Emerging-Technologies/Templates,
  WaylonWalker/devtainer, GoogleCloudPlatform/solutions-builder,
  mitodl/ol-infrastructure): all (a) clone-then-local-path, (b) use a
  custom wrapper CLI/script as the chooser, (c) give each template its
  own answers file, (d) accept degraded versioning (repo-global tags).
- Chosen patterns resembling cc's goals: sdsc-ordes hands template 1's
  answers to template 2 via `--data`; UABGH delegates via `_tasks`
  running `copier copy` on a `common/` template; worldworm layers
  `-ext` templates with separate answers files; SS-NES meta-template
  maintains a REGISTRY.md of derived templates (hand-maintained).
- No copier-native chooser/meta-picker exists anywhere found — one
  `copier.yml` asking "which stack?" then delegating onward is
  unclaimed. Choosers are always external tools (fzf scripts, just
  targets, bespoke CLIs). The one-template-with-toggles alternative
  (lincc-frameworks/python-project-template) trades per-stack
  repos/tags for a single questionnaire.

Direction this gives C3: cc's monorepo + chooser is the gap everyone
works around with custom wrappers; the price of admission is solving
subdir-addressable URLs/tags or wrapper-based local-path flows, and
`!include`/`_external_data` are the sanctioned sharing primitives any
shared-data design must build on rather than replace.
