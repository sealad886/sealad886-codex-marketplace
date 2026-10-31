---
name: machine-learning
description: "Use when developing JAX-based machine-learning models, functional training state, automatic differentiation, or device-efficient training."
---

# Machine Learning

## When to invoke

Use for developing JAX-based machine-learning models, functional training state, automatic differentiation, or device-efficient training.

## Inputs and evidence

Inspect dataset splits/provenance, JAX/backend versions, model state, PRNG keys, objective/metrics, shapes, dtypes and resource budget. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define task-specific baseline and held-out evaluation before tuning the model.
2. Implement explicit parameters/optimizer/state/random keys in pure training and evaluation functions.
3. Select JAX transformations and control flow based on traced values and measured bottlenecks.
4. Validate gradients, reproducibility, numerical stability and held-out task behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Training and evaluation checks establish correct gradients/state, reproducibility and held-out behavior within budget.

## Must not

Do not equate lower training loss or JIT compilation with validated model quality/performance. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
