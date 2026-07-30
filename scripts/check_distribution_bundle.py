#!/usr/bin/env python3
"""Build and validate the exact self-contained plugin distribution payload."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path, PurePosixPath, PureWindowsPath

from check_plugin import validate


OPTIONAL_ROOT_FILES = {
    ".codexignore",
    "LICENSE",
    "LICENSE.md",
    "LICENSE.txt",
    "NOTICE.md",
    "README.md",
    "SECURITY.md",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "pyproject.toml",
    "yarn.lock",
}
COMPONENT_FIELDS = ("skills", "scripts", "apps", "app", "appConfig", "hooks")
PROJECT_DELIVERY_SHARED_RUNTIME_PATHS = (
    "skills/.shared/operating-model.md",
    "skills/.shared/artifact-templates.md",
    "skills/.shared/external-systems.md",
    "skills/.shared/live-route-receipt-v3.schema.json",
    "skills/.shared/route-profiles-v1.json",
)
EXPECTED_SKILL_COUNTS = {
    "conversation-visuals": 4,
    "project-delivery": 13,
}
UNIVERSAL_FORBIDDEN_DISTRIBUTION_PARTS = {
    ".git",
    ".github",
    ".venv",
    "__pycache__",
    "node_modules",
    "tests",
}
PROJECT_DELIVERY_FORBIDDEN_DISTRIBUTION_PARTS = {"references", "scripts"}
PLUGIN_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_PLUGIN_NAME_LENGTH = 64
SUPPORTED_MCP_SERVER_FIELDS = {"command", "args", "cwd", "tool_timeout_sec"}


def forbidden_distribution_parts(plugin_name: str) -> set[str]:
    forbidden = set(UNIVERSAL_FORBIDDEN_DISTRIBUTION_PARTS)
    if plugin_name == "project-delivery":
        forbidden.update(PROJECT_DELIVERY_FORBIDDEN_DISTRIBUTION_PARTS)
    return forbidden


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).parents[1] / "plugins" / "project-delivery"),
        help="plugin source root",
    )
    parser.add_argument(
        "--output",
        help="materialize the validated runtime closure at this exact plugin directory",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="replace an existing clean distribution directory after identity and safety checks",
    )
    return parser.parse_args(argv)


def is_absolute_path(value: str) -> bool:
    return (
        Path(value).is_absolute()
        or PurePosixPath(value).is_absolute()
        or PureWindowsPath(value).is_absolute()
    )


def safe_relative_path(value: str) -> Path:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    candidate = Path(normalized)
    if not normalized or is_absolute_path(value) or ".." in candidate.parts:
        raise ValueError(f"unsafe manifest path: {value}")
    return candidate


def add_declared_path(root: Path, selected: set[Path], value: str) -> None:
    relative = safe_relative_path(value)
    source = root / relative
    if source.is_file():
        selected.add(relative)
    elif source.is_dir():
        selected.update(path.relative_to(root) for path in source.rglob("*") if path.is_file())
    else:
        raise ValueError(f"declared path does not exist: {value}")


def add_local_python_mcp_dependencies(
    root: Path,
    selected: set[Path],
    declaration: str,
) -> None:
    """Select the one local MCP launch contract used by Conversation Visuals."""
    declaration_path = safe_relative_path(declaration)
    config_path = root / declaration_path
    if not config_path.is_file():
        raise ValueError(f"declared path does not exist: {declaration}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("local MCP config must contain an object")
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise ValueError("local MCP config must contain a non-empty mcpServers object")

    selected.add(declaration_path)
    resolved_root = root.resolve()
    for server_name, server in servers.items():
        if not isinstance(server_name, str) or not isinstance(server, dict):
            raise ValueError("local MCP server config must contain a named object")
        unsupported_fields = set(server) - SUPPORTED_MCP_SERVER_FIELDS
        if unsupported_fields:
            raise ValueError(
                "unsupported local MCP server fields: "
                + ", ".join(sorted(unsupported_fields))
            )
        if server.get("command") != "python3":
            raise ValueError("local MCP server command must be python3")
        if server.get("cwd") != ".":
            raise ValueError("local MCP server cwd must be '.'")
        timeout = server.get("tool_timeout_sec")
        if timeout is not None and (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise ValueError("local MCP server tool_timeout_sec must be positive")

        arguments = server.get("args")
        if not isinstance(arguments, list) or len(arguments) != 1:
            raise ValueError("local MCP server args must contain one Python script")
        script = arguments[0]
        if not isinstance(script, str):
            raise ValueError("local MCP server script must be a string")
        script_path = safe_relative_path(script)
        if script_path.suffix != ".py":
            raise ValueError("local MCP server must launch a .py script")

        script_source = root / script_path
        resolved_script = script_source.resolve()
        if not resolved_script.is_relative_to(resolved_root):
            raise ValueError(f"local MCP server script escapes the plugin root: {script}")
        if not script_source.is_file():
            raise ValueError(f"local MCP server script is not a regular file: {script}")
        selected.add(script_path)


def select_paths(root: Path) -> set[Path]:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("plugin manifest must contain an object")
    selected = {Path(".codex-plugin/plugin.json")}
    selected.update(path for path in map(Path, OPTIONAL_ROOT_FILES) if (root / path).is_file())

    for field in COMPONENT_FIELDS:
        value = manifest.get(field)
        if isinstance(value, str):
            add_declared_path(root, selected, value)

    mcp_declaration = manifest.get("mcpServers")
    if manifest.get("name") == "conversation-visuals" and mcp_declaration is None:
        raise ValueError("conversation-visuals must declare its local MCP config")
    if mcp_declaration is not None:
        if not isinstance(mcp_declaration, str):
            raise ValueError("mcpServers must declare a local config file")
        add_local_python_mcp_dependencies(root, selected, mcp_declaration)

    interface = manifest.get("interface", {})
    if isinstance(interface, dict):
        for field in ("composerIcon", "logo"):
            value = interface.get(field)
            if isinstance(value, str):
                add_declared_path(root, selected, value)
        screenshots = interface.get("screenshots", [])
        if isinstance(screenshots, list):
            for value in screenshots:
                if isinstance(value, str):
                    add_declared_path(root, selected, value)
    return selected


def payload_sha256(root: Path, relative_paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for relative in relative_paths:
        encoded_path = relative.as_posix().encode("utf-8")
        contents = (root / relative).read_bytes()
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        digest.update(len(contents).to_bytes(8, "big"))
        digest.update(contents)
    return digest.hexdigest()


def read_plugin_name(root: Path) -> str:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("plugin manifest must contain an object")
    plugin_name = manifest.get("name")
    if not isinstance(plugin_name, str) or not PLUGIN_NAME.fullmatch(plugin_name):
        raise ValueError("plugin name must be lower-case hyphen-case")
    if len(plugin_name) > MAX_PLUGIN_NAME_LENGTH:
        raise ValueError(
            f"plugin name must not exceed {MAX_PLUGIN_NAME_LENGTH} characters"
        )
    return plugin_name


def copy_selected(root: Path, destination: Path, selected: list[Path]) -> None:
    started = time.monotonic()
    for index, relative in enumerate(selected, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(selected) - index)
        print(f"CLOSURE [{index}/{len(selected)}] file={relative} eta={eta:.1f}s", flush=True)
        source = root / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def expected_directories(relative_paths: list[Path] | set[Path]) -> set[Path]:
    expected: set[Path] = set()
    for relative in relative_paths:
        parent = relative.parent
        while parent != Path("."):
            expected.add(parent)
            parent = parent.parent
    return expected


def inventory_tree(
    root: Path,
    label: str,
    phase: str,
    forbidden_parts: set[str] | None = None,
) -> tuple[set[Path], set[Path], list[str]]:
    if forbidden_parts is None:
        forbidden_parts = forbidden_distribution_parts(read_plugin_name(root))
    files: set[Path] = set()
    directories: set[Path] = set()
    errors: list[str] = []
    entries = sorted(root.rglob("*"))
    started = time.monotonic()
    for index, path in enumerate(entries, 1):
        elapsed = time.monotonic() - started
        eta = (elapsed / index) * (len(entries) - index)
        relative = path.relative_to(root)
        print(
            f"{phase} [{index}/{len(entries)}] side={label} path={relative} eta={eta:.1f}s",
            flush=True,
        )
        if path.is_symlink():
            errors.append(f"{label} contains unsupported symlink: {relative}")
            continue
        if path.is_file():
            files.add(relative)
            if path.stat().st_mode & 0o111:
                errors.append(f"{label} contains executable file: {relative}")
        elif path.is_dir():
            directories.add(relative)
        else:
            errors.append(f"{label} contains unsupported file type: {relative}")

        forbidden = forbidden_parts.intersection(relative.parts)
        if forbidden:
            errors.append(
                f"{label} contains forbidden path: {relative} "
                f"({', '.join(sorted(forbidden))})"
            )
    return files, directories, errors


def validate_source_boundary(
    root: Path,
    selected: list[Path],
    forbidden_parts: set[str] | None = None,
) -> list[str]:
    if forbidden_parts is None:
        forbidden_parts = forbidden_distribution_parts(read_plugin_name(root))
    actual_files, actual_directories, errors = inventory_tree(
        root,
        "plugin package boundary",
        "BOUNDARY",
        forbidden_parts,
    )
    expected_files = set(selected)
    expected_directory_set = expected_directories(expected_files)
    for missing in sorted(expected_files - actual_files):
        errors.append(f"plugin package boundary is missing selected file: {missing}")
    for extra in sorted(actual_files - expected_files):
        errors.append(f"plugin package boundary contains undeclared file: {extra}")
    for missing in sorted(expected_directory_set - actual_directories):
        errors.append(f"plugin package boundary is missing selected directory: {missing}")
    for extra in sorted(actual_directories - expected_directory_set):
        errors.append(f"plugin package boundary contains undeclared directory: {extra}")
    return errors


def validate_distribution_tree(
    destination: Path,
    selected: list[Path],
    plugin_name: str,
    forbidden_parts: set[str],
) -> list[str]:
    errors, skill_count, _ = validate(destination, "source")
    expected_skill_count = EXPECTED_SKILL_COUNTS.get(plugin_name)
    if expected_skill_count is None:
        if skill_count < 1:
            errors.append("runtime closure must contain at least one skill")
    elif skill_count != expected_skill_count:
        errors.append(
            f"runtime closure must contain {expected_skill_count} skills, "
            f"found {skill_count}"
        )

    shared_runtime_paths = (
        PROJECT_DELIVERY_SHARED_RUNTIME_PATHS
        if plugin_name == "project-delivery"
        else ()
    )
    for required in shared_runtime_paths:
        if not (destination / required).is_file():
            errors.append(f"runtime closure is missing dependency: {required}")

    actual_files, actual_directories, inventory_errors = inventory_tree(
        destination,
        "runtime closure",
        "RUNTIME",
        forbidden_parts,
    )
    errors.extend(inventory_errors)
    expected_files = set(selected)
    expected_directory_set = expected_directories(expected_files)
    for missing in sorted(expected_files - actual_files):
        errors.append(f"runtime closure is missing selected file: {missing}")
    for extra in sorted(actual_files - expected_files):
        errors.append(f"runtime closure contains unselected file: {extra}")
    for missing in sorted(expected_directory_set - actual_directories):
        errors.append(f"runtime closure is missing selected directory: {missing}")
    for extra in sorted(actual_directories - expected_directory_set):
        errors.append(f"runtime closure contains unselected directory: {extra}")
    return errors


def build_runtime_closure(root: Path, destination: Path) -> tuple[list[str], list[Path], str]:
    errors: list[str] = []
    try:
        plugin_name = read_plugin_name(root)
        selected = sorted(select_paths(root))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [str(error)], [], ""

    forbidden_parts = forbidden_distribution_parts(plugin_name)
    errors.extend(validate_source_boundary(root, selected, forbidden_parts))
    if errors:
        return errors, selected, ""
    copy_selected(root, destination, selected)
    errors.extend(
        validate_distribution_tree(
            destination,
            selected,
            plugin_name,
            forbidden_parts,
        )
    )
    digest = payload_sha256(destination, selected) if not errors else ""
    return errors, selected, digest


def control_plane_owner(output: Path) -> Path | None:
    for candidate in (output, *output.parents):
        markers = [
            marker
            for marker in (candidate / ".git", candidate / ".venv")
            if marker.exists() or marker.is_symlink()
        ]
        if markers:
            return candidate
    return None


def validate_existing_output(output: Path, plugin_name: str) -> list[str]:
    errors: list[str] = []
    if output.name != plugin_name:
        errors.append(f"output directory must be named {plugin_name}: {output}")
    if not output.is_dir():
        errors.append(f"refusing to replace a non-directory output: {output}")

    control_plane = control_plane_owner(output)
    if control_plane is not None:
        errors.append(
            "refusing to replace a distribution inside a source checkout or "
            f"Python environment: {output} (control plane: {control_plane})"
        )

    manifest_path = output / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"refusing to replace output with unreadable identity: {error}")
    else:
        if not isinstance(manifest, dict):
            errors.append(
                "refusing to replace output with invalid identity: "
                "plugin manifest must contain an object"
            )
        elif manifest.get("name") != plugin_name:
            errors.append(
                f"refusing to replace output for plugin {manifest.get('name')!r}; "
                f"expected {plugin_name!r}"
            )
    if errors:
        return errors

    try:
        selected = sorted(select_paths(output))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [f"refusing to replace output with invalid package boundary: {error}"]

    boundary_errors = validate_source_boundary(
        output,
        selected,
        forbidden_distribution_parts(plugin_name),
    )
    structural_errors, _, _ = validate(output, "source")
    errors.extend(f"refusing to replace unclean output: {error}" for error in boundary_errors)
    errors.extend(f"refusing to replace invalid output: {error}" for error in structural_errors)
    return errors


def materialize_runtime_closure(
    root: Path,
    output: Path,
    replace: bool,
) -> tuple[list[str], int, str]:
    try:
        plugin_name = read_plugin_name(root)
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ) as error:
        return [f"cannot resolve plugin identity: {error}"], 0, ""

    lexical_output = Path(os.path.abspath(os.fspath(output.expanduser())))
    if lexical_output.is_symlink():
        return [f"refusing to materialize through an output symlink: {lexical_output}"], 0, ""
    resolved_output = lexical_output.resolve()
    if (
        resolved_output == root
        or resolved_output.is_relative_to(root)
        or root.is_relative_to(resolved_output)
    ):
        return [f"output must be separate from the source checkout: {lexical_output}"], 0, ""
    if lexical_output.name != plugin_name:
        return [f"output directory must be named {plugin_name}: {lexical_output}"], 0, ""
    control_plane = control_plane_owner(lexical_output)
    if control_plane is not None:
        return [
            "refusing to materialize a distribution inside a source checkout or "
            f"Python environment: {lexical_output} (control plane: {control_plane})"
        ], 0, ""
    if lexical_output.exists() and not replace:
        return [
            f"output already exists; rerun with --replace after inspection: {lexical_output}"
        ], 0, ""
    if lexical_output.exists():
        existing_errors = validate_existing_output(lexical_output, plugin_name)
        if existing_errors:
            return existing_errors, 0, ""
    output = lexical_output

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{plugin_name}-distribution-",
        dir=output.parent,
    ) as temporary:
        staging_parent = Path(temporary)
        staging = staging_parent / plugin_name
        errors, selected, digest = build_runtime_closure(root, staging)
        if errors:
            return errors, len(selected), ""

        previous: Path | None = None
        if output.exists():
            previous = output.parent / f".{plugin_name}-previous-{uuid.uuid4().hex}"
        try:
            if previous is not None:
                os.replace(output, previous)
            os.replace(staging, output)
        except OSError as error:
            if previous is not None and previous.exists() and not output.exists():
                try:
                    os.replace(previous, output)
                except OSError as restore_error:
                    return [
                        f"distribution swap failed: {error}; rollback also failed: "
                        f"{restore_error}; prior output retained at {previous}"
                    ], len(selected), ""
            if previous is None:
                return [
                    f"distribution staging swap failed before an output was created: {error}"
                ], len(selected), ""
            return [
                f"distribution swap failed and the prior output was preserved: {error}"
            ], len(selected), ""
        if previous is not None:
            try:
                shutil.rmtree(previous)
            except OSError as error:
                return [
                    "new distribution was installed, but the prior clean distribution "
                    f"could not be removed and remains at {previous}: {error}"
                ], len(selected), ""
    return [], len(selected), digest


def validate_runtime_closure(root: Path) -> tuple[list[str], int, str]:
    try:
        plugin_name = read_plugin_name(root)
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ) as error:
        return [f"cannot resolve plugin identity: {error}"], 0, ""
    with tempfile.TemporaryDirectory(prefix=f"{plugin_name}-runtime-closure-") as temporary:
        destination = Path(temporary) / plugin_name
        errors, selected, digest = build_runtime_closure(root, destination)
    return errors, len(selected), digest


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).expanduser().resolve()
    if args.replace and not args.output:
        print("ERROR --replace requires --output")
        return 1
    if args.output:
        errors, selected_count, digest = materialize_runtime_closure(
            root,
            Path(args.output),
            args.replace,
        )
    else:
        errors, selected_count, digest = validate_runtime_closure(root)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1
    action = "materialized" if args.output else "validated"
    output = f" output={Path(args.output).expanduser().resolve()}" if args.output else ""
    plugin_name = read_plugin_name(root)
    _, skill_count, _ = validate(root, "source")
    shared_runtime_count = (
        len(PROJECT_DELIVERY_SHARED_RUNTIME_PATHS)
        if plugin_name == "project-delivery"
        else 0
    )
    print(
        f"PASS action={action} plugin={plugin_name} selected_files={selected_count} "
        f"skills={skill_count} shared_runtime={shared_runtime_count} "
        f"payload_sha256={digest}{output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
