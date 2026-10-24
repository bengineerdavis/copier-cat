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

## CLI

The `copier-cat` CLI is a thin surface over the libraries (spec C5):
stable commands, stable exit codes, machine-readable JSON. Every
command's `--help` carries its copier-native equivalent, examples, and
exit-code contract — the graduation principle (spec C6) made
enforceable: nothing cc produces requires cc.

| Command | What it does | Copier equivalent |
| --- | --- | --- |
| `merge` | Three-way merge of one file through the merger registry (TOML/YAML mergers, `git merge-file` fallback) | None — the per-file, pluggable form of copier's internal update merge (copier#2376) |
| `mergers` | List the shipped registry composition | None — copier's merge strategy is fixed; cc's is pluggable per format |
| `adopt` | Bring an existing project under a template: render → classify → per-file review → land → stamp | The middle ground copier lacks (copier#2486): between `copy --overwrite` (destroys) and `--skip` (starves); after adopt, plain `copier update` works |

Exit codes (all commands): `0` clean, `1` conflicts were presented
(resolved or not), `2` error. `--json` emits a machine-readable result
on stdout; in JSON mode the command is non-interactive by construction
— unanswered questions take the template's defaults, and files needing
review are refused with exit 2 unless `--accept-all` or
`--reject-all` is passed.

Examples:

```sh
# Human: review each proposed file (y/n/e per file)
copier-cat adopt ~/templates/python ~/my-project

# Agent: non-interactive, JSON on stdout, everything accepted
copier-cat adopt ~/templates/python ~/my-project --json --accept-all

# Answer questions explicitly, one flag per answer
copier-cat adopt ~/templates/python ~/my-project -a project_name=cc

# Merge one file through the registry
copier-cat merge --ours pyproject.toml --theirs render/pyproject.toml
```

Origin: spun out of
[`agentic-project-template`](https://github.com/bengineerdavis/agentic-project-template)
— see HANDOFF.md for the relationship.
