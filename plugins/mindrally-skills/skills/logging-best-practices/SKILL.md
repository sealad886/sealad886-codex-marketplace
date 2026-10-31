---
name: logging-best-practices
description: "Use when designing structured application logs, severity, trace correlation, redaction, retention, or logging reliability."
---

# Logging Best Practices

## When to invoke

Use for designing structured application logs, severity, trace correlation, redaction, retention, or logging reliability.

## Inputs and evidence

Inspect logging library/output contracts, execution environment, sensitive fields, trace context, ingestion limits and retention/access policy. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define useful events and minimal structured fields at meaningful boundaries.
2. Propagate request/trace context only where present and sanitize untrusted values.
3. Configure redaction, severity, buffering/backpressure and retention for the environment.
4. Test useful failure records, secret absence, correlation and sink-unavailable behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Synthetic logs remain useful and parseable without secrets, and failure/load checks establish the chosen delivery policy.

## Must not

Do not log sensitive identifiers merely because they aid correlation. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
