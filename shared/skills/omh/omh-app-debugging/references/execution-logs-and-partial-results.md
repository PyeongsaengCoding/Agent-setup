# Execution logs and partial results

Use this recipe when an AI application loses useful answers, leaves accepted work unstarted, or needs process logs with bounded server cost.

## 1. Pin the failure layer

Read the response-mode contract and write separate expectations for:

| Layer | Observation to capture |
| --- | --- |
| Execution | request accepted, claim acquired, provider attempted, result validated, persistence completed |
| Requirements | requested facts supported, conditional, missing, or inaccessible |
| Presentation | ordinary conversational answer or explicit structured judgment |
| Replay | the same authorized saved answer and its exact execution identity |

Use a completed status only for the layer it proves. A successful save proves persistence; an answer's self-reported coverage needs separate evidence when semantic fulfillment is the acceptance criterion.

## 2. Trace instrumentation to its saved consumer

1. Use `search_files` to locate the helper definition, every call site, tests, checkpoint writer, and diagnostic projection; read the actual files.
2. Follow one real application call through the helper, caller result, saved checkpoint, authorized read, and UI consumer. Test every newly added field at these boundaries.
3. Add an optional, content-free receipt callback when the helper must preserve its existing return and exception contracts. Give outcomes a bounded vocabulary and record elapsed time with a monotonic clock.
4. Test successful calls, legitimate skips, unavailable-provider fallback, and cancellation separately. A skip needs its reason; it does not become an execution failure.
5. Before widening the helper signature, search tests for hand-written adapters and patched callables. Exercise both the actual import and the adapters because a stub can retain the old signature after production code changes.
6. Verify the caller actually forwards the receipt into existing persistence. A sanitizer and projection can both pass isolated tests while the application never emits their input.

Retain stage status, safe reason, duration, counts, and usage identity. Store large inputs and outputs once and refer to their existing protected records; omit bodies, private queries, tokens, and arbitrary exception text from diagnostic projections.

## 3. Measure log burden without overstating it

Wrap the actual instrumentation with a counting store that records operation type and serialized payload bytes. Run several provider-attempt counts and distinguish repeated upserts from unique documents. Include lifecycle and conversation checkpoints when estimating the complete path.

Compare baseline and candidate operation counts to show whether the change adds persistence calls. Record which overhead remains unmeasured: real database request charges, synchronous write latency, CPU, memory, ingestion volume, and concurrency. Local write counts establish mechanism; operating capacity and timeout causality require operating measurements.

## 4. Preserve useful results narrowly

1. Reproduce failure after authorized original sources or a validated first answer have been acquired.
2. Preserve those artifacts for explicitly classified timeout or availability failures. Reuse existing deduplication and source identity; assert that source reads and searches do not repeat.
3. Keep cancellation, permission denial, binding drift, malformed source results, and storage/resource failures observable. Test each guard and the zero-originals case so the fallback cannot turn every exception into success.
4. Test the actual tool return and saved checkpoint, including the partial lookup reason. Successful source delivery can otherwise discard the diagnostic evidence explaining why enrichment stopped.
5. Exercise answer generation, persistence, authorized reentry, and rendering. Preserve ordinary conversational wording; judgments keep their result/comparison/reason structure.
6. Pin the delivery timing separately. A partial answer retained after a failed continuation and a partial answer streamed before continuation completes require different assertions; prove the requested one.

## 5. Recover accepted work without duplicate execution

Trace registration and execution claiming separately. Capture claim timestamp, attempt count, heartbeat count, terminal reason, and elapsed time; a saved preparation result does not establish a provider attempt.

For an explicit restart, reproduce a running-but-never-claimed job through the real start entry point and server claim operation. Verify the connected client's execution gate accepts the response while the server still allows exactly one claim. Preserve the same input binding and owner checks.

For an expired unclaimed registration, bind the successor key deterministically to the abandoned receipt and bound successor traversal. Test repeated starts, an active claim, interrupted claimed work, user cancellation, foreign ownership, and input drift. Read-only reentry retains its observation contract; execution requires the approved start action.

## 6. Verify after integration

Run each lane's failing reproduction before implementation, then its passing regression. Wait for all writers before the integrated suite because a reader can observe another lane's unfinished function or test. When a failure overlaps concurrent edits, reproduce it against the recorded base with identical fixtures before assigning responsibility.

Run focused application-boundary tests, connected component/request tests, then the wider suite warranted by shared-contract risk. Report controlled-provider checks, actual model quality, browser/account QA, and deployment as separate observed outcomes. Keep remaining operating-load and delivery-timing gaps explicit.
