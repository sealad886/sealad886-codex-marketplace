#!/usr/bin/env python3
"""Cooperative, root-owned unfinished-work records for existing local Git worktrees.

No network, liveness inference, messaging, worktree creation, or automatic cleanup.
Requires POSIX flock and local filesystems with atomic rename and fsync support.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import time

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit("ERROR jsonschema is missing; use the package's isolated setup instructions")

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references/worktree-activity-v1.schema.json"
UUID_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z")
STAMP_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\Z")
TERMINAL = {"completed", "canceled"}
STATUSES = ("pending", "in_progress", "blocked", "paused", "completed", "canceled")
MAX_RECORD_BYTES = 1024 * 1024


class RegistryError(Exception):
    """Visible, nondestructive validation or operation failure."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def native_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not UUID_PATTERN.fullmatch(value):
        raise RegistryError(f"{label} must be a native canonical UUID-shaped identifier (any version)")
    return value


def identity(require: bool = False) -> dict:
    owner = os.environ.get("CODEX_THREAD_ID")
    session = os.environ.get("CODEX_SESSION_ID") or None
    if owner is not None:
        native_id(owner, "CODEX_THREAD_ID")
    if require and owner is None:
        raise RegistryError("CODEX_THREAD_ID is missing; mutation requires native executing-thread identity")
    if session is not None:
        native_id(session, "CODEX_SESSION_ID")
    return {"root_thread_id": owner, "session_id": session,
            "runtime_version": os.environ.get("CODEX_VERSION"),
            "role_enforcement": "explicit --coordinator assertion; no supported shell role detector"}


def safe_path(path: Path) -> Path:
    """Reject symlinks before resolving, including existing ancestors."""
    path = Path(os.path.abspath(os.path.expanduser(str(path))))
    for part in reversed((path, *path.parents)):
        if part.is_symlink():
            raise RegistryError(f"unsafe symlink: {part}")
    return path


def regular_file(path: Path) -> None:
    safe_path(path)
    info = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise RegistryError(f"expected a regular, singly linked file: {path}")


def git(path: Path, *arguments: str) -> str:
    # Explicit -C owns repository selection; inherited Git directory overrides do not.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    try:
        result = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
                                 "-C", str(path), *arguments], capture_output=True,
                                text=True, timeout=15, env=env)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RegistryError(f"Git inspection failed at {path}: {error}") from error
    if result.returncode:
        raise RegistryError(f"Git inspection failed at {path}: {result.stderr.strip()}")
    return result.stdout.rstrip("\n")


def git_worktrees(path: Path) -> list[Path]:
    fields = git(path, "worktree", "list", "--porcelain", "-z").split("\0")
    return [Path(field[len("worktree "):]) for field in fields if field.startswith("worktree ")]


