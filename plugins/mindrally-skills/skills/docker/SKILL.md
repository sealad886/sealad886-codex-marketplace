---
name: docker
description: "Use when building or diagnosing Docker images, Compose services, container security, networking, or persistent data."
---

# Docker Development

## When to invoke

Use when building or diagnosing Docker images, Compose services, container security, networking, or persistent data. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Docker/Compose version, Dockerfile stages, base image/digest, build context, runtime user, mounts, ports, and target architecture. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define image/runtime inputs and inspect what enters each build layer and mounted directory.
2. Implement reproducible builds and least-privilege runtime configuration with explicit health, signal, and persistence behavior.
3. Build and run the intended architecture, verify startup/failure/shutdown, image contents, dependency readiness, and data retention.

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
