---
name: security-devsecops
description: "Use when integrating security review, secret/dependency checks, CI trust boundaries, or evidence-based vulnerability remediation."
---

# Security throughout delivery

## When to invoke

Use when integrating security review, secret/dependency checks, CI trust boundaries, or evidence-based vulnerability remediation.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect repository security policy, trust boundaries, CI permissions, dependency sources, configured scanners, and finding evidence.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Map the change to concrete security requirements and existing delivery gates.
2. Run available scoped checks and confirm actionable findings at their owning boundary.
3. Fix root causes, preserve gates, and document verification and unresolved exposure.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Record exact source/artifact revision, tool versions, findings triage, regression checks, and unavailable scanner/runtime coverage.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
