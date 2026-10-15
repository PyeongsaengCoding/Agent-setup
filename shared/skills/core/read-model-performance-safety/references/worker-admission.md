# Worker admission and rollback

Use when a synchronous private read is dispatched through an async supervisor that reserves real thread-pool capacity before creating its worker task.

## Inspect ownership before changing code

1. Trace reservation, ownership registration, task construction, done-callback registration and permit release in execution order.
2. Distinguish three outcomes: refusal before reservation, failure after reservation but before dispatch, and running work awaiting actual pool completion. Choose a test for each; they require different cleanup.
3. Identify the concrete constructor boundary. Inject failure before the task constructor delegates to its superclass so the reproduction proves that no worker started. A failure injected after task creation needs a separate lifetime analysis; closing its coroutine and releasing its permit could invalidate running ownership.

## Reproduce with real capacity

Use the project's existing compatible interpreter and limiter. Keep provider/network dependencies outside this test.

- Replace only the worker-task constructor with one that captures the incoming coroutine and raises a specific exception instance.
- Assert the callback never starts, then measure borrowed tokens and retained ownership records. Before the fix, leaked reservation counts establish the failure.
- Clean up the reproduction's captured coroutine and exact reservation explicitly so the experiment cannot contaminate later tests.

## Implement the narrow rollback

- Resolve the running loop before capacity acquisition; missing-loop refusal must consume no slot.
- Hold the newly created coroutine in a local variable before constructing the worker task.
- On pre-dispatch constructor failure, close that unused coroutine, return its own permit, remove its ownership record and rethrow the original exception. Cover `BaseException` at this cleanup boundary when cancellation or allocation failure can interrupt construction.
- Keep the normal done-callback release path after actual pool completion. Preserve worker cancellation and disconnect semantics independently from admission rollback.
- Treat set insertion or done-callback registration failures as separate boundaries. Establish whether work already exists before choosing cleanup; a blanket release around the entire start method can free a live worker's slot. Keep allocation failure reachability unverified until checked; an injected failure demonstrates cleanup behavior, while its production frequency needs separate evidence.
- For a constructor that raises after superclass task creation, identify any already-scheduled task and observe its completion or exception. Token rollback alone leaves task-lifetime and exception-log behavior unproven. Retrieve test-owned task exceptions during cleanup and assert that no callback dispatched or token was returned twice.

## Verify in this order

1. Constructor failures: inject `RuntimeError` and `MemoryError`; assert the exact original exception is rethrown, callback count stays zero, borrowed tokens return to their baseline, and no owned record remains.
2. Coroutine cleanup: capture warnings and force collection; assert no `never awaited` warning. Run the focused tests with `python -B -m pytest -p no:cacheprovider -W error::RuntimeWarning` using the project's interpreter.
3. Recovery: restore the real constructor and admit a real callback through the same supervisor; assert normal completion and final ownership/token cleanup.
4. Isolation: hold another callback at an observed entry barrier with capacity two. Fail a second admission and assert exactly one token remains, the first work is still owned and uncancelled, and a further admission refuses when capacity is full. Release the held callback and verify normal cleanup.
5. Controls: capacity-full refusal and missing-running-loop refusal consume no new token or ownership record.
6. Run adjacent cancellation, owner shutdown, authentication admission and source-response regressions. Verify architecture budgets and lint without widening their limits for the fix.
7. Review each independent edge probe's assertions. Assert token and retained-work outcomes instead of merely printing them; record a passing diagnostic that confirms a leak as a reproduced limitation, not a passing cleanup guarantee.
8. After the code-level gate, reopen a retained source through the approved real account and isolated storage composition. Verify the admitted identity/workspace, response status, applied conditions, URL and body hash, plus missing/invalid authentication controls. This validates the normal path after the change; keep injected rollback coverage and deployed-capacity coverage separate.

A direct supervisor or service-helper invocation proves that layer. Label HTTP transport, authenticated storage and deployed-user checks only when those paths were actually exercised.
