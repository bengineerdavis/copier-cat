"""THROWAWAY prototype for copier-cat assembly UX.

Help is a first-class human/agent interface. Assembly syntax is:
  ccc assemble DESTINATION --stack STACK

DESTINATION is the new project directory, not a template or stack name.

Examples:
  # Read-only plan; no writes or --yes required.
  python3 prototype.py assemble example-project --stack example-stack --json

  # Interactive assembly; approve the displayed destination explicitly.
  python3 prototype.py assemble example-project --stack example-stack

  # Explicit approval to write only ./example-project.
  python3 prototype.py assemble example-project --stack example-stack --yes

  # Explicit guided review of answers and composition.
  python3 prototype.py assemble example-project --stack example-stack --guided

  # Inspect and modify a stack, not a project.
  python3 prototype.py stack show example-stack -v
  python3 prototype.py --stack example-stack use example-overlay -v

`ccc` is the accepted local alias for the real product; /usr/bin/cc is the C compiler.
All sources, paths, answers, validation results, and writes are simulated.
CCC_CONFIG_FILE selects a review-only config marker. After explicit consent,
init creates that marker so later invocations know setup completed. Its content
is a comment only; no preferences are parsed. Without it, the real default is
untouched. Use `uv run --with prompt-toolkit --with rapidfuzz` for fuzzy selection.
"""

from __future__ import annotations

import argparse
import difflib
import json
import logging
import os
import sys
from pathlib import Path
from dataclasses import asdict, dataclass, field

from help_contract import ASSEMBLE_HELP, HELP_SCHEMA, SCHEMA, TOP_LEVEL_HELP

log = logging.getLogger("prototype")
COMMANDS = ("assemble", "stack", "use", "adopt", "contribute", "catalog", "init")
STACKS = ("agentic-python", "python", "agentic")
DEFAULT_CONFIG_PATH = "~/.config/copier-cat/config.yml"
BUILTIN_DEFAULTS = {
    "output": "default",
    "selector": "fuzzy",
    "preview_cleanup": True,
    "default_stack": None,
}


@dataclass
class Result:
    operation: str
    status: str = "ok"
    project: str | None = None
    stack: str | None = None
    destination: str | None = None
    approved: bool = False
    preview: str | None = None
    preview_retained: bool = False
    preview_cleaned: bool = False
    stages: list[str] = field(default_factory=list)
    reviews: list[str] = field(default_factory=list)
    answers: dict[str, str | bool | None] = field(default_factory=dict)
    validations: list[str] = field(default_factory=list)
    evidence: str | None = None
    saved_stack: str | None = None
    synthetic: bool = True


def emit(result: Result, args: argparse.Namespace) -> None:
    if args.json:
        print(json.dumps(asdict(result), separators=(",", ":")))
        return
    if result.operation == "assemble":
        if result.status == "cancelled":
            print("Cancelled. No writes.")
            return
        if result.status == "preview":
            print(f"Previewed plan for ./{result.project}")
            print("  no project writes; explicit assembly approval required")
        else:
            print(f"{'Created' if result.approved else 'Previewed'} {result.destination}")
        print(f"  {result.stack} · {'guided' if result.reviews else 'all'}")
        if result.status != "preview":
            print(f"  validated · preview {'retained' if result.preview_retained else 'cleaned'}")
        if result.saved_stack:
            print(f"  saved stack: {result.saved_stack}")
        if args.verbose:
            print("  templates: python [base] + agentic [overlay]")
            print(f"  answers: {result.answers}")
            print("  composition: mise.toml [TOML], .gitignore [patterns]")
            print(f"  evidence: {result.evidence}")
            print("  update: copier update -a <template-answers-file>")
    elif result.operation.startswith("stack"):
        verb = "Updated" if result.operation == "stack-use" else "Saved"
        if result.operation == "stack-show":
            print(f"Stack {result.stack}")
        else:
            print(f"{verb} stack {result.stack} (simulated)")
        if args.verbose:
            print("  python [base] + agentic [overlay]")
            if result.stages:
                print(f"  changes: {', '.join(result.stages)}")
            print(f"  next: ccc assemble example-project --stack {result.stack} --dry-run")


def parser(name: str) -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog=f"ccc {name}",
        description=ASSEMBLE_HELP if name == "assemble" else f"Prototype {name} operation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    result.add_argument(
        "args",
        metavar="DESTINATION" if name == "assemble" else "ARGS",
        nargs=None if name == "assemble" else "*",
        help=(
            "New project directory, for example example-project. "
            "This is not a stack or template name."
            if name == "assemble"
            else "Command-specific operands; see command examples."
        ),
    )
    result.add_argument("-v", "--verbose", action="store_true")
    result.add_argument("--debug", action="store_true")
    result.add_argument("--json", action="store_true")
    return result


