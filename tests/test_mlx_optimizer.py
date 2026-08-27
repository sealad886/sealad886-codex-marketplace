import json
import os
import platform
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_audit.py"
ENV_PROBE = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_env_probe.py"
MLX_FIXTURE = ROOT / "tests" / "fixtures" / "mlx_optimizer" / "mlx_project"
PLAIN_FIXTURE = ROOT / "tests" / "fixtures" / "mlx_optimizer" / "plain_project"
PLUGIN_ROOT = ROOT / "plugins" / "mlx-optimizer"


class MlxAuditTests(unittest.TestCase):
    def write_python(self, path, lines, encoding="utf-8"):
        path.write_text("\n".join(lines) + "\n", encoding=encoding)

    def run_audit_json(self, target):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "audit.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(AUDIT),
                    str(target),
                    "--format",
                    "json",
                    "--output",
                    str(output),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Scanning", result.stderr)
            return json.loads(output.read_text())

    def run_audit_stdout_json(self, target):
        result = subprocess.run(
            [
                sys.executable,
                str(AUDIT),
                str(target),
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Scanning", result.stderr)
        return json.loads(result.stdout)

    def test_audit_reports_sync_and_eval_findings(self):
        payload = self.run_audit_json(MLX_FIXTURE)
        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("sync-in-loop", categories)
        self.assertIn("eval-in-loop", categories)
        self.assertIn("benchmark-missing-eval", categories)

    def test_audit_plain_project_has_no_mlx_findings(self):
        payload = self.run_audit_json(PLAIN_FIXTURE)
        self.assertEqual(payload["summary"]["files_scanned"], 1)
        self.assertEqual(payload["findings"], [])

    def test_audit_reports_single_missing_eval_per_timed_function(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "bench.py"
            self.write_python(
                target,
                [
                    "import time",
                    "",
                    "import mlx.core as mx",
                    "",
                    "",
                    "def benchmark(batch):",
                    "    start = time.perf_counter()",
                    "    value = mx.sum(batch)",
                    "    end = time.perf_counter()",
                    "    return end - start, value",
                ],
            )

            payload = self.run_audit_json(target)

        findings = [
            finding
            for finding in payload["findings"]
            if finding["category"] == "benchmark-missing-eval"
        ]
        self.assertEqual(len(findings), 1)

    def test_audit_recognizes_full_mlx_core_eval_in_timed_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "full_import.py"
            self.write_python(
                target,
                [
                    "import time",
                    "",
                    "import mlx.core",
                    "",
                    "",
                    "def benchmark(batches):",
                    "    start = time.perf_counter()",
                    "    for batch in batches:",
                    "        loss = mlx.core.sum(batch)",
                    "        mlx.core.eval(loss)",
                    "    end = time.perf_counter()",
                    "    return end - start",
                ],
            )

            payload = self.run_audit_json(target)

        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("eval-in-loop", categories)
        self.assertNotIn("benchmark-missing-eval", categories)

    def test_audit_recognizes_imported_eval_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "alias_eval.py"
            self.write_python(
                target,
                [
                    "import mlx.core as mx",
                    "from mlx.core import eval as mlx_eval",
                    "",
                    "",
                    "def train_epoch(batches):",
                    "    for batch in batches:",
                    "        loss = mx.sum(batch)",
                    "        mlx_eval(loss)",
                ],
            )

            payload = self.run_audit_json(target)

        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("eval-in-loop", categories)

    def test_audit_reads_python_source_encoding_cookie(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "latin1_bench.py"
            self.write_python(
                target,
                [
                    "# -*- coding: latin-1 -*-",
                    "# cafe: café",
                    "import time",
                    "",
                    "import mlx.core as mx",
                    "",
                    "",
                    "def benchmark(batch):",
                    "    start = time.perf_counter()",
                    "    value = mx.sum(batch)",
                    "    end = time.perf_counter()",
                    "    return end - start, value",
                ],
                encoding="latin-1",
            )

            payload = self.run_audit_json(target)

        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("benchmark-missing-eval", categories)

    def test_audit_writes_json_to_stdout_without_output(self):
        payload = self.run_audit_stdout_json(PLAIN_FIXTURE)

        self.assertEqual(payload["summary"]["files_scanned"], 1)
        self.assertEqual(payload["findings"], [])


class MlxEnvProbeTests(unittest.TestCase):
    def run_env_probe_json(self, *args):
        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(PLAIN_FIXTURE),
                *args,
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_env_probe_reports_missing_venv(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(PLAIN_FIXTURE),
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "missing-venv")
        self.assertIn(".venv", payload["recommended_action"])

    def test_env_probe_uses_explicit_python(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(PLAIN_FIXTURE),
                "--python",
                sys.executable,
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(Path(payload["python"]["executable"]).resolve(), Path(sys.executable).resolve())

    def test_env_probe_preserves_explicit_venv_python_symlink(self):
        venv_python = ROOT / ".venv" / "bin" / "python"
        if not venv_python.exists():
            self.skipTest("repo-local .venv is required for symlink preservation check")

        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(ROOT),
                "--python",
                str(venv_python),
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["python"]["executable"], str(venv_python))
        self.assertEqual(payload["python"]["prefix"], str(ROOT / ".venv"))

    def test_env_probe_reports_invalid_explicit_python_as_probe_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing_python = Path(tmp) / "missing-python"

            payload = self.run_env_probe_json("--python", str(missing_python))

        self.assertEqual(payload["status"], "probe-failed")
        self.assertIn("recommended_action", payload)
        self.assertIn(str(missing_python), payload["python"]["executable"])

    def test_env_probe_reports_non_json_child_stdout_as_probe_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_python = Path(tmp) / "fake-python"
            fake_python.write_text("#!/bin/sh\nprintf 'not json\\n'\n", encoding="utf-8")
            fake_python.chmod(0o755)

            payload = self.run_env_probe_json("--python", str(fake_python))

        self.assertEqual(payload["status"], "probe-failed")
        self.assertEqual(payload["stdout"], "not json\n")
        self.assertIn("valid JSON", payload["recommended_action"])

    def test_env_probe_markdown_reports_python_and_mlx_evidence(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(PLAIN_FIXTURE),
                "--python",
                sys.executable,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"- Python version: `{sys.version.split()[0]}`", result.stdout)
        self.assertIn(f"- Python platform: `{platform.platform()}`", result.stdout)
        self.assertIn("- MLX available:", result.stdout)

    def test_env_probe_reports_mlx_import_status_without_host_assumptions(self):
        payload = self.run_env_probe_json("--python", sys.executable)

        self.assertIn("mlx", payload)
        self.assertIsInstance(payload["mlx"]["available"], bool)
        if not payload["mlx"]["available"]:
            self.assertIn("import_error", payload["mlx"])

    def test_env_probe_prefers_core_device_info(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_root = Path(tmp)
            fake_mlx = fake_root / "mlx"
            fake_mlx.mkdir()
            (fake_mlx / "__init__.py").write_text("", encoding="utf-8")
            (fake_mlx / "core.py").write_text(
                "\n".join(
                    [
                        "__version__ = 'fake-mlx'",
                        "",
                        "",
                        "def device_info():",
                        "    return {'device_name': 'modern-api'}",
                        "",
                        "",
                        "class metal:",
                        "    @staticmethod",
                        "    def is_available():",
                        "        return True",
                        "",
                        "    @staticmethod",
                        "    def device_info():",
                        "        raise RuntimeError('deprecated metal.device_info used')",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(fake_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ENV_PROBE),
                    str(PLAIN_FIXTURE),
                    "--python",
                    sys.executable,
                    "--format",
                    "json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                env=env,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["mlx"]["device_info"], {"device_name": "modern-api"})
        self.assertNotIn("device_info_error", payload["mlx"])


class MlxBenchmarkTemplateTests(unittest.TestCase):
    script = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_benchmark_template.py"
    no_mlx = ROOT / "tests" / "fixtures" / "mlx_optimizer" / "no_mlx"

    def run_template(self, *args, env=None):
        result = subprocess.run(
            [
                sys.executable,
                str(self.script),
                *args,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=env,
        )
        return result

    def test_benchmark_template_runs_without_mlx(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.no_mlx)
        result = self.run_template(
            "--runs",
            "2",
            "--warmup",
            "1",
            "--format",
            "json",
            env=env,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["runs"], 2)
        self.assertIn("median_seconds", payload)
        self.assertIn("Benchmark", result.stderr)

    def test_benchmark_template_rejects_invalid_numeric_args(self):
        cases = (
            ("--runs", "0"),
            ("--warmup", "-1"),
            ("--size", "-5"),
        )
        for option, value in cases:
            with self.subTest(option=option, value=value):
                result = self.run_template(option, value)

                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("Traceback", result.stdout)

    def test_benchmark_template_writes_json_to_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "benchmark.json"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.no_mlx)

            result = self.run_template(
                "--runs",
                "2",
                "--warmup",
                "0",
                "--format",
                "json",
                "--output",
                str(output),
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertIn("Benchmark", result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["runs"], 2)

    def test_benchmark_template_synchronizes_actual_workload_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_root = Path(tmp)
            fake_mlx = fake_root / "mlx"
            fake_mlx.mkdir()
            (fake_mlx / "__init__.py").write_text("", encoding="utf-8")
            (fake_mlx / "core.py").write_text(
                "\n".join(
                    [
                        "import os",
                        "from pathlib import Path",
                        "",
                        "LOG = Path(os.environ['FAKE_MLX_LOG'])",
                        "",
                        "",
                        "def _append(message):",
                        "    with LOG.open('a', encoding='utf-8') as handle:",
                        "        handle.write(message + '\\n')",
                        "",
                        "",
                        "def array(value):",
                        "    _append('array:' + repr(value))",
                        "    return ('array', value)",
                        "",
                        "",
                        "def eval(*args):",
                        "    _append('eval:' + repr(args))",
                        "",
                        "",
                        "def synchronize():",
                        "    _append('synchronize')",
                        "",
                        "",
                        "def get_active_memory():",
                        "    return 1",
                        "",
                        "",
                        "def get_peak_memory():",
                        "    return 2",
                        "",
                        "",
                        "def get_cache_memory():",
                        "    return 3",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            log = fake_root / "mlx.log"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(fake_root)
            env["FAKE_MLX_LOG"] = str(log)

            result = self.run_template(
                "--runs",
                "1",
                "--warmup",
                "0",
                "--size",
                "4",
                "--format",
                "json",
                env=env,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            records = log.read_text(encoding="utf-8").splitlines()
            self.assertIn("eval:(14,)", records)
            self.assertIn("synchronize", records)
            self.assertNotIn("array:[0]", records)
