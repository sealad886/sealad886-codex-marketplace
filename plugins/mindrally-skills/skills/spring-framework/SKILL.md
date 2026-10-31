---
name: spring-framework
description: "Use when implementing Spring dependency injection, bean lifecycle, web handling, transactions, scheduling, or framework integration."
---

# Spring Framework container and services

## When to invoke

Use when implementing Spring dependency injection, bean lifecycle, web handling, transactions, scheduling, or framework integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Spring/Java versions, bean configuration, proxy boundaries, web stack, transaction manager, and supporting Boot usage if any.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Separate core Spring behavior from optional Boot auto-configuration.
2. Implement clear bean/service boundaries using installed framework APIs.
3. Test lifecycle, validation, transaction, and web/concurrency behavior at real invocation boundaries.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run focused container/service/web tests including actual proxy boundaries and failure propagation; report missing deployment/runtime coverage.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
