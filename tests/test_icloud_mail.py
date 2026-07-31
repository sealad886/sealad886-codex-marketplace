from __future__ import annotations

import importlib.util
import email
import json
import os
import subprocess
import sys
import tempfile
import unittest
from email.message import EmailMessage
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parents[1]
PLUGIN = ROOT / "plugins" / "icloud-mail"
SERVER = PLUGIN / "mcp" / "server.py"
SPEC = importlib.util.spec_from_file_location("icloud_mail_server", SERVER)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class ICloudMailTests(unittest.TestCase):
    def config_environment(self, root: str) -> mock._patch_dict:
        return mock.patch.dict(
            os.environ,
            {"ICLOUD_MAIL_CONFIG_PATH": str(Path(root) / "config.json")},
            clear=True,
        )

    def test_manifest_and_mcp_identity(self) -> None:
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
        config = json.loads((PLUGIN / ".mcp.json").read_text())
        self.assertEqual(manifest["name"], "icloud-mail")
        self.assertEqual(manifest["version"], server.SERVER_INFO["version"])
        self.assertEqual(config["mcpServers"]["icloud-mail"]["args"], ["./mcp/server.py"])

    def test_self_test_is_offline_and_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SERVER), "--self-test"],
            cwd=PLUGIN,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS icloud-mail MCP self-test")

    def test_message_reference_round_trip_and_rejects_malformed(self) -> None:
        reference = server._encode_ref("Sent Messages", 15, 99)
        self.assertEqual(server._decode_ref(reference), ("Sent Messages", 15, 99))
        for malformed in ("", "icloud-mail:not-base64", "gmail:abc"):
            with self.assertRaises(ValueError):
                server._decode_ref(malformed)
        injected = server._encode_ref("INBOX\r\nA001 EXPUNGE", 15, 99)
        with self.assertRaisesRegex(ValueError, "invalid or too long"):
            server._decode_ref(injected)

    def test_modified_utf7_mailbox_names_decode(self) -> None:
        self.assertEqual(server._decode_imap_utf7(b"Sent Messages"), "Sent Messages")
        self.assertEqual(server._decode_imap_utf7(b"Fish &- Chips"), "Fish & Chips")
        self.assertEqual(server._decode_imap_utf7(b"&ZeVnLIqe-"), "日本語")
        self.assertEqual(server._encode_imap_utf7("Sent Messages"), "Sent Messages")
        self.assertEqual(server._encode_imap_utf7("Fish & Chips"), "Fish &- Chips")
        self.assertEqual(server._encode_imap_utf7("日本語"), "&ZeVnLIqe-")

    def test_imap_search_values_reject_protocol_line_breaks(self) -> None:
        for field in ("query", "from", "to", "subject"):
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "invalid or too long"
            ):
                server.search_emails({field: "safe\r\nA001 EXPUNGE"})

    def test_non_ascii_mailbox_is_reencoded_for_wire_commands(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        self.assertEqual(server._select(client, "日本語", readonly=True), 7)
        client.select.assert_called_once_with('"&ZeVnLIqe-"', readonly=True)

    def test_non_ascii_search_uses_utf8_charset_and_bytes(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"0"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = ("OK", [b""])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context):
            server.search_emails({"subject": "日本語"})
        client.uid.assert_called_once_with(
            "search", "UTF-8", b"ALL", b"SUBJECT", b'"\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e"'
        )

    def test_attachment_filter_has_a_bounded_scan_budget(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1000"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = (
            "OK",
            [b" ".join(str(index).encode() for index in range(1, 1001))],
        )
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server,
            "_fetch_summary",
            side_effect=lambda _client, mailbox, validity, uid: {
                "id": server._encode_ref(mailbox, validity, uid),
                "has_attachments": False,
            },
        ) as fetch:
            result = server.search_emails(
                {"has_attachment": True, "max_results": 1}
            )
        self.assertEqual(result["returned"], 0)
        self.assertEqual(result["scanned"], 50)
        self.assertTrue(result["truncated"])
        self.assertEqual(fetch.call_count, 50)

    def test_search_summary_fetches_headers_without_full_message_body(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        headers = (
            b"Message-ID: <one@example.com>\r\n"
            b"Subject: One\r\n"
            b"From: Alice <alice@example.com>\r\n\r\n"
        )
        client.uid.return_value = (
            "OK",
            [(b'9 (UID 9 FLAGS (\\Seen) BODYSTRUCTURE ("TEXT" "PLAIN"))', headers)],
        )
        result = server._fetch_summary(client, "INBOX", 7, 9)
        self.assertEqual(result["subject"], "One")
        self.assertFalse(result["has_attachments"])
        fetch_arguments = client.uid.call_args.args[2]
        self.assertIn("HEADER.FIELDS", fetch_arguments)
        self.assertNotIn("BODY.PEEK[]", fetch_arguments)

    def test_tools_match_handlers_and_mutations_are_explicit(self) -> None:
        names = {tool["name"] for tool in server.TOOLS}
        self.assertEqual(names, set(server.HANDLERS))
        for required in {
            "search_emails",
            "read_email",
            "read_attachment",
            "create_draft",
            "update_draft",
            "send_email",
            "send_draft",
            "forward_emails",
            "archive_emails",
            "trash_emails",
            "configure_account",
            "validate_account",
            "open_keychain_access",
        }:
            self.assertIn(required, names)
        self.assertNotIn("permanently_delete", names)

    def test_configuration_persists_non_secret_settings_with_private_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ):
            result = server.configure_account(
                {
                    "account_address": "primary@icloud.com",
                    "default_from": "alias@example.com",
                    "allowed_from": (
                        "alias@example.com, primary@icloud.com, alias@example.com"
                    ),
                    "display_name": "Example User",
                }
            )
            path = Path(result["config_path"])
            payload = json.loads(path.read_text())

            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(payload["account_address"], "primary@icloud.com")
            self.assertEqual(payload["allowed_from"], ["alias@example.com"])
            self.assertEqual(payload["default_from"], "alias@example.com")
            self.assertNotIn("password", json.dumps(payload).lower())
            self.assertEqual(server._username(), "primary@icloud.com")

    def test_configuration_does_not_chmod_an_existing_override_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ):
            os.chmod(temporary, 0o755)
            server.configure_account({"account_address": "primary@icloud.com"})
            self.assertEqual(Path(temporary).stat().st_mode & 0o777, 0o755)

    def test_incoming_aliases_are_all_mail_and_sender_aliases_are_restricted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ):
            server.configure_account(
                {
                    "account_address": "primary@icloud.com",
                    "allowed_from": ["allowed@example.com"],
                }
            )
            allowed = server._outgoing(
                {
                    "from": "allowed@example.com",
                    "to": ["recipient@example.com"],
                    "subject": "Allowed",
                    "body": "Body",
                }
            )
            self.assertEqual(
                email.utils.parseaddr(allowed["From"])[1], "allowed@example.com"
            )
            with self.assertRaisesRegex(ValueError, "configured allowed alias"):
                server._outgoing(
                    {
                        "from": "attacker@example.com",
                        "to": ["recipient@example.com"],
                        "subject": "Rejected",
                        "body": "Body",
                    }
                )
            status = server.get_account_status({})
            self.assertEqual(
                status["incoming_alias_scope"], "all aliases in the iCloud mailbox"
            )

    def test_clear_configuration_preserves_keychain_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ):
            server.configure_account({"account_address": "primary@icloud.com"})
            with self.assertRaises(ValueError):
                server.clear_account_configuration({"confirm": False})
            result = server.clear_account_configuration({"confirm": True})
            self.assertTrue(result["configuration_removed"])
            self.assertFalse(result["keychain_credential_removed"])
            self.assertFalse(Path(temporary, "config.json").exists())

    def test_validate_account_authenticates_without_sending(self) -> None:
        imap = mock.MagicMock()
        imap.status.return_value = ("OK", [b"INBOX (MESSAGES 12)"])
        imap_context = mock.MagicMock()
        imap_context.__enter__.return_value = imap
        smtp = mock.MagicMock()
        smtp.__enter__.return_value = smtp
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ), mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_APP_PASSWORD": "secret"}, clear=False
        ), mock.patch.object(server, "_imap", return_value=imap_context), mock.patch.object(
            server.smtplib, "SMTP", return_value=smtp
        ):
            server.configure_account({"account_address": "primary@icloud.com"})
            result = server.validate_account({})

        self.assertTrue(result["imap_authenticated"])
        self.assertTrue(result["smtp_authenticated"])
        self.assertFalse(result["email_sent"])
        self.assertEqual(result["inbox_messages"], 12)
        smtp.login.assert_called_once_with("primary@icloud.com", "secret")
        smtp.send_message.assert_not_called()

    def test_draft_mutations_reject_an_ordinary_message_reference(self) -> None:
        ordinary_id = server._encode_ref("Sent Messages", 7, 9)
        client = mock.MagicMock()
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_special_mailbox", return_value="Drafts"
        ), mock.patch.object(server, "create_draft") as create:
            with self.assertRaisesRegex(ValueError, "Drafts mailbox"):
                server.update_draft(
                    {
                        "draft_id": ordinary_id,
                        "to": ["recipient@example.com"],
                        "subject": "Replacement",
                        "body": "Body",
                    }
                )
            with self.assertRaisesRegex(ValueError, "Drafts mailbox"):
                server.send_draft({"draft_id": ordinary_id})
        create.assert_not_called()

    def test_send_draft_preserves_acceptance_when_cleanup_fails(self) -> None:
        draft_id = server._encode_ref("Drafts", 7, 9)
        message = EmailMessage()
        accepted = {"status": "accepted", "internet_message_id": "<sent@example.com>"}
        first_context = mock.MagicMock()
        first_context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", side_effect=[first_context, server.MailError("offline")]
        ), mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "_fetch_message", return_value=(message, b"", "\\Draft")
        ), mock.patch.object(
            server, "_smtp_send", return_value=accepted.copy()
        ):
            result = server.send_draft({"draft_id": draft_id})
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["draft_cleanup"]["status"], "failed")
        self.assertFalse(result["draft_cleanup"]["retry_send"])

    def test_update_draft_preserves_replacement_when_cleanup_fails(self) -> None:
        old_id = server._encode_ref("Drafts", 7, 9)
        replacement = {"draft_id": "replacement", "status": "created"}
        validate_context = mock.MagicMock()
        validate_context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", side_effect=[validate_context, server.MailError("offline")]
        ), mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "create_draft", return_value=replacement.copy()
        ):
            result = server.update_draft(
                {
                    "draft_id": old_id,
                    "to": ["recipient@example.com"],
                    "subject": "Replacement",
                    "body": "Body",
                }
            )
        self.assertEqual(result["draft_id"], "replacement")
        self.assertEqual(result["old_draft_cleanup"]["status"], "failed")
        self.assertFalse(result["old_draft_cleanup"]["retry_update"])

    def test_update_draft_preserves_old_draft_when_replacement_is_unresolved(self) -> None:
        old_id = server._encode_ref("Drafts", 7, 9)
        unresolved = {
            "draft_id": None,
            "internet_message_id": "<replacement@example.com>",
            "status": "created_unresolved",
            "retry_create": False,
        }
        validate_context = mock.MagicMock()
        validate_context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", return_value=validate_context
        ), mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "create_draft", return_value=unresolved.copy()
        ), mock.patch.object(server, "_move") as move:
            result = server.update_draft(
                {
                    "draft_id": old_id,
                    "to": ["recipient@example.com"],
                    "subject": "Replacement",
                    "body": "Body",
                }
            )
        self.assertEqual(result["status"], "created_unresolved")
        self.assertEqual(result["old_draft_cleanup"]["status"], "preserved")
        move.assert_not_called()

    def test_create_draft_preserves_append_receipt_when_id_recovery_fails(self) -> None:
        message = EmailMessage()
        message["Message-ID"] = "<draft@example.com>"
        message.set_content("draft")
        client = mock.MagicMock()
        client.append.return_value = ("OK", [b"APPEND completed"])
        client.response.side_effect = [
            ("APPENDUID", None),
            ("UIDVALIDITY", None),
        ]
        client.select.return_value = ("OK", [b"1"])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(
            server, "_prepare_outgoing", return_value=message
        ), mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_special_mailbox", return_value="Drafts"
        ):
            result = server.create_draft({})
        self.assertEqual(result["status"], "created_unresolved")
        self.assertEqual(result["internet_message_id"], "<draft@example.com>")
        self.assertIsNone(result["draft_id"])
        self.assertFalse(result["retry_create"])

    def test_create_draft_preserves_receipt_on_raw_imap_recovery_error(self) -> None:
        message = EmailMessage()
        message["Message-ID"] = "<draft@example.com>"
        message.set_content("draft")
        client = mock.MagicMock()
        client.append.return_value = ("OK", [b"APPEND completed"])
        client.response.return_value = ("APPENDUID", None)
        client.select.side_effect = OSError("connection reset")
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(
            server, "_prepare_outgoing", return_value=message
        ), mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_special_mailbox", return_value="Drafts"
        ):
            result = server.create_draft({})
        self.assertEqual(result["status"], "created_unresolved")
        self.assertFalse(result["retry_create"])

    def test_batch_moves_return_completed_and_failed_receipts(self) -> None:
        client = mock.MagicMock()
        with mock.patch.object(
            server,
            "_move",
            side_effect=[
                {"message_id": "first", "destination": "Archive", "status": "moved"},
                server.MailError("stale"),
            ],
        ):
            result = server._move_batch(client, ["first", "second"], "Archive")
        self.assertEqual(result["results"][0]["status"], "moved")
        self.assertEqual(result["results"][1]["status"], "failed")
        self.assertEqual(result["results"][1]["message_id"], "second")

    def test_batch_moves_preserve_receipts_on_transport_failure(self) -> None:
        client = mock.MagicMock()
        with mock.patch.object(
            server,
            "_move",
            side_effect=[
                {"message_id": "first", "destination": "Archive", "status": "moved"},
                OSError("connection reset"),
            ],
        ):
            result = server._move_batch(client, ["first", "second"], "Archive")
        self.assertEqual(result["results"][0]["status"], "moved")
        self.assertEqual(result["results"][1]["status"], "failed")

    def test_move_rejects_a_missing_source_uid_even_when_imap_returns_ok(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 9)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"0"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = ("OK", [None])
        with self.assertRaisesRegex(server.MailError, "no longer exists"):
            server._move(client, message_id, "Archive")

    def test_flag_update_rejects_a_missing_source_uid(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 9)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"0"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = ("OK", [None])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context):
            result = server.set_email_flags(
                {"message_ids": [message_id], "read": True}
            )
        self.assertEqual(result["results"][0]["status"], "failed")
        self.assertIn("no longer exists", result["results"][0]["error"])

    def test_flag_batch_preserves_earlier_success_receipts(self) -> None:
        first = server._encode_ref("INBOX", 7, 1)
        second = server._encode_ref("INBOX", 7, 2)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"2"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"1 (UID 1)"]),
            ("OK", [b"1 (FLAGS (\\Seen))"]),
            ("OK", [None]),
        ]
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context):
            result = server.set_email_flags(
                {"message_ids": [first, second], "read": True}
            )
        self.assertEqual(result["results"][0]["status"], "updated")
        self.assertEqual(result["results"][1]["status"], "failed")

    def test_flag_receipt_reports_partial_per_flag_outcome(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 1)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"1 (UID 1)"]),
            ("OK", [b"1 (FLAGS (\\Seen))"]),
            ("NO", [b"flag update rejected"]),
        ]
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context):
            result = server.set_email_flags(
                {"message_ids": [message_id], "read": True, "flagged": True}
            )
        receipt = result["results"][0]
        self.assertEqual(receipt["status"], "partial")
        self.assertEqual(receipt["changes"]["read"]["status"], "updated")
        self.assertEqual(receipt["changes"]["flagged"]["status"], "failed")

    def test_batch_forward_returns_receipts_and_formats_sender(self) -> None:
        original = {
            "subject": "Status",
            "from": [{"name": "Alice", "address": "alice@example.com"}],
            "date": "Thu, 31 Jul 2026 09:00:00 +0000",
            "body_text": "Original",
        }
        forwarded = EmailMessage()
        forwarded.set_content("forward")
        source = EmailMessage()
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server,
            "read_email",
            side_effect=[original, server.MailError("missing message")],
        ), mock.patch.object(
            server, "_prepare_outgoing", return_value=forwarded
        ) as prepare, mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(
            server, "_fetch_message", return_value=(source, b"", "")
        ), mock.patch.object(
            server,
            "_smtp_send",
            return_value={"status": "accepted", "internet_message_id": "<sent>"},
        ):
            result = server.forward_emails(
                {
                    "message_ids": ["first", "second"],
                    "to": ["recipient@example.com"],
                }
            )
        self.assertEqual(result["results"][0]["status"], "accepted")
        self.assertEqual(result["results"][0]["source_message_id"], "first")
        self.assertEqual(result["results"][1]["status"], "failed")
        self.assertEqual(result["results"][1]["source_message_id"], "second")
        self.assertIn(
            "From: Alice <alice@example.com>",
            prepare.call_args.args[0]["body"],
        )

    def test_forwarding_enforces_aggregate_attachment_limit(self) -> None:
        original = {
            "subject": "Files",
            "from": [{"name": "", "address": "alice@example.com"}],
            "date": "Thu, 31 Jul 2026 09:00:00 +0000",
            "body_text": "Files",
            "body_html": "",
        }
        source = EmailMessage()
        source.set_content("body")
        for index in range(3):
            source.add_attachment(
                b"x" * (4 * 1024 * 1024),
                maintype="application",
                subtype="octet-stream",
                filename=f"file-{index}.bin",
            )
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(server, "read_email", return_value=original), mock.patch.object(
            server, "_prepare_outgoing", return_value=EmailMessage()
        ), mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_fetch_message", return_value=(source, b"", "")
        ), mock.patch.object(server, "_smtp_send") as send:
            result = server.forward_emails(
                {"message_ids": ["source"], "to": ["recipient@example.com"]}
            )
        self.assertEqual(result["results"][0]["status"], "failed")
        self.assertIn("10 MiB total", result["results"][0]["error"])
        send.assert_not_called()

    def test_html_only_forward_content_is_converted_to_text(self) -> None:
        self.assertEqual(
            server._html_to_text("<p>Hello &amp; welcome</p><div>Next</div>"),
            "Hello & welcome\nNext",
        )

    def test_thread_read_filters_same_subject_messages_by_reference_headers(self) -> None:
        anchor = {
            "id": "anchor",
            "mailbox": "INBOX",
            "subject": "Status",
            "internet_message_id": "<anchor@example.com>",
            "references": [],
            "in_reply_to": "",
        }
        related = {
            "id": "related",
            "mailbox": "INBOX",
            "subject": "Re: Status",
            "internet_message_id": "<related@example.com>",
            "references": ["<anchor@example.com>"],
            "in_reply_to": "<anchor@example.com>",
        }
        unrelated = {
            "id": "unrelated",
            "mailbox": "INBOX",
            "subject": "Status",
            "internet_message_id": "<other@example.com>",
            "references": [],
            "in_reply_to": "",
        }
        messages = {"anchor": anchor, "related": related, "unrelated": unrelated}
        with mock.patch.object(
            server, "read_email", side_effect=lambda args: messages[args["message_id"]]
        ), mock.patch.object(
            server,
            "search_emails",
            return_value={
                "emails": [unrelated, related, anchor],
                "truncated": False,
            },
        ):
            result = server.read_email_thread(
                {"message_id": "anchor", "max_results": 20}
            )
        self.assertEqual(
            {message["id"] for message in result["messages"]},
            {"anchor", "related"},
        )

    def test_empty_subject_thread_returns_only_anchor(self) -> None:
        anchor = {
            "id": "anchor",
            "mailbox": "INBOX",
            "subject": "",
            "internet_message_id": "<anchor@example.com>",
            "references": [],
            "in_reply_to": "",
        }
        with mock.patch.object(server, "read_email", return_value=anchor), mock.patch.object(
            server, "search_emails"
        ) as search:
            result = server.read_email_thread({"message_id": "anchor"})
        self.assertEqual(result["messages"], [anchor])
        search.assert_not_called()

    def test_truncated_thread_always_includes_requested_anchor(self) -> None:
        def message(index: int) -> dict[str, object]:
            return {
                "id": f"message-{index}",
                "mailbox": "INBOX",
                "subject": "Status",
                "internet_message_id": f"<message-{index}@example.com>",
                "references": (
                    [] if index == 0 else [f"<message-{index - 1}@example.com>"]
                ),
                "in_reply_to": (
                    "" if index == 0 else f"<message-{index - 1}@example.com>"
                ),
            }

        messages = {item["id"]: item for item in (message(i) for i in range(25))}
        anchor = messages["message-24"]
        search_results = [messages[f"message-{index}"] for index in reversed(range(25))]
        with mock.patch.object(
            server, "read_email", side_effect=lambda args: messages[args["message_id"]]
        ), mock.patch.object(
            server,
            "search_emails",
            return_value={"emails": search_results, "truncated": False},
        ):
            result = server.read_email_thread(
                {"message_id": anchor["id"], "max_results": 20}
            )
        self.assertEqual(len(result["messages"]), 20)
        self.assertIn(anchor, result["messages"])
        self.assertTrue(result["truncated"])

    def test_gui_helpers_open_only_fixed_targets(self) -> None:
        completed = mock.MagicMock(returncode=0)
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ), mock.patch.object(server.sys, "platform", "darwin"), mock.patch.object(
            server.subprocess, "run", return_value=completed
        ) as run:
            server.configure_account({"account_address": "primary@icloud.com"})
            apple = server.open_apple_password_page({})
            keychain = server.open_keychain_access({})

        self.assertEqual(apple["target"], "Apple Account")
        self.assertEqual(
            keychain["instructions"]["keychain_item_name"], "codex-icloud-mail"
        )
        self.assertEqual(
            keychain["instructions"]["account_name"], "primary@icloud.com"
        )
        calls = [call.args[0] for call in run.call_args_list]
        self.assertEqual(
            calls[0],
            ["/usr/bin/open", "https://account.apple.com/account/manage"],
        )
        self.assertEqual(
            calls[1],
            [
                "/usr/bin/open",
                "/System/Applications/Utilities/Keychain Access.app",
            ],
        )

    def test_bcc_is_removed_from_wire_copy(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message["Bcc"] = "hidden@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")

        smtp = mock.MagicMock()
        smtp.__enter__.return_value = smtp
        with mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            result = server._smtp_send(message)

        sent = smtp.send_message.call_args.args[0]
        self.assertIsNone(sent.get("Bcc"))
        self.assertEqual(result["recipients"], ["to@example.com", "hidden@example.com"])

    def test_tool_errors_do_not_disclose_secret(self) -> None:
        secret = "do-not-leak"
        with mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": secret,
            },
            clear=True,
        ), mock.patch.object(
            server.smtplib,
            "SMTP",
            side_effect=server.smtplib.SMTPAuthenticationError(535, b"rejected"),
        ):
            response = server.handle(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "send_email",
                        "arguments": {
                            "to": ["to@example.com"],
                            "subject": "Test",
                            "body": "Body",
                        },
                    },
                }
            )
        rendered = json.dumps(response)
        self.assertNotIn(secret, rendered)
        self.assertIn("SMTPAuthenticationError", rendered)


if __name__ == "__main__":
    unittest.main()
