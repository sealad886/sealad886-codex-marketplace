#!/usr/bin/env python3
"""Dependency-free MCP planner and result validator for Conversation Visuals."""

from __future__ import annotations

import ipaddress
import json
import socket
import sys
from typing import Any
from urllib.parse import unquote, urlparse


PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "conversation-visuals", "version": "0.1.0"}
VISUAL_KINDS = {
    "source-image",
    "diagram",
    "chart",
    "generated-image",
    "slides",
    "video",
}
PREFERENCES = {"automatic", "suggest-first", "on-request", "quiet"}


def public_http_url(value: Any) -> bool:
    """Apply static URL checks without claiming fetch-time network safety.

    Hostname resolution and redirect validation belong to the approved host
    fetcher because this dependency-free metadata server never fetches URLs.
    """
    if (
        not isinstance(value, str)
        or len(value) > 4096
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        return False
    try:
        parsed = urlparse(value)
        username = parsed.username
        password = parsed.password
        port = parsed.port
        hostname = parsed.hostname
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    if any(character in parsed.netloc for character in "[]"):
        try:
            ipaddress.IPv6Address(hostname)
        except (ipaddress.AddressValueError, ValueError):
            return False
    if username or password:
        return False
    if port is not None and not 1 <= port <= 65535:
        return False
    if parsed.netloc.endswith(":"):
        return False
    try:
        decoded_hostname = unquote(hostname, errors="strict") if hostname else ""
    except UnicodeDecodeError:
        return False
    # Python's standard-library IDNA codec does not implement the contextual
    # validation used by WHATWG URL hosts. Require callers to provide the
    # equivalent ASCII IDNA form so accepted URLs remain usable by Node hosts.
    if "%" in decoded_hostname or not decoded_hostname.isascii():
        return False
    try:
        address = ipaddress.ip_address(decoded_hostname)
    except ValueError:
        address = None
    if address is not None:
        return address.is_global and not address.is_multicast
    if any(
        character in "%:/\\@?#[]<>^|"
        or character.isspace()
        or ord(character) < 32
        or ord(character) == 127
        for character in decoded_hostname
    ):
        return False
    try:
        normalized_hostname = (
            decoded_hostname.encode("idna").decode("ascii").rstrip(".").lower()
        )
    except UnicodeError:
        return False
    if any(
        character in "%:/\\@?#[]<>^|"
        or character.isspace()
        or ord(character) < 32
        or ord(character) == 127
        for character in normalized_hostname
    ):
        return False
    if (
        not normalized_hostname
        or normalized_hostname == "localhost"
        or normalized_hostname.endswith(".localhost")
    ):
        return False
    try:
        address = ipaddress.ip_address(socket.inet_aton(normalized_hostname))
    except OSError:
        final_label = normalized_hostname.rsplit(".", 1)[-1].lower()
        ipv4_number = final_label.isdecimal() or (
            final_label.startswith("0x")
            and len(final_label) > 2
            and all(character in "0123456789abcdef" for character in final_label[2:])
        )
        return not ipv4_number
    return address.is_global and not address.is_multicast


def plan_visual(arguments: dict[str, Any]) -> dict[str, Any]:
    unknown_fields = set(arguments) - {
        "intent",
        "explicit",
        "utility",
        "preference",
        "requested_kind",
    }
    if unknown_fields:
        raise ValueError(f"unsupported plan_visual fields: {sorted(unknown_fields)}")
    intent_value = arguments.get("intent", "explain")
    if not isinstance(intent_value, str):
        raise ValueError("intent must be a string")
    intent = intent_value.strip()[:80] or "explain"
    explicit = arguments.get("explicit", False)
    if not isinstance(explicit, bool):
        raise ValueError("explicit must be a boolean")
    utility = arguments.get("utility", "medium")
    preference = arguments.get("preference", "automatic")
    if not isinstance(preference, str) or preference not in PREFERENCES:
        raise ValueError(f"unsupported preference: {preference}")
    if not isinstance(utility, str) or utility not in {"low", "medium", "high"}:
        raise ValueError(f"unsupported utility: {utility}")
    requested_kind = arguments.get("requested_kind")
    if requested_kind is not None and (
        not isinstance(requested_kind, str) or requested_kind not in VISUAL_KINDS
    ):
        raise ValueError(f"unsupported requested_kind: {requested_kind}")

    if preference == "quiet" and not explicit:
        disposition = "no-visual"
        kind = None
        consent_required = False
        rationale = "Quiet mode suppresses inferred visuals."
    elif preference == "on-request" and not explicit:
        disposition = "no-visual"
        kind = None
        consent_required = False
        rationale = "On-request mode requires an explicit visual request."
    elif utility == "low" and not explicit:
        disposition = "no-visual"
        kind = None
        consent_required = False
        rationale = "The expected explanatory benefit is too small."
    else:
        kind = requested_kind or {
            "locate": "source-image",
            "identify": "source-image",
            "compare": "chart",
            "map": "diagram",
            "present": "slides",
            "narrate": "slides",
        }.get(intent, "diagram")
        expensive = kind in {"generated-image", "slides", "video"}
        consent_required = not explicit and (
            preference == "suggest-first" or expensive
        )
        disposition = "suggest-first" if consent_required else "produce"
        rationale = (
            "Explicit or sufficiently useful visual treatment selected; "
            "the active preference and media cost determine consent."
        )

    return {
        "disposition": disposition,
        "kind": kind,
        "consent_required": consent_required,
        "intent": intent,
        "preference": preference,
        "rationale": rationale,
        "constraints": {
            "max_items": 1,
            "require_alt_text": True,
            "require_source_for_sourced_media": True,
            "require_generation_disclosure": True,
            "minimum_context_only": True,
        },
    }


def normalize_visual(arguments: dict[str, Any]) -> dict[str, Any]:
    unknown_fields = set(arguments) - {
        "kind",
        "provenance",
        "title",
        "summary",
        "alt_text",
        "media_url",
        "artifact_ref",
        "sources",
        "generation_disclosure",
        "warnings",
    }
    if unknown_fields:
        raise ValueError(f"unsupported normalize_visual fields: {sorted(unknown_fields)}")
    provenance = arguments.get("provenance")
    if not isinstance(provenance, str) or provenance not in {
        "sourced",
        "generated",
        "mixed",
    }:
        raise ValueError("provenance must be sourced, generated, or mixed")
    title_value = arguments.get("title")
    alt_text_value = arguments.get("alt_text")
    if not isinstance(title_value, str):
        raise ValueError("title must be a string")
    if not isinstance(alt_text_value, str):
        raise ValueError("alt_text must be a string")
    title = title_value.strip()
    alt_text = alt_text_value.strip()
    if not title or len(title) > 200:
        raise ValueError("title must contain 1 to 200 characters")
    if not alt_text or len(alt_text) > 2000:
        raise ValueError("alt_text must contain 1 to 2000 characters")

    summary_value = arguments.get("summary", "")
    if not isinstance(summary_value, str):
        raise ValueError("summary must be a string")
    summary = summary_value.strip()[:1000]

    media_url = arguments.get("media_url")
    if media_url is not None and not public_http_url(media_url):
        raise ValueError("media_url must be a public HTTP(S) URL without credentials")
    artifact_ref = arguments.get("artifact_ref")
    if artifact_ref is not None and (
        not isinstance(artifact_ref, str)
        or not artifact_ref.strip()
        or len(artifact_ref) > 4096
        or any(
            ord(character) < 32 or ord(character) == 127
            for character in artifact_ref
        )
    ):
        raise ValueError("artifact_ref must be a non-empty host-issued reference")
    sources = arguments.get("sources", [])
    if not isinstance(sources, list) or len(sources) > 10:
        raise ValueError("sources must be an array with at most 10 entries")
    normalized_sources = []
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        source_title_value = source.get("title")
        if not isinstance(source_title_value, str):
            raise ValueError("each source title must be a string")
        source_title = source_title_value.strip()
        source_url = source.get("url")
        if not source_title or not public_http_url(source_url):
            raise ValueError("each source needs a title and public HTTP(S) URL")
        publisher = source.get("publisher", "")
        license_name = source.get("license", "unknown")
        retrieved_at = source.get("retrieved_at", "")
        if not isinstance(publisher, str):
            raise ValueError("source publisher must be a string")
        if not isinstance(license_name, str):
            raise ValueError("source license must be a string")
        if not isinstance(retrieved_at, str):
            raise ValueError("source retrieved_at must be a string")
        normalized_sources.append(
            {
                "title": source_title[:300],
                "url": source_url,
                "publisher": publisher.strip()[:200] or None,
                "license": license_name.strip()[:200] or "unknown",
                "retrieved_at": retrieved_at.strip()[:80] or None,
            }
        )
    if provenance in {"sourced", "mixed"} and not normalized_sources:
        raise ValueError("sourced and mixed visuals require an originating source")

    disclosure_value = arguments.get("generation_disclosure", "")
    if not isinstance(disclosure_value, str):
        raise ValueError("generation_disclosure must be a string")
    disclosure = disclosure_value.strip()
    if len(disclosure) > 2000:
        raise ValueError("generation_disclosure must not exceed 2000 characters")
    if provenance in {"generated", "mixed"} and not disclosure:
        raise ValueError("generated and mixed visuals require a generation disclosure")
    if provenance in {"generated", "mixed"} and not (media_url or artifact_ref):
        raise ValueError("generated and mixed visuals require a media or artifact reference")
    if provenance == "sourced" and not (media_url or artifact_ref):
        raise ValueError("sourced visuals require a media or artifact reference")

    kind = arguments.get("kind")
    if kind is None:
        kind = "source-image" if provenance == "sourced" else "generated-image"
    if not isinstance(kind, str) or kind not in VISUAL_KINDS:
        raise ValueError(f"unsupported kind: {kind}")
    if provenance == "sourced" and kind == "generated-image":
        raise ValueError("sourced provenance cannot use generated-image kind")
    if provenance == "generated" and kind == "source-image":
        raise ValueError("generated provenance cannot use source-image kind")
    warnings = arguments.get("warnings", [])
    if not isinstance(warnings, list):
        raise ValueError("warnings must be an array")
    if not all(isinstance(item, str) for item in warnings):
        raise ValueError("warnings must contain only strings")

    return {
        "kind": kind,
        "provenance": provenance,
        "title": title,
        "summary": summary,
        "alt_text": alt_text,
        "media_url": media_url,
        "artifact_ref": artifact_ref.strip() if artifact_ref is not None else None,
        "sources": normalized_sources,
        "generation": {
            "generated": provenance in {"generated", "mixed"},
            "disclosure": disclosure or None,
        },
        "warnings": [item[:500] for item in warnings[:10]],
    }


TOOLS = [
    {
        "name": "plan_visual",
        "description": "Select the smallest useful visual treatment and whether consent is required. This deterministic tool performs no search, generation, network access, or file writes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "intent": {"type": "string"},
                "explicit": {"type": "boolean", "default": False},
                "utility": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "default": "medium",
                },
                "preference": {
                    "type": "string",
                    "enum": sorted(PREFERENCES),
                    "default": "automatic",
                },
                "requested_kind": {
                    "type": "string",
                    "enum": sorted(VISUAL_KINDS),
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "normalize_visual",
        "description": "Validate and normalize visual provenance, accessibility text, source records, and generated-media disclosure without fetching any URL.",
        "inputSchema": {
            "type": "object",
            "required": ["provenance", "title", "alt_text"],
            "anyOf": [
                {"required": ["media_url"]},
                {"required": ["artifact_ref"]},
            ],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "provenance": {"enum": ["sourced", "mixed"]}
                        },
                        "required": ["provenance"],
                    },
                    "then": {
                        "required": ["sources"],
                        "properties": {"sources": {"minItems": 1}},
                    },
                },
                {
                    "if": {
                        "properties": {
                            "provenance": {"enum": ["generated", "mixed"]}
                        },
                        "required": ["provenance"],
                    },
                    "then": {
                        "required": ["generation_disclosure"],
                        "properties": {
                            "generation_disclosure": {
                                "minLength": 1,
                                "pattern": r"\S",
                            }
                        },
                    },
                },
                {
                    "if": {
                        "properties": {"provenance": {"const": "sourced"}},
                        "required": ["provenance"],
                    },
                    "then": {
                        "properties": {
                            "kind": {
                                "enum": sorted(
                                    VISUAL_KINDS - {"generated-image"}
                                )
                            }
                        }
                    },
                },
                {
                    "if": {
                        "properties": {"provenance": {"const": "generated"}},
                        "required": ["provenance"],
                    },
                    "then": {
                        "properties": {
                            "kind": {
                                "enum": sorted(VISUAL_KINDS - {"source-image"})
                            }
                        }
                    },
                },
            ],
            "properties": {
                "kind": {
                    "type": "string",
                    "enum": sorted(VISUAL_KINDS),
                },
                "provenance": {
                    "type": "string",
                    "enum": ["sourced", "generated", "mixed"],
                },
                "title": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200,
                    "pattern": r"\S",
                },
                "summary": {"type": "string"},
                "alt_text": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000,
                    "pattern": r"\S",
                },
                "media_url": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 4096,
                },
                "artifact_ref": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 4096,
                    "pattern": r"\S",
                    "description": "Opaque host-issued local artifact, attachment, or resource reference. The server records but never dereferences it.",
                },
                "sources": {
                    "type": "array",
                    "maxItems": 10,
                    "items": {
                        "type": "object",
                        "required": ["title", "url"],
                        "properties": {
                            "title": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 300,
                                "pattern": r"\S",
                            },
                            "url": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 4096,
                                "description": "Public HTTP(S) source URL without credentials.",
                            },
                            "publisher": {"type": "string"},
                            "license": {"type": "string"},
                            "retrieved_at": {"type": "string"},
                        },
                    },
                },
                "generation_disclosure": {"type": "string", "maxLength": 2000},
                "warnings": {"type": "array", "items": {"type": "string"}},
            },
            "additionalProperties": False,
        },
    },
]


