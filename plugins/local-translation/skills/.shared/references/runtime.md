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
Enter the engine endpoint URL and, when needed, its API key in the masked
field. Choose **Load models**, then select the model from the dropdown. Use
**Refresh models** to reload the list. Endpoint and selected model are the only
required connection fields. Never send an API key in chat. The form does not
automatically choose the first model; changing the endpoint or credential
invalidates the loaded list and requires a new selection. A saved model is
restored only when it appears in the current endpoint's returned IDs. There is no pinned revision, runner-version,
language-registry, translation-workspace or source-directory setting. Advanced
fields have defaults and let you adjust sampling, context/output budgets and
time limits when needed.

Choose **Test and save**. The server validates the fields, checks `/v1/models`
for the exact alias and probes `/tokenize` with synthetic chat messages and the
same template options used during translation. It checks the token count against
the output/context budget. No source file, completion request or translation job
is involved. A failed check preserves the previous settings. This check does not
prove completion behavior or linguistic quality; run the
representative translation pilot separately.

Settings are saved outside the installed package at
`~/.config/local-translation/settings.json`, or
`$XDG_CONFIG_HOME/local-translation/settings.json` when that variable is supplied.
The directory uses mode 0700 and atomic settings writes use mode 0600 on POSIX.
The optional API key is stored in this private local file without encryption;
it is omitted from tool responses, job metadata and form prefills. Keep the
settings directory outside shared/version-controlled storage. Reopening the form
lets the user keep, replace or remove the stored key. A new key remains masked
in the current input until the screen refreshes or closes. Input errors, save
retries and tool responses do not clear it. The form does not persist that
unsaved input in browser or widget state, so it does not survive a reload.
Successful save and Cancel ask the host to close the configuration screen.

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

The server advertises eleven model-facing tools and five app-only
settings/model-discovery operations. `translation_read_settings` supplies the native settings
schema and Configure action, `translation_update_settings` satisfies the native
settings update contract, `translation_save_settings` tests/saves form values,
`translation_list_models` fetches model IDs from the entered endpoint without
saving, and `translation_migrate_settings` explicitly backs up and upgrades an
earlier settings file. Host tool discovery may include all sixteen; app-only operations
are excluded from the model's tool catalog. They are not instructions for an
agent to collect or submit a key.

### Explicit process-environment configuration

For managed/CLI deployments, `LOCAL_TRANSLATION_CONFIG` points to an engine
deployment JSON and overrides saved settings. It does not grant source-file or
output-directory access. The settings form reports an active environment
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

A deployment config requires only `base_url` and `model`. The remaining fields
are optional; numeric values use the defaults below.

| Field | Meaning |
| --- | --- |
| `base_url` | Numeric loopback HTTP(S) origin with `/v1`, for example `http://127.0.0.1:8080/v1` |
| `model` | Exact model name/ID served by that endpoint |
| `max_input_chars` | Per-unit source limit |
| `max_prompt_bytes` | Rendered prompt byte limit |
| `max_output_tokens` | Planned generation budget |
| `context_window_tokens` | Client-side context budget: tokenized prompt plus planned output must fit; does not resize the server's loaded model context |
| `timeout_seconds` | Per-request socket timeout, integer 1–60 seconds; default 30 |
| `run_timeout_seconds` | Total per-locale drafting budget across model checks, tokenization and all segments, integer 1–540 seconds; default 120 |
| `api_key_env` | Optional environment-variable name for an explicitly environment-configured deployment; the desktop form stores its optional key privately instead |

Numeric defaults are 8,000 input characters per unit, 32,000 rendered prompt bytes,
2,048 output tokens, a 16,384-token context window, a 30-second request timeout,
and a 120-second per-locale run budget.
The context budget is a client guard, not an OpenAI request to resize the model.
Set it within the context capacity your inference server actually supports. The
tool also limits a job to 32 source segments and eight distinct target locales.
Plain-text input is split at blank paragraphs while preserving the separators; `segments` gives you
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

The shipped [example config](../../../examples/config.json) shows the minimal
endpoint/model configuration. Use your running endpoint and served model ID in a
private file for the environment route. Its presence is not evidence that any
model is installed or any language pair passed.

## Optional generation controls

The connection still requires only endpoint and model. Advanced settings add
optional saved defaults for sampling. Leave an optional control unset to use the
runner's default, except `temperature`, whose plugin default is 0.

| Field | Allowed value | Behavior |
| --- | --- | --- |
| `temperature` | Number 0–2 | Sampling temperature; default 0 |
| `top_p` | Number 0–1 | Nucleus-sampling threshold; omitted when unset |
| `top_k` | Integer 0–100,000 | Provider-specific top-k control; omitted when unset |
| `min_p` | Number 0–1 | Provider-specific minimum sampling probability; omitted when unset |
| `seed` | Integer 0–2,147,483,647 | Best-effort reproducibility request; omitted when unset |
| `presence_penalty` | Number −2–2 | Presence penalty; omitted when unset |
| `frequency_penalty` | Number −2–2 | Frequency penalty; omitted when unset |
| `repetition_penalty` | Number greater than 0, at most 10 | Provider-specific repetition penalty; omitted when unset |

