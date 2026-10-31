# General Best Practices: implementation guidance

## Code, architecture and tests

Use clear names and cohesive functions rather than fixed line counts. Introduce
interfaces/layers/DI only for real boundaries or present reuse, and preserve local
conventions. Define expected failures and propagate useful safe errors without
duplicate logging. Tests should prove requirements, invariants and regressions;
choose unit/integration/end-to-end layers by the behavior and avoid testing private
layout or merely maximizing coverage. Isolate fixtures and clean only resources
owned by the test. A passing mocked test is not external integration evidence.

## Security, performance and operations

Validate external inputs and use contextual encoding/parameterized queries rather
than a generic sanitize-everything claim. Authenticate then authorize the resource
and action; protect sessions/secrets and redact private identifiers/content in logs.
Retries, rate limits, circuit breakers, caches and pools require bounded policies,
correct ownership and measured need. Cache keys include relevant user/tenant/data
versions and freshness/invalidation rules. Collect useful latency/error/throughput
signals without automatically adding telemetry services or alerts. Follow actual
branch/commit/review policy; this skill does not grant commits, releases, repository
settings or unrelated cleanup. Report static, runtime and human acceptance separately.

## Primary documentation

- [Behavior, tests, design and complexity review](https://google.github.io/eng-practices/review/reviewer/looking-for.html).
- [Application trust and authorization concerns](https://owasp.org/www-project-top-ten/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
