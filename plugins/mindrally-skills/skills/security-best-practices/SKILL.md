---
name: security-best-practices
description: "Use when reviewing or implementing input handling, authorization, secrets, sessions, injection defenses, or backend security controls."
---

# Secure application boundaries

## When to invoke

Use when reviewing or implementing input handling, authorization, secrets, sessions, injection defenses, or backend security controls.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect trust boundaries, threat model, auth/session design, data sensitivity, database APIs, logs, and existing security policy.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Trace untrusted input to sensitive reads/writes and output contexts.
2. Apply established validation, parameterization, authorization, and secret primitives.
3. Verify concrete misuse cases and report residual risk with supporting evidence.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Run focused negative tests for authorization, input/output contexts, CSRF/session boundaries, and sensitive-log exposure; separate findings from hypothetical hardening.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
