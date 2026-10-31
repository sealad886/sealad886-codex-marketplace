---
name: beautifulsoup-parsing
description: "Use when extracting or navigating HTML/XML using Python BeautifulSoup."
---

# BeautifulSoup HTML Parsing

## When to invoke

Use when extracting or navigating HTML/XML using Python BeautifulSoup. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect saved/authorized markup, encoding, parser/dependency versions, selectors, output schema, and fetch limits. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Select an explicit installed parser and reproduce the source document structure before defining selectors.
2. Extract typed fields with explicit missing/error policy, correct tree navigation, and bounded URL handling.
3. Test malformed markup, absent fields, nested text, tables, encoding, and changed selectors against local fixtures.

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
