---
name: analytics-data-analysis
description: "Use when performing exploratory data analysis, cleaning datasets, creating statistical plots, or building reproducible analytics notebooks."
---

# Analytics and Data Analysis

## When to invoke

Use when performing exploratory data analysis, cleaning datasets, creating statistical plots, or building reproducible analytics notebooks. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect data provenance and schema, units, population, missingness, privacy constraints, analysis question, and environment. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define metrics and inspect types, row counts, missingness, duplicates, and collection bias before transformation.
2. Apply justified cleaning and analysis with explicit selection and join semantics; preserve a reproducible data lineage.
3. Visualize the relevant comparisons and report uncertainty, assumptions, exclusions, and reproducibility checks.

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
