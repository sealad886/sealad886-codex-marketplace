---
name: react-native-r3f
description: "Use when building React Three Fiber scenes, especially when selecting web versus React Native rendering and assets."
---

# React Three Fiber across web and native

## When to invoke

Use when building React Three Fiber scenes, especially when selecting web versus React Native rendering and assets.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect renderer target, React/Fiber/Three versions, GL availability, asset loading, frame work, and device constraints.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Select the correct web or native renderer and compatible packages before editing a scene.
2. Compose scene objects and scoped hooks; load assets through target-supported paths.
3. Profile frame work, draw calls, resource lifetime, resize behavior, and graceful rendering failures.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Render the changed scene on the intended target, check asset failures and teardown, and measure frame behavior when claiming optimization.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
