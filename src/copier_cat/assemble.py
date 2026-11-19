"""Assemble one independent Copier template from a named local stack.

Copier owns rendering and native updates. This module owns catalog resolution,
answer planning, isolated previews, validation, and narrowly scoped writes.
Multi-template structured composition belongs to CCC-25, not this slice.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import copier
import yaml

from .adopt import Rendered, render
from .merge import default_registry

PROVENANCE_FILE = ".copier-cat-stack.yml"


class AssemblyError(Exception):
    """A readable assembly failure with a stable stage for CLI reporting."""

    def __init__(self, stage: str, message: str) -> None:
        super().__init__(message)
        self.stage = stage


@dataclass(frozen=True)
class Member:
    """One independently renderable template in a stack recipe."""

    name: str
    role: str
    source: str
    ref: str | None = None
    answers: dict[str, Any] = field(default_factory=dict)
    trust: bool = False


@dataclass(frozen=True)
class Question:
    """Human-readable template question metadata, not a raw JSON mapping."""

    name: str
    label: str
    help: str
    kind: str
    default: Any = None
    required: bool = False
    choices: tuple[Any, ...] = ()


@dataclass(frozen=True)
class Stack:
    """The initial local catalog contract: named templates and stacks."""

    name: str
    members: tuple[Member, ...]


@dataclass(frozen=True)
class AssemblyPlan:
    """A validated, inspectable preview; not approval to write."""

    stack: Stack
    destination: Path
    preview: Path
    rendered: Rendered
    answers: dict[str, Any]
    update_command: str
    checks: tuple[str, ...]
    retained: bool


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AssemblyError("catalog", f"{label} must be a mapping")
    return value


def load_catalog(path: Path, stack_name: str) -> Stack:
    """Load one named stack; no other project's answers file is consulted."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError as error:
        raise AssemblyError(
            "catalog", f"cannot read catalog {path}: {error}"
        ) from error
    except yaml.YAMLError as error:
        raise AssemblyError("catalog", f"invalid YAML in {path}: {error}") from error
    root = _mapping(raw, "catalog")
    templates = _mapping(root.get("templates", {}), "templates")
    stacks = _mapping(root.get("stacks", {}), "stacks")
    entry = _mapping(stacks.get(stack_name, {}), f"stack {stack_name!r}")
    names = entry.get("templates")
    if (
        not isinstance(names, list)
        or not names
        or not all(isinstance(name, str) for name in names)
    ):
        raise AssemblyError(
            "catalog", f"stack {stack_name!r} must name at least one template"
        )
    if len(names) != 1:
        raise AssemblyError(
            "catalog",
            "this Python-only slice accepts one template; multi-template composition "
            "is tracked separately",
        )
    members: list[Member] = []
    for name in names:
        if name not in templates:
            raise AssemblyError("catalog", f"unknown template {name!r}")
        data = _mapping(templates[name], f"template {name!r}")
        source = data.get("source")
        if not isinstance(source, str) or not source:
            raise AssemblyError("catalog", f"template {name!r} needs a source")
        ref = data.get("ref")
        if ref is not None and not isinstance(ref, str):
            raise AssemblyError("catalog", f"template {name!r} ref must be a string")
        answers = _mapping(data.get("answers", {}), f"template {name!r} answers")
        members.append(
            Member(
                name=name,
                role=str(data.get("role", "base")),
                source=source,
                ref=ref,
                answers=answers,
                trust=bool(data.get("trust", False)),
            )
        )
    return Stack(name=stack_name, members=tuple(members))


def questions_for(member: Member) -> tuple[Question, ...]:
    """Read questions from the template Copier itself resolves."""
    try:
        with contextlib.redirect_stdout(os.sys.stderr):
            template = copier.Template(url=member.source, ref=member.ref)
            question_data = template.questions_data
        result = []
        for name, data in question_data.items():
            data = _mapping(data, f"question {name!r}")
            label = str(data.get("label", name.replace("_", " ").capitalize()))
            result.append(
                Question(
                    name=name,
                    label=label,
                    help=str(data.get("help", "")),
                    kind=str(data.get("type", "str")),
                    default=data.get("default"),
                    required="default" not in data,
                    choices=tuple(data.get("choices", ())),
                )
            )
        return tuple(result)
    except Exception as error:
        raise AssemblyError(
            "discovery", f"cannot inspect template {member.source}: {error}"
        ) from error


