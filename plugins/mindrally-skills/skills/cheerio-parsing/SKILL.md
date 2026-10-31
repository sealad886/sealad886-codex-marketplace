---
name: cheerio-parsing
description: "Use when parsing or extracting HTML/XML with Cheerio in Node.js."
---

# Cheerio HTML Parsing

## When to invoke

Use when parsing or extracting HTML/XML with Cheerio in Node.js. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Node/Cheerio versions, document encoding/parser options, selectors, schema, and authorized fetch boundaries. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Load a local fixture with explicit HTML/document versus XML/fragment behavior.
2. Extract validated fields with deliberate missing-value, URL, and numeric handling.
3. Test malformed and absent markup, document changes, table shape, pagination, and fetch failures.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
