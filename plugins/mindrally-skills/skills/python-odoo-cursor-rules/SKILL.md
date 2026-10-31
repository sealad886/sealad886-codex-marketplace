---
name: python-odoo-cursor-rules
description: "Use when developing Python Odoo addons, ORM methods, XML/QWeb views, controllers, translations, or security rules."
---

# Python and Odoo Development

## When to invoke

Use for developing Python Odoo addons, ORM methods, XML/QWeb views, controllers, translations, or security rules.

## Inputs and evidence

Inspect Odoo version/edition, addon manifest/load order, recordset model semantics, base views and ACL/record-rule requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend the owning addon through supported model/view inheritance.
2. Implement computed fields, constraints and ORM operations with batch/transaction awareness.
3. Validate controller inputs and enforce ordinary-user/multi-company permissions.
4. Install/upgrade an isolated database and test server invariants and rendered views.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Addon install/upgrade and ordinary-user model/controller/view tests prove server invariants, access and versioned UI behavior.

## Must not

Do not modify Odoo core or use sudo to bypass a failing access-control test. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
