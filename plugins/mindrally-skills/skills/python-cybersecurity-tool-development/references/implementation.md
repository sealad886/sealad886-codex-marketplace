# Python Cybersecurity Tool Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Scope and secure execution

- Do not add attacker/bruteforce/exploit modules as a default project structure; implement only the authorized capability.
- Prefer subprocess argument vectors with shell disabled and validate option/path boundaries; generic string sanitization is not shell escaping.
- Use supported TLS verification and credential stores; do not log request headers, command secrets or sensitive target configuration.

## Concurrency and evidence

- Async scanning requires actual non-blocking APIs, bounded concurrency/timeouts and cancellation-safe connection/session cleanup.
- Protocol libraries such as Scapy, Nmap wrappers and SSH clients have distinct privilege/external process requirements; add only necessary pinned dependencies.
- Cache DNS/vulnerability results with freshness and scope metadata; stale findings are not current vulnerabilities.
- Report evidence, false-positive limits and incomplete targets separately; scan completion time alone is not a security quality metric.

## Primary documentation

- [Primary documentation](https://docs.python.org/3/library/subprocess.html) — subprocess argument-vector and shell/security behavior governs safe external process invocation.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
