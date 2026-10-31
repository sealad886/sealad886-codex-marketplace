---
name: flutter
description: "Use when implementing Flutter/Dart widgets, state management, navigation, asynchronous data, or app architecture."
---

# Flutter

## When to invoke

Use when implementing Flutter/Dart widgets, state management, navigation, asynchronous data, or app architecture. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Flutter/Dart/package versions, current state/DI/router choices, widget lifecycle, platform targets and accessibility requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define screen/data ownership and the requested user behavior using existing architecture.
2. Implement focused widgets and cancellable/disposable state resources with supported navigation/data APIs.
3. Run analyzer and meaningful unit/widget/integration checks plus target-device layout, accessibility and lifecycle verification.

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
