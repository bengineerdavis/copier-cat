---
id: CCC-22
title: Publish approved session artifacts and queued project PRs
status: To Do
created_date: 2026-11-14 19:00
updated_date: 2026-11-15 06:22
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
All previously planned copier-cat PRs have merged, but the current design session created new untracked tasks, approved local implementation issues, and an unsaved-to-version-control prototype. These records need explicit publication and PR ownership rather than disappearing at cleanup.

Ship:

- Reconciliation of the session’s modified and untracked artifacts into an approved publication inventory, preserving the separate testkit specification and prototype evidence in their intended project records or prototype branches.
- One or more focused copier-cat PRs publishing the approved backlog-task corrections, implementation tickets, and explicitly approved prototype evidence without mixing them with unrelated work.
- A publication and handoff report identifying each PR, unmerged artifact, and downstream owner after the PRs are merged and any finished worktrees are cleaned up.

Constraints:

- Git commits, branch/worktree creation, pushes, and PR creation require separate explicit maintainer approval at each action.
- Keep the testkit specification out of copier-cat’s implementation scope; its content belongs to the standalone testkit project path.
- Reconcile .scratch tickets into the configured Backlog tracker before implementation rather than preserving two active ticket systems.
- Do not implement the assembly MVP or a fork-based upstream submission workflow in this task.
- Any new skill introduced by implementation is declared in agents.toml in the same change.

Agreed with the maintainer 2026-11-14: the handoff must account for the PRs and publication work still needed for copier-cat.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The publication inventory accounts for every session-created artifact and its intended owner without discarding other sessions’ work
- [ ] #2 Approved copier-cat records and prototype evidence are published in focused PRs with their contents and scope verified
- [ ] #3 The handoff names merged PRs, remaining unmerged artifacts, downstream owners, and completed cleanup
- [ ] #4 backlog-py board shows this publication task with its full description and acceptance criteria
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Publication scope approved 2026-11-14: the first records-only PR contains CCC-11, CCC-19, CCC-20, CCC-21, and CCC-22. The six .scratch tickets require native Backlog reconciliation; the UX prototype uses a separate prototype branch; the testkit specification follows the standalone testkit project path. APT-49..51 and APL-26..27 remain separate repository records. No implementation or fork-based upstream workflow is included.
Artifact preservation 2026-11-14: the testkit specification moved unchanged from .worktrees/copier-testkit-spec/.spec-testkit.md to the standalone copier-testkit project as docs/SPEC.md. Published privately at https://github.com/bengineerdavis/copier-testkit (initial commit e067c93). Scaffold verification: 3 tests, Ruff, formatting, and pyrefly passed. TASK-1 records the template-prefix and agentic-source provenance issues. The old copier-testkit-spec branch is contained in main and has no task-specific commits; its worktree and local branch are safe to remove after this preservation link is published.
Assembly UX evidence published 2026-11-14 on prototype/cc-assembly-ux at bf924fd. The older prototype/cc-composition-cli branch remains separate. Earlier cc-stack-probe experiments under ~/code/try are separate exploratory artifacts, not included in this evidence publication. The external UX source directory is superseded after main links to the branch; the original ticket archive in DOC-10 and CCC-23 local task remain untouched.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
