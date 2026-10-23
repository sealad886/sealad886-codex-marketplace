# Remote iCloud Mail (optional operator deployment)

The normal plugin installation continues to start the dependency-free local
stdio server. This package also supplies a **read-only remote server** for an
always-on Linux/macOS host with outbound TLS IMAP access to Apple. Hosting this
server on the same Mac, or tunnelling back to that Mac, does not provide access
when it is offline. No public hosted endpoint is included in this release.

Publishing/installing this package does not deploy a service, connect a mailbox,
create an OAuth grant, or start monitoring. An operator must approve the host,
domain, identity provider, storage, region, costs and support arrangements first.
Do not claim unattended access until an authorized cloud runner has successfully
read a test mailbox through the deployed HTTPS endpoint with the Mac offline.

## Architecture and permissions

`remote.py` uses the pinned official MCP Python SDK's stateless Streamable HTTP
transport and the same `server.py` mail core as local stdio. Each request must
have an OAuth JWT **access token**, signed with RS256, `typ=at+jwt`, and valid
`iss`, `aud`, `sub`, `iat`, `exp`, and space-separated `scope` claims. `nbf`, when
present, is validated. Tokens may live at most one hour. ID tokens, unsigned
tokens, shared API keys and arbitrary issuer discovery from token contents are
rejected. The configured issuer/JWKS URL are operator trust decisions; `jku` and
`x5u` in a token never select a key source. JWT verification uses PyJWT.

Configure an established OAuth/OIDC provider to issue resource-specific tokens
and enforce user consent, login protection, short token lifetimes and grant
revocation. Its issuer metadata and authorization-code-with-PKCE flow must work
with the intended MCP clients (pre-register public clients where necessary).
The private setup CLI additionally requires the provider's device authorization
flow and a registered **public** device client. This implementation is an OAuth
resource server; it does not implement a new authorization server or Apple OAuth.
An arbitrary OIDC provider's default ID token is insufficient.

| Scope | Remote access |
| --- | --- |
| `mail:read` | Required for every operation. Folder/search/message/thread/draft reads. |
| `mail:attachments` | Additionally permits advertised attachment bytes. |
| `mail:watch` | Additionally permits explicitly requested watch scans and completion receipts. |
| `mail:configure` | Additionally permits private HTTP onboarding/disconnection, never MCP credential tools. |

There is no remote mail-write scope in this release. Sending, flagging, moving,
draft mutation, local file attachments, raw MIME, account/GUI tools and SMTP
validation are absent from remote discovery **and** denied at execution. Local
stdio retains all existing tools and its Keychain/environment setup.

The server derives the tenant key from the validated `(issuer, subject)` pair.
Callers cannot provide tenant IDs, mailbox credentials, hostnames or ports as MCP
arguments. Private onboarding verifies possession of the mailbox password against
`imap.mail.me.com:993` with certificate validation before binding that mailbox
to the principal. A principal cannot replace its mailbox address without first
disconnecting. Custom iCloud domains are supported; endpoint selection remains
fixed to Apple. Different users each supply their own credential. The service
never exports or migrates local Keychain items.

## Install and configure on the approved host

Use Python 3.11 or later in a dedicated virtual environment. From the plugin root:

```sh
python3 -m venv /opt/icloud-mail/venv
/opt/icloud-mail/venv/bin/python -m pip install --require-hashes -r mcp/requirements-remote.txt
```

Run under a dedicated non-root service account. Provision a private persistent
data directory (0700) and a separate secret mount holding a Fernet key file
(0600), both owned by that service account. Generate the key using
`cryptography.fernet.Fernet.generate_key()` directly into the approved secret
store; never print it or place it in source, shell arguments, logs, release assets,
tool results or the database volume. The key and database must have different
parent directories. All account settings/passwords and watch payloads are
authenticated-encrypted with Fernet, including their tenant/kind binding.
Database owner/permissions, symlinks and a second service process fail closed.

Provide these **non-secret configuration values** in the service environment:

