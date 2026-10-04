# Common operating contract

Read this once per task. Load only references relevant to the requested change. Source facts and refresh triggers live in [research](research.md).

## Repository and authority

Inspect instructions, Git status/branch/worktrees, manifests, lockfiles, scripts, target configuration, tests and existing design before edits. Preserve unrelated changes. Use the current task branch or a safe local branch; worktrees require explicit authorization. Keep one active checklist step for multi-stage work. Build/debug authority does not grant credential access, signing, notarization, publishing, deployment, data deletion or device reset. Inspect hooks and wrappers before execution; a build command can bundle, sign or upload. Stop only dependent work when authority or evidence is missing.

Use the repository's package manager and installed local CLI. Read package.json, Cargo.toml/Cargo.lock, rust-toolchain configuration and native SDK/build files before choosing commands. Keep CLI, Rust Tauri crates and JS bindings on compatible major versions; plugin crate/JS compatibility comes from their own releases, not a requirement that all patch numbers match. Reuse environments; no global installations or package-manager migration by default.

## Discovery receipt

Record the revision, dirty scope, framework, package manager, Tauri/CLI/plugin versions, requested targets, host/toolchain, existing target projects and available test tools. Use installed CLI help and primary documentation for exact flags. Context7 is optional; when available resolve the appropriate Tauri 2 library and query the actual topic. If unavailable, use official docs/upstream source and record uncertainty. Never invent MCP tool names or assume a source plugin is installed.

## Feature and evidence matrix

For each requested feature record target, implementation owner (frontend, Rust, official plugin, native bridge or remote API), permission, persistence/lifetime, behavior when unavailable and verification method. Desktop support does not imply mobile support. A browser deployment is a separate environment with no Rust core; require a real browser implementation or an explicit unavailable state for native features. Introduce one narrow service boundary only where these distinct implementations actually exist.

Evidence levels: static/source → unit/mocked → browser rendered → packaged native integration → simulator/emulator → physical device → signed channel artifact → installed/released outcome. Passing one level never proves the next. Report per-target verified, failed, blocked or not run with reason, exact artifact and bounded residual uncertainty.

## Handoff

Lead with outcome, behavior/files changed, commands/results, platform/build/device identity, remaining gaps and branch/commit/publication status. Keep screenshots, traces and temporary captures in a unique run folder outside package source. Redact secrets and personal data. Clean up only processes, listeners and temporary instrumentation owned by this task; preserve user sessions and artifacts.
