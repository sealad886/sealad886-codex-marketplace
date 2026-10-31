# API Development: implementation guidance

## Go HTTP boundary

Use `http.NewServeMux` patterns supported by the installed Go toolchain; method
and wildcard patterns require Go 1.22 or later. Apply request-body size limits,
strict decoding where the contract requires it, and request contexts/timeouts.
Close bodies and resources; return an error before writing a second response.
Use appropriate status codes without exposing internal errors.

## NestJS boundary

Keep controllers thin and domain work in services. DTO decorators only validate
when a ValidationPipe is configured; choose transform, whitelist, and rejection
behavior deliberately. TypeScript types alone do not validate runtime JSON.
Use guards for authentication and authorization, filters for safe errors, and
interceptors for suitable cross-cutting concerns. Do not add a generic CommonModule
or barrel exports solely to satisfy a template. Validate inputs and use parameterized
queries; generic sanitization is not a substitute for context-specific injection
prevention. Install or upgrade dependencies only when required by the task.

## Primary documentation

- [ServeMux routing and MaxBytesReader](https://pkg.go.dev/net/http).
- [ValidationPipe runtime validation](https://docs.nestjs.com/techniques/validation).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
