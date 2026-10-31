# Turborepo tasks and cache correctness: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Workspace configuration belongs to the selected package manager; pnpm uses pnpm-workspace.yaml, and workspace:* support is manager-specific.

- ^build refers to dependency-package builds, while package#task and same-package dependencies have distinct graph meanings.

- Declare every required output and avoid caching disposable tool caches unless intentionally supported. A successful cache hit with missing artifacts is a defect.

- Include behavior-affecting environment variables and files in hashes; pass-through credentials must not accidentally cause cross-environment artifact reuse.

- Persistent dev tasks should not be cached as ordinary completed artifacts; select watch behavior supported by installed Turbo.

- Remote caching can upload artifacts and logs; inspect secrets/private data, provider permissions, and user authority before enabling it.

- Filters/dry runs help scope work but do not replace needed dependency validation; compare actual graph and outputs.

- Root apps/packages/tooling layout and TypeScript references are conventions, not mandatory Turbo architecture.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Turbo caches task outputs based on declared inputs/environment and needs deterministic task behavior.](https://turborepo.com/docs/crafting-your-repository/caching)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
