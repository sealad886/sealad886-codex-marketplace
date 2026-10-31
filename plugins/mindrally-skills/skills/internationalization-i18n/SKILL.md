---
name: internationalization-i18n
description: "Use when engineering multilingual web or mobile interfaces, locale-aware formatting, translation loading, or RTL behavior."
---

# Internationalization (i18n)

## When to invoke

Use for application internationalization architecture and runtime behavior.

## Inputs and evidence

Inspect the existing message library, locale identifiers/fallbacks, SSR boundaries, device locale APIs, formatting, and translator context. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Separate message identity, UI language, formatting locale, currency, and time-zone requirements.
2. Externalize complete translatable messages using the existing plural/interpolation system.
3. Implement locale loading, persistence, SSR isolation, RTL, and accessible language metadata.
4. Check pseudolocales, real translations, missing keys, plural boundaries, and language switching.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Representative locale tests demonstrate correct messages, formatting, direction, fallback, SSR isolation, and layout under expansion.

## Must not

Do not force one translation/state library, concatenate grammatical fragments, or convert date-only values into instants unnecessarily. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
