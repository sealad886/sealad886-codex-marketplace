# NestJS Clean TypeScript: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Architecture and types

- A module groups related providers/controllers; one module per route or one service per entity is not a framework requirement.
- Use the established ORM; MikroORM is optional, not a NestJS default.
- TypeScript readonly/as const constrain type-level mutation and do not provide deep runtime immutability.

## Validation and tests

- ValidationPipe/class-validator need concrete DTO classes and deliberate whitelist/transform settings; interfaces disappear at runtime.
- Guards handle authorization, pipes validate/transform inputs, filters map exceptions, and interceptors wrap execution; choose the right boundary.
- Prefer tests for requirements and failure contracts over fixed function/class instruction limits or every-public-method test counts.
- Use global modules/providers only when their lifecycle/scope justifies broad visibility.

## Primary documentation

- [Primary documentation](https://docs.nestjs.com/techniques/validation) — Nest validation depends on runtime DTO metadata and ValidationPipe configuration.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
