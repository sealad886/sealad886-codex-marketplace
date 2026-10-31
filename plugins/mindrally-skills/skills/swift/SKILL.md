---
name: swift
description: "Use when changing Swift models, concurrency, errors, persistence, platform integration, or SwiftUI-facing application behavior."
---

# Swift implementation on Apple platforms

## When to invoke

Use when changing Swift models, concurrency, errors, persistence, platform integration, or SwiftUI-facing application behavior.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect Swift/Xcode versions, package/deployment targets, platform APIs, actor isolation, state ownership, and available devices.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define the behavior and deployment-compatible API boundary.
2. Implement clear ownership, error handling, and isolation using the project’s architecture.
3. Build supported targets and run focused tests, then profile only when performance is part of the change.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Build declared targets and run applicable unit/UI checks; identify unavailable SDK, device, signing, or distribution acceptance.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
