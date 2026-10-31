---
name: mongodb-development
description: "Use when designing MongoDB documents, indexes, aggregation, transactions, or version-aware Mongoose and Payload integration."
---

# MongoDB Development

## When to invoke

Use for designing MongoDB documents, indexes, aggregation, transactions, or version-aware Mongoose and Payload integration.

## Inputs and evidence

Inspect server/driver/ODM/CMS versions, topology, document invariants, query patterns, indexes and access-control boundaries. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Model documents around actual read/write and atomicity requirements.
2. Implement validated queries/aggregations and targeted indexes with selected driver/ODM APIs.
3. Use transactions only for coupled multi-document effects and supported deployment topology.
4. Test access control, pagination, query plans, failure recovery and schema updates.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Selected-topology tests establish query/data invariants, authorization, pagination and transaction outcomes.

## Must not

Do not substitute distributed transactions for sound document modeling or trust arbitrary query operators. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
