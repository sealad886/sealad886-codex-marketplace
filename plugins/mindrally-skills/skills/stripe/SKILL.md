---
name: stripe
description: "Use when implementing Stripe checkout, PaymentIntents, subscriptions, customer ownership, webhooks, or payment-state reconciliation."
---

# Stripe payment and subscription integrity

## When to invoke

Use when implementing Stripe checkout, PaymentIntents, subscriptions, customer ownership, webhooks, or payment-state reconciliation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Stripe SDK/API version, payment flow, server-owned catalog, authenticated account mapping, webhook delivery, and test-mode setup.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define server-authoritative order totals and customer/resource ownership.
2. Implement the selected Stripe flow with idempotency and version-matched client/server APIs.
3. Reconcile signed webhook events and test retries, declines, authentication, and subscription transitions.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Use Stripe test mode and signed synthetic webhook tests for tampered totals, cross-account IDs, duplicate/out-of-order events, declines, and lifecycle state.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
