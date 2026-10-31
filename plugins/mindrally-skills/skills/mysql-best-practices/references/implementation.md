# MySQL Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Schema and queries

- InnoDB is the common transactional engine; choose alternatives only for a demonstrated supported need.
- Composite index order follows equality/range/order and query patterns, not a universal most-selective-column-first rule.
- FULLTEXT search and substring LIKE have different semantics; replacing one with the other can change results.
- Use stable tie-breakers for keyset pagination and verify generated-column/JSON casts against actual values.

## Version and operations

- MySQL 8 removed the query cache; setting query_cache_type=0 is not a valid way to disable a removed feature.
- SHOW REPLICA STATUS and current replication metrics replace legacy terminology where supported; replication lag is not simply one timestamp difference in every topology.
- Use numeric configuration values supported by the version, not placeholders such as 70%_of_RAM; size buffers and connections from the real host workload.
- Transaction examples need explicit validation/rollback and deadlock handling; plaintext placeholder passwords and broad host grants are not deployment recipes.
- ANALYZE/OPTIMIZE/index deletion can consume locks/resources or rebuild data; plan impact and recovery before live execution.

## Primary documentation

- [Primary documentation](https://dev.mysql.com/doc/refman/8.4/en/added-deprecated-removed.html) — MySQL configuration and replication options have version-specific additions, deprecations and removals.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
