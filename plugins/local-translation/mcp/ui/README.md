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
state. It never prefills a saved key, clears the password field on submission,
failure, cancellation, page hide, and resource teardown, and shows only fixed
safe error messages. The private save call carries an entered key directly to
the MCP server; no claim is made about arbitrary host debug logging. Cancel
clears the form's key and ends editing; the host's close button dismisses the
popup. Interrupted saves require a reload to check current settings before retry.

The explicit migration button backs up the earlier workspace-format settings
before converting them through the existing server migrator. Migration never
runs automatically. Environment-supplied configuration remains read-only.

Bundled package versions and their complete upstream license/NOTICE files are
recorded in `THIRD_PARTY_NOTICES.md`. Build dependencies remain in the lockfile;
they are not required by users installing the plugin.
