"""macOS Keychain access without putting credentials in process arguments."""
import ctypes as C
import sys


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
