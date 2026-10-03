"""macOS Keychain access without putting credentials in process arguments."""
import ctypes as C
import json
import os
from pathlib import Path
import subprocess
import sys


class KeychainReader:
    """Keep potentially interactive native reads outside the MCP process."""

    def __init__(self, service="codex-icloud-mail", timeout=10.0):
        self.service = service
        self.timeout = timeout

    def get(self, account):
        try:
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--read"],
                input=json.dumps({"service": self.service, "account": account}),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=self.timeout,
                check=False,
                env={key: value for key, value in os.environ.items()
                     if key != "ICLOUD_MAIL_APP_PASSWORD"},
            )
            if result.returncode != 0:
                raise RuntimeError("macOS Keychain could not retrieve the credential")
            password = json.loads(result.stdout)
            if password is not None and not isinstance(password, str):
                raise ValueError("Invalid credential response")
            return password
        except (OSError, subprocess.SubprocessError, ValueError):
            # subprocess.run kills and reaps the helper after a timeout. Never
            # include exception text: it can contain captured credential bytes.
            raise RuntimeError("macOS Keychain could not retrieve the credential") from None


class Keychain:
    def __init__(self, service="codex-icloud-mail"):
        if sys.platform != "darwin":
            raise RuntimeError("The connection page requires macOS Keychain")
        self.service = service.encode()
        self.sec = C.CDLL("/System/Library/Frameworks/Security.framework/Security")
        self.cf = C.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        self.cf.CFRelease.argtypes = [C.c_void_p]
        signatures = {
            "SecKeychainFindGenericPassword": [C.c_void_p, C.c_uint32, C.c_char_p, C.c_uint32, C.c_char_p, C.POINTER(C.c_uint32), C.POINTER(C.c_void_p), C.POINTER(C.c_void_p)],
            "SecKeychainAddGenericPassword": [C.c_void_p, C.c_uint32, C.c_char_p, C.c_uint32, C.c_char_p, C.c_uint32, C.c_void_p, C.POINTER(C.c_void_p)],
            "SecKeychainItemModifyAttributesAndData": [C.c_void_p, C.c_void_p, C.c_uint32, C.c_void_p],
            "SecKeychainItemFreeContent": [C.c_void_p, C.c_void_p],
            "SecKeychainItemDelete": [C.c_void_p],
        }
        for name, args in signatures.items():
            fn = getattr(self.sec, name)
            fn.argtypes, fn.restype = args, C.c_int32

    @staticmethod
    def _check(status):
        if status:
            raise RuntimeError("macOS Keychain could not save or retrieve the credential")

    def _find(self, account):
        account = account.encode()
        size, data, item = C.c_uint32(), C.c_void_p(), C.c_void_p()
        status = self.sec.SecKeychainFindGenericPassword(None, len(self.service), self.service, len(account), account, C.byref(size), C.byref(data), C.byref(item))
        if status == -25300:
            return None, None
        self._check(status)
        try:
            password = C.string_at(data, size.value).decode()
        except Exception:
            if item:
                self.cf.CFRelease(item)
            raise RuntimeError("macOS Keychain contains an invalid credential") from None
        finally:
            self.sec.SecKeychainItemFreeContent(None, data)
        return password, item

    def get(self, account):
        password, item = self._find(account)
        if item:
            self.cf.CFRelease(item)
        return password

    def set(self, account, password):
        _, item = self._find(account)
        raw, encoded = password.encode(), account.encode()
        try:
            if item:
                self._check(self.sec.SecKeychainItemModifyAttributesAndData(item, None, len(raw), raw))
            else:
                self._check(self.sec.SecKeychainAddGenericPassword(None, len(self.service), self.service, len(encoded), encoded, len(raw), raw, None))
        finally:
            if item:
                self.cf.CFRelease(item)

    def delete(self, account):
        _, item = self._find(account)
        if item:
            try:
                self._check(self.sec.SecKeychainItemDelete(item))
            finally:
                self.cf.CFRelease(item)


def _read_main():
    """Private stdin/stdout protocol; never called on the MCP transport."""
    try:
        request = json.loads(sys.stdin.read(4097))
        if not isinstance(request, dict) or set(request) != {"account", "service"}:
            return 1
        if any(not isinstance(value, str) or not value or len(value) > 1024
               for value in request.values()):
            return 1
        password = Keychain(request["service"]).get(request["account"])
        sys.stdout.write(json.dumps(password))
        sys.stdout.flush()
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(_read_main() if sys.argv[1:] == ["--read"] else 1)
