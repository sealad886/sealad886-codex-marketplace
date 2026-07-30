#!/usr/bin/env python3
"""Build and validate the exact self-contained plugin distribution payload."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlparse

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
COMPONENT_FIELDS = ("skills", "scripts", "mcpServers", "apps", "app", "appConfig", "hooks")
PROJECT_DELIVERY_SHARED_RUNTIME_PATHS = (
    "skills/.shared/operating-model.md",
    "skills/.shared/artifact-templates.md",
    "skills/.shared/external-systems.md",
    "skills/.shared/live-route-receipt-v3.schema.json",
    "skills/.shared/route-profiles-v1.json",
)
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
    if is_absolute_path(value) or ".." in candidate.parts:
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


def is_python_command(command: str) -> bool:
    command_name = Path(command.replace("\\", "/")).name
    return re.fullmatch(
        r"(?:python(?:\d+(?:\.\d+)*)?|py)(?:\.exe)?", command_name
    ) is not None


def is_node_command(command: str) -> bool:
    command_name = Path(command.replace("\\", "/")).name
    return command_name in {"node", "node.exe"}


def python_launch_operand(
    command: str,
    arguments: list[str],
) -> tuple[str, str | None] | None:
    """Return Python's interpreter launch mode and its first operand."""
    if not is_python_command(command):
        return None
    simple_options = set("bBdEhiIOPqsSuvVx?")
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            if index + 1 >= len(arguments):
                return None
            operand = arguments[index + 1]
            return ("stdin", None) if operand == "-" else ("script", operand)
        if argument == "-":
            return ("stdin", None)
        if argument == "--check-hash-based-pycs":
            if index + 1 >= len(arguments):
                raise ValueError(
                    "local Python --check-hash-based-pycs requires an operand"
                )
            index += 2
            continue
        if argument.startswith("--check-hash-based-pycs="):
            index += 1
            continue
        if argument.startswith("--"):
            index += 1
            continue
        if argument.startswith("-"):
            options = argument[1:]
            option_index = 0
            consumed_following_value = False
            while option_index < len(options):
                option = options[option_index]
                attached_value = options[option_index + 1 :]
                if option in {"c", "m"}:
                    operand = (
                        attached_value
                        if attached_value
                        else (
                            arguments[index + 1]
                            if index + 1 < len(arguments)
                            else None
                        )
                    )
                    if operand is None:
                        raise ValueError(
                            f"local Python -{option} launch requires an operand"
                        )
                    return ("command" if option == "c" else "module", operand)
                if option in {"W", "X"}:
                    consumed_following_value = not attached_value
                    if consumed_following_value and index + 1 >= len(arguments):
                        raise ValueError(
                            f"local Python -{option} option requires an operand"
                        )
                    break
                if option not in simple_options:
                    break
                option_index += 1
            index += 2 if consumed_following_value else 1
            continue
        return ("script", argument)
    return None


def node_launch_operand(
    command: str,
    arguments: list[str],
) -> tuple[str, str | None] | None:
    """Return Node's launch mode and its first program operand."""
    if not is_node_command(command):
        return None
    options_with_values = {
        "-C",
        "--build-snapshot-config",
        "--conditions",
        "--env-file",
        "--env-file-if-exists",
        "--experimental-config-file",
        "--experimental-loader",
        "--experimental-sea-config",
        "--icu-data-dir",
        "--import",
        "--loader",
        "--openssl-config",
        "-r",
        "--require",
        "--snapshot-blob",
        "--test-global-setup",
        "--watch-path",
    }
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            if index + 1 >= len(arguments):
                return None
            operand = arguments[index + 1]
            return ("stdin", None) if operand == "-" else ("script", operand)
        if argument == "-":
            return ("stdin", None)
        if argument in {"-c", "--check"}:
            raise ValueError(
                "local Node syntax-check mode cannot serve an MCP server"
            )
        if argument.startswith("--run="):
            script_name = argument.removeprefix("--run=")
            if not script_name:
                raise ValueError("local Node --run option requires an operand")
            return ("package-script", script_name)
        if argument in {"-e", "--eval", "-p", "--print"}:
            if index + 1 >= len(arguments):
                raise ValueError(f"local Node {argument} option requires an operand")
            return ("command", arguments[index + 1])
        if (
            (argument.startswith(("-e", "-p")) and len(argument) > 2)
            or argument.startswith(("--eval=", "--print="))
        ):
            return ("command", argument)
        if argument in options_with_values:
            if index + 1 >= len(arguments):
                raise ValueError(f"local Node {argument} option requires an operand")
            index += 2
            continue
        if argument.startswith("-"):
            index += 1
            continue
        return ("script", argument)
    return None


