---
name: data-jupyter-python
description: "Use when implementing reusable Python data transformations and Jupyter analysis workflows."
---

# Data Analysis and Jupyter Python Development

## When to invoke

Use when implementing reusable Python data transformations and Jupyter analysis workflows. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect data provenance/schema/units, analysis question, missingness, joins, notebook kernel/environment, and intended outputs. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define the question and inspect types, ranges, missingness, duplicates, datetime zones, and sample composition.
2. Apply justified transformations and aggregation with explicit shape/index/grouping and missing-data policies.
3. Execute reproducibly and validate summaries/plots against sanity checks, assumptions, and source counts.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
