---
name: terraform
description: "Use when preparing Terraform configuration, provider/module constraints, plans, state handling, or infrastructure change review."
---

# Terraform infrastructure changes

## When to invoke

Use when preparing Terraform configuration, provider/module constraints, plans, state handling, or infrastructure change review.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Terraform/provider versions, lockfile, backend/workspace identity, current state, environment, permissions, and intended resource diff.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Verify backend, account, region, and workspace before any remote access or mutation.
2. Prepare scoped configuration and validate formatting/schema with supported providers.
3. Review the full plan and obtain existing required authorization before apply or state migration.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run fmt/check and validate, then inspect a complete plan when authorized; identify unavailable provider/account/state and apply evidence.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
