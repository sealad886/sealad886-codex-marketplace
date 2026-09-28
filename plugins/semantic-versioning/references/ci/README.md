# CI reference index

Load only the needed page:

- [GitHub Actions](github-actions.md): complete inactive workflow templates, assembly instructions, tool versions, identity and authorization prerequisites.
- [Recovery](recovery.md): partial releases, collisions, retry evidence, promotion and emergency patches.
- [Other providers and packaging recipes](other-providers.md): adaptations for non-GitHub CI and mobile/Ruby/PHP/C++/plugin publication.
- [Native configuration examples](../../templates/native/README.md): concrete GoReleaser, Maven, Gradle and Rust prerequisites.
- [Action pin evidence](action-pins.md): immutable action revisions and their upstream references.
- [Release tools](../tools/release-tools.md): version owner selection and native Release Please, Changesets, semantic-release configuration.

Hosted publishing has not been exercised. Static validation, local package builds, installed-plugin behavior, and registry publication are separate evidence levels. Templates use `.yml.template` so packaging them never activates a release workflow.
