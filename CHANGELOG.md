# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/); versioning follows
[SemVer](https://semver.org).

## [Unreleased]

### Changed

- Assembly writes one `<stack name>.stack.yml` containing the stack definition
  and its application state, rather than `.copier-cat-stack.yml` and a separate
  stamp record. Copier's native per-template answers files remain separate.
  The assembly JSON result names this artifact in `stack_artifact` rather than
  `provenance`.

### Fixed

- Adopt preserves Copier's rendered answers file byte-for-byte, including
  template-specific formatting. Sequential native updates no longer leave a
  formatting-only change that makes Copier refuse the next dirty project.
- Stack names and template IDs are validated before preview paths are built,
  so catalog input cannot write outside the isolated preview or destination.
  A template contribution that uses the reserved stack-artifact path is
  rejected rather than overwritten.
- Plain-directory templates can be assembled without Git. They have no commit
  baseline for a versioned Copier update, which validation reports explicitly.
  Dirty no-ref Git templates retain their working-tree render; validation uses
  a clean committed copy without modifying the source template.
- Trusted templates pass their `unsafe` setting to native-update validation,
  and their emitted update commands include `--trust`.
- Shared TOML same-key conflicts require a declared precedence rule or review.
  Empty TOML documents are accepted as valid contributions.

### Verified

- Lifecycle scenarios apply a base stack, extend it through reviewed
  single-template adoption, delete the stack artifact, and upgrade both
  templates to real tagged versions through plain Copier. Project-owned files
  survive and repeated unchanged updates leave Git clean.

## [0.1.0] - bootstrap

### Added

- Initial project scaffold, stamped from `python-project-template` (base)
  and `agentic-project-template` (agentic layer).
