# Mindrally skills plugin delivery

Source: [Mindrally/skills](https://github.com/Mindrally/skills), pinned to
`7682ca77710e0971eab4e0ae5dddfa281aea0ba5` (265 skills, Apache-2.0).
The source inventory records every skill's path and SHA-256 before adaptation.

## Authorized outcome

Ship all 265 separately discoverable skills in one `mindrally-skills` plugin,
valid for Codex and GitHub Copilot. Review every source skill individually,
correct unsupported or obsolete guidance, and move conditional technical detail
into directly linked references. Preserve the upstream license and attribution.
Commit milestones, push the verified remote, use the Iterating PR Bot Fixes
lifecycle, and publish after review and repository gates pass. Install the
published package, remove this package's development installs, and disable skills
irrelevant to development projects worked on since 2026-08-31.

## Checklist

- [x] Inventory and individually audit the 265 source skills.
- [x] Integrate the package, provenance, catalogs, and meaningful validation.
- [ ] Commit, push, and complete bounded independent and configured PR reviews (active).
- [ ] Merge and publish the validated plugin and marketplace release.
- [ ] Install the published package, remove development variants, and verify
      per-skill enablement against recent project evidence.

## Review method

Three non-overlapping audit batches own their assigned skill directories and
per-skill audit records. Each reviewer reads each complete source skill,
checks technical claims against current primary documentation, and writes
specific corrections and documentation links. Preserve skill identity and
capability coverage; do not count mechanical splitting or lint as accuracy review.
Keep metadata concise, workflow essentials in `SKILL.md`, and conditional
API/configuration/examples in the skill's `references/` directory. Every skill
retains the repository's invocation, evidence, workflow, handoff, completion,
and authority contract. Unavailable runtime validation remains explicit.

## Milestones and boundaries

1. Pinned source inventory and review plan.
2. Complete audited skill package and cross-client catalogs.
3. Review corrections and final release evidence as needed.

Use the existing checkout on `codex/mindrally-skills-plugin`; no new worktree.
Only the coordinating agent stages and commits. Preserve unrelated work and
user settings during isolated tests. User plugin enablement changes occur only
for this package after publication. Do not change billing or review settings.
