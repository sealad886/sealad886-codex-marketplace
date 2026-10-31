# Build Multi-target Tauri Apps

Build, debug, test and prepare Tauri 2 apps for Windows, Linux, macOS, iOS and Android. Share frontend/domain behavior while checking native permissions, plugins, WebView differences and platform evidence. Optional browser deployment has explicit native-feature replacements or unavailable states.

Current package version: **0.2.0**. Marketplace package; publication is gated by PR review and CI, while native consumer acceptance requires separate target evidence. This original synthesis adapts capabilities from Build iOS Apps, Build Web Apps, Build macOS Apps and Test Android Apps. It does not copy their skill text or require them to be installed. [Original adaptation and research ledger](skills/.shared/research.md). The [2026-10-31 performance refresh](skills/.shared/performance/research.md) adds mobile-first responsiveness, battery, thermal and memory guidance from current primary sources.

## Skills

| Skill | Use |
| --- | --- |
| [tauri-app-builder](skills/tauri-app-builder/SKILL.md) | Start here for a new app or multi-target adaptation |
| [tauri-architecture](skills/tauri-architecture/SKILL.md) | Typed IPC, state, cancellation and persistence |
| [tauri-frontend](skills/tauri-frontend/SKILL.md) | Accessible responsive UI and rendered iteration |
| [tauri-native-build](skills/tauri-native-build/SKILL.md) | Target setup, build/run/debug and native integrations |
| [tauri-security](skills/tauri-security/SKILL.md) | Capabilities, custom commands, CSP, resource scopes and secrets |
| [tauri-testing](skills/tauri-testing/SKILL.md) | Rust/frontend tests, native E2E and mobile device QA |
| [tauri-performance](skills/tauri-performance/SKILL.md) | Mobile responsiveness, battery/thermal efficiency and memory ownership |
| [tauri-distribution](skills/tauri-distribution/SKILL.md) | Artifacts, CI, signing, updates and release preparation |

Shared references ship inside the skills tree and load by topic. Use only the workflow needed; no full lifecycle ceremony for a small edit.

## Example requests

- Build this existing Tauri app for macOS, Windows, Linux, iOS and Android; report target gaps.
- Adapt this frontend into a Tauri app while retaining its current framework.
- Fix Android keyboard/back behavior and verify the real installed app.
- Restrict this Rust command to the intended window and prove denied callers fail.
- Optimize this Tauri app's mobile launch and scrolling while checking battery and peak memory costs.
- Find background battery drain and stop unnecessary work without breaking resume or durable operations.
- Investigate memory growth after repeating this flow, with comparable captures and retaining-owner evidence.
- Prepare desktop packages and mobile release gates without publishing.

## Performance workflow

`tauri-performance` measures a reproducible user task, identifies the responsible
WebView/Rust/native layer, implements a bounded causal improvement, and compares
the result with correctness and resource guardrails. Its focused guides cover
[measurement and tools](skills/.shared/performance/measurement.md),
[energy/lifecycle](skills/.shared/performance/mobile-energy.md),
[memory ownership](skills/.shared/performance/memory.md), and a
[before/after receipt](skills/.shared/performance/receipt.md).

Use physical production-equivalent mobile captures for acceptance; browser,
emulator and debug profiles remain diagnostic. Power tools have device/OS and
attribution limits. This instruction package does not itself measure an app,
expose new native APIs, promise battery savings or require SDK installation.

## Prerequisites and boundaries

Use consumer repository's package manager, locked frontend/Rust dependencies and local Tauri 2 CLI. Selected native targets require their documented SDK/toolchain and authorized device. iOS requires full Xcode on macOS; Android requires matching SDK/NDK/JDK/Gradle and Rust ABIs. Windows/Linux/macOS packages require supported native build hosts and runtime libraries. No SDK installation is performed by this plugin.

Browser automation, Xcode tools, adb and profilers are optional capabilities detected at runtime. Missing tools have explicit fallback or not-run evidence; no invented tool APIs. Native Tauri plugins are dependencies of the consumer app, distinct from this Codex plugin.

Current WebdriverIO embedded automation supports desktop macOS, Windows and Linux; direct official tauri-driver supports Windows/Linux. Provider/version setup must be verified, and instrumentation stays in test-only builds. Browser mocks cannot prove real IPC ACLs, OS permissions or native lifecycle behavior.

Signing, notarization, store submission, release publication, deployment and device/data reset need exact authority. Build/test requests do not imply them. See [security policy](SECURITY.md) and [operating contract](skills/.shared/operating-model.md).

## Validation and contribution

From marketplace repository root, using its selected Python environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python scripts/check_plugin.py plugins/build-multi-target-tauri-apps --layout source
PYTHONDONTWRITEBYTECODE=1 python scripts/check_distribution_bundle.py plugins/build-multi-target-tauri-apps
PYTHONDONTWRITEBYTECODE=1 python scripts/check_marketplace.py .
PYTHONDONTWRITEBYTECODE=1 python scripts/check_copilot_marketplace.py .
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_*.py' -v
```

These check package structure, local links, exact distribution closure and both Codex/Copilot marketplace formats. Regenerate the Copilot catalog with `scripts/check_copilot_marketplace.py --write` after version or description changes. Verify discovery and installation in both clients with isolated settings when changing metadata or package layout. They do not prove native app behavior, fresh Codex routing, visual plugin-card rendering or storefront compliance. Validate consumer changes using the target evidence matrix in [testing reference](skills/.shared/validation.md). Keep original prose/artwork, refresh affected sources, preserve unrelated changes and commit only coherent scope. No credentials or captures belong in the distribution.
