---
name: observability-guidelines
description: "Use when instrumenting distributed tracing, metrics, structured logs, context propagation, sampling, or telemetry pipelines."
---

# Observability Guidelines

## When to invoke

Use for instrumenting distributed tracing, metrics, structured logs, context propagation, sampling, or telemetry pipelines.

## Inputs and evidence

Inspect language SDK/collector versions, existing semantic conventions, telemetry destinations, data sensitivity, cardinality and sampling budgets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define user-impact questions and instrument meaningful service/dependency boundaries.
2. Propagate context and record useful bounded attributes using the language’s actual APIs.
3. Configure metrics/log correlation, sampling, redaction and exporter failure behavior.
4. Validate end-to-end traces/metrics/logs with controlled requests and missing/degraded collectors.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Controlled requests produce correlated expected signals without secrets, and exporter/sampling limits are demonstrated.

## Must not

Do not infer complete request coverage from sampled telemetry or expose payloads to unapproved collectors. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
