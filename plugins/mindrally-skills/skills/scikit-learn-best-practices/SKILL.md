---
name: scikit-learn-best-practices
description: "Use when building scikit-learn preprocessing pipelines, model selection, evaluation, or persisted estimators."
---

# Scikit-learn model workflows

## When to invoke

Use when building scikit-learn preprocessing pipelines, model selection, evaluation, or persisted estimators.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect dataset units/groups/time, target leakage risks, sklearn version, baseline, metrics, split policy, and compute budget.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define the deployment question and a leakage-resistant split before fitting transforms.
2. Fit preprocessing and estimator together within training/CV boundaries.
3. Evaluate frozen choices on held-out data and record reproducibility, uncertainty, and artifact limits.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run small leakage/split/schema checks and the planned evaluation; report dataset scope, seeds, environment, and unperformed deployment acceptance.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
