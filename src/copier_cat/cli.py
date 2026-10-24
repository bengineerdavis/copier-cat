"""copier-cat CLI: a thin surface over the libraries (spec C5).

The engines are importable libraries; this CLI exposes the same
operations with stable commands, stable exit codes, and JSON output.
The merge registry surface is here from CC-1; adopt from CC-3.

Exit codes: 0 merged clean, 1 merged with conflicts, 2 error. Adopt
completes with 1 whenever any rendered file conflicted — resolved or
not, the run presented conflicts.
"""

from __future__ import annotations

import difflib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import typer

from .adopt import (
    CONFLICT,
    IDENTICAL,
    FilePlan,
    Rendered,
    apply,
    classify,
    render,
    stamp,
)
from .merge import MergeToolError, default_registry

app = typer.Typer(
    help="copier-cat: template manager for copier.",
    epilog=(
        "copier-cat extends copier's lifecycle: copier renders and updates a\n"
        "project from one template; cc brings existing projects under\n"
        "templates (adopt), routes template-worthy fixes back upstream\n"
        "(phone home, planned), and manages template collections. Nothing\n"
        "cc produces requires cc: every command documents its copier-native\n"
        "equivalent and leaves you with plain copier."
    ),
    no_args_is_help=True,
)

EXIT_CLEAN = 0
EXIT_CONFLICTED = 1
EXIT_ERROR = 2

# The graduation principle made visible (spec C6): every command's help
# carries its copier-native equivalent, usage examples, and its
# exit-code contract. The "Copier equivalent:" marker is enforced by
# test — a new command without its teaching fails review.

_MERGE_EPILOG = """\
Copier equivalent: none — copier merges whole trees inside `copier
update` (git-merge-based per copier#2376); this is the same machinery
in pluggable, per-file form, usable independently of adopt. An empty
--base is the adopt shape: the template file arrives as a fresh
addition resolved against the project's current content.

Examples:
  copier-cat merge --ours pyproject.toml --theirs render/pyproject.toml
  copier-cat merge --ours a.toml --theirs b.toml --base base.toml
  copier-cat merge --ours a.toml --theirs b.toml --json

Exit codes: 0 merged clean; 1 merged with conflict markers in the
output (resolve them yourself — cc never writes the tree); 2 error.
"""

_MERGERS_EPILOG = """\
Copier equivalent: none — copier's merge strategy is fixed inside
`copier update`; cc's registry is pluggable per file format. Lists the
shipped composition (format mergers plus the git merge-file fallback)
so you can predict how adopt resolves each file.

Exit codes: 0.
"""

_ADOPT_EPILOG = """\
Copier equivalent: the middle ground copier lacks (copier#2486).
`copier copy --overwrite` destroys project content; `--skip` and
_skip_if_exists starve the project of template improvements; `copier
update` needs a recorded baseline an adopted project doesn't have.
adopt renders the template, classifies every file (add / identical /
merge / conflict), takes your per-file consent, lands only what you
accept, and writes the answers file — after which plain `copier
update` works (the stamped-project guarantee).

Examples:
  copier-cat adopt ~/templates/python ~/my-project
  copier-cat adopt ~/templates/python ~/my-project --defaults
  copier-cat adopt gh:org/tpl ~/proj -a project_name=cc --json --accept-all

Exit codes: 0 clean adopt; 1 conflicts were presented (resolved or
not); 2 error.
"""


