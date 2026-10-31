# Tauri application boundaries: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Tauri v2 invoke imports from @tauri-apps/api/core; old @tauri-apps/api/tauri and tauri::api::path examples belong to v1.

- V2 uses capabilities/permissions and plugin scopes; the old tauri.conf.json allowlist is not the v2 security model.

- Custom commands must enforce their own input/resource authorization; exposing read_file(path) or write_file(path,content) with arbitrary paths grants broad filesystem access.

- Resolve paths against approved roots, account for traversal/symlink behavior, bound file sizes, and avoid exposing raw secret-bearing OS errors.

- Unlisten event handlers when component/context ownership ends, including async registration races.

- Keep blocking file/CPU work off latency-sensitive runtime threads using the appropriate supported execution model.

- Frontend framework/styling is optional; Next.js usually requires a suitable static/export architecture rather than assuming an embedded Node server exists.

- Desktop/mobile permissions, native plugins, signing, updater signatures, and platform acceptance require separate checks; one web build is insufficient.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [V2 invoke comes from api/core and event listeners require lifecycle cleanup.](https://v2.tauri.app/develop/calling-rust/)
- [V2 capabilities constrain frontend access to supported native permissions.](https://v2.tauri.app/security/capabilities/)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
