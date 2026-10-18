from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from email.message import EmailMessage
from pathlib import Path
from unittest import mock


SERVER = Path(__file__).parents[1] / "plugins/icloud-mail/mcp/server.py"
SPEC = importlib.util.spec_from_file_location("icloud_mail_html_security", SERVER)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class HtmlConversionSecurityTests(unittest.TestCase):
    def test_malformed_html_finishes_through_read_and_forward(self) -> None:
        # Exercise real callers in a killable process; the old regexes take
        # quadratic time on these finite inputs. No provider is contacted.
        code = r'''
import importlib.util, sys
from email.message import EmailMessage
from unittest import mock
spec = importlib.util.spec_from_file_location("mail", sys.argv[1])
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
message = EmailMessage()
if sys.argv[2] in {"read", "thread"}:
    message.set_content("Introduction")
    message.make_mixed()
    child = EmailMessage()
    child.set_content("<" * 300_000, subtype="html")
    message.attach(child)
else:
    message.set_content("<script>" * 12_000, subtype="html")
message_id = server._encode_ref("INBOX", 7, 9)
with mock.patch.object(server, "_imap"), mock.patch.object(
    server, "_fetch_message", return_value=(message, message.as_bytes(), "")
), mock.patch.object(server, "_prepare_outgoing", return_value=EmailMessage()), mock.patch.object(
    server, "_smtp_send", return_value={"status": "accepted"}
):
    if sys.argv[2] in {"read", "thread"}:
        if sys.argv[2] == "thread":
            result = server.read_email_thread({"message_id": message_id})["messages"][0]
        else:
            result = server.read_email({"message_id": message_id})
        assert result["body_text"].startswith("Introduction")
        assert result["body_text_truncated"]
    else:
        result = server.forward_emails({"message_ids": [message_id], "to": ["reader@example.com"]})
        assert result["results"][0]["status"] == "accepted", result
'''
        for action in ("read", "thread", "forward"):
            with self.subTest(action=action):
                try:
                    result = subprocess.run(
                        [sys.executable, "-c", code, str(SERVER), action],
                        capture_output=True, text=True, timeout=5, check=False,
                    )
                except subprocess.TimeoutExpired:
                    self.fail(f"{action} did not finish bounded HTML conversion")
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_quotes_comments_and_raw_text_do_not_leak_markup(self) -> None:
        markup = (
            '<p title="one > zero">Hello &amp; café</p>'
            '<!-- private > comment --><SCRIPT>secret</scripture>still secret</SCRIPT>'
            '<style>hidden</style><div>Next<br />line</div>'
        )
        self.assertEqual(server._html_to_text(markup), "Hello & café\nNext\nline")

    def test_unclosed_script_and_style_suppress_remaining_raw_text(self) -> None:
        for tag in ("script", "style"):
            with self.subTest(tag=tag):
                self.assertEqual(
                    server._html_to_text(f"<p>Visible</p><{tag}>hidden < text"),
                    "Visible",
                )

    def test_conversion_rejects_input_outside_message_budget(self) -> None:
        with mock.patch.object(server, "MAX_MESSAGE_BYTES", 1024):
            with self.assertRaises(server.MailError):
                server._html_to_text("x" * 1025)

    def test_conversion_observes_operation_deadline(self) -> None:
        deadline = server.OperationDeadline(seconds=0, clock=lambda: 0)
        token = server._ACTIVE_DEADLINE.set(deadline)
        try:
            with self.assertRaises(server.OperationTimeout):
                server._html_to_text("<p>Visible</p>")
        finally:
            server._ACTIVE_DEADLINE.reset(token)

    def test_mixed_body_keeps_tail_after_large_html_whitespace(self) -> None:
        message = EmailMessage()
        message.set_content("Introduction")
        message.make_mixed()
        child = EmailMessage()
        child.set_content("<p>" + " " * 100_100 + "Important tail</p>", subtype="html")
        message.attach(child)
        text, _ = server._message_bodies(message)
        self.assertIn("Introduction", text)
        self.assertIn("Important tail", text)


if __name__ == "__main__":
    unittest.main()