def node_runtime_dependency_operands(
    command: str,
    arguments: list[str],
) -> list[tuple[str, bool, bool]]:
    """Return Node file operands, CommonJS mode, and whether each is required."""
    if not is_node_command(command):
        return []
    module_dependency_options = {
        "--experimental-loader",
        "--import",
        "--loader",
        "--require",
        "-r",
    }
    required_file_options = {
        "--build-snapshot-config",
        "--env-file",
        "--experimental-config-file",
        "--experimental-sea-config",
        "--icu-data-dir",
        "--openssl-config",
        "--snapshot-blob",
        "--test-global-setup",
        "--watch-path",
    }
    optional_file_options = {"--env-file-if-exists"}
    dependency_options = (
        module_dependency_options | required_file_options | optional_file_options
    )
    operands: list[tuple[str, bool, bool]] = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument in {"--", "-", "-e", "--eval", "-p", "--print"}:
            break
        if (
            (argument.startswith(("-e", "-p")) and len(argument) > 2)
            or argument.startswith(("--eval=", "--print="))
        ):
            break
        if argument in dependency_options:
            if index + 1 >= len(arguments):
                raise ValueError(f"local Node {argument} option requires an operand")
            operands.append(
                (
                    arguments[index + 1],
                    argument in {"--require", "-r"},
                    argument not in optional_file_options,
                )
            )
            index += 2
            continue
        matched_attached = False
        for option in dependency_options - {"-r"}:
            prefix = f"{option}="
            if argument.startswith(prefix):
                operand = argument[len(prefix) :]
                if not operand:
                    raise ValueError(
                        f"local Node {option} option requires an operand"
                    )
                operands.append(
                    (
                        operand,
                        option == "--require",
                        option not in optional_file_options,
                    )
                )
                matched_attached = True
                break
        if matched_attached:
            index += 1
            continue
        if argument.startswith("-r") and len(argument) > 2:
            operand = argument[2:].removeprefix("=")
            if not operand:
                raise ValueError("local Node -r option requires an operand")
            operands.append((operand, True, True))
            index += 1
            continue
        if not argument.startswith("-"):
            break
        index += 1
    return operands


