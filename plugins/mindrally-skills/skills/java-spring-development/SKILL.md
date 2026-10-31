---
name: java-spring-development
description: "Use when implementing Spring Boot services, dependency injection, web contracts, persistence, security, or asynchronous work."
---

# Java Spring Development Best Practices

## When to invoke

Use for Java Spring applications with their configured Boot/Framework generation.

## Inputs and evidence

Inspect the Spring BOM, Java target, MVC versus WebFlux stack, persistence model, security configuration, and executor policies. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Implement the requested behavior within existing domain and dependency boundaries.
2. Use explicit validation, error mapping, authentication, and resource authorization.
3. Bound transactions and async/executor ownership; avoid blocking work on reactive event loops.
4. Run focused unit, web/security, and database tests for affected contracts.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests establish web status/error behavior, access control, transaction outcomes, and async failure/cleanup behavior where applicable.

## Must not

Do not call @Async inherently non-blocking or impose a microservice, Lombok, or framework upgrade without task need. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
