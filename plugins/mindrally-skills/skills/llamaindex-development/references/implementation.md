# LlamaIndex Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Indexing and retrieval

- LlamaIndex core and reader/model/vector integrations may require separate packages; inspect actual imports before adding dependencies.
- Chunk size, overlap, semantic splitting, similarity thresholds and reranking need corpus/query evaluation, not fixed universal values.
- Use explicit embeddings and LLMs: default constructors may invoke paid remote providers or download models.
- Persisted index metadata and vector data have backend-specific ownership/reload requirements; storage_context.persist is not a universal backup.

## Agents, concurrency and observability

- Use the supported workflow-agent API for the installed version; older ReActAgent.from_tools/chat examples are not portable to current generations.
- Do not use the unverified LLMCache/Settings.llm_cache recipe from upstream; select a documented cache integration and identity/expiry policy.
- Bound async query concurrency and provider retries; asyncio.gather alone does not impose rate/resource limits.
- Evaluate authorized document access, retrieval precision/recall, answer grounding, prompt injection resilience, and tenant isolation.

## Primary documentation

- [Primary documentation](https://developers.llamaindex.ai/python/framework/) — Current framework documentation separates ingestion, storage, retrieval and workflow-agent integrations.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
