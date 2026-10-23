"""The adopt flow (spec C1): render, classify, review, stamp.

Decision-2 shapes the whole module: adopt renders the template fresh at
its current version, resolves every rendered file against the project
through the merger registry with the empty tree as the merge base, and
writes the copier answers file as the recorded update baseline. The
per-file review (the consent moment) decides which proposals land;
applying accepted merges writes into the working tree, and cc never
commits — committing stays the user's act (decision log: Adopt apply
flow).

The template is never asked to cooperate (decision log:
Classification ownership): classification is derived from what the
render produces, and the answers file is derived from the worker copier
already ran — its questions, their answers, the template's current
commit, and its configured answers filename (copier's per-template
naming). Rendering runs at `vcs_ref="HEAD"` — the adopted template's
current version is the baseline future updates merge against; a plain
directory template carries no commit, and the answers file then records
`_src_path` only. Copier's own answers filter (its worker's
`_answers_to_remember`) is replicated here rather than reached into —
private API across copier versions is not a dependency cc takes.

Classification is terminal over the registry's result: a project file
that is absent or empty is an add (the registry fast path takes the
render); a conflicted merge is a conflict (its proposal carries conflict
markers for review); a merged text equal to the project's is identical
(nothing to consent to); anything else is a merge proposal. Binary
content is the one carve-out: a file that is not valid UTF-8 — in the
render or the project — never enters the registry, whose mergers are
text-shaped. It is classified directly from existence and byte
equality, carries a warning naming the shape, and lands verbatim: the
template's bytes on accept, the project's bytes on reject. All merging
goes through the registry — adopt carries no merge logic of its own
(task CC-3 DOD).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import copier
import yaml

from .merge import Registry, default_registry

ADD = "add"
IDENTICAL = "identical"
MERGE = "merge"
CONFLICT = "conflict"

ANSWERS_HEADER = "# Changes here will be overwritten by Copier\n"


@dataclass(frozen=True)
class Rendered:
    """What one template render yields, plus the stamp inputs.

    `answers` carries the questions copier asked and their adopted
    answers; `commit` is the template's current version (short sha for
    git templates, None for a plain directory); `answers_relpath` is
    the template-configured answers filename — copier's per-template
    naming, not a cc convention.
    """

    src: str
    root: Path
    answers_relpath: str
    commit: str | None
    answers: dict[str, Any]


@dataclass(frozen=True)
class FilePlan:
    """One rendered file's adopt resolution, before review.

    `binary` marks content that never enters the text merger: its
    `current`/`proposed` strings are display text (replacement-decoded),
    while landing copies the render's bytes verbatim.
    """

    path: str
    classification: str
    merger: str
    conflicted: bool
    warnings: tuple[str, ...]
    current: str | None
    proposed: str
    binary: bool = False


def render(
    src: str,
    dst: Path,
    data: dict[str, Any],
    *,
    defaults: bool = False,
    trust: bool = False,
) -> Rendered:
    """Render the template at its current version into `dst`.

    `dst` is caller-owned (a temp dir in the CLI): rendering never
    touches the project — classification and review stand between the
    render and the working tree. Questions without an answer in `data`
    prompt interactively unless `defaults` takes the template's
    defaults; `trust` passes copier's unsafe flag for templates with
    jinja extensions. Template tasks are skipped: adopt renders, it does
    not run the template's update-time machinery.
    """
    worker = copier.run_copy(
        src,
        dst,
        data=data,
        defaults=defaults,
        overwrite=True,
        quiet=True,
        unsafe=trust,
        skip_tasks=True,
        vcs_ref="HEAD",
    )
    # The answers filter mirrors copier's worker `_answers_to_remember`:
    # only questions the template actually asks, never injected jinja
    # helpers (`now`, `make_secret`), internal keys, hidden or secret
    # questions.
    answers = {
        str(key): value
        for key, value in worker.answers.combined.items()
        if not str(key).startswith("_")
        and key not in worker.answers.hidden
        and key not in worker.template.secret_questions
        and key in worker.template.questions_data
    }
    return Rendered(
        src=worker.template.url,
        root=dst,
        answers_relpath=str(worker.template.answers_relpath),
        commit=worker.template.commit,
        answers=answers,
    )


def _binary_plan(
    rel: str, theirs: str, ours_bytes: bytes, theirs_bytes: bytes
) -> FilePlan:
    """Classify a non-UTF-8 payload without touching the text merger.

    The registry is text-shaped, so binary content is resolved directly:
    byte-identical is identical, a missing or empty project side is an
    add, anything else is a conflict — accept lands the render's bytes
    verbatim, reject keeps the project's. The plan's `current`/`proposed`
    are replacement-decoded display text; landing never writes them.
    """
    if not ours_bytes.strip():
        return FilePlan(
            path=rel,
            classification=ADD,
            merger="",
            conflicted=False,
            warnings=("binary file: accept lands the template's bytes verbatim",),
            current=None,
            proposed=theirs,
            binary=True,
        )
    if ours_bytes == theirs_bytes:
        return FilePlan(
            path=rel,
            classification=IDENTICAL,
            merger="",
            conflicted=False,
            warnings=(),
            current=theirs,
            proposed=theirs,
            binary=True,
        )
    return FilePlan(
        path=rel,
        classification=CONFLICT,
        merger="",
        conflicted=True,
        warnings=(
            (
                "binary file: conflicting versions — accept lands the "
                "template's bytes verbatim, reject keeps the project's"
            ),
        ),
        current=ours_bytes.decode("utf-8", errors="replace"),
        proposed=theirs,
        binary=True,
    )


def classify(
    rendered: Rendered,
    project: Path,
    registry: Registry | None = None,
) -> list[FilePlan]:
    """Classify every rendered file against the project (decision-2).

    The merge base is always the empty tree: adopt passes it and the
    registry never invents one. The answers file is deliberately
    absent from the plans — it is the stamp, derived and written by cc,
    not template-owned content under review. Content that is not valid
    UTF-8 — in the render or the project — never reaches the registry:
    it is classified from existence and byte equality, and its plan
    carries `binary=True` so landing copies the render's bytes
    verbatim.
    """
    registry = registry or default_registry()
    plans: list[FilePlan] = []
    for path in sorted(
        p.relative_to(rendered.root) for p in rendered.root.rglob("*") if p.is_file()
    ):
        rel = path.as_posix()
        if rel == rendered.answers_relpath:
            continue
        theirs_bytes = (rendered.root / path).read_bytes()
        project_file = project / path
        ours_bytes = project_file.read_bytes() if project_file.is_file() else b""
        try:
            theirs = theirs_bytes.decode("utf-8")
        except UnicodeDecodeError:
            theirs = theirs_bytes.decode("utf-8", errors="replace")
            plans.append(_binary_plan(rel, theirs, ours_bytes, theirs_bytes))
            continue
        try:
            ours = ours_bytes.decode("utf-8")
        except UnicodeDecodeError:
            ours = ours_bytes.decode("utf-8", errors="replace")
            plans.append(_binary_plan(rel, theirs, ours_bytes, theirs_bytes))
            continue
        result = registry.merge(rel, "", ours, theirs)
        if not project_file.is_file() or not ours.strip():
            classification = ADD
        elif result.conflicted:
            classification = CONFLICT
        elif result.text == ours:
            classification = IDENTICAL
        else:
            classification = MERGE
        plans.append(
            FilePlan(
                path=rel,
                classification=classification,
                merger=result.merger,
                conflicted=result.conflicted,
                warnings=result.warnings,
                current=ours or None,
                proposed=result.text,
            )
        )
    return plans


def apply(
    plan: FilePlan,
    project: Path,
    *,
    rendered: Rendered | None = None,
    edited: str | None = None,
) -> Path:
    """Land one accepted plan in the working tree; never commit.

    `edited` replaces the proposal when review chose to edit — the
    per-file review flow resolves conflicts there, not in the tree.
    Binary plans land the render's bytes verbatim (a text write of
    replacement-decoded content would corrupt them), so they require
    the render; editing a binary plan is an explicit choice to replace
    its bytes with the edited text.
    """
    target = project / plan.path
    target.parent.mkdir(parents=True, exist_ok=True)
    if plan.binary and edited is None:
        if rendered is None:
            raise ValueError(
                f"binary plan {plan.path} needs the render to land verbatim"
            )
        target.write_bytes((rendered.root / plan.path).read_bytes())
        return target
    target.write_text(edited if edited is not None else plan.proposed, encoding="utf-8")
    return target


def stamp(rendered: Rendered, project: Path) -> Path:
    """Write the answers file: the recorded baseline for future updates.

    `_commit` first (when the template has one), `_src_path` second, the
    adopted answers after — copier's own answers-file order, so plain
    `copier update` finds the baseline it expects.
    """
    record: dict[str, Any] = {}
    if rendered.commit is not None:
        record["_commit"] = rendered.commit
    record["_src_path"] = rendered.src
    record.update(rendered.answers)
    target = project / rendered.answers_relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        ANSWERS_HEADER
        + yaml.safe_dump(record, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    return target
