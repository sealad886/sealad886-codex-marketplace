---
name: deep-learning-python
description: "Use when integrating PyTorch training, Transformer/diffusion models, or bounded inference demos."
---

# Deep Learning Python Development

## When to invoke

Use when integrating PyTorch training, Transformer/diffusion models, or bounded inference demos. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect dataset/split provenance, model/weights/license, tensor shapes/dtypes, actual backend, package versions, metric, and compute budget. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Establish a baseline, leakage-safe splits, task metrics, and reproducible configuration before training changes.
2. Implement model/data/training or inference boundaries with correct modes, gradients, optimizer state, and device-aware precision.
3. Check finite losses/gradients, held-out quality, reproducibility limits, checkpoint resume, memory, and measured latency/throughput.

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
