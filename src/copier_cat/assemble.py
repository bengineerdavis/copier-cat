"""Assemble independent Copier templates from a named local stack.

Copier owns rendering and native per-template updates. This module owns catalog
resolution, answer planning, isolated previews, structured composition,
validation, and narrowly scoped writes.
"""

from __future__ import annotations

import contextlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

import copier
import yaml

from .adopt import Rendered, render
from .merge import TomlMerger


def _safe_path_component(value: str, label: str) -> str:
    """Reject identifiers that cannot safely name one directory entry."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) or value in {".", ".."}:
        raise AssemblyError(
            "catalog", f"{label} is not a safe path component: {value!r}"
        )
    return value


def stack_artifact_name(stack_name: str) -> str:
    """Return one safe project-local artifact name, or reject the stack name."""
    return f"{_safe_path_component(stack_name, 'stack name')}.stack.yml"


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
    capabilities: tuple[str, ...] = ()


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
    answers: dict[str, dict[str, Any]]
    update_command: str
    update_commands: tuple[str, ...]
    checks: tuple[str, ...]
    retained: bool


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AssemblyError("catalog", f"{label} must be a mapping")
    return value


def _is_git_template(source: str) -> bool:
    """Recognize local Git checkouts, including linked-worktree .git files."""
    path = Path(source)
    return path.is_dir() and (path / ".git").exists()


def _git_head(source: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _native_answers_source(source: Path | None, rendered: Rendered) -> Rendered:
    """Record a resolvable Git source and committed baseline for native update."""
    if source is None or rendered.commit is None:
        return rendered
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return replace(
        rendered,
        src=f"git+{source.resolve()}",
        commit=_git_head(source)[:7] if dirty else rendered.commit,
    )


def _validation_source(
    member: Member, rendered: Rendered, source: Path, preview: Path
) -> tuple[str, str | None]:
    """Use a committed copy when a no-ref local template is dirty.

    Copier's dirty update mode can record a synthetic ref that its next clone
    cannot resolve. The user's source is never modified; only this disposable
    validation project uses the clean source and its real committed baseline.
    """
    local = _local_git_source(member.source)
    if local is None or member.ref is not None or rendered.commit is None:
        return rendered.src, member.ref or rendered.commit
    if not subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=local,
        check=True,
        capture_output=True,
        text=True,
    ).stdout:
        return rendered.src, member.ref or rendered.commit
    clean = preview / f"validation-source-{member.name}"
    subprocess.run(
        ["git", "clone", "-q", str(local), str(clean)],
        check=True,
        capture_output=True,
        text=True,
    )
    return f"git+{clean.resolve()}", _git_head(local)[:7]


def _local_git_source(source: str) -> Path | None:
    """Recover the original local checkout from Copier's Git URL form."""
    if source.startswith("git+"):
        path = Path(source[4:])
        if _is_git_template(str(path)):
            return path
    return None


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
    if len(set(names)) != len(names):
        raise AssemblyError("catalog", "a stack cannot repeat a template")
    for name in names:
        _safe_path_component(name, "template ID")
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
        if ref is not None and Path(source).is_dir() and not _is_git_template(source):
            raise AssemblyError(
                "catalog",
                f"template {name!r} selects a ref but is not a Git repository",
            )
        answers = _mapping(data.get("answers", {}), f"template {name!r} answers")
        capabilities = data.get("capabilities", [])
        if not isinstance(capabilities, list) or not all(
            isinstance(capability, str) for capability in capabilities
        ):
            raise AssemblyError(
                "catalog", f"template {name!r} capabilities must be strings"
            )
        if role := str(data.get("role", "base")):
            if role == "base" and any(member.role == "base" for member in members):
                raise AssemblyError("catalog", "a stack may have only one base")
        if role == "overlay" and not capabilities:
            raise AssemblyError(
                "catalog",
                f"overlay {name!r} must declare capabilities, not a Python dependency",
            )
        members.append(
            Member(
                name=name,
                role=role,
                source=(
                    f"git+{Path(source).resolve()}"
                    if _is_git_template(source)
                    else source
                ),
                ref=ref,
                answers=answers,
                trust=bool(data.get("trust", False)),
                capabilities=tuple(capabilities),
            )
        )
    return Stack(name=stack_name, members=tuple(members))


