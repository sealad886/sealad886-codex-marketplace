# Logging Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Records and correlation

- Choose a machine-readable schema compatible with the collector; JSON is useful but not the only valid log representation.
- Timestamp, severity, body and resource identity should be deliberate; trace/span/request IDs are optional when no such context exists.
- Keep severity semantics consistent with the chosen logging ecosystem and attach exceptions once at the owning boundary.

## Privacy and reliability

- Avoid tokens, passwords and unnecessary personal identifiers; pseudonymous identifiers can still be sensitive and need access/retention controls.
- Sanitize line breaks/control data and avoid logging entire requests/responses by default.
- Async logging needs bounded queues and documented loss/blocking policy; security/audit events may require different durability from debug sampling.
- Test redaction and sink failures and measure overhead; full stack/request context must not override privacy or volume limits.

## Primary documentation

- [Primary documentation](https://opentelemetry.io/docs/specs/otel/logs/data-model/) — OpenTelemetry log records have optional trace/span context and structured severity/body/resource fields.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
