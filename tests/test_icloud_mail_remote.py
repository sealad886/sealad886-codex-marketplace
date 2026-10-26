"""Remote trust boundaries use synthetic keys/accounts; never access live mail."""
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

try:
    import jwt
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.asymmetric import rsa
    from starlette.testclient import TestClient
    import anyio
    import mcp
except ImportError:
    if os.environ.get("ICLOUD_REMOTE_TESTS_REQUIRED") == "1":
        raise
    jwt = None


@unittest.skipIf(jwt is None, "Install the optional pinned remote requirements to test HTTP/OIDC")
class RemoteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("icloud_mail_remote_tests", Path(__file__).parents[1] / "plugins/icloud-mail/mcp/remote.py")
        cls.remote = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.remote
        spec.loader.exec_module(cls.remote)
        cls.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.data = root / "data"
        self.data.mkdir(mode=0o700)
        keys = root / "keys"
        keys.mkdir(mode=0o700)
        self.key_file = keys / "fernet"
        self.key_file.write_bytes(Fernet.generate_key())
        self.key_file.chmod(0o600)
        self.settings = self.remote.Settings("https://issuer.example", "mail-api", "https://issuer.example/jwks",
            "https://mail.example/mcp", self.data / "mail.sqlite", self.key_file)
        self.store = self.remote.Store(self.settings.database, self.key_file)
        self.service = self.remote.Service(self.store)
        self.verifier = self.remote.Verifier(self.settings)
        patcher = mock.patch.object(self.verifier.jwks, "get_signing_key_from_jwt", return_value=mock.Mock(key=self.key.public_key()))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.token = self.verifier.decode(self.jwt())
        self.owner = self.remote.principal(self.token, self.remote.READ)
        self.seed(self.owner, "one@icloud.com")

    def jwt(self, **overrides):
        claims = {"iss": self.settings.issuer, "aud": self.settings.audience, "sub": "user-one",
            "iat": int(time.time()) - 1, "exp": int(time.time()) + 300,
            "scope": "mail:read mail:configure mail:attachments mail:watch"}
        claims.update(overrides)
        return jwt.encode(claims, self.key, algorithm="RS256", headers={"typ": "at+jwt"})

    def seed(self, owner, address):
        self.store.put(owner, "account", {"config": {**self.remote.core._default_config(), "account_address": address},
            "password": "fake-app-password", "generation": "generation-one"})

    def client(self, token=None):
        client = TestClient(self.remote.create_app(self.settings, store=self.store, verifier=self.verifier),
            base_url="https://mail.example", headers={"Authorization": "Bearer " + (token or self.jwt())},
            raise_server_exceptions=True)
        return client

    def rpc(self, client, method, params=None):
        return client.post("/mcp", headers={"Accept": "application/json, text/event-stream"},
            json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}})

    def test_access_token_claims_and_signature_fail_closed(self):
        for changes in ({"iss": "https://other.example"}, {"aud": "other"}, {"exp": time.time() - 1},
                {"nbf": time.time() + 100}, {"iat": time.time() + 100}, {"sub": ""}, {"scope": []}):
            with self.subTest(changes=changes):
                self.assertIsNone(self.verifier.decode(self.jwt(**changes)))
        claims = jwt.decode(self.jwt(), options={"verify_signature": False})
        for field in ("exp", "iat", "sub", "aud", "iss"):
            incomplete = {k: v for k, v in claims.items() if k != field}
            self.assertIsNone(self.verifier.decode(jwt.encode(incomplete, self.key, algorithm="RS256", headers={"typ": "at+jwt"})))
        self.assertIsNone(self.verifier.decode(jwt.encode(claims, self.key, algorithm="RS256")))
        self.assertIsNone(self.verifier.decode(jwt.encode(claims, "fake-symmetric-key-for-tests-only", algorithm="HS256", headers={"typ": "at+jwt"})))
        other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.assertIsNone(self.verifier.decode(jwt.encode(claims, other, algorithm="RS256", headers={"typ": "at+jwt"})))

    def test_no_credentials_or_plaintext_mail_metadata_in_database(self):
        content = self.settings.database.read_bytes()
        self.assertNotIn(b"fake-app-password", content)
        self.assertNotIn(b"one@icloud.com", content)
        self.assertEqual(self.settings.database.stat().st_mode & 0o777, 0o600)
        self.key_file.chmod(0o644)
        with self.assertRaises(ValueError):
            self.remote.Store(self.data / "other.sqlite", self.key_file)

    def test_swapped_rows_and_cross_tenant_cursors_rejected(self):
        second = self.verifier.decode(self.jwt(sub="user-two"))
        second_owner = self.remote.principal(second, self.remote.READ)
        self.seed(second_owner, "two@icloud.com")
        encrypted = self.store.wrap(self.owner, "generation-one", "icloud-mail:fake")
        for owner, generation, cursor in ((second_owner, "generation-one", encrypted),
                (self.owner, "new-generation", encrypted), (self.owner, "generation-one", encrypted[:-5] + "AAAAA")):
            with self.assertRaises(self.remote.RemoteError):
                self.store.unwrap(owner, generation, cursor)
        with self.store.connection() as db:
            db.execute("UPDATE records SET payload=(SELECT payload FROM records WHERE principal=? AND kind='account') WHERE principal=?", (self.owner, second_owner))
        with self.assertRaises(self.remote.RemoteError):
            self.store.get(second_owner, "account")

    def test_discovery_and_execution_enforce_scope(self):
        token = self.verifier.decode(self.jwt(scope="mail:read"))
        names = {tool.name for tool in self.service.tools(token)}
        self.assertIn("search_emails", names)
        self.assertFalse(names & {"read_attachment", "send_email", "configure_account", "poll_watch"})
        for name in ("send_email", "configure_account", "read_attachment", "poll_watch"):
            with self.assertRaises(self.remote.RemoteError):
                self.service.call(token, name, {})
        with self.assertRaises(self.remote.RemoteError):
            self.service.call(token, "read_email", {"message_id": "x", "include_raw_mime": True})

    def test_local_credentials_never_used_and_threads_are_isolated(self):
        second = self.verifier.decode(self.jwt(sub="user-two"))
        second_owner = self.remote.principal(second, self.remote.READ)
        self.seed(second_owner, "two@icloud.com")
        def read(args):
            time.sleep(0.01)
            return {"address": self.remote.core._username(), "source": self.remote.core._password(self.remote.core._username())[1]}
        with mock.patch.dict(self.remote.core.HANDLERS, {"search_emails": read}), mock.patch.object(self.remote.core, "_keychain", side_effect=AssertionError("Keychain touched")):
            with concurrent.futures.ThreadPoolExecutor(2) as pool:
                results = list(pool.map(lambda token: self.service.call(token, "search_emails", {}), (self.token, second)))
        self.assertEqual([r["address"] for r in results], ["one@icloud.com", "two@icloud.com"])
        self.assertTrue(all(r["source"] == "account session" for r in results))
        self.assertIsNone(self.remote.core._ACCOUNT_SESSION.get())

    def test_interrupted_onboarding_preserves_previous_connection(self):
        before = self.store.get(self.owner, "account")
        with mock.patch.object(self.remote.core, "_imap", side_effect=RuntimeError("fake-app-password")):
            with self.assertRaises(RuntimeError):
                self.service.onboard(self.owner, {"account_address": "one@icloud.com", "app_password": "replacement-fake"})
        self.assertEqual(before, self.store.get(self.owner, "account"))
        with mock.patch.object(self.remote.core, "_imap", return_value=mock.MagicMock()):
            self.service.onboard(self.owner, {"account_address": "one@icloud.com", "app_password": "replacement-fake"})
        self.assertNotEqual(before["generation"], self.store.get(self.owner, "account")["generation"])

    def test_revoke_removes_account_watch_state_and_prevents_reads(self):
        self.store.put(self.owner, "watch:test", {"pending": "fake"})
        self.store.revoke(self.owner)
        self.assertIsNone(self.store.get(self.owner, "account"))
        self.assertIsNone(self.store.get(self.owner, "watch:test"))
        with self.assertRaises(self.remote.RemoteError):
            self.service.call(self.token, "search_emails", {})

    def test_http_authentication_metadata_and_boundaries(self):
        with self.client() as client:
            metadata = client.get("/.well-known/oauth-protected-resource/mcp")
            self.assertEqual(metadata.status_code, 200)
            self.assertEqual(metadata.json()["resource"], self.settings.resource)
            self.assertEqual(set(metadata.json()["scopes_supported"]), {"mail:read", "mail:watch", "mail:attachments", "mail:configure"})
            for headers in ({"Authorization": "Bearer invalid"}, {"Authorization": ""}):
                self.assertEqual(client.post("/mcp", headers=headers).status_code, 401)
            self.assertEqual(client.get("/account", headers={"Host": "evil.example"}).status_code, 400)
            self.assertEqual(client.put("/account", headers={"Origin": "https://evil.example"}, json={}).status_code, 400)
            self.assertEqual(client.put("/account?token=not-a-real-secret", json={}).status_code, 400)
            listed = self.rpc(client, "tools/list")
            self.assertEqual(listed.status_code, 200, listed.text)
            self.assertIn("search_emails", [t["name"] for t in listed.json()["result"]["tools"]])
            self.assertEqual(listed.headers["cache-control"], "no-store")

    def test_http_setup_scope_size_errors_and_secret_redaction(self):
        with self.client(self.jwt(scope="mail:read")) as client:
            self.assertEqual(client.put("/account", json={}).status_code, 403)
        with self.client() as client:
            self.assertEqual(client.put("/account", content="x" * 4097).status_code, 413)
            with mock.patch.object(self.remote.core, "_imap", side_effect=RuntimeError("fake-private-password")):
                response = client.put("/account", json={"account_address": "one@icloud.com", "app_password": "fake-private-password"})
            self.assertEqual(response.status_code, 400)
            self.assertNotIn("fake-private-password", response.text)
            with mock.patch.dict(self.remote.core.HANDLERS, {"search_emails": mock.Mock(side_effect=RuntimeError("fake-private-password"))}):
                result = self.rpc(client, "tools/call", {"name": "search_emails", "arguments": {}})
            self.assertTrue(result.json()["result"]["isError"])
            self.assertNotIn("fake-private-password", result.text)
            self.assertEqual(client.delete("/account").status_code, 200)
            self.assertIsNone(self.store.get(self.owner, "account"))

    def page(self, emails, more=False):
        return {"emails": emails, "truncated": False, "has_more": more, "next_page_token": "core-page" if more else None}

    def message(self, uid, internet="<same@example.invalid>"):
        return {"id": self.remote.core._encode_ref("INBOX", 1, uid), "internet_message_id": internet, "subject": "fake-private-subject"}

    def test_watch_durable_scan_delivery_progress_and_dedup_are_separate(self):
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([self.message(2)], True)):
            first = self.service.call(self.token, "poll_watch", {"watch": "requested"})
        receipt = first["deliveries"][0]["delivery_id"]
        state = self.store.get(self.owner, "watch:requested")
        self.assertEqual(state["page"], "core-page")
        self.assertEqual(state["completed"], {})
        self.assertNotIn("fake-private-subject", json.dumps(state))
        # Recreate service: pending survives a crash and is returned before new scan.
        self.service = self.remote.Service(self.store)
        with mock.patch.object(self.remote.core, "_imap", return_value=mock.MagicMock()), mock.patch.object(self.remote.core, "_select", return_value=1), mock.patch.object(self.remote.core, "_fetch_summary", return_value=self.message(2)), mock.patch.object(self.remote.core, "search_emails") as search:
            retry = self.service.call(self.token, "poll_watch", {"watch": "requested"})
        search.assert_not_called()
        self.assertEqual(retry["deliveries"][0]["delivery_id"], receipt)
        with self.assertRaises(self.remote.RemoteError):
            self.service.call(self.token, "acknowledge_watch", {"watch": "requested", "delivery_ids": ["forged"]})
        self.service.call(self.token, "acknowledge_watch", {"watch": "requested", "delivery_ids": [receipt]})
        # A lost acknowledgement response can be retried without changing state.
        self.service.call(self.token, "acknowledge_watch", {"watch": "requested", "delivery_ids": [receipt]})
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([self.message(99)])) as search:
            duplicate = self.service.call(self.token, "poll_watch", {"watch": "requested"})
        self.assertEqual(search.call_args.args[0]["page_token"], "core-page")
        self.assertEqual(duplicate["deliveries"], [])

    def test_no_alert_outcome_advances_filtered_watch_without_claiming_delivery(self):
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([self.message(1)], True)):
            page = self.service.call(self.token, "poll_watch", {"watch": "filtered"})
        receipt = page["deliveries"][0]["delivery_id"]
        self.service.call(self.token, "acknowledge_watch", {"watch": "filtered", "delivery_ids": [receipt], "outcome": "no_alert"})
        state = self.store.get(self.owner, "watch:filtered")
        self.assertEqual(next(iter(state["completed"].values()))["outcome"], "no_alert")
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([self.message(2, "<match@example.invalid>")])):
            following = self.service.call(self.token, "poll_watch", {"watch": "filtered"})
        self.assertEqual(len(following["deliveries"]), 1)
        with self.assertRaises(self.remote.RemoteError):
            self.service.call(self.token, "acknowledge_watch", {"watch": "filtered", "delivery_ids": [receipt], "outcome": "delivered"})

    def test_pending_watch_transient_failures_do_not_become_missing_mail(self):
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([self.message(1)])):
            self.service.call(self.token, "poll_watch", {"watch": "requested"})
        before = self.store.get(self.owner, "watch:requested")
        for failure in (self.remote.core.OperationTimeout("timeout"), self.remote.core.MailError("IMAP transient failure")):
            with mock.patch.object(self.remote.core, "_imap", return_value=mock.MagicMock()), mock.patch.object(self.remote.core, "_select", return_value=1), mock.patch.object(self.remote.core, "_fetch_summary", side_effect=failure):
                with self.assertRaises(self.remote.core.MailError):
                    self.service.call(self.token, "poll_watch", {"watch": "requested"})
            self.assertEqual(self.store.get(self.owner, "watch:requested"), before)
        with mock.patch.object(self.remote.core, "_imap", return_value=mock.MagicMock()), mock.patch.object(self.remote.core, "_select", return_value=1), mock.patch.object(self.remote.core, "_fetch_summary", side_effect=self.remote.core.MailError("Message no longer exists in this mailbox")):
            missing = self.service.call(self.token, "poll_watch", {"watch": "requested"})
        self.assertTrue(missing["deliveries"][0]["email"]["unavailable"])

    def test_pending_watch_imap_no_response_is_retryable_using_real_summary_parser(self):
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([self.message(1)])):
            self.service.call(self.token, "poll_watch", {"watch": "requested"})
        before = self.store.get(self.owner, "watch:requested")
        imap = mock.MagicMock()
        imap.__enter__.return_value = imap
        imap.uid.return_value = ("NO", [b"synthetic temporary failure"])
        with mock.patch.object(self.remote.core, "_imap", return_value=imap), mock.patch.object(self.remote.core, "_select", return_value=1):
            with self.assertRaises(self.remote.core.MailError):
                self.service.call(self.token, "poll_watch", {"watch": "requested"})
        self.assertEqual(self.store.get(self.owner, "watch:requested"), before)

    def test_second_service_process_is_rejected_and_identifiers_expire(self):
        with self.assertRaises(ValueError):
            self.remote.Store(self.settings.database, self.key_file)
        cursor = self.store.wrap(self.owner, "generation-one", "core-page")
        with mock.patch("time.time", return_value=time.time() + 3601):
            with self.assertRaises(self.remote.RemoteError):
                self.store.unwrap(self.owner, "generation-one", cursor)

    def test_http_success_uses_principal_account_and_fixed_apple_destination(self):
        with self.client() as client, mock.patch.dict(self.remote.core.HANDLERS, {
            "search_emails": lambda _: {"address": self.remote.core._username()}
        }):
            result = self.rpc(client, "tools/call", {"name": "search_emails", "arguments": {}})
        self.assertEqual(json.loads(result.json()["result"]["content"][0]["text"])["address"], "one@icloud.com")
        fake = mock.MagicMock()
        fake.login.return_value = ("OK", [])
        with mock.patch.object(self.remote.core.imaplib, "IMAP4_SSL", return_value=fake) as connect:
            self.service.configure(self.token, {"account_address": "one@icloud.com", "app_password": "fake-app-password"})
        self.assertEqual(connect.call_args.args[:2], ("imap.mail.me.com", 993))
        with self.assertRaises(self.remote.RemoteError):
            self.service.configure(self.token, {"account_address": "one@icloud.com", "app_password": "fake", "host": "evil.example"})

    def test_revocation_serializes_with_active_read_then_blocks_new_reads(self):
        started, finish = threading.Event(), threading.Event()
        def read(args):
            started.set()
            self.assertTrue(finish.wait(2))
            return {"read": True}
        with mock.patch.dict(self.remote.core.HANDLERS, {"search_emails": read}), concurrent.futures.ThreadPoolExecutor(2) as pool:
            active = pool.submit(self.service.call, self.token, "search_emails", {})
            self.assertTrue(started.wait(1))
            revoke = pool.submit(self.service.disconnect, self.token)
            finish.set()
            self.assertEqual(active.result()["read"], True)
            revoke.result()
        with self.assertRaises(self.remote.RemoteError):
            self.service.call(self.token, "search_emails", {})

    def test_device_onboarding_cli_handles_pending_slowdown_without_printing_tokens(self):
        spec = importlib.util.spec_from_file_location("icloud_remote_cli_tests", Path(__file__).parents[1] / "plugins/icloud-mail/mcp/connect_remote.py")
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        def response(payload):
            result = mock.Mock()
            result.json.return_value = payload
            result.raise_for_status.return_value = result
            result.is_success = "access_token" in payload
            return result
        client = mock.Mock()
        client.get.return_value = response({"issuer": self.settings.issuer, "device_authorization_endpoint": "https://issuer.example/device", "token_endpoint": "https://issuer.example/token"})
        client.post.side_effect = [response({"verification_uri": "https://issuer.example/activate", "user_code": "FAKE-CODE", "device_code": "fake-private-device", "expires_in": 600}),
            response({"error": "authorization_pending"}), response({"error": "slow_down"}),
            response({"access_token": "fake-private-access", "token_type": "Bearer"})]
        with mock.patch.object(cli.time, "sleep"), mock.patch.object(cli.webbrowser, "open"), mock.patch("builtins.print") as output:
            token = cli.authorize(client, self.settings.issuer, "public-client-id", self.settings.resource)
        self.assertEqual(token, "fake-private-access")
        self.assertNotIn("fake-private", str(output.call_args_list))
        self.assertEqual(client.post.call_args.kwargs["data"]["resource"], self.settings.resource)

    def test_watch_uidvalidity_restart_and_truncation_do_not_lose_progress(self):
        with mock.patch.object(self.remote.core, "search_emails", return_value=self.page([], True)):
            self.service.call(self.token, "poll_watch", {"watch": "requested"})
        with mock.patch.object(self.remote.core, "search_emails", side_effect=[ValueError("stale token"), self.page([self.message(1)])]) as search:
            result = self.service.call(self.token, "poll_watch", {"watch": "requested"})
        self.assertEqual(len(result["deliveries"]), 1)
        self.assertNotIn("page_token", search.call_args.args[0])
        before = self.store.get(self.owner, "watch:other")
        with mock.patch.object(self.remote.core, "search_emails", return_value={**self.page([]), "truncated": True}):
            with self.assertRaises(self.remote.RemoteError):
                self.service.call(self.token, "poll_watch", {"watch": "other"})
        self.assertEqual(self.store.get(self.owner, "watch:other"), before)

    def test_remote_paging_identifiers_are_opaque_bound_and_round_trip(self):
        with mock.patch.dict(self.remote.core.HANDLERS, {"search_emails": lambda _: self.page([self.message(1)], True)}):
            result = self.service.call(self.token, "search_emails", {})
        opaque = result["emails"][0]["id"]
        self.assertNotEqual(opaque, self.message(1)["id"])
        with mock.patch.dict(self.remote.core.HANDLERS, {"read_email": lambda args: args}):
            read = self.service.call(self.token, "read_email", {"message_id": opaque})
        self.assertEqual(self.store.unwrap(self.owner, "generation-one", read["message_id"]), self.message(1)["id"])


if __name__ == "__main__":
    unittest.main()
