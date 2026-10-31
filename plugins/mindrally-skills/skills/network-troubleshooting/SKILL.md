---
name: network-troubleshooting
description: "Use when diagnosing target-scoped developer DNS, TCP, TLS, proxy, HTTP, or registry connectivity failures."
---

# Network Troubleshooting

## When to invoke

Use for diagnosing target-scoped developer DNS, TCP, TLS, proxy, HTTP, or registry connectivity failures.

## Inputs and evidence

Inspect sanitized failing command/error, exact authorized target/port, operating system, client version, and known proxy/VPN context. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Classify the symptom without treating it as a proven root cause.
2. Run the smallest bounded read-only DNS/TCP/TLS/HTTP check on the failing target.
3. Interpret results and identify a concrete remediation with effects and required authority.
4. After an authorized repair, repeat the original operation or an equivalent scoped check.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Results tie a supported diagnosis and scoped repair to successful rerun evidence, with secrets redacted.

## Must not

Do not dump configuration or bypass certificate verification to make a connectivity check appear successful. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
