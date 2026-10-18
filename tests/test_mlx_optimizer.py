import json
import os
import platform
import runpy
import struct
import subprocess
import sys
import tempfile
import types
import unittest
import venv
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_audit.py"
ENV_PROBE = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_env_probe.py"
MLX_FIXTURE = ROOT / "tests" / "fixtures" / "mlx_optimizer" / "mlx_project"
PLAIN_FIXTURE = ROOT / "tests" / "fixtures" / "mlx_optimizer" / "plain_project"
PLUGIN_ROOT = ROOT / "plugins" / "mlx-optimizer"


class MlxBrandAssetTests(unittest.TestCase):
    def test_manifest_brand_assets_exist_and_are_valid_png(self):
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        interface = manifest["interface"]

        expected_dimensions = {"composerIcon": (256, 256), "logo": (1024, 1024)}
        for field, dimensions in expected_dimensions.items():
            relative_path = interface[field]
            self.assertTrue(relative_path.startswith("./assets/"))
            asset = (PLUGIN_ROOT / relative_path).resolve()
            self.assertTrue(asset.is_relative_to((PLUGIN_ROOT / "assets").resolve()))
            self.assertTrue(asset.is_file(), f"missing {field}: {asset}")
            payload = asset.read_bytes()
            self.assertGreaterEqual(len(payload), 33, f"truncated PNG header: {asset}")
            self.assertEqual(payload[8:16], b"\x00\x00\x00\x0dIHDR")
            self.assertEqual(payload[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", payload[16:24]), dimensions)


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

    def run_audit_stdout_json(self, target, timeout=10):
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
            timeout=timeout,
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

    def test_audit_rejects_symlink_sources_and_linked_ancestors(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp).resolve()
            outside = fixture / "outside"
            outside.mkdir()
            source = outside / "source.py"
            source.write_text("import mlx.core as mx\n", encoding="utf-8")
            project = fixture / "project"
            project.mkdir()
            linked_file = project / "linked.py"
            linked_file.symlink_to(source)
            linked_dir = fixture / "linked-dir"
            linked_dir.symlink_to(outside, target_is_directory=True)

            for target in (linked_file, project, linked_dir):
                with self.subTest(target=target):
                    payload = self.run_audit_stdout_json(target)

                    self.assertEqual(payload["summary"]["mlx_files"], 0)
                    self.assertEqual([item["category"] for item in payload["findings"]], ["read-error"])

            module = runpy.run_path(str(AUDIT))
            with self.assertRaises(OSError):
                module["analyze_file"](linked_dir / "source.py", fixture)

    def test_audit_rejects_oversized_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp).resolve() / "large.py"
            target.write_bytes(b"#" + b" " * (2 * 1024 * 1024))

            payload = self.run_audit_stdout_json(target)

        self.assertEqual([item["category"] for item in payload["findings"]], ["read-error"])

    def test_audit_accepts_source_at_byte_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp).resolve() / "at-limit.py"
            target.write_bytes(b"#" + b" " * (2 * 1024 * 1024 - 1))

            payload = self.run_audit_stdout_json(target)

        self.assertEqual(payload["summary"]["files_scanned"], 1)
        self.assertEqual(payload["findings"], [])

    @unittest.skipUnless(Path("/dev/zero").exists(), "requires /dev/zero")
    def test_audit_rejects_device_symlink_and_continues_scanning(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            (project / "device.py").symlink_to("/dev/zero")
            (project / "valid.py").write_text("import mlx.core as mx\n", encoding="utf-8")

            payload = self.run_audit_stdout_json(project, timeout=2)

        self.assertEqual(payload["summary"]["files_scanned"], 2)
        self.assertEqual(payload["summary"]["mlx_files"], 1)
        self.assertEqual([item["category"] for item in payload["findings"]], ["read-error"])

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO requires POSIX")
    def test_audit_rejects_fifo_without_waiting_for_a_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            os.mkfifo(project / "blocked.py")

            payload = self.run_audit_stdout_json(project, timeout=1)

        self.assertEqual([item["category"] for item in payload["findings"]], ["read-error"])

    def test_audit_accepts_utf8_bom_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp).resolve() / "bom.py"
            target.write_bytes(b"\xef\xbb\xbfimport mlx.core as mx\n")

            payload = self.run_audit_stdout_json(target)

        self.assertEqual(payload["summary"]["mlx_files"], 1)
        self.assertEqual(payload["findings"], [])

    @unittest.skipUnless(os.name == "posix", "requires POSIX descriptor limits")
    def test_audit_closes_nonregular_source_descriptors(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            for index in range(40):
                (project / f"directory-{index:02}.py").mkdir()
            (project / "z-valid.py").write_text("import mlx.core as mx\n", encoding="utf-8")
            driver = (
                "import resource, runpy, sys; "
                "resource.setrlimit(resource.RLIMIT_NOFILE, (32, resource.getrlimit(resource.RLIMIT_NOFILE)[1])); "
                f"sys.argv = [{str(AUDIT)!r}, {str(project)!r}, '--format', 'json']; "
                f"runpy.run_path({str(AUDIT)!r}, run_name='__main__')"
            )

            result = subprocess.run(
                [sys.executable, "-I", "-c", driver],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=10,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["mlx_files"], 1)
        self.assertEqual(len(payload["findings"]), 40)
        self.assertNotIn("Too many open files", result.stdout)

    def test_audit_writes_json_to_stdout_without_output(self):
        payload = self.run_audit_stdout_json(PLAIN_FIXTURE)

        self.assertEqual(payload["summary"]["files_scanned"], 1)
        self.assertEqual(payload["findings"], [])


class MlxEnvProbeTests(unittest.TestCase):
    def test_env_probe_ignores_working_directory_and_pythonpath_modules(self):
        for injection in ("cwd", "pythonpath"):
            with self.subTest(injection=injection), tempfile.TemporaryDirectory() as tmp:
                fixture = Path(tmp)
                hostile = fixture / "hostile"
                hostile.mkdir()
                marker = fixture / "unexpected-import"
                poison = f"from pathlib import Path\nPath({str(marker)!r}).touch()\nraise RuntimeError('untrusted import')\n"
                (hostile / "json.py").write_text(poison, encoding="utf-8")
                (hostile / "runpy.py").write_text(poison, encoding="utf-8")
                mlx = hostile / "mlx"
                mlx.mkdir()
                (mlx / "__init__.py").write_text(poison, encoding="utf-8")
                env = os.environ.copy()
                env["PYTHONPATH"] = str(hostile) if injection == "pythonpath" else ""
                driver = (
                    "import json, pathlib, runpy, sys; "
                    f"module = runpy.run_path({str(ENV_PROBE)!r}); "
                    "print(json.dumps(module['run_child'](pathlib.Path(sys.executable))))"
                )

                result = subprocess.run(
                    [sys.executable, "-I", "-c", driver],
                    cwd=hostile if injection == "cwd" else fixture,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    timeout=15,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(marker.exists(), "probe imported attacker-controlled Python")
                self.assertEqual(json.loads(result.stdout)["status"], "ok")

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
            cwd=ROOT,
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
        with tempfile.TemporaryDirectory() as tmp:
            venv_root = Path(tmp).resolve() / ".venv"
            venv.create(venv_root, with_pip=False, symlinks=True)
            venv_python = venv_root / "bin" / "python"
            # Isolation must retain the selected environment's installed packages.
            site_packages = Path(subprocess.check_output(
                [str(venv_python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
                text=True,
            ).strip())
            fake_mlx = site_packages / "mlx"
            fake_mlx.mkdir()
            (fake_mlx / "__init__.py").write_text("", encoding="utf-8")
            (fake_mlx / "core.py").write_text(
                "__version__ = 'trusted-fixture'\n"
                "def device_info(): return {'device_name': 'venv-fixture'}\n",
                encoding="utf-8",
            )

            for selected in (str(venv_python), os.path.relpath(venv_python, ROOT)):
                with self.subTest(selected=selected):
                    payload = self.run_env_probe_json("--python", selected)

                    self.assertEqual(payload["status"], "ok")
                    self.assertEqual(payload["python"]["executable"], str(venv_python))
                    self.assertEqual(payload["python"]["prefix"], str(venv_root))
                    self.assertTrue(payload["mlx"]["available"])
                    self.assertEqual(payload["mlx"]["version"], "trusted-fixture")
                    self.assertEqual(payload["mlx"]["device_info"], {"device_name": "venv-fixture"})

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
        module = runpy.run_path(str(ENV_PROBE))
        fake_mlx = types.ModuleType("mlx")
        fake_core = types.ModuleType("mlx.core")
        fake_mlx.core = fake_core
        fake_core.__version__ = "fake-mlx"
        fake_core.device_info = lambda: {"device_name": "modern-api"}
        fake_core.metal = types.SimpleNamespace(
            is_available=lambda: True,
            device_info=mock.Mock(side_effect=RuntimeError("deprecated metal.device_info used")),
        )
        with mock.patch.dict(sys.modules, {"mlx": fake_mlx, "mlx.core": fake_core}):
            payload = module["child_probe"]()

        self.assertTrue(payload["mlx"]["available"])
        self.assertEqual(payload["mlx"]["device_info"], {"device_name": "modern-api"})
        self.assertNotIn("device_info_error", payload["mlx"])
        fake_core.metal.device_info.assert_not_called()


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
