---
name: python-uv
description: "Use when managing uv project dependencies, lockfiles, environments, or PEP723 standalone Python scripts."
---

# Python Package Management with uv

## When to invoke

Use for managing uv project dependencies, lockfiles, environments, or PEP723 standalone Python scripts.

## Inputs and evidence

Inspect declared Python/tooling workflow, uv version, pyproject/lock/script metadata, interpreter availability and package-index trust. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use uv only where selected by repository or requested migration scope.
2. Update project dependencies with add/remove or script-specific metadata commands as appropriate.
3. Lock/sync/run using supported version flags and explicit environment/download policy.
4. Verify resolved changes and execute focused checks through the intended environment.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Resolved dependencies/lockfiles and selected environment are verified and relevant commands/tests use the intended interpreter.

## Must not

Do not silently download interpreters, alter global Python, or migrate dependency managers outside scope. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
