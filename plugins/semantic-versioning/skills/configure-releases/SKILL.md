---
name: configure-releases
description: Configure native version ownership, release PR automation and authorized version-source migrations for a project.
license: MIT
---

# Configure Releases

## When to invoke

Use when establishing or changing release configuration, CI, version ownership, package groups, or canonical version sources.

## Inputs and evidence

Inspect current release docs, CI, Git rules, manifests, native tool versions, registry identities and user authorization. Start from existing working automation. Read [policy worksheet](../../templates/release-policy.md) for decisions that need a recorded answer.

## Workflow

1. Read [core rules](../../references/core.md), then the matching ecosystem references below. Read [architectures](../../references/architectures.md) only for grouping/dependency/migration decisions.
2. Preserve an appropriate existing tool. For new supported GitHub projects choose Release Please; use Changesets for JS workspaces requiring explicit per-package intent. Resolve tool/API versions from current primary docs before editing.
3. Record exactly one version writer per release unit. Define release PR approval, channels, pre-1.0 policy, native metadata checks and publication authority. Configuration or credentials do not grant authority.
4. Select only the needed CI recipe from [CI guide](../../references/ci/README.md). Prepare a concrete local diff; keep templates inactive until deliberately copied into the consumer project under authority.
5. Configure exact release revision, scoped permissions, concurrency, immutable version handling, artifact retention and consumer verification. Inspect commands that can install, execute build scripts, commit, tag or publish.
6. For consolidation, back up original affected files locally and perform a scoped once-off conversion with native verification and restoration instructions. Remove duplicate active definitions within the authorized migration.
7. Validate configuration, build/package metadata and failure/recovery paths. Ask only for unresolved material policy choices or consequential effects outside authority.

- [JavaScript](../../references/ecosystems/javascript.md), [Python](../../references/ecosystems/python.md), [Rust](../../references/ecosystems/rust.md), [Go](../../references/ecosystems/go.md): read only for matching package types.
- [JVM](../../references/ecosystems/jvm.md), [.NET](../../references/ecosystems/dotnet.md): read for inherited/build-derived versions.
- [Mobile and Swift](../../references/ecosystems/mobile.md), [C/C++](../../references/ecosystems/cpp.md), [Ruby/PHP](../../references/ecosystems/ruby-php.md), [containers/charts/plugins](../../references/ecosystems/containers-plugins.md): read for the matching distribution.

## Outputs and handoff

Deliver the version-source map, native config/workflow diff, prerequisites, standing-authority boundaries, checks and migration/recovery instructions. Handoff to verify-release for readiness.

## Completion evidence

One owner per unit; examples match selected tool versions; local checks pass; hosted/registry prerequisites and unexecuted publication remain explicit.

## Must not

- Load all references or execute example workflows during inspection.
- Treat commit labels as proof, guess dynamic versions, rewrite unrelated files, or install global dependencies.
- Add a second version writer or repeat bumps from a pending version.
- Commit, push, tag, publish, deploy, change registry settings or delete releases beyond user authority.
- Claim static checks prove hosted publishing or agent behavior.
