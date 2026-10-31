# Salesforce source-driven workflow: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use supported `sf project deploy start` and `sf project retrieve start` commands for the installed CLI; old sfdx force:source push/pull examples are not current defaults.

- Check `sf ... --help` and plugin versions before selecting flags; source tracking availability differs by org type and configuration.

- Preview retrieval/deployment scope and preserve local changes before retrieval can overwrite them.

- Scratch-org creation consumes org resources; use explicit target/dev-hub identity and authorized lifecycle cleanup.

- Keep scratch definitions, features, metadata API versions, and seeding fixtures consistent with supported test scenarios.

- Do not commit auth files, refresh tokens, real production data, or local connection state.

- For LWC Flow/navigation use LWC targets/services rather than the Aura interfaces copied into old DX examples.

- Package version creation/promotion and org deployments are external operations requiring user authority; validation success alone is not publication.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [Current official deploy/retrieve plugin documents sf project deploy/retrieve command families.](https://github.com/salesforcecli/plugin-deploy-retrieve)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
