---
name: monitoring-guidelines
description: "Use when defining service metrics, SLOs, actionable alerts, dashboards, probes, or capacity signals."
---

# Monitoring Guidelines

## When to invoke

Use for defining service metrics, SLOs, actionable alerts, dashboards, probes, or capacity signals.

## Inputs and evidence

Inspect critical user journeys, existing SLIs/SLOs, metrics labels, alert ownership, baseline traffic and observability costs. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define success/latency indicators and denominator/window semantics for critical journeys.
2. Collect bounded-cardinality metrics with relevant resource and failure signals.
3. Design actionable alerts, routing, runbooks and dashboard drill-downs.
4. Test alert expressions, missing-data behavior, notification routing and monitoring failure.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Alert/query tests and controlled signal checks establish expected routing and behavior under missing data and failures.

## Must not

Do not page on every threshold or claim monitoring coverage from dashboard presence alone. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
