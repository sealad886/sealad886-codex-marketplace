# Blockchain Development: implementation guidance

## Contracts and storage

Rust type safety does not prove authorization, arithmetic safety, or contract
correctness. Validate addresses through the chain API; check sender and attached
funds explicitly. Use cw-storage-plus Item/Map/IndexedMap only with understood key
and index semantics. Minimize storage work without breaking accounting invariants.
Migration needs authorized code/admin changes, schema/version checks, and tested
state conversion. Not every deployed contract is immutable or upgradeable.

## IBC and cross-chain behavior

Separate local transaction atomicity from asynchronous cross-chain outcomes.
Validate channels, counterparties, protocol versions, packets, acknowledgements,
and timeouts; use the IBC version supported by the chain. Track pending/completed
state and prevent duplicate processing or replay where application semantics
require it. A timeout is not proof that an arbitrary external effect never occurred.
Bound packet/gas work, test relayer delays, and document recovery/compensation.
Use multi-test/simulations and actual testnets for their separate evidence scopes.
Mainnet deployment, admin changes, and funds movement need explicit authority.

## Primary documentation

- [CosmWasm contract architecture and IBC documentation](https://cosmwasm.cosmos.network/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
