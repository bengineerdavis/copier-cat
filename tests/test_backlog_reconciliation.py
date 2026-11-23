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
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["First meaning", "Other meaning"]} in (
        payload["collisions"]
    ), payload
    assert {
        "id": "decision-10",
        "paths": ["backlog/decisions/one.md", "backlog/decisions/two.md"],
    } in payload["collisions"], payload


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
    # Both refs carry the SAME record, so committed refs alone do not collide.
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "First meaning")
    commit("first")
    git("checkout", "-qb", "other")
    write_record(tmp_path, "backlog/tasks/branch-marker.md", "CCC-98", "Marker")
    commit("marker on other")
    git("checkout", "-q", "main")
    # An uncommitted working-tree record colliding with the shared ID.
    write_record(tmp_path, "backlog/decisions/three.md", "decision-10", "Other meaning")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["First meaning", "Other meaning"]} in (
        payload["collisions"]
    ), payload


def test_audit_allows_uncommitted_title_edit_of_an_existing_record(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Old title")
    commit("first")
    git("checkout", "-qb", "other")
    write_record(tmp_path, "backlog/tasks/branch-marker.md", "CCC-98", "Marker")
    commit("marker on other")
    git("checkout", "-q", "main")
    # Routine uncommitted title edit: one record, not two meanings.
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "New title")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_detects_duplicate_ids_inside_a_non_current_branch(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "other")
    # The non-current branch alone carries the duplicate; same ID, same title,
    # different paths — duplicate_ids must still catch it per branch.
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "Same title")
    commit("second on other")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert {
        "id": "decision-10",
        "paths": ["backlog/decisions/one.md", "backlog/decisions/two.md"],
    } in payload["collisions"], payload


def test_audit_allows_committed_retitle_on_a_sibling_branch(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Old title")
    commit("first")
    git("checkout", "-qb", "other")
    # Same path, retitled on the sibling branch: one record, not two meanings.
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "New title")
    commit("retitle on other")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_detects_retitle_when_the_id_means_two_different_records(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Old title")
    commit("first")
    git("checkout", "-qb", "other")
    # Different path, different title: a genuinely different record —
    # a same-path retitle would NOT collide.
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "New meaning")
    commit("different record on other")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    # Under option A the distinct record is flagged where it is visible:
    # branch `other` carries the ID at two unrelated paths.
    assert {
        "id": "decision-10",
        "paths": ["backlog/decisions/one.md", "backlog/decisions/two.md"],
    } in payload["collisions"], payload


def test_audit_detects_id_reuse_when_no_branch_holds_both_paths(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Old title")
    commit("first")
    git("checkout", "-q", "--orphan", "other")
    git("rm", "-rq", "--cached", ".")
    (tmp_path / "backlog/decisions/one.md").unlink()
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "New meaning")
    commit("unrelated branch reuses the id")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["New meaning", "Old title"]} in (
        payload["collisions"]
    ), payload


def test_audit_detects_retitle_plus_rename_hiding_id_reuse(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Old title")
    commit("first")
    git("checkout", "-qb", "retitle")
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "New title")
    commit("retitle")
    git("checkout", "-q", "main")
    git("checkout", "-qb", "rename")
    # Remove the path and re-add the ID at a new path with a new title:
    # a genuinely different record wearing the same ID.
    (tmp_path / "backlog/decisions/one.md").unlink()
    write_record(
        tmp_path, "backlog/decisions/two.md", "decision-10", "Different meaning"
    )
    commit("rename to a different record")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    expected = {
        "id": "decision-10",
        "titles": ["Different meaning", "New title", "Old title"],
    }
    assert expected in payload["collisions"], payload


def test_audit_allows_a_local_edit_matching_a_divergent_branch_title(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Other meaning")
    commit("divergent same-path on other")
    git("checkout", "-q", "main")
    # Uncommitted edit on main matches the divergent branch's title. One
    # path is one record lineage: same-path title differences are retitles
    # (option A), and same-path divergence is delegated to git's own merge
    # conflict. The audit exits clean.
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Other meaning")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_detects_same_title_records_on_independent_branches(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "other")
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "Same title")
    commit("second")
    git("checkout", "-q", "--orphan", "third")
    git("rm", "-rq", "--cached", ".")
    for stale in (tmp_path / "backlog").rglob("*.md"):
        stale.unlink()
    write_record(tmp_path, "backlog/decisions/three.md", "decision-10", "Same title")
    commit("third")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["Same title"]} in (payload["collisions"]), (
        payload
    )


