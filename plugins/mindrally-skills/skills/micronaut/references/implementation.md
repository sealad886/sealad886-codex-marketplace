# Micronaut: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Compile-time infrastructure

- Use the platform BOM and required annotation processors; compile-time DI is not the same as a native executable or optional AOT optimization.
- Prefer constructor injection and ConfigurationProperties for grouped validated configuration; scalar Value injection is a different capability.
- Match Java/Jakarta annotations and data/serialization modules to installed versions.

## Execution and delivery

- Reactive return types do not make blocking libraries non-blocking; select ExecuteOn or supported executors according to the actual workload.
- Use Micronaut Data JPA/JDBC/reactive access intentionally and test database rollback and migrations.
- Use Security authorization alongside JWT/OIDC authentication; keep management endpoints and logs appropriately protected.
- Native-image startup/memory benefits require measured artifact-specific evidence and reflection/resource support tests.

## Primary documentation

- [Primary documentation](https://docs.micronaut.io/5.2.x/core/) — Micronaut documents compile-time DI, configuration and explicit execution/threading facilities.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
