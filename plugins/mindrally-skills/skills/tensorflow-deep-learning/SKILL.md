---
name: tensorflow-deep-learning
description: "Use when implementing TensorFlow/Keras input pipelines, training, evaluation, callbacks, or serving exports."
---

# TensorFlow and Keras model workflows

## When to invoke

Use when implementing TensorFlow/Keras input pipelines, training, evaluation, callbacks, or serving exports.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect TensorFlow/Keras/backend versions, device support, dataset splits, shapes/dtypes, metric selection, and compute budget.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Validate data/labels and leakage-resistant splits before training.
2. Run a small baseline with explicit precision and checkpoint selection.
3. Evaluate frozen choices and smoke-test the exact exported artifact with serving preprocessing.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run bounded shape/loss/finite-gradient checks, selected evaluation, and export reload/inference; report unperformed device or serving acceptance.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
