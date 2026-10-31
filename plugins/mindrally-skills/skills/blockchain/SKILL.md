---
name: blockchain
description: "Use when working on CosmWasm/Cosmos contracts, storage, migration, or IBC cross-chain messages."
---

# Blockchain Development

## When to invoke

Use when working on CosmWasm/Cosmos contracts, storage, migration, or IBC cross-chain messages. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect chain and CosmWasm versions, entrypoints, message schemas, authorization, funds, storage layout, and IBC channel semantics. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define deterministic state transitions, access/funds checks, and upgrade authority before changing contract logic.
2. Implement typed storage and version-correct entrypoints with idempotency and cross-chain acknowledgement/timeout handling.
3. Run contract/integration tests for invalid senders, replay, partial failure, gas bounds, migrations, and IBC lifecycle.

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
