"""Connection page security and persistence contracts; never access real Keychain."""
import http.client
import importlib.util
import json
import os
import smtplib
import tempfile
from pathlib import Path
import sys
import threading
import time
import unittest
from unittest import mock

MCP = Path(__file__).parents[1] / "plugins/icloud-mail/mcp"
with mock.patch.dict(sys.modules):
    spec = importlib.util.spec_from_file_location("keychain", MCP / "keychain.py")
    keychain = importlib.util.module_from_spec(spec)
    sys.modules["keychain"] = keychain
    spec.loader.exec_module(keychain)
    spec = importlib.util.spec_from_file_location("mail_setup", MCP / "setup.py")
    setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup)
spec = importlib.util.spec_from_file_location("setup_core", MCP / "server.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

PASSWORD = "abcd-efgh-ijkl-mnop"
ACCOUNT = "example@icloud.com"


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        environment = mock.patch.dict(os.environ, {"ICLOUD_MAIL_CONFIG_PATH": str(Path(directory.name) / "config.json")})
        environment.start()
        self.addCleanup(environment.stop)

    def test_password_shape(self):
        self.assertEqual(setup.normalize_password("abcdefghijklmnop"), PASSWORD)
        self.assertEqual(setup.normalize_password("abcd efgh ijkl mnop"), PASSWORD)
        for value in ("normalPassword123!", "", None, "a" * 100, "abcd-efgh-ijkl-mno1"):
            with self.assertRaises(ValueError):
                setup.normalize_password(value)

    def test_validation_before_any_persistence(self):
        store = mock.Mock()
        with mock.patch.object(core, "_load_config", return_value={}), mock.patch.object(core, "validate_account", side_effect=RuntimeError(PASSWORD)), mock.patch.object(core, "_write_config") as write:
            with self.assertRaises(RuntimeError):
                setup.connect(core, store, ACCOUNT, PASSWORD)
            write.assert_not_called()
            store.set.assert_not_called()

    def test_config_failure_restores_previous_secret(self):
        for previous in (None, "previous-secret"):
            store = mock.Mock()
            store.get.return_value = previous
            with mock.patch.object(core, "_load_config", return_value={}), mock.patch.object(core, "validate_account"), mock.patch.object(core, "_write_config", side_effect=OSError()):
                with self.assertRaises(setup.SetupError) as failure:
                    setup.connect(core, store, ACCOUNT, PASSWORD)
            self.assertEqual(failure.exception.code, "config_failed")
            if previous is None:
                store.delete.assert_called_once_with(ACCOUNT)
            else:
                self.assertEqual(store.set.call_args.args, (ACCOUNT, previous))

    def test_same_account_preserves_aliases(self):
        old = core._default_config()
        old.update(account_address=ACCOUNT, default_from=ACCOUNT, allowed_from=["alias@icloud.com"], display_name="Example")
        with mock.patch.object(core, "_load_config", return_value=old), mock.patch.object(core, "validate_account"), mock.patch.object(core, "_write_config") as write:
            setup.connect(core, mock.Mock(), ACCOUNT, PASSWORD)
            self.assertEqual(write.call_args.args[0]["allowed_from"], old["allowed_from"])
            setup.connect(core, mock.Mock(), "different@icloud.com", PASSWORD)
            self.assertEqual(write.call_args.args[0]["allowed_from"], [])

    def test_stale_save_never_touches_keychain(self):
        store = mock.Mock()
        with mock.patch.object(core, "account_config_revision", side_effect=["old", "new"]), mock.patch.object(core, "_load_config", return_value={}), mock.patch.object(core, "validate_account"), mock.patch.object(core, "_write_config") as write:
            with self.assertRaises(setup.SetupError) as failure:
                setup.connect(core, store, ACCOUNT, PASSWORD)
        self.assertEqual(failure.exception.code, "stale_configuration")
        store.get.assert_not_called()
        store.set.assert_not_called()
        write.assert_not_called()

    def test_rollback_failure_requires_repair(self):
        for previous in (None, "previous-secret"):
            store = mock.Mock()
            store.get.return_value = previous
            if previous is None:
                store.delete.side_effect = RuntimeError(PASSWORD)
            else:
                store.set.side_effect = [None, RuntimeError(PASSWORD)]
            with mock.patch.object(core, "_load_config", return_value={}), mock.patch.object(core, "validate_account"), mock.patch.object(core, "_write_config", side_effect=OSError(PASSWORD)):
                with self.assertRaises(setup.SetupError) as failure:
                    setup.connect(core, store, ACCOUNT, PASSWORD)
            self.assertEqual(failure.exception.code, "repair_required")
            self.assertNotIn(PASSWORD, str(failure.exception))

    def test_network_keychain_and_auth_failures_are_distinct(self):
        for failure, expected in [(OSError(PASSWORD), "network_failed"), (RuntimeError(PASSWORD), "verification_failed"), (smtplib.SMTPAuthenticationError(535, PASSWORD.encode()), "verification_failed")]:
            with mock.patch.object(core, "_load_config", return_value={}), mock.patch.object(core, "validate_account", side_effect=failure):
                with self.assertRaises(setup.SetupError) as receipt:
                    setup.connect(core, mock.Mock(), ACCOUNT, PASSWORD)
            self.assertEqual(receipt.exception.code, expected)
            self.assertNotIn(PASSWORD, str(receipt.exception))
        store = mock.Mock()
        store.set.side_effect = RuntimeError(PASSWORD)
        with mock.patch.object(core, "_load_config", return_value={}), mock.patch.object(core, "validate_account"), mock.patch.object(core, "_write_config") as write:
            with self.assertRaises(setup.SetupError) as receipt:
                setup.connect(core, store, ACCOUNT, PASSWORD)
        self.assertEqual(receipt.exception.code, "keychain_failed")
        write.assert_not_called()


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.server = setup.SetupServer(core, mock.Mock(), lifetime=5)
        self.worker = threading.Thread(target=self.server.run)
        self.worker.start()

    def tearDown(self):
        self.server.deadline = 0
        self.worker.join(timeout=6)
        self.server.server_close()

    def request(self, method="POST", headers=None, data=None, path=None):
        body = json.dumps(data if data is not None else {"account": ACCOUNT, "password": PASSWORD})
        request_headers = {"Origin": self.server.origin, "Content-Type": "application/json", "X-Setup-Token": self.server.token}
        request_headers.update(headers or {})
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        try:
            conn.request(method, path or self.server.path, body=body if method == "POST" else None, headers=request_headers)
            response = conn.getresponse()
            return response.status, response.read().decode(), dict(response.getheaders())
        finally:
            conn.close()

    def test_page_contains_no_session_secret(self):
        status, body, headers = self.request("GET")
        self.assertEqual(status, 200)
        self.assertNotIn(self.server.token, body)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])

    def test_rejects_cross_origin_host_and_token(self):
        for headers in ({"Host": "attacker.example"}, {"Origin": "https://attacker.example"}, {"X-Setup-Token": "wrong"}, {"Content-Length": "999999"}):
            with mock.patch.object(setup, "connect") as connect:
                status, body, _ = self.request(headers=headers)
                self.assertIn(status, (403, 413))
                connect.assert_not_called()
                self.assertNotIn(PASSWORD, body)

    def test_rejects_normal_password_before_apple(self):
        with mock.patch.object(setup, "connect") as connect:
            self.assertEqual(self.request(data={"account": ACCOUNT, "password": "ApplePassword123!"})[0], 400)
            connect.assert_not_called()

    def test_error_does_not_echo_secret(self):
        with mock.patch.object(setup, "connect", side_effect=RuntimeError(PASSWORD)):
            status, body, _ = self.request()
            self.assertEqual(status, 400)
            self.assertNotIn(PASSWORD, body)

    def test_failure_receipt_code_preserves_repair_state(self):
        with mock.patch.object(setup, "connect", side_effect=setup.SetupError("repair_required")):
            status, body, _ = self.request()
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body)["code"], "repair_required")
        self.assertFalse(self.server.connected)

    def test_size_bounds_reject_before_validation(self):
        for size in ("0", "2049", "-1", "invalid"):
            with mock.patch.object(setup, "connect") as connect:
                self.assertEqual(self.request(headers={"Content-Length": size})[0], 413)
                connect.assert_not_called()

    def test_success_stops_server(self):
        with mock.patch.object(setup, "connect"):
            status, body, _ = self.request()
        self.assertEqual(status, 200)
        self.assertNotIn(PASSWORD, body)
        self.worker.join(timeout=2)
        self.assertFalse(self.worker.is_alive())

    def test_expiry_stops_server(self):
        self.server.deadline = time.monotonic() - 1
        self.worker.join(timeout=2)
        self.assertFalse(self.worker.is_alive())


if __name__ == "__main__":
    unittest.main()
