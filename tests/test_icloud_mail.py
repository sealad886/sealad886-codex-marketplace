from __future__ import annotations

import importlib.util
import base64
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

    def test_multipart_attachment_payload_is_serialized(self) -> None:
        attachment = EmailMessage()
        attachment.make_mixed()
        nested = EmailMessage()
        nested.set_content("nested payload")
        attachment.attach(nested)
        attachment.add_header(
            "Content-Disposition", "attachment", filename="bundle.mime"
        )
        payload = server._attachment_payload(attachment)
        self.assertIn(b"multipart/mixed", payload)
        self.assertIn(b"nested payload", payload)

    def test_attachment_entries_do_not_descend_into_attached_email(self) -> None:
        nested = EmailMessage()
        nested.set_content("nested body")
        nested.add_attachment(
            b"pdf data",
            maintype="application",
            subtype="pdf",
            filename="inside.pdf",
        )
        outer = EmailMessage()
        outer.set_content("outer body")
        outer.add_attachment(nested, filename="attached.eml")
        entries = server._attachment_entries(outer, "message")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["filename"], "attached.eml")

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

    def test_search_rejects_non_boolean_attachment_filter_before_connecting(self) -> None:
        with mock.patch.object(server, "_imap") as connect:
            with self.assertRaisesRegex(ValueError, "has_attachment must be a boolean"):
                server.search_emails({"has_attachment": "false"})
        connect.assert_not_called()

    def test_non_ascii_mailbox_is_reencoded_for_wire_commands(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        self.assertEqual(server._select(client, "日本語", readonly=True), 7)
        client.select.assert_called_once_with('"&ZeVnLIqe-"', readonly=True)

    def test_select_rejects_missing_and_invalid_uidvalidity(self) -> None:
        for response in ([None], [b"not-a-number"]):
            client = mock.MagicMock()
            client.select.return_value = ("OK", [b"1"])
            client.response.return_value = ("UIDVALIDITY", response)
            with self.subTest(response=response), self.assertRaisesRegex(
                server.MailError, "UIDVALIDITY"
            ):
                server._select(client, "INBOX", readonly=True)

    def test_select_reuses_current_mailbox_on_one_connection(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        self.assertEqual(server._select(client, "INBOX", readonly=True), 7)
        self.assertEqual(server._select(client, "INBOX", readonly=True), 7)
        client.select.assert_called_once()

    def test_non_ascii_search_uses_utf8_charset_and_bytes(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"0"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = ("OK", [b""])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(
            server, "_imap", return_value=context
        ) as connect:
            server.search_emails({"subject": "日本語"})
        connect.assert_called_once_with(socket_timeout=5.0)
        client.uid.assert_called_once_with(
            "search", "UTF-8", b"ALL", b"SUBJECT", b'"\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e"'
        )

    def test_thread_reference_search_caps_search_and_fetch_phases(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"0"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = ("OK", [b""])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_TIMEOUT": "120"}
        ), mock.patch.object(server, "_imap", return_value=context):
            server.search_emails(
                {"_thread_reference_ids": ["<a@example.com>"]}
            )
        self.assertEqual(
            client.sock.settimeout.call_args_list,
            [mock.call(10.0), mock.call(5.0)],
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

    def test_attachment_scan_caps_socket_timeout_and_total_fetches(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1000"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])

        def search_before_timeout(*_args: object) -> tuple[str, list[bytes]]:
            client.sock.settimeout.assert_not_called()
            return (
                "OK",
                [b" ".join(str(index).encode() for index in range(1, 1001))],
            )

        client.uid.side_effect = search_before_timeout
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_TIMEOUT": "120"}
        ), mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(
            server,
            "_fetch_summary",
            return_value={"id": "message", "has_attachments": False},
        ) as fetch:
            result = server.search_emails(
                {"has_attachment": True, "max_results": 50}
            )
        client.sock.settimeout.assert_called_once_with(5.0)
        self.assertEqual(result["scanned"], 80)
        self.assertEqual(fetch.call_count, 80)

    def test_search_skips_a_message_that_vanishes_during_summary_fetch(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"2"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.return_value = ("OK", [b"1 2"])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        surviving = {
            "id": server._encode_ref("INBOX", 7, 1),
            "has_attachments": False,
        }
        with mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server,
            "_fetch_summary",
            side_effect=[
                server.MailError("Message no longer exists in this mailbox"),
                surviving,
            ],
        ):
            result = server.search_emails({"max_results": 2})
        self.assertEqual(result["emails"], [surviving])
        self.assertEqual(result["scanned"], 2)

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

    def test_mailbox_list_parses_nil_delimiter_and_literal_name(self) -> None:
        client = mock.MagicMock()
        client.list.return_value = (
            "OK",
            [(b"(\\HasNoChildren) NIL {11}", b"Project Box")],
        )
        result = server._mailboxes(client)
        self.assertEqual(
            result,
            [{"name": "Project Box", "flags": ["\\HasNoChildren"]}],
        )

    def test_mailbox_counts_remain_unknown_when_status_is_unavailable(self) -> None:
        client = mock.MagicMock()
        client.list.return_value = (
            "OK",
            [b'(\\HasNoChildren) "/" "INBOX"'],
        )
        client.status.return_value = ("NO", None)
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context):
            result = server.list_mailboxes({})
        self.assertIsNone(result["mailboxes"][0]["messages"])
        self.assertIsNone(result["mailboxes"][0]["unread"])

    def test_mailbox_status_enumeration_has_time_and_count_bounds(self) -> None:
        client = mock.MagicMock()
        mailboxes = [
            {"name": f"Folder {index}", "flags": []}
            for index in range(server.MAX_MAILBOX_STATUS + 1)
        ]
        client.status.return_value = ("OK", [b"(MESSAGES 1 UNSEEN 0)"])
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_TIMEOUT": "120"}
        ), mock.patch.object(
            server, "_imap", return_value=context
        ) as connect, mock.patch.object(server, "_mailboxes", return_value=mailboxes):
            result = server.list_mailboxes({})
        connect.assert_called_once_with(socket_timeout=4.0)
        client.sock.settimeout.assert_called_once_with(4.0)
        self.assertEqual(client.status.call_count, server.MAX_MAILBOX_STATUS)
        self.assertIsNone(result["mailboxes"][-1]["messages"])

    def test_search_summary_detects_content_type_name_attachment(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        headers = b"Subject: Legacy attachment\r\n\r\n"
        client.uid.return_value = (
            "OK",
            [
                (
                    b'9 (UID 9 BODYSTRUCTURE ("APPLICATION" "PDF" '
                    b'("NAME" "report.pdf") NIL NIL "BASE64" 100))',
                    headers,
                )
            ],
        )
        result = server._fetch_summary(client, "INBOX", 7, 9)
        self.assertTrue(result["has_attachments"])

    def test_search_summary_does_not_match_attachment_in_content_id(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        headers = b"Subject: No attachment\r\n\r\n"
        client.uid.return_value = (
            "OK",
            [
                (
                    b'9 (UID 9 BODYSTRUCTURE ("TEXT" "PLAIN" '
                    b'NIL "<attachment@example.com>" NIL "7BIT" 10 1))',
                    headers,
                )
            ],
        )
        result = server._fetch_summary(client, "INBOX", 7, 9)
        self.assertFalse(result["has_attachments"])

    def test_bodystructure_description_named_name_is_not_attachment(self) -> None:
        metadata = (
            b'9 (BODYSTRUCTURE ("TEXT" "PLAIN" NIL NIL "NAME" '
            b'"7BIT" 10 1) FLAGS ())'
        )
        self.assertFalse(server._bodystructure_has_attachment(metadata))

    def test_bodystructure_inline_disposition_filename_is_attachment(self) -> None:
        metadata = (
            b'9 (BODYSTRUCTURE ("IMAGE" "PNG" NIL NIL NIL "BASE64" 10 '
            b'NIL ("INLINE" ("FILENAME" "image.png"))) FLAGS ())'
        )
        self.assertTrue(server._bodystructure_has_attachment(metadata))

    def test_bodystructure_extended_filename_parameter_is_attachment(self) -> None:
        for parameter in (b"FILENAME*", b"FILENAME*0*", b"NAME*0"):
            metadata = (
                b'9 (BODYSTRUCTURE ("APPLICATION" "PDF" ('
                + b'"' + parameter + b'" "UTF-8\'\'report.pdf") '
                + b'NIL NIL "BASE64" 10))'
            )
            with self.subTest(parameter=parameter):
                self.assertTrue(server._bodystructure_has_attachment(metadata))

    def test_search_summary_reads_only_the_flags_response_field(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        headers = b"Subject: Flag-like filename\r\n\r\n"
        client.uid.return_value = (
            "OK",
            [
                (
                    b'9 (UID 9 BODYSTRUCTURE ("APPLICATION" "PDF" '
                    b'("NAME" "\\Seen \\Flagged.pdf") NIL NIL "BASE64" 10) FLAGS ())',
                    headers,
                )
            ],
        )
        result = server._fetch_summary(client, "INBOX", 7, 9)
        self.assertTrue(result["unread"])
        self.assertFalse(result["flagged"])

    def test_full_message_fetch_aggregates_separate_flags_metadata(self) -> None:
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        raw = b"Subject: Draft\r\n\r\nbody"
        client.uid.return_value = (
            "OK",
            [(b"9 (UID 9 BODY[] {24}", raw), b" FLAGS (\\Draft))"],
        )
        message, returned_raw, flags = server._fetch_message(
            client, "Drafts", 7, 9
        )
        self.assertEqual(message["Subject"], "Draft")
        self.assertEqual(returned_raw, raw)
        self.assertEqual(flags, "\\Draft")

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
        forward = next(tool for tool in server.TOOLS if tool["name"] == "forward_emails")
        self.assertEqual(forward["inputSchema"]["required"], ["message_ids"])

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

    def test_blank_xdg_config_home_uses_default_config_directory(self) -> None:
        with mock.patch.object(server.sys, "platform", "linux"), mock.patch.dict(
            os.environ, {"XDG_CONFIG_HOME": "   "}, clear=True
        ):
            self.assertEqual(
                server._config_path(),
                Path.home() / ".config" / "codex" / "icloud-mail" / "config.json",
            )

    def test_legacy_imap_username_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "primary@icloud.com",
                "ICLOUD_MAIL_IMAP_USERNAME": "safe\r\nA001 EXPUNGE",
            },
            clear=True,
        ), self.assertRaisesRegex(
            server.MailError, "ICLOUD_MAIL_IMAP_USERNAME"
        ):
            server._load_config()

    def test_keychain_lookup_failure_is_normalized(self) -> None:
        with mock.patch.object(server.sys, "platform", "darwin"), mock.patch.object(
            server.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired("security", 10),
        ), self.assertRaisesRegex(server.MailError, "No app-specific password"):
            server._password("primary@icloud.com")

    def test_decode_header_preserves_value_on_parser_error(self) -> None:
        with mock.patch.object(
            server,
            "decode_header",
            side_effect=email.errors.HeaderParseError("malformed"),
        ):
            self.assertEqual(server._decode_header("Original"), "Original")

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

    def test_outgoing_message_accepts_cc_or_bcc_without_to(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ):
            server.configure_account({"account_address": "primary@icloud.com"})
            cc_only = server._outgoing(
                {
                    "cc": ["copy@example.com"],
                    "subject": "Cc only",
                    "body": "Body",
                }
            )
            bcc_only = server._outgoing(
                {
                    "bcc": ["hidden@example.com"],
                    "subject": "Bcc only",
                    "body": "Body",
                }
            )
        self.assertIsNone(cc_only.get("To"))
        self.assertEqual(cc_only["Cc"], "copy@example.com")
        self.assertIsNone(bcc_only.get("To"))
        self.assertEqual(bcc_only["Bcc"], "hidden@example.com")

    def test_outgoing_message_requires_a_recipient(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ):
            server.configure_account({"account_address": "primary@icloud.com"})
            with self.assertRaisesRegex(ValueError, "at least one"):
                server._outgoing({"subject": "Nobody", "body": "Body"})

    def test_attached_email_is_not_used_as_parent_body(self) -> None:
        nested = EmailMessage()
        nested["Subject"] = "Attached"
        nested.set_content("attached plain text")
        outer = EmailMessage()
        outer.set_content("<p>outer html</p>", subtype="html")
        outer.add_attachment(nested, filename="attached.eml")
        plain, html_body = server._body(outer)
        self.assertEqual(plain, "")
        self.assertIn("outer html", html_body)
        self.assertNotIn("attached plain text", html_body)

    def test_unnamed_attached_email_is_an_attachment_boundary(self) -> None:
        nested = EmailMessage()
        nested["Subject"] = "Forwarded"
        nested.set_content("forwarded plain text")
        outer = EmailMessage()
        outer.set_content("<p>outer html</p>", subtype="html")
        outer.add_attachment(nested)
        attached = list(outer.iter_parts())[-1]
        if "Content-Disposition" in attached:
            del attached["Content-Disposition"]
        plain, html_body = server._body(outer)
        entries = server._attachment_entries(outer, "message")
        self.assertEqual(plain, "")
        self.assertIn("outer html", html_body)
        self.assertNotIn("forwarded plain text", html_body)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["content_type"], "message/rfc822")

    def test_filename_marked_inline_text_is_not_used_as_parent_body(self) -> None:
        outer = EmailMessage()
        outer.set_content("<p>outer html</p>", subtype="html")
        outer.add_attachment(
            "attached plain text",
            subtype="plain",
            filename="notes.txt",
            disposition="inline",
        )
        plain, html_body = server._body(outer)
        self.assertEqual(plain, "")
        self.assertIn("outer html", html_body)
        self.assertNotIn("attached plain text", html_body)

    def test_read_attachment_serializes_attached_email(self) -> None:
        nested = EmailMessage()
        nested["From"] = "alice@example.com"
        nested["Subject"] = "Attached"
        nested.set_content("attached body")
        outer = EmailMessage()
        outer.set_content("outer body")
        outer.add_attachment(nested, filename="attached.eml")
        message_id = server._encode_ref("INBOX", 7, 9)
        attachment_id = server._attachment_entries(outer, message_id)[0][
            "attachment_id"
        ]
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_fetch_message", return_value=(outer, b"", "")
        ):
            result = server.read_attachment(
                {"message_id": message_id, "attachment_id": attachment_id}
            )
        payload = base64.b64decode(result["content_base64"])
        self.assertIn(b"Subject: Attached", payload)
        self.assertIn(b"attached body", payload)

    def test_read_attachment_rejects_guessed_body_part_id(self) -> None:
        outer = EmailMessage()
        outer.set_content("private body")
        message_id = server._encode_ref("INBOX", 7, 9)
        body_token = base64.urlsafe_b64encode(b"0").decode().rstrip("=")
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(
            server, "_fetch_message", return_value=(outer, b"", "")
        ), self.assertRaisesRegex(server.MailError, "not an advertised attachment"):
            server.read_attachment(
                {
                    "message_id": message_id,
                    "attachment_id": f"{message_id}.{body_token}",
                }
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

    def test_draft_validation_uses_case_sensitive_mailbox_identity(self) -> None:
        draft_id = server._encode_ref("drafts", 7, 9)
        client = mock.MagicMock()
        with mock.patch.object(server, "_special_mailbox", return_value="Drafts"):
            with self.assertRaisesRegex(ValueError, "Drafts mailbox"):
                server._validate_draft_ref(client, draft_id)

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
        ) as connect, mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "create_draft", return_value=replacement.copy()
        ) as create:
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
        create.assert_called_once_with(
            {
                "to": ["recipient@example.com"],
                "subject": "Replacement",
                "body": "Body",
            },
            socket_timeout=10.0,
        )
        self.assertEqual(
            connect.call_args_list,
            [mock.call(socket_timeout=10.0), mock.call(socket_timeout=10.0)],
        )

    def test_reply_preparation_caps_imap_phase(self) -> None:
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        reply = EmailMessage()
        with mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server, "_imap", return_value=context
        ) as connect, mock.patch.object(
            server, "_fetch_message", return_value=(reply, b"", "")
        ), mock.patch.object(
            server, "_outgoing", return_value=EmailMessage()
        ):
            server._prepare_outgoing({"reply_message_id": "message"})
        connect.assert_called_once_with(socket_timeout=10.0)

    def test_update_draft_preserves_partial_move_cleanup_receipt(self) -> None:
        old_id = server._encode_ref("Drafts", 7, 9)
        replacement = {"draft_id": "replacement", "status": "created"}
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        partial = {
            "message_id": old_id,
            "destination": "Trash",
            "status": "copied_source_cleanup_failed",
            "retry_move": False,
        }
        with mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "create_draft", return_value=replacement.copy()
        ), mock.patch.object(
            server, "_special_mailbox", return_value="Trash"
        ), mock.patch.object(server, "_move", return_value=partial):
            result = server.update_draft(
                {
                    "draft_id": old_id,
                    "to": ["recipient@example.com"],
                    "subject": "Replacement",
                    "body": "Body",
                }
            )
        self.assertEqual(
            result["old_draft_cleanup"]["status"],
            "copied_source_cleanup_failed",
        )
        self.assertFalse(result["old_draft_cleanup"]["retry_update"])

    def test_send_draft_preserves_partial_move_cleanup_receipt(self) -> None:
        draft_id = server._encode_ref("Drafts", 7, 9)
        message = EmailMessage()
        accepted = {"status": "accepted"}
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        partial = {
            "message_id": draft_id,
            "destination": "Trash",
            "status": "copied_source_cleanup_unconfirmed",
            "retry_move": False,
        }
        with mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "_fetch_message", return_value=(message, b"", "\\Draft")
        ), mock.patch.object(
            server, "_smtp_send", return_value=accepted
        ), mock.patch.object(
            server, "_special_mailbox", return_value="Trash"
        ), mock.patch.object(server, "_move", return_value=partial):
            result = server.send_draft({"draft_id": draft_id})
        self.assertEqual(
            result["draft_cleanup"]["status"],
            "copied_source_cleanup_unconfirmed",
        )
        self.assertFalse(result["draft_cleanup"]["retry_send"])

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
        ), mock.patch.object(
            server, "_imap", return_value=context
        ) as connect, mock.patch.object(
            server, "_special_mailbox", return_value="Drafts"
        ):
            result = server.create_draft({})
        self.assertEqual(result["status"], "created_unresolved")
        self.assertEqual(result["internet_message_id"], "<draft@example.com>")
        self.assertIsNone(result["draft_id"])
        self.assertFalse(result["retry_create"])
        connect.assert_called_once_with(socket_timeout=10.0)

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

    def test_create_draft_reports_unconfirmed_append_without_retry(self) -> None:
        message = EmailMessage()
        message["Message-ID"] = "<draft@example.com>"
        message.set_content("draft")
        client = mock.MagicMock()
        client.append.side_effect = OSError("connection reset")
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(
            server, "_prepare_outgoing", return_value=message
        ), mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_special_mailbox", return_value="Drafts"
        ):
            result = server.create_draft({})
        self.assertEqual(result["status"], "creation_unconfirmed")
        self.assertIsNone(result["draft_id"])
        self.assertFalse(result["retry_create"])
        self.assertIn("Internet Message-ID", result["next_step"])

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

    def test_move_batch_caps_socket_timeout_and_public_batch_size(self) -> None:
        client = mock.MagicMock()
        with mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_TIMEOUT": "120"}
        ), mock.patch.object(
            server,
            "_move",
            return_value={"message_id": "one", "status": "moved"},
        ):
            server._move_batch(client, ["one"], "Archive")
        client.sock.settimeout.assert_called_once_with(25.0)
        for name in ("move_emails", "archive_emails", "trash_emails"):
            tool = next(item for item in server.TOOLS if item["name"] == name)
            self.assertEqual(
                tool["inputSchema"]["properties"]["message_ids"]["maxItems"],
                5,
            )

    def test_move_workflows_bound_imap_session_setup(self) -> None:
        for name, arguments in (
            ("move_emails", {"message_ids": ["one"], "destination": "Folder"}),
            ("archive_emails", {"message_ids": ["one"]}),
            ("trash_emails", {"message_ids": ["one"]}),
        ):
            context = mock.MagicMock()
            context.__enter__.return_value = mock.MagicMock()
            with self.subTest(name=name), mock.patch.object(
                server, "_imap", return_value=context
            ) as connect, mock.patch.object(
                server, "_special_mailbox", return_value=name
            ), mock.patch.object(
                server, "_move_batch", return_value={"results": []}
            ):
                getattr(server, name)(arguments)
            connect.assert_called_once_with(socket_timeout=10.0)

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

    def test_move_copy_fallback_reports_source_marked_deleted(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 9)
        client = mock.MagicMock()
        client.capabilities = ()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"9 (UID 9)"]),
            ("OK", [b"COPY completed"]),
            ("OK", [b"STORE completed"]),
        ]
        result = server._move(client, message_id, "Archive")
        self.assertEqual(result["status"], "copied_and_marked_deleted")
        client.uid.assert_called_with(
            "STORE", "9", "+FLAGS.SILENT", "(\\Deleted)"
        )

    def test_move_copy_fallback_preserves_copy_receipt_on_cleanup_failure(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 9)
        client = mock.MagicMock()
        client.capabilities = ()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"9 (UID 9)"]),
            ("OK", [b"COPY completed"]),
            OSError("connection reset"),
        ]
        result = server._move(client, message_id, "Archive")
        self.assertEqual(result["status"], "copied_source_cleanup_unconfirmed")
        self.assertFalse(result["retry_move"])
        self.assertIn("destination copy exists", result["next_step"])

    def test_move_copy_fallback_reports_lost_copy_response_without_retry(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 9)
        client = mock.MagicMock()
        client.capabilities = ()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"9 (UID 9)"]),
            OSError("connection reset"),
        ]
        result = server._move(client, message_id, "Archive")
        self.assertEqual(result["status"], "copy_unconfirmed")
        self.assertFalse(result["retry_move"])
        self.assertIn("both source and destination", result["next_step"])

    def test_native_move_reports_lost_response_without_retry(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 9)
        client = mock.MagicMock()
        client.capabilities = (b"MOVE",)
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"9 (UID 9)"]),
            OSError("connection reset"),
        ]
        result = server._move(client, message_id, "Archive")
        self.assertEqual(result["status"], "move_unconfirmed")
        self.assertFalse(result["retry_move"])
        self.assertIn("both source and destination", result["next_step"])

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

    def test_flag_batch_caps_socket_timeout_and_public_batch_size(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 1)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"1 (UID 1)"]),
            ("OK", [b"1 (FLAGS (\\Seen))"]),
        ]
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_TIMEOUT": "120"}
        ), mock.patch.object(server, "_imap", return_value=context) as connect:
            server.set_email_flags({"message_ids": [message_id], "read": True})
        connect.assert_called_once_with(socket_timeout=10.0)
        client.sock.settimeout.assert_called_once_with(25.0)
        tool = next(item for item in server.TOOLS if item["name"] == "set_email_flags")
        self.assertEqual(
            tool["inputSchema"]["properties"]["message_ids"]["maxItems"],
            5,
        )

    def test_thread_reference_search_rejects_protocol_line_breaks(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid"):
            server._text(
                "<message@example.com>\r\nA001 EXPUNGE",
                "_thread_reference_ids",
            )

    def test_flag_batch_preserves_receipts_on_transport_failure(self) -> None:
        first = server._encode_ref("INBOX", 7, 1)
        second = server._encode_ref("INBOX", 7, 2)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"2"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"1 (UID 1)"]),
            ("OK", [b"1 (FLAGS (\\Seen))"]),
            OSError("connection reset"),
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

    def test_flag_receipt_preserves_success_before_transport_failure(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 1)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"1 (UID 1)"]),
            ("OK", [b"1 (FLAGS (\\Seen))"]),
            OSError("connection reset"),
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
        self.assertEqual(receipt["changes"]["flagged"]["status"], "unconfirmed")
        self.assertIn("connection reset", receipt["error"])

    def test_flag_receipt_marks_first_store_transport_failure_unconfirmed(self) -> None:
        message_id = server._encode_ref("INBOX", 7, 1)
        client = mock.MagicMock()
        client.select.return_value = ("OK", [b"1"])
        client.response.return_value = ("UIDVALIDITY", [b"7"])
        client.uid.side_effect = [
            ("OK", [b"1 (UID 1)"]),
            OSError("connection reset"),
        ]
        context = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.object(server, "_imap", return_value=context):
            result = server.set_email_flags(
                {"message_ids": [message_id], "read": True}
            )
        receipt = result["results"][0]
        self.assertEqual(receipt["status"], "unconfirmed")
        self.assertEqual(receipt["changes"]["read"]["status"], "unconfirmed")

    def test_list_drafts_bounds_both_imap_sessions(self) -> None:
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", return_value=context
        ) as connect, mock.patch.object(
            server, "_special_mailbox", return_value="Drafts"
        ), mock.patch.object(
            server, "search_emails", return_value={"emails": [], "truncated": False}
        ) as search:
            result = server.list_drafts({"max_results": 5})
        self.assertEqual(result, {"emails": [], "truncated": False})
        connect.assert_called_once_with(socket_timeout=10.0)
        search.assert_called_once_with(
            {"mailbox": "Drafts", "max_results": 5}, socket_timeout=10.0
        )

    def test_flag_update_rejects_non_boolean_values_before_connecting(self) -> None:
        with mock.patch.object(server, "_imap") as connect:
            with self.assertRaisesRegex(ValueError, "read must be a boolean"):
                server.set_email_flags(
                    {"message_ids": ["message"], "read": "true"}
                )
        connect.assert_not_called()

    def test_forward_returns_receipt_and_formats_sender_with_one_fetch(self) -> None:
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
            "_read_email_result",
            return_value=original,
        ), mock.patch.object(
            server, "_prepare_outgoing", return_value=forwarded
        ) as prepare, mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server, "_imap", return_value=context
        ) as connect, mock.patch.object(
            server, "_fetch_message", return_value=(source, b"", "")
        ) as fetch, mock.patch.object(
            server,
            "_smtp_send",
            return_value={"status": "accepted", "internet_message_id": "<sent>"},
        ):
            result = server.forward_emails(
                {
                    "message_ids": ["first"],
                    "to": ["recipient@example.com"],
                }
            )
        self.assertEqual(result["results"][0]["status"], "accepted")
        self.assertEqual(result["results"][0]["source_message_id"], "first")
        self.assertIn(
            "From: Alice <alice@example.com>",
            prepare.call_args.args[0]["body"],
        )
        fetch.assert_called_once()
        connect.assert_called_once_with(socket_timeout=10.0)

    def test_forward_rejects_multiple_sources_before_connecting(self) -> None:
        with mock.patch.object(server, "_imap") as connect:
            with self.assertRaisesRegex(ValueError, "at most 1"):
                server.forward_emails(
                    {
                        "message_ids": ["first", "second"],
                        "to": ["recipient@example.com"],
                    }
                )
        connect.assert_not_called()

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
        with mock.patch.object(server, "_read_email_result", return_value=original), mock.patch.object(
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

    def test_forwarding_serializes_attached_email_once(self) -> None:
        original = {
            "subject": "Attached mail",
            "from": [{"name": "", "address": "alice@example.com"}],
            "date": "Thu, 31 Jul 2026 09:00:00 +0000",
            "body_text": "x" * server.MAX_BODY_CHARS,
            "body_html": "",
        }
        nested = EmailMessage()
        nested["Subject"] = "Nested"
        nested.set_content("nested body")
        source = EmailMessage()
        source.set_content("outer body")
        source.add_attachment(nested, filename="nested.eml")
        outgoing = EmailMessage()
        outgoing.set_content("forward")
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_read_email_result", return_value=original
        ), mock.patch.object(
            server, "_prepare_outgoing", return_value=outgoing
        ) as prepare, mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(
            server, "_fetch_message", return_value=(source, b"", "")
        ), mock.patch.object(
            server,
            "_smtp_send",
            return_value={"status": "accepted"},
        ):
            result = server.forward_emails(
                {"message_ids": ["source"], "to": ["recipient@example.com"]}
            )
        self.assertEqual(result["results"][0]["status"], "accepted")
        attachments = list(outgoing.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_content_type(), "application/octet-stream")
        self.assertIn(b"Subject: Nested", server._attachment_payload(attachments[0]))
        self.assertLessEqual(
            len(prepare.call_args.args[0]["body"]), server.MAX_BODY_CHARS
        )

    def test_html_only_forward_content_is_converted_to_text(self) -> None:
        self.assertEqual(
            server._html_to_text("<p>Hello &amp; welcome</p><div>Next</div>"),
            "Hello & welcome\nNext",
        )

    def test_forward_wraps_serialized_multipart_attachment_as_binary(self) -> None:
        original = {
            "subject": "Source",
            "from": [],
            "date": "",
            "body_text": "Body",
            "body_html": "",
        }
        multipart_attachment = EmailMessage()
        multipart_attachment.make_mixed()
        nested = EmailMessage()
        nested.set_content("nested payload")
        multipart_attachment.attach(nested)
        multipart_attachment.add_header(
            "Content-Disposition", "attachment", filename="bundle.mime"
        )
        source = EmailMessage()
        source.set_content("outer")
        source.make_mixed()
        source.attach(multipart_attachment)
        outgoing = EmailMessage()
        outgoing.set_content("forward")
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_read_email_result", return_value=original
        ), mock.patch.object(
            server, "_prepare_outgoing", return_value=outgoing
        ), mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(
            server, "_fetch_message", return_value=(source, b"", "")
        ), mock.patch.object(
            server, "_smtp_send", return_value={"status": "accepted"}
        ):
            server.forward_emails(
                {"message_ids": ["source"], "to": ["recipient@example.com"]}
            )
        attachments = list(outgoing.iter_attachments())
        self.assertEqual(attachments[0].get_content_type(), "application/octet-stream")
        self.assertIn(b"nested payload", server._attachment_payload(attachments[0]))

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
        ), mock.patch.object(
            server,
            "_read_emails_shared",
            side_effect=lambda ids: [messages[item] for item in ids],
        ):
            result = server.read_email_thread(
                {"message_id": "anchor", "max_results": 20}
            )
        self.assertEqual(
            {message["id"] for message in result["messages"]},
            {"anchor", "related"},
        )

    def test_thread_read_splits_multiple_in_reply_to_message_ids(self) -> None:
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
            "references": [],
            "in_reply_to": "<anchor@example.com> <other@example.com>",
        }
        messages = {"anchor": anchor, "related": related}
        with mock.patch.object(
            server, "read_email", side_effect=lambda args: messages[args["message_id"]]
        ), mock.patch.object(
            server,
            "search_emails",
            return_value={"emails": [related, anchor], "truncated": False},
        ), mock.patch.object(
            server,
            "_read_emails_shared",
            side_effect=lambda ids: [messages[item] for item in ids],
        ):
            result = server.read_email_thread({"message_id": "anchor"})
        self.assertEqual(
            {message["id"] for message in result["messages"]},
            {"anchor", "related"},
        )

    def test_thread_read_connects_siblings_through_missing_parent(self) -> None:
        anchor = {
            "id": "anchor",
            "mailbox": "INBOX",
            "subject": "Re: Project",
            "internet_message_id": "<anchor@example.com>",
            "references": ["<missing-parent@example.com>"],
            "in_reply_to": "<missing-parent@example.com>",
        }
        sibling = {
            "id": "sibling",
            "mailbox": "INBOX",
            "subject": "Re: Project",
            "internet_message_id": "<sibling@example.com>",
            "references": ["<missing-parent@example.com>"],
            "in_reply_to": "<missing-parent@example.com>",
        }
        with mock.patch.object(
            server, "read_email", return_value=anchor
        ), mock.patch.object(
            server,
            "search_emails",
            return_value={"emails": [sibling, anchor], "truncated": False},
        ), mock.patch.object(
            server, "_read_emails_shared", return_value=[sibling]
        ):
            result = server.read_email_thread({"message_id": "anchor"})
        self.assertEqual(
            {message["id"] for message in result["messages"]},
            {"anchor", "sibling"},
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
        unrelated = {
            **anchor,
            "id": "unrelated",
            "internet_message_id": "<unrelated@example.com>",
        }
        with mock.patch.object(
            server, "read_email", return_value=anchor
        ), mock.patch.object(
            server,
            "search_emails",
            return_value={"emails": [unrelated, anchor], "truncated": False},
        ) as search, mock.patch.object(
            server, "_read_emails_shared", return_value=[]
        ):
            result = server.read_email_thread({"message_id": "anchor"})
        self.assertEqual(result["messages"], [anchor])
        self.assertNotIn("subject", search.call_args.args[0])

    def test_thread_read_finds_linked_reply_with_changed_subject(self) -> None:
        anchor = {
            "id": "anchor",
            "mailbox": "INBOX",
            "subject": "Original",
            "internet_message_id": "<anchor@example.com>",
            "references": [],
            "in_reply_to": "",
        }
        reply = {
            "id": "reply",
            "mailbox": "INBOX",
            "subject": "Completely changed",
            "internet_message_id": "<reply@example.com>",
            "references": ["<anchor@example.com>"],
            "in_reply_to": "<anchor@example.com>",
        }
        with mock.patch.object(
            server, "read_email", return_value=anchor
        ), mock.patch.object(
            server,
            "search_emails",
            return_value={"emails": [reply, anchor], "truncated": False},
        ) as search, mock.patch.object(
            server, "_read_emails_shared", return_value=[reply]
        ):
            result = server.read_email_thread({"message_id": "anchor"})
        self.assertEqual(
            {message["id"] for message in result["messages"]},
            {"anchor", "reply"},
        )
        self.assertNotIn("subject", search.call_args.args[0])
        self.assertEqual(
            search.call_args_list[0].args[0]["_thread_reference_ids"],
            ["<anchor@example.com>"],
        )

    def test_thread_discovery_expands_one_in_reply_to_generation(self) -> None:
        anchor = {
            "id": "a",
            "mailbox": "INBOX",
            "subject": "Thread",
            "internet_message_id": "<a@example.com>",
            "references": [],
            "in_reply_to": "",
        }
        reply_b = {
            **anchor,
            "id": "b",
            "internet_message_id": "<b@example.com>",
            "references": ["<a@example.com>"],
        }
        reply_c = {
            **anchor,
            "id": "c",
            "internet_message_id": "<c@example.com>",
            "in_reply_to": "<b@example.com>",
        }
        with mock.patch.object(
            server, "read_email", return_value=anchor
        ), mock.patch.object(
            server,
            "search_emails",
            side_effect=[
                {"emails": [anchor, reply_b], "truncated": False},
                {"emails": [reply_b, reply_c], "truncated": False},
            ],
        ) as search, mock.patch.object(
            server, "_read_emails_shared", return_value=[reply_b, reply_c]
        ):
            result = server.read_email_thread({"message_id": "a"})
        self.assertEqual(
            {item["id"] for item in result["messages"]}, {"a", "b", "c"}
        )
        self.assertEqual(
            search.call_args_list[1].args[0]["_thread_reference_ids"],
            ["<b@example.com>"],
        )

    def test_thread_reports_truncation_when_second_wave_seeds_are_capped(self) -> None:
        anchor = {
            "id": "anchor",
            "mailbox": "INBOX",
            "subject": "Thread",
            "internet_message_id": "<anchor@example.com>",
            "references": [f"<parent-{index}@example.com>" for index in range(4)],
            "in_reply_to": "",
        }
        replies = [
            {
                **anchor,
                "id": f"reply-{index}",
                "internet_message_id": f"<reply-{index}@example.com>",
                "references": ["<anchor@example.com>"],
            }
            for index in range(6)
        ]
        with mock.patch.object(
            server, "read_email", return_value=anchor
        ), mock.patch.object(
            server,
            "search_emails",
            side_effect=[
                {"emails": replies, "truncated": False},
                {"emails": [], "truncated": False},
            ],
        ) as search, mock.patch.object(
            server, "_read_emails_shared", return_value=replies
        ):
            result = server.read_email_thread({"message_id": "anchor"})
        self.assertTrue(result["truncated"])
        self.assertEqual(
            len(search.call_args_list[1].args[0]["_thread_reference_ids"]), 5
        )

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
        ), mock.patch.object(
            server,
            "_read_emails_shared",
            side_effect=lambda ids: [messages[item] for item in ids],
        ):
            result = server.read_email_thread(
                {"message_id": anchor["id"], "max_results": 20}
            )
        self.assertEqual(len(result["messages"]), 20)
        self.assertIn(anchor, result["messages"])
        self.assertTrue(result["truncated"])

    def test_selected_thread_messages_share_one_imap_session(self) -> None:
        context = mock.MagicMock()
        client = mock.MagicMock()
        context.__enter__.return_value = client
        with mock.patch.dict(
            os.environ, {"ICLOUD_MAIL_TIMEOUT": "120"}
        ), mock.patch.object(server, "_imap", return_value=context) as connect, mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server, "_fetch_message", return_value=(EmailMessage(), b"", "")
        ), mock.patch.object(
            server,
            "_read_email_result",
            side_effect=lambda _message, _raw, _flags, message_id, _mailbox: {
                "id": message_id
            },
        ):
            result = server._read_emails_shared(["first", "second"])
        self.assertEqual(result, [{"id": "first"}, {"id": "second"}])
        connect.assert_called_once_with()
        client.sock.settimeout.assert_called_once_with(8.0)

    def test_shared_thread_fetch_skips_vanished_non_anchor_message(self) -> None:
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        message = EmailMessage()
        with mock.patch.object(server, "_imap", return_value=context), mock.patch.object(
            server, "_decode_ref", return_value=("INBOX", 7, 9)
        ), mock.patch.object(
            server,
            "_fetch_message",
            side_effect=[
                server.MailError("Message no longer exists in this mailbox"),
                (message, b"", ""),
            ],
        ), mock.patch.object(
            server,
            "_read_email_result",
            return_value={"id": "surviving"},
        ):
            result = server._read_emails_shared(["vanished", "surviving"])
        self.assertEqual(result, [{"id": "surviving"}])

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

    def test_keychain_helper_requires_configuration_before_opening(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, self.config_environment(
            temporary
        ), mock.patch.object(server.sys, "platform", "darwin"), mock.patch.object(
            server.subprocess, "run"
        ) as run:
            with self.assertRaisesRegex(server.MailError, "not configured"):
                server.open_keychain_access({})
        run.assert_not_called()

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
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(
            server.smtplib, "SMTP", return_value=smtp
        ) as smtp_class:
            result = server._smtp_send(message)

        sent = smtp.send_message.call_args.args[0]
        self.assertIsNone(sent.get("Bcc"))
        self.assertEqual(result["recipients"], ["to@example.com", "hidden@example.com"])
        smtp_class.assert_called_once_with(
            server.SMTP_HOST, server.SMTP_PORT, timeout=15.0
        )

    def test_smtp_rejects_more_than_twenty_recipients(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = ", ".join(
            f"person{index}@example.com"
            for index in range(server.MAX_RECIPIENTS + 1)
        )
        message.set_content("body")
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), self.assertRaisesRegex(ValueError, "at most 20 recipients"):
            server._smtp_send(message)

    def test_smtp_acceptance_survives_quit_failure(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.send_message.return_value = {}
        smtp.quit.side_effect = server.smtplib.SMTPServerDisconnected("closed")
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            result = server._smtp_send(message)
        self.assertEqual(result["status"], "accepted")
        self.assertFalse(result["retry_send"])
        self.assertIn("cleanup failed", result["cleanup_warning"])

    def test_smtp_data_disconnect_returns_unconfirmed_without_retry(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.getreply.return_value = (354, b"continue")

        def lose_final_response(_payload: bytes) -> None:
            smtp.getreply()
            smtp.send(b"wire")
            raise server.smtplib.SMTPServerDisconnected("connection reset")

        smtp.data.side_effect = lose_final_response
        smtp.send_message.side_effect = lambda *_args, **_kwargs: smtp.data(b"wire")
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            result = server._smtp_send(message)
        self.assertEqual(result["status"], "acceptance_unconfirmed")
        self.assertFalse(result["retry_send"])
        self.assertIn("Check Sent Mail", result["next_step"])

    def test_smtp_partial_payload_write_is_a_definite_failure(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.getreply.return_value = (354, b"continue")
        smtp.send.side_effect = server.smtplib.SMTPServerDisconnected("partial")

        def lose_during_payload(_payload: bytes) -> None:
            smtp.getreply()
            smtp.send(b"partial wire")

        smtp.data.side_effect = lose_during_payload
        smtp.send_message.side_effect = lambda *_args, **_kwargs: smtp.data(b"wire")
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(
            server.smtplib, "SMTP", return_value=smtp
        ), self.assertRaisesRegex(server.MailError, "SMTPServerDisconnected"):
            server._smtp_send(message)

    def test_smtp_rejection_survives_rset_disconnect(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.data.return_value = (550, b"rejected")

        def reject_then_disconnect(*_args: object, **_kwargs: object) -> None:
            smtp.data(b"wire")
            raise server.smtplib.SMTPServerDisconnected("RSET failed")

        smtp.send_message.side_effect = reject_then_disconnect
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(
            server.smtplib, "SMTP", return_value=smtp
        ), self.assertRaisesRegex(server.MailError, "SMTPDataError"):
            server._smtp_send(message)

    def test_smtp_disconnect_before_data_payload_is_a_definite_failure(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.getreply.side_effect = server.smtplib.SMTPServerDisconnected(
            "connection reset"
        )
        smtp.data.side_effect = lambda _payload: smtp.getreply()
        smtp.send_message.side_effect = lambda *_args, **_kwargs: smtp.data(b"wire")
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            with self.assertRaisesRegex(server.MailError, "rejected"):
                server._smtp_send(message)

    def test_smtp_disconnect_before_data_is_a_definite_failure(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "to@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.send_message.side_effect = server.smtplib.SMTPServerDisconnected(
            "connection reset"
        )
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            with self.assertRaisesRegex(server.MailError, "rejected"):
                server._smtp_send(message)

    def test_smtp_partial_recipient_acceptance_is_explicit(self) -> None:
        message = EmailMessage()
        message["From"] = "me@icloud.com"
        message["To"] = "accepted@example.com, refused@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.send_message.return_value = {
            "refused@example.com": (550, b"rejected")
        }
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            result = server._smtp_send(message)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["retry_recipients"], ["refused@example.com"])
        self.assertFalse(result["retry_send"])

    def test_smtp_authorizes_normalized_sender_domain(self) -> None:
        message = EmailMessage()
        message["From"] = "me@iCloud.com"
        message["To"] = "to@example.com"
        message["Subject"] = "Test"
        message["Message-ID"] = "<test@icloud.com>"
        message.set_content("body")
        smtp = mock.MagicMock()
        smtp.send_message.return_value = {}
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
                "ICLOUD_MAIL_USERNAME": "me@icloud.com",
                "ICLOUD_MAIL_APP_PASSWORD": "secret",
            },
            clear=True,
        ), mock.patch.object(server.smtplib, "SMTP", return_value=smtp):
            result = server._smtp_send(message)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["from"], "me@icloud.com")

    def test_send_draft_preserves_draft_after_partial_smtp_acceptance(self) -> None:
        draft_id = server._encode_ref("Drafts", 7, 9)
        message = EmailMessage()
        context = mock.MagicMock()
        context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", return_value=context
        ), mock.patch.object(server, "_validate_draft_ref"), mock.patch.object(
            server, "_fetch_message", return_value=(message, b"", "\\Draft")
        ), mock.patch.object(
            server,
            "_smtp_send",
            return_value={"status": "partial", "retry_send": False},
        ), mock.patch.object(server, "_move") as move:
            result = server.send_draft({"draft_id": draft_id})
        self.assertEqual(result["draft_cleanup"]["status"], "preserved")
        move.assert_not_called()

    def test_send_draft_reuses_message_fetched_during_validation(self) -> None:
        draft_id = server._encode_ref("Drafts", 7, 9)
        message = EmailMessage()
        message["Date"] = "Thu, 01 Jan 1970 00:00:00 +0000"
        first_context = mock.MagicMock()
        first_context.__enter__.return_value = mock.MagicMock()
        with mock.patch.object(
            server, "_imap", side_effect=[first_context, server.MailError("offline")]
        ) as connect, mock.patch.object(
            server, "_validate_draft_ref", return_value=message
        ), mock.patch.object(
            server, "_fetch_message"
        ) as fetch, mock.patch.object(
            server, "_smtp_send", return_value={"status": "accepted"}
        ):
            result = server.send_draft({"draft_id": draft_id})
        self.assertEqual(result["status"], "accepted")
        self.assertNotEqual(message["Date"], "Thu, 01 Jan 1970 00:00:00 +0000")
        self.assertEqual(
            connect.call_args_list,
            [mock.call(socket_timeout=10.0), mock.call(socket_timeout=10.0)],
        )
        fetch.assert_not_called()

    def test_tool_errors_do_not_disclose_secret(self) -> None:
        secret = "do-not-leak"
        with tempfile.TemporaryDirectory() as temporary, mock.patch.dict(
            os.environ,
            {
                "ICLOUD_MAIL_CONFIG_PATH": str(Path(temporary) / "config.json"),
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
