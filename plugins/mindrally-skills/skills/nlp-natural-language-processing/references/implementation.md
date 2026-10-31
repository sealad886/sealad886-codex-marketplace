# Natural Language Processing (NLP) Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Text and model compatibility

- Do not remove special characters, punctuation or stopwords automatically; they can encode meaning, negation, entities or code.
- Use the pretrained model’s actual tokenizer/special tokens, not a universal CLS/SEP list; align padding/truncation and attention/loss masks.
- Offsets and entity spans must map back to original text after normalization; nested/overlapping NER needs a representation the chosen model supports.

## Evaluation and deployment

- Choose F1/precision/recall/AUC or generation metrics according to task and class imbalance; fluent text is not factuality evidence.
- Use embedding pooling/normalization and distance metrics matching the selected model; evaluate retrieval on known queries.
- Quantization, ONNX, batching and distillation are optional measured paths with backend/quality constraints.
- Validate empty/long/malformed/multilingual inputs, privacy-sensitive data handling and model output contracts.

## Primary documentation

- [Primary documentation](https://huggingface.co/docs/transformers/en/main_classes/tokenizer) — Tokenizer special tokens, padding, truncation and offsets are model/API-dependent.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
