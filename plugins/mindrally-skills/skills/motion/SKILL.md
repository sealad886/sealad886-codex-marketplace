---
name: motion
description: "Use when building Motion JavaScript animations, sequences, scroll/in-view behavior, playback control, or cleanup."
---

# Motion Animation Guidelines

## When to invoke

Use for building Motion JavaScript animations, sequences, scroll/in-view behavior, playback control, or cleanup.

## Inputs and evidence

Inspect motion version/import surface, vanilla versus React integration, selected elements, timeline ownership and reduced-motion/device requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use the installed animate API for tweens or sequence graphs.
2. Connect supported scroll/inView/event callbacks with explicit ownership and teardown.
3. Select easing/spring and reduced-motion behavior supported by the actual version.
4. Test interruption, replay, element removal, SSR boundaries and measured rendering.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Actual installed APIs build and behavior checks establish lifecycle cleanup, reduced motion and intended end states.

## Must not

Do not mix Motion One legacy examples with current Motion APIs without version confirmation. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
