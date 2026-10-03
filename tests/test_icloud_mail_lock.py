"""Account configuration transactions and private setup launch behavior."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from unittest import mock

SERVER = Path(__file__).parents[1] / "plugins/icloud-mail/mcp/server.py"
SPEC = importlib.util.spec_from_file_location("icloud_mail_lock_server", SERVER)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class AccountLockTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "config.json"
        patcher = mock.patch.dict(os.environ, {"ICLOUD_MAIL_CONFIG_PATH": str(self.path)}, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_nested_transaction_can_configure_and_detect_revision_change(self):
        with server.account_config_lock():
            before = server.account_config_revision()
            server.configure_account({"account_address": "one@icloud.com"})
            after = server.account_config_revision()
            self.assertNotEqual(before, after)
            self.assertEqual(after, server.account_config_revision())
            server.clear_account_configuration({"confirm": True})
            self.assertEqual(server.account_config_revision(), "missing")

    def test_lock_blocks_other_threads_and_releases_after_error(self):
        with ThreadPoolExecutor(max_workers=1) as pool:
            with self.assertRaises(ValueError):
                with server.account_config_lock():
                    def attempt():
                        with server.account_config_lock(timeout=0.05):
                            return True
                    with self.assertRaisesRegex(server.MailError, "in progress"):
                        pool.submit(attempt).result(timeout=2)
                    raise ValueError("interrupted")
            self.assertTrue(pool.submit(attempt).result(timeout=2))

    def test_external_process_lock_prevents_mutation(self):
        import fcntl
        # The external holder uses the same OS lock contract as another MCP process.
        lock_path = str(self.path) + ".lock"
        script = "import fcntl,sys; f=open(sys.argv[1],'a'); fcntl.flock(f,fcntl.LOCK_EX); print('ready',flush=True); sys.stdin.read()"
        child = subprocess.Popen([server.sys.executable, "-c", script, lock_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(), "ready")
            with self.assertRaisesRegex(server.MailError, "in progress"):
                with server.account_config_lock(timeout=0.05):
                    pass
        finally:
            child.communicate(input="", timeout=5)
        server.configure_account({"account_address": "one@icloud.com"})
        self.assertTrue(self.path.exists())

    def test_lock_and_revision_reject_symlinks(self):
        target = self.path.parent / "other"
        target.write_text("untouched")
        lock_path = Path(str(self.path) + ".lock")
        lock_path.symlink_to(target)
        with self.assertRaises(OSError):
            with server.account_config_lock():
                pass
        self.assertEqual(target.read_text(), "untouched")
        lock_path.unlink()
        self.path.symlink_to(target)
        with self.assertRaises(OSError):
            server.account_config_revision()


class SetupLaunchTests(unittest.TestCase):
    def test_launch_returns_no_private_url_or_password_and_sanitizes_environment(self):
        child = mock.Mock()
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "private-password"}
        ), mock.patch.object(server.subprocess, "Popen", return_value=child) as launch, mock.patch.object(
            server.select, "select", return_value=([child.stdout], [], [])
        ), mock.patch.object(server.os, "read", return_value=b"READY\n"), mock.patch.object(server.threading, "Thread"):
            result = server.open_account_setup({})
        self.assertNotIn("ICLOUD_MAIL_APP_PASSWORD", launch.call_args.kwargs["env"])
        self.assertNotIn("private-password", repr(result))
        self.assertNotIn("http", repr(result))
        self.assertFalse(result["connected"])
        child.stdout.close.assert_called_once()

    def test_dead_child_cleanup_preserves_safe_error(self):
        child = mock.Mock()
        child.poll.return_value = 1
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.object(
            server.subprocess, "Popen", return_value=child
        ), mock.patch.object(server.select, "select", return_value=([], [], [])), self.assertRaisesRegex(
            server.MailError, "Could not open"
        ):
            server.open_account_setup({})
        child.terminate.assert_not_called()
        child.wait.assert_called_once_with(timeout=2)
        child.stdout.close.assert_called_once()

    def test_child_exit_race_does_not_replace_safe_error(self):
        child = mock.Mock()
        child.poll.return_value = None
        child.terminate.side_effect = ProcessLookupError("private process details")
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.object(
            server.subprocess, "Popen", return_value=child
        ), mock.patch.object(server.select, "select", return_value=([], [], [])), self.assertRaises(server.MailError) as caught:
            server.open_account_setup({})
        self.assertNotIn("private process details", str(caught.exception))
        child.stdout.close.assert_called_once()
