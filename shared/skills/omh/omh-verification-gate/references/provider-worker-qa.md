# Bounded provider and worker QA

## 1. Establish current evidence and ownership

Read the integration receipt, current implementation, and latest saved QA result before selecting a follow-up. Compare source freshness with the run; an earlier failure can already have a tested fix. Reserve product changes for the implementation owner.

For a shared dirty checkout, inspect tracked and untracked target files directly. `git diff` covers tracked changes; read untracked implementations and tests before accepting a child's patch summary.

## 2. Freeze the quality test before calls

Create a case matrix with input provenance, expected choices, allowed alternatives, and failure conditions before invoking the provider. Separate authentic public excerpts from synthetic injection and encoding probes so adversarial fixtures retain their test provenance.

Set a request ceiling and count actual HTTP attempts. Record skipped inputs and harness errors separately; a case returning before transport contributes zero provider calls. Include authentication-error probes in the request count while separating their usage from successful calls.

For an advisory excerpt classifier, cover factual content, interactive lookup instructions, unavailable content, mixed pages, prompt injection, and UTF-8 truncation. Compare answers with the exact transmitted excerpt. Inspect mixed error-plus-form pages against frozen alternatives; an accepted classification can still leave the requested fact unconfirmed.

### Paired conversational and formal-judgment evaluation

1. Preserve the agreed benchmark product and exact observed inputs. Record preceding turns for follow-up cases and keep candidate labels consistent within a conversation; remapping each turn can create a false context failure.
2. Match the comparison boundary before grading. Raw Markdown, rendered DOM text and rich-card copies serialize differently. Preserve original captures, compare factual content and requested depth fairly, and use actual rendering to judge tables or buttons; extraction fragments can otherwise dominate a blind verdict.
3. Freeze acceptance for ordinary explanations, comparisons, recommendations and explicit formal judgment separately. Check requested length and examples, unknown facts, numeric value kinds and changed conditions. Distinguish total price, difference and percentage in complete sentences; correct arithmetic can still produce an incorrect price claim when the comparison direction is omitted.
4. Retest the demonstrated defect with the actual model and then use undisclosed inputs held by an independent reviewer. A spy asserting that an instruction reaches the provider supplies wire-contract coverage; a canned provider response supplies fixture behavior. Record real generated body, exact saved input and settled reload text as separate quality evidence.
5. Name the counted resource: user submissions, HTTP attempts and provider model calls need separate counters. Carry consumed allowance across owned server restarts, reserve holdout slots before dispatch, and assign the remaining submissions to one owner; a reset process counter silently expands the authorized cost boundary.
6. Reduce raw result histories before printing: inspect the container type, select the final sample and emit only allowed fields. Keep lease/claim tokens, account identifiers and unrelated sidebar content out of durable reports. Record configured model and effort separately from observed metadata for each actual stage; a search-stage model does not identify conclusion generation.

## 3. Exercise the existing adapter within its approved boundary

Invoke the application adapter with the process-scoped client and approved credential loader. Keep secret values out of evidence. Record payload field names, passage counts, byte limits, source hashes, truncation flags, response model, latency, and usage.

Use sentinel fields in local inputs to assert that user messages, identity, Workspace identifiers, and URLs stay outside an excerpt-only provider contract. Verify original citations remain unchanged and preserve configured default activation.

Test cancellation before and after the provider call, insufficient remaining time, exhausted research budget, provider errors, malformed responses, and response-size limits. Check that cancellation propagates and fallback preserves collected evidence. Verify that consumers retain required conditions and original source state when using advisory confidence.

For byte-prefix limits, test a multibyte code point crossing the cutoff and confirm valid UTF-8 plus accurate truncation. Compare prefix contents with page structure: navigation can consume the available bytes before substantive content begins.

### Post-bind source-catalog replay

1. Trace input preparation, binding/normalization, first review, correction reviews and cached replay. Record the catalog at each boundary; server-bound question or clock entries can appear after the original input is frozen.
2. Capture the actual outgoing review request through the real binding and execution path. Include an authorized document together with question/calculation input and a valid clock when applicable. Assert document identity/body preservation, unique references and absence of cited-but-missing entries; testing a handwritten review clone alone skips the integration that can lose sources.
3. Preserve the full authorized catalog plus validated additions in a separate review input. Keep frozen generation input, digest, baseline snapshots and cached final behavior unchanged; substituting only a narrowed selection can omit evidence needed for review.
4. Cover first review, correction re-review, legacy fallback and cached replay without another generation/review call. Supply the clock through the normal saved execution-time fields and validate its timezone/date binding; a fixture without those fields supplies no clock coverage.
5. Describe the observed source representation faithfully. Calculation operands may be represented by question evidence rather than a separate calculation source. Label direct execution, document injection and recording-provider substitutes explicitly, and retain the full HTTP/document-admission gap when that path was not exercised.

## 4. Diagnose worker warnings from a timeline

Read the exact owned QA partition and correlate job creation, turn journal update, tool start/completion, awaiting-checkpoint persistence, worker scan/claim, attempts, lease, terminal state, source reads, and later model calls.

Identify tool names and arguments before labeling a second call as duplicate execution. A source-read follow-up can result from inaccurate truncation metadata even when the browser executed once. Compare stored body with citation flags and keep bounded observation coverage separate from text truncation.

If a scan lands between job creation and checkpoint persistence, reproduce it by wrapping real job creation and invoking one worker batch immediately after create returns. Assert the pending job stays unclaimed with zero attempts, then checkpoints and dispatches once. Add a paired case with no live tool call or changed authority to prove genuine refusal remains intact. Deferred scans must preserve pending state and authority enforcement.

## 5. Verify in layers and close owned resources

Discover actual test paths before constructing a command. Start with the reproducer and affected guards, then adjacent suites, lint, and architecture checks. Record commands and exits; an empty pytest selection supplies no regression evidence.

Give independent QA the natural user input, goal, account/data scope, and acceptance criteria. Exercise the authenticated API, real model, worker, saved answer, and source reopen when behavior changes. Read back exact saved targets and reconcile provider receipts with the ledger before claiming that flow passed.

Classify process-exit notifications using process role and owner evidence: terminating a preflight server can be intentional cleanup. Keep the verdict pending until actual flow results arrive. Record owned process/tab cleanup and transient authentication cleanup separately from product success.

Inspect final captures for unfinished cell-level states and ancillary failures as well as the main result. Record automatic-title failures, source-detail placeholders and projection retries with their scope; a completed job, rendered table or successful reload proves only that boundary. Report limited QA completion together with uncovered acceptance checks and follow-ups, and preserve broader HOLD findings even when the task checklist closes. Read back checkpoint records and their computed gate before summarizing; recording a PASS declaration does not resolve recorded findings.
