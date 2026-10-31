# Solidity contracts and transaction UX: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Checks-effects-interactions and guards reduce reentrancy risk but require analyzing every external call and cross-function invariant.

- Solidity 0.8 arithmetic checks have exceptions such as unchecked blocks and casts; validate bounds and precision explicitly.

- Use maintained token/permission primitives compatible with the installed OpenZeppelin major; ERC20Snapshot was removed in v5.

- Do not introduce proxies by default. Upgradeable contracts require initialization, storage-layout discipline, compatible libraries, and explicit governance.

- Use immutable values, packing, custom errors, and unchecked arithmetic only when correctness and measured gas justify them.

- Randomness, oracle trust, front-running, signature replay/domain separation, and token callback behavior need task-specific analysis.

- Simulation can expose likely reverts but is not a guarantee against state changes before inclusion; show submitted, pending, reverted, and confirmed states separately.

- Wallet connection does not authorize arbitrary transactions; keep network, destination, value, allowances, and admin authority reviewable.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [External calls and cross-contract state require deliberate reentrancy analysis.](https://docs.soliditylang.org/en/latest/security-considerations.html)
- [OpenZeppelin v5 removed ERC20Snapshot and changed supported APIs.](https://docs.openzeppelin.com/contracts/5.x/changelog)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
