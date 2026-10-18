"""copier-cat CLI: a thin surface over the merge libraries (spec C5).

The engines are importable libraries; this CLI exposes the same
operations with stable commands, stable exit codes, and JSON output.
Adopt flows arrive with CC-3; the merge registry surface is here from
CC-1.

Exit codes: 0 merged clean, 1 merged with conflicts, 2 error.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import typer

from .merge import MergeToolError, default_registry

app = typer.Typer(
    help="copier-cat: template manager for copier.",
    no_args_is_help=True,
)

EXIT_CLEAN = 0
EXIT_CONFLICTED = 1
EXIT_ERROR = 2


def _read(path: Path, what: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
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


@app.command()
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
        None, "--output", help="Write merged text to this file instead of stdout"
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
        _write_text(result.text, output)
    raise typer.Exit(EXIT_CONFLICTED if result.conflicted else EXIT_CLEAN)


def _write_text(text: str, output: Path | None) -> None:
    if output is not None:
        try:
            output.write_text(text, encoding="utf-8")
        except OSError as error:
            typer.secho(
                f"error: cannot write {output}: {error}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(EXIT_ERROR) from error
        return
    sys.stdout.write(text if text.endswith("\n") else text + "\n")


@app.command()
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


if __name__ == "__main__":
    app()