def reject(result: Result, args: argparse.Namespace, status: str) -> int:
    result.status = status
    result.destination = None
    result.approved = False
    result.stages = []
    result.reviews = []
    result.answers = {}
    emit(result, args)
    return 1


def review(question: str, allow_edit: bool = False) -> str:
    """Return a normalized decision; re-prompt on unrecognized text."""
    suffix = " [Y/n/edit]" if allow_edit else " [Y/n]"
    while True:
        print(question + suffix + " ", end="", file=sys.stderr)
        try:
            answer = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("Cancelled. No writes.", file=sys.stderr)
            return "n"
        if not answer:
            return "y"
        if answer in ("y", "yes", "n", "no"):
            return "yes" if answer in ("y", "yes") else "n"
        if allow_edit and answer in ("e", "edit"):
            return "e"
        print("Please answer y/yes, n/no, or press Enter for the default.", file=sys.stderr)


def assemble(argv: list[str], selected_stack: str | None = None, source: str | None = None) -> int:
    args_parser = parser("assemble")
    args_parser.add_argument("--stack", default=selected_stack)
    args_parser.add_argument("--yes", action="store_true")
    args_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the plan without creating project files; no --yes required.",
    )
    args_parser.add_argument("--guided", "--staged", dest="staged", action="store_true")
    args_parser.add_argument("--keep-preview", action="store_true")
    args_parser.add_argument("--save", metavar="NAME")
    args = args_parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.WARNING,
        format="debug: %(message)s",
        stream=sys.stderr,
    )
    if isinstance(args.args, str):
        project = args.args
    elif args.args:
        project = args.args[0]
    else:
        args_parser.error("DESTINATION is required, for example example-project")
    if not args.stack:
        if args.yes or args.json:
            args_parser.error("stack required; use --stack STACK or interactive stack selection")
        args.stack = choose_stack()
        if not args.stack:
            print("No stack selected. No writes.", file=sys.stderr)
            return 2
    if args.stack.startswith("new-stack-from:"):
        template_source = args.stack.removeprefix("new-stack-from:")
        if review(f"Preview new stack from {template_source}; approve download for isolated inspection?") != "yes":
            print("Cancelled. No writes.", file=sys.stderr)
            return 1
        if review("Save the reviewed stack as agentic-python for this prototype?") != "yes":
            print("Cancelled. No writes.", file=sys.stderr)
            return 1
        args.stack = "agentic-python"
    if source and review(f"Add {source} to {args.stack} for isolated inspection?") != "yes":
        print("Cancelled. No writes.", file=sys.stderr)
        return 1
    answers: dict[str, str | bool | None] = {
        "project_name": project,
        "python_version": "3.12",
        "include_backlog": True,
        "include_lore": True,
    }
    result = Result(
        operation="assemble",
        project=project,
        stack=args.stack,
        destination=f"./{project}",
        preview="/synthetic/cc-preview-abc123",
        preview_retained=args.keep_preview,
        answers=answers,
        evidence=f"./{project}/.copier-cat-stack.yml",
    )
    log.debug("resolved stack=%s templates=python,agentic", args.stack)
    log.debug("isolated preview=%s", result.preview)

    if args.dry_run:
        result.status = "preview"
        result.destination = None
        result.approved = False
        emit(result, args)
        return 0
    if args.json and not args.yes:
        result.status = "preview"
        result.destination = None
        emit(result, args)
        return 0

    if args.staged:
        stages = ("resolve", "answers", "compose", "assemble")
        result.stages = ["resolve", "answers", "compose", "validate", "assemble"]
        result.reviews.append("validate:automatic")
        reviews = (
            ("resolve", "1/4 Use stack agentic-python: python [base] + agentic [overlay]?", False),
            ("answers", "2/4 Use these answers? " + json.dumps(answers), True),
            ("compose", "3/4 Review composition: mise.toml [TOML] + .gitignore [patterns]. Continue?", False),
            ("assemble", f"4/4 Create ./{project}?", False),
        )
        print("Validation will run automatically: structure, attribution, project tests [simulated].", file=sys.stderr)
        for stage, question, editable in reviews:
            if args.json and args.yes:
                result.reviews.append(stage)
                continue
            answer = review(question, allow_edit=editable)
            if answer == "n":
                return reject(result, args, "cancelled")
            if editable and answer in ("e", "edit"):
                change = review("Enter key=value").split("=", 1)
                if len(change) != 2:
                    return reject(result, args, "invalid-answer")
                answers[change[0]] = change[1]
                result.reviews.append(f"{stage}:edited")
            else:
                result.reviews.append(stage)
    else:
        result.stages = ["all"]
        if not args.yes and review(f"Create ./{project} from {args.stack}?") == "n":
            return reject(result, args, "cancelled")

    result.approved = True
    result.validations = ["structure", "attribution", "project-tests"]
    result.preview_cleaned = not args.keep_preview
    result.saved_stack = args.save
    log.debug("synthetic validation only; Copier and project tests were not run")
    emit(result, args)
    return 0


