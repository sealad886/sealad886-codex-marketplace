---
name: quarkus
description: "Use when developing Quarkus configuration, CDI, REST/data/security integrations, observability, or JVM/native artifacts."
---

# Quarkus

## When to invoke

Use for developing Quarkus configuration, CDI, REST/data/security integrations, observability, or JVM/native artifacts.

## Inputs and evidence

Inspect Quarkus platform BOM/extensions, Java target, configured REST/data stack, profiles, execution model and requested artifact type. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Extend platform-aligned application/configuration and CDI boundaries.
2. Implement validated authorized endpoints and transaction-safe data access.
3. Select supported observability/executor integrations without mixing deprecated extensions.
4. Run framework tests and actual built-artifact checks for any JVM/native/container claims.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Platform build and relevant REST/security/data tests pass; artifact-specific claims have actual runtime evidence.

## Must not

Do not claim native compatibility or non-blocking behavior from annotations/configuration alone. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
