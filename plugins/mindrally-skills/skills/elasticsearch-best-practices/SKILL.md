---
name: elasticsearch-best-practices
description: "Use when designing Elasticsearch mappings, analysis, queries, pagination, bulk indexing, lifecycle, or cluster performance."
---

# Elasticsearch Best Practices

## When to invoke

Use when designing Elasticsearch mappings, analysis, queries, pagination, bulk indexing, lifecycle, or cluster performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Elasticsearch version/deployment/license, query corpus, mappings/analyzers, shard/data size, security scope, and operational authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define search relevance and data/update requirements before selecting mappings, analyzers, and shards.
2. Implement bounded queries/aggregations/indexing with explicit error, pagination, and authorization semantics.
3. Check mappings/analyzer tokens and relevance judgments, inspect bulk item errors, and measure resource/latency behavior.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
