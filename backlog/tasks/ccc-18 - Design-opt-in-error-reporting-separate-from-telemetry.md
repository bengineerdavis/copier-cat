---
id: CCC-18
title: Design opt-in error reporting separate from telemetry
status: To Do
created_date: 2026-11-14 16:22
updated_date: 2026-11-14 17:03
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Why: errors should produce understandable, useful feedback and an easy path to a bug report without silently collecting user or project data. Error reporting and general usage telemetry are separate trust decisions.

Ship:
- A user-friendly error explanation naming the proposed action, what failed, the current operation, and safe next steps.
- An opt-in bug-report flow that previews exactly what would be shared, with whom, where, and why; redaction and secret/path exclusions are explicit.
- Independent preferences for bug reporting and general telemetry, asked during init and changeable later; both default to no automatic sharing.
- First-time offers for newly identified issues, without repeatedly prompting for the same issue or blocking recovery.
- Local-only report export when external reporting is unavailable or declined. No required Sentry account or service.
- An optional Sentry integration design, dynamically enabled only after consent, with no hidden telemetry dependency.
- Testable privacy, consent, deduplication, offline behavior, and maintainer diagnostics.

Constraints:
- Sharing is always opt-in and never bundled with assembly approval.
- Bug reporting is not general telemetry; enabling one never enables the other.
- A disable option must suppress the feature without breaking core CLI use.
- Do not send, upload, or create an issue merely because an error occurred.
- MVP scope and provider integration points remain design questions until reviewed.
- No implementation until the workflow review and privacy/consent boundaries are settled.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The design separates bug-report consent from general-telemetry consent and records their defaults and independent settings
- [ ] #2 A user can inspect a human-friendly error and the exact report payload, destination, recipients, purpose, and redactions before any sharing
- [ ] #3 Declining or disabling reporting and telemetry leaves local error explanations, validation, and recovery fully functional
- [ ] #4 Unique-issue prompts are deduplicated and bounded, never repeatedly block the user, and do not auto-submit reports
- [ ] #5 The design supports a local report artifact without Sentry and an optional consent-gated Sentry adapter
- [ ] #6 Privacy tests cover secrets, paths, answers, project contents, environment data, redaction, and no-network behavior before consent
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
