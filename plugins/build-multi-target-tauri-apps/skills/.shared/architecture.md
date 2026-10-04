# Architecture, IPC and persistence

Grounding: [R01–R02, R05, R11–R13, R24–R26](research.md). Use frontend presentation and Rust domain services with small command handlers. Tauri's shared library entry supports desktop and mobile; retain the scaffold's mobile entry attribute and crate types. Keep generated Xcode/Gradle integration in the canonical project workflow; do not regenerate over native customization.

## Command contracts

Define request and result shapes, field naming, serialized error codes and size limits before wiring invoke. Bind UI loading/error/cancellation state to operation identity. Validate untrusted strings, paths, URLs, ranges and user authority in Rust; TypeScript types are not runtime validation. Keep handlers thin and domain logic independently testable. Do not expose a generic execute-shell, arbitrary SQL or unrestricted filesystem command merely for convenience.

Use asynchronous handlers for asynchronous I/O. Move CPU-heavy or blocking work to an appropriate bounded worker/spawn_blocking path; an async function alone does not move blocking computation off an executor. Do not hold synchronous locks across await. Define task cancellation explicitly: dropping a frontend promise is not evidence that backend work stopped. Return actionable errors without private paths or secrets.

## Messages and lifetime

Use request/response commands for finite operations, events for small notifications and channels for ordered streaming/progress. Avoid bulk/base64 payloads or high-frequency global events when a bounded stream/resource path fits. Correlate messages with operation/session identity, reject stale updates and bound producer buffers. Remove listeners on view/session disposal, including listeners whose async registration resolves after disposal. Events are not a privileged command authorization mechanism; never put secrets in broadly observable notifications.

Use managed Rust state for process-owned resources. Define ownership for window, session, account and operation resources; use locks only for the shared portion, not across network/disk work. Persist authoritative data before claiming a transaction completed. Crash/restart and mobile suspension can interrupt work independently of UI lifetime.

## Storage

Use platform app-data/config/cache paths, not cwd or hard-coded home paths. Store plugin suits small preferences; inspect autosave/save semantics for the pinned version and test restart persistence. SQL suits relational state; choose driver features deliberately, parameterize queries, run ordered migrations and use transactions for multi-step invariants. Avoid exposing unrestricted SQL directly to every renderer.

Secrets need a deliberately selected OS credential mechanism or vault with an understood key/unlock/recovery lifecycle. Store/localStorage/ordinary JSON are not encrypted credential storage. Stronghold is an option, not automatic OS Keychain parity. For a schema change, inspect existing data, make a local backup and design a one-off conversion with dry-run/verification before authorized overwrite; do not add indefinite legacy adapters. Test interruption and restore where data integrity matters.

## Browser deployment

Static hosting can render shared UI but cannot execute Tauri invoke. Keep native imports/calls behind an actual environment boundary; do not fake successful native operations in production web builds. Where browser support is requested, implement server/browser storage and permissions intentionally, reconcile authentication and offline state, and test both implementations. Server secrets never enter bundled frontend assets.
