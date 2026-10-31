---
name: gcp-development
description: "Use when implementing Google Cloud Run/functions, Firestore, BigQuery, Storage, Terraform, IAM, or operational telemetry."
---

# GCP Development Best Practices

## When to invoke

Use when implementing Google Cloud Run/functions, Firestore, BigQuery, Storage, Terraform, IAM, or operational telemetry. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect target projects/regions, service/runtime/SDK generations, IaC/state ownership, IAM identities, data policies, limits and cost authority. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define workload/data contracts and inspect existing infrastructure plans, service identity, rollout and recovery requirements.
2. Implement bounded runtime/data access, least privilege, explicit consistency/idempotency, safe secrets and observability.
3. Validate source/IaC locally and perform authorized emulator/hosted tests separately with revision, data and cost evidence.

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
