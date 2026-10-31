# Solana program and client development: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Mutable program state resides in supplied data accounts; program code and account state have separate ownership/lifecycle.

- Validate owner, signer, writable, executable, address/seed, and relationship constraints required by each instruction; receiving a public key is not authorization.

- Use canonical PDA derivation and correct signer seeds for CPI; validate invoked program identity and account aliasing.

- Anchor constraints help but do not automatically prove every business invariant or safe close/reinitialization behavior.

- On-chain program execution does not provide ordinary Rust thread concurrency; optimize compute units, account contention, serialization, and instruction size.

- Choose the actual installed client SDK; do not assume legacy web3.js APIs and newer clients are interchangeable.

- RPC submission is not confirmed success; track commitment, blockhash expiry, simulation errors, and duplicate/retry behavior.

- Treat upgrades, authority changes, signed transactions, and mainnet operations as separate explicitly authorized effects.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Solana programs are executable accounts and mutable state resides in separate data accounts.](https://solana.com/docs/core/programs)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
