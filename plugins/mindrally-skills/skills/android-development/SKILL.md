---
name: android-development
description: "Use when implementing or debugging Kotlin Android UI, navigation, lifecycle, background work, or app architecture."
---

# Android Development Best Practices

## When to invoke

Use when implementing or debugging Kotlin Android UI, navigation, lifecycle, background work, or app architecture. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Gradle/SDK/Kotlin versions, current Compose or Views stack, UI state ownership, manifest, and device requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Locate the UI/data boundaries and define state, events, persistence, and lifecycle behavior for the requested feature.
2. Implement within the established Compose or Views architecture using lifecycle-aware state and cancellable work.
3. Exercise recreation, navigation, permissions, background limits, loading/error states, and relevant device UI paths.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
