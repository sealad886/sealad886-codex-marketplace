# LangChain Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## APIs and state

- For LangChain v1, create_agent is the standard agent interface; older AgentExecutor/create_react_agent and memory recipes require their matching legacy generation.
- Use runnable invoke/batch/stream or async variants supported by the component; bind_tools is the model-facing convenience when available, not an assumption that bind alone converts definitions.
- Use message-aware reducers and checkpoint/thread IDs for state; simple list concatenation is not a complete persisted message update strategy.

## Tools, retrieval and observability

- Validate tools at the boundary and enforce authorization outside model instructions; set execution, token, concurrency, and retry limits.
- Evaluate chunking, filtering, retrieval and reranking with known questions; advanced retrieval is optional until it improves evidence.
- Keep tenant identities in checkpoint/cache/vector filters and protect document metadata.
- Tracing can send prompts and outputs to LangSmith; enable only with approved destination and redaction/retention rules.

## Primary documentation

- [Primary documentation](https://docs.langchain.com/oss/python/releases/langchain-v1) — LangChain v1 introduces create_agent and moves legacy functionality to langchain-classic.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
