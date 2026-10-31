---
name: azure
description: "Use when implementing Azure infrastructure, managed identity, Pipelines, monitoring, or AKS workloads."
---

# Azure Cloud Development

## When to invoke

Use when implementing Azure infrastructure, managed identity, Pipelines, monitoring, or AKS workloads. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect Azure resource scope, IaC/pipeline versions, identities, RBAC, network boundaries, availability and cost requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Review the current resource topology and proposed Bicep/ARM/Terraform plan against requested behavior.
2. Implement configuration, identities, least-privilege access, health signals, and workload-appropriate deployment controls.
3. Validate configuration and plans locally; test authorized environments with explicit identity, rollout, and recovery evidence.

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
