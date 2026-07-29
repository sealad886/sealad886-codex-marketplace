#!/usr/bin/env python3
"""Dependency-free MCP planner and result validator for Conversation Visuals."""

from __future__ import annotations

import ipaddress
import json
import sys
from typing import Any
from urllib.parse import urlparse


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
    if not isinstance(value, str) or len(value) > 4096:
        return False
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    if parsed.username or parsed.password:
        return False
    hostname = parsed.hostname
    if not hostname or hostname.lower() == "localhost":
        return False
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return True
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def plan_visual(arguments: dict[str, Any]) -> dict[str, Any]:
    intent = str(arguments.get("intent", "explain")).strip()[:80] or "explain"
    explicit = bool(arguments.get("explicit", False))
    utility = arguments.get("utility", "medium")
    preference = arguments.get("preference", "automatic")
    if preference not in PREFERENCES:
        raise ValueError(f"unsupported preference: {preference}")
    if utility not in {"low", "medium", "high"}:
        raise ValueError(f"unsupported utility: {utility}")
    requested_kind = arguments.get("requested_kind")
    if requested_kind is not None and requested_kind not in VISUAL_KINDS:
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
        consent_required = kind == "video" or (
            expensive and preference == "suggest-first" and not explicit
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
    provenance = arguments.get("provenance")
    if provenance not in {"sourced", "generated", "mixed"}:
        raise ValueError("provenance must be sourced, generated, or mixed")
    title = str(arguments.get("title", "")).strip()
    alt_text = str(arguments.get("alt_text", "")).strip()
    if not title or len(title) > 200:
        raise ValueError("title must contain 1 to 200 characters")
    if not alt_text or len(alt_text) > 2000:
        raise ValueError("alt_text must contain 1 to 2000 characters")

    media_url = arguments.get("media_url")
    if media_url is not None and not public_http_url(media_url):
        raise ValueError("media_url must be a public HTTP(S) URL without credentials")
    sources = arguments.get("sources", [])
    if not isinstance(sources, list) or len(sources) > 10:
        raise ValueError("sources must be an array with at most 10 entries")
    normalized_sources = []
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        source_title = str(source.get("title", "")).strip()
        source_url = source.get("url")
        if not source_title or not public_http_url(source_url):
            raise ValueError("each source needs a title and public HTTP(S) URL")
        normalized_sources.append(
            {
                "title": source_title[:300],
                "url": source_url,
                "publisher": str(source.get("publisher", "")).strip()[:200] or None,
                "license": str(source.get("license", "unknown")).strip()[:200]
                or "unknown",
                "retrieved_at": str(source.get("retrieved_at", "")).strip()[:80]
                or None,
            }
        )
    if provenance in {"sourced", "mixed"} and not normalized_sources:
        raise ValueError("sourced and mixed visuals require an originating source")

    disclosure = str(arguments.get("generation_disclosure", "")).strip()
    if provenance in {"generated", "mixed"} and not disclosure:
        raise ValueError("generated and mixed visuals require a generation disclosure")

    kind = arguments.get("kind", "source-image")
    if kind not in VISUAL_KINDS:
        raise ValueError(f"unsupported kind: {kind}")
    warnings = arguments.get("warnings", [])
    if not isinstance(warnings, list):
        raise ValueError("warnings must be an array")

    return {
        "kind": kind,
        "provenance": provenance,
        "title": title,
        "summary": str(arguments.get("summary", "")).strip()[:1000],
        "alt_text": alt_text,
        "media_url": media_url,
        "sources": normalized_sources,
        "generation": {
            "generated": provenance in {"generated", "mixed"},
            "disclosure": disclosure or None,
        },
        "warnings": [str(item)[:500] for item in warnings[:10]],
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
            "properties": {
                "kind": {
                    "type": "string",
                    "enum": sorted(VISUAL_KINDS),
                    "default": "source-image",
                },
                "provenance": {
                    "type": "string",
                    "enum": ["sourced", "generated", "mixed"],
                },
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "alt_text": {"type": "string"},
                "media_url": {"type": "string"},
                "sources": {"type": "array", "items": {"type": "object"}},
                "generation_disclosure": {"type": "string"},
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
    if not isinstance(method, str):
        return error_response(request_id, -32600, "Invalid Request: method is required")
    if method == "notifications/initialized":
        return None
    if method == "initialize":
        params = request.get("params", {})
        if not isinstance(params, dict):
            return error_response(
                request_id,
                -32602,
                "Invalid params: expected an object",
            )
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = request.get("params", {})
        if not isinstance(params, dict):
            return error_response(
                request_id,
                -32602,
                "Invalid params: expected an object",
            )
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            return error_response(
                request_id,
                -32602,
                "Invalid params: arguments must be an object",
            )
        try:
            if params.get("name") == "plan_visual":
                result = result_content(plan_visual(arguments))
            elif params.get("name") == "normalize_visual":
                result = result_content(normalize_visual(arguments))
            else:
                raise ValueError(f"unknown tool: {params.get('name')}")
        except (TypeError, ValueError) as error:
            result = result_content({"error": str(error)}, is_error=True)
    elif method == "ping":
        result = {}
    else:
        return error_response(request_id, -32601, f"Method not found: {method}")
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def self_test() -> None:
    assert plan_visual({"utility": "low"})["disposition"] == "no-visual"
    assert plan_visual({"explicit": True, "requested_kind": "video"})[
        "consent_required"
    ]
    sourced = normalize_visual(
        {
            "provenance": "sourced",
            "title": "Example",
            "alt_text": "An example visual.",
            "sources": [{"title": "Origin", "url": "https://example.com/item"}],
        }
    )
    assert sourced["sources"][0]["license"] == "unknown"
    assert not public_http_url("http://127.0.0.1/private")
    print("PASS conversation-visuals MCP self-test")


def main() -> int:
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return 0
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle(request)
        except (UnicodeError, json.JSONDecodeError) as error:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {error}"},
            }
        except Exception:
            request_id = request.get("id") if isinstance(request, dict) else None
            response = error_response(request_id, -32603, "Internal error")
        if response is not None:
            print(json.dumps(response, separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
