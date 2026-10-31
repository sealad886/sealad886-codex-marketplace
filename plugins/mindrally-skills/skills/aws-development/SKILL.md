---
name: aws-development
description: "Use when implementing AWS Lambda, SAM/CDK infrastructure, DynamoDB access, API Gateway, or Step Functions."
---

# AWS Development Best Practices

## When to invoke

Use when implementing AWS Lambda, SAM/CDK infrastructure, DynamoDB access, API Gateway, or Step Functions. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect runtime/architecture compatibility, IaC ownership, event source semantics, IAM policies, access patterns, quotas, and authorized account. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Inspect the service contract and infrastructure diff; choose runtime, architecture, capacity, and workflow type from evidence.
2. Implement least-privilege access, input validation, idempotent processing, bounded retries, and redacted observability.
3. Validate IaC and unit contracts locally; perform authorized integration checks separately and report cost/runtime limits.

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
