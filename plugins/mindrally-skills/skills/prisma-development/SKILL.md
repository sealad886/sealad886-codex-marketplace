---
name: prisma-development
description: "Use when evolving Prisma schemas, migrations, generated TypeScript clients, data access boundaries, or persistence tests."
---

# Prisma ORM Development

## When to invoke

Use for evolving Prisma schemas, migrations, generated TypeScript clients, data access boundaries, or persistence tests.

## Inputs and evidence

Inspect Prisma major/generator, database provider, migration state/history, generated paths, adapter/runtime and schema ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Design schema and migration effects around required invariants and data conversion.
2. Generate the matching client and update typed callers with runtime validation.
3. Use supported transactions and query instrumentation without hiding authorization.
4. Validate migrations and behavior on the real provider in an isolated database.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Client generation and isolated provider migrations/tests demonstrate intended schema/data evolution and query contracts.

## Must not

Do not run production migration/reset commands or expose raw database credentials from skill invocation. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