def node_package_script(
    root: Path,
    cwd: Path,
    script_name: str,
) -> tuple[Path, list[str]]:
    """Return the nearest package manifest and tokens for a Node package script."""
    resolved_root = root.resolve()
    directory = cwd
    while directory.is_relative_to(resolved_root):
        package_path = directory / "package.json"
        if package_path.is_file():
            try:
                package = json.loads(package_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise ValueError(
                    f"local Node package manifest is invalid: {package_path.relative_to(resolved_root)}"
                ) from error
            if not isinstance(package, dict):
                raise ValueError("local Node package manifest must contain an object")
            scripts = package.get("scripts")
            if not isinstance(scripts, dict):
                raise ValueError("local Node package manifest must contain scripts")
            script = scripts.get(script_name)
            if not isinstance(script, str) or not script.strip():
                raise ValueError(
                    f"local Node package script does not exist: {script_name}"
                )
            try:
                tokens = shlex.split(script)
            except ValueError as error:
                raise ValueError(
                    f"local Node package script is invalid: {script_name}"
                ) from error
            if not tokens:
                raise ValueError(
                    f"local Node package script is empty: {script_name}"
                )
            return package_path, tokens
        if directory == resolved_root:
            break
        directory = directory.parent
    raise ValueError(
        f"local Node --run package manifest does not exist from: {cwd.relative_to(resolved_root)}"
    )


def add_parent_package_initializers(
    root: Path,
    cwd: Path,
    selected: set[Path],
    dependency: Path,
) -> None:
    resolved_root = root.resolve()
    for parent in dependency.parents:
        if parent == cwd or not parent.is_relative_to(cwd):
            break
        initializer = parent / "__init__.py"
        if initializer.is_file():
            selected.add(initializer.relative_to(resolved_root))


def add_python_module_dependencies(
    root: Path,
    cwd: Path,
    selected: set[Path],
    command: str,
    arguments: list[str],
) -> None:
    """Include bundled modules launched through a Python ``-m`` operand."""
    launch = python_launch_operand(command, arguments)
    if launch is None or launch[0] != "module" or launch[1] is None:
        return
    resolved_root = root.resolve()
    module = launch[1]
    parts = module.split(".")
    if not parts or not all(part.isidentifier() for part in parts):
        return
    module_path = cwd.joinpath(*parts)
    module_file = module_path.with_suffix(".py").resolve()
    package_directory = module_path.resolve()
    if (
        not module_file.is_relative_to(resolved_root)
        or not package_directory.is_relative_to(resolved_root)
    ):
        raise ValueError(f"local Python module escapes plugin root: {module}")
    if module_file.is_file():
        selected.add(module_file.relative_to(resolved_root))
        add_parent_package_initializers(root, cwd, selected, module_file)
    elif package_directory.is_dir():
        selected.update(
            path.relative_to(resolved_root)
            for path in package_directory.rglob("*")
            if path.is_file()
        )
        add_parent_package_initializers(root, cwd, selected, package_directory)


def add_launch_dependencies(
    root: Path,
    cwd: Path,
    selected: set[Path],
    command: str,
    arguments: list[str],
) -> None:
    """Include file dependencies referenced by one local launch command."""
    resolved_root = root.resolve()
    python_launch = python_launch_operand(command, arguments)
    node_launch = node_launch_operand(command, arguments)
    required_launch_script = None
    for launch in (python_launch, node_launch):
        if launch is not None and launch[0] == "script":
            required_launch_script = launch[1]
            break
    node_dependencies = node_runtime_dependency_operands(command, arguments)
    commonjs_preloads = {
        operand
        for operand, uses_commonjs_resolution, _ in node_dependencies
        if uses_commonjs_resolution
    }
    required_node_dependencies = {
        operand for operand, _, required in node_dependencies if required
    }
    optional_node_dependencies = {
        operand for operand, _, required in node_dependencies if not required
    }
    dependency_arguments = list(arguments)
    dependency_arguments.extend(operand for operand, _, _ in node_dependencies)
    for argument in dependency_arguments:
        is_explicit_path = (
            argument.startswith(("./", "../"))
            and (
                argument not in optional_node_dependencies
                or argument in required_node_dependencies
            )
        ) or argument == required_launch_script
        if is_absolute_path(argument):
            raise ValueError(
                f"absolute local MCP dependency is not portable: {argument}"
            )
        source = (cwd / argument).resolve()
        if not source.is_relative_to(resolved_root):
            raise ValueError(f"local MCP dependency escapes plugin root: {argument}")
        if not source.exists() and argument in commonjs_preloads:
            source = next(
                (
                    candidate
                    for suffix in (".js", ".json", ".node")
                    if (candidate := Path(f"{source}{suffix}")).is_file()
                ),
                source,
            )
        if source.is_file():
            selected.add(source.relative_to(resolved_root))
        elif source.is_dir():
            selected.update(
                path.relative_to(resolved_root)
                for path in source.rglob("*")
                if path.is_file()
            )
        elif is_explicit_path:
            raise ValueError(f"local MCP dependency does not exist: {argument}")
    add_python_module_dependencies(root, cwd, selected, command, arguments)


def add_local_mcp_dependencies(
    root: Path,
    selected: set[Path],
    declaration: str | dict[str, object],
    executable_commands: set[Path] | None = None,
) -> None:
    """Include local command arguments referenced by a declared MCP config."""
    if isinstance(declaration, str):
        config_path = safe_relative_path(declaration)
        config = json.loads((root / config_path).read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("local MCP config must contain an object")
        servers = config.get("mcpServers", {})
    else:
        servers = declaration
    resolved_root = root.resolve()
    if not isinstance(servers, dict):
        raise ValueError("mcpServers config must contain an object")
    for server in servers.values():
        if not isinstance(server, dict):
            raise ValueError("each local MCP server config must contain an object")
        if "url" in server:
            url = server["url"]
            if not isinstance(url, str) or not url.strip():
                raise ValueError("remote MCP server url must be a non-empty string")
            if any(
                character.isspace()
                or ord(character) < 32
                or ord(character) == 127
                for character in url
            ):
                raise ValueError(f"remote MCP server url is invalid: {url}")
            try:
                parsed_url = urlparse(url)
                port = parsed_url.port
            except ValueError as error:
                raise ValueError(f"remote MCP server url is invalid: {url}") from error
            if (
                parsed_url.scheme not in {"http", "https"}
                or not parsed_url.netloc
                or not parsed_url.hostname
                or any(
                    character.isspace()
                    or ord(character) < 32
                    or ord(character) == 127
                    for character in parsed_url.netloc
                )
                or parsed_url.username is not None
                or parsed_url.password is not None
                or (port is not None and not 1 <= port <= 65535)
            ):
                raise ValueError(f"remote MCP server url is invalid: {url}")
            if any(field in server for field in ("command", "args", "cwd")):
                raise ValueError(
                    "remote MCP server config cannot contain local command fields"
                )
            continue
        cwd_value = server.get("cwd", ".")
        if not isinstance(cwd_value, str):
            raise ValueError("local MCP server cwd must be a string")
        cwd_relative = safe_relative_path(cwd_value)
        cwd = (root / cwd_relative).resolve()
        if not cwd.is_relative_to(resolved_root):
            raise ValueError(f"local MCP server cwd escapes plugin root: {cwd_value}")
        if not cwd.is_dir():
            raise ValueError(f"local MCP server cwd does not exist: {cwd_value}")
        command = server.get("command")
        if not isinstance(command, str) or not command.strip():
            raise ValueError("local MCP server command must be a non-empty string")
        if is_absolute_path(command):
            raise ValueError(f"absolute local MCP command is not portable: {command}")
        command_source = (cwd / command).resolve()
        if not command_source.is_relative_to(resolved_root):
            raise ValueError(f"local MCP command escapes plugin root: {command}")
        command_is_explicit_path = command.startswith(("./", "../")) or any(
            separator in command for separator in ("/", "\\")
        )
        if command_source.is_file():
            relative_command = command_source.relative_to(resolved_root)
            selected.add(relative_command)
            if command_is_explicit_path and executable_commands is not None:
                executable_commands.add(relative_command)
        elif command_is_explicit_path:
            raise ValueError(f"local MCP command does not exist: {command}")
        arguments = server.get("args", [])
        if not isinstance(arguments, list):
            raise ValueError("local MCP server args must be an array")
        if not all(isinstance(argument, str) for argument in arguments):
            raise ValueError("local MCP server args must contain only strings")
        python_launch = python_launch_operand(command, arguments)
        node_launch = node_launch_operand(command, arguments)
        if is_python_command(command) and (
            python_launch is None or python_launch[0] == "stdin"
        ):
            raise ValueError(
                "local Python MCP launch requires a script, module, or command"
            )
        if is_node_command(command) and (
            node_launch is None or node_launch[0] == "stdin"
        ):
            raise ValueError(
                "local Node MCP launch requires a script or command"
            )
        add_launch_dependencies(root, cwd, selected, command, arguments)
        if node_launch is not None and node_launch[0] == "package-script":
            script_name = node_launch[1]
            if script_name is None:
                raise ValueError("local Node --run option requires an operand")
            package_path, script_tokens = node_package_script(
                root,
                cwd,
                script_name,
            )
            selected.add(package_path.relative_to(resolved_root))
            script_cwd = package_path.parent
            script_command = script_tokens[0]
            script_arguments = script_tokens[1:]
            script_python_launch = python_launch_operand(
                script_command,
                script_arguments,
            )
            script_node_launch = node_launch_operand(
                script_command,
                script_arguments,
            )
            if is_python_command(script_command) and (
                script_python_launch is None or script_python_launch[0] == "stdin"
            ):
                raise ValueError(
                    "local Node package script must launch a serving command"
                )
            if is_node_command(script_command) and (
                script_node_launch is None or script_node_launch[0] == "stdin"
            ):
                raise ValueError(
                    "local Node package script must launch a serving command"
                )
            if not is_python_command(script_command) and not is_node_command(
                script_command
            ):
                script_command_source = (script_cwd / script_command).resolve()
                script_command_is_explicit = script_command.startswith(
                    ("./", "../")
                ) or any(separator in script_command for separator in ("/", "\\"))
                if (
                    not script_command_is_explicit
                    or not script_command_source.is_relative_to(resolved_root)
                    or not script_command_source.is_file()
                ):
                    raise ValueError(
                        "local Node package script must launch a contained executable, Python, or Node command"
                    )
                relative_script_command = script_command_source.relative_to(
                    resolved_root
                )
                selected.add(relative_script_command)
                if executable_commands is not None:
                    executable_commands.add(relative_script_command)
            add_launch_dependencies(
                root,
                script_cwd,
                selected,
                script_command,
                script_arguments,
            )


def select_paths(
    root: Path,
    executable_commands: set[Path] | None = None,
) -> set[Path]:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected = {Path(".codex-plugin/plugin.json")}
    selected.update(path for path in map(Path, OPTIONAL_ROOT_FILES) if (root / path).is_file())

    for field in COMPONENT_FIELDS:
        value = manifest.get(field)
        if isinstance(value, str):
            add_declared_path(root, selected, value)
            if field == "mcpServers":
                add_local_mcp_dependencies(
                    root,
                    selected,
                    value,
                    executable_commands,
                )
        elif field == "mcpServers" and isinstance(value, dict):
            add_local_mcp_dependencies(
                root,
                selected,
                value,
                executable_commands,
            )

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
    plugin_name = manifest["name"]
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
    executable_commands: set[Path] | None = None,
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
            if path.stat().st_mode & 0o111 and (
                executable_commands is None or relative not in executable_commands
            ):
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
    executable_commands: set[Path] | None = None,
) -> list[str]:
    actual_files, actual_directories, errors = inventory_tree(
        root,
        "plugin package boundary",
        "BOUNDARY",
        forbidden_parts,
        executable_commands,
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
    executable_commands: set[Path] | None = None,
) -> list[str]:
    errors, skill_count, _ = validate(destination, "source")
    if skill_count < 1:
        errors.append("runtime closure must contain at least one skill")
    expected_skill_count = 13 if plugin_name == "project-delivery" else None
    if expected_skill_count is not None and skill_count != expected_skill_count:
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
        executable_commands,
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
    executable_commands: set[Path] = set()
    try:
        plugin_name = read_plugin_name(root)
        selected = sorted(select_paths(root, executable_commands))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [str(error)], [], ""

    forbidden_parts = forbidden_distribution_parts(plugin_name)
    errors.extend(
        validate_source_boundary(
            root,
            selected,
            forbidden_parts,
            executable_commands,
        )
    )
    if errors:
        return errors, selected, ""
    copy_selected(root, destination, selected)
    errors.extend(
        validate_distribution_tree(
            destination,
            selected,
            plugin_name,
            forbidden_parts,
            executable_commands,
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

    executable_commands: set[Path] = set()
    try:
        selected = sorted(select_paths(output, executable_commands))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [f"refusing to replace output with invalid package boundary: {error}"]

    boundary_errors = validate_source_boundary(
        output,
        selected,
        forbidden_distribution_parts(plugin_name),
        executable_commands,
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
        KeyError,
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
        KeyError,
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
    manifest = json.loads(
        (root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    plugin_name = manifest["name"]
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
