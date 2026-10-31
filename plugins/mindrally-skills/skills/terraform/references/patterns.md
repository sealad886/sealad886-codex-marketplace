# Terraform infrastructure changes: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Terraform state and saved plans can contain secrets even when outputs are marked sensitive; protect access, storage, logs, and retention.

- Use a backend that supports the needed locking and encryption; remote state alone does not guarantee every safety feature is enabled.

- CLI workspaces separate state but are not automatically a strong credential/access boundary between environments.

- Commit provider locks according to repository policy and constrain modules/providers intentionally; init may download code and alter locks.

- Resource targeting is for exceptional recovery/workaround cases, not routine change optimization; it can omit dependencies and leave incomplete convergence.

- A rollback means a reviewed new desired state or provider-specific recovery, not a guaranteed reversal of every apply.

- State mv/rm/import and backend migration change authoritative tracking; inspect backups and exact scope and do not run them as ordinary read-only review.

- Plan/refresh can read remote systems and sensitive values. Apply, destroy, provisioning, and cost changes require explicit task authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Resource targeting is an exceptional planning option and plan behavior is explicit.](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [State can contain sensitive data requiring secure handling.](https://developer.hashicorp.com/terraform/language/state/sensitive-data)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
