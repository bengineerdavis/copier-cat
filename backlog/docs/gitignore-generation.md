---
id: DOC-4
title: Reuse evidence for deterministic gitignore generation
---

# Gitignore generation and composition

## Requirement

Assemble shared `.gitignore` files quickly and reproducibly from ordered
project-template contributions. Ordinary assembly and its tests must work
offline, preserve intentional negation/order semantics, and never discard a
local contribution silently. Requiring a network service, a server runtime, or
a guessed conflict winner disqualifies a candidate.

## Recommendation

Reuse **GitHub's official CC0 template collection** as the optional pattern-data
source. Pin its commit in a stack definition and cache the selected templates
locally before ordinary assembly. Compose them with a small deterministic
adapter: first occurrence of each exact nonblank/noncomment pattern wins;
preserve order and comments; retain the first local negation at its original
position; report discarded exact duplicates by contributor.

Do not call gitignore.io during ordinary assembly. Its JSON endpoint is a useful
online acquisition alternative, not an offline generation engine. No network
access is required after a stack's pattern-data revision has been cached.

This is a design recommendation with primary-source evidence, not an approved
implementation or a performance measurement.

## Evidence

### Primary sources

- [GitHub gitignore collection](https://github.com/github/gitignore): the
  repository describes its templates as the source for GitHub's template
  choosers. Common patterns live at the root; `Global/` and `community/` hold
  specialized patterns. [Its license](https://github.com/github/gitignore/blob/main/LICENSE)
  is CC0 1.0 Universal.
- [GitHub REST gitignore documentation](https://docs.github.com/en/rest/gitignore/gitignore):
  `GET /gitignore/templates` lists names and `GET /gitignore/templates/{name}`
  returns a template. This is another acquisition option, not a requirement.
- [Git's gitignore manual](https://git-scm.com/docs/gitignore): within one
  precedence level, the last matching pattern decides the outcome. A negated
  pattern (`!`) re-includes a previously excluded file, but cannot re-include a
  file beneath an excluded parent directory.
- [gitignore.io README](https://github.com/toptal/gitignore.io/blob/master/README.md):
  generated files are CC0; the service is MIT-licensed. Its documented
  [`api/list?format=json`](https://docs.gitignore.io/use/api.md) endpoint returns
  template key, name, contents, and filename.

### Repository observations

At `toptal/gitignore.io` commit
[`fd3331d935ac5029c59d4f4455c4bd1b29dcb3b1`](https://github.com/toptal/gitignore.io/commit/fd3331d935ac5029c59d4f4455c4bd1b29dcb3b1)
(2024-12-23), the service is Swift/Vapor and references a `gitignore` submodule
at `0a7fb01801c62ca53ab2dcd73ab96185e159e864`. The URL stored in `.gitmodules`
(`https://github.com/toptal/gitignore.git`) returns 404. Do not pin a stack to
that unavailable data path. The current public service can be queried instead;
its runtime implementation does not need to be adopted.

The API was queried successfully on 2026-11-14. This establishes availability at
that time, not an uptime or stability guarantee.

## Proposed behavior

1. A stack may request named patterns or use a template's explicit `.gitignore`
   contribution. Unknown named patterns fail visibly.
2. Acquisition uses an explicitly pinned data revision. Missing cached data is a
   clear offline error, never a silent empty contribution.
3. Exact duplicate pattern lines deduplicate at first occurrence. Do not
   normalize slashes, whitespace, comments, or negations.
4. Preserve a local negation's position relative to the template exclusions that
   precede it. Deduplication must not move a negation above its first match.
5. Do not discard one of two semantically different patterns. Git decides
   behavior using its documented last-match rule; suspicious reorderings or
   incompatible contribution contracts are review items, not automatic merges.
6. Validate with `git check-ignore` fixtures for ordinary exclusion, negation,
   excluded-parent, exact duplicate, order preservation, offline cache,
   idempotence, and attribution cases.

This deliberately avoids a universal "semantic line merge." Git's matching
semantics remain the authority; the adapter performs only transformations whose
preservation properties are demonstrated by tests.

## Rejected options

| Option | Why rejected |
| --- | --- |
| Runtime gitignore.io API dependency | Network availability and unpinned responses would make ordinary assembly nondeterministic and non-offline. |
| Run the Swift/Vapor service locally | Adds a server/runtime to generate a small text file; unnecessary for a pinned-data adapter. |
| `toptal/gitignore` submodule data | The referenced repository URL currently returns 404; it is not a dependable source to pin. |
| Plain set union or sorted pattern list | Destroys meaningful order, especially negation behavior. |
| Global last-pattern-wins deduplication | Can move or discard a negation relative to the exclusion it overrides. |
| Hand-maintained technology-pattern catalog | Duplicates the curation already supplied by the CC0 collections; use it only for explicit project-specific contributions. |
| Alphabetical or "semantic" conflict guessing | No deterministic evidence supports discarding a different pattern or choosing a winner. |

## Open implementation choices

- Whether the initial data cache contains only selected templates or a pinned
  archive of the collection.
- How template metadata requests optional technology patterns versus supplying
  literal project-specific patterns.
- Exact cache location and the command used for explicit data refresh.
- Whether negation-sensitive cases beyond the tested safe path block assembly or
  produce a review-required result.

These choices do not justify a new general-purpose gitignore service.
