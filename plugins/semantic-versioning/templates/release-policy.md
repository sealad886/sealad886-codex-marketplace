# Release policy worksheet

Record answers in existing repository release documentation. This worksheet is not executable authorization.

- Release units, public contracts, private packages, dependency edges and version groups.
- Canonical version source, generated mirrors and exactly one version writer per unit.
- Native tool and pinned version; update/plan/build/check commands with side effects.
- Baseline evidence, branch/tag pattern, registry/package identity, stable/prerelease channels.
- Pre-1.0 policy and explicit stability decision; runtime/ABI/schema compatibility policy.
- Release PR approval and publication trigger; required checks and exact source/artifact identity.
- Standing authority granted by the user: repository, branches, packages, registries, channels and effects; grant evidence and revocation path.
- Permissions, OIDC/app prerequisites, protected environment, recovery retention and consumer checks.

Default new GitHub projects to a reviewed release PR followed by publication under configured standing authority. Do not infer authority from this file or from credentials existing.
