"""Behavioral checks for the packaged watcher using local throwaway jobs."""

import json
import os
import shlex
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


WATCHER = (
    Path(__file__).resolve().parents[1]
    / "plugins/event-driven-job-watcher/skills/event-driven-job-watcher/scripts/watch.py"
)
THREAD = "00000000-0000-4000-8000-000000000001"


class WatcherTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.receipt = self.directory / "status.json"
        self.log = self.directory / "job.log"

    def command(self, *arguments):
        return [sys.executable, str(WATCHER), "--receipt", str(self.receipt), *arguments]

    def run_job(self, *child, options=()):
        return subprocess.run(
            self.command(*options, "run", "--log", str(self.log), "--", *child),
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def read_receipt(self):
        return json.loads(self.receipt.read_text(encoding="utf-8"))

    def test_records_success_and_passes_argv_without_shell_expansion(self):
        literal = "spaces; $VARIABLE"
        result = self.run_job(sys.executable, "-c", "import sys; print(sys.argv[1])", literal)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.read_receipt()
        self.assertEqual((receipt["status"], receipt["exit_code"]), ("completed", 0))
        self.assertNotIn("callback", receipt)
        self.assertEqual(self.log.read_text(encoding="utf-8"), literal + "\n")
        for path in (self.receipt, self.log):
            self.assertEqual(stat.S_IMODE(path.stat().st_mode) & 0o077, 0)

    def test_existing_receipt_prevents_a_duplicate_job(self):
        self.receipt.write_text("previous receipt", encoding="utf-8")
        result = self.run_job(sys.executable, "-c", "print('duplicate job')")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.receipt.read_text(encoding="utf-8"), "previous receipt")
        self.assertFalse(self.log.exists())

    def test_existing_log_is_preserved(self):
        self.log.write_text("previous job output", encoding="utf-8")
        result = self.run_job(sys.executable, "-c", "print('overwrite')")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.read_receipt()["status"], "needs_attention")
        self.assertEqual(self.log.read_text(encoding="utf-8"), "previous job output")

    def test_saves_child_failure_before_one_queue_attempt(self):
        fake_cli = self.directory / "fake-codex"
        fake_script = self.directory / "fake_codex.py"
        calls = self.directory / "callback.jsonl"
        fake_cli.write_text(
            f'#!/bin/sh\nexec {shlex.quote(sys.executable)} {shlex.quote(str(fake_script))} "$@"\n',
            encoding="utf-8",
        )
        fake_cli.chmod(0o700)

        for queue_code, queue_status in [(0, "queued"), (2, "uncertain")]:
            with self.subTest(queue_code=queue_code):
                self.receipt = self.directory / f"status-{queue_code}.json"
                self.log = self.directory / f"job-{queue_code}.log"
                fake_script.write_text(
                    "import json, pathlib, sys\n"
                    f"receipt = json.loads(pathlib.Path({str(self.receipt)!r}).read_text())\n"
                    f"with open({str(calls)!r}, 'a') as calls:\n"
                    "    calls.write(json.dumps([sys.argv[1:], receipt]) + '\\n')\n"
                    "print('synthetic resume warning', file=sys.stderr)\n"
                    f"sys.exit({queue_code})\n",
                    encoding="utf-8",
                )
                result = self.run_job(
                    sys.executable, "-c", "raise SystemExit(23)",
                    options=("--thread", THREAD, "--codex", str(fake_cli)),
                )
                self.assertNotEqual(result.returncode, 0)
                receipt = self.read_receipt()
                self.assertEqual((receipt["status"], receipt["exit_code"]), ("failed", 23))
                self.assertEqual(receipt["callback"], {"status": queue_status, "exit_code": queue_code})
                call, saved_receipt = json.loads(calls.read_text(encoding="utf-8"))
                self.assertEqual(call[:-1], ["queue", "--thread", THREAD, "--resume", "--message"])
                self.assertIn(str(self.receipt), call[-1])
                self.assertEqual(saved_receipt["exit_code"], 23)
                self.assertEqual(saved_receipt["callback"], {"status": "submitting"})
                self.assertEqual(result.stderr, "")
                calls.unlink()

    @unittest.skipUnless(sys.platform == "darwin", "macOS PID attachment")
    def test_macos_attachment_observes_exit_without_inventing_status(self):
        with subprocess.Popen(["/bin/cat"], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL) as child:
            try:
                try:
                    start = subprocess.check_output(
                        ["/bin/ps", "-p", str(child.pid), "-o", "lstart="],
                        env={**os.environ, "LC_ALL": "C"},
                        text=True,
                    ).strip()
                except PermissionError:
                    self.skipTest("process inspection is restricted by the host")
                command = self.command("attach", "--pid", str(child.pid), "--start", start)
                with subprocess.Popen(command, stderr=subprocess.PIPE, text=True) as watcher:
                    try:
                        deadline = time.monotonic() + 5
                        status = None
                        while time.monotonic() < deadline and watcher.poll() is None:
                            if self.receipt.is_file():
                                status = self.read_receipt()["status"]
                                if status == "watching":
                                    break
                            time.sleep(0.02)
                        self.assertEqual(status, "watching")
                        child.communicate(timeout=5)
                        _, error = watcher.communicate(timeout=5)
                        self.assertEqual(watcher.returncode, 0, error)
                    finally:
                        if watcher.poll() is None:
                            watcher.kill()
            finally:
                if child.poll() is None:
                    child.kill()
        receipt = self.read_receipt()
        self.assertEqual((receipt["status"], receipt["exit_code"]), ("exit_observed", None))
        self.assertFalse(self.log.exists())


if __name__ == "__main__":
    unittest.main()
