---
name: web-scraping
description: "Use when extracting authorized website data, choosing HTTP/parser/browser tools, or implementing bounded crawl and validation behavior."
---

# Bounded web extraction

## When to invoke

Use when extracting authorized website data, choosing HTTP/parser/browser tools, or implementing bounded crawl and validation behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect source authorization/scope, page/API behavior, data sensitivity, expected schema, rate/volume limits, and existing extraction tools.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose the smallest source/tool that exposes the required data reliably.
2. Implement bounded requests, parsing, pagination, normalization, and deduplication.
3. Validate against saved fixtures and run a small authorized live sample when needed.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Test parsers on missing/malformed/duplicate/page-loop fixtures and record exact coverage/freshness of any live sample.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
