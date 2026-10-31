# Snowflake ingestion and transformation: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- JSON null in VARIANT is a distinct JSON null value, not the ordinary string "null"; distinguish SQL NULL, missing fields, JSON null, and text values.

- VARIANT can provide efficient columnar extraction for suitable data; flatten/cast based on types and query needs rather than assuming nested data prevents optimization.

- Choose Dynamic Tables, Streams/Tasks, Snowpipe, or streaming ingestion from supported SQL and operational needs; no universal default fits every pipeline.

- TARGET_LAG is a freshness target, not a hard latency guarantee; inspect refresh history and upstream dependencies.

- CREATE OR REPLACE can drop/recreate objects and affect grants, streams, or retention; it is not inherently a safe idempotent migration.

- Resource monitors do not cap every Snowflake service charge; inspect serverless/service billing separately and avoid claiming a hard total credit ceiling.

- Clones initially share storage, but subsequent changes/retention incur storage costs; Time Travel and Fail-safe depend on object type, edition, and retention settings.

- Postgres/Iceberg capabilities and DDL vary by current product availability; verify exact syntax and privileges before provisioning, rather than retaining speculative instance/FORK examples.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [VARIANT distinguishes JSON null, SQL NULL, and missing values.](https://docs.snowflake.com/en/user-guide/semistructured-considerations)
- [Resource monitor coverage and limitations must be assessed for the service involved.](https://docs.snowflake.com/en/user-guide/resource-monitors)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
