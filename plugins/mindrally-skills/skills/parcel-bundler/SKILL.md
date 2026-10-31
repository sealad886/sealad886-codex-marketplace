---
name: parcel-bundler
description: "Use when configuring Parcel entries, targets, assets, CSS/TypeScript transforms, code splitting, or development proxying."
---

# Parcel Bundler

## When to invoke

Use for configuring Parcel entries, targets, assets, CSS/TypeScript transforms, code splitting, or development proxying.

## Inputs and evidence

Inspect Parcel/Node/plugin versions, entry/target metadata, package type, browser targets, dependency workflow and generated output ownership. Inspect the installed versions and repository conventions before
choosing APIs or adding dependencies.

## Workflow

Read [implementation guidance](references/implementation.md) when selecting the
relevant patterns, APIs, or failure checks; load only the sections needed.

1. Use the existing entry and target graph with minimal supported configuration.
2. Configure necessary transforms, asset URLs and environment exposure.
3. Build production artifacts and separately run TypeScript checking where needed.
4. Inspect runtime paths, code splitting/proxy behavior and package output under target conditions.

## Outputs and handoff

Report the changed behavior, affected interfaces, validation results, and any
version or environment limitations. Keep operational commands reviewable.

## Completion evidence

Production artifacts build/type-check and targeted browser/library tests confirm asset paths, exports and environment safety.

## Must not

Do not delete existing build/configuration or auto-install packages merely to diagnose a build. Do not expose credentials, modify unrelated work, or treat this
skill as authority to deploy, publish, incur costs, or change external systems.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
