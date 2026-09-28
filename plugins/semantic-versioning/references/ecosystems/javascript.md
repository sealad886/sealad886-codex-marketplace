# JavaScript and TypeScript

Read when npm package metadata, workspaces, or JavaScript release tooling owns versions.

## Sources and ownership

`package.json.version` becomes the packed package version. The package manager owns its lockfile; run its normal lock update after native versioning. `private: true` excludes a package from publication but does not imply its changes cannot affect consumers. Type declarations, exports maps, supported engines, peer dependency requirements, and CLI behavior are contracts.

Use the repository's npm, pnpm, or Yarn version and lock format. npm/Yarn workspaces use the root `workspaces` field; pnpm also uses `pnpm-workspace.yaml`. The root can remain private while child packages publish independently. Existing Changesets intent is the owner until its version command applies releases; avoid additionally running `npm version`.

## Example and checks

[Minimal package and workspace](../../examples/javascript/package.json). From the simple package run `npm test` then `npm pack --ignore-scripts --json`. Read `package/package.json` from the produced tarball and compare name/version/files to the release record. TypeScript projects must also build declarations and verify the packed exports resolve.

For the workspace, choose one package manager and generate its lockfile. npm: `npm install --package-lock-only --ignore-scripts`, then `npm pack --workspace @example/core --ignore-scripts --dry-run`. pnpm and Yarn variants need their pinned manager and native install/pack commands; do not keep three competing lockfiles. With pnpm/Yarn workspace protocol dependencies, verify published dependencies were rewritten to usable registry ranges.

For Changesets, configure `fixed` for packages that always release together; `linked` synchronizes versions when they release but does not force every linked package to publish. Empty groups support independent releases. Review dependent package bumps and internal ranges before publication.

## Sources

[Package metadata](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/), [pnpm workspaces](https://pnpm.io/workspaces), [Yarn workspaces](https://yarnpkg.com/features/workspaces), [Changesets configuration](https://github.com/changesets/changesets/blob/main/docs/config-file-options.md).
