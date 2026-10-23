# copier-cat (cc)

A template manager for [copier](https://copier.readthedocs.io): adopt
templates into existing projects without data loss, push project fixes back
upstream as reviewable PRs ("phone home"), and run a whole collection of
templates as one monorepo with a chooser for picking between them.
First-class CLI + library API for humans and agents, with agentic skills
for building templates and driving cc — built so that cc leaves you better
at copier, never locked in (the graduation principle, spec C5/C6).

**Status: Phase 1, adopt MVP complete.** The governance stack and
harness are seeded: [`PRINCIPLES.md`](PRINCIPLES.md) is the
constitution, [`spec.md`](spec.md) carries the requirements, the
[`backlog/`](backlog) store carries the working memory (tasks with
acceptance criteria, drafts, decisions, evidence), and roborev reviews
every commit. The adopt MVP (CC-1..3) is implemented and archived —
the merge engine, adopt flow, and CLI ship with a passing test suite.
Work continues from [`HANDOFF.md`](HANDOFF.md): the first cc skill
(C6) and the dogfood adopt.

The name: verified free on PyPI, npm, and crates.io (2026-10-12). The CLI
binary is `copier-cat`; `cc` collides with the C compiler and is left to
personal shell configuration (chezmoi), not to the project.

Origin: spun out of
[`agentic-project-template`](https://github.com/bengineerdavis/agentic-project-template)
— see HANDOFF.md for the relationship.
