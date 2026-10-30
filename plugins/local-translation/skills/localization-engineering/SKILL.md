---
name: localization-engineering
description: Prepare and verify translation source assets, segment context, protected structure, and reconstruction routes. Use when a translation coordinator assigns source preparation, extraction checks, working-package engineering, or investigation of missing content across languages.
---

# Localization Engineering

Own the source-to-working-package boundary. Make every commissioned element
traceable before downstream teams multiply a preparation error across locales.
Read the [shared expert contract](../.shared/references/expert-contract.md) and
acknowledge this skill, your assigned scope, and missing evidence before working.

## When to invoke

Use for source inventory, extraction or import assessment, stable segmentation,
functional-token protection, and round-trip feasibility checks. Use again when a
reviser discovers omissions that may originate in a shared source or filter.

## Inputs and evidence

- Approved source revision, source locale, intended locales and output formats.
- Native files or recordings, visible/rendered references, and an element inventory.
- Treatment of comments, tracked changes, hidden text and embedded objects.
- Authorized preparation tools, workspace, disclosure rules and target application.
- Existing extraction/segment map, protected tokens and known source defects.

Read the [runtime guide](../.shared/references/runtime.md) before preparing its
inline UTF-8 prose or explicit segments. Supply the prepared content through
MCP, not a source path, and keep any caller-managed source map separate from the
server's temporary session. A supplied PDF is evidence to inspect; it is not
evidence that the runtime can extract or reconstruct that format.

## Workflow

### 1. Establish the asset inventory

Identify files, revisions and their relationships. Account for headings, body
paragraphs, tables, footnotes, figures, image text, labels and cross-references.
Compare the inventory with actual source views, rather than relying on word count.
Mark inaccessible content and ambiguous inclusion decisions for the coordinator.

### 2. Verify extraction and context

Compare prepared text against its source location. Inspect column order, table
relationships, symbols, superscripts and text embedded in objects. Retain enough
surrounding context to interpret short labels and repeated terms. Give each unit
a stable identifier and map it to the original location; avoid identifiers that
change whenever a neighbouring paragraph is inserted.

Do not silently repair factual or evidentiary source errors. Record the defect
and route a proposed amendment through the content liaison and actual owner.

### 3. Protect function without freezing language

Identify placeholders, markup, product identifiers, numbers and protected spans.
For deliberate printf strings, use the runtime's explicit format mode. Ordinary
percentages remain prose. Separate a token's required function from the sentence
around it, which may need reordering in the target language. Flag unsupported
native grammars rather than claiming that literal-token checks validate them.

### 4. Prove the proposed route on a representative unit

When commissioned tools are available, test import, translation-unit mapping,
export and actual rendering with representative difficult elements. Compare the
reconstructed result with the input inventory. Record missing fonts, script or
layout limitations. If those tools are unavailable, hand off a bounded text
package and an unverified reconstruction route, not a completed native product.

### 5. Hand off or investigate a shared defect

Give translators and revisers the source map, contextual views, protected-token
policy and unresolved questions. If a common omission is found, identify every
locale derived from the defective package. Propose a corrected source package
and replacement immutable job through the coordinator; do not patch stored job
JSON or ask each translator to improvise a different missing passage.

## Outputs and handoff

Use the [expert handoff](../.shared/templates/expert-handoff.md). Include:

- Asset/revision inventory and source-to-segment map, with inclusion decisions.
- Verified preparation steps, coverage gaps and functional-token policy.
- Working files and identities, export/rendering evidence or explicit tool gaps.
- Shared defects, affected locales, owner questions and required replacement work.

For example, a table label absent from all three target languages is first a
source-package investigation; three independent target rewrites do not repair it.

## Completion evidence

Every commissioned source element is mapped or explicitly excluded by an
attributed decision. Representative preparation and reconstruction checks have
actual artifacts when that route is commissioned. Translators can locate context,
and the coordinator can distinguish verified preparation from unsupported output.

## Must not

Do not equate extracted word count with completeness, overwrite originals,
invent inaccessible text, discard functional structure, claim unsupported
PDF/DOCX/media reconstruction, or conceal a shared input defect behind target
proofreading. A native-file operation requires real tools and an authorized remit.
