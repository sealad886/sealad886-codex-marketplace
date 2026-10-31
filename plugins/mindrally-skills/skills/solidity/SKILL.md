---
name: solidity
description: "Use when implementing or reviewing Solidity state transitions, permissions, token interactions, gas behavior, or wallet transaction integration."
---

# Solidity contracts and transaction UX

## When to invoke

Use when implementing or reviewing Solidity state transitions, permissions, token interactions, gas behavior, or wallet transaction integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect compiler/EVM target, dependencies, storage layout, value flow, admin/upgrade authority, invariants, and test network.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define asset/state invariants and all external-call and authority boundaries.
2. Implement version-compatible contract logic and explicit frontend transaction states.
3. Run unit/adversarial/invariant checks and gas evidence before any authorized signing or deployment.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run compiler/static and behavioral tests for invariants and unauthorized/reentrant/failing paths; report audit and mainnet acceptance limits.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
