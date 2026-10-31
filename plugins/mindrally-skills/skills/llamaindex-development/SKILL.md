---
name: llamaindex-development
description: "Use when building LlamaIndex ingestion, indexes, retrievers, query engines, agents, or persistent RAG applications."
---

# LlamaIndex Development

## When to invoke

Use for building LlamaIndex ingestion, indexes, retrievers, query engines, agents, or persistent RAG applications.

## Inputs and evidence

Inspect core/integration versions, LLM/embedding configuration, storage backend, document ownership, retrieval evaluation set, and resource budgets. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Select only required supported integrations and configure models explicitly.
2. Build ingestion/chunking with source identity, access filters and deterministic update behavior.
3. Connect retrieval/synthesis or current workflow agents with bounded tools and persistence.
4. Evaluate retrieval and generation separately and test storage reload/failure paths.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Synthetic retrieval and reload tests pass; model quality, provider access and cost claims require separate authorized runtime evidence.

## Must not

Do not send private documents to default cloud models or treat retrieval quality as proven by fluent output. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
