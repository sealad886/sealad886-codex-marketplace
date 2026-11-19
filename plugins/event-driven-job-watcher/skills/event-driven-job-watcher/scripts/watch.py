#!/usr/bin/env python3
"""Wait for one local job and optionally queue one Codex wakeup."""

import argparse
import json
import os
import select
import subprocess
import tempfile
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save(path, state, *, create=False):
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
        try:
            json.dump(state, temporary, indent=2)
            temporary.write("\n")
            temporary.close()
            if create:
                # Publish valid JSON and reserve the receipt without clobbering an attempt.
                os.link(temporary_path, path)
            else:
                temporary_path.replace(path)
        finally:
            temporary_path.unlink(missing_ok=True)


def birth(pid):
    return subprocess.check_output(
        ["/bin/ps", "-p", str(pid), "-o", "lstart="],
        env={**os.environ, "LC_ALL": "C"},
        text=True,
    ).strip()


def attach(args, state):
    if not hasattr(select, "kqueue"):
        raise RuntimeError("PID attachment requires kqueue on this host")
    if birth(args.pid) != args.start:
        raise RuntimeError("PID birth time differs from supplied identity")
    event = select.kevent(
        args.pid, filter=select.KQ_FILTER_PROC,
        flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
        fflags=select.KQ_NOTE_EXIT,
    )
    with closing(select.kqueue()) as queue:
        queue.control([event], 0, 0)
        if birth(args.pid) != args.start:
            raise RuntimeError("PID identity changed while arming watcher")
        state.update(status="watching", job_pid=args.pid, job_start=args.start)
        save(args.receipt, state)
        observed = queue.control(None, 1, None)[0]
        if observed.flags & select.KQ_EV_ERROR or not observed.fflags & select.KQ_NOTE_EXIT:
            raise RuntimeError("Watcher did not receive a process exit event")
    state.update(status="exit_observed", exit_code=None)


def run(args, state):
    # Logs can contain sensitive job output. Preserve restrictive permissions
    # regardless of the caller's umask.
    log_fd = os.open(args.log, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(log_fd, "wb") as log:
        child = subprocess.Popen(
            args.command, stdin=subprocess.DEVNULL, stdout=log,
            stderr=subprocess.STDOUT, start_new_session=True,
        )
        state.update(status="running", job_pid=child.pid, job_log=str(args.log.resolve()))
        save(args.receipt, state)
        code = child.wait()
    state.update(status="completed" if code == 0 else "failed", exit_code=code)


def notify(args, state):
    state["callback"] = {"status": "submitting"}
    save(args.receipt, state)
    try:
        result = subprocess.run(
            [
                args.codex, "queue", "--thread", args.thread, "--resume", "--message",
                f"Job watcher settled. Read {args.receipt} first.",
            ],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=30, check=False,
        )
        state["callback"] = {
            # The CLI can report successful queueing even if resume failed.
            "status": "queued" if result.returncode == 0 else "uncertain",
            "exit_code": result.returncode,
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        state["callback"] = {"status": "uncertain", "error": type(error).__name__}
    save(args.receipt, state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--thread", type=lambda value: str(uuid.UUID(value)))
    parser.add_argument("--codex", default="codex")
    subcommands = parser.add_subparsers(dest="mode", required=True)
    launch = subcommands.add_parser("run")
    launch.add_argument("--log", type=Path, required=True)
    launch.add_argument("command", nargs=argparse.REMAINDER)
    existing = subcommands.add_parser("attach")
    existing.add_argument("--pid", type=int, required=True)
    existing.add_argument("--start", required=True)
    args = parser.parse_args()
    if args.mode == "run":
        if args.command and args.command[0] == "--":
            args.command.pop(0)
        if not args.command:
            parser.error("run requires a command after --")
    elif args.pid <= 0:
        parser.error("attach requires a positive PID")

    args.receipt = args.receipt.absolute()
    state = {"status": "starting", "mode": args.mode, "started_at": timestamp(),
             "watcher_pid": os.getpid(), "exit_code": None}
    try:
        save(args.receipt, state, create=True)
    except OSError as error:
        parser.exit(1, f"Could not create receipt: {error}\n")
    try:
        (run if args.mode == "run" else attach)(args, state)
    except (OSError, subprocess.SubprocessError, RuntimeError, KeyboardInterrupt) as error:
        state.update(status="needs_attention", error=f"{type(error).__name__}: {error}")
    state["finished_at"] = timestamp()
    save(args.receipt, state)
    if args.thread:
        notify(args, state)
    return int(state["status"] not in {"completed", "exit_observed"})


if __name__ == "__main__":
    raise SystemExit(main())
