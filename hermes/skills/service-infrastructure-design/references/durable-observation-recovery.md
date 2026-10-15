# Durable observation recovery

Use when a model tool suspends a user request while a trusted worker performs external observation. Apply after source readers and retained-answer authority are qualified.

## 1. Trace and gate the connected flow

Trace tool admission, saved provider response, tool checkpoint, job creation, worker selection, result publication, input freeze and saved-original reading. Inspect inline HTTP and background worker paths separately. Keep missing transport or storage dependencies default-off for new work; retain a reconciliation path for already-saved awaiting state.

Derive an idempotent execution identity from server-owned turn/context identity, persisted step position and the immutable tool signature. A model call identifier may participate in this binding; it must not independently select tenant, storage path or authority.

## 2. Separate awaiting from unknown side effects

Persist a typed awaiting checkpoint and return normally with the existing retrying state, released lease and bounded next-attempt time. Keep unresolved started provider or ordinary tool calls fail-closed; their side effects cannot be safely inferred from an awaiting job.

Pin an absolute deadline to the original admitted execution. Preserve it, paid-call counters and final-answer reserve across polls and restarts. Exclude ordinary awaiting polls from failure retry attempts; use the fixed deadline and separate job attempt cap to bound recovery.

## 3. Treat notification as a hint

Persist awaiting before notifying. Catch only notification transport failures and log a safe category or exception type; run authority checks outside that catch so revocation still propagates.

Rediscover claimable jobs from durable state independently of notification delivery. Reissue hints with capped backoff after a lost hint or expired worker lease. Suppress hints for a valid lease, exhausted attempts, completed work or an expired deadline. Reclaim with the existing CAS and fencing token; never use a second notification as proof that a second observation is safe.

Test a crash between checkpoint persistence and notification, a raising observer, a lost hint, expired versus valid leases, and rejection of the old worker after reclaim.

## 4. Reconcile results without manufacturing evidence

Validate body size, hash, requested/applied conditions and current authority before consuming a committed result. Return a verified empty observation as a limited tool result without creating an empty citation. Return unavailable dependencies or observation failures as explicit unverified outcomes instead of making tool lookup fail the whole request.

Keep new admission separate from replay: removing an observer can disable new work while a stored committed result remains readable through its configured reader. Removing the reader prevents evidence use; it does not justify trusting the saved excerpt alone.

Test corrupt empty results, authority changes during I/O, dependency removal while awaiting and final limited-answer behavior.

### Classify failures at the external-work boundary

1. Trace exception inheritance through the engine and controller before mapping error types to public outcomes; a controller failure derived from ValueError can represent lost ownership after external I/O.
2. Set an external-work-entered marker immediately before calling the engine, after preflight guards. Preserve unknown work on subsequent unresolved exceptions, including an engine opening call that raises after partial side effects; suppress automatic re-observation.
3. Keep explicit deadline failures mapped to timeout. Validate a completed result's body in a separate narrow catch so a deterministic admission failure remains unapplied without swallowing later ownership or freshness failures.
4. Recheck ownership and the original deadline after observation and after cleanup before returning a result; work that finished late must not become successful evidence.
5. Add a regression that raises the real controller exception after one recorded engine observation and requires exactly unknown. Add late-observation and slow-cleanup cases requiring exactly timeout; an assertion accepting either timeout or unapplied conceals misclassification. Run these cases RED before changing the mapper, then run the connected receiver, lifecycle and saved-original tests GREEN.

These checks establish local failure semantics. Keep actual external side effects and host cleanup qualification as separate observed gates.

## 5. Fence authorized context revisions

On an authorized monotone message or instruction revision, discard stale awaiting state and replan under the new context while preserving deadline and actual paid-call accounting. Continue denying changed membership, lifecycle or unresolved started calls. Update the design contract when choosing replan rather than terminal failure.

Derive current context from server message/instruction records and the active checkpoint at claim, stage, validation and commit. Deny stale pending and running jobs, not merely stale result consumption; otherwise obsolete work can still incur external cost.

