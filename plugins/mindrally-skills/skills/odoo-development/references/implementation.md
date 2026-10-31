# Odoo Development: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## ORM and versioned APIs

- Modern Odoo recordset methods do not use removed @api.multi; use model/depends/constrains/onchange decorators for their actual purposes.
- onchange assists interactive forms and is not a persistent invariant; imports and direct ORM writes need constraints or other server validation.
- Computed fields must assign values for every relevant record and declare dependencies; test recomputation and batch behavior.

## Security and modules

- ACLs grant model permissions and record rules restrict records; verify both with ordinary users and multi-company context.
- sudo and raw SQL can bypass ORM/security behavior; use only a necessary scoped privileged boundary.
- XML list/tree syntax and modifiers vary by Odoo release; validate inherited XPath against the actual installed base view.
- Manifest load order and data IDs affect installation/upgrades; translate user-facing exceptions and avoid logging business secrets.

## Primary documentation

- [Primary documentation](https://github.com/odoo/documentation/blob/20.0/content/developer/tutorials/server_framework_101/08_compute_onchange.rst) — Official Odoo documentation distinguishes depends-driven recomputation from form-only onchange behavior; apply within the installed version.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
