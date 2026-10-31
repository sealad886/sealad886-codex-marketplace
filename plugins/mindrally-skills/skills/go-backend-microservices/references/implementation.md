# Go Backend Development for Microservices: implementation guidance

## HTTP, types and errors

Go 1.22 ServeMux supports method/host/path patterns and named wildcards, not arbitrary
regular-expression routing. Check the installed toolchain and actual pattern
conflicts/path escaping. Bound request bodies with MaxBytesReader, handle decode
failures and trailing input according to the contract, and validate query/path values.
Use context-aware clients, server timeouts, and consistent safe response/status
handling. Parameterize database values; generic input sanitization is insufficient.
Wrap errors with %w when preserving identity matters and use errors.Is/As rather
than text matching. Keep logging at the owning boundary to avoid duplicates.

## Concurrency, structure and telemetry

Propagate cancellation/deadlines to work; Context cancellation signals do not forcibly
stop every goroutine. Bound fan-out, close owned response bodies/resources, join
workers and coordinate graceful shutdown. Channels do not automatically prevent
races; use the appropriate mutex/channel/atomic invariant and exercise race tests.
Use small consumer-owned interfaces where needed; cmd/internal/pkg and layered
folders are choices, and pkg alone does not enforce public API semantics. Structured
slog and OpenTelemetry integrations need actual versions, redaction, sampling and
shutdown/flush ownership. Keep metric cardinality bounded and never trust remote
trace baggage as authorization. Parallel tests require isolated shared state.

## Primary documentation

- [ServeMux routing semantics](https://go.dev/src/net/http/server.go).
- [HTTP parsing/timeouts/context contracts](https://pkg.go.dev/net/http).
- [Race detector scope](https://go.dev/doc/articles/race_detector).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
