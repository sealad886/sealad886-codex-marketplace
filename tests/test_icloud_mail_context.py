"""Candidate credentials stay isolated until setup explicitly persists them."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import importlib.util
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock

SERVER = Path(__file__).parents[1] / "plugins/icloud-mail/mcp/server.py"
SPEC = importlib.util.spec_from_file_location("icloud_mail_context_server", SERVER)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


def config(account: str) -> dict:
    return {**server._default_config(), "account_address": account, "default_from": account}


class AccountSessionTests(unittest.TestCase):
    def setUp(self):
        self.keychain = mock.Mock()
        self.keychain.get.return_value = None
        patcher = mock.patch.object(server, "_keychain", return_value=self.keychain)
        self.keychain_factory = patcher.start()
        self.addCleanup(patcher.stop)

    def test_saved_keychain_password_overrides_old_environment_on_macos(self):
        self.keychain.get.return_value = "new-keychain-password"
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "old-environment-password"}
        ):
            self.assertEqual(
                server._password("one@icloud.com"),
                ("new-keychain-password", "macOS Keychain"),
            )

    def test_unavailable_keychain_falls_back_to_environment(self):
        for outcome in (None, OSError("unavailable"), RuntimeError("denied")):
            with self.subTest(outcome=type(outcome).__name__), mock.patch.object(
                server.sys, "platform", "darwin"
            ), mock.patch.dict(os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "environment-password"}), mock.patch.object(
                self.keychain, "get", **(
                    {"side_effect": outcome} if isinstance(outcome, Exception)
                    else {"return_value": outcome}
                )
            ):
                self.assertEqual(server._password("one@icloud.com"), ("environment-password", "environment"))

    def test_non_macos_environment_lookup_does_not_query_keychain(self):
        with mock.patch.object(server.sys, "platform", "linux"), mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "environment-password"}
        ), mock.patch.object(server, "_keychain") as lookup:
            self.assertEqual(server._password("one@icloud.com"), ("environment-password", "environment"))
            lookup.assert_not_called()

    def test_candidate_context_overrides_keychain_and_environment(self):
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "environment-password"}
        ), mock.patch.object(server, "_keychain") as lookup, server.account_session(
            config("one@icloud.com"), "candidate-password"
        ):
            self.assertEqual(server._password("one@icloud.com"), ("candidate-password", "account session"))
            lookup.assert_not_called()

    def test_candidate_validation_does_not_persist_or_use_existing_credentials(self):
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(os.environ, {
            "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
            "ICLOUD_MAIL_APP_PASSWORD": "old-password",
        }, clear=True):
            server.configure_account({"account_address": "old@icloud.com"})
            before = Path(temporary, "config.json").read_bytes()
            imap = mock.MagicMock()
            imap.status.return_value = ("OK", [b"INBOX (MESSAGES 3)"])
            smtp = mock.MagicMock()
            with mock.patch.object(server.imaplib, "IMAP4_SSL", return_value=imap), mock.patch.object(
                server.smtplib, "SMTP", return_value=smtp
            ), mock.patch.object(server, "_keychain") as subprocess_run:
                with server.account_session(config("new@icloud.com"), "candidate-password"):
                    result = server.validate_account({})
                imap.login.assert_called_once_with("new", "candidate-password")
                smtp.login.assert_called_once_with("new@icloud.com", "candidate-password")
                smtp.send_message.assert_not_called()
                subprocess_run.assert_not_called()
            self.assertEqual(result["account_address"], "new@icloud.com")
            self.assertFalse(result["email_sent"])
            self.assertEqual(Path(temporary, "config.json").read_bytes(), before)
            self.assertEqual(server.get_account_status({})["account_address"], "old@icloud.com")
            self.assertEqual(os.environ["ICLOUD_MAIL_APP_PASSWORD"], "old-password")

    def test_nested_failure_restores_outer_account_and_then_persistent_account(self):
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(os.environ, {
            "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
            "ICLOUD_MAIL_USERNAME": "saved@icloud.com",
            "ICLOUD_MAIL_APP_PASSWORD": "saved-password",
        }, clear=True):
            with server.account_session(config("outer@icloud.com"), "outer-password"):
                with self.assertRaises(RuntimeError):
                    with server.account_session(config("inner@icloud.com"), "inner-password"):
                        raise RuntimeError("validation interrupted")
                self.assertEqual(server.get_account_status({})["account_address"], "outer@icloud.com")
                self.assertEqual(server._password("outer@icloud.com")[0], "outer-password")
            self.assertEqual(server.get_account_status({})["account_address"], "saved@icloud.com")
            self.assertEqual(server._password("saved@icloud.com")[0], "saved-password")

    def test_mismatched_identity_cannot_fall_back_to_environment_or_keychain(self):
        with mock.patch.dict(os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "fallback"}), mock.patch.object(
            server, "_keychain"
        ) as lookup, server.account_session(config("one@icloud.com"), "candidate"):
            with self.assertRaisesRegex(server.MailError, "does not match"):
                server._password("another@icloud.com")
            lookup.assert_not_called()

    def test_sessions_are_isolated_between_concurrent_threads(self):
        barrier = threading.Barrier(2)

        def observe(account):
            with server.account_session(config(account), account + "-password"):
                barrier.wait(timeout=5)
                return server.get_account_status({})["account_address"], server._password(account)[0]

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(observe, ("one@icloud.com", "two@icloud.com")))
        self.assertEqual(results, [(account, account + "-password") for account in ("one@icloud.com", "two@icloud.com")])

    def test_input_and_loaded_config_mutations_cannot_change_session_identity(self):
        candidate = config("one@icloud.com")
        candidate["allowed_from"] = ["alias@icloud.com"]
        with server.account_session(candidate, "candidate"):
            candidate["account_address"] = "changed@icloud.com"
            candidate["allowed_from"].clear()
            loaded = server._load_config()
            loaded["allowed_from"].clear()
            self.assertEqual(server.get_account_status({})["account_address"], "one@icloud.com")
            self.assertEqual(server.get_account_status({})["allowed_from"], ["alias@icloud.com"])

    def test_authentication_rejection_does_not_echo_server_supplied_secret(self):
        imap = mock.MagicMock()
        imap.login.side_effect = server.imaplib.IMAP4.error("candidate-password")
        with server.account_session(config("one@icloud.com"), "candidate-password"), mock.patch.object(
            server.imaplib, "IMAP4_SSL", return_value=imap
        ), self.assertRaises(server.MailError) as caught:
            server.validate_account({})
        self.assertNotIn("candidate-password", str(caught.exception))
        self.assertIn("authentication failed", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
