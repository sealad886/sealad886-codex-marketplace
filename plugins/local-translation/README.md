# Local Translation

![Local Translation: coordinated language work across documents](assets/banner.png)

Coordinate expert agents through translation, independent bilingual AI revision,
terminology and subject review, correction loops, and a human release decision.
The bundled local MCP tool drafts supported text into multiple target locales
using an explicitly configured Index-Translate deployment.

The coordinator and drafting specialists share a
[model-input guide](skills/.shared/references/index-inputs.md), then load only the
selected Translate, Homura or NativeLong recipe. Those references teach approved
glossary/requirements/context preparation and actual caller-owned MCP messages;
role skills keep their own preparation and review responsibilities.

The [Translation Project coordinator](skills/translation-project/SKILL.md) assigns
work to nineteen separately invocable specialist skills. Each subagent loads its
assigned skill, acknowledges the remit and evidence gaps, follows that role's
working method, and returns an attributed handoff. The [role directory](skills/.shared/references/roles.md)
maps all sixteen whitepaper functions and the additional editing, proofreading,
media-coordination and conformance responsibilities to actual skills. Agents
exchange findings, replies and adjudications through the host's real
collaboration tools.

## Assign a specialist

Use `$local-translation:translation-project` for end-to-end coordination. The
coordinator commissions only the roles needed by the job, respecting host agent
slots; twenty available skills do not require twenty simultaneous agents.
Translator and independent reviser assignments for the same material must go to
different actual subagents.

Individual skills also work directly. For example:

> Use `$local-translation:bilingual-revision` to compare this French candidate
> against the approved English source, brief and glossary. Identify meaning and
> completeness errors, ask the translator to respond, and return the unresolved
> decisions with their evidence.

Each assignment names the installed role-skill path, owned locale and segments,
current artifact and shared-context identities, allowed tools, recipient and
stop conditions. A role-loading receipt shows which skill was read. Findings
then receive an actual counterpart response, adjudication where needed, and a
recheck. The [shared expert contract](skills/.shared/references/expert-contract.md)
and [handoff template](skills/.shared/templates/expert-handoff.md) define that
exchange once for every role.

Skills provide specialist procedures and decision support. They do not retrain
an agent, prove language/domain competence, or confer human qualifications.
Evaluate a representative pilot and the returned work; loading a role alone is
not a quality result. See the [role directory](skills/.shared/references/roles.md)
for all twenty entry points and their evidence requirements.

## Start a project

1. Install this package using your client's supported local marketplace/plugin
   flow. It ships portable Agent Plugins 1.0 components and the Codex overlay;
   client support and delegation capabilities differ.
2. Supply Python 3.11+ and an already running local oMLX or vLLM-compatible
   Index-Translate runner with model listing, chat completions and chat tokenization. Installation
   does not download weights or start inference.
3. Open the plugin's settings and choose **Configure local inference**. Codex
   opens the bundled configuration form as a modal inside the app. Enter the
   engine endpoint URL and any optional API key, then choose **Load models**.
   Select the model from the returned dropdown and choose **Test and save**.
   Endpoint and selected model are the only required connection fields.
   Authentication goes directly into the masked key field, never into chat. No translation workspace,
   MCP settings editor, terminal environment variables or app restart is required.
   The coordinator can also open the form inside a compatible MCP App host when
   you ask **“Open Local Translation settings.”** See the
   [runtime guide](skills/.shared/references/runtime.md) for fields and limits.
   Advanced sampling controls and context/output budgets are optional; you can
   also set generation controls for an individual translation request.
4. Give the calling agent your approved source content, source and target locales,
   audience, resources and acceptance owner. The agent supplies plain text or
   explicit segments through MCP. Run a representative pilot before a large batch.

Example request:

> Use Translation Project to translate this approved guide from en-US into
> fr-FR and de-DE. Use the approved UI terminology, assign a translator and a
> separate bilingual reviser for each locale, resolve shared questions through
> me, and return delivery candidates for my review.

The calling agent supplies `source_text` or `segments` to `translation_create_job`;
the tool does not read a caller-selected source path. It keeps frozen inputs,
candidates and review records in a private temporary directory for the MCP
process. Calls within that session share job state. Normal process exit removes
it; restarting the server invalidates the job IDs. A crash or forced termination
may leave files in the operating system's temporary storage.

