---
name: java
description: "Use when developing Java language features, application modules, concurrency, persistence boundaries, or enterprise services."
---

# Java

## When to invoke

Use for Java development independently of a particular enterprise framework.

## Inputs and evidence

Inspect build toolchains, Java release target, preview flags, framework BOMs, module boundaries, and test conventions. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Choose language features supported by the configured release and deployment runtime.
2. Implement cohesive domain interfaces and explicit validation/error contracts.
3. Use the project’s existing Spring, Quarkus, Jakarta, or plain-Java architecture only where relevant.
4. Run compiler, unit/integration checks, and profiling for the changed behavior.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

The declared toolchain compiles/tests the change and framework-specific integration behavior is checked where used.

## Must not

Do not assume every Java application uses Spring or upgrade language/framework versions as an incidental change. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
