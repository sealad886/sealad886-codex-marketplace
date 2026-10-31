---
name: odoo-development
description: "Use when extending Odoo models, computed fields, constraints, XML views, controllers, security rules, or scheduled jobs."
---

# Odoo Development

## When to invoke

Use for extending Odoo models, computed fields, constraints, XML views, controllers, security rules, or scheduled jobs.

## Inputs and evidence

Inspect exact Odoo edition/version, addons dependencies/manifest, model ownership, view syntax, ACLs/record rules and test database. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend through supported addon/model/view inheritance without modifying core.
2. Implement recordset-aware ORM methods, computed dependencies and persistent invariants.
3. Configure access controls, translations and controllers with explicit authorization.
4. Install/upgrade in an isolated database and test record rules, ORM behavior and views.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Isolated addon installation/upgrade, model tests and ordinary-user/multi-company access checks pass.

## Must not

Do not assume onchange or administrator testing proves data integrity/access control. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
