---
name: woocommerce
description: "Use when implementing WooCommerce hooks, products/orders, checkout extensions, REST endpoints, or data integrity."
---

# WooCommerce store extensions

## When to invoke

Use when implementing WooCommerce hooks, products/orders, checkout extensions, REST endpoints, or data integrity.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect WordPress/WooCommerce/PHP versions, HPOS mode, classic versus block checkout, hooks/data stores, permissions, and payment test setup.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Locate the supported extension/data boundary for the requested store behavior.
2. Implement validated inputs, capability/ownership checks, and WooCommerce CRUD semantics.
3. Test cart/checkout/order lifecycle behavior with synthetic transactions in an isolated store.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run isolated product/cart/order and permission tests for the active checkout/HPOS modes, including duplicate hooks and failed payments where affected.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
