# PySpark ETL: implementation guidance

Read the relevant section after inspecting the target project. These patterns
are conditional on its runtime and dependency versions.

## Transformations and resources

- Prefer native functions where suitable, but UDFs are not universally forbidden and F.col without aliases does not automatically resolve ambiguous joins.
- Windows need intentional frames/order/ties; ignore-null behavior must follow domain semantics rather than always discarding nulls.
- printSchema does not materialize the entire dataset, while collect/count/show have different action and resource costs.
- Only stop a SparkSession the job owns; an injected shared session must remain available to its owner.

## Iceberg and integrity

- df.write.byName().insertInto is not the supported PySpark recipe. Iceberg recommends df.writeTo(table) DataFrameWriterV2 operations, which resolve columns by name.
- Use catalog-supported metadata names such as table.partitions and table.snapshots; a latest partition is not necessarily the latest snapshot.
- Idempotent merges need unique keys and a deterministic version/time conflict rule so older backfills cannot overwrite newer state.
- Broadcast, persistence and write distribution depend on actual sizes/plans/memory; no none/range setting universally guarantees fastest or best scans.
- Use typed nulls and explicit unknown-category handling; never silently discard duplicate/unmapped records to make validation pass.

## Primary documentation

- [Primary documentation](https://iceberg.apache.org/docs/latest/spark-writes/) — Iceberg recommends DataFrameWriterV2 writeTo operations that match table columns by name and expose explicit overwrite behavior.
- [PySpark DataFrameWriter API](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.html) — DataFrameWriter has no general byName method; use supported writer interfaces.
- [Iceberg metadata queries](https://iceberg.apache.org/docs/latest/spark-queries/) — Catalog table metadata distinguishes partitions and snapshots.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
