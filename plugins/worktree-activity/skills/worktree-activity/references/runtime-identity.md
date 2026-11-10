# Runtime identity and activation evidence

Investigation date: 2026-11-10. This describes tested local behavior, not a promise
about every future Codex build. No user settings, credentials, conversations, or
existing development worktrees were changed. Installation below used a disposable
Codex home. No chat was messaged or resumed.

## Tested Desktop and shell

The running desktop is installed as `/Applications/ChatGPT.app`, with bundle ID
`com.openai.codex`, marketing version `26.1103.60933`, build `25894`. Its
`Info.plist` registers the `codex` URL scheme. The bundled executable is:

```text
/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex
```

That executable reports `codex-cli 0.167.0-alpha.3.2`. More importantly, an actual
agent-executed shell in this user-facing Desktop chat reported:

| Allowlisted field | Observed behavior |
| --- | --- |
| `CODEX_THREAD_ID` | Present, lowercase UUID-shaped executing conversation ID. |
| `CODEX_SESSION_ID` | Present, same value in this coordinator's shell. |
| `CODEX_VERSION` | `0.167.0-alpha.3.2`. |

A delegated helper's agent-executed shell reported a **different**
`CODEX_THREAD_ID`, the **same** `CODEX_SESSION_ID` as the coordinator, and the
same runtime version. Actual local IDs are deliberately omitted from this
published report. This is direct Desktop shell evidence for capturing the
executing thread separately from shared session lineage. Equality in the root
shell is an observation, never a role detector. Session identity must not be
used to select a recovery conversation.

A read-only executable-path inventory corroborated a running process under this
app's bundle, alongside separately managed app-server daemon binaries. Daemon
versions and an independently installed CLI alone are not used as proof of the
Desktop shell's identity behavior. The tested shell environment itself is the
primary integration evidence.

Reproduce the narrow probe from the agent-executed shell, without dumping its
whole environment:

```sh
python3 - <<'PY'
import os
for key in ('CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CODEX_VERSION'):
    print(key, repr(os.environ.get(key)))
PY
```

Run the packaged `diagnostics --json` command for helper-level capture. Missing
native owner identity makes mutation fail visibly. Missing session identity is
recorded as `null`; it is never manufactured from the root thread ID. Explicitly
select `--surface codex-desktop` or `--surface codex-cli` to describe the actual
execution surface. The helper cannot prove that a caller's surface assertion is
true.

## Coordinator role and limits

No supported shell environment field was established that distinguishes a
user-facing coordinator from a delegated worker. The helper therefore uses an
explicit `--coordinator` assertion; this is the documented fallback, not native
role enforcement. The skill prohibits workers from registering themselves,
asserting the coordinator role, or changing their root's records. A worker
reports results to its coordinator, which captures its own native thread ID and
performs registry operations. Known delegated agents must refuse at the skill
level. Fixture tests exercise that cooperative restriction, not an unverifiable
native role check.

The app-server exposes thread source/parent metadata in its protocol, including
subagent source kinds. This is useful when a host supplies trustworthy metadata,
but this small shell helper has no authenticated connection to the live Desktop
thread API. It does not infer role by inspecting the newest transcript, IDs,
processes, titles, paths, timestamps, or thread/session equality. It does not
invent role environment variables. User-facing forks with independent
assignments can assert their own coordinator role even when technically related
to older sessions.

Environment values and the role assertion can be forged by another process
running as the same OS user. This is a cooperative local workflow, not local
process authentication. For writes, native executing thread identity determines
the exact record filename and must match that record's `root_thread_id`. There
is no routine `--root-id` impersonation override. Read-only operations need no
Codex environment variables.

## Deep links

