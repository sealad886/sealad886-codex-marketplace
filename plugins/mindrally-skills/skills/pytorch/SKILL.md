---
name: pytorch
description: "Use when developing PyTorch modules, training/evaluation, autograd, mixed precision, data loading, or device-aware inference."
---

# PyTorch Development

## When to invoke

Use for developing PyTorch modules, training/evaluation, autograd, mixed precision, data loading, or device-aware inference.

## Inputs and evidence

Inspect PyTorch/backend versions, CPU/CUDA/MPS capabilities, model/data revisions, tensor shapes/dtypes, resource budget and evaluation requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define model/loss/data and held-out evaluation contracts with owned random state.
2. Implement modules/parameters/buffers and correct gradient/training-state behavior.
3. Choose supported device precision/distribution and optimize measured bottlenecks.
4. Test numerical/gradient/checkpoint behavior and evaluate quality/performance separately.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Numerical/gradient/training-resume and target-backend tests pass; task quality and performance have separate evidence.

## Must not

Do not infer correct inference from no_grad alone or launch large model/download/training work without authority. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
