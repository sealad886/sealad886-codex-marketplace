# Rust implementation and concurrency: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Both module.rs and module/mod.rs layouts are supported; preserve repository layout rather than requiring mod.rs.

- Use Result for recoverable failure and Option for legitimate absence; reserve unwrap/expect for justified invariants and test code.

- Prefer borrowing where it simplifies lifetime/ownership; a clone can be correct and cheap, while forcing references can complicate APIs.

- Tokio is one async runtime; retain the chosen runtime or synchronous design. Do not add Tokio solely for ordinary Rust work.

- Select Mutex, RwLock, atomics, or channels from access patterns and contention; RwLock is not a universal shared-state default.

- Bound channels and spawned work; define cancellation, shutdown, and task-error handling. Dropping a handle is not always cancellation.

- Avoid holding synchronous locks across await and use blocking-task facilities for blocking work where supported.

- Use cargo fmt/check/clippy/test with relevant features/targets; property testing is optional when it proves a useful invariant.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Rust permits modern module.rs and directory mod.rs layouts.](https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