def resolve_stack_answers(
    stack: Stack,
    overrides: dict[str, Any],
    *,
    interactive: bool,
    guided: bool,
    input_fn: Any,
) -> dict[str, dict[str, Any]]:
    """Resolve each template's answers; multi-template overrides are member-scoped."""
    questions = {member.name: questions_for(member) for member in stack.members}
    resolved: dict[str, dict[str, Any]] = {}
    for member in stack.members:
        member_overrides = dict(overrides)
        if len(stack.members) > 1:
            member_overrides = {}
            for key, value in overrides.items():
                member_name, separator, question = key.partition(".")
                if separator and member_name == member.name:
                    member_overrides[question] = value
                elif not separator and any(
                    question.name == key for question in questions[member.name]
                ):
                    member_overrides[key] = value
        resolved[member.name] = resolve_answers(
            member,
            member_overrides,
            interactive=interactive,
            guided=guided,
            input_fn=input_fn,
        )
    if len(stack.members) > 1:
        known = {
            f"{member.name}.{question.name}"
            for member in stack.members
            for question in questions[member.name]
        }
        known.update(
            question.name
            for member_questions in questions.values()
            for question in member_questions
        )
        unknown = sorted(set(overrides) - known)
        if unknown:
            raise AssemblyError("answers", f"unknown answer(s): {', '.join(unknown)}")
    return resolved


def questions_for(member: Member) -> tuple[Question, ...]:
    """Read questions from the template Copier itself resolves."""
    try:
        with contextlib.redirect_stdout(sys.stderr):
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


def _member_preview_path(preview: Path, prefix: str, member: Member) -> Path:
    """Contain every generated member path inside the isolated preview."""
    path = (preview / f"{prefix}-{member.name}").resolve()
    try:
        path.relative_to(preview)
    except ValueError as error:
        raise AssemblyError(
            "catalog", f"template ID escapes the preview: {member.name!r}"
        ) from error
    return path


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
    destination: Path,
    rendered: Rendered,
    run_tests: bool,
    environment: Path,
    stack_artifact: Path | None = None,
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
            "validation", "native answers source does not match the rendered template"
        )
    if stack_artifact is not None and not stack_artifact.is_file():
        raise AssemblyError(
            "validation", f"missing disposable stack artifact: {stack_artifact}"
        )
    if list(destination.rglob("*.rej")):
        raise AssemblyError("validation", "Copier left rejected update hunks (.rej)")
    for path in destination.rglob("*.toml"):
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as error:
            raise AssemblyError("validation", f"invalid TOML: {path}") from error
    tests_ran = _run_project_tests(destination, environment) if run_tests else False
    return (
        "rendered output exists",
        "native answers source verified",
        "disposable stack artifact present",
        "no rejected Copier hunks",
        "TOML parse validation passed",
        "generated project tests passed"
        if tests_ran
        else "no generated test suite declared",
    )


def _gitignore_lines(text: str) -> list[str]:
    """Retain ordered rules and comments; deduplicate only exact lines."""
    lines = text.splitlines()
    if text.endswith("\n"):
        return lines
    return lines


def _compose_members(
    stack: Stack,
    renders: list[tuple[Member, Rendered, Path]],
    destination: Path,
) -> list[tuple[Member, Rendered, Path]]:
    """Compose disjoint files and explicit shared structures into one preview."""
    artifact = stack_artifact_name(stack.name)
    for _, rendered, source in renders:
        if rendered.answers_relpath == artifact or (source / artifact).exists():
            raise AssemblyError(
                "composition",
                f"template contribution uses reserved stack artifact path: {artifact}",
            )
    destination.mkdir()
    seen: dict[str, Member] = {}
    answers: dict[str, Path] = {}
    for member, rendered, source in renders:
        if rendered.answers_relpath in answers:
            raise AssemblyError(
                "composition",
                f"templates {answers[rendered.answers_relpath].parent.name} and "
                f"{member.name} share answers file {rendered.answers_relpath}; "
                "declare a distinct native answers file for each template",
            )
        answers[rendered.answers_relpath] = destination / rendered.answers_relpath
        answers_target = destination / rendered.answers_relpath
        answers_target.parent.mkdir(parents=True, exist_ok=True)
        native_answers = source / rendered.answers_relpath
        if not native_answers.is_file():
            # Copier does not require a template to stamp its answers file.
            # Adopt already owns the sanctioned native record format.
            from .adopt import stamp

            stamp(rendered, source)
        # The render may carry a normalized Git source for future updates.
        # Copy that prepared answers file once; do not replace it with the raw
        # render's source metadata in the second file-composition pass.
        answers_record = native_answers.read_bytes()
        answers_target.write_bytes(answers_record)
        for path in sorted(source.rglob("*")):
            if path.is_dir():
                continue
            relative = path.relative_to(source).as_posix()
            if relative == rendered.answers_relpath:
                continue
            target = destination / relative
            if relative not in seen:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
                seen[relative] = member
                continue
            first = seen[relative]
            if relative == ".gitignore":
                lines = _gitignore_lines(target.read_text(encoding="utf-8"))
                for line in _gitignore_lines(path.read_text(encoding="utf-8")):
                    if line not in lines:
                        lines.append(line)
                target.write_text("\n".join(lines) + "\n", encoding="utf-8")
                continue
            if relative.endswith(".toml"):
                merger = TomlMerger()
                ours = target.read_text(encoding="utf-8")
                theirs = path.read_text(encoding="utf-8")
                if not merger.accepts(relative, "", ours, theirs):
                    raise AssemblyError(
                        "composition",
                        f"cannot parse shared TOML {relative} from {member.name}",
                    )
                result = merger.merge(relative, "", ours, theirs)
                if result.warnings:
                    raise AssemblyError(
                        "composition",
                        f"same-key conflict in {relative} from {member.name}: "
                        + "; ".join(result.warnings)
                        + "; require a declared precedence rule or review",
                    )
                target.write_text(result.text, encoding="utf-8")
                continue
            raise AssemblyError(
                "composition",
                f"unsupported shared file {relative}: {first.name} and "
                f"{member.name} both contribute it; identical or text/binary "
                "files are not concatenated or silently selected",
            )
    return renders


