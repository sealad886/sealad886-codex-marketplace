# Version 1 lifecycle and CLI contract

The [Draft 2020-12 schema](worktree-activity-v1.schema.json) defines JSON shape and formats. The helper additionally validates filenames, native identity, task uniqueness, Git metadata, intended checkout location, transitions, and finalization. It uses the published schema through the pinned `jsonschema` validator; it does not implement a schema engine.

## Record and task fields

All root fields are required. Unknown root and task fields are rejected. Optional fields are omitted when unavailable unless the field explicitly permits `null`.

| Field | Contract |
| --- | --- |
| `schema_version` | Integer exactly `1`; unknown versions are rejected without overwrite. |
| `session_type` | `codex-desktop` or `codex-cli`, explicitly selected for the actual execution surface. |
| `root_thread_id` | Native lowercase UUID-shaped thread ID; no UUID version restriction. Must match `<root_thread_id>.activity.json` exactly. |
| `session_id` | Separate native UUID-shaped session value or `null`; never inferred from the thread ID. |
| `worktree_path` | Absolute checkout root resolved through Git, stored as last reconciled. |
| `branch` | Actual branch name as last reconciled, or `null` for detached HEAD. |
| `tasks` | Nonempty array with stable, unique IDs within this record. |

Every task requires `id`, `description`, `registered_at`, `last_activity`, and `status`. IDs contain 1–80 characters matching `[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}`. Descriptions are nonblank. Both timestamps use UTC RFC 3339 with a terminal `Z`; registration time is retained across updates and resumption. `last_activity` describes meaningful progress, never a heartbeat.

Optional task fields are `assignee_thread_id` (native diagnostic ID only), `note` (blocker/recovery note), `verification` (concrete completion evidence), `cancellation_reason`, and `authorization_ref`. Text fields must be nonblank when supplied. `verification` is allowed only for `completed`; cancellation fields are allowed only for `canceled`. Do not add arbitrary metadata, transcripts, credentials, or broad project-management data.

The array contains at most 1,000 tasks. Descriptions, branch names, and optional text fields are limited to 8,192 characters. Optional task fields do not accept `null`; only `session_id` and `branch` explicitly do. The schema accepts fractional UTC seconds and requires date-time format checking as well as its terminal-`Z` pattern.

JSON Schema validation does not establish a caller's role, actual Git state, ownership, or lifecycle history. Validation and inspection report those semantic limits instead of silently repairing them.

The [active example](../examples/valid-active.json) includes a delegated diagnostic assignee and blocker. The [terminal example](../examples/valid-terminal.json) includes verified completion, authorized cancellation, and detached HEAD. The [unsupported-version example](../examples/invalid-unknown-version.json) must fail schema validation. The [duplicate-task example](../examples/invalid-duplicate-task-ids.json) has a valid JSON shape but must fail semantic uniqueness validation. These files use synthetic IDs and illustrative paths; a live record must use its actual native owner filename and Git-resolved checkout path.

## Status transitions and idempotence

New tasks start `pending`. Nonterminal statuses are `pending`, `in_progress`, `blocked`, and `paused`; they may transition to one another. Mark `blocked` with a useful note explaining the obstacle and next recovery step. Mark `paused` when work has intentionally paused; neither state permits removal.

`completed` requires nonblank `verification` describing the root's reconciliation and checks. `canceled` requires both a nonblank `cancellation_reason` and `authorization_ref` identifying explicit user approval. The helper checks the required evidence fields; the coordinator remains responsible for their truth. Elapsed time, a worker exit, or ending a turn is not cancellation authorization.

Completed and canceled tasks are terminal and cannot be reopened or silently reset. Repeating an identical terminal update is a no-op. Register new follow-up work with a new stable task ID rather than rewriting a terminal assignment.

Repeating `register` for the same task ID and description is idempotent: existing tasks, status, evidence, registration time, and activity time stay intact. A conflicting description produces an error; use an explicit task update when changing nonterminal work. Adding another task never replaces the prior list. Original session metadata remains intact on resumption. Reads and metadata-only reconciliation do not refresh task activity times.

## CLI

Invoke `scripts/worktree_activity.py` using the configured environment's Python, resolving the script from the installed skill directory. Paths can contain spaces or non-ASCII characters; quote them in your shell. The helper uses subprocess argument arrays and timeouts, not shell interpolation.

