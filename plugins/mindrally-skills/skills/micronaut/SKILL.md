---
name: micronaut
description: "Use when developing Micronaut dependency injection, HTTP services, configuration, data/security integrations, or native builds."
---

# Micronaut

## When to invoke

Use for developing Micronaut dependency injection, HTTP services, configuration, data/security integrations, or native builds.

## Inputs and evidence

Inspect Micronaut BOM/runtime generation, Java target, annotation processing, HTTP execution model, integrations, and artifact targets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend compile-time DI and typed configuration using the installed framework generation.
2. Implement validated/authorized endpoints and explicit persistence/transaction boundaries.
3. Keep blocking work on a supported executor and configure observability through selected integrations.
4. Run framework integration tests and separately verify native/container artifacts when claimed.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Configured builds and integration tests establish DI/configuration, auth, persistence and thread behavior; native claims are separately checked.

## Must not

Do not assume a reactive wrapper or compile-time DI proves non-blocking execution or native compatibility. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
