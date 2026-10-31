---
name: phoenix
description: "Use when developing Phoenix contexts, Ecto persistence, LiveView interactions, real-time processes, or authenticated web flows."
---

# Phoenix Framework Development

## When to invoke

Use for developing Phoenix contexts, Ecto persistence, LiveView interactions, real-time processes, or authenticated web flows.

## Inputs and evidence

Inspect Phoenix/LiveView/Elixir versions, context boundaries, Ecto schemas/queries, authentication hooks, supervision and test conventions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Implement domain operations in existing contexts with Ecto validation/transactions.
2. Build controller or LiveView interfaces using version-supported rendering and lifecycle APIs.
3. Authorize mounts, events and domain operations; own concurrent work through supervision.
4. Run context, connection/LiveView and failure tests including reconnect/denied actions.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Context/Ecto and web/LiveView tests verify authorization, transaction behavior, reconnect and supervised failure handling.

## Must not

Do not treat an authenticated socket or changeset as sufficient resource authorization. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
