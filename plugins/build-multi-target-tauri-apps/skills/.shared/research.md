# Research and adaptation ledger

Reviewed 2026-10-04. Scope: Tauri 2, not v1 allowlists. This is an original capability-level synthesis. Source plugins were inspected locally at Build iOS Apps 0.1.2, Build Web Apps 0.1.2, Build macOS Apps 0.1.4 and Test Android Apps 0.1.2. No prompts, code, assets or proprietary schemas were copied. No companion plugin is a runtime requirement.

## Source capability adaptation

| Source | Inspected capabilities | Tauri adaptation | Boundary |
| --- | --- | --- | --- |
| Build iOS Apps | ios-debugger-agent, ios-simulator-browser | Exact Xcode project, simulator identity, native launch/log/UI evidence | Tauri CLI owns Rust/frontend integration; tool APIs discovered rather than assumed |
| Build iOS Apps | swiftui-ui-patterns, swiftui-view-refactor, swiftui-liquid-glass | Stable component ownership, navigation, native conventions and accessible responsive frontend | SwiftUI view recipes and SwiftUI preview hosts do not implement a Tauri WebView |
| Build iOS Apps | ios-app-intents | Small system-facing actions and one domain routing path | App Intents need a deliberate native extension, not a JavaScript-only promise |
| Build iOS Apps | swiftui-performance-audit, ios-ettrace-performance, ios-memgraph-leaks | Focused scenario, matching symbols, ownership proof and comparable captures | Separate WebView JS, Rust and native allocations; optional instrumentation stays out of production |
| Build Web Apps | frontend-app-builder, frontend-testing-debugging | Design intent, rendered iteration, interaction/console/screenshot evidence | Browser testing alone cannot prove native IPC, ACLs or OS integrations |
| Build Web Apps | react-best-practices, shadcn-best-practices | Existing framework conventions, component reuse and measured rerender/loading work | React/shadcn conditional on actual project; do not mandate a framework |
| Build Web Apps | stripe-best-practices, supabase-postgres-best-practices | Explicit remote-service boundary and server-owned secrets | Service-specific work only when requested; no payment or database integration by default |
| Build macOS Apps | build-run-debug, swiftpm-macos, test-triage | Canonical build commands, causal failure triage and artifact identity | Cargo/Tauri are app owners; SwiftPM used only for an actual native dependency |
| Build macOS Apps | swiftui-patterns, view-refactor, window-management, liquid-glass, appkit-interop | Desktop keyboard/menu/window behavior and narrow native bridges | Avoid replacing Tauri with a second SwiftUI shell; no simulated CSS glass claim |
| Build macOS Apps | telemetry | Structured, redacted, bounded logs correlated across frontend/Rust/native | No sensitive payload logging or always-on instrumentation |
| Build macOS Apps | signing-entitlements, packaging-notarization | Inspect exact signature, entitlements, channel and notarization independently | Preparation does not authorize credential use, submission or publishing |
| Test Android Apps | android-emulator-qa | Serial-scoped adb, activity resolution, UI inspection, screenshots and logcat | WebView descendants can be absent from native tree; use supported WebView automation or recorded manual evidence |
| Test Android Apps | android-performance | Simpleperf/Perfetto/frame/memory tool selection and symbol-aware capture | Emulator timings do not establish physical-device performance |

## Primary source registry

Each row identifies a decision used in a shipped workflow. Recheck relevant sources against the consumer's installed CLI, Cargo.lock, frontend lockfile and native toolchain before implementing version-sensitive behavior. Exact patch versions are consumer evidence, not universal defaults.

