# GitHub Actions release examples

Read when implementing a GitHub release workflow. Load only the chosen template and its ecosystem reference. These are inactive reference implementations; none has been published from this repository or proven against a live registry.

## Assemble one workflow

1. Copy [Release Please coordinator](../../templates/workflows/release-please.yml.template) to the target repository as `.github/workflows/release.yml`.
2. Copy one publisher below as `.github/workflows/release-publish.yml`. The default tag contract is `vVERSION`; adapt tag validation and output routing together for component-prefixed tags. Its reusable inputs are `revision` (full commit SHA), `tag` (existing tag), and `version` (expected package version). Manual dispatch supports an explicitly approved recovery using the same identity.
3. Add the native configuration from [release tools](../tools/release-tools.md), preserving the existing owner. The coordinator's outputs cover a root package only. For independently released paths, create one publisher call per released path using the corresponding `<path>--release_created`, `<path>--sha`, `<path>--tag_name`, and `<path>--version` outputs. Do not reuse root outputs for every package.
4. Protect `main`, require tests for release PRs, and configure a `release` environment permitting only `main`. Record standing authorization and approved package/registry/channel scope. Require environment reviewers when that is the agreed approval point. A repository configuration does not grant the agent authority.
5. Remove unused caller permissions: `id-token: write` for npm/PyPI, `packages: write` for GitHub Maven/GHCR, and `contents: write` for GoReleaser. A reusable workflow cannot raise permissions beyond its caller. Scope inherited secrets to the called workflow's declared secrets or environment.
6. Configure each registry publisher identity for the actual caller/called workflow and environment according to that provider's OIDC policy. Run a disposable staging-project release before production enablement.

Release Please runs on a main-branch push and passes the resulting release SHA directly to publication. This avoids depending on a second tag/release event. String outputs are compared explicitly with `'true'`.

For npm, the publisher accepts `dist_tag` (default `latest`). Stable releases can use that default; prereleases must select an authorized preview channel such as `next` or `beta`. Add `dist_tag: next` under the coordinator publisher job's `with` only when selecting the npm publisher for that preview policy; other publishers do not declare this input. Manual recovery dispatch exposes the same field. The publisher rejects a prerelease on `latest` before building and passes the selected tag explicitly to npm. Channel selection is part of standing publication authority, not permission granted by an input. [npm distribution tags](https://docs.npmjs.com/adding-dist-tags-to-packages/).

