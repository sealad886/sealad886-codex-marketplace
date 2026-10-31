# Pandas Best Practices: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Selection and dtype safety

- In pandas 3 Copy-on-Write is the only mode and chained assignment cannot update the parent; use one loc/iloc assignment.
- to_numpy may copy/coerce or return a read-only view; do not assume mutation-safe zero-copy access.
- errors=coerce turns invalid values into missing data; count/report those conversions rather than calling them inherently safe.
- Nullable dtypes, categoricals and string defaults vary by version and domain; preserve identifier leading zeros and numerical precision.

## Joins, time and scale

- Use merge(validate=...) and key/null checks to detect fan-out or unmatched rows; pandas null-key joins differ from SQL expectations.
- Choose groupby null/category behavior deliberately and test empty groups and missing values.
- Preserve time-zone/date-only semantics through to_datetime/resample/rolling and check daylight-saving boundaries when relevant.
- Chunked I/O only bounds memory if downstream computation is also incremental; vectorization can allocate large temporaries.

## Primary documentation

- [Primary documentation](https://pandas.pydata.org/docs/user_guide/migration.html) — pandas3 Copy-on-Write disallows parent mutation through chained assignments and can expose read-only underlying arrays.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