def stack_command(argv: list[str], selected_stack: str | None = None) -> int:
    args_parser = parser("stack")
    args_parser.add_argument("--from", dest="templates", nargs="+", default=[])
    args_parser.add_argument("--set", dest="settings", action="append", default=[])
    args = args_parser.parse_args(argv)
    if not args.args or args.args[0] not in ("new", "edit", "show", "list"):
        args_parser.error("expected new, edit, show, or list and a stack name")
    action = args.args[0]
    if action == "list":
        for name in STACKS:
            print(name)
        return 0
    name = args.args[1] if len(args.args) > 1 else selected_stack
    if not name:
        args_parser.error("stack name required")
    result = Result(
        operation=f"stack-{action}",
        stack=name,
        stages=args.templates or args.settings,
        saved_stack=name if action != "show" else None,
    )
    log.debug("stack operation=%s settings=%s", action, args.settings)
    emit(result, args)
    return 0


def use_template(argv: list[str], selected_stack: str | None) -> int:
    args_parser = parser("use")
    args = args_parser.parse_args(argv)
    if not selected_stack or not args.args:
        args_parser.error("usage: --stack STACK use TEMPLATE|SOURCE")
    template = args.args[0]
    result = Result(
        operation="stack-use",
        stack=selected_stack,
        stages=[f"add:{template}"],
        saved_stack=selected_stack,
    )
    log.debug("resolve template=%s through catalog or Copier-compatible source", template)
    emit(result, args)
    return 0


def typo(token: str) -> int:
    if token in ("recipe", "recipie"):
        suggestion = "stack"
    else:
        matches = difflib.get_close_matches(token, COMMANDS + STACKS, n=1, cutoff=0.7)
        suggestion = matches[0] if matches else None
    if suggestion:
        print(f"Unknown command {token!r}. Did you mean {suggestion!r}?", file=sys.stderr)
        print(f"No writes. To use the literal name, run: ccc assemble {token}", file=sys.stderr)
        return 2
    return 0


def split_global(argv: list[str]) -> tuple[str | None, list[str], str | None, dict[str, str | bool | None], str | None]:
    """Extract global options without mutating the caller's arguments."""
    selected_stack = None
    source = None
    config_path = None
    config = dict(BUILTIN_DEFAULTS)
    remaining = []
    index = 0
    while index < len(argv):
        if argv[index] in ("--stack", "--source", "--config"):
            option = argv[index]
            if index + 1 >= len(argv):
                print(f"{option} requires a value", file=sys.stderr)
                raise SystemExit(2)
            if option == "--stack":
                selected_stack = argv[index + 1]
            elif option == "--source":
                source = argv[index + 1]
            else:
                config_path = argv[index + 1]
            index += 2
        else:
            remaining.append(argv[index])
            index += 1
    if config_path:
        config["config_path"] = config_path
    return selected_stack, remaining, source, config, config_path


def init_command(
    argv: list[str], config: dict[str, str | bool | None], explicit: bool = True
) -> int:
    # Simulation only: preferences are not parsed. Explicit init may create the
    # selected marker; its content is a comment, not a real user configuration.
    args = parser("init").parse_args(argv)
    destination = os.environ.get("CCC_CONFIG_FILE") or str(
        config.get("config_path", DEFAULT_CONFIG_PATH)
    )
    result = Result(
        operation="init",
        evidence=destination,
        answers={"selector": config["selector"], "default_stack": None},
    )
    if args.json:
        if explicit:
            result.status = "approval-required"
            result.destination = None
            emit(result, args)
            return 1
        # A missing config never makes automation interactive.
        return 0
    if review(f"Write initial config marker to {result.evidence}? [simulated]") != "yes":
        if not explicit:
            print("Setup skipped; built-in defaults active. No config written.", file=sys.stderr)
            return 0  # Built-in defaults keep the original command usable.
        result.status = "cancelled"
        result.destination = None
        if args.json:
            emit(result, args)
        else:
            print("Cancelled. No writes.")
        return 1
    if not os.environ.get("CCC_CONFIG_FILE"):
        print("Dry run: set CCC_CONFIG_FILE to a review path to persist the marker.")
        print(f"Would initialize: {destination}")
    else:
        marker = Path(destination).expanduser()
        if not marker.is_absolute():
            print("Use CCC_CONFIG_FILE with an absolute path for this simulation.", file=sys.stderr)
            return 2
        if marker.exists():
            print(f"Existing marker preserved: {marker}")
        else:
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(
                "# Prototype review marker only. No preferences are stored.\n",
                encoding="utf-8",
            )
        print(f"Initialized review marker: {marker}")
        print("  no preferences saved; no default stack selected")
    result.approved = True
    result.reviews = ["confirm-marker"]
    if args.json:
        emit(result, args)
    else:
        print(f"Initialized review marker: {marker}")
        print("  no preferences saved; no default stack selected")
    return 0