def test_audit_detects_rename_plus_sibling_retitle_divergence(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Shared title")
    commit("first")
    # Branch A renames the record without retitling it.
    git("checkout", "-qb", "renamer")
    (tmp_path / "backlog/decisions/one.md").rename(
        tmp_path / "backlog/decisions/two.md"
    )
    commit("rename")
    git("checkout", "-q", "main")
    # Independent sibling branch B retitles the original record.
    git("checkout", "-qb", "retitler")
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "New title")
    commit("retitle")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    # Git itself merges both orders cleanly here (verified with real
    # `git merge`): the rename carries the retitled content to the new
    # path — one record's history, not ID reuse. The audit agrees.
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_allows_an_ordinary_git_mv_rename(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "rename")
    # An ordinary rename: git mv removes the old path on this branch.
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_allows_a_rename_when_the_parent_advances(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "rename")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed")
    # The parent advances with unrelated work after the fork.
    git("checkout", "-q", "main")
    write_record(tmp_path, "backlog/tasks/unrelated.md", "CCC-90", "Unrelated")
    commit("parent advances")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_allows_an_uncommitted_rename(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    # A routine staged rename, not yet committed.
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_allows_a_rename_when_the_base_path_carried_another_id(
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
    # The base's one.md carries a DIFFERENT id — not this record's history.
    write_record(tmp_path, "backlog/decisions/one.md", "CCC-1", "Same title")
    commit("first")
    git("checkout", "-qb", "replace")
    (tmp_path / "backlog/decisions/one.md").unlink()
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "Same title")
    commit("replaced with a different record")
    git("checkout", "-q", "main")
    git("checkout", "-qb", "sibling")
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("independently adds decision-10 at the old path")
    git("checkout", "-q", "main")
    # Git's own merge resolves this as one lineage: rename detection sees
    # one.md become two.md while the sibling's same-content edit rides the
    # rename, leaving a single path carrying decision-10 (verified with
    # git merge-tree, both merge orders). Under the option A ruling the
    # merge machinery is the arbiter — a clean merge is one record, not
    # an ID collision.

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert not any(c["id"] == "decision-10" for c in payload["collisions"]), payload


def test_audit_allows_a_rename_plus_independent_same_path_retitle(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Original")
    commit("first")
    git("checkout", "-qb", "rename")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed")
    git("checkout", "-q", "main")
    git("checkout", "-qb", "independent")
    # Same path, different meaning on an independent branch. Git merges
    # the whole sequence cleanly (verified with real `git merge` in both
    # orders): the rename carries the retitled content to the new path —
    # one record's history, not ID reuse. The audit agrees (option A).
    write_record(
        tmp_path, "backlog/decisions/one.md", "decision-10", "Different meaning"
    )
    commit("different record same path")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_detects_id_reuse_alongside_an_ordinary_rename(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "rename")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed")
    git("checkout", "-q", "main")
    git("checkout", "-qb", "reuse")
    # An independent third record wearing the same ID and title while a
    # sibling branch renamed the original: the ID means two things.
    write_record(tmp_path, "backlog/decisions/three.md", "decision-10", "Same title")
    commit("independent third path")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert any(c["id"] == "decision-10" for c in payload["collisions"]), payload


def test_audit_detects_divergent_renames_of_one_record(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "left")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/q.md")
    commit("renamed q")
    git("checkout", "-q", "main")
    git("checkout", "-qb", "right")
    # The same record renamed to two different destinations on sibling
    # branches: git reports a rename/rename conflict, and both files
    # keep the ID after any resolution — a divergence, not one lineage.
    git("mv", "backlog/decisions/one.md", "backlog/decisions/r.md")
    commit("renamed r")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["Same title"]} in (payload["collisions"]), (
        payload
    )


def test_audit_detects_titleless_id_reuse_on_another_branch(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    # No title: the record is malformed, but the ID still means a second
    # record — the audit must not treat the path as nonexistent. The
    # branch is an orphan holding only two.md, so duplicate_ids has no
    # within-branch pair to report; only the cross-branch path check
    # can catch it.
    git("checkout", "-q", "--orphan", "other")
    subprocess.run(
        ["git", "rm", "-rq", "--cached", "."],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    for stale in (tmp_path / "backlog").rglob("*.md"):
        stale.unlink()
    target = tmp_path / "backlog/decisions/two.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("---\nid: decision-10\n---\n")
    commit("titleless record reusing the id")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1, result.stdout + result.stderr


def test_audit_allows_sequential_renames_along_one_lineage(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "b1")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed one to two")
    git("checkout", "-qb", "b2")
    git("mv", "backlog/decisions/two.md", "backlog/decisions/three.md")
    commit("renamed two to three")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_allows_a_staged_second_rename_in_a_chain(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "b1")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed one to two")
    # Second rename staged but uncommitted — the lint-time state.
    git("mv", "backlog/decisions/two.md", "backlog/decisions/three.md")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 0, result.stdout + result.stderr


def test_audit_ignores_a_staged_rename_of_an_unrelated_id(
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
    # main's one.md is an unrelated record; two siblings independently
    # give decision-10 the same path and a new path — a collision the
    # audit must keep reporting.
    write_record(tmp_path, "backlog/decisions/one.md", "CCC-1", "Same title")
    commit("first")
    git("checkout", "-qb", "sib1")
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("sib1 carries decision-10 at one.md")
    git("checkout", "-q", "main")
    git("checkout", "-qb", "sib2")
    write_record(tmp_path, "backlog/decisions/two.md", "decision-10", "Same title")
    commit("sib2 carries decision-10 at two.md")
    git("checkout", "-q", "main")
    # Staging a rename of the CCC-1 record between the same two paths
    # must not union decision-10's nodes and hide the collision: staged
    # evidence is scoped to the audited record's own ID.
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["Same title"]} in (payload["collisions"]), (
        payload
    )


def test_audit_detects_independent_competing_rename_chains(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Same title")
    commit("first")
    git("checkout", "-qb", "bx")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("bx renames one to two")
    git("checkout", "-qb", "b2")
    git("mv", "backlog/decisions/two.md", "backlog/decisions/three.md")
    commit("b2 renames two to three")
    git("checkout", "-q", "main")
    # An independent sibling builds its own rename history over the same
    # paths; git reports rename/rename when the histories meet, so the
    # audit keeps them apart instead of composing one lineage. Both
    # renames are committed so duplicate_ids has no within-branch pair.
    git("checkout", "-qb", "b1")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("b1 independently renames one to two")
    git("mv", "backlog/decisions/two.md", "backlog/decisions/four.md")
    commit("b1 renames two to four")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert {"id": "decision-10", "titles": ["Same title"]} in (payload["collisions"]), (
        payload
    )


def test_audit_detects_id_reuse_from_an_orphan_at_a_renamed_path(
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
    write_record(tmp_path, "backlog/decisions/one.md", "decision-10", "Original")
    commit("first")
    git("checkout", "-qb", "rename")
    git("mv", "backlog/decisions/one.md", "backlog/decisions/two.md")
    commit("renamed")
    # An orphan branch shares no history: no git merge will ever exist to
    # catch its ID reuse at the old path, so the audit reports it.
    git("checkout", "-q", "--orphan", "orphan")
    subprocess.run(
        ["git", "rm", "-rq", "--cached", "."],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    for stale in (tmp_path / "backlog").rglob("*.md"):
        stale.unlink()
    write_record(
        tmp_path, "backlog/decisions/one.md", "decision-10", "Different record"
    )
    commit("orphan independently creates one.md")
    git("checkout", "-q", "main")

    result = run_audit(tmp_path, "--refs")
    assert result.returncode == 1, result.stdout + result.stderr


def test_current_checkout_has_unique_backlog_ids() -> None:
    result = run_audit(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
