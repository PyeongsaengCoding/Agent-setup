# Decision and retrieval tools

Use when adopting a small decision model, search grounding, API connector, or browser automation into an existing AI product. This is a design and evaluation procedure, not proof of an installed integration.

## Procedure

1. Establish the outcome and terminology. Search and read project contracts to resolve named components and prior decisions before associating an acronym with a web result. Read user-supplied conversations as proposals, not evidence that a competitor or tool works. Extract the general capability and retain the user's original failing examples as acceptance cases.
2. Inspect the actual runtime entry point, tool definitions, retrieval handlers, source catalog, frozen model input, formal-decision handoff, and result persistence. Use the project's context graph when required. Prefer current source over older design summaries; do not resurrect removed planner/team/review stages from historical documentation.
3. Build a responsibility table before choosing dependencies. Keep goal interpretation, compound reasoning, and final explanation with the main model. Assign a small decision model only bounded semantic questions about observed state. Keep data acquisition and browser actions in executable adapters. Enforce identity, permissions, approved transmission, cancellation, and limits in the server.
4. Choose acquisition by the required fact. Use public search for discoverable documents, an authorized API for supported structured queries, and browser interaction for information revealed by form input or navigation. Go directly to interactive lookup when it is already required; making search exhaust its budget first can leave no opportunity to execute the necessary task.
5. Define a goal-level browser request: target, user-bound conditions, required facts, result scope, allowed actions, and execution budget. Inside that request, observe the current page, select real elements, apply conditions, read back the applied values, submit the query, verify the new result, and extract the needed original data. Do not require a small-model judgment before every click unless an evaluation justifies it.
6. Bind the result through every consumer. Preserve requested and applied conditions, original text/table structure, locator, snapshot identity, retrieval time, actual data-effective time, and unresolved facts. Trace the same evidence through citations, input freeze, formal handoff, final answer, persistence, and reopening. Test each boundary rather than stopping when the browser returns text.
7. Define fallback and failure semantics. Let uncertain or conflicting narrow judgments escalate to the main model using the same source state. Distinguish normal scoped zero results, partial coverage, condition mismatch, loading failure, access blocks, missing user input, cancellation, and unknown execution outcomes. Preserve valid results while repairing only the missing fact or failed narrow decision.
8. Evaluate the full task before promoting the tool. Compare several structurally different interactive scenarios and original user conditions with human-observed same-condition results. Measure total task latency, model calls, browser actions, retries, tokens, cost, evidence correctness, and result restoration. Leave confidence thresholds and numerical limits proposed until representative measurements support them.

## Decision-model placement

| Question | Preferred owner | Reason |
|---|---|---|
| Do exact dates, numbers, IDs, or permissions match? | Deterministic validation | A model probability cannot substitute for an exact invariant. |
| Does a passage support a specific claim under these conditions? | Narrow semantic model with escalation | Support depends on meaning, but requires an actual source passage. |
| Which retrieval route fits this information gap? | Narrow model or existing main model | Route selection can be scoped without transferring overall task ownership. |
| What should this user choose, and why? | Main reasoning model | Personal constraints and competing evidence require compound judgment and explanation. |
| May an external write execute? | Server authorization and scoped user approval | Model confidence does not confer authority. |

## Evidence and execution pitfalls

- Preserve a rendered result snapshot instead of re-fetching its URL as the sole verification method, because the same URL may return a blank form or a different query state.
- Keep the snapshot's text, table headers, units, options, and query conditions together, because an isolated value can describe a different period or configuration.
- Distinguish retrieval time from a value's effective date, because newly collected data may still describe an earlier period.
- Keep source existence, source integrity, semantic support, and current applicability as separate checks, because success on one does not establish the others.
- Do not let a routing model's negative result erase an unresolved required condition; allow the main loop to recover an incorrect route classification.
- Count nested browser-model and decision-model calls in the parent task's usage and limits, because a single top-level tool call can conceal many costly operations.
- Keep product sessions separate from the operator's personal browser profiles; authenticated interactive retrieval needs its own account, consent, and isolation contract.
- Review new-provider data transmission separately from public-search permission, because permission to search does not authorize sending private source bodies to another model provider.
- Classify read-intent form submissions by their effect rather than HTTP method alone, because legitimate queries may use POST and seemingly harmless controls may perform writes.

## Graph exploration and partial-delivery references

Use this procedure when an existing knowledge graph is slow or its visualization purpose is being reconsidered.

1. Trace the deployed path from map page to renderer, snapshot loader, delivery manifest, and authority validation. Classify materialized snapshots, transport parts, local display filters, selected-detail endpoints, and true neighborhood queries separately; precomputed data can still trigger expensive whole-map validation on delivery.
2. Fix the source comparison to repository commits and read the actual expansion, restoration, visibility, and data-update functions. Record license coverage for each inspected source, including paid example boundaries; a public core license does not establish rights to a separate commercial example.
3. Identify which work each implementation performs: hiding already-loaded elements, restoring retained children and edges, querying additional neighbors, or batching transport. Treat local add/remove APIs as model mutations until an actual server caller is found; renderer expansion alone cannot establish a partial backend read.
4. Prefer borrowing behavior into the existing renderer when it already provides layout and stable identities. Examine original-model versus visible-projection separation, reversible edge grouping, node and edge provenance, and position stability before proposing replacement; replacing rendering leaves upstream authorization and query costs unchanged.
5. For a proposed partial API, define seed, direction, relation types, depth, result bounds, and principal/scope/snapshot-bound cursors. Keep not-loaded, loading, partial, complete, empty, failed, and stale states explicit; complete-snapshot integrity checks require a distinct contract for partial results.
6. Verify shared neighbors, cycles, parallel edges, duplicate requests, response reordering, collapse/expand restoration, and generation changes. Test revocation, deletion, and identity switches against visible and hidden retained data, because reopening a collapsed group can resurrect an obsolete permission decision.
7. Measure the requested read scope and its authority checks separately from layout and rendering. Require a partial request to bound the delivered subset without silently weakening current access checks. Keep staged improvements, projections, and observed production behavior distinct; an optimized API that still leaves the user's screen failing remains an incomplete fix.

## Acceptance

Require condition fidelity, observed original evidence, truthful failure states, unauthorized-action blocking, session isolation, and consistent saved/reopened answers. Verify the explicit formal-decision handoff when the product has one. Separate software execution completion from satisfaction of the user's requested live lookup; a useful partial recommendation is not a confirmed exact-condition result.
