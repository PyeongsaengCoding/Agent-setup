# Consumer Impact and Sunset

The contract's shape and the contract's evolution belong to the same owner.
Split across two skills, the response envelope and the deprecation window drift
apart, and the surface ends up with a rule for how it looks and no rule for how
it changes.

## Enumerate consumers before designing the change

Work the sources in order, and record which ones were searched - the list is
only as good as its coverage, and the coverage is the part a reader cannot
reconstruct later:

| Source | Finds |
| --- | --- |
| This repository | internal callers, generated clients, fixtures and contract tests naming the field |
| Generated client packages | published SDKs whose consumers you cannot see |
| Access logs by API key, user agent, or client id | who actually calls the endpoint, and how often |
| The spec's own history | who asked for the field, in the commit or PR that added it |
| Partner or integration registries | named external consumers under an agreement |

Then say what the search could not reach. Consumers outside the repository are
unknowable from it: a public API, a published SDK, a webhook anybody may
subscribe to, and an internal caller in another team's repo are all invisible
to a code search.

**An empty consumer list is a claim.** Reporting zero consumers says the search
was complete and found nothing, which is a much stronger statement than "the
search covered this repository and no more". When the set cannot be closed,
report `consumers_not_enumerable` and name what was searched, so the reader
knows the shape of the gap rather than reading confidence into silence.

## Grade what breaks, per consumer

Not every change breaks every caller. Say which, and say why:

- **Removing a field** breaks readers that require it; a reader tolerating
  unknown fields is unaffected by an addition but not by a removal.
- **Narrowing a type or an enum** breaks writers sending the old range, and
  silently breaks readers that switch exhaustively.
- **Adding a required request field** breaks every existing caller.
- **Changing an error code, status, or error body shape** breaks retry and
  error-handling logic, which is the breakage nobody's contract test covers.
- **Changing pagination, ordering, or default limits** breaks clients that
  depend on the old behaviour without declaring it - the hardest class to find
  and the one access logs answer better than code search.

## The window, the path, and the date

A deprecation with no date is a warning nobody acts on:

- **Compatibility window** - how long both behaviours are served, stated as a
  date and not a release count. Size it against the slowest consumer you
  identified, not the median, and against `consumers_not_enumerable` if the set
  is open.
- **Migration path** - what a consumer does, concretely, including the new
  field or endpoint and any semantic difference. "Use v2" is not a path.
- **Announcement** - where consumers are told, and the observation that proves
  they were told. A changelog entry nobody reads is prepared, not delivered.
- **Sunset date** - when the old behaviour stops. Name what is observed before
  it arrives: the old surface's traffic falling to zero, or to a known set of
  consumers who have accepted the break.
- **What happens after** - the removed surface returns a specific status and
  error body rather than a generic 404, so a late caller gets a diagnosis.

An open consumer set does not block the deprecation; it changes the window and
the announcement, and it must say so rather than shortening the window on an
assumption.

## Semantic edits across stores and projections

Use this trace when one user edit is expected to change both a knowledge visualization and a later generated answer:

| Stage | Inspect | Required distinction |
| --- | --- | --- |
| Editor | Actual payload and selected target | Sentence interpretation versus an accepted canonical mutation |
| Authority | User, scope, source and record identity | Personal condition versus shared assertion versus schema definition |
| Persistence | Version checks, event proof and combined writes | Save success versus partially applied replacement |
| Projection | Dirty marker, durable job and publication/version | Requested refresh versus a readable updated snapshot |
| Consumer | Selection, feature gate, input manifest and model caller | Explicitly selected data versus automatically eligible data |
| Withdrawal | Exclusion, deletion, expiry and access changes | Retained history versus permitted new use |

Keep the current authoritative record and project its identity/revision into the view; avoid copying one user's condition into independent graph and memory records without a reconciliation owner. Values, units, application scope and valid time need an explicit representation rather than being inferred anew from display labels.

Treat instance changes and ontology/schema extensions as separate operations. Existing relationship validation can check a known relation's endpoint types; adding a new semantic relationship also needs its definition, scope, publication authority and downstream eligibility. Preserve unsupported meanings as reviewable candidates until those contracts are established.

