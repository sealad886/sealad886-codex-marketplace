# Java: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Language and design

- Records, sealed classes, pattern matching, and preview features have distinct release requirements; consult the actual source/target configuration.
- Prefer clear ownership and immutable values where appropriate; use constructor injection when the selected container supports it.
- Preserve domain validation, nullability and exception contracts across API boundaries; choose DTOs where a separate external representation is useful.

## Runtime and frameworks

- Use Maven/Gradle wrappers and pinned dependencies; avoid adding competing framework stacks.
- Virtual threads, reactive libraries, and executor pools serve different workloads; measure blocking/concurrency behavior before selecting one.
- For persistence, bound transactions, inspect query plans/N+1 behavior, and use established migrations.
- Use JUnit and integration facilities already configured; benchmark or profile before caching or connection-pool changes.

## Primary documentation

- [Java language updates](https://docs.oracle.com/en/java/javase/25/language/index.html) — Language features have documented release-specific availability.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