def result_content(value: dict[str, Any], is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(value, sort_keys=True)}],
        "structuredContent": value,
        "isError": is_error,
    }


def error_response(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def handle(request: Any) -> dict[str, Any] | None:
    if not isinstance(request, dict):
        return error_response(None, -32600, "Invalid Request: expected an object")

    method = request.get("method")
    request_id = request.get("id")
    if request.get("jsonrpc") != "2.0":
        return error_response(None, -32600, "Invalid Request: jsonrpc must be 2.0")
    if "id" in request and (
        isinstance(request_id, bool) or not isinstance(request_id, (str, int))
    ):
        return error_response(
            None,
            -32600,
            "Invalid Request: id must be a string or integer",
        )
    if not isinstance(method, str):
        return error_response(None, -32600, "Invalid Request: method is required")

    is_notification = "id" not in request

    def request_error(code: int, message: str) -> dict[str, Any] | None:
        if is_notification:
            return None
        return error_response(request_id, code, message)

    if "params" in request and not isinstance(request["params"], dict):
        return request_error(-32602, "Invalid params: expected an object")
    if is_notification:
        return None
    if method == "initialize":
        params = request.get("params", {})
        if not isinstance(params, dict):
            return request_error(
                -32602,
                "Invalid params: expected an object",
            )
        protocol_version = params.get("protocolVersion")
        capabilities = params.get("capabilities")
        client_info = params.get("clientInfo")
        if (
            not isinstance(protocol_version, str)
            or not isinstance(capabilities, dict)
            or not isinstance(client_info, dict)
            or not isinstance(client_info.get("name"), str)
            or not isinstance(client_info.get("version"), str)
        ):
            return request_error(
                -32602,
                "Invalid params: initialize requires protocolVersion, capabilities, and clientInfo",
            )
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }
    elif method == "tools/list":
        params = request.get("params", {})
        if "cursor" in params and not isinstance(params["cursor"], str):
            return request_error(-32602, "Invalid params: cursor must be a string")
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = request.get("params", {})
        if not isinstance(params, dict):
            return request_error(
                -32602,
                "Invalid params: expected an object",
            )
        tool_name = params.get("name")
        if tool_name not in {"plan_visual", "normalize_visual"}:
            return request_error(-32602, f"Unknown tool: {tool_name}")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            return request_error(
                -32602,
                "Invalid params: arguments must be an object",
            )
        try:
            if tool_name == "plan_visual":
                result = result_content(plan_visual(arguments))
            else:
                result = result_content(normalize_visual(arguments))
        except (TypeError, ValueError) as error:
            result = result_content({"error": str(error)}, is_error=True)
    elif method == "ping":
        result = {}
    else:
        return request_error(-32601, f"Method not found: {method}")
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def self_test() -> None:
    def check(condition: bool, message: str) -> None:
        if not condition:
            raise RuntimeError(f"self-test failed: {message}")

    check(
        plan_visual({"utility": "low"})["disposition"] == "no-visual",
        "low utility should suppress an inferred visual",
    )
    check(
        not plan_visual({"explicit": True, "requested_kind": "video"})[
            "consent_required"
        ],
        "explicit video requests should not require consent",
    )
    sourced = normalize_visual(
        {
            "provenance": "sourced",
            "title": "Example",
            "alt_text": "An example visual.",
            "media_url": "https://example.com/item.png",
            "sources": [{"title": "Origin", "url": "https://example.com/item"}],
        }
    )
    check(
        sourced["sources"][0]["license"] == "unknown",
        "missing source licenses should normalize to unknown",
    )
    check(
        not public_http_url("http://127.0.0.1/private"),
        "loopback URLs should be rejected",
    )
    print("PASS conversation-visuals MCP self-test")


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def main() -> int:
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return 0
    for line in sys.stdin:
        if not line.strip():
            continue
        request: Any = None
        try:
            request = json.loads(line, parse_constant=reject_json_constant)
        except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {error}"},
            }
        else:
            try:
                response = handle(request)
            except Exception:
                request_id = request.get("id") if isinstance(request, dict) else None
                response = error_response(request_id, -32603, "Internal error")
        if response is not None:
            print(json.dumps(response, separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
