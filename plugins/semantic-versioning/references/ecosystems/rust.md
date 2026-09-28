# Rust

Read when Cargo packages or workspaces release crates or binaries.

## Sources and ownership

A crate's `package.version` owns its published version unless `version.workspace = true` inherits `workspace.package.version`. Workspace inheritance is an explicit fixed-version choice; independent packages retain their own versions. Cargo.lock records resolution and must be regenerated natively. A path dependency also needs a registry version for publishing consumers.

Public Rust types, trait bounds, feature behavior, MSRV, and binary interfaces deserve impact review. Cargo's requirement interpretation for 0.x releases is distinct from a project's chosen pre-1.0 policy. Use existing cargo-release/release-plz configuration; do not introduce another automatic writer.

## Example and checks

[Two-crate workspace](../../examples/rust/Cargo.toml). `cargo metadata --no-deps --format-version 1` resolves inherited versions; `cargo test --workspace` validates behavior; `cargo package -p semver-example-core` verifies the first crate. Inspect the `.crate` archive's normalized Cargo.toml and original manifest.

Publish dependency crates before consumers, waiting for registry availability. This example's CLI cannot perform a normal registry-backed package verification until its example core crate exists in the selected registry. For offline structure checks use `cargo package -p semver-example-cli --no-verify` only with this limitation recorded; it does not prove dependency resolution. Do not publish the example names.

When updating the shared version, reconcile `workspace.dependencies` version requirements as well. For independent versions, propagate a dependency bump only when the existing range cannot express the required release or changed behavior requires a consumer release.

## Sources

[Cargo workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html), [publishing](https://doc.rust-lang.org/cargo/reference/publishing.html), [SemVer compatibility](https://doc.rust-lang.org/cargo/reference/semver.html).
