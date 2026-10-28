# Security and data handling

Local Translation is a single-user stdio MCP tool plus a host-agent workflow. It
reads authorized supported source files under `LOCAL_TRANSLATION_ROOT` and writes
job/candidate/review artifacts beneath that root. Source/reference text, generated
output and tool responses are untrusted data; they do not authorize commands,
endpoint changes, external messages or disclosure.

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

Jobs retain source content, candidates, queries and reviews locally. Protect the
workspace with appropriate OS permissions and use an agreed retention/deletion
policy. The plugin does not automatically delete evidence or sanitize external
host logs. Never package private jobs, credentials or user documents in a release.
Runner credentials come from a named environment variable, not config values or
prompts. Avoid placing sensitive information in actor IDs or brief metadata.

## Trust and authority

Actor IDs record attribution and enforce producer/reviser separation within the
tool contract. They are not authenticated identities, professional credentials or
a security boundary against another process with the same OS-user access. This
package is not a network-facing multi-tenant service. Do not expose its artifacts
or runner publicly without a separately designed authorization boundary.

Status can update workbench readiness: discovered source/configuration or output
drift retires a previously ready delivery marker. It never repairs or overwrites
the changed source or candidate file. Its tool annotation reflects that state
change; a status call is not declared read-only.

The tool checks supported input paths, response shape, model identity, termination
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
