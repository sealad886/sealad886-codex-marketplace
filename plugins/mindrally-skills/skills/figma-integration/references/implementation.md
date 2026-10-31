# Figma Integration Guidelines: implementation guidance

## Design interpretation

Figma auto-layout, constraints and variants inform code but do not prescribe a
one-to-one DOM/component tree or exact CSS layout. Reuse existing design-system
primitives, preserve semantic accessible controls, and check responsive behavior
instead of inferring all breakpoints from one frame. Verify font licensing and
availability, typography, density, token aliases and component states. Export SVG
or raster at the target size with ownership/provenance; do not turn all text into
images or load oversized assets by default.

## API and host boundaries

The REST API exposes file, nodes and image-render endpoints; a global figma.getFile/
getNode/getImages object is not a standard browser API. Distinguish REST clients,
Plugin API and discovered MCP tools. This skill installs no Figma server and cannot
guarantee Cursor Composer auto-invocation or approval behavior in Codex/Copilot.
Use actual connected tool capabilities and account access, narrow node requests,
handle rate limits/expired asset links, and keep tokens private. Writing back to
Figma, posting feedback, or publishing previews requires user authority. Visual
matching alone does not establish usability or accessibility.

## Primary documentation

- [File/node endpoint contracts](https://developers.figma.com/docs/rest-api/file-endpoints/).
- [Official MCP integration and availability](https://developers.figma.com/docs/figma-mcp-server/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
