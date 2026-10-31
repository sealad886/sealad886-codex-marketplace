---
name: serverless
description: "Use when adapting functions or APIs to serverless event sources, retries, cold starts, quotas, or managed service boundaries."
---

# Serverless execution contracts

## When to invoke

Use when adapting functions or APIs to serverless event sources, retries, cold starts, quotas, or managed service boundaries.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect cloud/runtime versions, event source delivery, function limits, IAM, concurrency, database connections, and cost constraints.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define invocation, duplicate delivery, timeout, and state ownership contracts.
2. Implement the smallest provider-supported handler/adapter and bounded downstream work.
3. Test retry/idempotency and failure behavior, then measure cold/warm execution where authorized.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run handler/contract tests for duplicate events, timeout, partial failure, and missing configuration; identify omitted live-cloud/cost tests.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
