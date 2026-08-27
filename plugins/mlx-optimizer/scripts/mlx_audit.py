#!/usr/bin/env python3
"""Static MLX Python audit tool.

The scanner reports candidate findings only. It never edits target code.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import time
import tokenize
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
}


@dataclass
class Finding:
    category: str
    severity: str
    file: str
    line: int
    evidence: str
    candidate_impact: str
    recommendation: str
    confidence: str


class Progress:
    def __init__(self, total: int) -> None:
        self.total = max(total, 1)
        self.start = time.monotonic()

    def update(self, count: int, label: str) -> None:
        elapsed = max(time.monotonic() - self.start, 0.001)
        rate = count / elapsed
        remaining = max(self.total - count, 0)
        eta = remaining / rate if rate else 0.0
        print(
            f"Scanning {count}/{self.total} files | ETA {eta:0.1f}s | {label}",
            file=sys.stderr,
        )


def iter_python_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".py":
        return [root]
    files: list[Path] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def is_mlx_import(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(alias.name == "mlx" or alias.name.startswith("mlx.") for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        return bool(node.module and (node.module == "mlx" or node.module.startswith("mlx.")))
    return False


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Attribute):
        parts = [func.attr]
        value = func.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if isinstance(value, ast.Name):
            parts.append(value.id)
        return ".".join(reversed(parts))
    if isinstance(func, ast.Name):
        return func.id
    return ""


class FileAnalyzer(ast.NodeVisitor):
    def __init__(self, path: Path, source: str, repo_root: Path) -> None:
        self.path = path
        self.source = source
        self.repo_root = repo_root
        self.findings: list[Finding] = []
        self.loop_depth = 0
        self.has_mlx_import = False
        self.has_timing_call = False
        self.has_eval_call = False
        self.function_stack: list[dict[str, ast.AST | bool]] = []
        self.timed_functions_without_eval: list[ast.AST] = []
        self.mlx_core_aliases: set[str] = set()
        self.mlx_eval_aliases: set[str] = set()

    @property
    def display_path(self) -> str:
        return display_path(self.path, self.repo_root)

    def add(self, category: str, severity: str, node: ast.AST, evidence: str, impact: str, recommendation: str, confidence: str) -> None:
        self.findings.append(
            Finding(
                category=category,
                severity=severity,
                file=self.display_path,
                line=getattr(node, "lineno", 1),
                evidence=evidence,
                candidate_impact=impact,
                recommendation=recommendation,
                confidence=confidence,
            )
        )

    def visit_Import(self, node: ast.Import) -> None:
        if is_mlx_import(node):
            self.has_mlx_import = True
        for alias in node.names:
            if alias.name == "mlx.core":
                self.mlx_core_aliases.add(alias.asname or "mlx.core")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if is_mlx_import(node):
            self.has_mlx_import = True
        if node.module == "mlx":
            for alias in node.names:
                if alias.name == "core":
                    self.mlx_core_aliases.add(alias.asname or alias.name)
        if node.module == "mlx.core":
            for alias in node.names:
                if alias.name == "eval":
                    self.mlx_eval_aliases.add(alias.asname or alias.name)
        self.generic_visit(node)

    def is_mlx_eval_call(self, name: str) -> bool:
        if name in self.mlx_eval_aliases:
            return True
        return any(name == f"{alias}.eval" for alias in self.mlx_core_aliases)

    def visit_For(self, node: ast.For) -> None:
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        state: dict[str, ast.AST | bool] = {"node": node, "has_timing_call": False, "has_eval_call": False}
        self.function_stack.append(state)
        self.generic_visit(node)
        self.function_stack.pop()
        if state["has_timing_call"] and not state["has_eval_call"]:
            self.timed_functions_without_eval.append(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = call_name(node)
        if name.endswith("perf_counter") or name.endswith("timeit"):
            self.has_timing_call = True
            if self.function_stack:
                self.function_stack[-1]["has_timing_call"] = True
        if self.is_mlx_eval_call(name):
            self.has_eval_call = True
            if self.function_stack:
                self.function_stack[-1]["has_eval_call"] = True
            if self.loop_depth:
                self.add(
                    "eval-in-loop",
                    "medium",
                    node,
                    name,
                    "Repeated evaluation can serialize work and reduce MLX scheduling benefits.",
                    "Measure whether this evaluation boundary is needed on every iteration.",
                    "medium",
                )
        if self.loop_depth and any(name.endswith(suffix) for suffix in (".item", ".tolist", ".numpy")):
            self.add(
                "sync-in-loop",
                "high",
                node,
                name,
                "Scalar or host conversion inside a loop can force synchronization.",
                "Move scalar extraction to a lower-frequency logging path and benchmark before/after.",
                "high",
            )
        self.generic_visit(node)

    def finalize(self) -> None:
        if self.has_mlx_import:
            for node in self.timed_functions_without_eval:
                self.add(
                    "benchmark-missing-eval",
                    "medium",
                    node,
                    "timing call without mx.eval in function",
                    "Benchmark may time scheduled work instead of completed MLX work.",
                    "Force completion before stopping timers and record the synchronization boundary.",
                    "medium",
                )

def analyze_file(path: Path, root: Path) -> tuple[bool, list[Finding]]:
    with tokenize.open(path) as handle:
        source = handle.read()
    tree = ast.parse(source, filename=str(path))
    analyzer = FileAnalyzer(path, source, root)
    analyzer.visit(tree)
    analyzer.finalize()
    return analyzer.has_mlx_import, analyzer.findings


def render_markdown(payload: dict) -> str:
    lines = [
        "# MLX Audit Report",
        "",
        "## Summary",
        "",
        f"- Target: `{payload['target']}`",
        f"- Files scanned: {payload['summary']['files_scanned']}",
        f"- Files with MLX imports: {payload['summary']['mlx_files']}",
        f"- Findings: {payload['summary']['finding_count']}",
        "",
        "## Findings",
        "",
    ]
    if not payload["findings"]:
        lines.append("No MLX candidate findings detected.")
    for finding in payload["findings"]:
        lines.extend(
            [
                f"### {finding['severity'].upper()} {finding['category']}",
                "",
                f"- File: `{finding['file']}:{finding['line']}`",
                f"- Evidence: `{finding['evidence']}`",
                f"- Candidate impact: {finding['candidate_impact']}",
                f"- Recommendation: {finding['recommendation']}",
                f"- Confidence: {finding['confidence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Verification",
            "",
            "Run representative benchmarks with warmup, explicit completion, memory telemetry, and correctness checks.",
            "",
            "## Residual Risks",
            "",
            "Static scanning can miss dynamic MLX behavior and can report false positives. Verify against the live workload.",
            "",
        ]
    )
    return "\n".join(lines)


def build_payload(target: Path) -> dict:
    root = target.resolve()
    scan_root = root if root.is_dir() else root.parent
    files = iter_python_files(root)
    progress = Progress(len(files))
    findings: list[Finding] = []
    mlx_files = 0
    for index, path in enumerate(files, start=1):
        progress.update(index, str(path))
        try:
            has_mlx, file_findings = analyze_file(path, scan_root)
        except SyntaxError as exc:
            findings.append(
                Finding(
                    category="syntax-error",
                    severity="low",
                    file=display_path(path, scan_root),
                    line=exc.lineno or 1,
                    evidence=str(exc),
                    candidate_impact="File could not be scanned.",
                    recommendation="Fix syntax before relying on static audit output.",
                    confidence="high",
                )
            )
            continue
        except (OSError, UnicodeError, LookupError) as exc:
            findings.append(
                Finding(
                    category="read-error",
                    severity="low",
                    file=display_path(path, scan_root),
                    line=1,
                    evidence=f"{type(exc).__name__}: {exc}",
                    candidate_impact="File could not be read or decoded.",
                    recommendation="Check file permissions and Python source encoding before relying on audit output.",
                    confidence="high",
                )
            )
            continue
        if has_mlx:
            mlx_files += 1
            findings.extend(file_findings)
    return {
        "target": str(root),
        "summary": {
            "files_scanned": len(files),
            "mlx_files": mlx_files,
            "finding_count": len(findings),
        },
        "findings": [asdict(finding) for finding in findings],
    }


def write_output(payload: dict, output_format: str, output: Path | None) -> None:
    if output_format == "json":
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    else:
        text = render_markdown(payload)
    if output:
        output.write_text(text, encoding="utf-8")
    else:
        print(text)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Python MLX repos for candidate performance findings.")
    parser.add_argument("target", type=Path, help="Repo, directory, or Python file to scan.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Output file. Defaults to stdout.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if not args.target.exists():
        print(f"Target does not exist: {args.target}", file=sys.stderr)
        return 2
    payload = build_payload(args.target)
    write_output(payload, args.format, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
