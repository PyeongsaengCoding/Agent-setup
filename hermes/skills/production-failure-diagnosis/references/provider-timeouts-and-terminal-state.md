# Provider timing and terminal-state evidence

## Investigation

1. Read exact turn/job status, last error, completion assessment, last model-step status and fallback receipt. Compare them with the visible answer.
2. Retrieve per-provider attempt receipts for the exact execution. Allowlist status, role, failure phase/category, start/end timestamps, duration, remaining budget, reservation and outbound timeout. Include search planning, grounding, page acquisition and OCR when present; account for overlap when calculating totals.
3. Match receipt values to the timeout adapter and budget policy. Distinguish before-dispatch, capacity-wait, transport, HTTP-response and decode failures. A transport timeout establishes that the local wait expired; explaining the provider's internal delay requires further evidence.
4. Trace exception conversion. Check whether a catch returns source excerpts with an answer outcome, whether the writer assigns completed and clears last_error, and whether error projection admits only failed statuses. Record each transition that changes user-visible meaning.
5. Cross-check committed/deployed source against the observed execution; retain durable receipt values as historical evidence while labeling local changes by their actual deployment state.

## Evidence escalation

Prefer owner-authorized diagnostic APIs. When they omit the original attempt boundary, locate the independent receipt store in source and use existing authorized operational reads. Empty centralized logs leave that channel without evidence; independently persisted receipts may still expose the cause.

### Azure Cosmos read-only recipe

1. Verify `az account show` against the project's account/subscription boundary.
2. Discover endpoint, database, container and partition metadata with `az cosmosdb list`, `az cosmosdb sql database list` and `az cosmosdb sql container list`.
3. Capture `az account get-access-token --resource https://cosmos.azure.com/ -o json` through an in-memory subprocess. Use existing Entra read permissions; keep token values out of output and artifacts.
4. POST a read-only SQL query to the discovered `/dbs/<database>/colls/<container>/docs` endpoint. URL-encode authorization `type=aad&ver=1.0&sig=<token>`; set `x-ms-date`, `x-ms-version: 2018-12-31`, `Content-Type: application/query+json` and `x-ms-documentdb-isquery: true`.
5. Parameterize exact execution predicates and SELECT needed fields only. When partition identity is unavailable, use a bounded exact-ID lookup with `x-ms-documentdb-query-enablecrosspartition: true`; obtain its partition identity and scope related attempts with `x-ms-documentdb-partitionkey` and the exact execution ID.
6. Print fixed operational timing/failure fields. Omit prompt bodies, source excerpts and unrelated records. Honor authorization failures and existing tenant boundaries; use access tokens without retrieving account keys or credential files.

## Tool selection and source delivery

1. Recover the exact user question, including dates, party size, route, filters and requested output facts. Compare each condition with what the deployed tool accepts.
2. Read the saved tool names and results for the exact execution. Treat absent browser calls as evidence of non-use; investigate tool exposure and admission to determine why it was omitted. Separate model selection, durable bookkeeping and actual dispatch: a completed row with a dependency-deferred result and absent start/transport evidence can record a local refusal. Trace the dependency predicate, later research admission and fallback writer before assigning the missing answer to a provider.
3. Read only allowlisted non-secret runtime settings for enablement, target URL and condition capability. Match the deployed contract with the adapter's validation, because a working transport may still be restricted to a controlled target.
4. Trace displayed excerpts to acquired page bodies. Classify access-challenge text as acquisition failure and inspect the source acceptance boundary before the fallback writer, because blocked pages can otherwise be presented as evidence.
5. Describe the observed omission and the unsupported conditions explicitly. Keep a proposed browser replay separate until the requested target and fields have been exercised.

## Removing a cumulative deadline

1. Inventory deadline creation and enforcement in execution scope, model loop, stream delivery, saved recovery anchors and child-task admission. Distinguish cumulative execution cutoff, individual transport timeout, call-count ceiling, lease and cancellation.
2. Write a failing regression through the real processing and saved-answer path. Advance a controlled clock across the old total window; verify delivery and persistence, with cancellation and authority controls exercised by adjacent tests. Label injected provider responses as controlled-boundary evidence.
3. Disable cumulative enforcement consistently while preserving finite operation windows. Let each new child operation receive its own admission window; retain that child's exact persisted expiry across polls and retries, because recreating it on each poll permits indefinite extension.
4. Replay completed saved calls against their recorded identity and current access checks. Validate newly dispatched calls against current tool availability, because an unavailable connector can still leave a completed historical result that needs reconciliation.
5. Update tests that intentionally require the retired policy. Retain explicit bounded-policy tests by injecting their bounds, and preserve their assertions about cancellation, source authority, identity and unresolved provider results.
6. Exercise aged execution admission, long multi-stage work, saved-result delivery, resumed execution and browser child expiry. Report local behavior, actual provider execution and deployment separately.

## Interpretation checks

- Inspect failure_phase and provider_error_category before assigning a 504 to the remote HTTP server, because application adapters generate the same code for local timeouts.
- Compare remaining budget, reserved tail and outbound timeout, because the configured execution window and final-call limit represent different constraints.
- Trace partial-result persistence and projection, because completed status can describe saved fallback content while the user's request remains unanswered.
- Separate blocked-page contamination from the stopping cause, because bad source acceptance alone does not establish why a provider call timed out.
