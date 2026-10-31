# Hugging Face Transformers workflows: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Pin model/tokenizer/config revisions and inspect trust_remote_code requirements; model repository code and serialized artifacts have trust implications.

- Use the correct AutoModel task class and AutoProcessor for multimodal inputs; AutoTokenizer alone does not cover every model.

- Token limits, special tokens, padding side, chat templates, and attention masks are model-specific; a universal 512-token example is not a safe default.

- Current Trainer arguments include eval_strategy and processing_class; older evaluation_strategy/tokenizer examples must match the installed release.

- Align save/evaluation strategy and selected metric when loading the best checkpoint.

- Use inference/eval context for the selected backend and move inputs consistently; MPS/CUDA/CPU dtype, attention, quantization, and LoRA support differ.

- bitsandbytes/Flash Attention/QLoRA are optional and not universally compatible or faster on all devices; benchmark memory and correctness.

- Reserve test data from tuning, evaluate distribution/task failure cases, and treat push_to_hub/downloads/billable training as separately scoped actions.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Current Trainer documents eval_strategy, checkpoint selection requirements, and versioned constructor fields.](https://huggingface.co/docs/transformers/en/main_classes/trainer)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
