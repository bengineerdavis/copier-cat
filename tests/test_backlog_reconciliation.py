"""Public CLI contract for the cross-branch Backlog identity audit."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
AUDIT = ROOT / "scripts" / "audit_backlog.py"


def run_audit(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUDIT), "--root", str(root), *extra],
        capture_output=True,
        text=True,
        check=False,
    )


def write_record(root: Path, path: str, identifier: str, title: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"---\nid: {identifier}\ntitle: {title}\n---\n")


def test_audit_detects_duplicate_ids_within_one_checkout(tmp_path: Path) -> None:
    write_record(tmp_path, "backlog/tasks/a.md", "CCC-99", "One task")
    write_record(tmp_path, "backlog/drafts/b.md", "CCC-99", "One task")
    result = run_audit(tmp_path)
    assert result.returncode == 1
    assert json.loads(result.stdout)["collisions"] == [
        {"id": "CCC-99", "paths": ["backlog/drafts/b.md", "backlog/tasks/a.md"]}
    ]


def test_audit_accepts_one_id_on_separate_branches(tmp_path: Path) -> None:
    write_record(tmp_path, "backlog/tasks/a.md", "CCC-99", "Same task")
    result = run_audit(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {"records": 1, "collisions": []}


def test_audit_detects_one_id_meaning_different_things_on_two_branches(
    tmp_path: Path,
) -> None:
    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    def commit(message: str) -> None:
        git("add", "-A")
        git(
            "-c",
            "user.name=tests",
            "-c",
            "user.email=tests@example.com",
            "commit",
            "-qm",
            message,
        )

    git("init", "-q", "-b", "main")
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "First meaning")
    commit("first")
    git("checkout", "-qb", "other")
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "Other meaning")
    commit("second")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    assert json.loads(result.stdout)["collisions"] == [
        {"id": "decision-10", "titles": ["First meaning", "Other meaning"]},
        {
            "id": "decision-10",
            "paths": ["backlog/decisions/one.md", "backlog/decisions/two.md"],
        },
    ]


def test_audit_detects_uncommitted_record_colliding_with_a_committed_branch(
    tmp_path: Path,
) -> None:
    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    def commit(message: str) -> None:
        git("add", "-A")
        git(
            "-c",
            "user.name=tests",
            "-c",
            "user.email=tests@example.com",
            "commit",
            "-qm",
            message,
        )

    git("init", "-q", "-b", "main")
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "First meaning")
    commit("first")
    git("checkout", "-qb", "other")
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "Other meaning")
    commit("second")
    git("checkout", "-q", "main")
    # Uncommitted working-tree edit that collides with the committed branch.
    write_record(tmp_path, "backlog/decisions/three.md", "decision-10", "Other meaning")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["First meaning", "Other meaning"]} in (
        payload["collisions"]
    ), payload


def test_current_checkout_has_unique_backlog_ids() -> None:
    result = run_audit(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
