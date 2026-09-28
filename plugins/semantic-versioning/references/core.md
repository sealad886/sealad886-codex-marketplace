# Release assessment rules

Read when assessing impact. This file is the shared policy; load once per task.

## Contract and evidence

[Semantic Versioning 2.0.0](https://semver.org/) requires a public API and immutable published versions. Record the actual supported consumer contract: library API/ABI, CLI arguments and exit codes, configuration defaults, schemas, persistent formats, protocol behavior, supported runtimes, app behavior, or agent/plugin instructions. Internal refactoring alone does not imply a release. A security fix can still break a contract; never classify it as patch merely because it fixes a vulnerability.

Inspect the cumulative diff from the release baseline, tests, documentation, and native release intent. Commit types and PR labels are hints, not authority. Explain conflicting evidence and correct release intent within the granted scope. Do not invent an API comparison result. Native API/ABI tools supplement review; their silence cannot prove all behavioral compatibility.

## Release units and baselines

Map package identity, source root, manifest/version owner, generated mirrors, internal dependencies, registry, tag prefix, branch, channel, and public contract. Private workspace helpers may have no independent release. One application may produce several artifacts sharing a version but different build identifiers.

Use reachable tags belonging to that unit and branch, corroborated with native release state and published package evidence where accessible. The highest tag across a repository is not a baseline. A tag is a candidate, not proof of publication. Missing/shallow history, multiple plausible tags, first releases, and tag/registry disagreement remain explicit gaps. Do not fetch without reconciling scope; do not guess a first baseline.

## Impact

- none: no released contract/artifact impact and native policy requires no release.
- patch: compatible correction.
- minor: compatible added behavior or deprecation.
- major: incompatible public behavior, removal, or supported-platform change.

For a new pre-1.0 policy, breaking changes and features increment minor; fixes increment patch. Record this as a project policy, not a SemVer requirement. Existing explicit pre-1.0 policy wins. Declaring stability at 1.0 requires an explicit decision.

Compute the pending version from the immutable released baseline and cumulative impact, never by repeatedly incrementing the current pending number. Take the greatest surviving impact per release unit; a reverted change cancels only its own effects. Do not silently reduce reviewed release intent or overwrite concurrent work: reconcile the reason first. Re-run native planning after a rebase or changed dependency graph.

## Ownership

Exactly one mechanism writes release numbers per unit. For Release Please, maintain accepted Conventional Commit/release intent and let its release PR write numbers. For Changesets, maintain the affected package changesets and let its version command reconcile them. For tag-derived versions, maintain release intent without editing generated version files. When the agent owns static versions, use the repository's native exact-version command and inspect the diff and lockfile consequences. Avoid commands that also commit/tag/publish unless explicitly authorized.

## Channels and identity

Stable versions outrank prereleases of the same core. Numeric prerelease identifiers have numeric ordering and no leading zeroes. Build metadata does not change SemVer precedence. Ecosystem normalization and store build numbers are distinct contracts; consult the matching reference before mapping them. Promotion must verify the chosen core, final source and rebuilt artifacts; it does not assume prerelease bytes equal stable bytes.

Backports compare against the maintenance branch's own release baseline. Preserve separate stable/preview channels. Never retag or overwrite a published version. If an existing release is wrong, propose a new corrective version with migration notes.

## Handoff

Report unit, baseline evidence, cumulative impact and rationale, release owner, proposed version/channel, local changes, validation, and missing release authority or evidence. Uncertainty blocks a final release claim, not independent authorized local work.
