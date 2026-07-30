from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "conversation-visuals"
SERVER_PATH = PLUGIN_ROOT / "mcp" / "server.py"
SUBPROCESS_TIMEOUT_SECONDS = 30

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

    def test_explicit_video_request_is_authorized(self) -> None:
        result = SERVER.plan_visual(
            {"explicit": True, "requested_kind": "video", "utility": "high"}
        )

        self.assertFalse(result["consent_required"])
        self.assertEqual(result["disposition"], "produce")

    def test_suggest_first_applies_to_inferred_low_cost_visuals(self) -> None:
        result = SERVER.plan_visual(
            {
                "preference": "suggest-first",
                "requested_kind": "diagram",
                "utility": "high",
            }
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

    def test_non_boolean_explicit_flag_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "explicit must be a boolean"):
            SERVER.plan_visual(
                {
                    "preference": "quiet",
                    "explicit": "false",
                    "requested_kind": "video",
                    "utility": "high",
                }
            )

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

    def test_generation_disclosure_is_bounded_for_all_provenance(self) -> None:
        invalid_visuals = (
            {
                "provenance": "generated",
                "title": "Generated visual",
                "alt_text": "A generated visual.",
                "generation_disclosure": "x" * 2001,
                "artifact_ref": "attachment:generated-visual",
            },
            {
                "provenance": "sourced",
                "title": "Sourced visual",
                "alt_text": "A sourced visual.",
                "generation_disclosure": "x" * 2001,
                "sources": [
                    {"title": "Origin", "url": "https://example.com/item"}
                ],
            },
        )

        for visual in invalid_visuals:
            with self.subTest(provenance=visual["provenance"]), self.assertRaisesRegex(
                ValueError,
                "generation_disclosure must not exceed 2000 characters",
            ):
                SERVER.normalize_visual(visual)

    def test_normalized_result_rejects_unsupported_visual_kind(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported kind"):
            SERVER.normalize_visual(
                {
                    "kind": "image",
                    "provenance": "generated",
                    "title": "Unsupported kind",
                    "alt_text": "A generated visual.",
                    "generation_disclosure": "Generated for this conversation.",
                    "artifact_ref": "attachment:unsupported-kind",
                }
            )

    def test_normalized_result_defaults_kind_from_provenance(self) -> None:
        generated = SERVER.normalize_visual(
            {
                "provenance": "generated",
                "title": "Generated visual",
                "alt_text": "A generated visual.",
                "generation_disclosure": "Generated for this conversation.",
                "artifact_ref": "/tmp/generated-visual.png",
            }
        )
        sourced = SERVER.normalize_visual(
            {
                "provenance": "sourced",
                "title": "Sourced visual",
                "alt_text": "A sourced visual.",
                "sources": [
                    {"title": "Origin", "url": "https://example.com/item"}
                ],
            }
        )

        self.assertEqual(generated["kind"], "generated-image")
        self.assertEqual(sourced["kind"], "source-image")

    def test_required_text_metadata_rejects_non_strings(self) -> None:
        invalid_values = (
            ("title", None, "title must be a string"),
            ("alt_text", False, "alt_text must be a string"),
            (
                "generation_disclosure",
                False,
                "generation_disclosure must be a string",
            ),
        )
        for field, value, expected_error in invalid_values:
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError,
                expected_error,
            ):
                arguments = {
                    "provenance": "generated",
                    "title": "Generated visual",
                    "alt_text": "A generated visual.",
                    "generation_disclosure": "Generated for this conversation.",
                }
                arguments[field] = value
                SERVER.normalize_visual(arguments)

    def test_private_and_credentialed_urls_are_rejected(self) -> None:
        rejected = (
            "http://[::1]/item",
            "http://[fe80::1]/item",
            "http://127.0.0.1/item",
            "http://127.0.0.1./item",
            "http://127.1/item",
            "http://2130706433/item",
            "http://0x7f000001/item",
            "http://0177.0.0.1/item",
            "http://%31%32%37.0.0.1/item",
            "http://%2531%2532%2537.0.0.1/item",
            "http://127%2e0%2e0%2e1/item",
            "http://127.0.0.1%3a80/item",
            "http://127.0.0.1%09/item",
            "http://127。0。0。1/item",
            "http://localhost./item",
            "http://media.localhost/item",
            "http://169.254.169.254/latest/meta-data",
            "http://100.64.0.1/item",
            "http://192.0.0.1/item",
            "https://user:secret@example.com/item",
            "https://example.com:/item",
            "https://example.com:bad/item",
            "https://example.com:99999/item",
            "file:///tmp/item.png",
            "https://example.com/a\nb",
            "https://example.com/a\rb",
            "https://example.com/a\tb",
            "https://example.com/item#unsafe\nfragment",
        )

        for url in rejected:
            with self.subTest(url=url):
                self.assertFalse(SERVER.public_http_url(url))

    def test_public_ipv6_literal_is_allowed(self) -> None:
        self.assertTrue(
            SERVER.public_http_url("https://[2606:4700:4700::1111]/item")
        )

    def test_mcp_stdio_initialize_and_tools_list(self) -> None:
        requests = "\n".join(
            json.dumps(item)
            for item in (
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "1900-01-01",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0"},
                    },
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
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
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

    def test_self_test_remains_active_under_python_optimization(self) -> None:
        result = subprocess.run(
            [sys.executable, "-O", str(SERVER_PATH), "--self-test"],
            check=False,
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS conversation-visuals MCP self-test")

    def test_normalize_visual_schema_describes_required_source_fields(self) -> None:
        normalize_tool = next(
            tool for tool in SERVER.TOOLS if tool["name"] == "normalize_visual"
        )
        source_items = normalize_tool["inputSchema"]["properties"]["sources"][
            "items"
        ]

        self.assertEqual(set(source_items["required"]), {"title", "url"})
        self.assertTrue(
            {"title", "url", "publisher", "license", "retrieved_at"}.issubset(
                source_items["properties"]
            )
        )
        self.assertEqual(
            normalize_tool["inputSchema"]["properties"]["generation_disclosure"][
                "maxLength"
            ],
            2000,
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
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
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

    def test_non_standard_json_constants_return_parse_errors(self) -> None:
        invalid_requests = (
            '{"jsonrpc":"2.0","id":1,"method":"ping","params":{"x":NaN}}',
            '{"jsonrpc":"2.0","id":2,"method":"ping","params":{"x":Infinity}}',
            '{"jsonrpc":"2.0","id":3,"method":"ping","params":{"x":-Infinity}}',
        )
        ping = '{"jsonrpc":"2.0","id":4,"method":"ping"}'
        result = subprocess.run(
            [sys.executable, str(SERVER_PATH)],
            input="\n".join((*invalid_requests, ping, "")),
            check=False,
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(
            [response["error"]["code"] for response in responses[:3]],
            [-32700, -32700, -32700],
        )
        self.assertEqual(
            responses[3],
            {"jsonrpc": "2.0", "id": 4, "result": {}},
        )

    def test_decoder_recursion_does_not_terminate_process(self) -> None:
        original_loads = json.loads
        ping = json.dumps({"jsonrpc": "2.0", "id": 3, "method": "ping"})
        output = io.StringIO()

        def load_line(line: str, **kwargs: object) -> object:
            if line == "too-deep\n":
                raise RecursionError("maximum nesting exceeded")
            return original_loads(line, **kwargs)

        with (
            mock.patch.object(SERVER.json, "loads", side_effect=load_line),
            mock.patch.object(SERVER.sys, "stdin", io.StringIO("too-deep\n" + ping + "\n")),
            mock.patch.object(SERVER.sys, "stdout", output),
            mock.patch.object(SERVER.sys, "argv", [str(SERVER_PATH)]),
        ):
            result = SERVER.main()

        self.assertEqual(result, 0)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[1], {"jsonrpc": "2.0", "id": 3, "result": {}})

    def test_mcp_notifications_never_receive_responses(self) -> None:
        requests = "\n".join(
            json.dumps(item)
            for item in (
                {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                },
                {
                    "jsonrpc": "2.0",
                    "method": "notifications/cancelled",
                    "params": {"requestId": 9},
                },
                {"jsonrpc": "2.0", "method": "unknown/notification"},
                {"jsonrpc": "2.0", "id": 3, "method": "ping"},
            )
        )

        result = subprocess.run(
            [sys.executable, str(SERVER_PATH)],
            input=requests + "\n",
            check=False,
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(responses, [{"jsonrpc": "2.0", "id": 3, "result": {}}])

    def test_generated_results_require_a_usable_reference(self) -> None:
        with self.assertRaisesRegex(ValueError, "media or artifact reference"):
            SERVER.normalize_visual(
                {
                    "provenance": "generated",
                    "title": "Missing artifact",
                    "alt_text": "A generated visual with no artifact.",
                    "generation_disclosure": "Generated for this conversation.",
                }
            )

        normalized = SERVER.normalize_visual(
            {
                "provenance": "generated",
                "title": "Local artifact",
                "alt_text": "A generated visual stored by the host.",
                "generation_disclosure": "Generated for this conversation.",
                "artifact_ref": "/tmp/generated visual.png",
            }
        )
        self.assertEqual(normalized["artifact_ref"], "/tmp/generated visual.png")

    def test_mcp_rejects_invalid_envelopes_and_unknown_tools(self) -> None:
        invalid_requests = (
            {},
            {"id": 1, "method": "ping"},
            {"jsonrpc": "1.0", "id": 2, "method": "ping"},
            {"jsonrpc": "2.0", "id": 1.5, "method": "ping"},
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "initialize",
                "params": {},
            },
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {"name": "missing-tool", "arguments": {}},
            },
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/list",
                "params": {"cursor": 1},
            },
        )

        responses = [SERVER.handle(request) for request in invalid_requests]

        self.assertEqual(
            [response["error"]["code"] for response in responses],
            [-32600, -32600, -32600, -32600, -32602, -32602, -32602],
        )
        self.assertEqual(
            [response["id"] for response in responses],
            [None, None, None, None, 4, 5, 6],
        )
        self.assertIn("Unknown tool", responses[-2]["error"]["message"])

    def test_tool_arguments_reject_undeclared_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported plan_visual fields"):
            SERVER.plan_visual({"unexpected": True})
        with self.assertRaisesRegex(ValueError, "unsupported normalize_visual fields"):
            SERVER.normalize_visual({"unexpected": True})

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
