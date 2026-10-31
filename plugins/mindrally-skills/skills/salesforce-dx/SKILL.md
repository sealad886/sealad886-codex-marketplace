---
name: salesforce-dx
description: "Use when managing Salesforce DX source, scratch-org configuration, metadata validation, packaging, or sf CLI workflows."
---

# Salesforce source-driven workflow

## When to invoke

Use when managing Salesforce DX source, scratch-org configuration, metadata validation, packaging, or sf CLI workflows.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect sf CLI/plugin versions, sfdx-project.json, target-org identity, manifests, .forceignore, source tracking, and package lineage.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Verify the intended org and source scope before any remote operation.
2. Prepare metadata changes and use supported preview/validation commands.
3. Run applicable tests and inspect deployment/retrieval results before publishing or promoting packages.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Validate source/manifests and run scoped metadata/Apex/LWC checks in an authorized org; report target and source-tracking limits.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
