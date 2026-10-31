# Python and Odoo Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## ORM and user interface

- Modern recordset methods do not use removed api.multi; select model/depends/onchange/constrains for their documented role.
- onchange is form assistance and can be absent from programmatic writes; persist required invariants through server constraints.
- Use supported XML list/tree/modifier syntax and verify inherited XPath against actual view versions.

## Data, access and jobs

- ACLs and record rules address different layers; administrator/sudo tests can hide denied-access defects.
- Use ORM batching/prefetch and query evidence before custom caching; caching must respect user/company context.
- Cron/scheduled actions are not automatically unlimited durable async queues; bound transactions and make retries idempotent.
- Translate user-facing content and use escaped QWeb output; raw SQL/sudo bypasses need a narrow justified authorization boundary.

## Primary documentation

- [Primary documentation](https://github.com/odoo/documentation/blob/20.0/content/developer/tutorials/server_framework_101/08_compute_onchange.rst) — Odoo official documentation separates computed-field dependencies from form-only onchange behavior; installed version controls syntax.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