| ID | Primary source | Decision / owning reference |
| --- | --- | --- |
| R01 | [Architecture](https://v2.tauri.app/concept/architecture/) | Separate WebView presentation, Rust core and native integration; architecture |
| R02 | [Process model](https://v2.tauri.app/concept/process-model/) | Attribute renderer/core work and lifetime separately; performance |
| R03 | [Prerequisites](https://v2.tauri.app/start/prerequisites/) | Host SDKs, Rust targets, Xcode and Android toolchain; platforms |
| R04 | [Create project](https://v2.tauri.app/start/create-project/) | Use canonical scaffold/init only in safe requested directory; build |
| R05 | [Project structure](https://v2.tauri.app/start/project-structure/) | Shared lib.rs mobile entry and generated native projects; architecture |
| R06 | [Frontend configuration](https://v2.tauri.app/start/frontend/) | Static SPA/SSG/MPA output; SSR is not embedded runtime; frontend |
| R07 | [Vite configuration](https://v2.tauri.app/start/frontend/vite/) | Fixed port and device-reachable dev host; frontend |
| R08 | [Configuration files](https://v2.tauri.app/develop/configuration-files/) | Target overrides use JSON Merge Patch; arrays replace; build |
| R09 | [CLI](https://v2.tauri.app/reference/cli/) | Resolve local CLI help and target-specific commands; build |
| R10 | [Development](https://v2.tauri.app/develop/) | Mobile init/dev and TAURI_DEV_HOST network setup; platforms |
| R11 | [Rust commands](https://v2.tauri.app/develop/calling-rust/) | Typed request/response/error contracts and async work; architecture |
| R12 | [Frontend messaging](https://v2.tauri.app/develop/calling-frontend/) | Events versus channels and listener lifetime; architecture |
| R13 | [State](https://v2.tauri.app/develop/state-management/) | Owned shared state and lock choice; architecture |
| R14 | [Capabilities](https://v2.tauri.app/security/capabilities/) | Default-enabled capability files, union of grants, custom commands unrestricted unless opted into ACL; security |
| R15 | [Permissions](https://v2.tauri.app/security/permissions/) | Explicit command grants; security |
| R16 | [Command scopes](https://v2.tauri.app/security/scope/) | Custom scope data needs enforcement in command logic; security |
| R17 | [CSP](https://v2.tauri.app/security/csp/) | Set explicit production CSP and allow only required sources; security |
| R18 | [Lifecycle threats](https://v2.tauri.app/security/lifecycle/) | Treat build, distribution and runtime as different trust boundaries; security |
| R19 | [Plugin catalog](https://v2.tauri.app/plugin/) | Check plugin support by target and pinned version; native |
| R20 | [Mobile plugins](https://v2.tauri.app/develop/plugins/develop-mobile/) | Swift/Kotlin bridge only for demonstrated missing native feature; native |
| R21 | [Sidecars](https://v2.tauri.app/develop/sidecar/) | Target-specific binaries, explicit shell scope, process lifecycle; native |
| R22 | [File system](https://v2.tauri.app/plugin/file-system/) | App directories, scoped access and platform storage constraints; security |
| R23 | [HTTP client](https://v2.tauri.app/plugin/http-client/) | Rust HTTP access needs scoped destinations; frontend CORS is different; security |
| R24 | [Store](https://v2.tauri.app/plugin/store/) | Persistent settings have explicit save behavior; architecture |
| R25 | [SQL](https://v2.tauri.app/plugin/sql/) | Schema migrations, driver features and transactions; architecture |
| R26 | [Stronghold](https://v2.tauri.app/plugin/stronghold/) | Vault choice needs key lifecycle; plain settings are not secret storage; security |
| R27 | [Deep links](https://v2.tauri.app/plugin/deep-linking/) | Platform registration and initial/running-app delivery; native |
| R28 | [Windows](https://v2.tauri.app/learn/window-customization/) | Decoration, drag regions and native interaction; frontend |
| R29 | [Tray](https://v2.tauri.app/learn/system-tray/) | Desktop integration is target-specific; native |
| R30 | [Debugging](https://v2.tauri.app/develop/debug/) | Frontend WebView inspector and Rust debugger are distinct; testing |
| R31 | [Mock APIs](https://v2.tauri.app/develop/tests/mocking/) | Mocks isolate frontend behavior and require cleanup; testing |
| R32 | [WebDriver](https://v2.tauri.app/develop/tests/webdriver/) | Embedded WDIO supports macOS; direct tauri-driver remains Windows/Linux; testing |
| R33 | [WebdriverIO Tauri](https://webdriver.io/docs/desktop-testing/tauri/) | Provider/dependency selection and test instrumentation; testing |
| R34 | [Distribution](https://v2.tauri.app/distribute/) | Native artifact and channel matrix; distribution |
| R35 | [macOS signing](https://v2.tauri.app/distribute/sign/macos/) | Signing and notarization are separate evidence; distribution |
| R36 | [iOS signing](https://v2.tauri.app/distribute/sign/ios/) | Team/profile/entitlement and device identity; distribution |
| R37 | [Android signing](https://v2.tauri.app/distribute/sign/android/) | Keystore and upload/signing identities; distribution |
| R38 | [Windows installer](https://v2.tauri.app/distribute/windows-installer/) | Installer format, architecture and WebView2 provision; distribution |
| R39 | [App Store](https://v2.tauri.app/distribute/app-store/) | Native channel metadata and submission constraints; distribution |
| R40 | [Google Play](https://v2.tauri.app/distribute/google-play/) | AAB, versionCode and channel requirements; distribution |
| R41 | [Updater](https://v2.tauri.app/plugin/updater/) | Desktop-only registration, required signatures and key custody; distribution |
| R42 | [GitHub pipeline](https://v2.tauri.app/distribute/pipelines/github/) | Host-specific build jobs and explicit release effects; distribution |
| R43 | [adb](https://developer.android.com/tools/adb) | Device serial, package/activity and scoped capture; testing |

## Freshness and contradictions

Context7 `/websites/v2_tauri_app` was unavailable (`library_not_finalized`). `/tauri-apps/tauri-docs` succeeded. Current official WebDriver and WebdriverIO pages supersede the older blanket statement that Tauri cannot automate macOS: embedded instrumentation provides a separate route. Do not conflate that with direct official tauri-driver support or infer mobile support from a desktop table. No native test run or platform installation was performed during research.

## Maintenance

Refresh affected rows when Tauri/CLI/plugin major or minor versions, native SDK requirements, automation providers or release-channel requirements change. Record installed versions and retrieval date in consumer evidence. Prefer primary docs and upstream source when examples disagree; do not silently upgrade dependencies to match an online snippet.
