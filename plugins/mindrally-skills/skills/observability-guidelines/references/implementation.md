# Observability Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Instrumentation and signals

- otel.Tracer/otel.Meter are not universal cross-language call syntax; use the installed language API and instrumentations.
- Avoid duplicate automatic/manual spans and use stable low-cardinality metric labels; user IDs generally do not belong in metric dimensions.
- Trace/span IDs are relevant when context exists; validate untrusted propagation and avoid exporting credentials/personal payloads.

## Sampling and operations

- Head sampling decides early and can discard traces later needed for error analysis; tail sampling cannot recover spans never recorded/exported upstream.
- Tail sampling needs state, capacity and coherent routing of spans for each trace; it is not a free switch guaranteeing every error.
- Choose retention/queues/drop policy from diagnostic and privacy needs, and monitor the telemetry pipeline itself.
- SLO dashboards and runbooks should link observed impact to action; a specific clean architecture is not required for observability.

## Primary documentation

- [Primary documentation](https://opentelemetry.io/docs/concepts/sampling/) — Head/tail sampling have different decision timing, retained evidence and operational costs.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