def resolve_answers(
    member: Member,
    overrides: dict[str, Any],
    *,
    interactive: bool,
    guided: bool,
    input_fn: Any,
) -> dict[str, Any]:
    """Resolve explicit, stack, and template answers with focused prompts."""
    metadata = questions_for(member)
    known = {question.name for question in metadata}
    unknown = sorted(set(overrides) - known)
    if unknown:
        raise AssemblyError(
            "answers", f"unknown answer(s) for {member.name}: {', '.join(unknown)}"
        )
    answers = dict(member.answers)
    answers.update(overrides)
    missing = [
        question
        for question in metadata
        if question.required and question.name not in answers
    ]
    if missing and not interactive:
        raise AssemblyError(
            "answers",
            "missing required answer(s): "
            + ", ".join(question.name for question in missing)
            + "; supply --answers QUESTION=ANSWER",
        )
    if interactive:
        for question in metadata:
            if question.name in answers and not guided:
                continue
            default = answers.get(question.name, question.default)
            prompt = question.label
            if question.help:
                prompt += f" — {question.help}"
            if question.choices:
                prompt += f" ({', '.join(map(str, question.choices))})"
            value = input_fn(prompt, default=default if default is not None else None)
            if value == "" and default is not None:
                value = default
            if value == "" and question.required:
                raise AssemblyError("answers", f"{question.name} is required")
            if value != "":
                answers[question.name] = value
    return answers


def _assert_new_destination(destination: Path) -> None:
    if destination.exists():
        raise AssemblyError(
            "approval",
            f"destination already exists: {destination}; refusing to update it",
        )
    if not destination.parent.is_dir():
        raise AssemblyError(
            "approval", f"destination parent is not a directory: {destination.parent}"
        )


