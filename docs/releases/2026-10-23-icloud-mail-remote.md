# iCloud Mail 0.4.0 release evidence

## Scope and decisions

The requested outcome is iCloud Mail access while the user's Mac is offline,
with a public package, private credentials and multiple independent users.
Baseline: `1d6b465`, plugin 0.3.1, clean checkout; branch
`codex/icloud-mail-remote`. No worktree was created. Existing stdio source and
`account_session` are the shared mail core; the installed plugin cache is untouched.

The selected delivery route is `medium-feature-change` (medium scale, high risk:
new network/identity boundary holding mailbox credentials). Context, acceptance,
design, planning, implementation, quality, documentation, independent review and
release owners apply. Security is active for tenant/secret boundaries; coordination
is active for GitHub publication. Retrospective is planned after a meaningful live
outcome; package publication alone does not establish that outcome.

Accepted constraints: preserve local tools; remote read-only by default; validate
OAuth issuer/audience/lifetime/signature/scopes; bind issuer/subject to a verified
mailbox; no secrets in MCP/URLs/logs/releases; encrypted per-user storage with key
separate from database/code; bounded resources; no live credentials, new grants,
paid hosting, service/network changes or live deployment without approval.

The smallest feasible architecture is an optional official-SDK HTTP adapter
around the existing core, a single private encrypted SQLite store, external
established OAuth/OIDC, and a private device-flow setup CLI. A Mac tunnel cannot
meet offline availability. A global mailbox password cannot isolate users.
No new scheduler, notification transport or unrelated agent is included.

## Acceptance and verification map

| Requirement | Evidence |
| --- | --- |
| Local behavior retained | Existing mail self-test and full local regression suite. |
| Identity/scopes fail closed | JWT validity/signature/issuer/audience/nbf/iat tests; HTTP unauthorized responses; discovery and execution scope tests. |
| Tenant/secret isolation | Concurrent candidate sessions, encrypted database, row-swap/cursor replay rejection, fake-secret error redaction. |
| Private setup/revocation | Verified Apple destination, interrupted setup preservation, HTTP configure scope, per-principal deletion, active-read serialization. |
| Durable watch correctness | Pending replay, no-alert disposition, idempotent delivery receipts, scan continuation, overlap, UIDVALIDITY restart and truncated/transient failure preservation. |
| Distribution/CI | Complete MCP runtime selected in bundle; hash-locked remote dependencies; CI requires remote tests rather than silently skipping them. |
| Actual Mac-offline availability | **Blocked on approved always-on hosting/OIDC and authorized live cloud-runner test. Not established by package tests.** |

## Executed local evidence

- All 13 packages passed source/distribution validation, route/receipt contracts,
  Semantic Versioning examples, both MCP self-tests and marketplace validation.
- Full repository suite: 605 tests passed before the final expanded remote cases;
  current focused remote suite: 19 tests passed. Exact-commit CI remains required.
- Official SHA-pinned OpenAI manifest validator and Skill Creator validation passed.
- Independent security/correctness review found and prompted fixes for filtered
  watch progress, transient-error handling, and private setup timeout. No tenant
  escape, write-scope bypass or credential-disclosure path was confirmed in the
  reviewed boundaries. Live issuer/hosting evidence remains outstanding.
- Complete optional dependencies are pinned with artifact hashes; pip accepted
  the lock. All test credentials/keys/mail are synthetic.

## Release sequence and rollback

1. Finish implementation, tests/docs and independent review corrections.
2. Validate source, complete distribution, official manifest/skill checks and
   repository aggregate checks. Commit package source, pin the catalog to that
   immutable source commit, and verify package parity.
3. Open the authorized draft PR; require exact-commit CI and the pinned HOL
   scanner without high/critical findings before merge/tag/release.
4. Release `icloud-mail-v0.4.0` from the validated merge commit without moving an
   existing tag. Verify package asset hashes and catalog package identity. The
   repository's plugin-release workflow publishes the next independent marketplace
   snapshot as Latest; verify its actual source/version/status afterward.

Package rollback is a catalog pin to the previous immutable source with a new
marketplace release, preserving historical tags. Remote service rollback requires
stopping service/client connections and reviewing encrypted state compatibility;
local stdio remains usable. No live infrastructure or credentials are changed by
this release. See the packaged [operator guide](../../plugins/icloud-mail/mcp/REMOTE.md).

## Deployment blockers

Pending operator choice/approval: always-on host with outbound IMAPS, domain/TLS,
OIDC issuer/audience/JWKS and public-client registrations, separate secret/data
mounts, residency/retention/support, backup/restore, real two-user consent and
revocation tests. No endpoint is invented or advertised as live. No account or
network change, secret migration, paid hosting or shared-service deployment has
been performed. The final proof remains an authorized cloud-runner mailbox read
while the Mac is offline.
