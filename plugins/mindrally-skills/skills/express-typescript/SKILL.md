---
name: express-typescript
description: "Use when implementing Express TypeScript routers, middleware, validation, authentication, or error handling."
---

# Express TypeScript Development

## When to invoke

Use when implementing Express TypeScript routers, middleware, validation, authentication, or error handling. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Express/Node/Zod versions, route contracts, parser limits, proxy topology, auth policy, and dependency types. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define middleware order and request/body/query/parameter plus authorization contracts.
2. Implement version-correct async handling and consume validated/transformed data before domain side effects.
3. Type-check and test malformed/oversized input, denied ownership, async failures, headers-sent behavior, and safe responses.

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
