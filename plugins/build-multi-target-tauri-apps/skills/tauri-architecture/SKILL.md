---
name: tauri-architecture
description: Use when designing or refactoring Tauri Rust/frontend boundaries, commands, channels, state, persistence or optional browser behavior.
license: MIT
---

# Tauri Architecture and IPC

Read [common operating contract](../.shared/operating-model.md) before work and [architecture reference](../.shared/architecture.md) for this workflow. Current sources and adaptation rationale: [research ledger](../.shared/research.md).

## When to invoke

Use when designing or refactoring Tauri Rust/frontend boundaries, commands, channels, state, persistence or optional browser behavior.

## Inputs and evidence

Handlers, JS callers, Rust state/types, schema/migrations, target matrix, existing public contracts and lockfiles.

## Workflow

1. Trace current user flow through components, invoke handlers, managed state, plugins and storage. Inspect actual serialization and resource lifetime before inventing abstractions.
2. Define target feature owners, request/result/error contracts, validation, task identity, cancellation and consistency. Keep domain logic independent of transport.
3. Follow [architecture reference](../.shared/architecture.md): choose commands/events/channels deliberately, bound work and messages, avoid blocking executor/UI or locks across await.
4. For persistence changes inspect existing schema/data, design local backup and one-off conversion/verification. Apply authorized future-state behavior without speculative adapters.
5. Route custom commands/data privileges through [tauri-security](../tauri-security/SKILL.md). Implement one canonical service; browser variants exist only when requested and actually supported.
6. Validate serialization, malformed inputs, operation completion/cancellation, listener disposal and restart durability through [tauri-testing](../tauri-testing/SKILL.md).

## Outputs and handoff

Boundary design/implementation, explicit lifecycle/storage contracts, migration disposition and focused evidence.

## Completion evidence

Contracts match real handlers/callers; changed invariants have behavioral evidence and sensitive boundaries are reviewed.

## Must not

Expose arbitrary shell/SQL/path operations; hold locks across await; equate abandoned UI promises with backend cancellation; place server secrets in frontend.