For automatic-source corrections, preserve the original statement and attach the user's correction with provenance. Exercise a failure between exclusion and replacement, repeated submission and concurrent edits; successful individual endpoints do not establish recovery of the combined operation.

## Knowledge-generation lifecycle audit

1. Build an ingress matrix before recommending a unified pipeline: connected providers/imports, uploaded documents or database rows, live user messages, assistant outputs, completed decisions and manual edits. Name the actual producer and caller for each; keep an untraced source category explicitly incomplete rather than generalizing from one connector.
2. Trace every ingress through canonical source/revision, candidate extraction, semantic admission, authoritative storage, search/map publication, and the next answer's frozen input. Record processed, candidate, admitted, held and published states separately, because a finished extraction job can admit no usable knowledge.
3. Distinguish searchable conversation history, personal-memory records and typed graph relationships. A message indexing receipt or remembered statement proves its own store, not a node/edge publication. Inspect any rule-based statement extractor before claiming broad language coverage; constrained patterns can miss ordinary paraphrases and scope qualifiers.
4. Preserve meaning by origin. Treat a question as a question, a user assertion as a scoped statement, a cited third-party claim as attributed evidence, an assistant recommendation as generated interpretation, and a completed decision as historical context. Promote personal preferences from authorized user statements or confirmations, because feeding generated recommendations back as personal facts creates circular evidence.
5. Trace ontology evolution separately: existing type/relation validation, extension candidate generation, semantic and compatibility review, authorized version publication, and affected-record re-evaluation. Reuse the existing authoritative records and workers before proposing a new common store; instance changes and shared semantic definitions have different owners.
6. Pin the serving revision and compare the inspected producer/consumer modules with it using file hashes or selected function ASTs. Query only the needed feature flags and report private rollout lists as counts. Separate configured enablement, account/workspace eligibility, provider readiness and actual completed work; missing settings require examining defaults and deployment composition before concluding the runtime is disabled.
7. Exercise focused offline contracts, then verify one connected case through source import, user condition, map publication, decision, voluntary edit, later answer and withdrawal. Inspect exact source/record/version references and the actual model input. Keep component tests, configuration readback, semantic quality and deployed UI results as separate verdicts.

### Investigate one generation stage with real evidence

1. Resolve the existing read-only account/source diagnostics route from its definition and caller. Verify the service identity and selected scope, then select an existing authorized source; preserve provider sync, model execution and rebuild operations for separately authorized recovery.
2. Record listing completeness, continuation or hard limit before counting work statuses. Report returned subset counts and any generation-level source total separately, because those quantities can cover different populations. Retain exact source identifiers privately for follow-up while keeping customer contents and credentials out of shared evidence.
3. Read source storage, extraction, assessment, admission, search projection and publication results for that exact source. Inspect both entity and relation counts even when the work is completed and the diagnostic blocker is empty; isolated admitted entities can leave the relationship experience incomplete.
4. Resolve each hold to candidate kind, classified meaning, assessment verdict and the eligibility rule. A generic kind-ineligible reason alone cannot distinguish a correct exclusion, a classification error or an unsupported user-condition policy. Keep unavailable classification metadata as a named gap and request the smallest additional read surface rather than inventing the held candidates' meaning.
5. Compare policy eligibility with the confirmed user outcome. If source claims, personal conditions and AI interpretations have different owners, preserve those distinctions and design a typed destination or projection for missing valid meanings. Do not admit every candidate merely to increase edge counts; that can turn generated interpretations or third-party statements into user facts.
6. Verify the selected source's membership in the published snapshot and actual map rendering independently. An active Workspace pointer proves publication metadata, not that this source is visible; a successful map render still leaves later answer use to verify.
7. Finish the current stage with observed state, unresolved semantic classifications and the next exact acceptance check. Expand to other ingress types after this result is settled, so repeated broad reviews do not replace the requested record-level diagnosis.

## Boundary

A consumer list, a window, and a sunset date are prepared. Traffic figures,
access-log analysis, and the observation that consumers migrated are observed
evidence and come from the operator; a prepared sunset plan is not a removed
endpoint and not proof that anybody was told.
