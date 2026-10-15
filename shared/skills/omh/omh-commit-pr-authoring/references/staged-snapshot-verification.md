# Verify a scoped staged snapshot

Use when requested changes share files with unrelated local work. The executor owns Git mutations; this workflow prepares scope and verification.

1. Inspect `git status --short`, `git diff`, and `git diff --cached`. Select related files and reviewed hunks from mixed files. Preserve other working-tree edits.
2. Have the executor export the index to a fresh scratch directory with `git checkout-index --all --prefix="$SNAPSHOT/"`. Keep the trailing slash and run tests from the exported project paths.
3. Resolve dependency placement before linking existing dependencies into the snapshot. Workspace packages can be hoisted to root `node_modules`; linking only the child package directory can leave imports unresolved. Reproduce the observed root and package-level dependency layout without modifying source files.
4. Run relevant tests and build on the exported index. Record the snapshot and exit status. If dependency resolution prevents execution, restore the observed layout and rerun; count success after actual test execution.
5. Review `git diff --cached --check` and staged paths. Inspect evidence for sensitive data and verify document links against tracked or staged targets. Ignored logs may stay local; published references need included evidence.
6. For authorized commit and push, hand the executor the verified scope and message. Compare `git ls-remote <remote> refs/heads/<branch>` with the local commit ID before reporting push completion.

Keep working-tree, staged-snapshot, and installed-device results separate. A workspace APK may include earlier uncommitted features that a scoped commit preserves locally.