def checkout(target: Path) -> dict:
    target = safe_path(target)
    top = safe_path(Path(git(target, "rev-parse", "--show-toplevel")))
    worktrees = git_worktrees(top)
    if not worktrees:
        raise RegistryError("Git did not return a primary workspace")
    primary = safe_path(worktrees[0])
    area = primary / ".worktrees"
    if top == primary:
        raise RegistryError("target must be an existing linked worktree; the primary checkout is not a registration target")
    if top not in worktrees:
        raise RegistryError(f"target is not registered with Git: {top}")
    # Keep the exact branch name even when a tag has the same short name.
    head = git(top, "rev-parse", "--symbolic-full-name", "HEAD")
    branch = head.removeprefix("refs/heads/") if head.startswith("refs/heads/") else None
    warnings = []
    if not top.is_relative_to(area) or top == area:
        warnings.append({"path": str(top), "warning": f"existing linked worktree is outside the preferred location {area}; no move or cleanup is implied"})
    return {"worktree_path": str(top), "branch": branch, "workspace_root": str(primary),
            "warnings": warnings}


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise RegistryError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> object:
    regular_file(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
        value = stream.read(MAX_RECORD_BYTES + 1)
    if len(value.encode("utf-8")) > MAX_RECORD_BYTES:
        raise RegistryError(f"record exceeds {MAX_RECORD_BYTES} bytes: {path}")
    return json.loads(value, object_pairs_hook=reject_duplicate_keys,
                      parse_constant=lambda value: (_ for _ in ()).throw(RegistryError(f"invalid JSON number: {value}")))


def validate_record(record: object, path: Path | None = None) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda error: str(list(error.path)))
    if errors:
        error = errors[0]
        raise RegistryError(f"schema validation {list(error.path)}: {error.message}")
    assert isinstance(record, dict)
    owner = native_id(record["root_thread_id"], "root_thread_id")
    if record["session_id"] is not None:
        native_id(record["session_id"], "session_id")
    if path is not None and path.name != owner + ".activity.json":
        raise RegistryError("root_thread_id must match the ownership filename exactly")
    saved_path = Path(record["worktree_path"])
    if not saved_path.is_absolute() or str(saved_path) != record["worktree_path"] or ".." in saved_path.parts:
        raise RegistryError("worktree_path must be an absolute normalized checkout root")
    ids = set()
    for task in record["tasks"]:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", task["id"]):
            raise RegistryError("task id has unsafe syntax")
        if "assignee_thread_id" in task:
            native_id(task["assignee_thread_id"], "assignee_thread_id")
        if task["id"] in ids:
            raise RegistryError(f"duplicate task id: {task['id']}")
        ids.add(task["id"])
        for field in ("registered_at", "last_activity"):
            stamp = task[field]
            if not STAMP_PATTERN.fullmatch(stamp):
                raise RegistryError(f"{field} must be UTC RFC 3339 with Z")
            try:
                datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            except ValueError as error:
                raise RegistryError(f"invalid {field}: {stamp}") from error
        if datetime.fromisoformat(task["last_activity"].replace("Z", "+00:00")) < datetime.fromisoformat(task["registered_at"].replace("Z", "+00:00")):
            raise RegistryError("last_activity cannot precede registered_at")
        if task["status"] != "canceled" and ("cancellation_reason" in task or "authorization_ref" in task):
            raise RegistryError("cancellation fields require canceled status")
        if task["status"] != "completed" and "verification" in task:
            raise RegistryError("verification requires completed status")
    return record


def discrepancies(record: dict, metadata: dict) -> list[str]:
    return [f"{field}: recorded {record[field]!r}, current {metadata[field]!r}"
            for field in ("worktree_path", "branch") if record[field] != metadata[field]]


