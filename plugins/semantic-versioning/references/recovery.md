# Publication recovery

Read for an interrupted release, collision, promotion, or backport.

First pin repository, unit, channel, tag/commit, artifact digests, registry, workflow run and authorization. Read remote state before retrying. Do not log credential values.

| Observed state | Next safe action |
|---|---|
| Tag/release exists; package absent | Recover the exact validated artifact and resume the native publish step under authority. A new Release Please run may report no new release; use the documented exact-version recovery dispatch. |
| Some workspace packages exist | Compare existing versions and artifact identity, skip only verified successes, then resume missing packages in dependency order. |
| Version exists with matching artifact | Record success and run consumer verification; do not republish. |
| Version exists with different or unprovable artifact identity | Stop. Investigate registry normalization and provenance. Never treat all HTTP failures as absence or silently skip a collision. |
| Credentials/OIDC unavailable | Report failed capability/prerequisite; do not fall back to a broad stored token automatically. |
| Tag points to unexpected commit | Stop before publication. Preserve evidence; immutable releases require a corrective release. |
| Registry published but consumer verification fails | Record incomplete release acceptance; diagnose package contents/platform constraints before a corrective release. |

For retries, verify remote existence with an authenticated registry-specific command and distinguish not-found from authorization, rate-limit, network, and server failures. Reuse validated artifacts where possible. Rebuilding requires a new artifact identity and renewed checks; source identity alone is not byte identity.

Preserve failed-run artifacts/checksums long enough for the repository's recovery window. Emergency fixes use the affected maintenance baseline and normal contract assessment, with compressed review rather than erased gates. Rollback of deployment or channels is separately authorized and does not delete/reuse package versions.

Publication is verified only after registry readback plus appropriate install/download/import or artifact-consumption checks. Report local validation, hosted execution, remote publication, and consumer acceptance separately.