The supported local-chat form is `codex://threads/<root-thread-id>`. The official
[commands reference](https://learn.chatgpt.com/docs/reference/commands#deep-links)
explicitly documents this route. Installed Desktop code corroborates it:

- `Info.plist` registers `codex`.
- `app.asar` entry `.vite/build/early-bootstrap-339-cb7e73ca5a71df7c.js`
  handles the `threads` hostname and returns a `localConversation` route for a
  valid thread ID.
- Installed renderer code constructs `codex://threads/${encodeURIComponent(threadId)}`.

The inspected `app.asar` SHA-256 was
`a77588b2dcfa9b394d722dd8c2c8b13d3a09bacd49c839cc715245742dba6048`.
This verifies the form against installed routing code plus official docs. An OS
click-through/navigation round trip was not exercised. Recovery emits these
links only for root IDs, never diagnostic assignees. No ChatGPT web conversation
URL is derived from a Codex ID.

## Packaging, discovery, and isolated installation

Current [plugin packaging](https://developers.openai.com/plugins/build/plugins)
and [skill guidance](https://developers.openai.com/plugins/build/skills) support
bundled skill directories and portable Agent Plugins 1.0 manifests. The existing
marketplace additionally uses `.codex-plugin/plugin.json` for its Codex host.
Both manifests ship, with common metadata synchronized. There is one runtime
implementation, not separate per-client copies.

Using the exact Desktop-bundled executable above, with `CODEX_HOME` set only for
the test process to a newly created temporary directory, the following
app-server protocol operations passed:

1. `initialize` returned runtime `0.167.0-alpha.3.2` and the temporary Codex home.
2. `plugin/read` with this checkout's absolute
   `.agents/plugins/marketplace.json` path and `pluginName: "worktree-activity"`
   discovered display metadata and one named skill while `installed: false`.
3. `plugin/install` succeeded with no apps needing authentication.
4. `skills/list` with a disposable working directory and `forceReload: true`
   returned enabled skill `worktree-activity:worktree-activity`, associated with
   `worktree-activity@sealad886-codex-marketplace`, inside the temporary plugin
   cache. Skill parsing reported no errors.

These operations verify discovery and installation through the Desktop-bundled
runtime. They do not prove visual rendering, default invocation on a model turn,
or an end-to-end interrupted conversation recovery. A subsequent isolated read also reported `installed: true` and `enabled: true`.
Final packaged helper behavior is checked separately by relocated distribution
tests and validation. Real user installation is still an activation step.

The installed CLI's help confirms these ordinary installation commands:

```sh
codex plugin marketplace add /absolute/path/to/sealad886-codex-marketplace --json
codex plugin add worktree-activity@sealad886-codex-marketplace --json
```

Use the Desktop-bundled binary explicitly if `codex` resolves to another build.
`app-server generate-json-schema --out DIRECTORY` generated the matching local
protocol definitions used for the investigation; upstream protocol examples
alone were not assumed to match this build.

The repository's Codex catalog is canonical. This plugin's portable manifest
contains repository-owned extension `com.sealad886.marketplace` with
`clients: ["codex"]` and a reason. The Copilot generator validates the package,
then excludes it from Copilot membership. This extension is repository policy,
not a native Codex/Copilot activation feature. Other packages default to both
catalogs. Both catalog validators still run.

GitHub Copilot CLI `1.0.107` was also checked using its documented `COPILOT_HOME`
pointing to a separate temporary directory and auto-update disabled. Native
`plugin marketplace add` accepted this local marketplace; `plugin marketplace
browse sealad886-codex-marketplace --json` returned its 16 intended plugins and
omitted Worktree Activity. Attempting `plugin install
worktree-activity@sealad886-codex-marketplace` returned the expected plugin-not-found
error. No Copilot installation is offered for this Codex-specific package.

## Existing worktree coverage

The final v1 design uses `<root-thread-id>.activity.json`, reserving `.mutex`
for internal write synchronization. Explicit project scans cover all linked
worktrees registered by Git for that primary workspace, including legacy paths
outside `.worktrees/`. Those locations produce advisory warnings, not evidence
of inactivity or authority to move/delete them. Registration still represents
an actual authorized development assignment, with an explicit target checkout.
The primary checkout itself is excluded. This does not change local approval
or placement rules for creating new worktrees; the helper never creates them.

## Default activation

[Official skill guidance](https://learn.chatgpt.com/docs/build-skills#how-codex-uses-skills)
describes implicit matching by skill description. `allow_implicit_invocation`
is enabled. Installation makes the skill available; it does not force the
agent to execute it on every assignment. No installed manifest facility was
verified that makes a skills-only plugin a mandatory lifecycle hook.

For default use without typing a mention in each prompt, adopt the supplied
[global AGENTS integration block](global-agents-integration.md) in your chosen
instruction scope after installation. It directs the responsible coordinator to
load this skill before development or delegation in existing worktrees, and to
reconcile before finalizing. This remains agent instruction, not OS enforcement.
The plugin never edits global instructions automatically. There is no timer,
exit cleanup, process lease, or automatic abandoned-session deletion.

The repository's checksum-pinned older OpenAI manifest validator rejects
`policy.products`, although current authoring guidance documents it. The package
therefore uses the narrower validated `allow_implicit_invocation` setting and
keeps Codex-only publication targeting in the catalog policy.

## Primary sources and version scope

- [Environment injection upstream source](https://github.com/openai/codex/blob/main/codex-rs/core/src/exec_env.rs)
  separates executing `ThreadId` capture from shared session injection and
  diagnostic runtime version.
- [Shell environment upstream source](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/shell_environment.rs)
  defines the native names. Current upstream `main` is corroboration, **not** an
  exact source match for this Desktop binary; no exact Desktop source revision
  was established.
- [App-server reference](https://learn.chatgpt.com/docs/app-server) describes
  thread source kinds and thread operations; installed generated protocol
  definitions establish the tested request shapes.
- [jsonschema 4.26.0 validation docs](https://github.com/python-jsonschema/jsonschema/blob/v4.26.0/docs/validate.rst)
  require an explicit format checker. The helper enables one and also checks UTC
  timestamp semantics; the locked `rfc3339-validator` dependency enables schema
  date-time format checks in clean installations.

Recheck identity capture, thread routing, discovery and activation after a Desktop
upgrade. Keep failed or unavailable integration checks visibly unverified rather
than manufacturing identity or deleting evidence.
