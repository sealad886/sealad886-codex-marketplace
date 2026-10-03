"""Mail operations must not persist content or emit it to diagnostic streams."""
import base64
import contextlib
import io
import json
import os
import tempfile
import unittest
from email.message import EmailMessage
from pathlib import Path
from unittest import mock
from test_icloud_mail import server


class MailPrivacyTests(unittest.TestCase):
    def test_requested_mail_remains_in_memory_and_remote_drafts(self):
        marker = 'PRIVATE-MAIL-SENTINEL-7e953'
        message = EmailMessage()
        message['Subject'] = marker
        message['From'] = 'sender@example.invalid'
        message['To'] = 'reader@icloud.com'
        message['Message-ID'] = '<synthetic@example.invalid>'
        message.set_content(marker)
        message.add_attachment(marker.encode(), maintype='application', subtype='octet-stream', filename='sample.bin')
        raw = message.as_bytes()
        client = mock.MagicMock()
        client.select.return_value = ('OK', [b'1'])
        client.response.side_effect = lambda name: (name, [b'7 9'] if name == 'APPENDUID' else [b'7'])
        def uid(command, *args):
            if command.lower() == 'search':
                return 'OK', [b'9']
            if any('HEADER.FIELDS' in str(arg) for arg in args):
                return 'OK', [(b'9 (UID 9 FLAGS () BODYSTRUCTURE ("TEXT" "PLAIN"))', raw.split(b'\n\n', 1)[0] + b'\n\n')]
            return 'OK', [(b'9 (UID 9 FLAGS () RFC822.SIZE ' + str(len(raw)).encode() + b')', raw)]
        client.uid.side_effect = uid
        client.append.return_value = ('OK', [b'complete'])
        session = mock.MagicMock()
        session.__enter__.return_value = client
        output, errors = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(os.environ, {'ICLOUD_MAIL_CONFIG_PATH': str(Path(directory) / 'config.json')}, clear=True):
            server.configure_account({'account_address': 'reader@icloud.com'})
            before = {p.name: p.read_bytes() for p in Path(directory).iterdir()}
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.object(server, '_imap', return_value=session))
                stack.enter_context(mock.patch.object(server, '_special_mailbox', return_value='Drafts'))
                stack.enter_context(contextlib.redirect_stdout(output))
                stack.enter_context(contextlib.redirect_stderr(errors))
                # Operation-time filesystem creation/writes are forbidden. Config reads remain allowed.
                real_open = os.open
                def checked_open(path, flags, *args, **kwargs):
                    if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                        raise AssertionError('Mail operation attempted filesystem write')
                    return real_open(path, flags, *args, **kwargs)
                stack.enter_context(mock.patch('os.open', side_effect=checked_open))
                real_io_open = io.open
                def checked_io(file, mode='r', *args, **kwargs):
                    if any(flag in mode for flag in 'wax+'):
                        raise AssertionError('Mail operation attempted file write')
                    return real_io_open(file, mode, *args, **kwargs)
                stack.enter_context(mock.patch('io.open', side_effect=checked_io))
                stack.enter_context(mock.patch('builtins.open', side_effect=checked_io))
                search = server.search_emails({'subject': marker})
                self.assertEqual(search['emails'][0]['subject'], marker)
                read = server.read_email({'message_id': search['emails'][0]['id']})
                attachment = server.read_attachment({'message_id': search['emails'][0]['id'], 'attachment_id': read['attachments'][0]['attachment_id']})
                self.assertEqual(base64.b64decode(attachment['content_base64']), marker.encode())
                draft = server.create_draft({'to': ['recipient@example.invalid'], 'subject': marker, 'body': marker})
                self.assertEqual(draft['status'], 'created')
                self.assertIn(marker.encode(), client.append.call_args.args[-1])
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(directory).iterdir()})
            self.assertNotIn(marker, output.getvalue() + errors.getvalue())
            self.assertNotIn(marker, json.dumps({k: v.decode() for k, v in before.items()}))
