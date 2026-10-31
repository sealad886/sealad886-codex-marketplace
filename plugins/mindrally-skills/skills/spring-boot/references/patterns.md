# Spring Boot application boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Boot and Java support requirements vary by major; do not impose Boot 3 or Java 17 examples on an incompatible project.

- Constructor injection and ConfigurationProperties binding are useful defaults; @Value is not equivalent to structured type-safe configuration binding.

- Autowired/Qualifier are Spring dependency-injection annotations, not Jakarta CDI annotations.

- @Async schedules work through a configured executor; it does not make blocking work nonblocking and default proxy mode does not intercept same-class calls.

- Transactional proxies have call-boundary limitations; test rollback and propagation rather than assuming annotations alone apply.

- Use Jakarta validation packages appropriate to the installed generation; request validation does not replace authorization or parameterized queries.

- Actuator endpoints require deliberate exposure and access control; adding the dependency does not make metrics safe to publish.

- Choose JPA, Testcontainers, cache, OpenAPI, and deployment tools from project needs; avoid mandatory dependency stacks.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Async annotations use executor/proxy interception and same-class calls are not intercepted.](https://docs.spring.io/spring-framework/reference/integration/scheduling.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
