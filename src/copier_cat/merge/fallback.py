"""The format-blind fallback: a plain `git merge-file` three-way merge.

Decision-1's fallback for formats no structure-aware merger accepts. It
is also the inner machinery the marked-section merger uses for the
non-region content of a file. Conflict markers are the output shape —
the per-file review flow resolves them (decision-2: the add/add cost is
paid once, in the review flow).
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .types import MergeResult


class MergeToolError(RuntimeError):
    """The merge tooling itself failed (git missing, unexpected exit)."""


def git_merge_file(
    base: str,
    ours: str,
    theirs: str,
    labels: tuple[str, str, str] = ("base", "ours", "theirs"),
) -> tuple[str, bool]:
    """Run `git merge-file -p` over the three inputs.

    Returns (merged_text, conflicted). The exit code is the conflict
    count, truncated at 127; above that range (or a negative code from a
    signal death) means the tool itself failed and raises
    MergeToolError, as does a missing git binary.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        ours_path = tmp_dir / "ours"
        base_path = tmp_dir / "base"
        theirs_path = tmp_dir / "theirs"
        ours_path.write_text(ours, encoding="utf-8")
        base_path.write_text(base, encoding="utf-8")
        theirs_path.write_text(theirs, encoding="utf-8")
        try:
            proc = subprocess.run(
                [
                    "git",
                    "merge-file",
                    "-p",
                    "-L",
                    labels[1],
                    "-L",
                    labels[0],
                    "-L",
                    labels[2],
                    str(ours_path),
                    str(base_path),
                    str(theirs_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            raise MergeToolError(f"git merge-file could not run: {error}") from error
    if proc.returncode < 0 or proc.returncode > 127:
        raise MergeToolError(f"git merge-file failed: {proc.stderr.strip()}")
    return proc.stdout, proc.returncode > 0


class GitMergeFileMerger:
    """The registry's fallback merger: accepts everything, merges blind."""

    name = "git-merge-file"

    def accepts(self, path: str, base: str, ours: str, theirs: str) -> bool:
        return True

    def merge(self, path: str, base: str, ours: str, theirs: str) -> MergeResult:
        text, conflicted = git_merge_file(base, ours, theirs)
        return MergeResult(text=text, conflicted=conflicted)
