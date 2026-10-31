---
name: koa-typescript
description: "Use when implementing typed Koa middleware, routing, validation, authentication, or API tests."
---

# Koa TypeScript Development

## When to invoke

Use for implementing typed Koa middleware, routing, validation, authentication, or API tests.

## Inputs and evidence

Inspect Koa/Node versions, router/body-parser dependencies, middleware order, context state types, and error/authentication policy. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Place error handling around downstream middleware and define typed request state.
2. Implement routes and body/query/path validation through maintained project dependencies.
3. Use awaited middleware composition and explicit authorization/error responses.
4. Test the composed app callback, denied requests, validation, and cleanup.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Type checking and composed HTTP tests demonstrate middleware order, validation, status/error mapping, and authorization.

## Must not

Do not call downstream next without awaiting/returning it or expose internal errors. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
