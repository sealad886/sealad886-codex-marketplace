# Native release-tool selection and configuration

Read when selecting or configuring the version owner. Inspect installed versions, lockfiles and existing automation first. Use one writer for a release unit. Preserve a suitable existing tool.

| Situation | Default |
|---|---|
| GitHub project with a supported Release Please strategy | Release Please manifest mode and a reviewed release PR. |
| JavaScript monorepo needing per-package intent | Changesets with explicit changeset files. |
| Existing semantic-release project | Retain semantic-release and its declared plugins/branch channels. |
| Unsupported or specialized packaging | Existing native release tool, or an explicit reviewed version change plus native packaging. |

Native tools remain authoritative for generated files, lockfiles, internal dependency ranges and package publication. A release tool cannot infer all contract breaks from commit messages; the agent must reconcile actual changes with recorded intent.

## Release Please

For the root npm example, save as `release-please-config.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "node",
      "include-component-in-tag": false,
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": false
    }
  }
}
```

Save the verified previously released version in `.release-please-manifest.json`:

```json
{ ".": "0.1.0" }
```

These values record an existing baseline, not authorization to claim a release exists. For a first release, set `bootstrap-sha` or the supported initial-version mechanism deliberately after inspecting history. Switch to `python`, `rust`, or another **currently supported** strategy only after checking what that strategy updates. Inspect the resulting release PR; additional files, shared workspace inheritance, dynamic metadata and lockfiles require explicit native configuration. Do not choose `simple` merely to bypass missing package updates.

For supported heterogeneous monorepos, use distinct package paths and native strategies in `packages`. Configure tag/component names to avoid collisions and map each path's release outputs to its own publisher. Release Please's manifest tracks released versions; do not add another plugin state file. [Manifest mode](https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md), [configuration schema](https://github.com/googleapis/release-please/blob/main/schemas/config.json), [action inputs/outputs](https://github.com/googleapis/release-please-action).

For the Go binary publisher, set `"draft": true` in that package's Release Please configuration. GitHub immutable releases lock assets when published, so Release Please must leave a draft until GoReleaser uploads and verifies all assets. The Go publisher verifies the draft's exact target SHA and creates the missing tag through GitHub's create-ref API if draft creation deferred it; it never overwrites a tag. Run GoReleaser with `--draft`, configure checksums as `checksums.txt`, and retain existing draft releases. Finalization occurs only after uploaded checksums match local checksums and downloaded assets pass checksum verification. Already populated drafts require reviewed recovery. Do not add newer `force-tag-creation` configuration without checking the pinned Release Please version supports it. [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases), [GoReleaser release configuration](https://goreleaser.com/customization/publish/scm/).

## Changesets

The shipped action is v1, paired deliberately with Changesets CLI v2. Pin an exact verified CLI v2 release in devDependencies and the native lockfile. Upstream action main targets v2/CLI v3; do not mix those APIs. Root scripts:

```json
{
  "scripts": {
    "version-packages": "changeset version && npm install --package-lock-only",
    "release": "changeset publish"
  }
}
```

A minimal `.changeset/config.json` for independent packages:

```json
{
  "$schema": "https://unpkg.com/@changesets/config@2.3.1/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

Use `fixed` only for packages intentionally released with one version. `linked` does not mean every member publishes every time. Keep root workspaces private and give each public package its own name/version. Changeset files state bump and rationale; merge those intents rather than manually incrementing versions repeatedly. Use the native pre-release enter/exit workflow for prereleases. Review dependent bumps and peer ranges before merging.

For pnpm or Yarn, replace npm commands with the project's pinned package manager and frozen install workflow; use native workspace protocols and lock regeneration. Do not regenerate a pnpm lockfile with npm. [Changesets v1 action](https://github.com/changesets/action/tree/maintenance/v1), [configuration](https://github.com/changesets/changesets/blob/main/docs/config-file-options.md).

## Existing semantic-release

Keep the locked tool/plugins and branch rules. A minimal npm configuration (`.releaserc.json`) is:

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/npm",
    "@semantic-release/github"
  ]
}
```

Confirm the installed npm plugin supports trusted publishing and its Node engine requirement. Configure branch/channel support in the native tool for maintenance and prerelease branches. Treat dry-run as evidence of analysis only: plugins may still perform reads and authentication checks. Never assert publishing passed because dry-run passed. [CI configuration](https://semantic-release.gitbook.io/semantic-release/usage/ci-configuration), [npm plugin](https://github.com/semantic-release/npm).

## Other native integrations

- **Rust:** `cargo release` or release-plz may own workspace version/dependency edits. A fixed-version sample can use native Cargo publishing with an explicit dependency order. Check `cargo metadata` and package contents; do not parse manifests with regex to rewrite versions.
- **Go:** use tag/module paths as version sources. GoReleaser packages the checked-out tag; configure `version: 2`, explicit builds and checksums in `.goreleaser.yaml`. The shipped root-module workflow expects `vVERSION`; nested modules require path-specific tags and package scope. [GoReleaser configuration](https://goreleaser.com/customization/).
- **JVM:** preserve Maven `${revision}`/flatten or Gradle's chosen source. Multi-module publishing must verify effective versions of every artifact. GitHub Maven distribution IDs must match the CI server ID. Gradle's example contract can be implemented with `tasks.register("printReleaseVersion") { doLast { println("RELEASE_VERSION=${project.version}") } }` in Kotlin DSL.
- **.NET:** preserve MSBuild, Nerdbank.GitVersioning or MinVer ownership. Verify `.nuspec` and assembly/file versions independently; do not overwrite generated assembly metadata.

Consulted primary sources on 2026-09-28. Recheck the actual pinned release before introducing configuration fields.