def _read(path: Path, what: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        typer.secho(
            f"error: {what} file {path} is not valid UTF-8: {error}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_ERROR) from error
    except OSError as error:
        typer.secho(
            f"error: cannot read {what} file {path}: {error}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_ERROR) from error


def _emit_warnings(warnings: tuple[str, ...]) -> None:
    for warning in warnings:
        typer.secho(f"warning: {warning}", fg=typer.colors.YELLOW, err=True)


@app.command(epilog=_MERGE_EPILOG)
def merge(
    ours: Path = typer.Option(
        ..., "--ours", help="Project-side file (kept on conflicts)"
    ),
    theirs: Path = typer.Option(..., "--theirs", help="Template-render file"),
    base: Path | None = typer.Option(
        None,
        "--base",
        help="Merge base file; omit for the empty tree (adopt, decision-2)",
    ),
    path: str | None = typer.Option(
        None, "--path", help="Path key for merger selection (default: theirs filename)"
    ),
    output: Path | None = typer.Option(
        None, "--output", help="Write merged text to this file (combinable with --json)"
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Emit a JSON result on stdout"
    ),
) -> None:
    """Merge one file three ways through the merger registry."""
    registry = default_registry()
    key = path if path is not None else theirs.name
    base_text = _read(base, "base") if base is not None else ""
    ours_text = _read(ours, "ours")
    theirs_text = _read(theirs, "theirs")
    try:
        result = registry.merge(key, base_text, ours_text, theirs_text)
    except MergeToolError as error:
        typer.secho(f"error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(EXIT_ERROR) from error
    except Exception as error:  # the exit-code contract outranks traceback noise
        typer.secho(
            f"error: {type(error).__name__}: {error}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(EXIT_ERROR) from error

    if output is not None:
        _write_file(result.text, output)
    if json_output:
        typer.echo(
            json.dumps(
                {
                    "path": key,
                    "merger": result.merger,
                    "conflicted": result.conflicted,
                    "warnings": list(result.warnings),
                    "text": result.text,
                },
                indent=2,
            )
        )
    else:
        _emit_warnings(result.warnings)
        if output is None:
            # Stdout carries exactly the bytes --output would write: the
            # merged text, verbatim.
            sys.stdout.write(result.text)
    raise typer.Exit(EXIT_CONFLICTED if result.conflicted else EXIT_CLEAN)


def _write_file(text: str, output: Path) -> None:
    try:
        output.write_text(text, encoding="utf-8")
    except OSError as error:
        typer.secho(
            f"error: cannot write {output}: {error}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(EXIT_ERROR) from error


@app.command(epilog=_MERGERS_EPILOG)
def mergers(
    json_output: bool = typer.Option(
        False, "--json", help="Emit a JSON result on stdout"
    ),
) -> None:
    """List the default merger registry's composition."""
    registry = default_registry()
    payload = {
        "mergers": [merger.name for merger in registry.mergers],
        "fallback": registry.fallback.name,
    }
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
    else:
        for name in payload["mergers"]:
            typer.echo(name)
        typer.echo(f"fallback: {payload['fallback']}")


def _fail(message: str) -> None:
    typer.secho(f"error: {message}", fg=typer.colors.RED, err=True)
    raise typer.Exit(EXIT_ERROR)


def _parse_answers(pairs: list[str]) -> dict[str, str]:
    """Split repeated QUESTION=ANSWER options into a answers mapping."""
    data: dict[str, str] = {}
    for pair in pairs:
        key, sep, value = pair.partition("=")
        if not sep or not key:
            _fail(f"--answers expects QUESTION=ANSWER, got {pair!r}")
        data[key] = value
    return data


def _describe(plan: FilePlan) -> str:
    if plan.current is None:
        return "new file"
    return "conflict markers" if plan.conflicted else "changed"


def _review_one(plan: FilePlan, project: Path) -> tuple[bool, str | None]:
    """Prompt for one file's consent: accept, reject, or edit (grill round 2)."""
    typer.echo(f"\n{plan.path} — {plan.classification} ({_describe(plan)})")
    for line in difflib.unified_diff(
        (plan.current or "").splitlines(keepends=True),
        plan.proposed.splitlines(keepends=True),
        fromfile=f"a/{plan.path}",
        tofile=f"b/{plan.path}",
    ):
        sys.stdout.write(line)
    for warning in plan.warnings:
        typer.secho(f"warning: {warning}", fg=typer.colors.YELLOW, err=True)
    while True:
        choice = (
            typer.prompt(
                f"Apply {plan.path}? [y]es/[n]o/[e]dit",
                default="n",
                show_default=False,
            )
            .strip()
            .lower()
        )
        if choice in ("y", "yes"):
            return True, None
        if choice in ("n", "no"):
            return False, None
        if choice in ("e", "edit"):
            edited = typer.edit(plan.proposed)
            if edited is None:
                return False, None
            return True, edited


def _review(
    plans: list[FilePlan],
    project: Path,
    *,
    accept_all: bool,
    reject_all: bool,
    json_output: bool,
) -> list[tuple[FilePlan, bool, str | None]]:
    """Collect per-file consent, or die refusing to apply without it."""
    reviewable = [plan for plan in plans if plan.classification != IDENTICAL]
    if not reviewable:
        return []
    if json_output and not accept_all and not reject_all:
        # Agent mode has no prompt: applying without consent is exactly
        # what the per-file review exists to prevent.
        _fail(
            f"{len(reviewable)} file(s) need review; pass --accept-all or "
            "--reject-all, or run without --json to review interactively"
        )
    decisions: list[tuple[FilePlan, bool, str | None]] = []
    for plan in reviewable:
        if accept_all:
            decisions.append((plan, True, None))
        elif reject_all:
            decisions.append((plan, False, None))
        else:
            accepted, edited = _review_one(plan, project)
            decisions.append((plan, accepted, edited))
    return decisions


def _adopt_payload(
    rendered: Rendered,
    dst: Path,
    plans: list[FilePlan],
    decisions: list[tuple[FilePlan, bool, str | None]],
) -> dict[str, Any]:
    decided = {plan.path: (accepted, edited) for plan, accepted, edited in decisions}
    return {
        "src": rendered.src,
        "dst": str(dst),
        "answers_file": rendered.answers_relpath,
        "commit": rendered.commit,
        "files": [
            {
                "path": plan.path,
                "classification": plan.classification,
                "merger": plan.merger,
                "conflicted": plan.conflicted,
                "applied": decided.get(plan.path, (False, None))[0],
                "edited": decided.get(plan.path, (False, None))[1] is not None,
                "warnings": list(plan.warnings),
            }
            for plan in plans
        ],
    }


@app.command(epilog=_ADOPT_EPILOG)
def adopt(
    src: str = typer.Argument(..., help="Template source: path or URL"),
    dst: Path = typer.Argument(
        ..., help="Existing project directory to adopt the template into"
    ),
    answers: list[str] | None = typer.Option(
        None,
        "--answers",
        "-a",
        help="Question answer as QUESTION=ANSWER (repeatable)",
    ),
    defaults: bool = typer.Option(
        False,
        "--defaults",
        help="Use the template's defaults for un-answered questions (no prompts)",
    ),
    trust: bool = typer.Option(
        False, "--trust", help="Allow the template's jinja extensions (copier unsafe)"
    ),
    accept_all: bool = typer.Option(
        False, "--accept-all", help="Accept every proposal without prompting"
    ),
    reject_all: bool = typer.Option(
        False, "--reject-all", help="Reject every proposal without prompting"
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help=(
            "Emit a JSON result on stdout. Non-interactive by construction: "
            "unanswered questions take the template's defaults (implies "
            "--defaults), and files needing review are refused with exit 2 "
            "unless --accept-all or --reject-all is passed"
        ),
    ),
) -> None:
    """Adopt a template into an existing project (render → classify → review → stamp)."""
    if not dst.is_dir():
        _fail(f"adopt targets an existing project directory: {dst} is not one")
    if accept_all and reject_all:
        _fail("--accept-all and --reject-all are mutually exclusive")
    data: dict[str, Any] = _parse_answers(answers or [])
    with tempfile.TemporaryDirectory() as tmp:
        try:
            # --json is agent mode: the render must never prompt, so
            # unanswered questions take the template's defaults
            # (documented on the --json flag) rather than reaching
            # copier's prompt machinery.
            rendered = render(
                src,
                Path(tmp),
                data,
                defaults=defaults or json_output,
                trust=trust,
            )
        except Exception as error:  # the exit-code contract outranks traceback noise
            typer.secho(
                f"error: rendering {src} failed: {type(error).__name__}: {error}",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(EXIT_ERROR) from error
        try:
            plans = classify(rendered, dst)
            decisions = _review(
                plans,
                dst,
                accept_all=accept_all,
                reject_all=reject_all,
                json_output=json_output,
            )
            for plan, accepted, edited in decisions:
                if accepted:
                    apply(plan, dst, rendered=rendered, edited=edited)
            stamp(rendered, dst)
        except typer.Exit:  # consent refusals pass through as exit-2
            raise
        except (OSError, UnicodeDecodeError, MergeToolError) as error:
            _fail(f"{type(error).__name__}: {error}")
    conflicted = any(plan.classification == CONFLICT for plan in plans)
    if json_output:
        typer.echo(
            json.dumps(_adopt_payload(rendered, dst, plans, decisions), indent=2)
        )
    else:
        accepted_paths = {plan.path for plan, accepted, _ in decisions if accepted}
        for plan in plans:
            if plan.classification == IDENTICAL:
                mark = "identical"
            elif plan.path in accepted_paths:
                mark = "applied"
            else:
                mark = "skipped"
            typer.echo(f"{plan.classification}\t{plan.path}\t{mark}")
            for warning in plan.warnings:
                typer.secho(f"warning: {warning}", fg=typer.colors.YELLOW, err=True)
        typer.echo(f"stamped: {rendered.answers_relpath}")
    raise typer.Exit(EXIT_CONFLICTED if conflicted else EXIT_CLEAN)


if __name__ == "__main__":
    app()
