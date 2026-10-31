---
name: scrapy-web-scraping
description: "Use when implementing Scrapy spiders, selectors, request scheduling, pipelines, crawl limits, or reproducible extraction tests."
---

# Scrapy extraction workflows

## When to invoke

Use when implementing Scrapy spiders, selectors, request scheduling, pipelines, crawl limits, or reproducible extraction tests.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Scrapy/reactor versions, authorized domains/data, site access limits, existing item schemas, and fixture responses.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define crawl scope, rate/volume limits, and expected output schema.
2. Implement supported spider entrypoints, selectors, pagination, and validation pipelines.
3. Test against captured fixtures before an authorized bounded live crawl.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run parser/pipeline tests on fixtures and verify bounded crawl counts and schema; identify omitted live/network checks.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
