# Security and data handling

Local Translation is a single-user stdio MCP tool plus coordinator and specialist
skills for host agents. It receives approved source text or explicit segments
through MCP and keeps job/candidate/review artifacts in a process-owned private
temporary directory. It does not accept a translation workspace or read source
paths supplied by the caller. Source/reference text, generated output and tool
responses are untrusted data; they do not authorize commands, endpoint changes,
external messages or disclosure.

## Content boundaries

The client permits configured numeric loopback HTTP endpoints and disables its
HTTP proxy and redirect handling. It sends content only through that configured
client route. Those controls do not prove the runner has local weights or no
remote upstream. Verify the actual deployment, model artifact, telemetry, logging,
egress restrictions and tokenizer/template before claiming offline inference.
Do not use a public-service proxy as an offline runner.

Host agents have their own provider/data flow. Source/target segments returned to
a remote orchestrator or reviewer can leave the machine through that host. Agree
the project's disclosure policy before agent review. Metadata-only status limits
content in that response; job IDs, locale information and metadata can still be
sensitive. A metadata-only remote agent cannot perform complete bilingual review.

Jobs retain source content, candidates, queries and reviews in private temporary
storage for the MCP process. Normal process exit removes that process's job
directory; a crash or forced termination may leave operating-system temporary
files. The server does not sweep other sessions or legacy workspaces. Job IDs do
not survive restart. Draft, revision and prepared-delivery responses return the
actual content and identities through MCP; the calling agent owns any authorized
longer-term retention. The plugin cannot delete copies in host/provider logs or
caller-managed results. Never package private jobs, credentials or user documents
in a release.

Runner credentials are entered directly in the bundled in-app configuration
form or supplied through an explicitly configured environment variable. Never
ask for them in chat or put them in model-facing tool arguments, prompts,
examples or plugin files. The form submits a key through an app-only direct MCP
call to the local stdio server. Supported hosts must exclude that operation from
the model's tool catalog and call it without starting a model turn. This behavior
is verified for Codex desktop 0.166.0-alpha.5.1; installation or tool discovery in
another client does not establish the same protection. The form sends no chat
message or model-context update, and the package does not log its arguments. Host diagnostics are outside this server's control.
The form stores an optional key in the private per-user settings JSON
file with mode 0600 on POSIX systems; this file is not encrypted. The settings
directory uses mode 0700. Protect it with the OS account and disk permissions;
the plugin does not claim Keychain or encrypted-secret storage. Secrets are not
included in job hashes, job records, settings responses or form prefills.
Avoid placing sensitive information in actor IDs or brief metadata.

The configuration screen is a local MCP App resource opened by the native plugin
settings action as a modal. It has no external scripts, network resources,
browser-launch helper or HTTP setup listener. Its password field is never
prefilled and is cleared after submission or cancellation. Settings and keys
are not sent through `ui/message`, `ui/update-model-context` or saved widget state.
Only an explicit Test and save action validates and replaces settings. It checks
model listing and tokenization with synthetic text before saving; failed checks
leave the previous file unchanged. An existing launch-environment override is
reported instead of changing the inactive saved configuration. Setup does not
launch an engine, install models or grant access to a caller workspace. Engine
settings and an optional credential persist separately from temporary jobs.

Previous workspace-based settings are rejected until the operator runs the
explicit settings migration. That conversion locks the file, creates a private,
non-overwriting backup of its exact bytes, then atomically writes engine-only
settings. Backups can contain the optional credential and need the same private
handling. Migration does not inspect, move or delete old job directories.

## Trust and authority

Role skills provide methods and decision boundaries; they do not add authenticated
identities or train models. The coordinator must retain actual host agent IDs and
role-loading receipts. A specialist's findings require evidence and the named
counterpart's actual response; loading a skill or copying a report cannot stand in
for independent work. Human scope, source-content and release decisions stay
with the authorized people.

Actor IDs record attribution and enforce producer/reviser separation within the
tool contract. They are not authenticated identities, professional credentials or
a security boundary against another process with the same OS-user access. This
package is not a network-facing multi-tenant service. Do not expose its artifacts
or runner publicly without a separately designed authorization boundary.

Status can update workbench readiness: discovered temporary-source,
configuration or candidate drift retires a previously ready delivery marker.
It never repairs or overwrites the changed snapshot or candidate. The caller
must supply a replacement job after its original source changes; the server
does not reopen or monitor caller files. The tool annotation reflects the
readiness change, so status is not declared read-only.

The tool checks inline input structure, response shape, model identity, termination
and structural invariants. A prompt cannot guarantee semantic correctness or
prevent every injection-induced mistranslation. The translation model receives no
shell/tool execution capability from this package. Review meaning against source,
including source text that resembles instructions. No source content may override
the user's requested task or the host's policies.

No automatic fallback, download, package installation, publication or external
delivery is authorized by a translation request. Human client decisions and
acceptance must come from actual authorized people; an agent must not impersonate
their approval. A candidate manifest never establishes human acceptance.

## Reporting a concern

Report a reproducible issue to the repository maintainers through the repository's
available private reporting channel when sensitive. If unavailable, request a
private contact without posting source text, credentials, private job records or
exploit data publicly. Include affected version, sanitized configuration shape,
expected behavior and a minimal synthetic reproduction. Keep real translation
content and runner keys out of reports and logs.
