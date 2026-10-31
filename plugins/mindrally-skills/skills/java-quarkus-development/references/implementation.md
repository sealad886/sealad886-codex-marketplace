# Java Quarkus Development Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Configuration and application code

- Use ConfigMapping for related typed settings and validate required values; keep secrets outside tracked configuration.
- Quarkus REST is the current name of the RESTEasy Reactive lineage; align extension names to the installed BOM.
- Choose Hibernate ORM/Panache or reactive clients according to the execution model; blocking ORM must not run on an event-loop thread.

## Testing and operations

- @QuarkusTest exercises the application test mode; @QuarkusIntegrationTest exercises a built artifact, which can be JVM, native, or container.
- Native-image reflection/resource requirements need their own tests; Dev Services may start containers and need available local resources.
- Use current Micrometer/OpenTelemetry integrations instead of prescribing retired MicroProfile Metrics or OpenTracing extensions.
- Separate liveness from dependency readiness and measure startup/RSS before claiming native-image benefits.

## Primary documentation

- [Quarkus OpenTelemetry](https://quarkus.io/guides/opentelemetry/) — Current OpenTelemetry extensions and migration from OpenTracing are documented.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
