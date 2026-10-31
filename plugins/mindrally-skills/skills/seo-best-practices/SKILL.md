---
name: seo-best-practices
description: "Use when reviewing crawlability, metadata, canonical URLs, structured data, page performance, or search-facing content."
---

# Search discoverability

## When to invoke

Use when reviewing crawlability, metadata, canonical URLs, structured data, page performance, or search-facing content.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect public routes, rendering output, robots/sitemaps, indexing intent, canonical origins, and field performance data.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define which public content should be discovered and indexed.
2. Implement accurate metadata, HTTP behavior, semantic content, and supported structured data.
3. Verify rendered output and diagnostic evidence without promising ranking improvements.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Check status codes, canonical/robots output, sitemap links, rendered metadata, structured data, and available field metrics.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
