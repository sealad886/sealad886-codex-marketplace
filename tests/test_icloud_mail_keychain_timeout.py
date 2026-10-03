"""Credential reads cannot leave the synchronous MCP transport blocked."""
from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest import mock

MCP = Path(__file__).parents[1] / "plugins/icloud-mail/mcp"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


keychain = load("timeout_keychain", MCP / "keychain.py")
server = load("timeout_server", MCP / "server.py")


class KeychainReadTests(unittest.TestCase):
    def test_real_blocked_helper_is_killed_and_reaped_then_next_read_completes(self):
        real_run = subprocess.run
        real_popen = subprocess.Popen
        children = []

        def start(*args, **kwargs):
            child = real_popen(*args, **kwargs)
            children.append(child)
            return child

        def blocked(_args, **kwargs):
            return real_run([sys.executable, "-c", "import time; time.sleep(60)"], **kwargs)

        reader = keychain.KeychainReader(timeout=0.15)
        started = time.monotonic()
        with mock.patch.object(keychain.subprocess, "run", side_effect=blocked), mock.patch.object(
            keychain.subprocess, "Popen", side_effect=start
        ), self.assertRaisesRegex(RuntimeError, "could not retrieve"):
            reader.get("example@icloud.com")
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(len(children), 1)
        self.assertIsNotNone(children[0].poll())
        with mock.patch.object(keychain.subprocess, "run", return_value=mock.Mock(returncode=0, stdout='"replacement"')):
            self.assertEqual(reader.get("example@icloud.com"), "replacement")

    def test_read_uses_private_pipes_and_strips_password_environment(self):
        with mock.patch.dict(os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "old-secret"}), mock.patch.object(
            keychain.subprocess, "run", return_value=mock.Mock(returncode=0, stdout='"stored-secret"')
        ) as run:
            self.assertEqual(keychain.KeychainReader(timeout=3).get("example@icloud.com"), "stored-secret")
        args, kwargs = run.call_args
        self.assertEqual(args[0][-1], "--read")
        self.assertNotIn("secret", repr(args))
        self.assertNotIn("ICLOUD_MAIL_APP_PASSWORD", kwargs["env"])
        self.assertEqual(kwargs["stdout"], subprocess.PIPE)
        self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 3)
        self.assertEqual(json.loads(kwargs["input"])["account"], "example@icloud.com")

    def test_child_protocol_calls_shared_native_reader(self):
        output = io.StringIO()
        with mock.patch.object(keychain.sys, "stdin", io.StringIO(json.dumps({"service": "test-service", "account": "example@icloud.com"}))), mock.patch.object(
            keychain.sys, "stdout", output
        ), mock.patch.object(keychain, "Keychain") as native:
            native.return_value.get.return_value = "private-password"
            self.assertEqual(keychain._read_main(), 0)
        native.assert_called_once_with("test-service")
        native.return_value.get.assert_called_once_with("example@icloud.com")
        self.assertEqual(json.loads(output.getvalue()), "private-password")

    def test_timeout_error_does_not_echo_captured_secret(self):
        with mock.patch.object(keychain.subprocess, "run", side_effect=subprocess.TimeoutExpired("helper", 1, output="private-password")), self.assertRaises(RuntimeError) as caught:
            keychain.KeychainReader().get("example@icloud.com")
        self.assertNotIn("private-password", str(caught.exception))

    def test_server_reader_respects_remaining_operation_deadline(self):
        deadline = mock.Mock()
        deadline.timeout.return_value = 0.2
        token = server._ACTIVE_DEADLINE.set(deadline)
        try:
            reader = server._keychain()
        finally:
            server._ACTIVE_DEADLINE.reset(token)
        deadline.timeout.assert_called_once_with(10.0)
        self.assertEqual(reader.timeout, 0.2)

    def test_failed_read_does_not_prevent_subsequent_mcp_request(self):
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.object(server, "_load_config", return_value={
            **server._default_config(), "account_address": "example@icloud.com"
        }), mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(server, "_keychain") as factory:
            factory.return_value.get.side_effect = RuntimeError("timed out")
            response = server.handle({"id": 1, "method": "tools/call", "params": {"name": "get_account_status", "arguments": {}}})
            status = json.loads(response["result"]["content"][0]["text"])
            self.assertFalse(status["credential_configured"])
            self.assertEqual(server.handle({"id": 2, "method": "ping"})["result"], {})
