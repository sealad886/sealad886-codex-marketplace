# Snowpark and dbt transformations: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Snowpark builds lazy plans, but collect/to_pandas and similar actions can transfer results to the client; do not claim data never leaves Snowflake.

- Use supported vectorized UDF annotations/registration. A plain pandas.Series annotation is not enough evidence for every Snowpark version.

- Register model artifacts through supported imports/stage access and load only trusted artifacts; sys.path[0]+model.pkl is not a portable artifact-location contract.

- Benchmark vectorized versus scalar UDFs for the actual workload; do not promise a universal 10–100x speedup.

- Incremental timestamp filters need initial/empty-target handling, late-arrival strategy, deterministic unique keys, and duplicate reconciliation. MAX(timestamp) can be NULL.

- on_schema_change sync_all_columns can remove/change columns; choose an explicit schema-evolution policy rather than calling it universally safe.

- Preserve target.schema isolation in generate_schema_name. Replacing it with only custom_schema can overwrite other developers’ or CI models.

- Use ref/source dependencies and appropriate materializations; dbt compile/build/freshness commands have different execution and remote-write effects. Close sessions and use managed authentication.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Snowpark actions execute plans and collect results.](https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes)
- [Vectorized UDFs use documented batched input/output annotations.](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udfs)
- [Removing target.schema from custom schema generation can cause developer and CI collisions.](https://docs.getdbt.com/docs/build/custom-schemas)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
