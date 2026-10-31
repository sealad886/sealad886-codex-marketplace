---
name: spring-boot
description: "Use when changing Spring Boot configuration, REST endpoints, persistence, security, async work, or application tests."
---

# Spring Boot application boundaries

## When to invoke

Use when changing Spring Boot configuration, REST endpoints, persistence, security, async work, or application tests.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Boot/Framework/Java versions, build dependencies, auto-configuration, active profiles, data/security configuration, and test slices.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify the owning endpoint/service/configuration boundary and installed-version constraints.
2. Implement validated configuration and authenticated/authorized behavior through existing Spring primitives.
3. Run focused slice tests and integration checks for affected transactions, scheduling, or HTTP behavior.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run build/type tests and relevant HTTP/configuration/data slice tests; check proxy-mediated behavior and exposed endpoints where affected.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
