# OnchainKit: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Providers and capabilities

- OnchainKit supplies React components and TypeScript utilities; inspect current exports rather than assuming historical FrameMetadata APIs remain available.
- Compose OnchainKitProvider with required wallet/query integrations for the installed version; do not duplicate existing application providers.
- Keep client-publishable API identifiers distinct from server secrets and enforce service restrictions as supported.

## Transactions and identity

- Identity/ENS/Basename resolution is chain-dependent and needs loading/fallback states; display names are not authorization identities.
- Quotes and gas estimates expire; validate chain, token decimals, recipient, slippage and approval amount before requesting wallet signing.
- Wallet connection does not authorize arbitrary spending or server resources; user approval is required for transaction effects.
- Test rejected signatures, sponsorship failures, reorg/confirmation policy and stale UI state; never claim guaranteed transaction completion.

## Primary documentation

- [Primary documentation](https://raw.githubusercontent.com/coinbase/onchainkit/main/README.md) — Official OnchainKit source identifies supported React/TypeScript component tooling and current documentation entrypoints.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
