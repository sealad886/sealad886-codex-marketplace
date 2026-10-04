# Build and target runbook

Grounding: [R03–R10, R19–R21, R27–R29](research.md). Commands below are illustrative for a project whose package.json has a `tauri` script and uses npm. Translate through the existing package manager; inspect scripts and installed `--help` before executing. No command below authorizes installation, credential use or provider writes.

## Canonical commands

```sh
npm run tauri -- --version
npm run tauri -- info
npm run tauri -- dev --help
npm run tauri -- build --help
npm run tauri -- android dev --help
npm run tauri -- ios dev --help
cargo test --manifest-path src-tauri/Cargo.toml --locked
cargo fmt --manifest-path src-tauri/Cargo.toml --check
```

For a new app use the current official scaffold in the user-selected empty directory, record selected framework/package manager and lock dependencies. For an existing frontend use local Tauri init only after inventorying existing src-tauri; never use force to overwrite user work. Do not execute @latest scaffolds as an uninspected upgrade.

Connect beforeDevCommand/devUrl and beforeBuildCommand/frontendDist to existing scripts. frontendDist resolves relative to configuration location; verify actual built index/assets. Platform files and --config overrides use JSON Merge Patch: arrays replace instead of append. Inspect the effective window, permission, bundle and identifier configuration for each target, not just the base JSON. Production must use intended packaged assets and exclude development hosts/debug features.

## Host and target matrix

| Target | Host/toolchain prerequisites | Native runtime | Evidence needed |
| --- | --- | --- | --- |
| Windows | Windows build runner, supported MSVC tools, Rust target, WebView2 | WebView2 | Native launch, installer/runtime provisioning, keyboard/DPI behavior |
| Linux | Distribution-specific compiler, WebKitGTK and packaging libraries | WebKitGTK | Launch on supported distro, package dependencies, display/graphics behavior |
| macOS | macOS runner, Apple tools, intended Rust architecture(s) | WKWebView | .app launch, window/menu behavior, architecture and channel checks |
| iOS | macOS, full Xcode, selected SDK, Rust device/simulator targets, required supporting tools | WKWebView | Exact simulator/device, bundle/profile identity when signed, lifecycle and input behavior |
| Android | SDK/platform-tools/build-tools, matching NDK, JDK/Gradle wrapper, Rust ABI targets | Android WebView | Exact serial/API/WebView version, APK ABI/package, lifecycle and permissions |
| Browser (optional) | Existing frontend build and hosting workflow | Browser engine | Static output, native-feature replacement/unavailability, routes and authentication |

Cross-compiling Rust is not equivalent to producing a usable native installer; default to a host build matrix and current target documentation. Select SDK/NDK versions from project requirements, not the last directory returned by ls. Confirm all requested ABIs/architectures without adding unrequested ones.

Initialize android/ios only when target project is absent and requested. Use the local CLI's `android init`, `ios init`, `android dev` or `ios dev`; preserve generated project customizations. For target selection use actual CLI help, device list and artifact architecture, not guessed flags. Mobile development requires a reachable frontend host: use TAURI_DEV_HOST where supplied, fixed port/strictPort and correct HMR host. Check device network/firewall rather than disabling production CSP or opening unrestricted hosts. Never expose dev service beyond the required network.

## Native integration

Prefer an official supported plugin before a bespoke bridge. Verify the plugin's target table, JS/Rust bindings, registration, permissions and OS declarations together. Guard desktop-only dependencies/registration/UI by target; runtime checks alone cannot compile an unsupported crate. Native mobile bridges use documented Swift/Kotlin plugin interfaces for a concrete missing feature. Keep a small typed boundary, error/cancellation handling and one shared domain owner.

Deep links must handle initial launch and already-running app delivery, validate URL/action/state and deduplicate callbacks. Authentication flows require state/PKCE and a server-owned secret where applicable. iOS associated domains and Android intent filters/app links are native configuration, not just frontend routes. Menus/tray/global shortcuts are desktop-specific. App Intents/widgets require explicit native extension work and identity/signing design. Desktop sidecars need per-target binaries, narrow shell arguments and owned process cleanup; do not promise Node/desktop sidecars on mobile.

For every failure identify first causal layer: frontend output/dev network, Rust compile, plugin registration/ACL, native toolchain/ABI, install/signing, launch or runtime. Inspect relevant logs before retries. Missing SDK/device is an environment gap, not evidence of a product defect.
