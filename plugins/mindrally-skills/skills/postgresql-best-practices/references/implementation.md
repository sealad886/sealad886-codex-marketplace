# PostgreSQL Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Plans and schema

- EXPLAIN ANALYZE actually executes its statement, including writes; use an isolated environment and approved transaction/resource limits.
- A sequential scan may be optimal and INCLUDE does not guarantee index-only execution; visibility, selectivity and index size matter.
- Choose JSON versus JSONB by semantics/storage/query needs; automatic JSONB/index/partitioning prescriptions are not universally beneficial.
- Window frame/tie ordering affects running totals; use explicit frames and stable ordering for the intended contract.

## Security and operations

- RLS can be bypassed by superusers/BYPASSRLS and usually table owners; test ordinary application roles and WITH CHECK behavior.
- A tenant setting is only as trustworthy as who can set it; reset per-transaction identity in pooled connections and prevent user-controlled tenant substitution.
- Session advisory locks interact poorly with transaction pooling; prefer a fitting transaction-scoped mechanism and guaranteed release.
- Dead tuple counts are not a complete bloat measurement; use current statistics and appropriate inspection before REINDEX/VACUUM operations.
- Use real schema columns in examples and test backup restoration; copying a pg_dump command does not establish recoverability.

## Primary documentation

- [Primary documentation](https://www.postgresql.org/docs/current/sql-explain.html) — EXPLAIN ANALYZE executes the statement and reports actual runtime rather than merely planning.
- [PostgreSQL RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) — Table owner and privileged-role bypass and policy checks must be considered when enforcing RLS.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
