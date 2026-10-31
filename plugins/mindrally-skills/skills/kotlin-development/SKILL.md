---
name: kotlin-development
description: "Use when implementing Kotlin domain models, null safety, functions, collections, or coroutine-backed behavior."
---

# Kotlin Development Best Practices

## When to invoke

Use for implementing Kotlin domain models, null safety, functions, collections, or coroutine-backed behavior.

## Inputs and evidence

Inspect Kotlin/platform versions, Gradle settings, nullability boundaries, coroutine scopes/dispatchers, and local style. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Model valid states with Kotlin types and explicit nullability.
2. Implement cohesive functions using inference and language idioms where clear.
3. Keep mutation and coroutine lifetimes owned; propagate cancellation.
4. Test domain behavior, platform interoperability, and concurrency/error paths.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Configured Kotlin targets compile and tests cover nullability/domain invariants and coroutine cancellation where affected.

## Must not

Do not use global unowned coroutines or force all values into explicitly annotated wrappers. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
