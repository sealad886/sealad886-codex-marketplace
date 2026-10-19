# Preservation and restoration proof

Read before transferring unique work or retiring a source whose recovery
depends on a backup. Use the existing ledger, secured storage outside
distributed source, and a deliberately selected scratch location. A backup's
existence never authorizes source deletion, worktree creation, or destructive
recovery into an active checkout. Inventory-only mode records needs and gaps;
it does not silently create recovery repositories or copy private data.

## Preserve each layer

Record exact source identities, ownership, timestamp, relevant file inventory
and retained recovery scope. Quiesce the owning writer or coordinate a coherent
capture; recheck source tips, index and working bytes afterward. A changing
source is not a completed snapshot. Retain the original until discrepancies
are resolved.

| Layer | Required recovery evidence |
| --- | --- |
| Committed Git objects and refs | Selected refs/tips, reachable objects, bundle heads and object checks. Record prerequisites for an incremental bundle; verification against the source alone does not prove an independent restore. |
| Index/staged content | Staged paths, blob contents, modes and stage entries, with the pinned base. Preserve partial staging separately from working content; a raw index copy without its required objects is insufficient. |
| Working, untracked, and relevant ignored content | Actual bytes and path/type inventory, including deletions, additions and relevant local artifacts. Binary patches can supplement, but do not replace, recoverable content and metadata. |
| Symlinks and modes | Preserve the link itself and its target text without following it, plus regular-file executable mode. Record other permissions/metadata when meaningful; Git does not preserve every filesystem attribute. |
| Gitlinks/nested repositories | A superproject records a submodule commit ID, not that repository's objects or dirty work. Identify each required repository and access gap; crossing its boundary still needs authority. |
| LFS-managed files | Git may retain only a pointer. Identify required object IDs/sizes and verify the actual LFS payload is available and preserved. A pointer or successful Git-object check is insufficient. |

Git bundles preserve the selected reachable Git history; they do not capture the
live index or dirty/untracked/ignored working files. Capture stash refs and all
needed stash payloads explicitly rather than assuming a named backup covers
them. Include required base objects and document external prerequisites. A
successful `git bundle verify` does not establish dirty-content or LFS recovery.

## Restore safely and compare

1. Select a fresh empty scratch directory outside all active checkouts and
   valuable data, with known ownership, access, space limits and cleanup policy.
   Use an ordinary scratch repository only when authorized; do not create a Git
   worktree implicitly. Never extract over source, the active index, or `.git`.
2. Inspect archive entries before extraction. Reject absolute/traversal paths,
   duplicate or colliding names, device entries and paths that escape through
   symlinks/hardlinks. Use a method that never follows archive-created links
   during extraction. If that cannot be established, inspect objects separately
   and keep restoration unproved. Do not execute restored hooks, scripts,
   filters or submodule updates merely to verify a backup.
3. In the scratch repository, verify bundle format, advertised heads, prerequisite
   availability and necessary objects; import only the intended refs. Start
   without checkout or automatic filter execution. Reconstruct the pinned base,
   staged layer and working layer separately using an inspected procedure.
   A test against the live source's object store is not an independent restore.
4. Compare restored content to the recorded capture: every required path,
   absence/deletion, bytes or secured digest, stage entry, file kind, executable
   mode and symlink target. Use no-follow inspection for links. Check gitlink
   targets and LFS payloads separately; never dereference an external symlink to
   claim its target data was backed up. Unsupported attributes remain explicit
   gaps, not silent success.
5. Record the scratch identity, commands/tool versions, restored scope, comparison
   result, gaps and restore instructions in the ledger. Leave recovery material
   protected through handoff. Retiring a source still requires current ownership,
   authorization, complete accounting, destination proof and the
   [cleanup rules](cleanup.md). A failed/partial restore retains the source.

For example, a valid bundle containing a branch tip but no staged draft or
untracked fixture is incomplete for that dirty checkout. Restore those layers
and compare their distinct bytes before declaring recovery proved. If an LFS
payload cannot be obtained, preserve the source holding it and report the exact
unavailable object; do not replace the gap with a pointer-file checksum. A
restored script with identical bytes but lost executable mode, or a symlink
converted into its target's contents, also fails the declared representation.

Primary references: [bundle](https://git-scm.com/docs/git-bundle),
[index entries](https://git-scm.com/docs/git-ls-files),
[tree entries](https://git-scm.com/docs/git-ls-tree),
[Git LFS storage model](https://git-lfs.com/).
