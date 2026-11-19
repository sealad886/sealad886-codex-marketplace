---
name: event-driven-job-watcher
description: Wait for a long-running job's exit or terminal event without polling. Use when asked to attach a watcher, save completion evidence for a build, test, benchmark or batch job, or resume the current Codex chat when the job finishes.
---

# Event-Driven Job Watcher

## When to invoke

Use for authorized jobs when the user wants completion-only monitoring. When a
durable callback can resume the conversation, arm one watcher, confirm its
receipt, tell the user where the result will land, and yield.

## Inputs and evidence

Identify the job, its owner, the authoritative result, and a fresh private
directory for the watcher receipt and any local logs. For a Codex callback,
verify the exact authorized chat UUID and run `codex queue --help` once. Use
the main chat for delegated work. Keep credentials, logs, and job details local.

## Workflow

1. Choose the wait that owns the completion evidence.
   - **New local command.** Run [watch.py](scripts/watch.py) as the job's parent
     and supply the command as an argument vector. The helper waits for the
     actual exit code.
   - **Existing local process on macOS.** Verify owner, command, and PID birth
     time once. Attach using that PID and birth time. The exit event establishes
     that the process ended. Use the original job result to determine success.
     If the process ends while attaching, reconcile against its existing result.
   - **Service-owned or remote job.** Use the service's durable completion event
     for the exact operation ID. If supported, read once, subscribe with replay
     from the saved cursor, then read the canonical result on the terminal event.
     Preserve the operation ID across disconnects and use an existing completion
     hook when available.
2. Use a permitted execution context that survives the agent turn. Read the
   running or watching receipt once. If the job has already finished, read its
   terminal receipt. If the host reaps background processes, use its persistent
   runner or supported waiter.
3. Persist the outcome before attempting one callback. The local helper can run
   `codex queue --thread UUID --resume --message TEXT` with a short receipt pointer.
   For Copilot and Claude Code, use the helper without a Codex callback. Use a
   supported host completion mechanism if available and authorized. Otherwise,
   explain that the saved receipt is available for later inspection.

### Local helper

Run from the intended job working directory. Substitute absolute executable,
helper, and receipt paths and the authorized Codex chat UUID. Use `nohup` only
where supported and approved by the host:

```bash
nohup /path/to/python /path/to/watch.py \
  --receipt /absolute/job-dir/status.json --thread CURRENT_CHAT_UUID \
  --codex /path/to/codex \
  run --log /absolute/job-dir/job.log -- ./build.sh \
  </dev/null >/absolute/job-dir/watcher.log 2>&1 &
```

Omit `--thread` and `--codex` to save a receipt without messaging a chat. For
an existing macOS process, replace the `run` arguments with
`attach --pid PID --start 'START_TIME'`. Obtain `START_TIME` with
`LC_ALL=C /bin/ps -p PID -o lstart=` and trim the surrounding whitespace.

## Outputs and handoff

Report what was started or attached and the receipt location. Read the receipt
first when resuming, then the original log or canonical artifacts. Keep
callback status separate from job status. `queued` means Codex acknowledged the
queue request. Resume can fail after queueing. A `submitting` or `uncertain`
callback needs reconciliation with the chat, without another send.

## Completion evidence

Use the child exit code, the original process result, or the exact service
operation's canonical terminal result. An attachment receipt records observed
exit with an unknown exit code. A missing or stalled receipt requires
reconciliation with the original job evidence. Report verified success, failure,
or unknown state and keep partial results and prior receipts.

## Must not

- Poll, sleep periodically, or send progress messages when only completion matters.
- Retry callbacks on a warning, timeout, or ambiguous delivery.
- Restart or cancel a job because the watcher failed or an observer disconnected.
- Bypass approvals, send job details in a callback, or overwrite prior receipts
  and job logs.
