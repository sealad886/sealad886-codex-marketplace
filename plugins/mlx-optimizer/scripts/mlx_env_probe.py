#!/usr/bin/env python3
"""Probe a repo-local Python/MLX environment without global installs."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def default_venv_python(target: Path) -> Path:
    return target / ".venv" / "bin" / "python"


def json_safe(value):
    try:
        json.dumps(value)
    except TypeError:
        return repr(value)
    return value


def probe_failed(
    python_executable: Path,
    recommended_action: str,
    *,
    error: str | None = None,
    stdout: str | None = None,
    stderr: str | None = None,
) -> dict:
    payload: dict = {
        "status": "probe-failed",
        "python": {"executable": str(python_executable)},
        "recommended_action": recommended_action,
    }
    if error:
        payload["error"] = error
    if stdout is not None:
        payload["stdout"] = stdout
    if stderr is not None:
        payload["stderr"] = stderr
    return payload


def child_probe() -> dict:
    payload: dict = {
        "python": {
            "executable": sys.executable,
            "prefix": sys.prefix,
            "base_prefix": sys.base_prefix,
            "version": sys.version.split()[0],
            "machine": platform.machine(),
            "platform": platform.platform(),
        },
        "mlx": {
            "available": False,
            "version": None,
            "metal_available": None,
            "device_info": None,
            "memory_api": {},
        },
    }
    try:
        import mlx.core as mx  # type: ignore
    except Exception as exc:
        payload["mlx"]["import_error"] = repr(exc)
        return payload

    payload["mlx"]["available"] = True
    payload["mlx"]["version"] = getattr(mx, "__version__", None)
    if payload["mlx"]["version"] is None:
        try:
            payload["mlx"]["version"] = importlib.metadata.version("mlx")
        except importlib.metadata.PackageNotFoundError:
            payload["mlx"]["version"] = None
        except Exception as exc:
            payload["mlx"]["version_error"] = repr(exc)
    metal = getattr(mx, "metal", None)
    if metal is not None:
        is_available = getattr(metal, "is_available", None)
        if callable(is_available):
            try:
                payload["mlx"]["metal_available"] = bool(is_available())
            except Exception as exc:
                payload["mlx"]["metal_available_error"] = repr(exc)
    device_info = getattr(mx, "device_info", None)
    if not callable(device_info) and metal is not None:
        device_info = getattr(metal, "device_info", None)
    if callable(device_info):
        try:
            payload["mlx"]["device_info"] = json_safe(device_info())
        except Exception as exc:
            payload["mlx"]["device_info_error"] = repr(exc)
    for name in (
        "get_active_memory",
        "get_peak_memory",
        "get_cache_memory",
        "set_memory_limit",
        "set_cache_limit",
        "set_wired_limit",
        "clear_cache",
    ):
        payload["mlx"]["memory_api"][name] = hasattr(mx, name)
    return payload


def run_child(python_executable: Path) -> dict:
    if not python_executable.exists():
        return probe_failed(
            python_executable,
            "Choose an existing Python executable, preferably inside the target repo .venv.",
            error="Python executable does not exist.",
        )
    if not os.access(python_executable, os.X_OK):
        return probe_failed(
            python_executable,
            "Choose an executable Python path, preferably inside the target repo .venv.",
            error="Python path exists but is not executable.",
        )
    code = (
        "import json, runpy; "
        f"module = runpy.run_path({str(Path(__file__).resolve())!r}); "
        "print(json.dumps(module['child_probe'](), sort_keys=True))"
    )
    try:
        result = subprocess.run(
            [str(python_executable), "-c", code],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        return probe_failed(
            python_executable,
            "Verify the repo-local Python executable can be launched by this process.",
            error=repr(exc),
        )
    if result.returncode != 0:
        return probe_failed(
            python_executable,
            "Verify the repo-local Python executable can run basic Python code.",
            stdout=result.stdout,
            stderr=result.stderr,
        )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return probe_failed(
            python_executable,
            "Verify the child probe emits valid JSON on stdout.",
            error=repr(exc),
            stdout=result.stdout,
            stderr=result.stderr,
        )
    if not isinstance(payload, dict) or not isinstance(payload.get("mlx"), dict):
        return probe_failed(
            python_executable,
            "Verify the child probe emits the expected JSON object on stdout.",
            stdout=result.stdout,
            stderr=result.stderr,
        )
    payload["status"] = "ok"
    if not payload["mlx"]["available"]:
        payload["recommended_action"] = "Install MLX only inside the target repo .venv if the project requires MLX."
    return payload


def render_markdown(payload: dict) -> str:
    lines = ["# MLX Environment Probe", ""]
    if "target" in payload:
        lines.append(f"- Target: `{payload['target']}`")
    lines.append(f"- Status: {payload['status']}")
    if "recommended_action" in payload:
        lines.append(f"- Recommended action: {payload['recommended_action']}")
    if "python" in payload:
        lines.append(f"- Python executable: `{payload['python'].get('executable')}`")
        lines.append(f"- Python prefix: `{payload['python'].get('prefix')}`")
        lines.append(f"- Python base prefix: `{payload['python'].get('base_prefix')}`")
        lines.append(f"- Python version: `{payload['python'].get('version')}`")
        lines.append(f"- Python machine: `{payload['python'].get('machine')}`")
        lines.append(f"- Python platform: `{payload['python'].get('platform')}`")
    if "mlx" in payload:
        lines.append(f"- MLX available: {payload['mlx'].get('available')}")
        lines.append(f"- MLX version: {payload['mlx'].get('version')}")
        if payload["mlx"].get("import_error") is not None:
            lines.append(f"- MLX import error: `{payload['mlx'].get('import_error')}`")
        lines.append(f"- Metal available: {payload['mlx'].get('metal_available')}")
        if payload["mlx"].get("metal_available_error") is not None:
            lines.append(f"- Metal availability error: `{payload['mlx'].get('metal_available_error')}`")
        lines.append(f"- Metal device info: `{payload['mlx'].get('device_info')}`")
        if payload["mlx"].get("device_info_error") is not None:
            lines.append(f"- Metal device info error: `{payload['mlx'].get('device_info_error')}`")
        memory_api = payload["mlx"].get("memory_api", {})
        if memory_api:
            lines.append("- Memory API availability:")
            for name in sorted(memory_api):
                lines.append(f"  - `{name}`: {memory_api[name]}")
    if "error" in payload:
        lines.append(f"- Error: `{payload['error']}`")
    if "stdout" in payload:
        lines.append("- Child stdout:")
        lines.append("```text")
        lines.append(payload["stdout"])
        lines.append("```")
    if "stderr" in payload:
        lines.append("- Child stderr:")
        lines.append("```text")
        lines.append(payload["stderr"])
        lines.append("```")
    return "\n".join(lines) + "\n"


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe a repo-local Python/MLX environment.")
    parser.add_argument("target", type=Path, help="Target repo path.")
    parser.add_argument("--python", type=Path, help="Explicit Python executable.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    target = args.target.resolve()
    python_executable = args.python if args.python else default_venv_python(target)
    if not args.python and not python_executable.exists():
        payload = {
            "status": "missing-venv",
            "target": str(target),
            "recommended_action": f"Create and use a repo-local virtual environment at {target / '.venv'}. Do not install Python packages globally.",
        }
    else:
        payload = run_child(python_executable)
        payload["target"] = str(target)
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
