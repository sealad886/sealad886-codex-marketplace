# Validation and debugging evidence

Grounding: [R30–R33, R43](research.md). Choose tests from changed contracts and target risks. Do not add snapshots of incidental prose, coordinates or private call sequences. Use existing project test/lint/build commands after inspecting effects.

| Level | Proves | Does not prove |
| --- | --- | --- |
| Rust domain/unit + mock runtime | Business rules, serialization, cancellation/storage invariants | Native WebView, IPC ACL, signing or OS permission behavior |
| Frontend/component with Tauri mocks | Rendering and invocation contract | Real Rust execution or capability enforcement |
| Browser rendered | Layout, focus, routing and browser interactions | Packaged native transport or OS integration |
| Native desktop E2E | Packaged app interaction under selected provider | Other OS engines/architectures or mobile |
| Simulator/emulator | Selected mobile artifact and lifecycle/interaction | Physical sensors, realistic performance or store signing |
| Physical/device/channel | Specific tested artifact/device/channel behavior | Untested devices or release variants |

## Automation selection

Current official Tauri guidance recommends WebdriverIO Tauri service with an embedded provider on Windows, Linux and macOS. Direct official tauri-driver works on Windows/Linux; it is not a macOS WKWebView driver. Confirm installed WDIO/service/Rust plugin versions and provider setup from primary docs before adding dependencies. Embedded testing requires test-only app instrumentation; keep it excluded from production. Do not silently adopt a paid provider. This desktop support table does not establish Android/iOS automation support.

If no supported native automation is configured, use an available platform UI tool or record a bounded manual run with exact artifact, steps, logs and screenshots. Do not replace missing native evidence with passing browser mocks. Test critical paths with real invoke and denied capabilities; IPC mocking only proves the mocked path. Reset mocks/listeners between frontend tests.

## Android run

Select an authorized target from `adb devices -l` and record its serial/API/ABI/WebView version. Scope every device command with `adb -s "$TAURI_SERIAL"`. Resolve package and launch activity from built APK/native metadata and device package manager; verify installation identity. Do not run unscoped install tasks that can target several devices.

Illustrative capture after selecting serial/package and a unique artifact directory:

```sh
adb -s "$TAURI_SERIAL" shell cmd package resolve-activity --brief "$TAURI_PACKAGE"
adb -s "$TAURI_SERIAL" shell pidof "$TAURI_PACKAGE"
adb -s "$TAURI_SERIAL" exec-out screencap -p > "$TAURI_ARTIFACT_DIR/android.png"
adb -s "$TAURI_SERIAL" shell uiautomator dump "$TAURI_REMOTE_UI_PATH"
adb -s "$TAURI_SERIAL" pull "$TAURI_REMOTE_UI_PATH" "$TAURI_ARTIFACT_DIR/android-ui.xml"
```

Set TAURI_REMOTE_UI_PATH to a unique task-owned device path before capture; confirm ownership before removal. Capture timestamp/PID-scoped logcat without clearing the user's existing logs. Native UI trees may expose only a WebView container: do not infer absent content or tap guessed coordinates. Use supported WebView automation/accessibility or recorded manual interaction. Reinspect after navigation. Verify back, keyboard, rotate, deny/revoke permissions and background/resume for changed flows. Do not reset device or app data without exact authority.

## iOS and desktop run

On macOS inspect `xcrun simctl list devices available`, select exact UDID, SDK/architecture and generated project/scheme. Use local Tauri CLI first for Rust/frontend integration; use available Xcode tools for native launch/log/UI work with documented APIs. Verify bundle identifier and live screen before interacting. Simulator streaming is optional and scoped to the selected UDID; a loaded viewer page is not proof of healthy frames. Never fabricate a SwiftUI preview host for the Tauri UI.

For desktop record executable path, build profile, WebView engine/version, OS/architecture and package digest. Reproduce flow, capture frontend console and Rust/native logs, identify first causal error, apply one fix and repeat same scenario. Cover fresh start, persistence restart and relevant multiple-window lifetime. Capture logs outside source and clean up only owned processes.

## Evidence record

Record requirement, scenario, method, command/exit status, revision/digest, target/device/runtime/build variant, observable result, capture location and limitation. Missing tools/SDK/profile/provider is a setup gap; runtime failure after valid setup is product evidence. Keep blocked/not-run targets visible. Static package validation proves instruction packaging, not autonomous agent behavior or native acceptance.
