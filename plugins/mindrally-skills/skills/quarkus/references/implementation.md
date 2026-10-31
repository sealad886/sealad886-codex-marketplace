# Quarkus: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Framework and execution

- ApplicationScoped/Inject are CDI/Jakarta and ConfigProperty is MicroProfile, not all Quarkus-specific annotations.
- Java language and extension requirements follow the selected platform BOM, not a fixed Java17 baseline.
- Use blocking ORM and reactive clients according to thread/executor constraints; a Uni wrapper does not make blocking calls safe on the event loop.

## Observability and delivery

- Current Micrometer/OpenTelemetry integrations supersede prescribing legacy MicroProfile Metrics/OpenTracing extensions.
- Separate liveness/readiness and protect management endpoints; export only authorized redacted telemetry.
- Native-image reflection/resources and startup/memory benefits require actual artifact tests/measurements, not configuration alone.
- In-memory test databases may differ from production SQL/locking behavior; use the actual provider where semantics matter.

## Primary documentation

- [Primary documentation](https://quarkus.io/guides/opentelemetry/) — Current Quarkus documents OpenTelemetry/Micrometer integration and migration from OpenTracing.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
