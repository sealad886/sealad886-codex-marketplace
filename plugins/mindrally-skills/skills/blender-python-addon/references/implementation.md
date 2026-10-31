# Blender Python Add-on Development: implementation guidance

## Packaging and bpy contracts

Blender 4.2+ Extensions use blender_manifest.toml and extension packaging; legacy
bl_info add-ons are a separate supported-version choice. Validate the actual
manifest and package rather than mixing formats. Register classes in dependency
order and unregister in reverse; remove owned properties, handlers, keymaps,
timers, and subscriptions. PropertyGroup data does not automatically make arbitrary
operations undo-safe. AddonPreferences can persist settings, but API keys there
are not automatically encrypted or protected.

## Context, data, and performance

Operators need poll checks for object type/mode/selection and valid return sets.
Use invoke for interaction and execute for work; do not mandate optional bl_options
on every operator. Read evaluated data via the depsgraph where needed, and manage
temporary mesh ownership. Use bmesh appropriately for edit versus object mode.
Panel.draw should read and lay out UI, without destructive scene edits. Modal/timer
work must yield and clean up; Blender Python API access is not generally thread-safe.
Use explicit user actions for destructive edits/file replacement. Test actual color
attribute domain/type and undo semantics instead of assuming all mesh layers match.

## Primary documentation

- [Blender 4.2 extension migration and manifest](https://docs.blender.org/manual/en/4.2/advanced/extensions/addons.html).
- [Blender Python threading limits](https://docs.blender.org/api/current/info_gotchas_threading.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
