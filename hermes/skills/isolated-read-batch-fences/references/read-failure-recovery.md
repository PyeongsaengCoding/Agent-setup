# Read failure classification and answer recovery

## Procedure

1. Capture the original answer-preservation contract and identify which execution owns each receipt. Inspect the synchronous callback, isolated worker, checkpoint and fallback boundaries together.
2. Reproduce first valid answer → corrective read → ordinary callback failure through the application service. Assert terminal turn status, stored assistant count, exact preserved answer and provider call count. Run the identical controlled case against the baseline and candidate when a regression is suspected.
3. Classify the failure using the table below before changing receipt status. Store only a safe category and empty citations for an observed unsuccessful read; keep raw exception text out of the saved result.
4. Permit saved-answer recovery only after live authority and frozen-source checks pass. Keep failure results outside the successful-result reuse cache.
5. Replay the exact checkpoint with callbacks that fail the test if invoked. Prove stable saved-answer readback and zero new provider or retrieval calls. Separately exercise prior-owner unknown receipts, interrupted batches and security failures.
6. Run the affected fallback, parallel-read, completion and takeover tests. Request independent review of the product-loop preservation probe before release; a green suite after weakening the old preservation expectation proves only the revised expectation.

## Decision table

| Observed boundary | Receipt handling | Answer handling |
| --- | --- | --- |
| Prior execution left a read started | Retain unresolved identity and signature | Follow fail-closed replay; keep unknown results out of fallback |
| Current synchronous read returned an ordinary exception | Record a sanitized terminal unsuccessful read after confirming the exception category | Preserve an earlier validated answer when current authority and source checks pass |
| Isolated batch has a running or unobserved branch | Stop dispatch, discard late output and retain unresolved branches | Keep partial merge/effects out of answer recovery |
| Cancellation, authority revocation, storage failure or deadline | Preserve the existing category-specific execution guard | Exercise the dedicated guarded path; do not reclassify it as an ordinary failed read |
| No earlier valid answer | Record the known failure at its actual boundary | Preserve the normal error outcome |

## Test pitfalls

- Construct unknown replay fixtures from completed controlled reads before replacing the receipt; building them through a live exception can fail before replay is reached.
- Assert first-answer preservation and unknown-replay refusal independently; they guard different ownership boundaries.
- Inspect exception inheritance before broadening a catch. Storage, authority or deadline errors can inherit common exception bases and require their original guards.
- Keep incomplete isolated branches distinct from an observed synchronous failure; a worker may still be running after the coordinator returns.
