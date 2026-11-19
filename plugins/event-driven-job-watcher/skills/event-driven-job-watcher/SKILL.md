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
directory for the watcher receipt and any local logs. Keep credentials, logs,
and job details local.

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
3. Persist the terminal result before sending the completion callback. When
   using Codex, follow the loop below. In Copilot and Claude Code, save the
   receipt and use an authorized host completion mechanism if available.

## Close the loop in Codex

1. **Bind the watcher to the originating chat.** Resolve the exact authorized
   chat UUID from trusted session context. Use `CODEX_THREAD_ID` when the host
   provides it for the owning chat. Use the main chat for delegated work.
   Run `codex queue --help` on the CLI the watcher will use. Verify that
   the callback runner can reach the chat's daemon and that the resumed chat
   can read the receipt. If any prerequisite is missing, save the result for
   later inspection and tell the user where to find it.
2. **Send one completion message.** After saving the terminal receipt,
   [watch.py](scripts/watch.py) sends this command to the local daemon. Use the
   same command from an authorized service completion hook when that hook
   owns the callback. Keep exactly one sender for the job.

   ```bash
   codex queue --thread "$chat_uuid" --resume \
     --message "Job watcher finished. Read the receipt at \"$receipt\" first. Verify the job outcome, report it to the user, and continue any authorized follow-up."
   ```

   - `--thread` targets the exact existing chat UUID. Keep that UUID when
     launching the job, so the callback returns to the conversation that owns it.
   - `--resume` asks Codex to resume the chat after queueing. A resume warning
     can accompany a successful queue request and an exit code of zero.
   - `--message` carries the receipt pointer and the action for the resumed
     chat. Keep job output and credentials in their local storage.
   - A service hook that uses a verified remote Codex daemon can select it
     with `--remote`. If the daemon requires authentication, use
     `--remote-auth-token-env` with the name of the configured environment
     variable. The packaged helper uses the local daemon.
3. **Close the job in the resumed chat.** Treat the callback as a continuation
   of the original request. Open the receipt first, then verify the outcome
   against the job log or canonical result. Tell the user what finished and
   what the evidence shows, then carry out any authorized follow-up. Use
   `status` and `exit_code` as job evidence. `callback.status` tracks message
   submission separately. If the callback arrives while that field is
   `submitting`, use the terminal job fields immediately. Reconcile uncertain
   delivery against the original chat and receipt without another send.

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

Before yielding, tell the user what was started or attached and where the result
will land. `queued` records CLI acceptance of the message. The resumed chat's
user-facing report closes the loop.

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
