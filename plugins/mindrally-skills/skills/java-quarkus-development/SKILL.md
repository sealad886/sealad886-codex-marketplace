---
name: java-quarkus-development
description: "Use when building Java Quarkus REST services, configuration, persistence, observability, or native-image paths."
---

# Java Quarkus Development Best Practices

## When to invoke

Use for Java Quarkus applications and their JVM/native delivery paths.

## Inputs and evidence

Inspect Quarkus platform BOM, Java/toolchain, extension names, REST stack, configuration profiles, and native-build requirements. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use the existing platform-aligned extensions and development/test commands.
2. Implement typed configuration and CDI ownership, preserving blocking/reactive boundaries.
3. Integrate persistence, security, and observability through supported extensions.
4. Test the JVM artifact and, when in scope, the actual native or container artifact separately.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Quarkus tests validate configuration, REST authorization and persistence; claimed native/container behavior has artifact-specific evidence.

## Must not

Do not present a JVM test as native-image proof or prescribe native compilation for every deployment. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
