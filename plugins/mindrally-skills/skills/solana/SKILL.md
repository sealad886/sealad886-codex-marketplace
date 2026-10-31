---
name: solana
description: "Use when implementing Solana or Anchor instructions, account validation, PDAs, compute limits, or transaction clients."
---

# Solana program and client development

## When to invoke

Use when implementing Solana or Anchor instructions, account validation, PDAs, compute limits, or transaction clients.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Solana/Anchor/client versions, account constraints, instruction authority, network, program upgrade authority, and test fixtures.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define account ownership, signers, PDA seeds, and permitted state transitions.
2. Implement validated instruction logic and version-matched clients with bounded compute.
3. Test adversarial accounts and transaction outcomes locally before any authorized network deployment.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run local program/integration tests for unauthorized or malformed accounts, bounds, CPI, and transaction errors; identify untested network/upgrade behavior.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
