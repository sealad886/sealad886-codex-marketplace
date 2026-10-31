---
name: rtl-internationalization
description: "Use when implementing RTL locales, logical layout properties, mixed-direction text, or direction-aware controls."
---

# RTL and bidirectional interfaces

## When to invoke

Use when implementing RTL locales, logical layout properties, mixed-direction text, or direction-aware controls.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect locale/script metadata, HTML lang/dir, logical and physical styles, mixed text, platform direction APIs, and screenshots.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Identify reading-direction intent for each layout and content region.
2. Use semantic direction metadata, logical layout, and isolated interpolated text.
3. Test real RTL content, focus sequence, number/date formatting, and direction-sensitive controls.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Check LTR and RTL views with real text and keyboard/screen-reader navigation, identifying any untested platform.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