Draft, revision and prepared-delivery responses include the actual UTF-8 content,
segments and digests through MCP. The calling agent decides where to retain the
returned results and evidence under the user's instructions. Temporary paths are
not a delivery interface. See
[session lifetime and migration](skills/.shared/references/runtime.md#temporary-session-lifecycle)
before upgrading or retaining results.

Default status omits source/target bodies and free-text review context.
`include_segments=true` returns segments, brief, glossary, questions/answers and
review/revision notes to the caller/host. Local inference and host-agent privacy
are separate: remote agents cannot fully review source/target content without
receiving it. Agree that data flow first.

Status checks the frozen temporary source snapshot, configuration and candidate
identities. Drift retires the workbench's ready-delivery marker. The calling
agent must create a replacement job when its original source changes; the MCP
server does not monitor the caller's files.

### Settings and connection checks

The plugin's MCP process connects Codex or Copilot to the translation tools. The
in-app form configures the tools' separate HTTP connection to your inference
engine. A discovered MCP tool does not establish a working engine connection.

**Test and save** checks the exact served model and the required chat-tokenization
endpoint using synthetic text. It creates no translation job and sends none of
your source content. A failed test preserves previous settings. Languages are
supplied with each job; setup does not require a language registry, pinned model
revision or runner version. Successful setup does not establish translation
quality; run a representative pilot afterward.

Optional advanced controls include temperature, top-p, top-k, seed and sampling
penalties. The context setting is a client-side token budget; it does not resize
the inference server's loaded model context. A `translation_run` request can
override generation options and set a per-segment output-token cap or stop
sequences. See [generation controls](skills/.shared/references/runtime.md#optional-generation-controls)
for defaults, ranges, provider support and the output-limit contract.

Callers that supply their own messages and JSON/schema response format can use
`translation_request`. It returns the local provider's response as unreviewed,
caller-managed output; it does not create a workbench job or delivery candidate.
The MCP resource `translation://capabilities` describes available controls and
limits and points to the shared model-input guide without reading credentials
or probing the engine.

### Use the model's native input format

For standard Translate, the [selected recipe](skills/.shared/references/index-translate.md)
shows the supported English native layout, source→target and identity glossary
pairs, mandatory requirements, preferences, genre/domain, approved instructions
and scoped context. The caller explicitly compiles these into `translation_request`
messages; they are not additional MCP fields or saved connection settings.
Native prompts use full language names; workbench jobs continue to take locale
codes. The optional [language reference](skills/.shared/references/index-languages.md)
helps resolve unfamiliar varieties/scripts without an engine language registry.

The [Homura recipe](skills/.shared/references/index-homura.md) covers its one
syllable target and optional glossary, with a complete caller-owned request and
actual syllable/meaning review duties. The
[NativeLong recipe](skills/.shared/references/index-nativelong.md) retains its four
fixed full-document templates and precise execution limit: this bounded
non-streaming MCP cannot express the full official streaming/token-ID-stop
profile. Do not present formatting or a generic segment request as full support.

The existing text workbench carries brief/glossary guidance and its candidate,
revision and delivery gates. It does not automatically add neighboring segments
or answered project queries to inference. The coordinator must propagate actual
owner answers into subsequent caller messages, apply/review a bounded correction,
or create a replacement job with a reconciled brief/glossary for a new generation.
Existing drafts do not regenerate. Exact native message control through the raw
route remains caller-managed and requires separate independent review.

For oMLX, use the port shown in its settings and append `/v1`, such as
`http://127.0.0.1:8000/v1` when using its default port. The model field must match
the served MLX model alias, which may differ from `IndexTeam/Index-Translate-9B`.
The popup fetches the endpoint's model IDs; it does not select a model for you.
Changing the endpoint or credential requires loading its model list again.
oMLX 0.7.3rc1's installed API supports the required chat-tokenization contract;
verify your running deployment through setup rather than assuming all versions
or model conversions behave identically.

Settings persist in `~/.config/local-translation/settings.json`, or under
`$XDG_CONFIG_HOME/local-translation/` when that environment variable is supplied.
The directory is private and the settings file is owner-readable/writable on
POSIX systems. An optional runner key is stored in that local file, without
encryption. In a supported MCP Apps host, the app-only save operation sends it
directly to the local server. The host must enforce app-only tool visibility and
call the server without creating a model turn; this is verified for Codex desktop
0.166.0-alpha.5.1. Keys are omitted from responses and form prefills, and the form
sends no state into model context or a message. Other hosts need the same
app-only enforcement before using this form for credentials.

A new key stays masked in the current input until the screen refreshes or
closes. Input errors, retries and tool responses do not clear it. Unsaved keys
are not persisted in browser or widget state and do not survive a reload. An
already saved key remains in the private settings file and is never prefilled.
After a successful save or Cancel, the form asks the host to close the
configuration screen. Settings survive plugin updates and apply on the next tool call. Keep this
directory outside a shared or version-controlled workspace.

`translation_settings` reports the active configuration source and redacted
engine settings. An explicit `LOCAL_TRANSLATION_CONFIG` launch-environment value
can point to an engine deployment JSON and takes precedence over saved settings.
The settings form reports that override rather than changing an inactive file.
Most desktop users need no launch-environment variables. For earlier saved
settings, the form offers **Back up and upgrade saved settings**.
That explicit action retains a private byte-for-byte backup before replacement.
The same migration is available through the packaged
[settings migration](skills/.shared/references/runtime.md#migrate-previous-settings)
before this version can use them.

### Local client commands

From this marketplace's root, the installed CLIs expose these commands:

```bash
codex plugin marketplace add "$PWD"
codex plugin add local-translation@sealad886-codex-marketplace
```

For GitHub Copilot CLI:

```bash
copilot plugin marketplace add "$PWD"
copilot plugin install local-translation@sealad886-codex-marketplace
```

These commands register/install in the selected client's settings; use a test
profile/home for an isolated check. If the marketplace is already registered,
inspect its source before adding another registration. For a temporary Copilot
session with the source package, the CLI also supports
`copilot --plugin-dir "$PWD/plugins/local-translation"`. Open the plugin settings
after installation and verify eleven model-facing tools and the twenty skills. Installation alone does not verify live inference or
multi-agent execution. Consult your installed client's help if its commands differ.

The native settings modal requires a host with MCP Apps and the `openai/settings`
extension. Its five app-only settings/model-discovery operations are hidden from the model's
tool catalog. Codex desktop provides this surface. A CLI that cannot render MCP
Apps can still use saved engine settings or the explicit deployment-file
environment route. The plugin never falls back to launching an external browser.

## Implemented scope

- Inline UTF-8 plain text or explicit text segments through MCP; multiple
  job-supplied source and target locale codes.
- Optional sampling and per-request output controls, plus caller-managed
  structured requests with provider-dependent JSON/schema response formats.
- Shared model-specific preparation recipes and caller-owned request examples,
  with explicit profile, API and execution limits; narrowly forwarded
  `chat_template_kwargs.enable_thinking` for tokenization/completion consistency.
- Frozen job inputs and configuration, local model checks, prompt tokenization,
  response/termination validation and supported invariant checks.
- Plain prose treats percentages literally; explicit JSON segments can declare
  `format: "printf"` for printf-placeholder and argument-order checks.
- Per-locale drafts, visible failures, query records, digest-bound revisions and
  independent-actor review records bound to the inspected shared-context revision,
  and a gated delivery candidate manifest.
- Expert-agent assignments, direct or PM-relayed conversations, bounded correction
  rounds, shared-change propagation, and human scope/content/acceptance decisions.

The runtime is synchronous, single-user local tooling. It does not implement the
supporting proposal's full HTTP gateway, asynchronous scheduling, cancellation,
multi-user authorization, model fallback or automatic model deployment. A client
needs a real delegation API to execute the multi-agent workflow. Role prompts
alone do not create agents; an unavailable capability must be reported.

## Formats and quality limits

This release does not extract or reconstruct arbitrary Markdown, PDF, DOCX, app
string catalogs or audiovisual media. The AV role/workflow references explain
what additional verified media and tools a commissioned service needs. A
translation from a verified transcript remains a text candidate until the timed
track, accessibility, conformance and playback work is actually performed.

A distinct reviser agent provides a separate AI pass, not qualified human revision
or ISO conformity. Structural checks and successful inference do not establish
meaning, completeness of every idea, product accuracy or publication quality.
`translation_prepare_delivery` returns a candidate manifest and each locale's
content through MCP. The actual human release owner must accept the identified
content or caller-retained files; this package does not publish them.

Read [acceptance evidence](skills/.shared/references/acceptance.md),
[format boundaries](skills/.shared/references/formats.md),
[security](SECURITY.md), and [source provenance](skills/.shared/references/provenance.md).

## Contributing and verification

Keep runtime/tool schemas, all role skills, shared protocols, examples, both MCP declarations and both
plugin manifests aligned. Preserve caller originals, immutable inline inputs,
temporary-session cleanup, returned-content identities, current-digest review
gates, visible partial failure, local endpoint restrictions and human decision
rights.
Do not add another format or runner by flattening unsupported input or bypassing
tokenization. Define the parser/runner contract and meaningful failure tests first.

From the marketplace root, use its existing Python environment with bytecode
writing disabled:

```bash
export PYTHONDONTWRITEBYTECODE=1
.venv/bin/python scripts/check_plugin.py plugins/local-translation --layout source
.venv/bin/python scripts/check_distribution_bundle.py plugins/local-translation
.venv/bin/python scripts/check_marketplace.py .
.venv/bin/python scripts/check_copilot_marketplace.py .
.venv/bin/python plugins/local-translation/mcp/server.py --self-test
.venv/bin/python -m unittest discover -s tests -p 'test_local_translation.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_local_translation_settings.py' -v
```

When catalog inputs change, regenerate the Copilot catalog with
`.venv/bin/python scripts/check_copilot_marketplace.py --write` first. For shared
catalog/packaging changes, validate every catalog package and run the marketplace,
Copilot, manifest and distribution regression suites as CONTRIBUTING requires.
Inspect the final distribution for manifests, MCP declarations, runtime, examples,
skills and referenced resources. Perform isolated client discovery/installation
checks where the clients are available; report unavailable checks honestly.

Deterministic tests with a fake local runner establish tool behavior. They do not
establish real Index inference, bilingual quality, measured hardware fit, verified
egress confinement or human acceptance. Record those as separate pilot evidence.

## License

Original plugin code and documentation use the [MIT License](LICENSE). Model
weights and runner dependencies retain their own licenses and are not bundled.
Reproduced upstream Homura/NativeLong prompt excerpts retain
[Apache License 2.0](skills/.shared/references/index-upstream-LICENSE.md) and their
source attribution in the selected profile references.
