---
name: ethereum
description: "Use when implementing or reviewing Ethereum Solidity contracts, OpenZeppelin integrations, upgrades, or tests."
---

# Ethereum Development

## When to invoke

Use when implementing or reviewing Ethereum Solidity contracts, OpenZeppelin integrations, upgrades, or tests. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect compiler/chain/EVM/library versions, storage layout, permissions, token semantics, economic invariants, and deployment authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define assets/roles/state transitions and threat assumptions before contract changes.
2. Implement version-correct interfaces and explicit authorization, reentrancy, arithmetic and external-call handling.
3. Compile and test invariants, adversarial calls, fuzz/property cases, upgrade layout and gas constraints before any authorized deployment.

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
