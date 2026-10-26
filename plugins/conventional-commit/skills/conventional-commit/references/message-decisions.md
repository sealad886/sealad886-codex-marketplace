# Choose a message from the resulting behavior

Use this guide when the type, scope, breaking marker, or revert meaning is
unclear. First inspect the selected diff, its callers and tests, repository
history, contribution guidance, commit lint rules, and release configuration.
The subject describes this commit's observable outcome. It does not certify
tests passed, assign a version, or authorize publication.

## Type and scope

Use the repository's accepted vocabulary. These common choices distinguish the
kind of change rather than the file extension or size of the patch:

| Evidence in the selected change | Candidate type | Check before choosing |
| --- | --- | --- |
| Adds a supported capability | `feat` | Identify who can now do what |
| Corrects behavior against an existing requirement | `fix` | Cite the defect and its expected behavior |
| Restructures implementation while preserving behavior | `refactor` | Check public and dynamic consumers, side effects and failure semantics |
| Improves measured runtime/resource behavior | `perf` | State the evidence and preserve required results |
| Changes prose/examples only | `docs` | An executable example can still change a documented contract |
| Changes tests only | `test` | Tests accompanying a fix usually stay in that fix's group |
| Changes packaging, compiler inputs or dependency tooling | `build` | A dependency update may also change shipped behavior |
| Changes CI workflow behavior | `ci` | Check triggers, permissions and resulting checks |
| Changes formatting only | `style` | No behavior or semantic configuration changes |
| Performs maintenance outside the other types | `chore` | Do not hide a feature or defect correction here |
| Reverses a specific earlier change | `revert` | Verify the actual net reversal as described below |

For a group with one outcome, choose the type that explains that outcome; its
tests and documentation need no separate commits merely to obtain matching
types. Split independent outcomes when each remains coherent and reviewable.
Do not change correct classifications merely to steer a release tool.

Choose a scope only if it helps the reader locate a stable responsibility such
as `parser`, `auth`, or `ci`. Prefer established scopes over an invented taxonomy.
One touched filename is not necessarily the right scope. Avoid a misleading
narrow scope for a cross-cutting change; omit it when no useful scope exists.

## Breaking changes need a concrete consumer impact

Check the accepted interface, supported users and version policy. A removed API,
renamed required configuration key, changed CLI output contract or incompatible
data format can break consumers despite a small diff. An internal rename with
no observable impact usually does not. A defect correction can be breaking when
supported callers must change; assess the contract rather than the intention.

When breaking, use the repository's required `!` and `BREAKING CHANGE:` footer.
This skill's default requires both. Explain the affected consumer, prior and
new behavior, and the concrete migration. Do not bury the footer in the subject
or body, claim a migration happened, or invent a legacy adapter merely to avoid
calling a change breaking.

```text
feat(config)!: require an explicit storage directory

Reject ambiguous process-relative paths so deployments use the intended store.

BREAKING CHANGE: Callers must provide storage.directory as an absolute path;
the former implicit current-directory default is removed.
```

The marker reports compatibility impact, not permission to apply a production
migration. Keep unresolved contract questions visible; do not guess the answer
from patch size, a `0.x` version, or a previous commit's message.

## Reverts, partial reversals and follow-up fixes

Inspect the referenced commit and the current tree. A true revert reverses its
effect in the current context; check what remains when later commits depend on
it. Use a repository-valid subject such as `revert(parser): restore the prior
token limit`, and put the full reverted hash and reason in the body. The hash
identifies intent but does not prove the resulting tree is correct.

If only one branch of an earlier change is corrected, describe that resulting
behavior as a `fix` or other applicable type, with the earlier hash in the body.
Do not call a selective repair a complete revert. A revert of a revert may
restore a capability or reintroduce an incompatibility: examine the net effect
and the repository's convention. Running `git revert`, creating its commit,
rewriting history or reverting a published deployment requires its own scope
and authorization; choosing wording grants none.

## Check actual automation without taking release authority

Read the configured parser, allowed scopes, ignored paths/types, breaking-footer
rules and branch/release rules. For example, a configured `docs` release rule
may publish documentation packages, while another repository may ignore it.
Report what the inspected configuration will interpret and what remains
unverified. Use an existing read-only parser/check when available; inspect it
before execution because a release command's default can perform writes.

Do not infer a SemVer bump, edit version sources, create tags, run release jobs,
or depend on a separate versioning plugin under a local commit request. If
wording and automation disagree, report the concrete mismatch and follow the
controlling convention; do not mislabel the change to suppress or trigger a
release. Re-read the final message after hooks, since the stored message is
what downstream tools consume.

Primary references: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
for message syntax and compatibility signals; [git revert](https://git-scm.com/docs/git-revert)
for the operation's effects. Repository policy and configured automation supply
the project-specific classification and publication behavior.
