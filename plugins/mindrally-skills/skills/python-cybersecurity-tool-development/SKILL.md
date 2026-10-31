---
name: python-cybersecurity-tool-development
description: "Use when building authorized Python security diagnostics, bounded network probes, secure command execution, or findings reporting."
---

# Python Cybersecurity Tool Development

## When to invoke

Use for building authorized Python security diagnostics, bounded network probes, secure command execution, or findings reporting.

## Inputs and evidence

Inspect explicit targets/actions/scope, Python/library versions, concurrency/rate limits, credential handling and evidence-retention requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Define a target allowlist and permitted diagnostic operations from user authorization.
2. Validate structured input and use safe process/network APIs with bounded resources.
3. Implement cancellation, backoff, redaction and distinguish observations from confirmed findings.
4. Test locally with synthetic targets and fixtures before authorized external probes.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Synthetic success/failure/cancellation tests prove scope limits, redaction, bounded resources and reproducible evidence.

## Must not

Do not expand scan targets, perform credential attacks/exploitation, or mutate target systems from skill invocation alone. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
