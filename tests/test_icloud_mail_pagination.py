"""Public paging contracts with synthetic mail; never connect to Apple."""
from __future__ import annotations

import copy
import base64
import json
import unittest
from unittest import mock

from test_icloud_mail import server


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.client.select.return_value = ("OK", [b"150"])
        self.client.response.return_value = ("UIDVALIDITY", [b"7"])
        self.uids = list(range(1, 126))
        self.client.uid.side_effect = self.search
        self.connection = mock.patch.object(server, "_imap")
        self.connection.start().return_value.__enter__.return_value = self.client
        self.addCleanup(self.connection.stop)
        self.summary = mock.patch.object(server, "_fetch_summary", side_effect=self.fetch)
        self.fetch_mock = self.summary.start()
        self.addCleanup(self.summary.stop)

    def search(self, _command, *criteria):
        upper = int(criteria[criteria.index("UID") + 1].split(":")[1]) if "UID" in criteria else 0xFFFFFFFF
        # SEARCH ordering is not a client contract; return descending IDs.
        return "OK", [b" ".join(str(uid).encode() for uid in reversed(self.uids) if uid <= upper)]

    def fetch(self, _client, mailbox, validity, uid):
        return {"id": server._encode_ref(mailbox, validity, uid), "has_attachments": False}

    def ids(self, result):
        return [server._decode_ref(item["id"])[2] for item in result["emails"]]

    def test_search_walks_beyond_old_scan_cap_without_duplicates(self):
        args = {}
        seen = []
        sizes = []
        while True:
            result = server.search_emails(args)
            seen.extend(self.ids(result))
            sizes.append(result["returned"])
            self.assertEqual(result["page_size"], 10)
            self.assertLessEqual(result["returned"], 10)
            if not result["has_more"]:
                self.assertIsNone(result["next_page_token"])
                break
            args["page_token"] = result["next_page_token"]
            # New arrival must not displace older messages on later pages.
            self.uids.append(1000 + len(sizes))
            self.uids = [uid for uid in self.uids if uid not in seen]
        self.assertEqual(seen, list(reversed(range(1, 126))))
        self.assertEqual(sizes, [10] * 12 + [5])

    def test_empty_and_exact_page_boundaries(self):
        for count in (0, 1, 9, 10, 11, 20):
            with self.subTest(count=count):
                self.uids = list(range(1, count + 1))
                result = server.search_emails({})
                self.assertEqual(result["returned"], min(count, 10))
                self.assertEqual(result["has_more"], count > 10)

    def test_filtered_empty_page_can_continue(self):
        args = {"has_attachment": True}
        first = server.search_emails(args)
        self.assertEqual(first["returned"], 0)
        self.assertEqual(first["scanned"], 80)
        self.assertTrue(first["has_more"])
        self.assertEqual(self.fetch_mock.call_count, 80)
        self.fetch_mock.side_effect = lambda *args: {**self.fetch(*args), "has_attachments": True}
        second = server.search_emails({**args, "page_token": first["next_page_token"]})
        self.assertEqual(self.ids(second), list(range(45, 35, -1)))

    def test_oversized_and_vanished_candidates_do_not_loop(self):
        self.uids = list(range(1, 23))
        def fetch(*args):
            if args[-1] == 22:
                raise server.SummaryTooLarge("too big")
            if args[-1] == 21:
                raise server.MailError("Message no longer exists in this mailbox")
            return self.fetch(*args)
        self.fetch_mock.side_effect = fetch
        first = server.search_emails({})
        second = server.search_emails({"page_token": first["next_page_token"]})
        self.assertEqual(self.ids(first) + self.ids(second), list(range(20, 0, -1)))
        self.assertTrue(first["truncated"])
        self.assertFalse(second["has_more"])

    def test_token_scope_and_uidvalidity_are_checked(self):
        token = server.search_emails({"subject": "original"})["next_page_token"]
        for changes in ({"subject": "changed"}, {"subject": "original", "mailbox": "Other"}):
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, "page_token"):
                server.search_emails({**changes, "page_token": token})
        self.client.response.return_value = ("UIDVALIDITY", [b"8"])
        with self.assertRaisesRegex(ValueError, "stale page_token"):
            server.search_emails({"subject": "original", "page_token": token})

    def test_invalid_tokens_and_old_limit_are_tool_errors(self):
        for tool in ("search_emails", "list_drafts", "list_mailboxes", "read_email_thread"):
            for value in (None, True, 1, "", "garbage", "x" * 1025):
                with self.subTest(tool=tool, value=str(value)[:20]):
                    args = {"page_token": value}
                    if tool == "read_email_thread":
                        args["message_id"] = server._encode_ref("INBOX", 7, 1)
                    with mock.patch.object(server, "read_email", return_value={"id": "anchor", "mailbox": "INBOX"}), mock.patch.object(server, "_special_mailbox", return_value="Drafts"):
                        response = server.handle({"id": 1, "method": "tools/call", "params": {"name": tool, "arguments": args}})
                    self.assertTrue(response["result"]["isError"])
            args = {"max_results": 50}
            response = server.handle({"id": 1, "method": "tools/call", "params": {"name": tool, "arguments": args}})
            self.assertTrue(response["result"]["isError"])

    def test_drafts_delegate_paging_and_reject_changed_folder(self):
        with mock.patch.object(server, "_special_mailbox", return_value="Drafts"):
            first = server.list_drafts({})
            second = server.list_drafts({"page_token": first["next_page_token"]})
        self.assertEqual(self.ids(first) + self.ids(second), list(range(125, 105, -1)))
        with mock.patch.object(server, "_special_mailbox", return_value="Renamed Drafts"):
            with self.assertRaisesRegex(ValueError, "page_token"):
                server.list_drafts({"page_token": first["next_page_token"]})

    def test_mailboxes_page_sorted_names_and_count_only_current_page(self):
        folders = [{"name": f"Folder {i:03}", "flags": []} for i in reversed(range(105))]
        self.client.status.return_value = ("OK", [b"(MESSAGES 5 UNSEEN 2)"])
        names = []
        args = {}
        with mock.patch.object(server, "_mailboxes", side_effect=lambda _client: (copy.deepcopy(folders), False)):
            while True:
                result = server.list_mailboxes(args)
                names.extend(item["name"] for item in result["mailboxes"])
                self.assertLessEqual(result["returned"], 10)
                self.assertFalse(result["truncated"])
                if not result["has_more"]:
                    break
                args["page_token"] = result["next_page_token"]
            self.assertEqual(self.client.status.call_count, 105)
            folders.append({"name": "New", "flags": []})
            with self.assertRaisesRegex(ValueError, "stale page_token"):
                server.list_mailboxes(args)
        self.assertEqual(names, [f"Folder {i:03}" for i in range(105)])

    def test_thread_pages_cover_anchor_once_and_detect_discovery_changes(self):
        messages = [{"id": server._encode_ref("INBOX", 7, i), "mailbox": "INBOX", "internet_message_id": f"<{i}@example.com>", "references": ["<1@example.com>"], "date": "Mon, 01 Jan 2024 00:00:00 +0000"} for i in range(1, 26)]
        anchor = messages[-1]
        args = {"message_id": anchor["id"]}
        seen = []
        with mock.patch.object(server, "read_email", return_value=anchor), mock.patch.object(server, "_search_emails", side_effect=lambda *a, **k: {"emails": list(messages), "truncated": False}), mock.patch.object(server, "_read_emails_shared", side_effect=lambda ids, *a: [item for item in messages if item["id"] in ids]):
            while True:
                result = server.read_email_thread(args)
                seen.extend(item["id"] for item in result["messages"])
                self.assertLessEqual(result["returned"], 10)
                if not result["has_more"]:
                    break
                args["page_token"] = result["next_page_token"]
            messages.pop(0)
            with self.assertRaisesRegex(ValueError, "stale page_token"):
                server.read_email_thread(args)
        self.assertEqual(seen, [server._encode_ref("INBOX", 7, i) for i in range(1, 26)])

    def test_thread_output_budget_preserves_continuation(self):
        messages = [{
            "id": server._encode_ref("INBOX", 7, i),
            "mailbox": "INBOX",
            "internet_message_id": f"<{i}@example.com>",
            "references": ["<1@example.com>"],
            "body_text": "x" * 250,
        } for i in range(1, 4)]
        args = {"message_id": messages[0]["id"]}
        seen = []
        with mock.patch.object(server, "read_email", return_value=messages[0]), mock.patch.object(
            server, "_search_emails", return_value={"emails": messages, "truncated": False}
        ), mock.patch.object(
            server, "_read_emails_shared",
            side_effect=lambda ids, *a: [item for item in messages if item["id"] in ids]
        ), mock.patch.object(server, "MAX_THREAD_OUTPUT_BYTES", 1000):
            while True:
                result = server.read_email_thread(args)
                self.assertLessEqual(len(json.dumps(result, ensure_ascii=False).encode()), 1000)
                seen.extend(item["id"] for item in result["messages"])
                if not result["has_more"]:
                    break
                self.assertGreater(result["returned"], 0)
                args["page_token"] = result["next_page_token"]
        self.assertEqual(seen, [item["id"] for item in messages])

    def test_malformed_token_payloads_cannot_change_bounds(self):
        token = server.search_emails({})["next_page_token"]
        payload = json.loads(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
        for value in (True, 0, -1, 1.5, "10", 0x100000000):
            forged = base64.urlsafe_b64encode(json.dumps({**payload, "position": value}).encode()).decode().rstrip("=")
            with self.subTest(position=value), self.assertRaisesRegex(ValueError, "page_token"):
                server.search_emails({"page_token": forged})

    def test_public_mcp_response_serializes_paging(self):
        request = {"id": 1, "method": "tools/call", "params": {
            "name": "search_emails", "arguments": {}
        }}
        response = server.handle(request)["result"]
        self.assertNotIn("isError", response)
        first = json.loads(response["content"][0]["text"])
        request["params"]["arguments"]["page_token"] = first["next_page_token"]
        second = json.loads(server.handle(request)["result"]["content"][0]["text"])
        self.assertEqual(self.ids(first) + self.ids(second), list(range(125, 105, -1)))

    def test_schema_advertises_fixed_paging(self):
        tools = server.handle({"id": 1, "method": "tools/list"})["result"]["tools"]
        for tool in tools:
            if tool["name"] in {"search_emails", "list_drafts", "list_mailboxes", "read_email_thread"}:
                self.assertIn("page_token", tool["inputSchema"]["properties"])
                self.assertNotIn("max_results", tool["inputSchema"]["properties"])


if __name__ == "__main__":
    unittest.main()
