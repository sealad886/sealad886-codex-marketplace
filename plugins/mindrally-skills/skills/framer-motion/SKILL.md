---
name: framer-motion
description: "Use when implementing Motion/Framer Motion React animations, gestures, layout transitions, scroll motion, or exit behavior."
---

# Framer Motion / Motion Animation Guidelines

## When to invoke

Use when implementing Motion/Framer Motion React animations, gestures, layout transitions, scroll motion, or exit behavior. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect installed motion/framer-motion version, React/rendering boundary, animated state, target elements, and accessibility/performance needs. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Choose imports and APIs matching the installed package and define animation ownership/state transitions.
2. Implement the selected variants/gestures/layout/scroll/exit path with stable identity and correct lifecycle.
3. Check reduced motion, keyboard interaction, interruption, unmount/exit and measured rendering cost on target devices.

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
