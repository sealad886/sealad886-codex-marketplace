"""Bounded snapshots of regular files inside a selected filesystem root."""

from __future__ import annotations

import os
import stat
from pathlib import Path


MAX_CONTROL_BYTES = 4 * 1024 * 1024
MAX_TEXT_BYTES = 16 * 1024 * 1024
MAX_PAYLOAD_BYTES = 32 * 1024 * 1024


def read_bytes(
    path: Path,
    *,
    root: Path | None = None,
    max_bytes: int = MAX_CONTROL_BYTES,
) -> bytes:
    """Read once without following links beneath root; reject oversized input.

    The selected root may use a filesystem alias (such as macOS /var). Every
    descendant is opened relative to a directory descriptor with O_NOFOLLOW.
    Nonblocking open lets fstat reject FIFOs before any blocking read.
    """
    path = path.absolute()
    if root is None:
        # The caller selected a file, so parent aliases such as /tmp are valid.
        # Retain the original final component for no-follow descriptor open.
        selected_root = path.parent.resolve()
        path = selected_root / path.name
    else:
        selected_root = root.absolute()
    if selected_root.is_symlink():
        raise OSError(f"regular non-symlink directory required: {selected_root}")
    try:
        relative = path.relative_to(selected_root)
    except ValueError:
        raise OSError(f"file escapes selected root: {path}") from None
    if not relative.parts or ".." in relative.parts:
        raise OSError(f"file escapes selected root: {path}")
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise OSError("regular non-symlink reads are unsupported on this platform")
    directories: list[int] = []
    descriptor: int | None = None
    try:
        directories.append(os.open(selected_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW))
        for part in relative.parts[:-1]:
            try:
                directories.append(os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directories[-1],
                ))
            except OSError as error:
                raise OSError(f"regular non-symlink directory required: {path}: {error}") from error
        try:
            descriptor = os.open(
                relative.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=directories[-1],
            )
        except OSError as error:
            raise OSError(f"regular non-symlink file required: {path}: {error}") from error
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise OSError(f"regular non-symlink file required: {path}")
        if metadata.st_size > max_bytes:
            raise OSError(f"file exceeds {max_bytes}-byte limit: {path}")
        chunks: list[bytes] = []
        count = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - count + 1))
            if not chunk:
                return b"".join(chunks)
            count += len(chunk)
            if count > max_bytes:
                raise OSError(f"file exceeds {max_bytes}-byte limit: {path}")
            chunks.append(chunk)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        for directory in reversed(directories):
            os.close(directory)


def read_text(path: Path, *, root: Path | None = None, max_bytes: int = MAX_CONTROL_BYTES) -> str:
    # Match ordinary text-file reads while keeping byte snapshots/hashes exact.
    text = read_bytes(path, root=root, max_bytes=max_bytes).decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n")