| Command | Purpose |
| --- | --- |
| `diagnostics [--worktree PATH]` | Read native identity diagnostics and, when provided, target Git state; no writes. |
| `register --worktree PATH --coordinator --surface SURFACE --task-id ID --description TEXT` | Create/resume this root's record and register a stable task before work. |
| `task --worktree PATH --coordinator --task-id ID [OPTIONS]` | Add a task with `--description`, or explicitly update existing nonterminal work. |
| `reconcile --worktree PATH --coordinator` | Explicitly accept legitimate branch/path metadata changes after owner review. |
| `finalize --worktree PATH --coordinator` | Remove only the current owner's record after rechecking every task's terminal evidence. |
| `inspect --worktree PATH` | Read records and report checkout discrepancies without refreshing timestamps. |
| `validate FILE` | Validate a record's schema and semantic filename/path contract without requiring current Codex identity. |
| `scan PROJECT... [--json] [--max-worktrees N] [--max-records N]` | Bounded read-only scan of Git-registered linked worktrees belonging to explicit primary projects, including existing external locations. |
| `recovery PROJECT... [--json] [--max-worktrees N] [--max-records N]` | Group read-only recovery findings by responsible root across projects. |

Task options are `--description`, `--status`, `--assignee-thread-id`, `--note`, `--verification`, `--cancellation-reason`, and `--authorization-ref`. Every mutation requires `--coordinator` plus the executing native `CODEX_THREAD_ID`. There is no owner-ID override. Missing or conflicting identity fails. See [runtime identity](runtime-identity.md) for the observed role metadata and limitations; an assertion does not prove a native role check.

Target paths must resolve to existing Git-registered linked worktrees. The primary workspace is determined from Git, not the current shell directory or plugin location. Scans recheck that each selected path still belongs to the supplied primary before reading its registry; stale paths reused by another project produce partial-scan errors. The primary checkout is rejected as a mutation target. Existing linked worktrees outside the preferred primary workspace `.worktrees/` directory produce placement warnings and remain available for explicitly assigned mutations, inspection, and recovery. This does not authorize creating worktrees or change new-worktree approval/placement rules. Detached HEAD stores `branch: null`. Branch/path mismatches are visible discrepancies; ordinary mutations refuse them until the owner explicitly reconciles. Reconciliation does not switch branches or move files. It preserves tasks and registration timestamps.

Inspection, validation, mutation, scan, and recovery results include a `warnings` array of `{ "path": WORKTREE_ROOT, "warning": TEXT }` objects; diagnostics reports it under `checkout.warnings`. These placement warnings remain visible even when a worktree has no records. They are advisory, are never stored in ownership records, and do not cause a nonzero exit status by themselves. They differ from record/Git metadata discrepancies, which require owner reconciliation.

Exit statuses are `0` for success, `1` for operational/identity/validation failure, `2` for command-line usage errors, and `3` for partial inspection/scan/recovery results with errors. Failures are visible on stderr; scans expose errors with partial findings and return nonzero. An empty result with errors is not proof that no records exist. Default scan limits are 1,000 worktrees and 10,000 records; each limit accepts 1–100,000. Mutation lock waits default to 10 seconds, configurable with `--lock-timeout` in the range greater than 0 through 300 seconds. Use `--help` for argument placement.

## Synchronization, failure, and durability

Each root uses a stable same-directory mutex separate from its replaceable JSON record. Mutations serialize the entire read/validate/modify/validate/write or finalization operation. Updates write a temporary file in the same directory, flush and synchronize it, then atomically replace the record and synchronize the directory. Readers see the previous or next complete JSON document. Finalization uses the same mutex; it cannot race a task addition into silently deleting unfinished work.

Do not unlink mutex files while processes may hold or await them. Temporary and mutex artifacts are distinguishable from `*.activity.json` and are excluded from ownership scan results. Finalization removes only the owner's exact JSON file; other records and synchronization files remain. An empty `.agent-activity/` directory may remain.

These guarantees assume a local POSIX filesystem with working advisory locks, atomic replacement, and file/directory synchronization. Network filesystems and host power-loss behavior are not qualified. Registry synchronization does not lock source files or authorize simultaneous conflicting edits.

Corrupt JSON, unsupported schema versions, unsafe filenames or symlinks, missing/conflicting identity, and metadata discrepancies fail visibly without destructive repair. Before atomic replacement, a failed mutation retains the last valid record. A failure after replacement can leave the newly committed valid record even when the command reports a durability error; inspect it before retrying. Never overwrite evidence merely to clear an error.

Records have no expiration. Keep them through crashes, inactivity, shutdown, ended turns, context compaction, completed subagents, and pending approval. Remove them only through explicit owner finalization after all registered work is reconciled. No exit trap, abandoned-session sweep, or background timer deletes records.
