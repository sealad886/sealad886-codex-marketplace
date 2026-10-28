# Local tool setup and API

This package installs a Python standard-library MCP server. It coordinates local
job artifacts and calls an already running, explicitly configured Index-Translate
deployment. It does not bundle model weights, install a runner, launch inference,
implement the supporting proposal's HTTP gateway, or provide asynchronous worker
leases, cancellation, fallback, an authenticated multi-user service or a scheduler.
Calls run synchronously; queue independent work through the host/PM.

## Prerequisites and configuration

Use Python 3.11 or newer and a vLLM-compatible local server exposing model listing,
chat completions and tokenization for chat messages. The required tokenization
endpoint is `/tokenize` on the same local origin, outside the `/v1` prefix. A server
with only an OpenAI chat endpoint is insufficient. In particular, do not assume
an Ollama or llama.cpp endpoint implements this package's tokenization contract.

Configure the actual host MCP process environment:

- `LOCAL_TRANSLATION_ROOT`: absolute path to an authorized existing workspace.
- `LOCAL_TRANSLATION_CONFIG`: absolute path to your local JSON deployment config.
- Optional runner credential: the environment variable named by `api_key_env`.
  Keep its value outside plugin files, config examples, prompts and logs.

The plugin's MCP declaration starts `python3` with its contained `mcp/server.py`.
You must supply configuration in the client environment/settings using that
client's documented mechanism. Installation alone cannot infer your workspace,
deployment identity or data permissions. Do not edit a versioned plugin cache.

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
| `timeout_seconds` | Request timeout within the runtime's allowed range |
| `api_key_env` | Optional environment-variable name for the runner credential |

Numeric defaults are 8,000 input characters per unit, 32,000 rendered prompt bytes,
2,048 output tokens, a 16,384-token context window, and a 30-second request timeout.
Set the context window to the real deployment limit. The tool also limits a job
to 32 source segments and eight distinct target locales. Plain-text input is split
at blank paragraphs while preserving the separators; JSON gives you explicit IDs.

The shipped [example config](../../../examples/config.json) contains illustrative
deployment metadata. Replace it with verified values in your own workspace. Its
presence is not evidence that any model is installed or any language pair passed.
The tool reads supported sources under the root and stores job records under
`.local-translation/jobs`. Those records include source and candidate text;
protect and retain them according to the project's approved policy.

Drafting and revision calls return target text to the caller. The default status
projection omits source/target bodies, brief, glossary, query text and review
notes; `include_segments=true` returns that full review context. This projection
is not a mode that confines all tool or host-agent processing to the machine.

## Supported inputs

A `.txt` file contains plain UTF-8 prose. An explicit `.json` source has this shape:

```json
{
  "segments": [
    {
      "id": "welcome",
      "text": "Welcome, {name}. Keep APP_ID unchanged.",
      "protected": ["APP_ID"]
    }
  ]
}
```

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
| `translation_health` | No arguments. Inspect local configuration and served-model availability before job creation/runs. It cannot prove that the runner itself has no remote upstream. |
| `translation_create_job` | `source_path` relative to root, `source_locale`, `target_locales`, `brief`, `glossary`. Freezes supported source, configuration and resources; returns a job ID. |
| `translation_run` | `job_id`, `target_locale`, `translator_id`. Drafts one target with the configured local deployment, validates completion and structural invariants, and stores a candidate or visible failure. |
| `translation_status` | `job_id`, optional `include_segments`. Default metadata omits segment bodies and free-text context. `include_segments=true` discloses source/target text, brief, glossary, query questions/answers and review/revision notes to the caller/host. |
| `translation_query` | `job_id`, `actor_id`, and `question` for a new query; use returned `query_id` and an attributed `answer` to resolve it according to the discovered schema. Runtime attribution is not proof of client authorization. |
| `translation_apply_revision` | `job_id`, `target_locale`, `actor_id`, `expected_target_sha256`, `replacements` mapping segment ID to corrected text, and `notes`. Applies validated corrections and invalidates prior reviews. |
| `translation_review` | `job_id`, `target_locale`, `reviewer_id`, `target_sha256`, `verdict`, `notes`. Verdict is `approved`, `changes_requested` or `blocked`; the reviewer must differ from recorded candidate authors. Approval is an attributed AI/tool record, not human acceptance. |
| `translation_prepare_delivery` | `job_id`. Requires current successful reviewed targets and no unresolved queries; prepares a candidate manifest, never publishes or asserts human acceptance. |

Review/apply-revision calls require current digests to prevent stale work from
becoming current evidence. Shared input/configuration changes require a new job.
Adding or answering a shared query invalidates existing target reviews; revisit
the answer's impact and obtain current review evidence before delivery.
The old job's files remain evidence; identify its successor in the project record.
Do not mutate stored JSON manually or reinterpret a failed language as completed.

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
