# Local tool setup and API

This package installs a Python standard-library MCP server. It accepts source
content through MCP, coordinates temporary session artifacts and returns results
through MCP. It calls an already running, explicitly configured Index-Translate
deployment. It does not bundle model weights, install a runner, launch inference,
implement the supporting proposal's HTTP gateway, or provide asynchronous worker
leases, cancellation, fallback, an authenticated multi-user service or a scheduler.
Calls run synchronously; queue independent work through the host/PM.

## Prerequisites and configuration

Use Python 3.11 or newer and a local oMLX or vLLM-compatible server exposing model listing,
chat completions and tokenization for chat messages. The required tokenization
endpoint is `/tokenize` on the same local origin, outside the `/v1` prefix. A server
with only an OpenAI chat endpoint is insufficient. In particular, do not assume
an Ollama or llama.cpp endpoint implements this package's tokenization contract.

oMLX 0.7.3rc1 accepts the required `model`, `messages`,
`add_generation_prompt` and `chat_template_kwargs` fields at `/tokenize` and
returns `count`. Its default port is 8000; use the actual port and served model
alias from your deployment. A converted MLX artifact often has a different alias
from the upstream model repository. The oMLX
[API compatibility guide](https://github.com/jundot/omlx#api-compatibility)
describes the routes. This support is a protocol contract, not evidence that a
particular installed Index artifact has passed a translation pilot.

### Desktop setup

Open the plugin's native settings and select **Configure local inference**. The
host opens the bundled MCP App as a modal above settings, even before the engine
is configured. The coordinator can also invoke `translation_open_settings` when
you ask **“Open Local Translation settings.”** A model-invoked view uses the
host's in-app MCP App presentation; the native settings action supplies the modal.
Enter the engine URL, exact model alias, verified
artifact revision and runner version, and locale registry. There is no translation
workspace or source-directory setting. Advanced fields control context and time
budgets.
Enter an optional runner API key directly in the form; never send it in chat.

Choose **Test and save**. The server validates the fields, checks `/v1/models`
for the exact alias and probes `/tokenize` with synthetic chat messages and the
same template options used during translation. It checks the token count against
the output/context budget. No source file, completion request or translation job
is involved. A failed check preserves the previous settings. This check does not
prove model provenance, completion behavior or linguistic quality; run the
representative translation pilot separately.

Settings are saved outside the installed package at
`~/.config/local-translation/settings.json`, or
`$XDG_CONFIG_HOME/local-translation/settings.json` when that variable is supplied.
The directory uses mode 0700 and atomic settings writes use mode 0600 on POSIX.
The optional API key is stored in this private local file without encryption;
it is omitted from tool responses, job metadata and form prefills. Keep the
settings directory outside shared/version-controlled storage. Reopening the form
lets the user keep, replace or remove the stored key.

Both Codex and Copilot use the same saved settings. They survive plugin updates
and apply on the next tool call without restarting either client.
`translation_settings` reports the active source, settings path and redacted
configuration. `translation_health` verifies the connection after setup. Do not
edit a versioned plugin cache or the client's MCP declaration to configure the
engine. The bundled stdio process and its downstream inference HTTP connection
are separate connections; tool discovery proves only the former.

The popup needs MCP Apps and the `openai/settings` extension in its host. It
uses a packaged UI resource and app-only settings operations. The host must
enforce app-only visibility and call the local server without a model turn; this
is verified for Codex desktop 0.166.0-alpha.5.1. Other clients need equivalent
enforcement before the form handles credentials. No form state is sent to model context,
messages or widget persistence. Unsupported hosts receive setup guidance; the
plugin does not launch a browser as a fallback. Copilot CLI can use the same
saved engine configuration or an explicit deployment file, even when it cannot
render the native popup.

The server advertises ten model-facing translation tools and four app-only
settings operations. `translation_read_settings` supplies the native settings
schema and Configure action, `translation_update_settings` satisfies the native
settings update contract, `translation_save_settings` tests/saves form values,
and `translation_migrate_settings` explicitly backs up and upgrades a retired
settings file. Host tool discovery may include all fourteen; app-only operations
are excluded from the model's tool catalog. They are not instructions for an
agent to collect or submit a key.

### Explicit process-environment configuration

For managed/CLI deployments, `LOCAL_TRANSLATION_CONFIG` points to an engine
deployment JSON and overrides saved settings. It does not grant source-file or
output-directory access. The settings page reports an active environment
override instead of changing an inactive file. No translation-root environment
variable is used.

An optional credential comes from the variable named by `api_key_env`. Codex's
declaration forwards `LOCAL_TRANSLATION_CONFIG` and `LOCAL_TRANSLATION_API_KEY`
from its launch environment. Use that credential name
in Codex. The portable declaration uses no Codex-specific forwarding extension;
other clients control their explicit environment. See the official
[stdio environment rules](https://learn.chatgpt.com/docs/extend/mcp#stdio-servers).
Restart a client only when changing this explicit launch environment. The normal
desktop saved-settings flow needs none of these variables.

The deployment config declares:

| Field | Meaning |
| --- | --- |
| `base_url` | Numeric loopback HTTP origin with `/v1`, for example `http://127.0.0.1:8080/v1` |
| `model` | Exact served alias, independently mapped to the intended Index artifact |
| `artifact_revision` | Actual pinned model artifact/revision, including quantization identity where applicable |
| `runner_version` | Actual runner version/build |
| `locales` | Allowed exact locale tags mapped to prompt labels; source and every target must be registered |
| `max_input_chars` | Per-unit source limit |
| `max_prompt_bytes` | Rendered prompt byte limit |
| `max_output_tokens` | Planned generation budget |
| `context_window_tokens` | Actual served context window; must fit tokenized prompt and planned output |
| `timeout_seconds` | Per-request socket timeout, integer 1–60 seconds; default 30 |
| `run_timeout_seconds` | Total per-locale drafting budget across model checks, tokenization and all segments, integer 1–540 seconds; default 120 |
| `api_key_env` | Optional environment-variable name for an explicitly environment-configured deployment; the desktop form stores its optional key privately instead |

Numeric defaults are 8,000 input characters per unit, 32,000 rendered prompt bytes,
2,048 output tokens, a 16,384-token context window, a 30-second request timeout,
and a 120-second per-locale run budget.
Set the context window to the real deployment limit. The tool also limits a job
to 32 source segments and eight distinct target locales. Plain-text input is split
at blank paragraphs while preserving the separators; `segments` gives you
explicit IDs.

Choose `run_timeout_seconds` for the whole locale before creating the job. A
multi-segment guide may need more than the default 120 seconds even when each
request completes within `timeout_seconds`. Raising the total budget does not
raise the per-request timeout. The 540-second maximum leaves time for saving and
stdio handling within the Codex declaration's 600-second tool timeout; other
clients may impose their own limits. The run deadline is checked between requests
and response reads, while a blocked socket read remains subject to its request
timeout. A timeout stays a visible failed locale and cannot produce a complete
candidate. Changing either configuration value requires a replacement job.

The shipped [example config](../../../examples/config.json) contains illustrative
deployment metadata. Replace it with verified values in a private engine
configuration file if using the environment route. Its presence is not evidence
that any model is installed or any language pair passed.

## Temporary session lifecycle

The server creates one private operating-system temporary directory for job work
in its MCP process. Multiple tool calls within that process share the frozen
source, candidates, queries and reviews. No caller workspace or source path is
accepted. Health/settings checks do not need job storage.

Normal server exit removes that process's temporary job directory. A crash or
forced termination can leave temporary files behind; the plugin does not sweep
other sessions or promise secure erasure. Job IDs and unfinished review state do
not survive restart. Keep a live session for the whole draft/revision workflow.
The calling agent must retain any returned content and evidence needed after
that session through the user's authorized route.

Successful drafting and revision return `format` (`txt` or `json`), the exact
rendered UTF-8 `content`, translated `segments` and `sha256`. Prepared delivery
returns these fields for every gated locale alongside the manifest and review
evidence. The caller receives the result through MCP and chooses any authorized
file creation or longer-term retention. Temporary server paths are not a delivery
interface. In the JSON format, `content` is the rendered JSON text; the segments
mapping provides direct access to translated units.

The default status projection omits source/target bodies, brief, glossary,
query text, review notes and content-bearing delivery fields.
`include_segments=true` returns the full review context. This projection does
not confine all tool or host-agent processing to the machine. Status checks the
frozen temporary source snapshot, configuration and candidate identities. Drift
retires the ready-delivery marker without modifying a snapshot or candidate.
Status is therefore declared as a state-changing tool. The calling agent must
create a replacement job when its original source changes; the server does not
reopen or monitor caller files.

## Supported inputs

Call `translation_create_job` with exactly one of `source_text` or `segments`.
The caller handles any authorized extraction or source-file access before
passing content to MCP. No `source_path` argument is supported.

Plain prose:

```json
{
  "source_locale": "en-US",
  "target_locales": ["fr-FR"],
  "brief": "Translate this greeting. Preserve the name placeholder.",
  "source_text": "Welcome, {name}."
}
```

Explicit segments:

```json
{
  "source_locale": "en-US",
  "target_locales": ["fr-FR"],
  "brief": "Translate this greeting. Preserve the name placeholder and APP_ID.",
  "segments": [
    {
      "id": "welcome",
      "text": "Welcome, {name}. Keep APP_ID unchanged.",
      "protected": ["APP_ID"]
    }
  ]
}
```

The [structured example](../../../examples/guide-segments.json) is a complete
`translation_create_job` argument object, including a deliberate printf string.

Segment `format` defaults to `plain`. For a string that is deliberately a printf
format, set `"format": "printf"` on that JSON segment. This enables printf
placeholder inventory and nonpositional argument-order checks. Ordinary prose
such as `Save 10% on orders.` stays in plain mode, so a percent sign is not
mistaken for the beginning of a formatting instruction. Brace placeholders,
literal numbers and explicitly protected spans are checked in either mode.
Use explicit segments for format-bearing strings; `source_text` is plain prose.

Prepare stable unique IDs for review/query linkage. `protected` lists literal
strings that must survive in that unit; it is not a native-resource grammar.
Supply enough context in the brief and source units for meaningful translation.
The locale glossary is a map of locale to source/target term pairs, for example
`{"fr-FR":{"Settings":"Paramètres"}}`. Terminology checks cannot prove conceptual
accuracy, inflection suitability or correspondence with the actual app.

## Tools

Inspect `tools/list` in the running host for the authoritative argument schemas;
the server rejects unsupported properties. The tool names below are the unprefixed
MCP names; a host may display them with a server namespace.

| Tool | Main inputs and result |
| --- | --- |
| `translation_settings` | No arguments. Report the active settings source and redacted configuration, including setup instructions when unconfigured. Does not contact the engine. |
| `translation_open_settings` | No arguments. Present the bundled MCP App inside the host. The native plugin settings action opens it as a modal. Keys are entered in its masked field and submitted only through the app-only save operation, outside model turns. Does not install or start inference. |
| `translation_health` | No arguments. Check the exact model and synthetic chat tokenization before job creation/runs. An unconfigured response points to setup. It cannot prove that the runner itself has no remote upstream. |
| `translation_create_job` | Exactly one of `source_text` or `segments`, plus `source_locale`, `target_locales`, `brief`, optional `glossary`. Freezes inline source, configuration and resources in temporary session storage; returns a job ID. |
| `translation_run` | `job_id`, `target_locale`, `translator_id`. Drafts one target with the configured local deployment, validates completion and structural invariants, and returns candidate content/segments/digest or a visible failure. |
| `translation_status` | `job_id`, optional `include_segments`. Default metadata omits segment bodies and free-text context. `include_segments=true` discloses source/target text, brief, glossary, query questions/answers and review/revision notes to the caller/host. |
| `translation_query` | `job_id`, `actor_id`, and `question` for a new query; use returned `query_id` and an attributed `answer` to resolve it according to the discovered schema. Runtime attribution is not proof of client authorization. |
| `translation_apply_revision` | `job_id`, `target_locale`, `actor_id`, `expected_target_sha256`, `replacements` mapping segment ID to corrected text, and `notes`. Applies validated corrections, invalidates prior reviews and returns the updated content/segments/digest. |
| `translation_review` | `job_id`, `target_locale`, `reviewer_id`, `target_sha256`, `expected_context_revision`, `verdict`, `notes`. Supply the integer context revision actually inspected. Verdict is `approved`, `changes_requested` or `blocked`; the reviewer must differ from recorded candidate authors. Approval is an attributed AI/tool record, not human acceptance. |
| `translation_prepare_delivery` | `job_id`. Requires current successful reviewed targets and no unresolved queries; returns a candidate manifest and each locale's actual content/segments/digest through MCP, never publishes or asserts human acceptance. |

Review/apply-revision calls require current digests to prevent stale work from
becoming current evidence. Shared input/configuration changes require a new job.
Adding or answering a shared query increments `context_revision` and invalidates
existing target reviews. Status and candidate responses expose the current
revision. Read full review context with `include_segments=true` and submit the
revision you actually inspected; the server rejects a delayed review from an
older context even when target text has not changed. Revisit the answer's impact
and obtain current review evidence before delivery.
Old jobs remain temporary session evidence; identify successors in the project
record and retain returned evidence through the caller when required. Do not
mutate stored JSON manually or reinterpret a failed language as completed.

## Migrate previous settings

This version replaces the workspace-based tool/configuration contract. It does
not automatically load old job directories, convert legacy saved settings or
accept the previous `source_path` API. Restarting on this version begins a new
temporary job session.

If saved settings use the retired format, open the configuration modal and
select **Back up and upgrade saved settings**. The app-only migration operation
uses the same one-off converter described below, against the normal private
settings file. It does not contact the engine or inspect previous job files.
Inspection and ordinary save calls never migrate implicitly.

For a CLI-only host, or when selecting another authorized file explicitly, run
the converter from a source checkout using its existing Python environment:

```bash
.venv/bin/python plugins/local-translation/mcp/migrate_settings.py
```

For an installed package, resolve that package's actual `mcp/migrate_settings.py`
and run it with Python 3.11+. The default target is the normal per-user settings
file. To select another authorized settings file, pass
`--settings /absolute/path/settings.json`.

The converter acquires the settings lock, validates the legacy settings, writes
an owner-only exact-byte backup beside the file as
`settings.json.pre-temporary-jobs.bak`, and atomically replaces the original with
schema version 2 engine-only settings. Deployment values and an optional
credential are preserved without printing them. An already-converted file is a
no-op. A conflicting backup is not overwritten; an identical backup can be
reused after a failed replacement. A validation, lock, backup or replacement
failure leaves the original settings unchanged. Protect the backup because it
can contain the credential. Reopen setup and verify `translation_health` after
migration.

Remove `LOCAL_TRANSLATION_ROOT` from any explicitly managed client launch
environment; only the engine configuration override remains. Retain or archive
legacy workspace job directories according to the user's existing policy. The
converter does not inspect, move, import or delete them. Before a deliberate
rollback, stop the new server and restore the exact private settings backup
through the operator's approved file-management procedure; do not overwrite a
newer credential or configuration silently.

## Runner behavior and limits

The client uses the configured model alias and an original versioned prompt
profile informed by Index's official text prompt contract. It tokenizes the actual
chat prompt before generation and requests non-thinking output. A prompt is a
request, not enforcement. The runtime independently checks response envelope,
served model, successful termination, nonempty candidate and supported structural
invariants. Linguistic review remains necessary.

Only numeric loopback endpoints are allowed. HTTP proxies and redirects are
disabled in the client. These controls constrain this client's requests; they do
not inspect the runner's internal network behavior, attest model weights, prevent
host-agent disclosure or guarantee an air-gapped machine. Verify the deployed
runner, egress restrictions, logging and artifact provenance separately.

No silent retry/fallback chooses a different model, no public Index endpoint is
configured, and no weights are downloaded. A timeout, unsupported tokenizer,
truncated/empty completion, model mismatch or invariant failure remains visible.
Resolve the cause and rerun deliberately; do not patch a broken candidate by
inventing text or suppressing the error. The service is single-user local tooling,
not an authentication boundary against other processes running as that user.
