# Snowflake Cortex AI and retrieval: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- For text AI_FILTER, supply the documented input/predicate prompt or PROMPT form; the source’s arbitrary text-plus-predicate positional call is not the general text signature.

- AI_EXTRACT accepts text/file plus a response-format argument, not an arbitrary list of separate field-name arguments.

- Casting generated JSON text to VARIANT does not by itself validate or necessarily parse the intended object; use documented structured outputs or explicit parsing and schema checks.

- Check model/function-specific token limits, supported modalities, result schemas, and error options. Do not assume a similarly named TRY function is a drop-in replacement.

- No universal claim establishes narrower functions are always cheaper or all aggregates have unlimited effective context; estimate current price and evaluate workload behavior.

- Verify region/cross-region inference configuration and data-handling policy; never promise data cannot leave the account region merely because SQL invokes it.

- Cortex Search access can expose indexed data under service ownership semantics; validate query privileges and row/tenant filtering rather than assuming source-table policies automatically protect every search result.

- Search service creation/refresh and model calls may incur costs. Warehouse size, primary keys, scoring options, and grants follow the current service definition, not fixed MEDIUM/default-PUBLIC assumptions.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Text AI_FILTER syntax takes input/PROMPT rather than the source’s two arbitrary text arguments.](https://docs.snowflake.com/en/sql-reference/functions/ai_filter)
- [AI_EXTRACT takes text/file and responseFormat.](https://docs.snowflake.com/en/sql-reference/functions/ai_extract)
- [Cortex capabilities and availability must be selected from current documented functions.](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
