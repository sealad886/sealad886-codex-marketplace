---
name: trpc
description: "Use when implementing tRPC procedures, input validators, auth context, transport links, errors, or React/query integration."
---

# tRPC typed procedures

## When to invoke

Use when implementing tRPC procedures, input validators, auth context, transport links, errors, or React/query integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect tRPC/TypeScript/client integration versions, adapters, context creation, validators, transformers, and procedure access rules.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define runtime-validated inputs and authenticated resource ownership for each procedure.
2. Implement version-correct router/transport/client boundaries with type-only server imports.
3. Test invalid, unauthorized, serialization, and success/failure paths through the actual adapter.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run router/adapter tests for invalid input, cross-user access, batches, errors, and transformed responses plus type checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