def choose_stack() -> str | None:
    """Interactive fuzzy selector; non-TTY input gets a simple numbered menu."""
    print("No stack selected. Search stacks or enter a Copier template source.", file=sys.stderr)
    for index, name in enumerate(STACKS, start=1):
        print(f"  {index}. {name}", file=sys.stderr)
    if sys.stdin.isatty() and sys.stderr.isatty():
        try:
            from prompt_toolkit import PromptSession
            from prompt_toolkit.completion import FuzzyCompleter, WordCompleter

            query = PromptSession().prompt(
                "stack> ",
                completer=FuzzyCompleter(WordCompleter(STACKS, sentence=True)),
                complete_while_typing=True,
            ).strip()
        except (EOFError, KeyboardInterrupt):
            return None
    else:
        print("stack> ", end="", file=sys.stderr)
        try:
            query = input().strip()
        except EOFError:
            return None
    if not query:
        return None
    if query.isdigit() and 0 < int(query) <= len(STACKS):
        return STACKS[int(query) - 1]
    if query in STACKS:
        return query
    if any(marker in query for marker in ("/", ":", ".git")):
        # A source is offered for review only; no clone/fetch occurs in this prototype.
        return f"new-stack-from:{query}"
    try:
        from rapidfuzz import fuzz

        scored = sorted(
            ((fuzz.WRatio(query.lower(), name), name) for name in STACKS),
            reverse=True,
        )
        best = scored[0][0]
        matches = [name for score, name in scored if score >= max(50, best - 10)]
    except ImportError:
        matches = difflib.get_close_matches(query, STACKS, n=3, cutoff=0.5)
    if len(matches) == 1:
        selected = matches[0]
        if review(f"Use stack {selected}?") == "yes":
            return selected
        return None
    if matches:
        print("Matches: " + ", ".join(matches), file=sys.stderr)
    return None


def main() -> int:
    original_argv = sys.argv[1:]
    selected_stack, argv, source, config, config_path = split_global(original_argv)
    config_marker = os.environ.get("CCC_CONFIG_FILE")
    if config_marker:
        config["config_path"] = config_marker
    config_exists = bool(config_marker and os.path.isfile(config_marker))
    if not argv:
        print(__doc__)
        return 2
    operation, arguments = argv[0], argv[1:]
    if operation in ("--help", "-h", "--version"):
        print(TOP_LEVEL_HELP if operation != "--version" else "ccc assembly UX prototype 0.1.0")
        return 0
    if operation == "help" and "--json" in arguments:
        print(json.dumps(HELP_SCHEMA, separators=(",", ":")))
        return 0
    if "--help" in arguments and "--json" in arguments:
        print(json.dumps(SCHEMA, separators=(",", ":")))
        return 0
    if operation == "help":
        print(TOP_LEVEL_HELP)
        return 0
    if operation == "init":
        return init_command(arguments, config)
    noninteractive = (
        "--json" in original_argv
        or "--yes" in original_argv
        or not sys.stdin.isatty()
        or not sys.stderr.isatty()
    )
    if not config_exists and not noninteractive:
        status = init_command([], config, explicit=False)
        if status:
            return status
    if operation == "stack":
        return stack_command(arguments, selected_stack)
    if operation == "use":
        return use_template(arguments, selected_stack)
    if operation == "assemble":
        return assemble(arguments, selected_stack, source)
    if operation in STACKS:
        if not arguments or arguments[0].startswith("-"):
            print(f"Stack {operation!r} needs a project name.", file=sys.stderr)
            return 2
        return assemble(arguments, operation, source)
    typo_status = typo(operation)
    if typo_status:
        return typo_status
    return assemble([operation] + arguments, selected_stack, source)


if __name__ == "__main__":
    raise SystemExit(main())
