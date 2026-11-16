"""copier-cat CLI: a thin surface over the libraries (spec C5).

The engines are importable libraries; this CLI exposes the same
operations with stable commands, stable exit codes, and JSON output.
The merge registry surface is here from CCC-1; adopt from CCC-3.

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

import click
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
from .assemble import AssemblyError, load_catalog, questions_for, resolve_answers
from .assemble import assemble as assemble_project
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
            edited = click.edit(plan.proposed)
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
    """Adopt a template into an existing project.

    Render → classify → review → stamp.
    """
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


_ASSEMBLE_EPILOG = """\
Copier equivalent: `copier copy TEMPLATE DESTINATION` renders one
ordinary template. cc resolves that template from a named local stack,
previews and validates it in isolation, and writes only after approval.
Plain `copier update -a ANSWERS_FILE` continues the resulting project;
the disposable .copier-cat-stack.yml provenance is not required.

Examples:
  copier-cat assemble example-project --stack python --catalog catalog.yml
  copier-cat assemble example-project --stack python --dry-run --json
  copier-cat assemble example-project --stack python --yes

DESTINATION is the new project directory, not a stack name. --dry-run and
--json without --yes never write the destination. --yes approves only the
displayed new-destination write; it does not authorize source changes,
publication, telemetry, agent installation, or updates to an existing project.

Exit codes: 0 preview or approved assembly; 1 validation failure; 2 error.
"""

_STACK_EPILOG = """\
Copier equivalent: `copier copy` accepts a template source directly.
The local catalog gives that source a reusable identity, role, ref, and
answers without depending on another project's answers file.

Exit codes: 0 inspection; 2 unknown stack or catalog error.
"""


def _assembly_failure(error: AssemblyError, json_output: bool) -> None:
    if json_output:
        typer.echo(
            json.dumps({"status": "error", "stage": error.stage, "error": str(error)})
        )
    else:
        typer.secho(f"error: {error.stage}: {error}", fg=typer.colors.RED, err=True)
    raise typer.Exit(EXIT_CONFLICTED if error.stage == "validation" else EXIT_ERROR)


def _assembly_payload(plan: Any, *, wrote: bool) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": "assembled" if wrote else "preview",
        "stack": plan.stack.name,
        "destination": str(plan.destination),
        "answers": plan.answers,
        "answers_file": plan.rendered.answers_relpath,
        "native_update": plan.update_command,
        "provenance": ".copier-cat-stack.yml",
        "validation": list(plan.checks),
        "preview": str(plan.preview) if plan.retained else None,
        "preview_cleanup": f"rm -rf {plan.preview.parent}"
        if plan.retained
        else "automatic",
        "approved_write": str(plan.destination) if wrote else None,
    }


@app.command(epilog=_ASSEMBLE_EPILOG)
def assemble(
    destination: Path = typer.Argument(..., help="New project directory to create"),
    stack: str = typer.Option(..., "--stack", help="Named stack in the local catalog"),
    catalog: Path = typer.Option(
        Path("catalog.yml"), "--catalog", help="Local YAML template and stack catalog"
    ),
    answers: list[str] | None = typer.Option(
        None, "--answers", "-a", help="Answer as QUESTION=ANSWER (repeatable)"
    ),
    guided: bool = typer.Option(
        False, "--guided", help="Review human-readable template questions interactively"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Render and validate without writing the destination"
    ),
    retain_preview: bool = typer.Option(
        False, "--retain-preview", help="Retain the isolated preview and report cleanup"
    ),
    yes: bool = typer.Option(
        False, "--yes", help="Approve only the displayed new-destination write"
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Emit one structured preview or assembly result"
    ),
) -> None:
    """Assemble a real Python project from a named local stack."""
    try:
        selected = load_catalog(catalog, stack)
        overrides = _parse_answers(answers or [])
        interactive = not json_output and not dry_run and not yes
        resolved = resolve_answers(
            selected.members[0],
            overrides,
            interactive=interactive,
            guided=guided,
            input_fn=typer.prompt,
        )
        if interactive and not guided:
            typer.echo(f"Destination: {destination}")
            typer.echo(f"Stack: {stack}")
            if not typer.confirm("Render and validate this preview?", default=True):
                typer.echo("Cancelled; no destination written.")
                raise typer.Exit(EXIT_CLEAN)
        write = yes and not dry_run
        if yes and dry_run:
            raise AssemblyError("approval", "--dry-run cannot be combined with --yes")
        plan = assemble_project(
            selected,
            destination,
            resolved,
            write=write,
            retain_preview=retain_preview,
        )
        if interactive and not write:
            typer.echo("Validation passed; no destination written.")
            if typer.confirm(f"Create {destination}?", default=False):
                plan = assemble_project(
                    selected,
                    destination,
                    resolved,
                    write=True,
                    retain_preview=retain_preview,
                )
                write = True
            else:
                typer.echo("Cancelled; no destination written.")
        if json_output:
            typer.echo(json.dumps(_assembly_payload(plan, wrote=write), indent=2))
        else:
            typer.echo(
                f"{'Created' if write else 'Preview validated'}: {destination} "
                f"({stack}); {len(plan.checks)} checks passed"
            )
            if write:
                typer.echo(f"Next: cd {destination} && {plan.update_command}")
            if plan.retained:
                typer.echo(
                    f"Preview: {plan.preview}; cleanup: rm -rf {plan.preview.parent}"
                )
    except AssemblyError as error:
        _assembly_failure(error, json_output)


stack_app = typer.Typer(
    help="Inspect the local template and stack catalog.", epilog=_STACK_EPILOG
)
app.add_typer(stack_app, name="stack")


@stack_app.command("list")
def stack_list(catalog: Path = typer.Option(Path("catalog.yml"), "--catalog")) -> None:
    """List named stacks in the local catalog."""
    import yaml

    try:
        raw = yaml.safe_load(catalog.read_text(encoding="utf-8")) or {}
        for name in raw.get("stacks", {}):
            typer.echo(name)
    except (OSError, yaml.YAMLError, AttributeError) as error:
        _fail(f"catalog: {error}")


@stack_app.command("show")
def stack_show(
    name: str = typer.Argument(..., help="Named stack to inspect"),
    catalog: Path = typer.Option(Path("catalog.yml"), "--catalog"),
) -> None:
    """Show a stack's independent template source, role, ref, and answers."""
    try:
        selected = load_catalog(catalog, name)
        member = selected.members[0]
        typer.echo(f"Stack: {name}")
        typer.echo(f"Template: {member.name} ({member.role})")
        typer.echo(f"Source: {member.source}")
        typer.echo(f"Ref: {member.ref or 'default'}")
        for question in questions_for(member):
            default = (
                "required" if question.required else f"default: {question.default}"
            )
            typer.echo(f"  {question.label} ({question.name}; {default})")
            if question.help:
                typer.echo(f"    {question.help}")
    except AssemblyError as error:
        _assembly_failure(error, False)


if __name__ == "__main__":
    app()