| Variable | Value |
| --- | --- |
| `ICLOUD_REMOTE_ISSUER` | Exact approved HTTPS issuer (including its canonical trailing slash, if any). |
| `ICLOUD_REMOTE_AUDIENCE` | Dedicated audience configured at that issuer for this API. |
| `ICLOUD_REMOTE_JWKS_URL` | Approved HTTPS JWKS endpoint obtained from trusted issuer configuration. |
| `ICLOUD_REMOTE_RESOURCE` | Actual public HTTPS MCP resource URL with path `/mcp`. |
| `ICLOUD_REMOTE_DATABASE` | Absolute private persistent SQLite database path. |
| `ICLOUD_REMOTE_KEY_FILE` | Absolute private key-file path on the separate secret mount. |

Start exactly one process:

```sh
/opt/icloud-mail/venv/bin/python mcp/remote.py
```

It listens only on `127.0.0.1:8080`. Put an approved HTTPS reverse proxy in front
of it. Preserve the public Host header; serve `/mcp`, `/account`, and
`/.well-known/oauth-protected-resource/mcp`. Expose no direct cleartext listener
to other machines. The app validates Host/Origin on all routes and disallows query
strings; do not put tokens in URLs. Configure the proxy to limit request bodies
to 64 KiB (4 KiB for `/account`), enforce header/body timeouts, rate limit by IP
and authenticated user, and disable request/response/header logging and tracing.
Do not enable debug or OTel exporters. Limit inbound connections and egress to
the configured identity provider plus Apple's IMAPS service and required DNS.
No SMTP egress is needed. Protect backups and operator access.

The service caps MCP requests at 64 KiB, concurrent mail operations at eight,
OIDC lookups at four with five-second JWKS timeouts, and lock/capacity waits at
one second. Mail operations share a 60-second budget; setup uses 45 seconds.
It inherits the core's bounded pages, MIME/body/attachment processing and Apple
socket timeouts. IMAP library response buffering is not a transport allocation
limit; size host memory for concurrent parsing and enforce deployment limits.
This SQLite release supports **one process on one durable host**, not replicas
or ephemeral/serverless filesystems. A process lock enforces that constraint.

## Private user onboarding and revocation

After the operator supplies the real issuer, resource URL and public device
client ID, the user runs this command themselves in a private terminal:

```sh
/opt/icloud-mail/venv/bin/python mcp/connect_remote.py \
  --issuer "$APPROVED_ISSUER" --client-id "$PUBLIC_DEVICE_CLIENT_ID" \
  --resource "$APPROVED_MCP_RESOURCE"
```

The browser handles identity-provider sign-in/consent. The terminal then accepts
the primary mailbox address and a hidden **Apple app-specific password**, sending
them directly to authenticated HTTPS `PUT /account`. Neither password nor token
is stored by the CLI. Do not run or screen-capture this interaction through an
agent, paste secrets into chat, pass secrets as tool/CLI arguments, or use a normal
Apple Account password. The CLI refuses redirects and inherited HTTP proxies.
Setup interrupted before verified storage preserves the prior connection;
after a lost success response, retry the same mailbox to verify it again.

Then connect the MCP client to the actual service URL using its normal OAuth
flow. For the current Codex CLI, after operator-approved client registration:

```sh
codex mcp add icloud-mail-remote --url "$APPROVED_MCP_RESOURCE" \
  --oauth-client-id "$PUBLIC_MCP_CLIENT_ID" --oauth-resource "$APPROVED_MCP_RESOURCE"
codex mcp login icloud-mail-remote --scopes mail:read
```

Request `mail:attachments` or `mail:watch` only when needed. Do not grant
`mail:configure` to routine monitoring clients. For ChatGPT, configure a remote
OAuth app using the approved endpoint, following the linked OpenAI deployment
guide. Existing stdio plugin manifests are intentionally unchanged: there is no
placeholder service or shared credential shipped to every installer.

Use the same private CLI with `--disconnect` to call authenticated
`DELETE /account`. It deletes that principal's connection and watch state after
active mail operations finish (retry a busy response). Subsequent reads fail.
Also revoke the app-specific password at Apple and the OAuth grant at the issuer.
JWT grant revocation otherwise takes effect at access-token expiry; this service
does not introspect each JWT. Re-verifying the same mailbox rotates client
identifier generation and preserves watch progress. Disconnecting clears it.
Other tenants' data is untouched. Encrypted deleted records may remain in SQLite
free pages/backups; Apple revocation invalidates those credentials. Apply the
operator's documented backup retention/deletion policy.

