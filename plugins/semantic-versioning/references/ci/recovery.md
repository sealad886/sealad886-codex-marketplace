# Release recovery

Read after an interrupted, duplicated, conflicting, or partially published release. Record the release unit, source SHA, tag, package version, workflow/run identity, expected artifacts, registry identities, and existing digests before changing anything.

## Reconcile then act

| Observed state | Next action |
|---|---|
| Version PR exists, no release | Fix validation or release intent through the existing PR/tool. Do not increment merely because CI failed. |
| Release/tag exists, package missing | Verify tag resolves to the approved SHA. Reuse retained artifacts when available; otherwise rebuild the same SHA and verify metadata. Dispatch only the missing publisher with the same version. |
| Package/version exists | Read registry metadata and compare provenance and digest with retained artifact evidence. If identity is uncertain, stop; never overwrite or assume a name/version match proves identity. |
| Workspace partially published | Record each package separately. Verify published artifacts, then resume only missing members in dependency order. Use native tools' recovery features after readback, or a reviewed one-time invocation for the missing members. |
| Registry unavailable/auth denied | Treat state as unknown, not absent. Repair authorization/connectivity without changing version. |
| Same version holds different content | Preserve published artifact and tag. Prepare a corrective release with a new version and disclose the defect. |
| Tag moved or SHA mismatch | Stop publication; investigate and recover the immutable release identity. Never force-move the tag. |
| Duplicate jobs | Serialize by unit/channel, verify registry identity, and mark already completed work as observed success; do not blindly repeat publishing. |

Example readbacks: `npm view PACKAGE@VERSION dist --json`; PyPI's project/version JSON endpoint; `cargo info CRATE@VERSION`; NuGet version metadata/download; GitHub release asset listing; OCI manifest digest and Helm pull digest. Downloaded artifacts are untrusted data: inspect without executing install hooks. Distinguish package registry state from GitHub Release state.

The supplied Rust loop intentionally stops if a previously published member conflicts. For partial recovery, verify the existing crate artifact/provenance, then invoke `cargo publish --locked --package <missing-crate>` from the original SHA for each missing crate in original order. Do not edit `release-order.txt` in the release checkout to bypass validation. Changesets may identify missing versions natively, but first reconcile existing versions because registry existence alone does not establish content identity.

A normal Release Please rerun may produce no new `release_created` output; use the publisher's manual dispatch with recorded SHA/tag/version, not a fake commit to generate another version. Dispatch from protected `main`; the publisher checks the release SHA is an ancestor and the tag matches. The environment approval must cover the exact recovery scope.

## Promotion and emergency patches

Promote prereleases under the native tool's policy; package versions and channel aliases are separate effects. Moving npm `latest`, a deployment pointer, or an OCI convenience tag needs authority even if no bytes change. Build metadata does not create a higher SemVer precedence.

Create emergency fixes from the supported maintenance line, choose that line's baseline, and backport intentionally. Do not release an unrelated newer major from `main`. Adapt branch/environment/concurrency rules together before using the templates on another release branch.

## Completion evidence

Read back package name/version, registry URL, artifact digest, source revision/provenance, and release/tag status. Install or consume the published artifact in a disposable environment when authorized. Retain checksums, test results and provenance with the release. CI green proves job completion, not consumer functionality. Generate SBOMs with the ecosystem's existing supported tool and attach them to the same immutable artifact identity; avoid treating an SBOM as proof of reproducible builds.

## Retained artifact lifetime

The npm, Python, NuGet and Helm templates upload package bytes, `SHA256SUMS`, and `source-revision.txt` **before** publication. Artifact names contain the source SHA and workflow attempt; retention is 14 days. A failed upload blocks publication. Download from the original trusted workflow run, verify the recorded SHA and checksums, and use those exact package bytes for a scoped recovery. The ordinary publish workflow rebuilds on dispatch; it does not automatically download a previous run's artifacts. Use a reviewed one-time native publish invocation for retained artifacts when exact-byte recovery is required.

GitHub Actions retention is temporary and repository policy may shorten it. Preserve release evidence in durable approved storage before expiration. Once bytes expire, a rebuild from the same commit is not proof of identical bytes: compare reproducibility evidence or record that limitation. GoReleaser's published GitHub release archives/checksums provide native retained artifacts. Rust publication runs Cargo's native packaging/verification; the template does not upload `target/package` between sequential crate publications, so retain successful crate artifacts from the registry and note missing prepublication build evidence on failure. The OCI image is retained by registry digest after push; only the Helm archive is retained by Actions before push. Registry garbage collection and retention policies still apply.
