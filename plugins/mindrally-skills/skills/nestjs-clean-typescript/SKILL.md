---
name: nestjs-clean-typescript
description: "Use when developing typed NestJS modules, providers, DTO validation, guards, persistence, or API tests."
---

# NestJS Clean TypeScript

## When to invoke

Use for developing typed NestJS modules, providers, DTO validation, guards, persistence, or API tests.

## Inputs and evidence

Inspect Nest/TypeScript versions, modules/providers, validation transformation settings, auth guards, ORM and testing conventions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend feature/domain modules with cohesive provider interfaces.
2. Validate external DTOs and authorize requests at the owning boundary.
3. Keep controllers focused and implement transactions/errors through existing abstractions.
4. Test observable API behavior, denied inputs/roles, and dependency integration.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Type checks and module/API tests demonstrate runtime validation, authorization, error mapping and relevant persistence behavior.

## Must not

Do not assume TypeScript DTO interfaces validate runtime payloads. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