@contextmanager
def record_lock(directory: Path, owner: str, timeout: float):
    safe_path(directory)
    directory.mkdir(mode=0o700, exist_ok=True)
    if not directory.is_dir():
        raise RegistryError(f"registry is not a directory: {directory}")
    mutex = directory / ("." + owner + ".mutex")
    if mutex.exists() or mutex.is_symlink():
        regular_file(mutex)
    descriptor = os.open(mutex, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise RegistryError(f"unsafe synchronization target: {mutex}")
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RegistryError(f"timed out waiting for registry synchronization: {mutex}")
                time.sleep(min(0.05, max(0, deadline - time.monotonic())))
        yield
    finally:
        os.close(descriptor)


def fsync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_write(path: Path, record: dict) -> None:
    """Called only under the stable per-record mutex; replacement never truncates JSON."""
    validate_record(record, path)
    safe_path(path)
    if path.exists() or path.is_symlink():
        regular_file(path)
    payload = (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(payload) > MAX_RECORD_BYTES:
        raise RegistryError("resulting record exceeds the record byte limit")
    descriptor, temporary = tempfile.mkstemp(prefix=".write-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def new_task(task_id: str, description: str) -> dict:
    timestamp = now()
    return {"id": task_id, "description": description, "registered_at": timestamp,
            "last_activity": timestamp, "status": "pending"}


def mutate(args: argparse.Namespace) -> dict:
    if not args.coordinator:
        raise RegistryError("mutation requires --coordinator: only the responsible user-facing root may assert this")
    current = identity(require=True)
    owner = current["root_thread_id"]
    metadata = checkout(Path(args.worktree))
    directory = Path(metadata["worktree_path"]) / ".agent-activity"
    path = directory / (owner + ".activity.json")
    with record_lock(directory, owner, args.lock_timeout):
        metadata = checkout(Path(args.worktree))
        exists = path.exists() or path.is_symlink()
        record = validate_record(read_json(path), path) if exists else None
        if record is not None and record["root_thread_id"] != owner:
            raise RegistryError("native owner identity does not match record")
        if record is None:
            if args.command != "register":
                raise RegistryError("current owner's record does not exist; register the assignment first")
            record = {"schema_version": 1, "session_type": args.surface,
                      "root_thread_id": owner, "session_id": current["session_id"],
                      "worktree_path": metadata["worktree_path"], "branch": metadata["branch"],
                      "tasks": [new_task(args.task_id, args.description)]}
            atomic_write(path, record)
            return {"file": str(path), "record": record, "changed": True,
                    "warnings": metadata["warnings"]}
        differences = discrepancies(record, metadata)
        if differences and args.command != "reconcile":
            raise RegistryError("checkout discrepancy; owner must explicitly reconcile: " + "; ".join(differences))
        before = json.dumps(record, sort_keys=True)
        if args.command == "reconcile":
            record.update({field: metadata[field] for field in ("worktree_path", "branch")})
        elif args.command == "finalize":
            unfinished = [task["id"] for task in record["tasks"] if task["status"] not in TERMINAL]
            if unfinished:
                raise RegistryError("cannot finalize unfinished tasks: " + ", ".join(unfinished))
            # Validation above enforces verification and cancellation authorization.
            regular_file(path)
            os.unlink(path)
            fsync_directory(directory)
            return {"file": str(path), "finalized": True, "warnings": metadata["warnings"]}
        elif args.command == "register":
            if record["session_type"] != args.surface:
                raise RegistryError("execution surface conflicts with existing record")
            task = next((task for task in record["tasks"] if task["id"] == args.task_id), None)
            if task is None:
                record["tasks"].append(new_task(args.task_id, args.description))
            elif task["description"] != args.description:
                raise RegistryError("task ID already exists with another description; use task for an explicit update")
        elif args.command == "task":
            task = next((task for task in record["tasks"] if task["id"] == args.task_id), None)
            if task is None:
                if args.description is None:
                    raise RegistryError("new task requires --description")
                task = new_task(args.task_id, args.description)
                record["tasks"].append(task)
            changes = {key: getattr(args, key) for key in ("description", "status", "assignee_thread_id", "note", "verification", "cancellation_reason", "authorization_ref")
                       if getattr(args, key) is not None}
            if task["status"] in TERMINAL and any(task.get(key) != value for key, value in changes.items()):
                raise RegistryError("terminal tasks cannot be reopened or rewritten; register a new task ID")
            if any(task.get(key) != value for key, value in changes.items()):
                task.update(changes)
                task["last_activity"] = max(now(), task["last_activity"])
        changed = before != json.dumps(record, sort_keys=True)
        validate_record(record, path)
        if changed:
            atomic_write(path, record)
        return {"file": str(path), "record": record, "changed": changed,
                "warnings": metadata["warnings"],
                "reconciled_discrepancies": differences if args.command == "reconcile" else []}


def inspect_worktree(target: Path, record_budget: int = 10000, *,
                     expected_workspace_root: Path | None = None) -> dict:
    metadata = checkout(target)
    if expected_workspace_root is not None:
        expected = safe_path(expected_workspace_root)
        if Path(metadata["workspace_root"]) != expected:
            raise RegistryError(
                f"Git workspace mismatch at {target}: expected primary {expected}, "
                f"current primary {metadata['workspace_root']}")
        if Path(metadata["worktree_path"]) != safe_path(target):
            raise RegistryError(f"Git-listed worktree path no longer resolves to that checkout root: {target}")
    directory = safe_path(Path(metadata["worktree_path"]) / ".agent-activity")
    result = {"records": [], "errors": [], "worktrees_scanned": 1, "records_examined": 0,
              "warnings": metadata["warnings"]}
    if not directory.exists():
        return result
    if not directory.is_dir():
        raise RegistryError(f"registry is not a directory: {directory}")
    # scandir propagates permission/I/O errors instead of treating them as emptiness.
    # Stop at the first ownership entry beyond the caller's remaining budget;
    # never materialize an unbounded directory listing before applying the cap.
    paths = []
    with os.scandir(directory) as entries:
        for entry in entries:
            if not entry.name.endswith(".activity.json"):
                continue
            if len(paths) == record_budget:
                result["errors"].append({"path": str(directory), "error": "record scan limit exceeded"})
                break
            paths.append(Path(entry.path))
    for path in sorted(paths):
        result["records_examined"] += 1
        try:
            record = validate_record(read_json(path), path)
            result["records"].append({"file": str(path), "record": record,
                                      "discrepancies": discrepancies(record, metadata)})
        except (RegistryError, OSError, ValueError, UnicodeError) as error:
            result["errors"].append({"path": str(path), "error": str(error)})
    return result


def scan(projects: list[str], max_worktrees: int, max_records: int) -> dict:
    result = {"records": [], "errors": [], "worktrees_scanned": 0, "warnings": []}
    seen = set()
    record_count = 0
    for project in projects:
        try:
            primary = safe_path(Path(project))
            top = safe_path(Path(git(primary, "rev-parse", "--show-toplevel")))
            worktrees = git_worktrees(top)
            if primary != top or not worktrees or primary != safe_path(worktrees[0]):
                raise RegistryError("scan input must be the project's primary workspace root")
            targets = worktrees[1:]
            for target in targets:
                target_key = (primary, target)
                if target_key in seen:
                    continue
                seen.add(target_key)
                if result["worktrees_scanned"] >= max_worktrees:
                    raise RegistryError("worktree scan limit exceeded")
                result["worktrees_scanned"] += 1
                try:
                    inspected = inspect_worktree(target, max(0, max_records - record_count),
                                                 expected_workspace_root=primary)
                    record_count += inspected["records_examined"]
                    result["records"].extend(inspected["records"])
                    result["errors"].extend(inspected["errors"])
                    result["warnings"].extend(inspected["warnings"])
                except (RegistryError, OSError, ValueError, UnicodeError) as error:
                    result["errors"].append({"path": str(target), "error": str(error)})
        except (RegistryError, OSError, ValueError, UnicodeError) as error:
            result["errors"].append({"path": project, "error": str(error)})
    return result


def recovery(result: dict) -> dict:
    grouped = {}
    for item in result["records"]:
        owner = item["record"]["root_thread_id"]
        grouped.setdefault(owner, {"root_thread_id": owner, "url": "codex://threads/" + owner,
                                   "worktrees": []})["worktrees"].append(item)
    return {**result, "owners": [grouped[owner] for owner in sorted(grouped)]}


def positive_limit(value: str) -> int:
    number = int(value)
    if not 1 <= number <= 100000:
        raise argparse.ArgumentTypeError("limit must be between 1 and 100000")
    return number


def lock_timeout(value: str) -> float:
    number = float(value)
    if not 0 < number <= 300:
        raise argparse.ArgumentTypeError("lock timeout must be greater than zero and at most 300 seconds")
    return number


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description=__doc__,
        epilog="Exit statuses: 0 success; 1 validation/identity/operation failure; "
               "2 CLI usage error; 3 partial inspection/scan with visible errors. "
               "All mutations require --coordinator. Records never expire.")
    sub = root.add_subparsers(dest="command", required=True)
    for command in ("diagnostics", "register", "task", "reconcile", "finalize", "inspect", "validate", "scan", "recovery"):
        command_parser = sub.add_parser(command)
        command_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
        if command in {"register", "task", "reconcile", "finalize"}:
            command_parser.add_argument("--coordinator", action="store_true", help="assert responsible user-facing coordinator role; delegated agents must not use this")
            command_parser.add_argument("--lock-timeout", type=lock_timeout, default=10.0)
        if command in {"diagnostics", "register", "task", "reconcile", "finalize", "inspect"}:
            command_parser.add_argument("--worktree", required=command != "diagnostics")
        if command in {"register", "task"}:
            command_parser.add_argument("--task-id", required=True)
            command_parser.add_argument("--description", required=command == "register")
        if command == "register":
            command_parser.add_argument("--surface", required=True, choices=("codex-desktop", "codex-cli"), help="explicitly select actual execution surface")
        if command == "task":
            command_parser.add_argument("--status", choices=STATUSES)
            for flag in ("assignee-thread-id", "note", "verification", "cancellation-reason", "authorization-ref"):
                command_parser.add_argument("--" + flag)
        if command == "validate":
            command_parser.add_argument("file")
        if command in {"scan", "recovery"}:
            command_parser.add_argument("projects", nargs="+")
            command_parser.add_argument("--max-worktrees", type=positive_limit, default=1000)
            command_parser.add_argument("--max-records", type=positive_limit, default=10000)
    return root


def render(result: dict, machine: bool) -> None:
    if machine:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    elif "owners" in result:
        for owner in result["owners"]:
            print(f"Owner {owner['root_thread_id']} {owner['url']}")
            for item in owner["worktrees"]:
                print(f"  {item['record']['worktree_path']}: {len(item['record']['tasks'])} registered task(s)")
                for task in item["record"]["tasks"]:
                    print(f"    {task['id']} [{task['status']}]: {task['description']}")
                    for field in ("note", "verification", "cancellation_reason", "authorization_ref"):
                        if field in task:
                            print(f"      {field}: {task[field]}")
                for difference in item["discrepancies"]:
                    print("  DISCREPANCY " + difference)
        print(f"{len(result['owners'])} recovery target(s); {result['worktrees_scanned']} worktree(s) scanned")
        for warning in result["warnings"]:
            print(f"WARNING {warning['path']}: {warning['warning']}")
        for error in result["errors"]:
            print(f"ERROR {error['path']}: {error['error']}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command in {"register", "task", "reconcile", "finalize"}:
            result = mutate(args)
        elif args.command == "diagnostics":
            result = identity()
            if args.worktree:
                result["checkout"] = checkout(Path(args.worktree))
        elif args.command == "inspect":
            result = inspect_worktree(Path(args.worktree))
        elif args.command == "validate":
            path = safe_path(Path(args.file))
            record = validate_record(read_json(path), path)
            metadata = checkout(path.parent.parent)
            if path.parent != Path(metadata["worktree_path"]) / ".agent-activity":
                raise RegistryError("record file must be directly inside the checkout root's .agent-activity directory")
            result = {"file": str(path), "record": record, "discrepancies": discrepancies(record, metadata),
                      "warnings": metadata["warnings"]}
        else:
            result = scan(args.projects, args.max_worktrees, args.max_records)
            if args.command == "recovery":
                result = recovery(result)
        render(result, args.json)
        return 3 if result.get("errors") else 0
    except (RegistryError, OSError, ValueError, UnicodeError) as error:
        if args.json:
            print(json.dumps({"error": str(error)}, ensure_ascii=False))
        else:
            print("ERROR " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
