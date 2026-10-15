---
name: isolated-read-batch-fences
description: Use when parallelizing read tools with mutable state.
---

# Isolated read batches

- Snapshot each callback's catalogue, plan, per-turn flags and callback-owned dictionaries before dispatch; buffer progress and persistence effects. A thread pool over shared callbacks still races source IDs and durable state.
- Admit the complete proposal before any callback. Reject malformed arguments, repeated call IDs, non-read operations, over-budget proposals and every unresolved receipt, including unexpected statuses.
- Keep reads requiring newly discovered IDs or private-derived public targets for a subsequent model round. Admit mixed public/private branches only with a conservative basis for independence; preserve privacy preparation.
- Persist all admitted reads as started before dispatch. Copy context separately per worker so existing thread-safe provider accounting and journals retain execution identity.
- Merge citations in proposal order and remap identifiers in structured results. Freeze merged sources and compare the exact returned frozen payload before releasing buffered effects or completed receipts.
- Classify read failures by execution ownership and certainty before choosing fallback. Keep prior-owner started receipts and unfinished isolated branches unresolved; stop pending work and discard late output. For a synchronous read that returns an observed ordinary failure in the current owner, persist a sanitized terminal failure before considering the previously validated answer. Recheck current authority and frozen sources before delivery; keep cancellation, authority, storage and deadline failures on their dedicated guarded paths. Marking every current failure unresolved can erase an already acquired answer.
- Test unknown replay with a successful controlled read whose saved receipt is replaced by the exact unresolved state. Test live corrective failure separately with first answer → failing read → saved-answer readback and replay without new calls. Preserve both assertions; changing answer preservation to an exception expectation can hide a user-visible regression.
- Use [read failure recovery](references/read-failure-recovery.md) when adding failure receipts or changing saved-answer fallback; it defines the classification and product-loop probes.
- Cache only completed reusable results under canonical arguments and exact turn/context authority. Revalidate source access on replay; preserve full results instead of returning an empty duplicate marker.
- Record callback time separately from freeze/authority overhead to preserve research-budget reserves.
- Prove overlap at real retrieval callbacks, then run a product-loop persistence probe. Cover cancellation with a blocked worker released after return, authority failure before effects, frozen-slot mismatch, unknown replay, provider-budget propagation and serial dependencies.
