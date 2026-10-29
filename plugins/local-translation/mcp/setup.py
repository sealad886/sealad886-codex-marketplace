"""Short-lived loopback browser setup; credentials never cross MCP responses."""

import hmac
import importlib.util
import json
import os
from pathlib import Path
import queue
import secrets
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


def _settings_module():
    name = "_local_translation_settings"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("settings.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


settings = _settings_module()
LIFETIME_SECONDS = 600
MAX_BODY = 65536


class SetupServer(HTTPServer):
    """A single-use page bound to a numeric loopback address.

    Injected validation/probe callbacks make the complete HTTP workflow testable
    without opening a browser or invoking an inference model.
    """

    def __init__(self, validate, verify, lifetime=LIFETIME_SECONDS):
        self.validate, self.verify = validate, verify
        self.token = secrets.token_urlsafe(32)
        self.path = "/" + secrets.token_urlsafe(24)
        self.nonce = secrets.token_urlsafe(24)
        self.deadline = time.monotonic() + min(max(lifetime, .01), LIFETIME_SECONDS)
        self.saved = False
        super().__init__(("127.0.0.1", 0), Handler)
        self.origin = "http://127.0.0.1:%d" % self.server_port
        self.timeout = .2

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(min(5, max(.01, self.deadline - time.monotonic())))
        return connection, address

    def handle_error(self, request, client_address):
        pass  # Never print credential-bearing requests or exception state.

    def run(self):
        while not self.saved and time.monotonic() < self.deadline:
            self.handle_request()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send_error(self, code, message=None, explain=None):
        self.reply(code, {"error": "Invalid setup request"})

    def reply(self, status, payload, *, html=False):
        body = payload.encode("utf-8") if html else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8" if html else "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'nonce-%s'; style-src 'nonce-%s'; connect-src 'self'; form-action 'none'; frame-ancestors 'none'; base-uri 'none'" % (self.server.nonce, self.server.nonce))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def valid(self):
        server = self.server
        return (time.monotonic() < server.deadline and not server.saved
                and self.headers.get_all("Host") == [server.origin.removeprefix("http://")]
                and self.path == server.path)

    def do_GET(self):
        if not self.valid():
            return self.reply(403, {"error": "Setup page expired or invalid"})
        try:
            page = Path(__file__).with_name("setup.html").read_text(encoding="utf-8")
        except OSError:
            return self.reply(500, {"error": "Could not load the setup page. Reinstall the plugin and try again."})
        self.reply(200, page.replace("{{NONCE}}", self.server.nonce), html=True)

    def do_POST(self):
        tokens = self.headers.get_all("X-Setup-Token", [])
        if (not self.valid() or self.headers.get_all("Origin") != [self.server.origin]
                or self.headers.get_all("Content-Type") != ["application/json"]
                or self.headers.get("Transfer-Encoding") is not None or len(tokens) != 1
                or not hmac.compare_digest(tokens[0].encode("utf-8"), self.server.token.encode("utf-8"))):
            return self.reply(403, {"error": "Setup page expired or invalid"})
        lengths = self.headers.get_all("Content-Length", [])
        if len(lengths) != 1 or not lengths[0].isdigit() or not 0 < int(lengths[0]) <= MAX_BODY:
            return self.reply(413, {"error": "Invalid setup request size"})
        try:
            data = settings._decode(self.rfile.read(int(lengths[0])))
            if not isinstance(data, dict):
                raise ValueError()
            if data == {"action": "read"}:
                return self.reply(200, settings.public_settings())
            required = {"action", "root", "deployment", "credential_action", "expected_revision"}
            if data.get("action") != "save" or not required <= set(data) or set(data) - required - {"api_key"}:
                raise ValueError()
            def verify(root, deployment, api_key):
                evidence = self.server.verify(root, deployment, api_key)
                if time.monotonic() >= self.server.deadline:
                    raise settings.SettingsError("page_expired")
                return evidence
            result = settings.save_settings(
                data["root"], data["deployment"], api_key_action=data["credential_action"],
                api_key=data.get("api_key"), expected_revision=data["expected_revision"],
                validate=self.server.validate, verify=verify)
        except settings.SettingsError as error:
            return self.reply(409 if error.code == "stale_configuration" else 400,
                              {"error": str(error), "code": error.code})
        except (ValueError, TypeError, UnicodeError):
            return self.reply(400, {"error": "Enter valid settings. Nothing was saved.", "code": "invalid_input"})
        except Exception as error:
            # Runner callbacks may provide safe, fixed error codes, but never
            # relay arbitrary dependency errors or exception strings.
            code = getattr(error, "code", None)
            messages = {
                "model_unavailable": "The exact model alias is not listed by this engine. Check the served model name. Nothing was saved.",
                "tokenizer_unsupported": "This engine must support POST /tokenize with chat messages and return a positive token count. A chat-only OpenAI endpoint is insufficient. Nothing was saved.",
                "runner_unreachable": "Could not reach this local engine. Start it, check its port and API key, and try again. Nothing was saved.",
            }
            return self.reply(400, {"error": messages.get(code, "The engine check failed. Check its local address, model alias and tokenizer support. Nothing was saved."),
                                    "code": code if code in messages else "verification_failed"})
        self.server.saved = True
        self.reply(200, result)


def open_settings():
    """Open a private page in the system browser, returning a safe receipt only."""
    child = None
    try:
        child = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--serve"],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            start_new_session=True)
        results = queue.Queue(maxsize=1)
        def read_ready():
            try:
                results.put(child.stdout.readline(1024))
            except OSError:
                results.put(b"")
        threading.Thread(target=read_ready, daemon=True).start()
        ready = results.get(timeout=12)
        if ready != b"READY\n":
            raise OSError()
        child.stdout.close()
        threading.Thread(target=child.wait, daemon=True).start()
    except (OSError, subprocess.SubprocessError, queue.Empty):
        if child is not None:
            try:
                child.terminate()
                child.wait(timeout=2)
            except (OSError, subprocess.SubprocessError):
                try:
                    child.kill()
                    child.wait(timeout=2)
                except (OSError, subprocess.SubprocessError):
                    pass
            if child.stdout is not None:
                child.stdout.close()
        raise settings.SettingsError("browser_unavailable") from None
    return {"browser_opened": True, "expires_in_seconds": LIFETIME_SECONDS,
            "instruction": "Complete Local Translation setup in the browser, then call translation_health. No app restart is needed."}


def main():
    # Production imports the sibling runtime only inside the bounded child.
    import server as core
    watchdog = threading.Timer(LIFETIME_SECONDS, lambda: os._exit(0))
    watchdog.daemon = True
    watchdog.start()
    try:
        with SetupServer(core.validate_config, core.verify_deployment) as server:
            if not webbrowser.open(server.origin + server.path + "#" + server.token):
                raise RuntimeError()
            print("READY", flush=True)
            sys.stdout.close()
            server.run()
    except Exception:
        try:
            print("ERROR", flush=True)
        except (OSError, ValueError):
            pass
        return 1
    finally:
        watchdog.cancel()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
