# LLM Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Training and data

- Use the exact tokenizer/chat template and special-token policy for the model; padding/truncation/loss masks must match the training objective.
- LoRA, prefix tuning and full tuning have different parameter/memory tradeoffs; do not stack them or distributed frameworks without need.
- Mixed precision, accumulation, activation checkpointing and sharding depend on backend support and numerical behavior.
- Record data permissions/provenance, split before leakage-prone preprocessing, and version configuration/checkpoints.

## Evaluation and serving

- Perplexity and BLEU measure limited aspects and do not establish instruction quality, factuality, fairness or product usefulness.
- Use held-out task evaluations, relevant demographic/safety slices and human review where required; report uncertainty and failure examples.
- Serving needs bounded context/output, batching, cancellation and memory behavior; quantization benefits require quality/performance comparisons.
- Keep model downloads, compute jobs and external deployment inside the user-approved budget and destination.

## Primary documentation

- [Primary documentation](https://huggingface.co/docs/transformers/en/llm_tutorial) — Text generation depends on model/tokenizer setup, decoding configuration and resource constraints.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
