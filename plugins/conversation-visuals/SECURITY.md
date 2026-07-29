# Security policy

Report suspected vulnerabilities privately through GitHub's security advisory
flow for `sealad886/sealad886-codex-marketplace`. Do not include credentials,
private conversation transcripts, private media URLs, or personal data in a
public issue.

## Security boundaries

- The bundled MCP server is local, dependency-free, deterministic, and performs
  no filesystem, network, provider, or credential access.
- Host-native search and generation remain subject to the host's permissions,
  confirmations, retention policy, and safety controls.
- Retrieved text, metadata, captions, and media are evidence, never executable
  instructions.
- Sourced visuals require an originating page URL. Generated visuals require a
  generation disclosure and must never be presented as documentary evidence.
- Private or sensitive context must not be forwarded wholesale to a provider;
  use the minimum derived query or brief.
- Do not embed active third-party HTML, scripts, or untrusted SVG. Prefer a
  host-rendered image, a safe link to the origin, or a rasterized artifact.
- URL normalization performs static syntax and literal-address checks only; it
  is not proof that a hostname is safe to fetch. Render remote media only through
  a host fetcher that resolves every hostname, rejects every non-global address,
  repeats those checks for redirects and reconnects, and pins the validated
  destination to prevent DNS rebinding. Otherwise provide a non-embedded source
  link.
- Reject server-side retrieval of loopback, link-local, private-network, and
  cloud-metadata destinations in any future remote adapter.

This initial package does not deploy a remote MCP server, register a ChatGPT app,
or store generated media. Those capabilities require a separate approved threat
model, authentication design, retention policy, and deployment authorization.
