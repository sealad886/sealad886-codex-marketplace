# Event-Driven Job Watcher

Version **0.1.1**. Wait for builds, tests, and batch jobs without polling. The
[shared skill](skills/event-driven-job-watcher/SKILL.md) records a local receipt
or uses a service's durable completion event. In Codex, the local helper can
also queue one wakeup for the originating chat.

## Install

Register the marketplace and install with your client. If it is already
registered, refresh it first. See the [marketplace install guide](https://github.com/sealad886/sealad886-codex-marketplace#install)
for client options.

```sh
codex plugin marketplace add sealad886/sealad886-codex-marketplace --ref main
codex plugin add event-driven-job-watcher@sealad886-codex-marketplace
```

```sh
copilot plugin marketplace add sealad886/sealad886-codex-marketplace
copilot plugin install event-driven-job-watcher@sealad886-codex-marketplace
```

```sh
claude plugin marketplace add sealad886/sealad886-codex-marketplace
claude plugin install event-driven-job-watcher@sealad886-codex-marketplace
```

Start a fresh session. In Codex, use
`$event-driven-job-watcher:event-driven-job-watcher`. In Copilot, ask for the
`event-driven-job-watcher` skill. In Claude Code, use
`/event-driven-job-watcher:event-driven-job-watcher`.

Example requests:

- “Run the tests with Event-Driven Job Watcher. Notify this Codex chat once the
  result is ready.”
- “Attach a watcher to the running build on this Mac. Use the build's existing
  report to determine success.”
- “Wait for the accepted service operation using its completion event.”

## Requirements

The [Python helper](skills/event-driven-job-watcher/scripts/watch.py) uses the
standard library. Run mode requires Python 3.8 or newer on macOS or Linux and
an existing job directory on a local filesystem that supports hard links.
PID attachment uses macOS kqueue. Run the helper from the job's working
directory in a host-approved process context that survives the conversation
turn.

Automatic chat wakeup requires a Codex CLI with `codex queue --resume`, an
authorized chat UUID, and access to that chat's local Codex daemon. Copilot
and Claude Code can save the local receipt using the same helper. Their own
completion mechanisms depend on the host. For remote jobs, use the service's
completion event and original operation result.

## Receipt

Run mode writes the child exit code to `status.json` and captures combined
output in the requested job log. Attach mode records observed exit with
`exit_code: null`. A setup or watcher failure records `needs_attention`.
Use a new receipt and log for each authorized attempt.

When given a chat UUID, the helper saves the terminal receipt, then sends one
`codex queue --thread UUID --resume --message TEXT` to the originating Codex
chat. The message contains the receipt path and asks the chat to verify the
result, report it to the user, and carry out any authorized follow-up. The
receipt records callback submission separately from the job result.

`queued` records CLI acceptance. Codex can accept the message even if resume
produces a warning. The user-facing report in the originating chat completes
the loop. A timeout, ambiguous CLI response, or interrupted submission needs
reconciliation without a resend. See the [callback workflow](skills/event-driven-job-watcher/SKILL.md#close-the-loop-in-codex)
and [security boundaries](SECURITY.md).

## Maintainer validation

From the marketplace checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_plugin.py plugins/event-driven-job-watcher --layout source
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_distribution_bundle.py plugins/event-driven-job-watcher
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p 'test_event_driven_job_watcher.py' -v
```

See the [marketplace contribution guide](https://github.com/sealad886/sealad886-codex-marketplace/blob/main/CONTRIBUTING.md)
for catalog checks, native installation verification, and release scanning.
