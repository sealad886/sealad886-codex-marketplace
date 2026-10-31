---
name: localization-l10n
description: "Use when adapting application content, regional terminology, formatting, layouts, or release QA for selected locales."
---

# Localization (l10n)

## When to invoke

Use for adapting application content, regional terminology, formatting, layouts, or release QA for selected locales.

## Inputs and evidence

Inspect source messages, locale/fallback policy, regional brief, translation assets, context, legal review ownership, and rendered target surfaces. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define target language/region variants and acceptance ownership.
2. Adapt complete messages, regional examples, formats, fonts, units and forms.
3. Integrate locale resources and fallback/loading behavior without losing placeholders or meaning.
4. Check actual rendered locales and obtain appropriate linguistic/domain acceptance.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Resource validation and rendered QA pass for named locales; linguistic/domain approval remains separately attributable.

## Must not

Do not claim native-language or legal acceptance from automated string checks. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
