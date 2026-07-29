from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "conversation-visuals"
SERVER_PATH = PLUGIN_ROOT / "mcp" / "server.py"

sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("conversation_visuals_server", SERVER_PATH)
assert SPEC is not None and SPEC.loader is not None
SERVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER)


class ConversationVisualsTests(unittest.TestCase):
    def test_quiet_and_low_utility_turns_stay_visual_free(self) -> None:
        quiet = SERVER.plan_visual({"preference": "quiet", "utility": "high"})
        low_utility = SERVER.plan_visual({"utility": "low"})

        self.assertEqual(quiet["disposition"], "no-visual")
        self.assertIsNone(quiet["kind"])
        self.assertEqual(low_utility["disposition"], "no-visual")

    def test_explicit_visual_request_overrides_quiet_mode(self) -> None:
        result = SERVER.plan_visual(
            {
                "preference": "quiet",
                "explicit": True,
                "requested_kind": "diagram",
                "utility": "high",
            }
        )

        self.assertEqual(result["disposition"], "produce")
        self.assertEqual(result["kind"], "diagram")

    def test_video_always_requires_consent(self) -> None:
        result = SERVER.plan_visual(
            {"explicit": True, "requested_kind": "video", "utility": "high"}
        )

        self.assertTrue(result["consent_required"])
        self.assertEqual(result["disposition"], "suggest-first")

    def test_inferred_expensive_visuals_require_consent_in_automatic_mode(self) -> None:
        for kind in ("generated-image", "slides"):
            with self.subTest(kind=kind):
                result = SERVER.plan_visual(
                    {"requested_kind": kind, "utility": "high"}
                )

                self.assertTrue(result["consent_required"])
                self.assertEqual(result["disposition"], "suggest-first")

    def test_sourced_result_requires_originating_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "originating source"):
            SERVER.normalize_visual(
                {
                    "provenance": "sourced",
                    "title": "Missing origin",
                    "alt_text": "A visual without a source.",
                }
            )

    def test_generated_result_requires_disclosure(self) -> None:
        with self.assertRaisesRegex(ValueError, "generation disclosure"):
            SERVER.normalize_visual(
                {
                    "provenance": "generated",
                    "title": "Undisclosed generation",
                    "alt_text": "A generated visual.",
                }
            )

    def test_normalized_result_rejects_unsupported_visual_kind(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported kind"):
            SERVER.normalize_visual(
                {
                    "kind": "image",
                    "provenance": "generated",
                    "title": "Unsupported kind",
                    "alt_text": "A generated visual.",
                    "generation_disclosure": "Generated for this conversation.",
                }
            )

    def test_private_and_credentialed_urls_are_rejected(self) -> None:
        rejected = (
            "http://127.0.0.1/item",
            "http://169.254.169.254/latest/meta-data",
            "https://user:secret@example.com/item",
            "file:///tmp/item.png",
        )

        for url in rejected:
            with self.subTest(url=url):
                self.assertFalse(SERVER.public_http_url(url))

    def test_mcp_stdio_initialize_and_tools_list(self) -> None:
        requests = "\n".join(
            json.dumps(item)
            for item in (
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {"protocolVersion": "1900-01-01"},
                },
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            )
        )
        result = subprocess.run(
            [sys.executable, str(SERVER_PATH)],
            input=requests + "\n",
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(responses[0]["result"]["serverInfo"]["name"], "conversation-visuals")
        self.assertEqual(
            responses[0]["result"]["protocolVersion"],
            SERVER.PROTOCOL_VERSION,
        )
        self.assertEqual(
            {tool["name"] for tool in responses[1]["result"]["tools"]},
            {"plan_visual", "normalize_visual"},
        )

    def test_mcp_malformed_requests_do_not_terminate_process(self) -> None:
        requests = "\n".join(
            json.dumps(item)
            for item in (
                [],
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": None,
                },
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {"name": "plan_visual", "arguments": None},
                },
                {"jsonrpc": "2.0", "id": 3, "method": "tools/list"},
            )
        )

        result = subprocess.run(
            [sys.executable, str(SERVER_PATH)],
            input=requests + "\n",
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(
            [response["error"]["code"] for response in responses[:3]],
            [-32600, -32602, -32602],
        )
        self.assertEqual(responses[3]["id"], 3)
        self.assertEqual(
            {tool["name"] for tool in responses[3]["result"]["tools"]},
            {"plan_visual", "normalize_visual"},
        )

    def test_manifest_declares_bundled_mcp_and_four_skills(self) -> None:
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(manifest["name"], "conversation-visuals")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        self.assertEqual(len(list((PLUGIN_ROOT / "skills").glob("*/SKILL.md"))), 4)


if __name__ == "__main__":
    unittest.main()
