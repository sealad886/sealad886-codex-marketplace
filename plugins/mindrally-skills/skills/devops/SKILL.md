---
name: devops
description: "Use when implementing DevOps automation, Ansible, Kubernetes, CI/CD, infrastructure, or operational recovery."
---

# DevOps Engineering

## When to invoke

Use when implementing DevOps automation, Ansible, Kubernetes, CI/CD, infrastructure, or operational recovery. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect inventory/account scope, current declarative ownership, runtime/tool versions, secrets, rollout gates, and recovery requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Trace the existing deployment/automation path and define requested operational behavior with measurable checks.
2. Implement idempotent configuration and bounded scripts using minimum identity/network permissions and controlled artifacts.
3. Validate syntax/plans and safe test environments before any authorized rollout; verify health and recovery explicitly.

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
