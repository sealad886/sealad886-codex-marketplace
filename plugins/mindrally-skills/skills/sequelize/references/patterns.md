# Sequelize data integrity: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Sequelize v6 imports differ from v7 packages/APIs; use installed-major documentation and supported dialect types.

- Model validation is not a substitute for database uniqueness/foreign-key constraints; async uniqueness checks race under concurrent inserts.

- Pass the same transaction to related queries/hooks or use the configured supported transaction-context mechanism.

- A beforeCreate hook cannot assume an auto-generated primary key is already available. Use the right lifecycle phase for dependent audit rows.

- Send email or other irreversible side effects only after commit, preferably through an outbox when reliable delivery is required; an afterCreate hook may run before transaction completion.

- Bulk operations do not always run individual instance hooks; validate requested semantics explicitly.

- Association includes can change join and count semantics; test aliases, required filters, pagination, and duplicate joined rows.

- Use migrations for reviewed schema changes; never run destructive undo-all or sync({force:true}) on user data under ordinary development authority.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Transactions propagate through query options and support afterCommit hooks.](https://sequelize.org/docs/v6/other-topics/transactions/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
