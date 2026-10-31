---
name: nlp-natural-language-processing
description: "Use when building NLP preprocessing, tokenization, classification, entity extraction, embeddings, or generation pipelines."
---

# Natural Language Processing (NLP) Development

## When to invoke

Use for building NLP preprocessing, tokenization, classification, entity extraction, embeddings, or generation pipelines.

## Inputs and evidence

Inspect task/data provenance, language/domain, model/tokenizer revisions, label schema, length limits, backend and evaluation splits. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define task/label semantics and leak-resistant train/validation/test data.
2. Preserve text information unless a measured task need justifies normalization/cleaning.
3. Use model-matched tokenization/masks and task-specific training/inference settings.
4. Evaluate held-out quality, language/subgroup failures, latency and input/output edge cases.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Held-out task evaluation, preprocessing/span invariants and backend performance checks support the claimed behavior.

## Must not

Do not let preprocessing leak test information or silently destroy task-relevant text. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
