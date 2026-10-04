# Packaging, signing and distribution

Grounding: [R34–R42](research.md). Preparation is distinct from execution: inspect wrappers and grant no implicit signing, credential use, notarization, store upload, release creation or deployment authority. Report exact actions still requiring authorization.

## Release identity

Resolve owning version source and align native metadata: product identifier, semantic app version, Apple bundle/build versions, Android versionName/versionCode and platform/package architecture. Retain stable identifier/channel unless change is explicitly requested. Capture revision, lockfiles, toolchain, config overlays, artifact digest, build profile and supported feature matrix. Avoid stale artifact glob matches; inspect the actual produced file.

Use CI jobs on supported native hosts. Reuse declared dependency locks and pin build actions/tools according to repository policy. Cache keys include target/toolchain/lock inputs; never put secrets into caches. Untrusted pull requests must not receive signing keys, privileged release tokens or writable release jobs. tauri-action can create/upload releases: inspect inputs and permissions before running. Separate ordinary build artifacts from authorized release publication. Do not invent a passing hosted CI result from local checks.

| Target/channel | Inspect prepared artifact | Distinct release gates |
| --- | --- | --- |
| macOS direct | .app/DMG, architectures, resources, entitlements | Code signature, notarization receipt/stapling, Gatekeeper and install launch |
| macOS App Store | App bundle and sandbox/channel config | Store signing/profile, required entitlements/privacy and submission |
| Windows | MSI/NSIS, target architecture and WebView2 policy | Signing/trust, clean install/uninstall/update and channel rules |
| Linux | Chosen AppImage/deb/rpm/etc., dependencies and supported distro baseline | Package integration/launch and channel-specific signing |
| iOS | Archive/IPA, identifier/build, architectures, profile/entitlements | Authorized device/TestFlight/store signing and actual install/run |
| Android | APK for device tests; AAB for Play, ABIs, applicationId/versionCode | Keystore/upload key/app-signing identity and track-specific delivery |
| Browser | Static assets and environment config | Independent hosting/deployment, service auth/CORS and native-feature behavior |

## Updates and recovery

Official updater is a desktop feature; guard Rust dependency/registration and frontend UI on desktop and use mobile store distribution for mobile. Updater signatures are mandatory and separate from OS code signing. Keep private update/signing keys out of repository, chat, logs and command arguments; use approved secret input. Verify endpoint, public key, matching artifact/architecture/version and signature on exact update metadata. Test failure/offline/restart and interruption paths plus data/schema changes before claiming recovery. A lost updater key affects existing client continuity; key recovery/rotation requires explicit design.

A binary rollback cannot undo a one-way data migration. Back up data locally, verify conversion and restore path before authorized overwrite, and state any downgrade limit. Do not maintain speculative compatibility layers when a one-off migration satisfies the future-state requirement.

## Final gate

For each target record built, inspected, signed, submitted, installed and published separately with command/receipt or reason not run. Inspect release dependencies/features for dev server URLs, debug APIs, embedded automation, mock commands and credentials. Verify fresh packaged launch and critical interaction on intended channel. Online platform policy can change: recheck current Apple/Google/Microsoft documentation before submission; this reference does not certify storefront compliance.
