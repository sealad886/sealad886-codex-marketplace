---
name: transformers-huggingface
description: "Use when loading, adapting, training, generating with, or evaluating Hugging Face Transformers models and processors."
---

# Hugging Face Transformers workflows

## When to invoke

Use when loading, adapting, training, generating with, or evaluating Hugging Face Transformers models and processors.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Transformers/backend/device versions, model revision/card/license, task class, tokenizer/processor, dataset splits, and compute limits.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Select a task/model/processor combination supported by the installed stack.
2. Implement consistent preprocessing and bounded training/inference settings.
3. Validate outputs, memory, metrics, and saved-artifact reload before any authorized publication.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run small processor/model shape tests and bounded generation/evaluation plus artifact reload where resources permit; report full-model/device limits.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
