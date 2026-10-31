---
name: llm
description: "Use when developing language-model training, parameter-efficient adaptation, evaluation, tokenization, or inference serving."
---

# LLM Development

## When to invoke

Use for developing language-model training, parameter-efficient adaptation, evaluation, tokenization, or inference serving.

## Inputs and evidence

Inspect model/tokenizer licenses and revisions, task/data provenance, backend capability, memory budget, evaluation splits, and serving constraints. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define task metrics, baselines, held-out data and acceptable resource use.
2. Choose full or parameter-efficient adaptation based on evidence and supported backend.
3. Implement reproducible tokenization, training/checkpoints, and bounded inference configuration.
4. Evaluate quality, leakage, safety/robustness and deployment performance separately.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Reproducible training/evaluation and backend-specific serving evidence support each claimed quality/resource outcome.

## Must not

Do not infer model quality from loss alone or launch expensive training/downloads without authority. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
