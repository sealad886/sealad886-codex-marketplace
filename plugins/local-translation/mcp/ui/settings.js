import { App, applyDocumentTheme, applyHostStyleVariables } from "@modelcontextprotocol/ext-apps";

const element = (id) => document.getElementById(id);
const form = element("settings");
const fields = element("fields");
const key = element("api_key");
const credentialAction = element("credential_action");
const save = element("save");
const cancel = element("cancel");
const reload = element("reload");
const migrate = element("migrate");
const status = element("status");
const textFields = ["base_url", "model"];
const numericFields = ["max_input_chars", "max_prompt_bytes", "max_output_tokens", "context_window_tokens", "timeout_seconds", "run_timeout_seconds"];

// Keep the key in the masked input for this screen’s lifetime.
// Only the in-flight private tool call receives a transient copy.
// Never send settings through messages, model context, logs, or persistent UI state.
const app = new App({ name: "Local Translation settings", version: "0.5.0" }, {}, { autoResize: true, strict: true });
let expectedRevision = null;
let connected = false;
let busy = false;
let editable = false;
let ended = false;
let needsMigration = false;

const safeErrors = {
  invalid_input: "Enter valid engine settings. Nothing was saved.",
  invalid_credential: "Enter a nonempty API key without line breaks, or choose Keep or Clear. Nothing was saved.",
  local_settings_failed: "Could not read or lock private settings. Check local file permissions and close other settings popups, then reload.",
  settings_busy: "Another settings save is active. Nothing was saved. Wait for it to finish, then try again.",
  stale_configuration: "Settings changed while this popup was open. Nothing was saved. Reload saved settings before trying again.",
  verification_failed: "The engine compatibility check failed. Nothing was saved. Check the endpoint, exact model alias and chat tokenizer support.",
  model_unavailable: "The engine does not list this exact model alias. Check the served model name. Nothing was saved.",
  tokenizer_unsupported: "This engine must support POST /tokenize with chat messages and return a positive token count. Check your installed engine version. Nothing was saved.",
  runner_unreachable: "Could not reach this local engine. Start it, check the port and API key, then try again. Nothing was saved.",
  auth_required: "The engine requires a valid API key. Choose Use a new key and enter the key configured in oMLX or your runner. Nothing was saved.",
  save_failed: "Could not save private settings. Previous settings were preserved. Check local file permissions and try again.",
  environment_override: "The MCP launch environment supplies the active configuration. This popup is read-only until LOCAL_TRANSLATION_CONFIG is removed from that launch environment.",
  migration_required: "Back up and upgrade saved settings before editing the engine connection.",
};

function clearKey() { key.value = ""; }
function showStatus(message, tone = "") {
  status.textContent = message;
  status.dataset.tone = tone;
}
function updateControls() {
  fields.disabled = !editable || busy || ended;
  save.disabled = fields.disabled;
  cancel.disabled = busy || ended;
  reload.disabled = busy || ended || !connected;
  migrate.disabled = busy || ended || !connected;
  form.setAttribute("aria-busy", String(busy));
  key.disabled = fields.disabled || credentialAction.value !== "replace";
  key.required = !key.disabled;
}
function applyHostContext(context) {
  if (context.theme) applyDocumentTheme(context.theme);
  if (context.styles?.variables) applyHostStyleVariables(context.styles.variables);
  if (context.safeAreaInsets) {
    const { top, right, bottom, left } = context.safeAreaInsets;
    document.body.style.padding = `${top}px ${right}px ${bottom}px ${left}px`;
  }
}
function safeError(result, fallback) {
  return safeErrors[result?.code] || fallback;
}
async function call(name, args = {}, timeout = 150000) {
  return app.callServerTool({ name, arguments: args }, { timeout, resetTimeoutOnProgress: false });
}

async function loadSettings() {
  if (busy || ended) return;
  busy = true;
  editable = false;
  clearKey();
  credentialAction.value = "keep";
  showStatus("Loading saved settings…");
  updateControls();
  try {
    const response = await call("translation_read_settings", {}, 30000);
    if (ended) return;
    const settings = response._meta?.["local-translation/settings"];
    if (!settings || typeof settings !== "object") {
      reload.hidden = false;
      showStatus("The plugin did not return private settings. Reload, or close this popup and open Configure again.", "error");
      return;
    }
    expectedRevision = typeof settings.settings_revision === "string" ? settings.settings_revision : null;
    needsMigration = settings.migration_required === true || settings.code === "migration_required";
    element("migration").hidden = !needsMigration;
    reload.hidden = false;
    element("storage").textContent = typeof settings.settings_path === "string" ? `Settings file: ${settings.settings_path}` : "";
    if (needsMigration) {
      showStatus(safeErrors.migration_required);
      return;
    }
    if (settings.configured && settings.deployment && typeof settings.deployment === "object") {
      const deployment = settings.deployment;
      for (const name of [...textFields, ...numericFields]) {
        if (typeof deployment[name] === "string" || typeof deployment[name] === "number") element(name).value = deployment[name];
      }
    }
    if (settings.environment_override === true) {
      showStatus(safeErrors.environment_override);
      return;
    }
    if (response.isError || settings.error) {
      showStatus(safeError(settings, "Could not load private settings. Check local file permissions, then reload."), "error");
      return;
    }
    editable = true;
    showStatus(settings.configured
      ? (settings.credential_configured ? "Saved settings loaded. A saved API key is present; its value is hidden." : "Saved settings loaded. No API key is saved.")
      : "Enter your endpoint and model name or ID.");
  } catch {
    if (!ended) {
      reload.hidden = false;
      showStatus("Could not load private settings. Reload, or close this popup and open Configure again.", "error");
    }
  } finally {
    clearKey();
    busy = false;
    updateControls();
  }
}

