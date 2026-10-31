---
name: three-js
description: "Use when implementing Three.js rendering, scene resources, loaders, animation, draw-call optimization, or React Three Fiber integration."
---

# Three.js scenes and GPU resources

## When to invoke

Use when implementing Three.js rendering, scene resources, loaders, animation, draw-call optimization, or React Three Fiber integration.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Three/renderer versions, target GPU, scene graph, asset/texture sizes, resource ownership, and frame/memory measurements.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define scene/camera/render-loop ownership and target rendering support.
2. Implement scene/asset changes with bounded frame work and explicit resource lifetime.
3. Verify resize, context/asset failure, teardown, and measured performance.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Render representative scenes, test resize/loading failures and repeated teardown, and compare frame/GPU resource evidence where performance changed.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
