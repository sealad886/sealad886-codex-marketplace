#!/usr/bin/env python3
"""Inject the installed skill after observed native worktree creation.

Pending-operation markers are transient correlation state, never ownership
records. This handler does not run Git, mutate a registry, or infer an owner.
"""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import sys

MAX_EVENT_BYTES = 1024 * 1024
MAX_SKILL_BYTES = 128 * 1024
TOOL_NAME = re.compile(r"(?:mcp__codex_app__)?(create_worktree|get_worktree_creation_status)")
OPERATION_ID = re.compile(r"[A-Za-z0-9_-]{1,128}")
SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"
STATE_DIRECTORY = "worktree-activity-pending"


class HookError(Exception):
    """A recoverable hook setup or correlation-state failure."""


def strict_json(value: str) -> object:
    def object_pairs(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = item
        return result

    def reject_constant(_value):
        raise ValueError("nonstandard JSON number")

    return json.loads(value, object_pairs_hook=object_pairs, parse_constant=reject_constant)


def response_payload(response: object) -> dict | None:
    """Unwrap only the native direct, MCP-text, and dynamic-text result forms."""
    if isinstance(response, str):
        try:
            response = strict_json(response)
        except (ValueError, RecursionError):
            return None
    if not isinstance(response, dict):
        return None
    if response.get("type") in ("created", "pending") or "stage" in response:
        return response
    for field, kind in (("content", "text"), ("contentItems", "inputText")):
        items = response.get(field)
        if not isinstance(items, list):
            continue
        candidates = []
        for item in items:
            if not isinstance(item, dict) or item.get("type") != kind or not isinstance(item.get("text"), str):
                continue
            try:
                payload = strict_json(item["text"])
            except (ValueError, RecursionError):
                continue
            if isinstance(payload, dict):
                candidates.append(payload)
        # A single structured native result is unambiguous. Do not search
        # diagnostic text or recursively interpret arbitrary nested fields.
        return candidates[0] if len(candidates) == 1 else None
    return None


def created(payload: object) -> bool:
    if not isinstance(payload, dict) or payload.get("type") != "created":
        return False
    return all(isinstance(payload.get(field), str) and payload[field].strip()
               and "\0" not in payload[field] and Path(payload[field]).is_absolute()
               for field in ("worktreeGitRoot", "worktreeWorkspaceRoot"))


def operation_id(value: object) -> str | None:
    return value if isinstance(value, str) and OPERATION_ID.fullmatch(value) else None


def safe_directory(path: Path) -> Path:
    if not path.is_absolute() or ".." in path.parts:
        raise HookError("PLUGIN_DATA must be an absolute directory without traversal")
    for ancestor in (*reversed(path.parents), path):
        if ancestor.is_symlink():
            raise HookError("pending correlation directory must not contain symlinks")
    return path


@contextmanager
def state_directory(*, create: bool):
    value = os.environ.get("PLUGIN_DATA")
    if not value:
        if create:
            raise HookError("PLUGIN_DATA is required to track pending worktree creation")
        yield None
        return
    path = safe_directory(Path(value)) / STATE_DIRECTORY
    safe_directory(path)
    if create:
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
    elif not path.exists():
        yield None
        return
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        # This directory is a stable synchronization target: the handler never
        # removes it. Serialize marker inspection, skill loading, and consumption
        # across callbacks; closing the descriptor also releases the lock.
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield descriptor
    finally:
        os.close(descriptor)


def marker_exists(directory: int, operation: str) -> bool:
    try:
        info = os.stat(operation + ".pending", dir_fd=directory, follow_symlinks=False)
    except FileNotFoundError:
        return False
    if not stat.S_ISREG(info.st_mode) or info.st_size != 0 or info.st_nlink != 1:
        raise HookError("unsafe pending correlation marker; preserved for inspection")
    return True


def remember_pending(operation: str) -> None:
    with state_directory(create=True) as directory:
        try:
            descriptor = os.open(operation + ".pending", os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
                                 0o600, dir_fd=directory)
        except FileExistsError:
            marker_exists(directory, operation)
            return
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.fsync(directory)


def consume_pending(directory: int, operation: str) -> bool:
    if not marker_exists(directory, operation):
        return False
    try:
        # The caller holds the stable state-directory lock across this claim.
        os.unlink(operation + ".pending", dir_fd=directory)
    except FileNotFoundError:
        return False
    os.fsync(directory)
    return True


def skill_context() -> str:
    try:
        with SKILL_PATH.open("r", encoding="utf-8") as stream:
            skill = stream.read(MAX_SKILL_BYTES + 1)
        if not skill.strip() or len(skill.encode("utf-8")) > MAX_SKILL_BYTES:
            raise HookError("installed SKILL.md is empty or exceeds the supported size")
    except (OSError, UnicodeError) as error:
        raise HookError("installed SKILL.md could not be loaded; pending correlation was retained") from error
    return ("Worktree Activity: a native tool reported that a new Git worktree was created. "
            "The trusted installed skill follows in full. Only the responsible user-facing "
            "coordinator may register or reconcile ownership for an actual authorized assignment. "
            "Delegated agents must report the new worktree to their coordinator and must not "
            "mutate ownership records. This hook does not register ownership, establish a root "
            "identity, or authorize development, worktree creation, cancellation, or deletion. "
            "Respect existing approval boundaries. Resolve skill-relative resources against "
            f"the following installed source: {json.dumps(str(SKILL_PATH), ensure_ascii=False)}.\n\n"
            + skill)


def handle(event: object) -> str | None:
    if not isinstance(event, dict) or event.get("hook_event_name") != "PostToolUse":
        return None
    name = event.get("tool_name")
    match = TOOL_NAME.fullmatch(name) if isinstance(name, str) else None
    if match is None:
        return None
    payload = response_payload(event.get("tool_response"))
    if payload is None:
        return None
    if match.group(1) == "create_worktree":
        if created(payload):
            return skill_context()
        if payload.get("type") == "pending":
            operation = operation_id(payload.get("operationId"))
            if operation is not None:
                remember_pending(operation)
        return None
    arguments = event.get("tool_input")
    if not isinstance(arguments, dict):
        return None
    operation = operation_id(arguments.get("operationId"))
    if operation is None or payload.get("operationId") != operation:
        return None
    if payload.get("stage") not in ("completed", "failed"):
        return None
    if payload["stage"] == "completed" and not created(payload.get("result")):
        # A malformed completion is not evidence that the observed creation
        # finished. Retain its correlation marker for a valid status callback.
        return None
    with state_directory(create=False) as directory:
        if directory is None or not marker_exists(directory, operation):
            return None
        # Load before claiming: a broken install must not consume retry evidence.
        context = skill_context() if created(payload.get("result")) else None
        if consume_pending(directory, operation):
            return context
    return None


def main() -> int:
    try:
        raw = sys.stdin.buffer.read(MAX_EVENT_BYTES + 1)
        if len(raw) > MAX_EVENT_BYTES:
            return 0
        try:
            event = strict_json(raw.decode("utf-8"))
        except (ValueError, UnicodeError, RecursionError):
            return 0
        context = handle(event)
        if context is not None:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                    "additionalContext": context}}, ensure_ascii=False))
        return 0
    except (HookError, OSError) as error:
        # Never echo a tool response, command output, native owner ID, or secret.
        message = str(error) if isinstance(error, HookError) else "pending correlation state could not be accessed"
        print("worktree-activity hook: " + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
