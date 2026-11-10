---
name: worktree-activity
description: Register and reconcile unfinished development owned by a user-facing Codex coordinator in existing authorized Git worktrees. Use before development or delegation into a worktree, after meaningful progress, when resuming interrupted work, and before finalizing its ownership record. Also use for read-only ownership inspection and recovery planning.
---

# Worktree Activity

Keep unfinished development attributable to its responsible user-facing conversation until that conversation verifies completion or reconciles user-authorized cancellation.

Read [runtime identity](references/runtime-identity.md) before relying on native identity. Read the [lifecycle and CLI contract](references/lifecycle.md) for mutations and failure handling. The packaged executable is [scripts/worktree_activity.py](scripts/worktree_activity.py); resolve it relative to this skill's installed directory, never the target checkout or an assumed cache path. Follow the [package setup](../../README.md) before running it.

## When to invoke

Invoke for an actual development assignment in existing authorized worktrees, before delegation into those worktrees, when reconciling progress or resuming unfinished work, and for requested read-only recovery inspection. Do not register merely because a chat opened or a directory was read.

## Inputs and evidence

- A root is the user-facing coordinator responsible for this assignment. An independently assigned user-facing fork can be a root. A delegated agent cannot.
- Only that root may register, update, reconcile, or finalize its record. Delegated agents report results to their coordinator; they never run registry mutations, including with their coordinator's environment or ID.
- Use the native `CODEX_THREAD_ID` of the executing coordinator. Keep optional `CODEX_SESSION_ID` separate; equality does not establish role. Missing identity must fail visibly. Never infer identity from filenames, transcripts, newest sessions, titles, timestamps, or PIDs.
- `--coordinator` is an explicit role assertion, not authentication or a native role detector. Do not make it on behalf of a delegated agent. Consult the runtime findings for any additional detected restriction.
- Use an explicit existing, authorized, Git-registered linked worktree. Report unexpected placement outside the primary workspace's preferred `.worktrees/` directory, but do not hide or abandon its unfinished work. The primary checkout is not a mutation target. Do not create a worktree, move a checkout, alter a branch, or modify a global file as a side effect; new-worktree approval and placement rules still apply independently.
- Preserve unrelated edits and coordinate overlapping file changes. Multiple roots can own unfinished work in the same checkout.

## Workflow

### Begin or resume

1. Identify the actual development assignment and all target worktrees, including worktrees used only by delegated workers. A read, opened chat, or scan alone does not justify registration.
2. Run read-only diagnostics for each target. Verify native thread identity and explicitly select the real execution surface; do not label CLI execution as Desktop.
3. Register a stable task ID and clear description before development or delegation. Existing records must validate and reconcile first. Preserve every existing task, registration timestamp, and previous result. Repeated registration must not reset progress or reopen terminal tasks.
4. Surface branch or path discrepancies. Use the explicit owner reconciliation operation only after checking that the change is legitimate; never silently replace last-reconciled metadata.

### Progress and delegation

Record meaningful progress, new blockers, changed scope, and delegated results. `last_activity` records progress, not liveness. Reads must not refresh timestamps; do not run timers or heartbeats.

Record delegated work before dispatch. Once its native ID is available, the root may add `assignee_thread_id` as diagnostic metadata. It is never a recovery destination. A worker returning, exiting, or completing its turn does not prove its assignment complete. The root reconciles the result and records a concrete verification summary before marking work completed.

### Finish or retain

Use task updates to record outcomes, then run explicit finalization separately. Finalization reads the latest record under the same synchronization as updates and removes only this owner's exact record when every task is terminal and its required evidence is present.

Retain records through interruption, pause, blocked work, pending approval, shutdown, compaction, ended turns, and failed agents. Records never expire. Cancel only after explicit user authorization; record both the reason and authorization reference. Do not invent permission from elapsed time or inactivity.

Never delete another root's record, sweep old records, recursively remove `.agent-activity/`, unlink mutex files, or implement a force-delete escape hatch. No records does not mean a checkout is safe to delete; Git-state, ownership, and approval checks remain independent.

### Read-only recovery

Scan only Git-registered linked worktrees of explicitly supplied primary project roots, with bounded traversal. Include existing worktrees outside preferred placement and report their warnings. Report partial errors alongside valid findings; do not describe errors as an empty registry. Build recovery plans grouped by `root_thread_id` across projects and worktrees. Direct any proposed recovery to that root alone, using its native Desktop link when verified. Do not message, resume, or mutate another conversation in this workflow.

## Outputs and handoff

Report target worktrees, root ownership, unfinished tasks/blockers, verification evidence, discrepancies, and whether each record remains or was explicitly finalized. Distinguish fixture coverage from live Desktop evidence. Installation permits implicit selection but does not guarantee every assignment loads this skill; offer the [global integration block](references/global-agents-integration.md) for deliberate default adoption without editing global instructions automatically.

## Completion evidence

Every registered task has a root-reconciled result: `completed` with concrete verification or `canceled` with explicit user authorization and reason. Explicit finalization must confirm removal of only the current owner's record under synchronization. Otherwise retain the record and identify outstanding work.

## Must not

Do not impersonate another owner, mutate records as a delegated agent, invent native identity, infer role from thread/session equality, expire records, delete mutex files, override corrupt or unsupported records, or bypass metadata discrepancies. Do not create worktrees, switch branches, modify global configuration, or message/resume recovery targets as part of registry operations. Never treat this advisory registry as an exclusive checkout lock or deletion approval.
