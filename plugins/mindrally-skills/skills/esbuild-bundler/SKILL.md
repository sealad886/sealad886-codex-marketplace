---
name: esbuild-bundler
description: "Use when configuring esbuild entries, loaders, targets, splitting, plugins, watch/serve, or production output."
---

# esbuild Bundler

## When to invoke

Use when configuring esbuild entries, loaders, targets, splitting, plugins, watch/serve, or production output. Preserve the repository's established stack and conventions.

## Inputs and evidence

Inspect esbuild version, package module type, TypeScript config, runtime/browser targets, dependency externals, and intended public bundle inputs. Identify installed versions, affected callers,
existing tests, and the user's requested behavior before editing.

## Workflow

1. Define entry/output/platform/format and inspect which files, dependencies, and environment values enter the bundle.
2. Implement version-correct context/build options and narrow plugins without embedding secrets or unsupported runtime assumptions.
3. Run separate type checks and inspect/test emitted artifacts, source maps, runtime loading, and watch-context cleanup.

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
