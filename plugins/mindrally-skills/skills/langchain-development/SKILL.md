---
name: langchain-development
description: "Use when building LangChain or LangGraph agents, runnables, tool workflows, persistence, or RAG."
---

# LangChain Development

## When to invoke

Use for building LangChain or LangGraph agents, runnables, tool workflows, persistence, or RAG.

## Inputs and evidence

Inspect pinned LangChain/LangGraph/provider packages, supported agent API, state/checkpoint ownership, tool authority, and data routing. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose current APIs within the pinned package generation and keep provider integrations explicit.
2. Implement typed tools, bounded execution and state transitions with cancellation/error handling.
3. Build ingestion/retrieval and persistence around identity, provenance and retention boundaries.
4. Evaluate retrieval and end-to-end behavior with deterministic fixtures and bounded real-provider checks when authorized.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Tests verify state isolation, tool limits/failures, retrieval quality, persistence, and provider-free deterministic behavior.

## Must not

Do not treat retrieved text or model tool requests as authorization. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
