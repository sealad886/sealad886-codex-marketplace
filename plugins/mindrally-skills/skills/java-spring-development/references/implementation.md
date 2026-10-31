# Java Spring Development Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Architecture and persistence

- Match APIs to the installed Boot/Framework/Java versions; use constructor injection for required collaborators.
- Select MVC or WebFlux according to the existing stack and workload; reactive wrappers do not make blocking I/O non-blocking.
- Use DTOs, Bean Validation and consistent exception mapping; inspect JPA fetch plans and paginated query behavior.
- Migration edits depend on whether a migration has been applied/shared; preserve immutable applied history.

## Async, security, and operations

- @Async submits method execution to an executor; it does not remove blocking inside the method. Proxy/self-invocation rules and exception handling matter.
- Bound executor/queue capacity and define rejection/cancellation behavior; test failures returned through Future/CompletableFuture.
- Use the configured password encoder and server authorization policy; CORS does not replace access control or CSRF defenses.
- Measure caching and Actuator exposure; protect management endpoints and redact sensitive logs.

## Primary documentation

- [Spring scheduling](https://docs.spring.io/spring-framework/reference/integration/scheduling.html) — @Async executes work through TaskExecutor and supports Future/CompletableFuture results.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
