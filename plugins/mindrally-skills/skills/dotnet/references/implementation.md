# .NET Development Guidelines: implementation guidance

## Async and persistence

Use Task by default for asynchronous APIs; ValueTask is an optimization for specific
measured allocation/completion patterns, with consumption restrictions. Propagate
CancellationToken and avoid Result/Wait. DbContext is not thread-safe; do not run
parallel operations on one instance. Project only needed columns, choose tracking
behavior deliberately, bound pagination and use stable ordering. A repository
wrapper and Clean Architecture projects are optional, not required over EF Core.
Migrations and transaction/concurrency handling must preserve actual data invariants.

## Validation, authorization, and testing

Choose existing validators and return safe, useful errors; annotations/types alone
do not guarantee every entry point is validated. Match authentication/session/token
choices to the application rather than mandating JWT everywhere. Enforce resource
policies server-side and isolate caches by user/tenant. Avoid captive scoped services
in singleton DI. EF InMemory is not a relational database replacement: provider
translation, constraints, transactions and SQL need tests against an appropriate
real provider. WebApplicationFactory tests have an explicit server/config scope.
OpenAPI generation and documentation tooling depend on the target .NET version.

## Primary documentation

- [Real provider versus test-double limits](https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy).
- [ValueTask use and consumption restrictions](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
