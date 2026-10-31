# Medusa Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Modules and workflow graphs

- Use model utilities/MedusaService where generated model CRUD is appropriate; confirm module registration and public interfaces.
- Workflow constructor functions describe a graph: use transform/when for dynamic values and do not execute async side effects directly in the constructor.
- Put effects in steps and provide meaningful compensation data; compensation is not automatically an isolated database transaction.

## Commerce correctness and interfaces

- Validate positive quantities/amounts and server-derived ownership before redemption or financial effects.
- Read-modify-write balances can race; use supported locking/atomic updates or transactions and idempotency. Restoring an old balance can overwrite concurrent legitimate changes.
- Query handles links and cross-module reads; internal module methods remain valid within their own supported boundaries.
- Admin widgets should follow supported SDK/UI conventions, but source style rules are not universal API restrictions.
- Event payloads need actual domain identifier resolution; an order ID must not be silently used as a loyalty-account ID.

## Primary documentation

- [Primary documentation](https://docs.medusajs.com/learn/fundamentals/workflows) — Workflow constructors describe step graphs and support compensation, conditions, transformation and locking.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
