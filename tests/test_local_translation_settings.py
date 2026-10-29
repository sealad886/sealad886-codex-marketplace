"""Desktop setup behavior, using isolated user settings and a synthetic runner."""

from contextlib import contextmanager
import hashlib
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock


MCP = Path(__file__).resolve().parents[1] / "plugins/local-translation/mcp"


def module(name, filename):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, MCP / filename)
        value = importlib.util.module_from_spec(spec)
        sys.modules[name] = value
        spec.loader.exec_module(value)
    return sys.modules[name]


settings = module("_local_translation_settings", "settings.py")
setup = module("_local_translation_setup", "setup.py")
core = module("local_translation_settings_test_runtime", "server.py")


@contextmanager
def engine():
    state = {"requests": [], "model": "index-setup-test", "count": 12, "tokenizer_status": 200}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, value, status=200):
            body = json.dumps(value).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            state["requests"].append((self.path, None, self.headers.get("Authorization")))
            self.send({"data": [{"id": state["model"]}]})

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            state["requests"].append((self.path, body, self.headers.get("Authorization")))
            self.send({"count": state["count"]}, state["tokenizer_status"])
    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        state["url"] = "http://127.0.0.1:%d/v1" % server.server_port
        try:
            yield state
        finally:
            server.shutdown()
            thread.join()


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / "workspace"
        self.root.mkdir()
        self.environment = mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.directory / "config")})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def deployment(self, url="http://127.0.0.1:8080/v1"):
        return {"base_url": url, "model": "index-setup-test", "artifact_revision": "test-revision",
                "runner_version": "test-only", "locales": {"en-US": "English", "fr-FR": "French"}}

    def save(self, deployment=None, **kwargs):
        return settings.save_settings(str(self.root), deployment or self.deployment(),
                                      validate=core.validate_config, verify=kwargs.pop("verify", lambda *_: None), **kwargs)

    def test_persistent_settings_without_launch_environment_and_private_permissions(self):
        self.assertIsNone(settings.load_settings())
        self.assertFalse(settings.public_settings()["configured"])
        receipt = self.save(api_key_action="replace", api_key="test-private-api-key", expected_revision=None)
        self.assertTrue(receipt["saved"])
        self.assertEqual(settings.load_settings()["api_key"], "test-private-api-key")
        self.assertEqual(settings.load_settings()["root"], str(self.root.resolve()))
        self.assertEqual(receipt["settings_revision"], hashlib.sha256(settings.settings_path().read_bytes()).hexdigest())
        self.assertNotIn("test-private-api-key", json.dumps(receipt))
        self.assertNotIn("test-private-api-key", json.dumps(settings.public_settings()))
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(settings.settings_path().stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(settings.settings_path().parent.stat().st_mode), 0o700)

    def test_default_user_path_does_not_require_xdg_setting(self):
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(Path, "home", return_value=self.directory):
            self.assertEqual(settings.settings_path(), self.directory / ".config/local-translation/settings.json")

    def test_browser_launcher_waits_for_ready_and_returns_no_private_page_capability(self):
        child = mock.Mock()
        child.stdout = io.BytesIO(b"READY\n")
        with mock.patch.object(setup.subprocess, "Popen", return_value=child) as launch:
            result = setup.open_settings()
        self.assertTrue(result["browser_opened"])
        self.assertNotIn("http://", json.dumps(result))
        self.assertNotIn("token", json.dumps(result).lower())
        self.assertIn("--serve", launch.call_args.args[0])
        child.terminate.assert_not_called()
        failed = mock.Mock()
        failed.stdout = io.BytesIO(b"ERROR\n")
        with mock.patch.object(setup.subprocess, "Popen", return_value=failed):
            with self.assertRaises(settings.SettingsError) as result:
                setup.open_settings()
        self.assertEqual(result.exception.code, "browser_unavailable")
        failed.terminate.assert_called_once()

    def test_keep_replace_clear_controls_and_never_prefill_secret(self):
        self.save(api_key_action="replace", api_key="first-secret")
        self.save(api_key_action="keep", expected_revision=settings.settings_revision())
        self.assertEqual(settings.load_settings()["api_key"], "first-secret")
        self.save(api_key_action="replace", api_key="replacement-secret")
        self.assertEqual(settings.load_settings()["api_key"], "replacement-secret")
        self.save(api_key_action="clear")
        self.assertNotIn("api_key", settings.load_settings())
        self.assertFalse(settings.public_settings()["credential_configured"])
        for action, key in (("replace", ""), ("replace", "bad\nkey"), ("keep", "unexpected"), ("clear", "unexpected")):
            with self.subTest(action=action), self.assertRaises(settings.SettingsError):
                self.save(api_key_action=action, api_key=key)

    def test_invalid_configuration_and_failed_verification_preserve_old_bytes(self):
        self.save(api_key_action="replace", api_key="unchanged-key")
        before = settings.settings_path().read_bytes()
        invalid = [dict(self.deployment(), base_url="http://example.com:8080/v1"),
                   dict(self.deployment(), artifact_revision="REPLACE_WITH_REVISION"),
                   dict(self.deployment(), api_key_env="SOME_VARIABLE"),
                   dict(self.deployment(), locales=[]), dict(self.deployment(), timeout_seconds=999)]
        for candidate in invalid:
            probe = mock.Mock()
            with self.subTest(candidate=candidate), self.assertRaises(settings.SettingsError):
                self.save(candidate, verify=probe)
            probe.assert_not_called()
            self.assertEqual(settings.settings_path().read_bytes(), before)
        def failure(*_):
            raise RuntimeError("PRIVATE_DEPENDENCY_ERROR_AND_KEY")
        with self.assertRaises(settings.SettingsError) as result:
            self.save(verify=failure)
        self.assertNotIn("PRIVATE_DEPENDENCY", str(result.exception))
        self.assertEqual(settings.settings_path().read_bytes(), before)

    def test_failed_atomic_write_preserves_previous_settings(self):
        self.save()
        before = settings.settings_path().read_bytes()
        with mock.patch.object(settings.os, "replace", side_effect=OSError("PRIVATE_WRITE_ERROR")):
            with self.assertRaises(settings.SettingsError) as result:
                self.save(dict(self.deployment(), artifact_revision="updated"))
        self.assertEqual(result.exception.code, "save_failed")
        self.assertEqual(settings.settings_path().read_bytes(), before)
        self.assertEqual(list(settings.settings_path().parent.glob(".settings-*")), [])

    def test_stale_edits_rejected_before_and_after_engine_probe(self):
        self.save()
        old_revision = settings.settings_revision()
        self.save(dict(self.deployment(), artifact_revision="second"))
        probe = mock.Mock()
        with self.assertRaises(settings.SettingsError) as result:
            self.save(expected_revision=old_revision, verify=probe)
        self.assertEqual(result.exception.code, "stale_configuration")
        probe.assert_not_called()
        latest_revision = settings.settings_revision()
        def concurrent_change(*_):
            self.save(dict(self.deployment(), artifact_revision="third"))
        with self.assertRaises(settings.SettingsError) as result:
            self.save(expected_revision=latest_revision, verify=concurrent_change)
        self.assertEqual(result.exception.code, "stale_configuration")
        self.assertEqual(settings.load_settings()["deployment"]["artifact_revision"], "third")

    def test_corrupt_or_symlink_settings_are_not_overwritten(self):
        path = settings.settings_path()
        path.parent.mkdir(parents=True)
        path.write_bytes(b'{"root":"PRIVATE_BAD_JSON"')
        path.chmod(0o600)
        before = path.read_bytes()
        with self.assertRaises(settings.SettingsError):
            self.save()
        self.assertEqual(path.read_bytes(), before)
        path.unlink()
        outside = self.directory / "outside.json"
        outside.write_text("private-outside-content")
        path.symlink_to(outside)
        with self.assertRaises(settings.SettingsError):
            settings.load_settings()
        self.assertEqual(outside.read_text(), "private-outside-content")

    @contextmanager
    def page(self, *, verify=None, lifetime=600):
        with setup.SetupServer(core.validate_config, verify or core.verify_deployment, lifetime=lifetime) as server:
            thread = threading.Thread(target=server.run, daemon=True)
            thread.start()
            try:
                yield server
            finally:
                server.deadline = time.monotonic()
                thread.join(timeout=7)
                self.assertFalse(thread.is_alive())

    def http(self, server, data=None, *, method="POST", path=None, headers=None, raw=None):
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        body = raw if raw is not None else json.dumps(data).encode() if data is not None else None
        base_headers = {"Origin": server.origin, "Content-Type": "application/json", "X-Setup-Token": server.token}
        base_headers.update(headers or {})
        connection.request(method, path or server.path, body=body, headers=base_headers)
        response = connection.getresponse()
        status, response_headers, content = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return status, response_headers, content

    def payload(self, deployment, revision=None, action="keep", key=None):
        data = {"action": "save", "root": str(self.root), "deployment": deployment,
                "credential_action": action, "expected_revision": revision}
        if key is not None:
            data["api_key"] = key
        return data

    def test_full_browser_http_setup_checks_model_tokenizer_saves_then_exits(self):
        with engine() as state, self.page() as server:
            status, headers, html = self.http(server, method="GET")
            self.assertEqual(status, 200)
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
            self.assertNotIn(server.token.encode(), html)
            status, _, content = self.http(server, {"action": "read"})
            self.assertEqual(status, 200)
            self.assertFalse(json.loads(content)["configured"])
            payload = self.payload(self.deployment(state["url"]), action="replace", key="browser-only-secret")
            status, _, content = self.http(server, payload)
            self.assertEqual(status, 200, content)
            self.assertTrue(json.loads(content)["saved"])
            self.assertNotIn(b"browser-only-secret", content)
            self.assertEqual(settings.load_settings()["api_key"], "browser-only-secret")
            self.assertEqual([item[0] for item in state["requests"]], ["/v1/models", "/tokenize"])
            self.assertTrue(all(item[2] == "Bearer browser-only-secret" for item in state["requests"]))
            self.assertIn("messages", state["requests"][1][1])
            self.assertTrue(server.saved)
        self.assertFalse((self.root / ".local-translation").exists())

    def test_incompatible_tokenizer_preserves_settings_and_explains_required_api(self):
        self.save()
        before = settings.settings_path().read_bytes()
        with engine() as state, self.page() as server:
            state["tokenizer_status"] = 404
            status, _, body = self.http(server, self.payload(self.deployment(state["url"]), settings.settings_revision()))
            self.assertEqual(status, 400)
            self.assertIn(b"tokeniz", body.lower())
            self.assertFalse(server.saved)
            self.assertEqual(settings.settings_path().read_bytes(), before)

    def test_browser_protects_state_with_origin_host_token_type_path_and_size_checks(self):
        probe = mock.Mock()
        with self.page(verify=probe) as server:
            cases = [({"Origin": "http://malicious.example"}, None),
                     ({"Host": "malicious.example"}, None),
                     ({"X-Setup-Token": "wrong"}, None),
                     ({"Content-Type": "text/plain"}, None),
                     ({}, server.path + "?unexpected=1"),
                     ({"Transfer-Encoding": "chunked"}, None)]
            for headers, path in cases:
                with self.subTest(headers=headers):
                    status, _, _ = self.http(server, self.payload(self.deployment()), headers=headers, path=path)
                    self.assertEqual(status, 403)
            status, _, _ = self.http(server, raw=b"x" * (setup.MAX_BODY + 1))
            self.assertEqual(status, 413)
            status, _, _ = self.http(server, raw=b'{"action":"read","action":"read"}')
            self.assertEqual(status, 400)
        probe.assert_not_called()
        self.assertIsNone(settings.load_settings())

    def test_http_prefill_hides_saved_key_and_rejects_stale_page(self):
        self.save(api_key_action="replace", api_key="never-prefill-me")
        with self.page(verify=lambda *_: None) as server:
            status, _, content = self.http(server, {"action": "read"})
            previous = json.loads(content)
            self.assertEqual(status, 200)
            self.assertTrue(previous["credential_configured"])
            self.assertNotIn(b"never-prefill-me", content)
            self.save(dict(self.deployment(), artifact_revision="newest"))
            status, _, content = self.http(server, self.payload(self.deployment(), previous["settings_revision"]))
            self.assertEqual(status, 409)
            self.assertEqual(json.loads(content)["code"], "stale_configuration")
            self.assertEqual(settings.load_settings()["deployment"]["artifact_revision"], "newest")

    def test_expired_page_rejects_save_without_running_probe(self):
        probe = mock.Mock()
        with setup.SetupServer(core.validate_config, probe) as server:
            server.deadline = time.monotonic() - 1
            # One HTTP request is accepted for this test even after expiry; the
            # authorization gate must reject it before inspecting saved state.
            thread = threading.Thread(target=server.handle_request, daemon=True)
            thread.start()
            status, _, _ = self.http(server, self.payload(self.deployment()))
            self.assertEqual(status, 403)
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())
        probe.assert_not_called()


if __name__ == "__main__":
    unittest.main()