def _native_update_commands(
    renders: list[tuple[Member, Rendered, Path]],
) -> tuple[str, ...]:
    return tuple(
        f"copier update --defaults -a {rendered.answers_relpath}"
        + (" --trust" if member.trust else "")
        for member, rendered, _ in renders
    )


def _write_stack_artifact(
    destination: Path,
    stack: Stack,
    renders: list[tuple[Member, Rendered, Path]],
    answers: dict[str, dict[str, Any]],
    *,
    status: str,
) -> None:
    """Write the definition and this application's state in one stack file.

    The application members point at native Copier answers files, not a second
    stamp record. The preview file becomes the approved project's artifact only
    after the already-authorized destination write.
    """
    record = {
        "schema_version": 1,
        "definition": {
            "name": stack.name,
            "members": [
                {
                    "id": member.name,
                    "role": member.role,
                    "source": member.source,
                    "ref": member.ref,
                    "capabilities": list(member.capabilities),
                }
                for member in stack.members
            ],
        },
        "application": {
            "status": status,
            "members": [
                {
                    "id": member.name,
                    "source": rendered.src,
                    "ref": rendered.commit,
                    "answers": answers[member.name],
                    "native": {
                        "answers_file": rendered.answers_relpath,
                        "update_command": (
                            f"copier update --defaults -a {rendered.answers_relpath}"
                            + (" --trust" if member.trust else "")
                        ),
                    },
                }
                for member, rendered, _ in renders
            ],
        },
    }
    (destination / stack_artifact_name(stack.name)).write_text(
        "# Stack definition and application state. Native Copier updates do not "
        "depend on this file.\n" + yaml.safe_dump(record, sort_keys=False),
        encoding="utf-8",
    )


def _validate_members(
    destination: Path,
    renders: list[tuple[Member, Rendered, Path]],
    run_tests: bool,
    environment: Path,
    stack_artifact: Path,
) -> tuple[str, ...]:
    checks: tuple[str, ...] = (
        "rendered output exists",
        "disjoint template files composed",
    )
    for _, rendered, _ in renders:
        checks += _validate(destination, rendered, False, environment, stack_artifact)
    checks += tuple(
        f"native answers verified: {rendered.answers_relpath}"
        for _, rendered, _ in renders
    )
    tests_ran = _run_project_tests(destination, environment) if run_tests else False
    return (
        *checks,
        "generated project tests passed"
        if tests_ran
        else "no generated test suite declared",
    )