Go publication binds `GORELEASER_CURRENT_TAG` to the verified input tag. This prevents GoReleaser from choosing another tag pointing to the same commit. [GoReleaser custom tag selection](https://goreleaser.com/resources/cookbooks/set-a-custom-git-tag/).

Go additionally requires Release Please `draft: true`, a draft targeting the exact release SHA, and GoReleaser checksums named `checksums.txt`. Its publisher creates an absent tag only for that verified draft, leaves the release draft while uploading, downloads/checks assets, then publishes the draft. This supports repositories enforcing GitHub immutable releases. An already published release or populated draft fails before asset mutation; partial recovery requires review of existing asset identity. Standing authorization must cover creating the tag, uploading assets and publishing the completed draft.

GitHub currently allows certain `GITHUB_TOKEN`-generated pull-request events to create approval-required runs; other generated events remain suppressed except documented dispatch exceptions. Check the repository's current policy and explicitly approve release-PR CI where needed, or configure a narrowly scoped GitHub App token. Do not weaken required checks or assume all token events behave alike. [GitHub trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Choose the publisher

| Template | Contract and prerequisites | Validation |
|---|---|---|
| [npm](../../templates/workflows/npm.yml.template) | Root `package.json`/lockfile; Node 22.14.0 and npm 11.5.1; public npm package; trusted publisher; `npm test`. Stable channel defaults to `latest`. | Version in manifest and packed tarball, tests/build, SHA-256. |
| [Python](../../templates/workflows/python.yml.template) | Python 3.12.9, build 1.2.2.post1, twine 6.1.0; one wheel and sdist; PyPI trusted publisher. Backend/build dependencies must be constrained in project configuration. | `twine check`; normalized wheel and sdist versions using packaging 24.2; hashes. |
| [Rust](../../templates/workflows/rust.yml.template) | Fixed-version workspace; checked-in exact `rust-toolchain.toml`, Cargo.lock, `release-order.txt` containing publishable crate names in dependency order; scoped `CARGO_REGISTRY_TOKEN`. | Metadata versions and order, workspace tests, Cargo's package verification. |
| [Go](../../templates/workflows/go.yml.template) | Root module with `vVERSION` tags; pinned Go directive/toolchain; GoReleaser v2.8.2 with v2 config and explicit build targets. | Source/tag check, Go tests; GoReleaser archives/checksums and release assets. |
| [NuGet](../../templates/workflows/nuget.yml.template) | .NET 8.0.408, checked-in restore lockfiles, uniform package versions, scoped expiring `NUGET_API_KEY`. Prefer provider-supported trusted publishing when available and validated for the target account. | Tests, every generated nuspec version, package hashes. |
| [Maven](../../templates/workflows/maven.yml.template) | Temurin 21.0.6+7, checked-in Maven wrapper with pinned distribution/checksum, root project version, GitHub Packages `distributionManagement` ID `github`. | Effective native version and Maven `verify`; release process must cover child versions. |
| [Gradle](../../templates/workflows/gradle.yml.template) | Temurin 21.0.6+7, wrapper distribution checksum, Maven Publish configuration for GitHub Packages; `printReleaseVersion` prints `RELEASE_VERSION=<project.version>`. | Gradle `check`, version contract, native `publish`. |
| [OCI and Helm](../../templates/workflows/oci-helm.yml.template) | Docker available on Ubuntu runner; Helm 3.17.2; chart named `demo` in `chart/`, app/chart share release version; GHCR packages enabled. Customize all names before adoption. | Chart lint/version, source labels, image digest and chart checksum. |

Versions are explicit example baselines, not a claim that they are newest. Update tool pins and project constraints together after checking primary release notes; resolve action revisions to full immutable SHAs. `ubuntu-24.04` is a maintained hosted image label, not an immutable build environment. Projects needing reproducibility should pin the container digest and compiler dependencies as well.

The Maven/Gradle examples publish to GitHub Packages. Maven Central requires its own account, signing, staging, and Central publisher plugin configuration; see [Central publishing requirements](https://central.sonatype.org/publish/requirements/). Do not claim this GitHub example configures Central.

Rust's publisher supports a fixed-version release. For independent crate versions, feed the expected version for each release unit and check it separately. Never force all crates to one version to fit this template. Maven/Gradle likewise require per-module checks for independent versions.

## Alternative version owners

[Changesets workflow](../../templates/workflows/changesets.yml.template) is standalone, using npm workspaces and Changesets CLI v2 with action v1. Pin the CLI in the project lockfile; define `version-packages` and `release` scripts as shown in the tools reference. The action creates/updates the version PR and publishes versioned packages from its merged commit. Private packages remain private. Do not add Release Please to the same packages. The action needs credential persistence for its own native branch/tag operations; run only trusted `main` code.

[Existing semantic-release workflow](../../templates/workflows/semantic-release.yml.template) is standalone. Preserve its native commit-driven version ownership. The configured main-branch merge is its release boundary, not a separate version PR. Use an installed, locked semantic-release version and npm plugin supporting OIDC; verify that their Node engine requirements accept the selected runner. Permissions for comments/releases follow the configured plugins; remove unused permissions and plugins. Do not add a second version writer to emulate a release PR.

## Failure and retry

See [recovery](recovery.md). The publishers deliberately fail on existing immutable package versions rather than hiding conflicts with `--skip-existing`, `--skip-duplicate`, or forced upload. A rerun after complete success may therefore fail with an existing-version error: that does not invalidate the earlier release. Confirm registry evidence before deciding what to resume.

The container example checks absence before push, but registries with mutable tags can still race another publisher. Restrict publisher credentials and use registry immutability where available. Concurrency protects this workflow only; it cannot serialize external publishers.

Source evidence: [Release Please outputs](https://github.com/googleapis/release-please-action), [npm OIDC prerequisites](https://docs.npmjs.com/trusted-publishers/), [PyPI trusted publishers](https://docs.pypi.org/trusted-publishers/), [Cargo publish](https://doc.rust-lang.org/cargo/commands/cargo-publish.html), [GoReleaser Actions](https://goreleaser.com/customization/ci/actions/), [NuGet publication](https://learn.microsoft.com/en-us/nuget/nuget-org/publish-a-package), [Helm OCI registries](https://helm.sh/docs/topics/registries/). Consulted 2026-09-28.
