---
name: graalvm
description: "Use when building or diagnosing GraalVM native images, reachability metadata, framework AOT, or native performance."
---

# GraalVM

## When to invoke

Use when building or diagnosing GraalVM native images, reachability metadata, framework AOT, or native performance. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect GraalVM/JDK/framework/plugin versions, target OS/architecture/libc, dynamic features, build/runtime config, and deployment requirements. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Identify closed-world/reflection/resource/proxy/JNI requirements and use the framework current AOT build path.
2. Configure only necessary metadata and safe initialization, then build with the target toolchain and owned resources.
3. Test the actual native binary for critical code paths, TLS/resources/serialization, configuration changes, and measured startup/memory/throughput.

Load [implementation guidance](references/implementation.md) only for the selected
feature, API, or verification concern; follow its primary links for version details.

## Outputs and handoff

Report the changed behavior, affected files, checks and their actual outcomes,
and remaining limitations. Include relevant configuration or migration steps.

## Completion evidence

Verify the requested behavior at its public boundary, including a meaningful
failure case. Separate static review from executed tests and runtime acceptance.

## Must not

Do not change the stack, dependencies, or architecture merely to match examples.
Do not expose credentials or private data. External writes, deployments, paid
operations, and destructive changes require authority from the user's request.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