def _check_native_update(
    member: Member,
    rendered: Rendered,
    source: Path,
    preview: Path,
) -> None:
    """Verify one ordinary Copier update without rewriting the composed preview."""
    update_root = _member_preview_path(preview, "update", member)
    update_source, update_ref = _validation_source(member, rendered, source, preview)
    shutil.copytree(source, update_root)
    if update_source != rendered.src:
        answers = update_root / rendered.answers_relpath
        original = answers.read_text(encoding="utf-8")
        original = re.sub(
            r"(?m)^_src_path: .*$", f"_src_path: {update_source}", original, count=1
        )
        original = re.sub(
            r"(?m)^_commit: .*$", f"_commit: {update_ref}", original, count=1
        )
        answers.write_text(original, encoding="utf-8")
    subprocess.run(
        ["git", "init", "-q", str(update_root.resolve())],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "add", "-A"],
        cwd=update_root,
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
            f"Initial {member.name} project",
        ],
        cwd=update_root,
        check=True,
        capture_output=True,
        text=True,
    )
    with contextlib.redirect_stdout(sys.stderr):
        update = copier.run_update(
            update_root,
            defaults=True,
            quiet=True,
            overwrite=True,
            skip_tasks=True,
            answers_file=rendered.answers_relpath,
            unsafe=member.trust,
            vcs_ref=update_ref,
        )
    if update.answers_relpath != Path(rendered.answers_relpath):
        raise AssemblyError(
            "validation", f"native update used the wrong answers file for {member.name}"
        )
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=update_root,
        check=True,
        capture_output=True,
        text=True,
    )
    if status.stdout:
        raise AssemblyError(
            "validation",
            f"native update left changes for {member.name}: {status.stdout}",
        )


def assemble(
    stack: Stack,
    destination: Path,
    answers: dict[str, dict[str, Any]],
    *,
    write: bool,
    retain_preview: bool,
    run_tests: bool = True,
) -> AssemblyPlan:
    """Render and validate in isolation; copy only after explicit write approval."""
    _assert_new_destination(destination)
    temporary = tempfile.TemporaryDirectory(prefix="copier-cat-assemble-")
    preview = Path(temporary.name).resolve()
    try:
        try:
            renders: list[tuple[Member, Rendered, Path]] = []
            for member in stack.members:
                member_preview = _member_preview_path(preview, "render", member)
                local_source = _local_git_source(member.source)
                render_source = (
                    str(local_source)
                    if member.ref is None and local_source is not None
                    else member.source
                )
                with contextlib.redirect_stdout(sys.stderr):
                    rendered = render(
                        render_source,
                        member_preview,
                        answers[member.name],
                        defaults=True,
                        trust=member.trust,
                        vcs_ref=member.ref or "HEAD",
                    )
                rendered = _native_answers_source(local_source, rendered)
                if rendered.src != render_source:
                    native_answers = member_preview / rendered.answers_relpath
                    original_text = native_answers.read_text(encoding="utf-8")
                    source_line = next(
                        line
                        for line in original_text.splitlines(keepends=True)
                        if line.startswith("_src_path:")
                    )
                    original_text = original_text.replace(
                        source_line, f"_src_path: {rendered.src}\n", 1
                    )
                    original_commit = yaml.safe_load(original_text)["_commit"]
                    if rendered.commit is not None and rendered.commit != str(
                        original_commit
                    ):
                        commit_line = next(
                            line
                            for line in original_text.splitlines(keepends=True)
                            if line.startswith("_commit:")
                        )
                        serialized_commit = yaml.safe_dump(
                            {"_commit": rendered.commit}, default_flow_style=False
                        ).split(": ", 1)[1]
                        original_text = original_text.replace(
                            commit_line, f"_commit: {serialized_commit}", 1
                        )
                    native_answers.write_text(original_text, encoding="utf-8")
                renders.append((member, rendered, member_preview))
            _compose_members(stack, renders, preview / "render")
            _write_stack_artifact(
                preview / "render", stack, renders, answers, status="preview"
            )
            checks = _validate_members(
                preview / "render",
                renders,
                run_tests,
                preview / "test-env",
                preview / "render" / stack_artifact_name(stack.name),
            )
            for member, rendered, source in renders:
                if rendered.commit is None:
                    checks += (
                        f"native Copier update unavailable: {member.name} has no "
                        "Git commit baseline",
                    )
                    continue
                _check_native_update(member, rendered, source, preview)
                checks += (f"native Copier update succeeded: {member.name}",)
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
            _write_stack_artifact(
                final_preview, stack, renders, answers, status="applied"
            )
            shutil.copytree(final_preview, destination)
        commands = _native_update_commands(renders)
        return AssemblyPlan(
            stack=stack,
            destination=destination,
            preview=final_preview,
            rendered=renders[0][1],
            answers=answers,
            update_command=commands[0],
            update_commands=commands,
            checks=checks,
            retained=retain_preview,
        )
    finally:
        temporary.cleanup()
