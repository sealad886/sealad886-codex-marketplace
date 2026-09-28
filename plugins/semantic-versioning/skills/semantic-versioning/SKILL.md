---
name: semantic-versioning
description: Assess cumulative release impact and maintain native version intent during coding, before handoff, or when versions drift.
license: MIT
---

# Semantic Versioning

## When to invoke

Use after meaningful authorized code changes, when choosing a release version, or when manifest/tag/package versions disagree. Installation alone does not trigger every coding task; offer the [opt-in instruction](../../templates/agent-instructions.md) when requested.

## Inputs and evidence

Inspect project instructions, Git state, release docs, manifests, pinned tooling, tests, changed contracts and native release intent. The [inspector](../../scripts/inspect_repository.py) reports candidates only; it does not determine semantic impact or prove publication.

## Workflow

1. Read [core rules](../../references/core.md) once. Identify release units, public contracts, version writers, generated mirrors and verified baselines.
2. Load only the matching ecosystem reference below; read [architectures](../../references/architectures.md) for workspaces or multi-artifact products.
3. Inspect cumulative changes including relevant local work. Classify none/patch/minor/major with evidence, resolving disagreement with commit labels. Preserve unrelated changes.
4. Reconcile native intent with existing pending work. If CI owns numbers, update its native intent within authority. If the agent owns numbers, use an exact native version command after inspecting its side effects. Recompute from baseline; never increment an already pending number mechanically.
5. Use [check_version.py](../../scripts/check_version.py) for SemVer arithmetic only. Consult ecosystem rules for normalization, build numbers and generated metadata. Validate the actual package with native tools.
6. Hand configuration changes to configure-releases; hand publication/readiness to verify-release. Stop only dependent work when required evidence or authority is missing.

- [JavaScript](../../references/ecosystems/javascript.md), [Python](../../references/ecosystems/python.md), [Rust](../../references/ecosystems/rust.md), [Go](../../references/ecosystems/go.md): read only for matching package types.
- [JVM](../../references/ecosystems/jvm.md), [.NET](../../references/ecosystems/dotnet.md): read for inherited/build-derived versions.
- [Mobile and Swift](../../references/ecosystems/mobile.md), [C/C++](../../references/ecosystems/cpp.md), [Ruby/PHP](../../references/ecosystems/ruby-php.md), [containers/charts/plugins](../../references/ecosystems/containers-plugins.md): read for the matching distribution.

## Outputs and handoff

Report unit, baseline evidence, owner, impact/rationale, target/channel, changes, native checks and gaps. Use existing project records; no mandatory plugin state file.

## Completion evidence

Each affected unit has an evidence-backed decision; repeated assessment leaves the same pending version; generated metadata and native intent agree or unresolved drift is explicit.

## Must not

- Load all references or execute example workflows during inspection.
- Treat commit labels as proof, guess dynamic versions, rewrite unrelated files, or install global dependencies.
- Add a second version writer or repeat bumps from a pending version.
- Commit, push, tag, publish, deploy, change registry settings or delete releases beyond user authority.
- Claim static checks prove hosted publishing or agent behavior.
