# Commit an independent subset of already-staged text hunks

Use only when a path contains selected and excluded **staged** hunks. Normal
staged commits and complete-file path-only commits stay simpler when applicable.
This is a deliberately narrow procedure, not general index reconciliation.
Plan-only mode stops after inspecting the proposal.

Let `H` be the original HEAD, `I` the real index, `W` the working files, and `C`
the selected candidate tree. Build `C` from `H` through an alternate index.
After committing `C`, leave `I` untouched: its original blob entries now differ
from new HEAD only by the excluded staged changes. `W` also stays untouched.
Do not replace the real index with the candidate or restore it to HEAD.

## Applicability gate

Proceed only when all these facts are established:

- The selected changes are complete, independently reviewed text hunks copied
  from the captured `H`-to-`I` diff of ordinary tracked regular files. No selected
  line comes from an unstaged diff or a later working-file read. Excluded
  unstaged edits may coexist in the same file when they do not overlap the
  selected hunks or their context.
- There is a normal, non-sparse, non-split index with no intent-to-add entries;
  selected paths have no special
  index flags, filters/encoding conversions, mode changes, rename/copy semantics,
  binary/LFS data, symlinks or gitlinks. Preserve flags on excluded entries;
  never clear them merely to fit this recipe. No external `GIT_INDEX_FILE` is
  already selecting another index.
- HEAD exists, the intended branch is known, no unmerged entries or Git
  operation is active, and no other writer can change HEAD, index, files, hooks
  or relevant configuration during preparation and commit. Checkpoints detect
  changes; they do not provide a transaction across concurrent processes.
- Selected and excluded staged changes make coherent independent outcomes.
  Both application orders reconstruct `I` as checked below. This mechanical
  property is necessary but cannot prove semantic independence: a selected
  caller needing an excluded helper, schema or lockfile change blocks selection.
- Every applicable hook, hook manager, signer and check is inspected. Hooks
  must support the alternate index and leave the candidate tree, real index
  and working files unchanged; message-only hooks may edit the message, which
  is read back. A hook that runs `git add`, formats files, reads an absolute real
  index, writes externally without authority, or requires the working tree to
  equal the candidate makes this recipe inapplicable. Unknown effects also block
  it. Do not bypass hooks or required signing to make it fit.

If any gate fails, preserve state and report the smallest staging/dependency
decision needed. Do not broaden the algorithm to arbitrary partial edits,
stash/reset another person's work, or promise restoration after unsafe hooks.

## Capture and construct the candidate

Choose a private task-local scratch directory outside the working tree, with
absolute paths. It holds potentially sensitive patches and index copies; do not
publish or stage it. Resolve the real index with `git rev-parse
--path-format=absolute --git-path index` rather than assuming `.git/index`.
Keep `GIT_OPTIONAL_LOCKS=0` on inspection commands so a status refresh does not
rewrite the baseline index. Never export `GIT_INDEX_FILE` across the session;
prefix each intended alternate-index command explicitly.

1. Record original HEAD and branch, real index bytes and semantic entries/flags
   (`git ls-files --stage --debug -z`), and working-file content and metadata
   needed to prove preservation, including retained untracked files. Use a
   bounded, secured snapshot that handles actual path types; a text diff alone
   is insufficient. Preserve the real index in `original_index_copy`; make a
   separate `index_tree_copy` for `write-tree`. Record hashes of these snapshots.
2. Capture the complete staged patch with stable native Git text output:

   ```sh
   git diff --cached --no-ext-diff --no-textconv --no-renames --no-color \
     --unified=3 --src-prefix=a/ --dst-prefix=b/ "$original_head" > "$staged_patch"
   ```

   Review the complete patch, then copy its complete independent hunks into
   `selected_patch` and the remainder into `excluded_patch`, preserving the
   relevant file headers and context. Every original hunk appears in exactly
   one proposal; do not add lines from working files, invent combined hunks,
   or use whitespace-ignore, three-way, recount or rejected-patch fallbacks.
   Reject an empty selection before mutation. If hunks need splitting or their
   contexts overlap, this recipe does not apply.
