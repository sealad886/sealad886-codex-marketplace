#!/usr/bin/env python3
"""Private user-run onboarding via the issuer's OAuth device authorization flow.

Never run this interactively on behalf of a user, capture its terminal, or pass
credentials through an agent. No tokens/passwords are persisted on the client.
"""
from __future__ import annotations

import argparse
import getpass
import time
from urllib.parse import urlsplit
import webbrowser

import httpx2 as httpx


def https(value):
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("An HTTPS URL without credentials, query or fragment is required")
    return value


def authorize(client, issuer, client_id, resource):
    metadata = client.get(issuer.rstrip("/") + "/.well-known/openid-configuration").raise_for_status().json()
    if metadata["issuer"] != issuer:
        raise ValueError("Issuer discovery mismatch")
    device_url = https(metadata["device_authorization_endpoint"])
    token_url = https(metadata["token_endpoint"])
    device = client.post(device_url, data={"client_id": client_id, "scope": "mail:read mail:configure",
        "resource": resource}).raise_for_status().json()
    verification = https(device["verification_uri"])
    print("Open", verification, "and enter this one-time code:", device["user_code"])
    webbrowser.open(verification)
    expires = time.monotonic() + min(int(device["expires_in"]), 600)
    interval = max(int(device.get("interval", 5)), 5)
    while time.monotonic() < expires:
        time.sleep(interval)
        response = client.post(token_url, data={"grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device["device_code"], "client_id": client_id, "resource": resource})
        token = response.json()
        if response.is_success and str(token.get("token_type", "")).lower() == "bearer":
            return token["access_token"]
        if token.get("error") == "slow_down":
            interval += 5
        elif token.get("error") != "authorization_pending":
            raise ValueError("Authorization declined or unavailable")
    raise ValueError("Authorization expired; run setup again")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issuer", required=True, type=https)
    parser.add_argument("--client-id", required=True, help="Operator-registered public OAuth device client ID")
    parser.add_argument("--resource", required=True, type=https, help="Approved service HTTPS URL ending in /mcp")
    parser.add_argument("--disconnect", action="store_true")
    args = parser.parse_args()
    resource = urlsplit(args.resource)
    if resource.path != "/mcp":
        parser.error("Resource must end in /mcp")
    try:
        # No redirects: never forward credentials to a redirected service. No
        # inherited HTTP proxy: the user must use a direct trusted TLS connection.
        with httpx.Client(timeout=15, follow_redirects=False, trust_env=False) as client:
            token = authorize(client, args.issuer, args.client_id, args.resource)
            headers = {"Authorization": "Bearer " + token}
            endpoint = "https://" + resource.netloc + "/account"
            if args.disconnect:
                response = client.delete(endpoint, headers=headers)
            else:
                account = input("Primary iCloud mailbox address: ").strip()
                password = getpass.getpass("Apple app-specific password (never your Apple Account password): ")
                response = client.put(endpoint, headers=headers, timeout=60, json={"account_address": account, "app_password": password})
            response.raise_for_status()
            print("Disconnected; revoke the app-specific password at Apple as well." if args.disconnect else "Connected for read-only access. Configure your MCP client's OAuth connection separately.")
    except (Exception, KeyboardInterrupt):
        # Provider errors can echo secrets. Never print response bodies/tracebacks.
        parser.exit(1, "Private setup did not finish. Check service/issuer configuration or try again.\n")


if __name__ == "__main__":
    main()
