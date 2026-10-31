# Ethereum Development: implementation guidance

## Solidity and libraries

Use PascalCase for contract/interface types and the project's function conventions.
constant values are compile-time expressions; immutable values can be assigned
during construction, so they are not the same mechanism. Solidity 0.8 checked
arithmetic still has unchecked blocks, casts and economic/rounding hazards.
Pin compiler and OpenZeppelin versions: ERC20Snapshot was removed from Contracts
5, and extension hooks/import paths changed. SafeERC20, access controls, pausing
and guards address specific risks, not complete security. Minimize assembly and
prove its invariants when genuinely required.

## Calls, upgrades, and acceptance

Checks-effects-interactions plus guards require review across every callback and
cross-function path. Handle external call results and nonstandard token behavior.
Use pull payments only when they fit the protocol; rate limits/timelocks require
explicit policy. Proxies are optional and add initialization, admin, storage-layout,
and upgrade trust risks. Do not add upgradeability by default. Log necessary events
without treating logs as enforceable state. Tool scans, test coverage, audits and
bug bounties provide different evidence; none guarantee safety. Mainnet transactions,
funds movement, governance changes and publication require explicit authorization.

## Primary documentation

- [Contracts v5 removals and extension changes](https://docs.openzeppelin.com/contracts/5.x/changelog).
- [Constant versus immutable semantics](https://docs.soliditylang.org/en/latest/contracts.html#constant-and-immutable-state-variables).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