Message/page/attachment identifiers are encrypted, tenant-bound and
connection-generation-bound, expire after one hour, and confer no authorization
without a current valid token. Restart a search after expiration/reconnection.
No mail bodies, subjects, attachments or mailbox index are retained by the
service. Requested mail still enters the client conversation/model handling.

## Explicit monitoring and durable checkpoints

No scheduler or notification transport is installed or resumed. A separately
authorized cloud runner may call `poll_watch` with a stable watch name and the
read/watch scopes. This scans INBOX from the initial two-day lookback, one page
at a time, persisting the core UIDVALIDITY-bound continuation independently of
delivery outcomes. A new cycle overlaps two days before the previous cycle's
start, including after runner downtime; it does not silently jump to today's
lookback. UIDVALIDITY changes restart that overlap scan and retain deduplication.
Backdated imports outside the overlap and pre-existing older mail are outside
this monitoring window; inspect them manually when needed.

Evaluate each candidate against the user's actual requested criteria. After an
alert is successfully delivered by the authorized runner, call
`acknowledge_watch` with its delivery ID and `outcome=delivered`. For evaluated
candidates that do not meet the criteria, use `outcome=no_alert`. Do not mark
merely scanned mail delivered. Pending candidates are re-fetched and retried
before further scanning, even after process restart. A disappeared message has
an `unavailable` receipt; inspect/resolve it explicitly, then complete it with
the truthful outcome. Receipt retries are idempotent; changing a completed
outcome is rejected. A crash between an external alert and acknowledgement can
redeliver; the runner should also use the delivery ID as its idempotency key.

Dedup uses a provider-independent hash of the trimmed RFC Message-ID, falling
back to a mailbox UID/UIDVALIDITY reference when missing. It operates within a
tenant/watch and recognizes duplicate IDs from imported/aliased copies; there is
no Gmail/Outlook connector or shared cross-provider checkpoint service in this
release. Each tenant has at most 20 watch names and each watch retains up to
10,000 completion receipts for 90 days. Hitting the limit or a truncated scan
fails explicitly without advancing scan progress. Watch state contains only
references, hashes, dates, outcomes and receipts, inside encrypted payloads.

## Operations and release acceptance

Back up the encrypted database and the secret key through separate approved
access paths. Rehearse restore with fake mail before storing user credentials.
Never replace the encryption key without decrypting/re-encrypting the records
in an approved offline maintenance window with access to both keys. Key loss
requires every user to reconnect. Rollback: stop the remote service and remove
its client connection; local stdio remains usable. Do not deploy an older server
against a newer database without a compatible backup/schema review.

Before public service onboarding, the operator must verify TLS/egress, OIDC
registration/consent/logout, scope denial, proxy redaction/rate limits, separate
volume/key backups, authenticated onboarding/revocation and restore on the real
host. Run two independent test users, expire/revoke their grants, and verify
that one user's identifiers cannot read another mailbox. Finally, run an
authorized cloud-runner read while the Mac is offline. Package tests cannot
establish these deployment facts. A hosted service also needs an operator-owned
privacy/retention policy and support process before public users entrust mail.

Offline verification from the repository root:

```sh
ICLOUD_REMOTE_TESTS_REQUIRED=1 PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m unittest discover -s tests -p 'test_icloud_mail*.py' -v
```

## Primary references (consulted 2026-10-23)

- [OpenAI remote connection and testing](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [OpenAI authentication](https://developers.openai.com/plugins/build/auth)
- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OAuth device authorization](https://www.rfc-editor.org/rfc/rfc8628)
- [JWT access token profile](https://www.rfc-editor.org/rfc/rfc9068)
- [PyJWT validation](https://pyjwt.readthedocs.io/en/stable/usage.html)
- [Fernet authenticated encryption](https://cryptography.io/en/latest/fernet/)
