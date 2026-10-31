---
name: python
description: "Use when developing Python application code, automation, data processing, or version-aware web services."
---

# Python

## When to invoke

Use for developing Python application code, automation, data processing, or version-aware web services.

## Inputs and evidence

Inspect Python/runtime constraints, declared environment/lockfiles, public interfaces, frameworks, I/O behavior and test conventions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use the existing project environment and supported language/dependency APIs.
2. Implement clear data/resource ownership and explicit validation/error contracts.
3. Select synchronous, asynchronous or worker execution from actual blocking/concurrency needs.
4. Run relevant formatting/static and behavioral checks without unrelated dependency changes.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Supported interpreter tests establish changed behavior, resource cleanup and relevant framework integration.

## Must not

Do not install dependencies globally or introduce an async/framework rewrite without task need. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
