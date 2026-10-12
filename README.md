# copier-cat (cc)

A template manager for [copier](https://copier.readthedocs.io): adopt
templates into existing projects without data loss, push project fixes back
upstream as reviewable PRs ("phone home"), and run a whole collection of
templates as one monorepo with a meta-template for choosing between them.

**Status: seed / handoff.** There is no code yet by design — this repo
carries the vision, the grounded design context, and the decision record so
work can start from a fresh agent session. Read [`HANDOFF.md`](HANDOFF.md)
first, then [`spec.md`](spec.md).

The name: verified free on PyPI, npm, and crates.io (2026-10-12). The CLI
binary is `copier-cat`; `cc` collides with the C compiler and is left to
personal shell configuration (chezmoi), not to the project.

Origin: spun out of
[`agentic-project-template`](https://github.com/bengineerdavis/agentic-project-template)
— see HANDOFF.md for the relationship.
