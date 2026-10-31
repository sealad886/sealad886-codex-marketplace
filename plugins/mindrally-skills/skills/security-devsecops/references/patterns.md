# Security throughout delivery: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use NIST SSDF/OWASP practices to select appropriate controls; do not claim standards compliance from a tool list or one scan.

- Differentiate SAST, dependency/SCA, secret, IaC, and dynamic testing; their coverage overlaps but none proves absence of vulnerabilities.

- Inspect scanner commands and data destinations before exporting private source or invoking paid services. Dynamic tests need an authorized environment and traffic scope.

- Pin trusted CI actions/dependencies, minimize token permissions, and isolate untrusted PR execution from privileged secrets and deployment jobs.

- Package popularity/download counts are weak signals; verify publisher/source, maintenance, integrity, lifecycle scripts, and vulnerability applicability.

- Do not blindly audit mutable latest image tags as proof of a released image; bind results to immutable digest/version and revision.

- JSON.parse of data is not inherently executable deserialization; assess dangerous object use, eval/template sinks, prototype handling, and unsafe loaders separately.

- Credential revocation, live policy changes, deployments, and external issue publication require corresponding task authority. Preserve actionable findings and time-bounded exceptions.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [SSDF provides security practices integrated into the development lifecycle.](https://csrc.nist.gov/pubs/sp/800/218/final)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
