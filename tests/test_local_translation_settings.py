"""Desktop setup behavior, using isolated user settings and a synthetic runner."""

from contextlib import contextmanager
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import queue
import stat
import subprocess
import sys
import tempfile
import threading
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
with mock.patch.dict(sys.modules, {"settings": settings}):
    migration = module("local_translation_settings_migration", "migrate_settings.py")


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
        self.environment = mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.directory / "config")})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def deployment(self, url="http://127.0.0.1:8080/v1"):
        return {"base_url": url, "model": "index-setup-test", "artifact_revision": "test-revision",
                "runner_version": "test-only", "locales": {"en-US": "English", "fr-FR": "French"}}

    def save(self, deployment=None, **kwargs):
        return settings.save_settings(deployment or self.deployment(),
                                      validate=core.validate_config, verify=kwargs.pop("verify", lambda *_: None), **kwargs)

    def test_persistent_settings_without_launch_environment_and_private_permissions(self):
        self.assertIsNone(settings.load_settings())
        self.assertFalse(settings.public_settings()["configured"])
        receipt = self.save(api_key_action="replace", api_key="test-private-api-key", expected_revision=None)
        self.assertTrue(receipt["saved"])
        self.assertEqual(settings.load_settings()["api_key"], "test-private-api-key")
        self.assertNotIn("root", settings.load_settings())
        self.assertNotIn("root", receipt)
        self.assertNotIn("root", settings.public_settings())
        self.assertEqual(receipt["settings_revision"], hashlib.sha256(settings.settings_path().read_bytes()).hexdigest())
        self.assertNotIn("test-private-api-key", json.dumps(receipt))
        self.assertNotIn("test-private-api-key", json.dumps(settings.public_settings()))
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(settings.settings_path().stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(settings.settings_path().parent.stat().st_mode), 0o700)

    def test_default_user_path_does_not_require_xdg_setting(self):
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(Path, "home", return_value=self.directory):
            self.assertEqual(settings.settings_path(), self.directory / ".config/local-translation/settings.json")

    def call(self, name, arguments=None):
        return core.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                              "params": {"name": name, "arguments": arguments or {}}})["result"]

    def save_arguments(self, deployment=None, revision=None, action="keep", key=None):
        value = {"deployment": deployment or self.deployment(), "credential_action": action,
                 "expected_revision": revision}
        if key is not None:
            value["api_key"] = key
        return value

    def prefill(self):
        return self.call("translation_read_settings")["_meta"]["local-translation/settings"]

    def test_native_settings_offer_a_modal_action_and_hide_private_tools_from_model(self):
        initialized = core.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize"})["result"]
        self.assertIn("resources", initialized["capabilities"])
        self.assertEqual(initialized["capabilities"]["extensions"]["openai/settings"],
                         {"readTool": "translation_read_settings", "updateTool": "translation_update_settings"})
        tools = core.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]
        self.assertEqual(len(tools), 14)
        private = {tool["name"] for tool in tools if tool.get("_meta", {}).get("ui", {}).get("visibility") == ["app"]}
        self.assertEqual(private, {"translation_read_settings", "translation_update_settings",
                                   "translation_save_settings", "translation_migrate_settings"})
        by_name = {tool["name"]: tool for tool in tools}
        self.assertEqual(by_name["translation_open_settings"]["_meta"]["ui"]["resourceUri"], setup.RESOURCE_URI)
        for name in private:
            self.assertIn("outputSchema", by_name[name])
        self.assertTrue(by_name["translation_read_settings"]["annotations"]["readOnlyHint"])
        self.assertFalse(by_name["translation_save_settings"]["annotations"]["readOnlyHint"])
        read = self.call("translation_read_settings")
        self.assertFalse(read["isError"])
        self.assertEqual(read["structuredContent"]["schema"], {"type": "object", "properties": {}})
        self.assertEqual(read["structuredContent"]["values"], {})
        self.assertEqual(read["structuredContent"]["layout"][0]["kind"], "group")
        action = read["structuredContent"]["layout"][0]["items"][0]
        self.assertEqual((action["kind"], action["tool"]), ("tool", "translation_open_settings"))
        self.assertFalse(self.prefill()["configured"])
        self.assertFalse(settings.settings_path().exists())

    def test_popup_resources_are_bundled_and_never_launch_a_browser_or_child_process(self):
        with mock.patch("subprocess.Popen", side_effect=AssertionError("No external setup process")), \
             mock.patch("webbrowser.open", side_effect=AssertionError("No browser launch")):
            opened = self.call("translation_open_settings")
            self.assertFalse(opened["isError"])
            self.assertEqual(opened["structuredContent"]["settings_ui"], "in_app")
            listed = core.dispatch({"jsonrpc": "2.0", "id": 1, "method": "resources/list"})["result"]["resources"]
            self.assertEqual([resource["uri"] for resource in listed], [setup.RESOURCE_URI])
            resource = core.dispatch({"jsonrpc": "2.0", "id": 2, "method": "resources/read",
                                      "params": {"uri": setup.RESOURCE_URI}})["result"]["contents"][0]
            self.assertEqual(resource["mimeType"], "text/html;profile=mcp-app")
            self.assertEqual(resource["text"], (MCP / "setup.html").read_text())
            self.assertEqual(resource["_meta"]["ui"]["csp"], {"connectDomains": [], "resourceDomains": []})
        for uri in ("file:///private/settings.json", setup.RESOURCE_URI + "?path=private", setup.RESOURCE_URI + "/other"):
            result = core.dispatch({"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": uri}})
            self.assertEqual(result["error"]["code"], -32602)
            self.assertNotIn(uri, json.dumps(result))
        self.assertFalse(settings.settings_path().exists())

    def test_private_form_save_checks_model_and_tokenizer_without_returning_key(self):
        key = "popup-private-test-key"
        with engine() as state:
            result = self.call("translation_save_settings", self.save_arguments(self.deployment(state["url"]), action="replace", key=key))
            self.assertFalse(result["isError"], result)
            self.assertTrue(result["structuredContent"]["saved"])
            self.assertNotIn(key, json.dumps(result))
            self.assertEqual([item[0] for item in state["requests"]], ["/v1/models", "/tokenize"])
            self.assertTrue(all(item[2] == "Bearer " + key for item in state["requests"]))
            self.assertIn("messages", state["requests"][1][1])
        prefill = self.prefill()
        self.assertEqual(prefill["settings_revision"], settings.settings_revision())
        self.assertTrue(prefill["credential_configured"])
        self.assertNotIn(key, json.dumps(prefill))
        self.assertEqual(set(settings.load_settings()), {"schema_version", "deployment", "api_key"})

    def test_private_save_failure_stale_revision_and_environment_preserve_previous_bytes(self):
        self.save(api_key_action="replace", api_key="preserved-private-key")
        before = settings.settings_path().read_bytes()
        revision = settings.settings_revision()
        with engine() as state:
            state["tokenizer_status"] = 404
            result = self.call("translation_save_settings", self.save_arguments(self.deployment(state["url"]), revision, "replace", "rejected-private-key"))
            self.assertTrue(result["isError"])
            self.assertEqual(result["structuredContent"]["code"], "tokenizer_unsupported")
            self.assertEqual(settings.settings_path().read_bytes(), before)
            self.assertNotIn("rejected-private-key", json.dumps(result))
        with mock.patch.object(core, "verify_deployment") as verify:
            stale = self.call("translation_save_settings", self.save_arguments(revision="0" * 64))
            self.assertEqual(stale["structuredContent"]["code"], "stale_configuration")
            with mock.patch.dict(os.environ, {"LOCAL_TRANSLATION_CONFIG": ""}):
                overridden = self.call("translation_save_settings", self.save_arguments(revision=revision))
                self.assertEqual(overridden["structuredContent"]["code"], "environment_override")
            verify.assert_not_called()
        self.assertEqual(settings.settings_path().read_bytes(), before)

    def test_private_save_validates_contract_and_sanitizes_dependency_failures(self):
        self.save()
        before = settings.settings_path().read_bytes()
        revision = settings.settings_revision()
        arguments = self.save_arguments(revision=revision, action="replace", key="must-not-be-echoed")
        invalid = [{**arguments, "root": "private-path"},
                   {key: value for key, value in arguments.items() if key != "expected_revision"},
                   {**arguments, "deployment": {**arguments["deployment"], "root": "private-path"}},
                   {**arguments, "credential_action": "invalid"},
                   {**arguments, "expected_revision": 1}]
        with mock.patch.object(core, "verify_deployment") as verify:
            for payload in invalid:
                with self.subTest(payload=payload):
                    result = self.call("translation_save_settings", payload)
                    self.assertTrue(result["isError"])
                    self.assertNotIn("must-not-be-echoed", json.dumps(result))
                    self.assertEqual(settings.settings_path().read_bytes(), before)
            verify.assert_not_called()
        with mock.patch.object(core, "verify_deployment", side_effect=RuntimeError("must-not-be-echoed")):
            result = self.call("translation_save_settings", arguments)
            self.assertEqual(result["structuredContent"]["code"], "verification_failed")
            self.assertNotIn("must-not-be-echoed", json.dumps(result))
        self.assertEqual(settings.settings_path().read_bytes(), before)

    def test_native_update_accepts_only_empty_set_and_cannot_bypass_form_validation(self):
        self.save()
        before = settings.settings_path().read_bytes()
        result = self.call("translation_update_settings", {"set": {}})
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"], {"values": {}})
        for arguments in ({"set": {"api_key": "private-key"}}, {"set": {}, "deployment": self.deployment()}, {}):
            result = self.call("translation_update_settings", arguments)
            self.assertTrue(result["isError"])
            self.assertNotIn("private-key", json.dumps(result))
        self.assertEqual(settings.settings_path().read_bytes(), before)

    def test_legacy_settings_keep_configure_action_and_require_explicit_private_upgrade(self):
        path, before = self.legacy_settings()
        read = self.call("translation_read_settings")
        self.assertFalse(read["isError"])
        prefill = read["_meta"]["local-translation/settings"]
        self.assertTrue(prefill["migration_required"])
        self.assertEqual(prefill["code"], "migration_required")
        self.assertNotIn("legacy-test-secret", json.dumps(read))
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse(path.with_name(path.name + migration.BACKUP_SUFFIX).exists())
        with mock.patch.object(core, "verify_deployment", side_effect=AssertionError("Upgrade must not contact engine")):
            result = self.call("translation_migrate_settings")
        self.assertFalse(result["isError"], result)
        self.assertTrue(result["structuredContent"]["migrated"])
        self.assertEqual(Path(result["structuredContent"]["backup_path"]).read_bytes(), before)
        self.assertNotIn("legacy-test-secret", json.dumps(result))
        self.assertFalse(self.prefill()["migration_required"])
        self.assertTrue(self.prefill()["credential_configured"])
        self.assertEqual(settings.load_settings()["api_key"], "legacy-test-secret")

    def test_private_upgrade_rejects_paths_environment_override_and_backup_failure(self):
        path, before = self.legacy_settings()
        with mock.patch.dict(os.environ, {"LOCAL_TRANSLATION_CONFIG": ""}):
            result = self.call("translation_migrate_settings")
            self.assertEqual(result["structuredContent"]["code"], "environment_override")
        result = self.call("translation_migrate_settings", {"path": str(path)})
        self.assertTrue(result["isError"])
        backup = path.with_name(path.name + migration.BACKUP_SUFFIX)
        backup.write_bytes(b"different-private-backup")
        backup.chmod(0o600)
        result = self.call("translation_migrate_settings")
        self.assertTrue(result["isError"])
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(backup.read_bytes(), b"different-private-backup")
        self.assertNotIn("legacy-test-secret", json.dumps(result))


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

    def test_process_death_releases_settings_lock_without_manual_recovery(self):
        self.save()
        before = settings.settings_path().read_bytes()
        script = """
import importlib.util
import sys
spec = importlib.util.spec_from_file_location('child_translation_settings', sys.argv[1])
settings = importlib.util.module_from_spec(spec)
spec.loader.exec_module(settings)
with settings._locked(settings.settings_path()):
    print('LOCKED', flush=True)
    sys.stdin.read(1)
"""
        child = subprocess.Popen(
            [sys.executable, "-c", script, str(MCP / "settings.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        try:
            ready = queue.Queue(maxsize=1)
            reader = threading.Thread(target=lambda: ready.put(child.stdout.readline()), daemon=True)
            reader.start()
            self.assertEqual(ready.get(timeout=5), "LOCKED\n")
            with self.assertRaises(settings.SettingsError) as result:
                self.save(dict(self.deployment(), artifact_revision="after-interruption"))
            self.assertEqual(result.exception.code, "settings_busy")
            self.assertEqual(settings.settings_path().read_bytes(), before)
            child.terminate()
            child.wait(timeout=5)
            # Termination bypassed the child's context-manager cleanup. A new
            # save must succeed without deleting or editing hidden lock files.
            self.save(dict(self.deployment(), artifact_revision="after-interruption"))
            self.assertEqual(settings.load_settings()["deployment"]["artifact_revision"], "after-interruption")
        finally:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=5)
            child.stdin.close()
            child.stdout.close()

    def test_settings_lock_rejects_symlink_and_nonregular_file_without_changing_settings(self):
        self.save()
        before = settings.settings_path().read_bytes()
        lock = settings.settings_path().parent / ".settings.lock"
        lock.unlink()
        outside = self.directory / "outside-lock-target"
        outside.write_text("outside-content")
        lock.symlink_to(outside)
        with self.assertRaises(settings.SettingsError) as result:
            self.save()
        self.assertEqual(result.exception.code, "local_settings_failed")
        self.assertEqual(outside.read_text(), "outside-content")
        self.assertEqual(settings.settings_path().read_bytes(), before)
        lock.unlink()
        lock.mkdir()
        with self.assertRaises(settings.SettingsError) as result:
            self.save()
        self.assertEqual(result.exception.code, "local_settings_failed")
        self.assertEqual(settings.settings_path().read_bytes(), before)

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










    def legacy_settings(self):
        path = settings.settings_path()
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        value = {"root": str(self.directory / "former-workspace"),
                 "deployment": core.validate_config(self.deployment()), "api_key": "legacy-test-secret"}
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        path.chmod(0o600)
        return path, raw

    def test_legacy_settings_require_explicit_migration_without_mutation(self):
        path, before = self.legacy_settings()
        with self.assertRaises(settings.SettingsError) as result:
            settings.load_settings()
        self.assertEqual(result.exception.code, "migration_required")
        with self.assertRaises(settings.SettingsError):
            self.save()
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse(path.with_name(path.name + migration.BACKUP_SUFFIX).exists())

    def test_explicit_migration_preserves_engine_secret_and_private_original_backup(self):
        path, before = self.legacy_settings()
        result = migration.migrate(validate=core.validate_config)
        backup = Path(result["backup_path"])
        self.assertTrue(result["migrated"])
        self.assertEqual(backup.read_bytes(), before)
        converted = settings.load_settings()
        self.assertEqual(set(converted), {"schema_version", "deployment", "api_key"})
        self.assertEqual(converted["deployment"], json.loads(before)["deployment"])
        self.assertEqual(converted["api_key"], "legacy-test-secret")
        self.assertNotIn("legacy-test-secret", json.dumps(result))
        self.assertFalse((self.directory / "former-workspace").exists())
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
        after = path.read_bytes()
        self.assertFalse(migration.migrate(validate=core.validate_config)["migrated"])
        self.assertEqual(path.read_bytes(), after)
        self.assertEqual(backup.read_bytes(), before)

    def test_migration_write_failure_preserves_original_and_retry_uses_exact_backup(self):
        path, before = self.legacy_settings()
        with mock.patch.object(settings.os, "replace", side_effect=OSError("PRIVATE_WRITE_FAILURE")):
            with self.assertRaises(settings.SettingsError) as result:
                migration.migrate(validate=core.validate_config)
        self.assertEqual(result.exception.code, "save_failed")
        self.assertEqual(path.read_bytes(), before)
        backup = path.with_name(path.name + migration.BACKUP_SUFFIX)
        self.assertEqual(backup.read_bytes(), before)
        self.assertTrue(migration.migrate(validate=core.validate_config)["migrated"])

    def test_migration_command_converts_explicit_file_without_printing_secret(self):
        path, before = self.legacy_settings()
        result = subprocess.run(
            [sys.executable, str(MCP / "migrate_settings.py"), "--settings", str(path)],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertTrue(receipt["migrated"])
        self.assertEqual(Path(receipt["backup_path"]).read_bytes(), before)
        self.assertNotIn("legacy-test-secret", result.stdout + result.stderr)
        self.assertNotIn("root", settings.load_settings())

    @unittest.skipUnless(os.name == "posix", "POSIX directory permission contract")
    def test_explicit_migration_preserves_parent_permissions_on_all_outcomes(self):
        parent = self.directory / "shared-settings-parent"
        parent.mkdir()
        parent.chmod(0o755)
        path = parent / "custom-settings.json"
        path.write_bytes(b"{}")
        path.chmod(0o600)
        with self.assertRaises(migration.MigrationError):
            migration.migrate(path, validate=core.validate_config)
        self.assertEqual(stat.S_IMODE(parent.stat().st_mode), 0o755)
        self.assertEqual(path.read_bytes(), b"{}")
        legacy = {"root": str(self.directory / "old-workspace"),
                  "deployment": core.validate_config(self.deployment())}
        before = json.dumps(legacy).encode()
        path.write_bytes(before)
        self.assertTrue(migration.migrate(path, validate=core.validate_config)["migrated"])
        self.assertEqual(stat.S_IMODE(parent.stat().st_mode), 0o755)
        self.assertFalse(migration.migrate(path, validate=core.validate_config)["migrated"])
        self.assertEqual(stat.S_IMODE(parent.stat().st_mode), 0o755)
        path.write_bytes(before)
        with mock.patch.object(settings.os, "replace", side_effect=OSError("TEST_WRITE_FAILURE")):
            with self.assertRaises(settings.SettingsError):
                migration.migrate(path, validate=core.validate_config)
        self.assertEqual(stat.S_IMODE(parent.stat().st_mode), 0o755)
        self.assertEqual(path.read_bytes(), before)

    def test_migration_rejects_conflicting_backup_or_unsafe_settings(self):
        path, before = self.legacy_settings()
        backup = path.with_name(path.name + migration.BACKUP_SUFFIX)
        backup.write_bytes(b"unrelated-private-backup")
        backup.chmod(0o600)
        with self.assertRaises(migration.MigrationError) as result:
            migration.migrate(validate=core.validate_config)
        self.assertEqual(result.exception.code, "backup_conflict")
        self.assertEqual(backup.read_bytes(), b"unrelated-private-backup")
        self.assertEqual(path.read_bytes(), before)
        backup.unlink()
        path.unlink()
        outside = self.directory / "outside-settings"
        outside.write_bytes(before)
        outside.chmod(0o600)
        path.symlink_to(outside)
        with self.assertRaises(settings.SettingsError):
            migration.migrate(validate=core.validate_config)
        self.assertEqual(outside.read_bytes(), before)

if __name__ == "__main__":
    unittest.main()
