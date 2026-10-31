# Network Troubleshooting: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Diagnosis and interpretation

- Connection refusal suggests no listener or an active reject; timeouts/reset/DNS errors each have multiple possible network/client causes.
- HTTP 403 is a server/policy authorization response; browser CORS enforcement is not a general explanation for CLI failures.
- Ping failure does not prove HTTP is unreachable, because ICMP may be blocked; HEAD behavior may differ from GET.
- A successful openssl s_client handshake alone is not full hostname/chain verification; use supported verification options and inspect return status.

## Sensitive output and changes

- Avoid verbose curl traces and raw proxy/package-manager configuration output by default; they can expose headers, tokens and internal addresses.
- Use bounded timeouts and sanitized status/timing output; do not probe unrelated hosts or broaden scans without authority.
- Keep normal certificate verification enabled and identify the actual trust/certificate problem.
- Changes to DNS/proxy/VPN/trust stores or global tools require the appropriate explicit user authorization; existing authorization should not be repeatedly requested.

## Primary documentation

- [Primary documentation](https://curl.se/docs/manpage.html) — curl documents timeout, TLS verification, write-out and verbose-output behavior.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
