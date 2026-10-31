---
name: automl-hyperparameter-optimization
description: "Use when designing or running bounded AutoML and hyperparameter searches with Optuna, Ray Tune, PyCaret, or forecasting tools."
---

# AutoML and Hyperparameter Optimization

## When to invoke

Use when designing or running bounded AutoML and hyperparameter searches with Optuna, Ray Tune, PyCaret, or forecasting tools. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target metric, baseline, data/split provenance, leakage risks, training loop, compute budget, and package versions. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Fix the evaluation metric, split strategy, untouched test data, and baseline before defining the search.
2. Fit preprocessing inside folds and run a domain-informed conditional search with trial, time, and resource bounds.
3. Refit the selected configuration and report baseline comparison, uncertainty, search cost, and untouched evaluation.

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