3. With fresh, distinct alternate index paths, run these commands one at a time,
   requiring success and inspecting the exact candidate diff/tree. Variables
   below refer to the captured HEAD and absolute private paths, not user text
   interpolated as shell code:

   ```sh
   GIT_INDEX_FILE="$candidate_index" git read-tree "$original_head"
   GIT_INDEX_FILE="$candidate_index" git apply --cached --check "$selected_patch"
   GIT_INDEX_FILE="$candidate_index" git apply --cached "$selected_patch"
   candidate_tree=$(GIT_INDEX_FILE="$candidate_index" git write-tree)
   GIT_INDEX_FILE="$candidate_index" git diff --cached --check "$original_head"
   GIT_INDEX_FILE="$candidate_index" git diff --cached "$original_head"
   original_staged_tree=$(GIT_INDEX_FILE="$index_tree_copy" git write-tree)
   ```

   Reject a candidate tree equal to `H`'s tree. The candidate must contain exactly
   the selected scope and no excluded staged or unstaged content. Checks run
   against `W` may exercise excluded code; use a reviewed candidate-aware check
   or an authorized temporary export of `C` when needed to verify this commit.
   Do not claim working-tree tests prove candidate behavior.
4. Prove reconstruction using only `verify_index`, never the real index:

   ```sh
   GIT_INDEX_FILE="$verify_index" git read-tree "$candidate_tree"
   GIT_INDEX_FILE="$verify_index" git apply --cached --check "$excluded_patch"
   GIT_INDEX_FILE="$verify_index" git apply --cached "$excluded_patch"
   GIT_INDEX_FILE="$verify_index" git write-tree
   ```

   The result must equal `original_staged_tree`. Then reset **only this alternate
   verification index** with `read-tree "$original_head"`, apply the excluded
   patch first and selected patch second with `--cached --check` before each
   application, and require the same tree again. Reject failed applications,
   unexpected paths/content, or either tree mismatch. Leave `candidate_index`
   containing `C`. Review the excluded result too; mechanical reconstruction
   does not establish ownership, completeness or dependency safety.

## Commit, then verify without reconciling the real index

Immediately before committing, compare HEAD, branch, complete real index,
working snapshot, candidate tree, hooks and relevant configuration to the
reviewed baseline. Stop on any difference. Commit normally, with no pathspec,
`-a`, bypass flags or signing overrides:

```sh
GIT_INDEX_FILE="$candidate_index" git commit -F "$reviewed_message_file"
```

Read back the actual result even if the command fails. Verify the commit's sole
parent is `H`, its tree is exactly `candidate_tree`, its stored message and
required signature are correct, and the branch is still the expected branch.
Compare the real index to `original_index_copy` **before** ordinary status
refreshes; byte identity also proves its semantic entries and flags survived.
Compare the working snapshot, including excluded unstaged and untracked bytes.
Only then inspect the fresh cached diff (now new HEAD to unchanged `I`) and the
working diff (`I` to unchanged `W`). They must contain exactly the reviewed
excluded staged and unstaged changes, respectively.

There is no post-commit `read-tree`, `reset`, `restore` or index-copy replacement
on the real index. The selected content already exists in both new HEAD and
`I`; it disappears from the staged delta naturally. Reclassify from fresh state
before another group rather than reusing the old HEAD or proposal.

## Failure and unexpected effects

- Empty or inapplicable proposals create no commit. Preserve all original work.
- A pre-commit or signing failure with unchanged HEAD, real index and working
  snapshot confirms no commit was created. Inspect candidate/message changes
  before considering a retry; do not disable the failing control.
- A successful command can still commit a hook-modified candidate. A failed
  command can still leave a commit or changed files. Compare actual HEAD/tree,
  index and work, record the mismatch, and stop for a bounded recovery decision.
  Do not retry, amend, reset, restore snapshots over current work, or pretend
  postflight detection prevented an unsafe hook's effects.

Disposable Git verification covered selected/excluded staged hunks in one file,
separate excluded staged and unstaged content, retained untracked bytes and
excluded assume-unchanged/skip-worktree flags; empty/unstaged/unmerged proposals;
read-only and rejecting hooks; signing failure; candidate/working-mutating hook
probes; and changes to HEAD, index or work before commit. Unsafe hook probes
demonstrate why the applicability gate is required, not support for those hooks.
No claim is made for arbitrary index formats, filters or hook implementations.

Primary references: [Git index environment](https://git-scm.com/docs/git#Documentation/git.txt-codeGITINDEXFILEcode),
[git read-tree](https://git-scm.com/docs/git-read-tree),
[git apply --cached](https://git-scm.com/docs/git-apply),
[git commit](https://git-scm.com/docs/git-commit), and
[hook execution](https://git-scm.com/docs/githooks).
