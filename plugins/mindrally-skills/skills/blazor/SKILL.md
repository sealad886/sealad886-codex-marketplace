---
name: blazor
description: "Use when implementing Blazor components, data binding, render modes, lifecycle, state, or authorization."
---

# Blazor Development Guidelines

## When to invoke

Use when implementing Blazor components, data binding, render modes, lifecycle, state, or authorization. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target .NET/render mode, prerendering, routing parameters, DI lifetimes, data endpoints, and browser interaction. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify render mode and the lifecycle that owns parameter-dependent loading and state.
2. Implement async component behavior with valid intermediate render state, disposal, cancellation, and server authorization.
3. Check parameter changes, prerender/hydration, reconnect, errors, list identity, and user interaction.

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