def _run_project_tests(destination: Path, environment: Path) -> bool:
    """Run generated-project tests without adding files to its update baseline."""
    config = destination / "pyproject.toml"
    tests = destination / "tests"
    if not tests.is_dir() or not any(tests.rglob("test_*.py")):
        return False
    if not config.is_file():
        raise AssemblyError(
            "validation", "generated tests need a declared pyproject.toml runner"
        )
    uv = shutil.which("uv")
    if uv is None:
        raise AssemblyError("validation", "generated project needs uv for its tests")
    env = os.environ.copy()
    env["UV_PROJECT_ENVIRONMENT"] = str(environment.resolve())
    try:
        result = subprocess.run(
            [uv, "run", "pytest", "tests/", "-x", "-q"],
            cwd=destination,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        raise AssemblyError(
            "validation", f"cannot run generated tests: {error}"
        ) from error
    if result.returncode:
        detail = (result.stdout + result.stderr).strip().splitlines()
        raise AssemblyError(
            "validation",
            "generated project tests failed: " + "\n".join(detail[-12:]),
        )
    return True


def _validate(
    destination: Path, rendered: Rendered, run_tests: bool, environment: Path
) -> tuple[str, ...]:
    answers_file = destination / rendered.answers_relpath
    if not answers_file.is_file():
        raise AssemblyError(
            "validation", f"missing native answers file: {answers_file}"
        )
    record = yaml.safe_load(answers_file.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise AssemblyError("validation", "native answers file is not a mapping")
    if record.get("_src_path") != rendered.src:
        raise AssemblyError(
            "validation", "native answers source does not match the catalog"
        )
    provenance = destination / PROVENANCE_FILE
    if not provenance.is_file():
        raise AssemblyError(
            "validation", f"missing disposable provenance: {provenance}"
        )
    if list(destination.rglob("*.rej")):
        raise AssemblyError("validation", "Copier left rejected update hunks (.rej)")
    for path in destination.rglob("*.toml"):
        result = default_registry().merge(
            path.relative_to(destination).as_posix(),
            "",
            path.read_text(encoding="utf-8"),
            path.read_text(encoding="utf-8"),
        )
        if result.merger != "toml":
            raise AssemblyError("validation", f"invalid TOML: {path}")
    tests_ran = _run_project_tests(destination, environment) if run_tests else False
    return (
        "rendered output exists",
        "native answers source verified",
        "disposable provenance present",
        "no rejected Copier hunks",
        "TOML parse validation passed",
        "generated project tests passed"
        if tests_ran
        else "no generated test suite declared",
    )


def _write_provenance(destination: Path, stack: Stack, answers: dict[str, Any]) -> None:
    member = stack.members[0]
    record = {
        "stack": stack.name,
        "templates": [
            {
                "name": member.name,
                "role": member.role,
                "source": member.source,
                "ref": member.ref,
                "answers": answers,
            }
        ],
    }
    (destination / PROVENANCE_FILE).write_text(
        "# Disposable assembly evidence; native Copier updates do not depend on "
        "this file.\n" + yaml.safe_dump(record, sort_keys=False),
        encoding="utf-8",
    )


def assemble(
    stack: Stack,
    destination: Path,
    answers: dict[str, Any],
    *,
    write: bool,
    retain_preview: bool,
    run_tests: bool = True,
) -> AssemblyPlan:
    """Render and validate in isolation; copy only after explicit write approval."""
    _assert_new_destination(destination)
    member = stack.members[0]
    temporary = tempfile.TemporaryDirectory(prefix="copier-cat-assemble-")
    preview = Path(temporary.name).resolve()
    try:
        try:
            with contextlib.redirect_stdout(os.sys.stderr):
                rendered = render(
                    member.source,
                    preview / "render",
                    answers,
                    defaults=True,
                    trust=member.trust,
                    vcs_ref=member.ref or "HEAD",
                )
            # The selected ref belongs to this recipe, not another project's
            # answers file. Local templates default to their current HEAD.
            # Copier's run_copy already wrote the native answers file; do not
            # re-stamp it with a different format, or native update would
            # rewrite it and leave the project dirty.
            _write_provenance(preview / "render", stack, answers)
            checks = _validate(
                preview / "render", rendered, run_tests, preview / "test-env"
            )
            # Copier's native update contract requires a Git-tracked
            # subproject. Initialize the generated project in isolation;
            # no commit or remote operation is performed by cc.
            subprocess.run(
                ["git", "init", "-q", str((preview / "render").resolve())],
                check=True,
                capture_output=True,
                text=True,
            )
            # The validation environment lives outside the generated project,
            # preserving a clean baseline for independent native Copier updates.
            subprocess.run(
                ["git", "add", "-A"],
                cwd=preview / "render",
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=copier-cat preview",
                    "-c",
                    "user.email=preview@localhost.invalid",
                    "commit",
                    "-qm",
                    "Initial generated project",
                ],
                cwd=preview / "render",
                check=True,
                capture_output=True,
                text=True,
            )
            # Prove the recorded native update path before reporting it.
            with contextlib.redirect_stdout(os.sys.stderr):
                update = copier.run_update(
                    preview / "render",
                    defaults=True,
                    quiet=True,
                    overwrite=True,
                    skip_tasks=True,
                    answers_file=rendered.answers_relpath,
                    # Validate the native update machinery without moving a
                    # pinned assembly to the template's latest version.
                    vcs_ref=member.ref,
                )
            if update.answers_relpath != Path(rendered.answers_relpath):
                raise AssemblyError(
                    "validation", "native update used the wrong answers file"
                )
            checks += ("native Copier update succeeded",)
        except AssemblyError:
            raise
        except Exception as error:
            raise AssemblyError("render", f"Copier assembly failed: {error}") from error

        final_preview = preview / "render"
        retained_path: Path | None = None
        if retain_preview:
            retained_path = (
                Path(tempfile.mkdtemp(prefix="copier-cat-preview-")).resolve()
                / destination.name
            )
            shutil.copytree(final_preview, retained_path)
            final_preview = retained_path
        if write:
            shutil.copytree(final_preview, destination)
        return AssemblyPlan(
            stack=stack,
            destination=destination,
            preview=final_preview,
            rendered=rendered,
            answers=answers,
            update_command=f"copier update --defaults -a {rendered.answers_relpath}",
            checks=checks,
            retained=retain_preview,
        )
    finally:
        temporary.cleanup()
