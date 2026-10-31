# Elasticsearch Best Practices: implementation guidance

## Mapping, search, and pagination

Use keyword for suitable exact fields, text/analyzers for full text, and nested
when object-array association must be preserved. Test analyzer output and synonyms;
edge-ngram ranges may need index.max_ngram_diff configuration. Filter context is
eligible for caching according to policy, not guaranteed automatically cached.
Terms aggregation can be approximate across shards; composite aggregation supports
bucket pagination. search_after needs a stable unique tiebreaker and often a point
in time; _id is restricted from sorting, so copy an identifier to a doc-values field
or use the documented PIT tiebreaker. Escape highlighted source fragments safely.

## Indexing and operations

Benchmark shard/bulk sizes for the workload. The 20-shards-per-GB-heap rule was
retired in 8.3; do not apply it to current clusters. Inspect every bulk item result
and retry only eligible failures. If changing refresh settings for an authorized
load, record/restore the prior value even on failure rather than hardcoding 1s.
ILM rollover/aliases/data-stream settings and security features depend on deployment.
Force merge is expensive and suited to appropriate read-only indices, not routine
cleanup on active data. Reindex needs reviewed mappings and a concurrent-write
strategy before an atomic alias switch; creating an alias does not prove data parity.

## Primary documentation

- [Modern shard guidance and retired heap rule](https://www.elastic.co/search-labs/blog/elasticsearch-node-shard-size-best-practices).
- [_id sorting restrictions](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-id-field).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
