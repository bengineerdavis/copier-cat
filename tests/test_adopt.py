"""The adopt flow library: render, classify, apply, stamp (spec C1).

Classification is terminal over the registry's result (decision-2's
empty base): add / identical / merge / conflict. The answers file is
the stamp — derived and written by cc, never a reviewed template file.
"""

import subprocess
from pathlib import Path

import yaml

from copier_cat.adopt import ADD, CONFLICT, IDENTICAL, MERGE, classify, render, stamp
from copier_cat.adopt import apply as apply_plan

ANSWERS = {"project_name": "demo"}


def short_sha(root: Path) -> str:
    """The template HEAD's short sha — the baseline adopt records."""
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def test_render_uses_head_and_derives_stamp_inputs(template, tmp_path):
    rendered = render(str(template), tmp_path / "render", ANSWERS)
    assert rendered.commit == short_sha(template)
    assert rendered.src == str(template)
    assert rendered.answers_relpath == ".copier-answers.yml"
    # Only questions the template asks: the injected jinja helpers
    # (`now`, `make_secret`) and internal keys never reach the stamp.
    assert rendered.answers == {"project_name": "demo"}


def test_render_records_head_after_a_template_change(template, tmp_path):
    (template / "notes.txt.jinja").write_text("template note v2\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=template, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=tests@example.com",
            "-c",
            "user.name=tests",
            "commit",
            "-qm",
            "template v2",
        ],
        cwd=template,
        check=True,
    )
    rendered = render(str(template), tmp_path / "render", ANSWERS)
    assert rendered.commit == short_sha(template)


def test_classify_covers_add_identical_merge_conflict(template, project, tmp_path):
    rendered = render(str(template), tmp_path / "render", ANSWERS)
    plans = {plan.path: plan for plan in classify(rendered, project)}

    # The answers file is the stamp, not a reviewed template file.
    assert ".copier-answers.yml" not in plans
    # Project-only files are not template-rendered: untouched.
    assert "keep.txt" not in plans

    assert plans["README.md"].classification == ADD
    assert plans["README.md"].current is None

    assert plans["mise.toml"].classification == IDENTICAL
    assert plans["mise.toml"].proposed == plans["mise.toml"].current

    # Disjoint TOML tables merge clean through the registry's TOML
    # merger: a proposal, not a conflict.
    assert plans["extra.toml"].classification == MERGE
    assert plans["extra.toml"].merger == "toml"
    assert plans["extra.toml"].conflicted is False
    assert 'key = "value"' in plans["extra.toml"].proposed
    assert 'own = "keep"' in plans["extra.toml"].proposed

    # Add/add text lands as conflict markers for review (decision-2:
    # the add/add cost is paid once, in the review flow).
    assert plans["notes.txt"].classification == CONFLICT
    assert plans["notes.txt"].conflicted is True
    assert "<<<<<<<" in plans["notes.txt"].proposed


def test_apply_lands_accepted_and_never_commits(template, project, tmp_path):
    rendered = render(str(template), tmp_path / "render", ANSWERS)
    plans = {plan.path: plan for plan in classify(rendered, project)}

    apply_plan(plans["README.md"], project)  # add
    apply_plan(plans["extra.toml"], project)  # clean merge proposal
    apply_plan(  # review's edit replaces the proposal, markers never land
        plans["notes.txt"], project, edited="resolved by hand\n"
    )

    assert (project / "README.md").read_text(encoding="utf-8") == "# demo\n"
    extra = (project / "extra.toml").read_text(encoding="utf-8")
    assert 'key = "value"' in extra and 'own = "keep"' in extra
    assert (project / "notes.txt").read_text(encoding="utf-8") == ("resolved by hand\n")
    # Rejected proposals leave the project file standing; the
    # project-only file was never template business.
    assert (project / "keep.txt").read_text(encoding="utf-8") == "project only\n"
    # cc never runs git: adopting leaves no repository behind.
    assert not (project / ".git").exists()


def test_stamp_writes_the_copier_answers_convention(template, project, tmp_path):
    rendered = render(str(template), tmp_path / "render", ANSWERS)
    target = stamp(rendered, project)

    assert target == project / ".copier-answers.yml"
    text = target.read_text(encoding="utf-8")
    assert text.startswith("# Changes here will be overwritten by Copier\n")
    record = yaml.safe_load(text)
    # _commit first (the baseline future updates merge against),
    # _src_path second, the adopted answers after — copier's own order.
    assert record["_commit"] == short_sha(template)
    assert record["_src_path"] == str(template)
    assert record["project_name"] == "demo"
    assert "now" not in record


def test_jinja_answers_filename_is_expanded_and_stamped(
    jinja_answers_template, project, tmp_path
):
    # copier-template-copier-template's shape: _answers_file is jinja'd
    # under custom envops. render() must capture the expanded name —
    # the raw name would let the answers file be reviewed as an ordinary
    # template file and stamp to the wrong path (dogfood finding).
    rendered = render(str(jinja_answers_template), tmp_path / "render", ANSWERS)
    assert rendered.answers_relpath == ".copier-answers.demo.yml"

    # The expanded answers file is skipped as the stamp, not reviewed.
    plans = {plan.path: plan for plan in classify(rendered, project)}
    assert ".copier-answers.demo.yml" not in plans
    assert plans["README.md"].classification == ADD

    # The stamp lands at the expanded path with the recorded baseline.
    target = stamp(rendered, project)
    assert target == project / ".copier-answers.demo.yml"
    record = yaml.safe_load(target.read_text(encoding="utf-8"))
    assert record["_commit"] == short_sha(jinja_answers_template)
    assert record["project_name"] == "demo"


def test_stamp_skips_commit_for_a_plain_directory_template(tmp_path, project):
    plain = tmp_path / "plain-tpl"
    plain.mkdir()
    (plain / "copier.yml").write_text("project_name:\n  type: str\n  default: demo\n")
    (plain / "hello.txt.jinja").write_text("hello {{ _copier_conf.project_name }}\n")

    rendered = render(str(plain), tmp_path / "render", ANSWERS)
    assert rendered.commit is None

    stamp(rendered, project)
    record = yaml.safe_load(
        (project / ".copier-answers.yml").read_text(encoding="utf-8")
    )
    assert "_commit" not in record
    assert record["_src_path"] == str(plain)
    assert record["project_name"] == "demo"
