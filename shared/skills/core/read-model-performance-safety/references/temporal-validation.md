# Temporal validation composition

Use when a read projection performs apparently duplicate authorization or immutable-reference validation and reducing those passes could lower storage reads.

## Establish the actual composition

1. Trace every caller from projection through disclosure or model reuse. Mark the last authority observation each caller actually reaches; source-opening fences cover only paths that invoke them.
2. Inspect stored references directly using payload-free counts. Compare complete references, frozen binding identities, source identities and excerpt hashes separately. Preserve every distinct frozen binding even when source and excerpt match.
3. Reconcile measured request operations against all validation passes and authentication work. Derive the proposed saving from directly counted references and validated operation costs; retain it as an estimate until the candidate is executed.
4. Identify sticky denial: check whether an early failed validation permanently redacts the result even if a later check succeeds. This behavior determines whether a late-only candidate preserves the contract.

## Run the mutation matrix before product edits

Build a scratch candidate changing only the proposed composition. Keep real application authority and store fixtures; replace only the external mutation boundary. Use fresh stores for baseline and candidate and assert each mutation's precondition.

| Mutation boundary | Control to assert | Decision it supports |
| --- | --- | --- |
| Stable valid state | Same content, citations, private-key filtering and all frozen bindings checked | Functional and operation-count baseline |
| Invalid before the call, remaining invalid | Both paths deny or redact | Persistent denial preservation |
| Valid during the early pass, revoked or replaced before the late pass | Early pass completed with valid content; mutation took effect; compare final disclosures | Detects removal of a later observation |
| Invalid during the early pass, restored before the late pass | Baseline early denial occurred; later store state is valid; compare final disclosures | Detects loss of sticky early denial |
| Mutation after the existing final pass | Record the existing protection boundary without asserting atomic disclosure | Bounds the claim honestly |
| Missing binding, mismatched excerpt or malformed reference | Actual exception/denial type, safe content and private-key stripping | Pairing and fail-closed behavior |
| Interruption during either retained pass | Original interruption propagates; existing budget is unchanged | Cancellation preservation |

Run the matrix for saved history and model reuse. Exercise standalone validation callers as well as service composition. Label helper invocations, ASGI requests, TCP requests and real authenticated storage flows according to the code actually executed.

## Decide and verify

- Preserve both observations when either removal changes required denial behavior. A lower operation count earns implementation only after the temporal contract and standalone callers pass the same matrix.
- Treat a caller-selected reference subset as an authorization-bypass surface even when its type is a list rather than a boolean. Prove validation ownership and every entry point before exposing such an argument in product code.
- Verify malformed-input claims with actual authority code before broadening exception handling; an earlier authority guard may already deny the input safely.
- Re-run the candidate and directly affected regressions in the parent. Preserve exact field bindings, citation pairing and public-key filtering while measuring operations.
- Report stable-state output agreement and temporal safety separately. A passing test that intentionally demonstrates candidate disclosure after revocation supports rejecting the candidate.
- Retain real account/storage reopening as a separate normal-path check. Keep provider duration, pure network latency, reported RU, complete billing and deployed capacity as distinct measurements.
