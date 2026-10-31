---
name: vite
description: "Use when configuring Vite framework plugins, assets, environment exposure, development proxying, HMR, or production builds."
---

# Vite build and development behavior

## When to invoke

Use when configuring Vite framework plugins, assets, environment exposure, development proxying, HMR, or production builds.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Vite/Node/plugin versions, module format, config, environment variables, build targets, and real dev/build failures.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Reproduce the issue in development or production mode and identify the actual versioned build pipeline.
2. Configure only necessary plugins, resolution, assets, and environment boundaries.
3. Run production build/type checks and exercise the built application with representative routes/assets.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run config/type/build checks and built-app smoke tests, checking env exposure, assets, proxy/HMR cleanup, and relevant routes.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