Fence every independently mutable row at the atomic publication boundary. A turn CAS alone cannot stop a message-only revision between validation and commit. If conditional replacement of an unchanged message row supplies the guard, record its extra write and ETag churn, and test same-turn job contention. Preserve retained committed-answer reads through their original binding instead of imposing live-execution context checks on history.

## 6. Retry contention without following changed authority

Bound CAS retries and keep the job ETag, worker lease, fence, deadline, authority and input identity fixed. Refresh only rows whose changes are permitted by the transition contract. Reject changed context, source authority, expired ownership or exhausted retries. Do not republish the body during a turn-row retry.

Exercise the successful retry path with a store that raises the real conflict exception, plus rejection cases for stale fence, authority change and deadline expiry. Assertion-only stores can miss the production retry branch.

Stop heartbeat threads before lease release. If transient renewal errors are isolated, retain thread-termination checks and the final owned-turn CAS so lost ownership remains fatal.

### Reconcile claim-induced reader ETag changes

1. Reproduce both a follow-up reading an inherited citation and a second observation claimed while the first citation body is being read. Exercise the actual claim batch during Blob I/O, because unchanged message guards can be rewritten alongside the turn and receive fresh ETags.
2. Compare semantic authority before allowing that transition: fixed message identity and content, fixed running status, owner, lease, fence, instructions, checkpoint, job bindings and other authority rows. Require exactly one valid revision increment and nondecreasing update time, with only the documented storage metadata changing. Keep the existing heartbeat transition separately typed.
3. Share the pure transition predicate between answer-freeze and evidence-reader guards; inspect each caller's complete authority snapshot, because permissive outer validation cannot repair a stricter inner reader and a permissive inner reader still needs the outer context fence.
4. Retain negative tests for edited message content, changed owner or lease, changed instructions or checkpoint, revision jumps, two overlapping writes and other authority-row changes. Preserve historical-answer binding independently from live new-use reconciliation.
5. Verify two committed observations through resume, final citations and both original-body readers, then verify the inherited-citation follow-up. Count additional point reads introduced by reconciliation so correctness improvements carry an explicit storage-operation delta.

## 7. Verify and account for the complete recovery path

Run targeted behavioral checks through real application functions and private local files, mocking only external model/transport boundaries. A useful command shape is:

```sh
.venv/bin/python -m pytest <producer-tests> <recovery-tests> <job-tests> <reader-tests> -q -p no:cacheprovider --tb=short
```

Verify child receipts against current source hashes, then independently run the connected tests. Parse full-suite JUnit failure identities when attributing unrelated failures; nondeterministic callback ordering can change parameter failures while leaving the total unchanged.

Recover an interrupted delegation from persisted artifacts before retrying work. Read its source manifest, scoped patch and recorded commands; compare current hashes and rerun the smallest connected local checks. Keep the delegation's missing terminal outcome unknown while reporting the independently reproduced artifact result. Verify external effects separately before replaying any side-effecting operation; surviving files or a partial transcript establish only what can be read back and exercised.

Inspect connected-flow assertions as well as their totals: verify same-question resume, the admitted source URL and applied conditions, saved-answer original reopening, empty-result behavior, and zero new execution or storage writes on committed replay. Label fixture-derived answers at the external boundary; a full local application path can still use a synthetic site result.

Run a second natural question in the same saved conversation as a separate acceptance case. If that follow-up fails, preserve the failed request, current message/context revisions, prior citation binding, and publication guard before testing a new conversation. A successful new-conversation run establishes that narrower path; the original follow-up remains open until its cause is fixed and the same-conversation case passes.

For every harness override, record the value's trusted source, the runtime entry point receiving it, and the corresponding default product producer/consumer. Remove overrides one at a time and rerun the connected flow to localize missing wiring. Keep genuine host observation, harness-assisted integration, default-product behavior, and deployed UI behavior as separate evidence fields.

Count reads, writes and accounting rows per pending poll. Report these as local operation counts, not measured cloud cost. Measure real transactional behavior, RU and distributed contention separately before scaling or enabling external execution.

Maintain distinct verdicts for local flow, independent review, actual host execution, isolation/security acceptance and deployment. A passed offline dispatcher does not qualify the host or prove real site conditions were applied.
