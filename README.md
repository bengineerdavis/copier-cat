# copier-cat (cc)

A template manager for [copier](https://copier.readthedocs.io): adopt
templates into existing projects without data loss, push project fixes back
upstream as reviewable PRs through `contribute`, and run a whole collection of
templates as one monorepo with a chooser for picking between them.
First-class CLI + library API for humans and agents, with agentic skills
for building templates and driving cc — built so that cc leaves you better
at copier, never locked in (the graduation principle, spec C5/C6).

**Status: adopt MVP complete; deterministic assembly in progress.** The
governance stack and harness are seeded: [`PRINCIPLES.md`](PRINCIPLES.md)
is the constitution, [`spec.md`](spec.md) carries the requirements, and
roborev reviews every commit. The adopt MVP (CCC-1..3) is implemented and
archived. The merge engine, adopt flow, and CLI ship with a passing test
suite.

The [`backlog/`](backlog) store carries current work. Start with CCC-24
for the first Python-assembly slice and DOC-9 for its requirements.
CCC-30 owns the adopt/update teaching skill. The completed dogfood adopt
stamped this project with `python-project-template`; update it with
`copier update -a .copier-answers.copier-cat.yml`.

For historical provenance, see DOC-11
(`backlog/docs/seed-and-implementation-session-handoff.md`). It is not an
active instruction source.

The name: verified free on PyPI, npm, and crates.io (2026-10-12). The CLI
binary is `copier-cat`; `cc` collides with the C compiler and is left to
personal shell configuration (chezmoi), not to the project.

## CLI

The `copier-cat` CLI is a thin surface over the libraries (spec C5):
stable commands, stable exit codes, machine-readable JSON. Every
command's `--help` carries its copier-native equivalent, examples, and
exit-code contract — the graduation principle (spec C6) made
enforceable: nothing cc produces requires cc.

Help is a first-class interface for humans and agents. It names operands,
explains effects and write/approval scope, and uses copy-safe placeholders
such as `example-project` and `example-stack`. A destination is not a stack
name; JSON output is not consent. The proposed `help --json` and
`COMMAND --help --json` discovery contract is being designed through CCC-17;
it is not shipped yet.

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
[`agentic-project-template`](https://github.com/bengineerdavis/agentic-project-template).
Its CLI supplied the original deterministic merge-engine prototype. cc
generalizes that work behind its merger registry. The agentic template is
an ordinary Copier template and a future assembly member, not an engine
owner or special consumer. See DOC-11 for the historical relationship.
