---
name: design-systems
description: "Use when creating or evolving design tokens, component libraries, theming, UI documentation, or governance."
---

# Design Systems Best Practices

## When to invoke

Use when creating or evolving design tokens, component libraries, theming, UI documentation, or governance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect current product UI, consumer frameworks, token definitions, component APIs, browser/platform targets, and accessibility acceptance. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inventory existing components/tokens and identify required semantic states and consumer compatibility.
2. Implement the smallest coherent token/component change with documented variants, ownership, and accessible behavior.
3. Validate rendered states and consuming apps, then document version/migration impact without publishing unless authorized.

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
