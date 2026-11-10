# Optional default integration

Installation makes the skill available for implicit invocation; it does not guarantee that every development assignment activates it. Add the following block to your chosen global or project `AGENTS.md` only when you deliberately adopt this workflow. The plugin does not edit global instructions or user configuration.

```markdown
## Recoverable worktree ownership

For actual development assignments in existing authorized Git-registered linked
worktrees, load the installed
`worktree-activity:worktree-activity` skill before development or delegation.
Resolve its helper/resources from the installed skill directory. If unavailable,
report that ownership registration could not run; never fabricate an owner ID.

The responsible user-facing coordinator owns one record per target worktree.
An independently assigned user-facing fork can own its own record. Delegated
agents never create or mutate records; they report to their coordinator.
Capture native CODEX_THREAD_ID as owner identity and keep optional
CODEX_SESSION_ID separate. Assert coordinator role only when actually serving
that role; thread/session equality does not establish it.

Register each assignment before work starts, including targets used only by
workers. Reconcile existing records, preserve tasks and timestamps, and update
after meaningful progress or delegated results. Record blockers and concrete
verification. Keep records through interruption, pause, compaction, ended turns,
pending approvals, and crashes. They never expire.

Include existing linked worktrees outside the primary workspace's preferred
`.worktrees/` directory and report their placement warnings. Do not mutate the
primary checkout. New-worktree approval and placement rules remain independent.

Finalize only after every registered task is verified complete or explicitly
user-authorized cancellation is recorded with its reason and authorization
reference. Remove only the current root's exact record through the helper.
Recovery plans target responsible roots, never diagnostic assignee IDs.

Records are advisory and allow multiple owners; coordinate overlapping edits.
Absence of records never authorizes checkout deletion. Do not create worktrees,
message/resume conversations, change global configuration, sweep old records,
or remove synchronization files as a side effect of this workflow.
```

This is an instruction-level default. It is not a host enforcement hook, process lock, liveness signal, or authentication boundary. A helper failure must stay visible while unrelated safe work can continue; do not claim registration succeeded until the helper confirms it.
