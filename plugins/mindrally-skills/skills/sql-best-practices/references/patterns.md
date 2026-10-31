# SQL correctness and query plans: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Optimizers generally choose predicate/join order; writing restrictive WHERE clauses first or largest tables first is not a universal optimization.

- EXISTS versus IN depends on semantics and planner behavior; NOT IN with NULLs differs from NOT EXISTS. Preserve correctness before plan changes.

- Use explicit required columns for stable interfaces, but SELECT * is legitimate in some ad-hoc or existence contexts.

- Design indexes from selectivity, access patterns, and write overhead, then inspect plans; not every filtered column needs an index.

- EXPLAIN ANALYZE executes the query; obtain authority and use a disposable transaction/environment for writes. Plain EXPLAIN and dialect equivalents differ.

- Use deterministic unique ordering for pagination; keyset pagination can avoid large offsets where the contract allows it.

- Transactions require engine-specific exception/rollback handling. The source’s SQL Server @@ERROR after only the second update can miss an earlier failed statement.

- Use database constraints and correct isolation/locking for concurrent integrity; previewing UPDATE with SELECT does not prevent concurrent changes.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Plans expose optimizer choices and EXPLAIN ANALYZE actually executes the query.](https://www.postgresql.org/docs/current/using-explain.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
