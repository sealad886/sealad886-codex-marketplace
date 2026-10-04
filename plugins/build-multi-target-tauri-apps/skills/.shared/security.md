# IPC and platform security review

Grounding: [R14–R18, R22–R23, R26, R41](research.md). Assume renderer inputs can be hostile. Trace entry → validation/authorization → privileged operation and prove both allowed and denied cases.

## Authority calculation

Capability files in src-tauri/capabilities are enabled by default unless configuration explicitly selects them. Compute grants across all matching windows/webviews: multiple capabilities union their privileges. Target-filter capabilities and constrain labels/origins. Inspect effective merged config and generated permission schema for the installed version. Core/plugin default grants are not a reason to grant every command.

Important: app commands registered via invoke_handler are accessible by default unless restricted through the application command manifest/ACL mechanism. Enumerate sensitive commands with tauri_build AppManifest::commands using current docs, define permissions and grant only intended callers. A capability cannot replace Rust-side object/user authorization. Custom scope values need enforcement by command logic; declaring JSON scope does not automatically validate arbitrary custom paths or URLs.

Do not allow remote pages access to native APIs without a concrete reviewed requirement and narrow origin/command scope. Keep external content in an unprivileged context or external browser, validate navigation and opened URL schemes and treat links as untrusted. Do not expose a broad shell/file/HTTP/SQL bridge to work around a denied operation.

## Resource and content policy

Set explicit production CSP for actual scripts/styles/images/connect endpoints and required IPC transport. Derive CSP sources from installed docs and runtime; do not copy a permissive example or switch CSP off to fix development. Dev/HMR needs belong in development configuration. Do not expose secrets through frontend environment prefixes, source maps, logs or bundled config.

Restrict filesystem access to purpose-specific app directories/user-selected resources. Validate custom-command paths and traversal/symlink behavior where relevant. Rust HTTP client is not constrained by browser CORS: allowlist destinations and validate redirects/credentials; browser fetch has its own CORS/CSP requirements. Sidecars need fixed executable identity and constrained arguments, no interpolated shell strings. Bound payload sizes, concurrent tasks, capture retention and log rotation where resources matter.

Persist credentials only through chosen secret storage with reviewed access, recovery and platform support. Redact auth data, private paths, document bodies and device identifiers from reports. Native usage descriptions/Android permissions must match feature need; denied/revoked OS permission should produce a recoverable UI state.

## Verification scenarios

Use a real native IPC boundary for sensitive-command denial, wrong window/origin, unavailable target, malformed input and out-of-scope resources. Unit tests establish domain validation; mocks cannot establish ACL enforcement. Inspect release dependency/features and binary/config to prove debug tooling, embedded WebDriver endpoints and test command mocking are absent. Use a dedicated explicit test feature/build variant, not a production-enabled dependency by accident. Updater signature and OS signing are separate controls; both need exact artifact evidence when applicable.
