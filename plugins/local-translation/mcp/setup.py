"""Bundled, network-free settings surface for MCP App hosts."""

from pathlib import Path


RESOURCE_URI = "ui://local-translation/settings"
RESOURCE_MIME = "text/html;profile=mcp-app"


def resource_descriptor():
    return {"uri": RESOURCE_URI, "name": "Local Translation settings",
            "description": "Configure the local inference engine inside the app.",
            "mimeType": RESOURCE_MIME}


def read_resource():
    """Read only the package-owned form; no caller-selected paths or network."""
    return {**resource_descriptor(),
            "text": Path(__file__).with_name("setup.html").read_text(encoding="utf-8"),
            "_meta": {"ui": {"csp": {"connectDomains": [], "resourceDomains": []},
                               "prefersBorder": True}}}


def open_settings():
    """Return a safe receipt; the host presents the associated MCP App."""
    return {"settings_ui": "in_app",
            "instruction": "Configure local inference in the in-app form. You can also open it from this plugin's settings. This client needs MCP Apps support to display the form."}


def read_settings():
    """Native settings contain a modal action, with no plaintext secret field."""
    return {"schema": {"type": "object", "properties": {}}, "values": {},
            "layout": [{"kind": "group", "title": "Local inference", "items": [
                {"kind": "tool", "tool": "translation_open_settings",
                 "description": "Set the local engine address, model and optional API key in an in-app popup."}]}]}