credentialAction.addEventListener("change", updateControls);
reload.addEventListener("click", loadSettings);
async function closeScreen(message) {
  ended = true;
  updateControls();
  showStatus(message + " Closing configuration… If it remains open, use the popup’s close button.");
  // Use the host’s documented close API when injected. Other MCP Apps hosts
  // receive the standard teardown request. Neither path clears a visible input.
  if (typeof window.openai?.requestClose === "function") {
    try {
      await window.openai.requestClose();
      return;
    } catch {
      // A host may expose this optional API without supporting this view.
    }
  }
  try {
    await app.requestTeardown();
  } catch {
    showStatus(message + " Close this popup using its close button.");
  }
}
cancel.addEventListener("click", () => { closeScreen("Cancelled. Nothing was saved."); });
migrate.addEventListener("click", async () => {
  if (!needsMigration || busy || ended) return;
  busy = true;
  updateControls();
  showStatus("Backing up and upgrading saved settings…");
  try {
    const response = await call("translation_migrate_settings", {}, 30000);
    if (ended) return;
    if (response.isError) {
      showStatus(safeError(response.structuredContent, "Could not upgrade saved settings. Existing settings were preserved. Check local permissions and try again."), "error");
      return;
    }
    busy = false;
    await loadSettings();
    if (editable) showStatus("Saved settings upgraded with a backup. Review the engine connection, then test and save.", "success");
  } catch {
    if (!ended) showStatus("The upgrade response was interrupted. Reload saved settings to check their current state before trying again.", "error");
  } finally {
    busy = false;
    updateControls();
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!editable || busy || ended) return;
  const invalid = form.querySelector("input:invalid, select:invalid");
  if (invalid) {
    if (invalid.closest("details")) invalid.closest("details").open = true;
    invalid.reportValidity();
    invalid.focus();
    showStatus("Complete the required fields within their allowed limits. Your key remains in the masked field.", "error");
    return;
  }
  const payload = { deployment: {}, credential_action: credentialAction.value, expected_revision: expectedRevision };
  if (payload.credential_action === "replace") payload.api_key = key.value;
  try {
    const deployment = payload.deployment;
    for (const name of textFields) deployment[name] = element(name).value.trim();
    for (const name of numericFields) {
      if (element(name).value.trim() !== "") deployment[name] = Number(element(name).value);
    }
    busy = true;
    updateControls();
    showStatus("Checking the exact model and chat tokenizer…");
    const response = await call("translation_save_settings", payload);
    if (ended) return;
    const result = response.structuredContent;
    if (!response.isError && result?.saved === true) {
      expectedRevision = result.settings_revision;
      await closeScreen("Settings saved. Model and tokenizer checks passed.");
    } else {
      if (["stale_configuration", "environment_override", "local_settings_failed", "migration_required"].includes(result?.code)) editable = false;
      if (result?.code === "migration_required") {
        needsMigration = true;
        element("migration").hidden = false;
      }
      showStatus(safeError(result, "The compatibility check or save failed. Saved settings were preserved. Your key remains in the masked field. Reload settings before trying again."), "error");
    }
  } catch {
    if (!ended) {
      editable = false;
      showStatus("The save response was interrupted. Reload saved settings to check whether the save completed before trying again.", "error");
    }
  } finally {
    delete payload.api_key;
    busy = false;
    updateControls();
  }
});

app.onhostcontextchanged = applyHostContext;
app.ontoolinput = () => {};
app.ontoolresult = () => {};
app.ontoolcancelled = () => { closeScreen("Cancelled."); };
app.onteardown = async () => {
  clearKey();
  ended = true;
  updateControls();
  return {};
};
window.addEventListener("pagehide", clearKey);

async function start() {
  if (window.parent === window) {
    showStatus("Open this settings popup from the plugin’s Configure action inside the app.", "error");
    cancel.disabled = true;
    return;
  }
  try {
    await app.connect(undefined, { timeout: 15000 });
    connected = true;
    applyHostContext(app.getHostContext() || {});
    await loadSettings();
  } catch {
    clearKey();
    showStatus("Could not connect to the plugin. Close this popup and open Configure again.", "error");
  }
}
start();
