---
name: fastify-typescript
description: "Use when implementing Fastify routes, schemas, plugins/decorators, database integrations, or request tests."
---

# Fastify TypeScript Development

## When to invoke

Use when implementing Fastify routes, schemas, plugins/decorators, database integrations, or request tests. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Fastify/Node/schema-provider versions, encapsulation tree, typed decorators, route schemas, hooks, and authorization. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define request/response schemas and trace plugin visibility, lifecycle and authentication hooks.
2. Implement validated handlers and response serialization with explicit database/resource cleanup and safe errors.
3. Use inject and relevant live integration tests for invalid input, access, serialization, plugin readiness and shutdown.

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
