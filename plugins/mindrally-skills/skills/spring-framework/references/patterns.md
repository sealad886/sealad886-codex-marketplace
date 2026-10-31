# Spring Framework container and services: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Spring Framework does not require Spring Boot starters, Actuator, application.yml, or Boot test slices; apply those only in Boot applications.

- Use constructor injection for required dependencies and explicit qualifiers where multiple beans match; avoid unnecessary interfaces solely for injection.

- Bean scopes and lifecycle affect resource/state ownership; singleton does not mean thread-safe.

- AOP proxy-based transactions/caching/async depend on calls passing through the proxy; self-invocation can bypass advice.

- @Async moves execution to an executor rather than converting blocking APIs to nonblocking IO; bound queues, threads, and shutdown.

- Choose MVC versus WebFlux from the existing application and dependencies; blocking persistence in a reactive path needs explicit handling.

- Use the configured transaction manager and error semantics; validate authorization and persistence constraints at appropriate boundaries.

- Use current Framework docs for the installed major and test context configuration directly when Boot is absent.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Task execution and proxy interception define @Async behavior.](https://docs.spring.io/spring-framework/reference/integration/scheduling.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
