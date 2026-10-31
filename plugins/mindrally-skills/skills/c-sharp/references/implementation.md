# C# Development Guidelines: implementation guidance

## Language and ownership

Follow .editorconfig/project conventions; .NET conventions generally use PascalCase
for constants rather than SCREAMING_SNAKE_CASE. Records are not automatically deeply
immutable: referenced objects can still mutate. Enable and honor nullable analysis
without using suppression to hide defects. Use IDisposable/IAsyncDisposable for
owned resources and correct DI lifetimes. Do not inject scoped dependencies into
a singleton without a deliberate scope. Match new syntax to the compiler/runtime;
Unity supports a subset/version that may differ from a current ASP.NET project.

## Async, performance, and hosts

Use async I/O with propagated cancellation; avoid sync-over-async deadlocks and
unobserved tasks. LINQ, Span/Memory, StringBuilder, caches, and pooling are measured
choices, not universal optimizations. Ordinary ORM use does not make interpolated
raw SQL safe: use parameterized APIs and authorization at the data boundary.
Blazor state must follow render mode/circuit lifetimes; client UI checks are not
server authorization. Unity MonoBehaviour/ScriptableObject lifecycle and coroutines
are host concepts; coroutines do not automatically create background threads.
Choose the existing test framework and prove behavior instead of a coverage target.

## Primary documentation

- [C# identifier and constant conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names).
- [Record mutability semantics](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
