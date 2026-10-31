---
name: salesforce-development
description: "Use when implementing Apex, bulk triggers, SOQL, Lightning Web Components, or Salesforce metadata security."
---

# Salesforce Apex and Lightning

## When to invoke

Use when implementing Apex, bulk triggers, SOQL, Lightning Web Components, or Salesforce metadata security.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect API versions, org features, object/field permissions, sharing model, trigger contexts, LWC targets, and test setup.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Define record/field authorization and bulk transaction behavior.
2. Implement bulk-safe Apex and target-correct Lightning components using existing metadata.
3. Validate positive, negative, bulk, and permission-sensitive behavior in an authorized test org.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run Apex and LWC tests plus metadata validation in an authorized environment; state org/deployment checks not executed.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