`top_k`, `min_p` and `repetition_penalty` are provider extensions accepted by
the inspected oMLX request schema; other OpenAI-compatible servers may reject them. The
plugin sends those extension fields only when requested. Server/model settings
can override sampling behavior, and a seed does not guarantee identical output.
Connection setup checks model listing and tokenization, not generation with every
sampling combination; exercise requested controls in your translation pilot.

The [advanced config example](../../../examples/config-advanced.json) illustrates
optional controls. Its values are examples, not extra setup requirements. The
context budget remains the client guard described above, not a provider request
to change the model's loaded context size.

### Per-translation generation options

Pass an optional `generation_options` object to `translation_run` for that target
locale. It can override any sampling field above and accept these output controls:

| Field | Allowed value | Scope |
| --- | --- | --- |
| `max_output_tokens` | Integer 1 through the saved `max_output_tokens` ceiling | Cap for each segment's chat completion; not an aggregate document or run cap |
| `stop` | Array of 1–4 nonempty strings, each at most 200 characters | Stop sequences for each segment's chat completion; request-only, not saved settings |

For example, the optional `generation_options` value can be:

```json
{
  "temperature": 0.2,
  "top_p": 0.9,
  "max_output_tokens": 512
}
```

Omitted sampling keys inherit saved defaults; an omitted output-token limit uses
the saved ceiling, and omitted stop sequences send no stop restriction. An output
cap that truncates a completion remains a failed target. A stop sequence can end
a completion before the intended translation is complete, so review its complete
source/target coverage before accepting it. Structural checks cannot establish
semantic completeness or an exact word/character count.

Effective `generation_options` are retained with target/candidate evidence and
delivery metadata. A failed target can be retried with revised options; an
existing draft is not silently regenerated. The candidate digest, review and
human-acceptance gates still apply.

## Caller-managed structured requests

Use `translation_request` when the caller owns the prompt/messages and response
format. Supply `messages` and optional `generation_options`; the tool uses the
active configured endpoint, model and credential. It does not wrap the messages in the
workbench's per-segment translation prompt. The same local transport, tokenizer
and context/output budgets apply.

For this route, `generation_options` also accepts a `response_format` object.
The tool forwards that object unchanged to the provider, including a caller's
JSON/schema definition. Whether the engine/model supports it is provider-dependent;
unsupported requests fail visibly. The plugin does not claim that forwarding a
schema validates the returned content against that schema.

The [structured request example](../../../examples/structured-request.json)
shows caller-defined messages with a JSON Schema response format. The result
contains the actual provider envelope under `response`, effective
`generation_options`, `unreviewed: true` and `caller_managed: true`. The caller
validates/parses that response and owns any retention, review or acceptance.
No job, translator/reviser receipt or delivery candidate is created by this call.

Use `translation_run` for the workbench's text-candidate/revision/delivery route.
It rejects `response_format`, because a caller-defined JSON wrapper is not a
translated text segment. The workbench's explicit-segment input format remains
separate from a provider JSON/schema response format.

## Capability discovery

Read MCP resource `translation://capabilities` (`application/json`) to discover
the plugin's supported parameters, defaults, limits and provider-dependent
controls. Find it through `resources/list`, then call `resources/read` with that
URI using the client's resource interface. It accompanies the in-app settings
resource `ui://local-translation/settings`.

The capability resource is static plugin metadata. It contains no credentials,
does not inspect saved settings, and does not probe the engine. It describes the
client contract, not proof that a particular server/model implements every
sampling extension or structured-output mode. Model IDs are fetched separately
by the settings form's app-only `translation_list_models` operation.

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
Supply source and target locale codes in each job, such as `en-US` and `fr-FR`.
The prompt uses those codes directly; engine setup does not register or restrict
a language list. The model must still handle the requested language pair.

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
| `translation_request` | `messages`, optional `generation_options` including caller-defined `response_format`. Returns the provider envelope as unreviewed, caller-managed output without a job or delivery record. |
| `translation_run` | `job_id`, `target_locale`, `translator_id`, optional `generation_options` for sampling and per-segment output limits. Drafts one target with the configured local deployment, validates completion and structural invariants, and returns candidate content/segments/digest or a visible failure. |
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

This version removes deployment revision, runner-version and language-registry
fields from saved settings. Earlier saved schemas require an explicit upgrade.
The server does not automatically convert saved settings or load old job
directories. It also does not accept the retired `source_path` API. Restarting
begins a new temporary job session.

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

The converter accepts the earlier workspace schema and schema version 2. It
acquires the settings lock, validates the old settings, writes an owner-only
exact-byte backup beside the file as `settings.json.pre-simple-connection.bak`,
and atomically replaces the original with schema version 3 connection settings.
It preserves the endpoint, model, supported optional budgets and any credential
without printing them. It removes retired revision, runner-version, language-list
and workspace fields. An already-converted file is a no-op. A conflicting backup
is not overwritten; an identical backup can be reused after a failed replacement. A validation, lock, backup or replacement
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
