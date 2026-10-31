---
name: angular-development
description: "Use when implementing or debugging Angular components, templates, signals, dependency injection, forms, or routing."
---

# Angular Development

## When to invoke

Use when implementing or debugging Angular components, templates, signals, dependency injection, forms, or routing. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Angular/TypeScript versions, standalone or NgModule structure, templates, routing, state, and test tooling. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify the component/state boundary and choose APIs supported by the installed Angular version.
2. Implement typed inputs, outputs, services, forms, and templates with explicit ownership and accessible semantics.
3. Verify rendered behavior, asynchronous updates, error handling, route loading, and relevant performance measurements.

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
