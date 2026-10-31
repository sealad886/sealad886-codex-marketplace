---
name: drupal-development
description: "Use when implementing Drupal modules, services, entities, routes, forms, queues, caching, or updates."
---

# Drupal Development

## When to invoke

Use when implementing Drupal modules, services, entities, routes, forms, queues, caching, or updates. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Drupal/PHP/contrib versions, extension points, configuration/schema, access rules, cacheability and test setup. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace the module behavior and choose the supported entity/service/plugin/hook boundary.
2. Implement access-aware data operations, dependency injection, render/cache metadata, and validated forms/configuration.
3. Run appropriate coding/static and kernel/functional checks, including permissions, cache variation, and update behavior.

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
