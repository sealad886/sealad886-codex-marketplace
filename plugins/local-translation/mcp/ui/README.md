# Settings popup source

`../setup.html` is the prebuilt MCP App served by the plugin's Python MCP server.
The installed plugin needs Python only. It does not start a browser page or HTTP
server, and the popup loads no CDN scripts, fonts, styles, or other network assets.

To rebuild after editing `settings.js` or `setup.template.html`, use Node 20 or
newer and npm:

```sh
node plugins/local-translation/mcp/ui/build.mjs
```

The script installs the exact lockfile dependencies into a temporary directory,
bundles the official `@modelcontextprotocol/ext-apps` SDK and controller into the
HTML, updates `THIRD_PARTY_NOTICES.md`, then removes the temporary directory. It
does not create `node_modules` or an npm cache inside the plugin. Rebuilding needs
registry access; running the installed popup does not.

Before writing the artifact, the build verifies that the HTML preserves exactly
one complete inline bundle and parses that emitted script with Node's `vm.Script`
without executing it. Dollar sequences in bundled code remain literal.

The native host opens the modal from the `translation_open_settings` tool's UI
resource association. The controller uses `App.callServerTool` for app-only
`translation_read_settings`, `translation_save_settings`, and
`translation_migrate_settings`. Read prefill comes from the response's private
`_meta["local-translation/settings"]` object. The SDK's standard handshake supplies
the host theme and style variables.

The controller sends no chat messages, model-context updates, or persistent UI
state. It never prefills a saved key. The masked field retains an entered key for
that screen’s lifetime, including validation errors, failed saves, pending calls,
and any successful result still visible before the host closes it. It clears
only on actual resource teardown, page hide, or refresh/reload. No key is stored
in localStorage, sessionStorage or widget state. It shows only fixed safe errors.
The private save call carries an entered key directly to the MCP server; its
transient payload copy is deleted after the call. No claim is made about
arbitrary host debug logging.

Success and Cancel call the documented `window.openai.requestClose()` when the
host injects it. Otherwise the official SDK’s `App.requestTeardown()` sends
`ui/notifications/request-teardown` to request dismissal of the entire resource.
The host decides whether to close it; standard MCP Apps teardown invokes
`onteardown` before unmounting.
If a host leaves the form visible, the typed key remains masked until the user
closes or refreshes it. Interrupted saves require a reload to check current
settings before retry.

The form needs only an endpoint and model name or ID, plus an optional API key.
Generation limits have defaults and can be omitted. Target languages are supplied
with each translation request.

The explicit migration button backs up earlier settings before converting them
to the current endpoint/model configuration through the existing server migrator.
Migration never runs automatically. Environment-supplied configuration remains read-only.

Bundled package versions and their complete upstream license/NOTICE files are
recorded in `THIRD_PARTY_NOTICES.md`. Build dependencies remain in the lockfile;
they are not required by users installing the plugin.
