---
name: onchainkit
description: "Use when integrating OnchainKit identity, wallet, transaction, swap, or supported mini-app components."
---

# OnchainKit

## When to invoke

Use for integrating OnchainKit identity, wallet, transaction, swap, or supported mini-app components.

## Inputs and evidence

Inspect OnchainKit/React/wagmi/viem versions, provider composition, chain/RPC configuration, supported exports and wallet permissions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose components available in the installed package and configure the required provider hierarchy.
2. Implement connection/identity and transaction UI with explicit chain/account state.
3. Validate transaction destination, value, approvals and user-visible fee/sponsorship behavior.
4. Test disconnected, wrong-chain, rejected, pending, failed and confirmed states on an approved test environment.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Installed exports type-check and approved test-chain/mock-wallet scenarios verify lifecycle and transaction intent.

## Must not

Do not submit mainnet transactions, spend assets, or grant token approvals from skill invocation alone. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
