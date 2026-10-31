# Monitoring Guidelines: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Signals and alerts

- Latency, traffic, errors and saturation are useful starting signals, not a requirement to instrument every business metric.
- Use burn-rate/multi-window alerts when SLO traffic and operational needs support them; low-volume services need deliberate treatment.
- Page for actionable user impact and route diagnostic/capacity warnings appropriately; fixed quarterly reviews are not universal.

## Probes and telemetry reliability

- Readiness controls traffic and liveness checks whether restart helps; dependency checks in liveness can amplify outages.
- Bound metric cardinality, scrape/storage cost and retention; do not put user/request IDs into metric labels.
- Treat absent/stale metrics explicitly and monitor the alerting pipeline itself.
- Validate dashboards against known events and annotate revisions without assuming correlation proves cause.

## Primary documentation

- [Primary documentation](https://sre.google/workbook/alerting-on-slos/) — SLO alert design balances precision, recall, detection/reset time and multi-window burn rates.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
