---
name: durable-sqlite-test-ledger
description: Use when building crash-safe SQLite test ledgers.
---

# Durable SQLite Test Ledgers

## When to Use

Use for local synthetic-only transaction simulators that must survive separate CLI processes. This is not authorization for external payments or a production financial design.

## Procedure

1. Read repository instructions and required Python version; verify the selected interpreter in a shell before RED. Preserve the existing in-memory API and unrelated dirty files.
2. Follow vertical TDD: deposit and reopen; idempotency and allocation; reservation; write claim; observation; independent provider persistence; CLI. Capture missing-interface RED separately from assertion RED. Add later coverage of existing behavior without fabricating failures.
3. Use separate databases for the local ledger and simulated provider. Their schema identities must differ. Create owner-only files exclusively; reject symlinks, permissive files, unsupported versions, and unknown schema instead of resetting.
4. Reserve and claim under `BEGIN IMMEDIATE`. Commit uncertain state, provider identity, stage, and correlation before the side effect. A claimed stage must never be resent, including after a crash before the provider actually wrote anything.
5. For multi-write providers, acknowledge each stage separately. Persist all next-stage lookup IDs atomically using an allowlisted identifier map; never store response bodies, credentials, or raw accounts. Do not call the next write until its predecessor is confirmed.
6. Match all observation identity fields and integer amount exactly. Repeated final results are idempotent; failure releases only the reservation; stale acknowledgements cannot reverse a final result. Make conflicts sticky and block new merchant writes.
7. Persist evidence events in the same transaction as the state transition. Test rollback by failing event persistence, and make event update/delete fail.
8. Keep the CLI opt-in and ahead of environment/credential loading. Sanitize both subparser errors and root-level unknown arguments. Display balances using the persisted payout member rather than the CLI default member.

## Verification

Run subprocess tests and the full repository suite with the same interpreter. Exercise actual process exits before and after provider commit; reopen both databases; prove query recovery without another write claim. Run concurrent CLI requests and submits, verify isolation and no overdraft, and check schema-corruption and sticky-conflict handling. Run a separate-process user-surface smoke, print observed state/counts and file permissions, then verify temporary database cleanup. Report exact observed totals, external integration boundaries, and interface path/line anchors.

## Recovering a lost staged-write response

- Before giving up on a missing provider key, check whether an official list/group inquiry returns multiple pending items; a key already stored from your own verified sibling request on the same shared demo account may expose the lost request. Match every identity field and the amount exactly; never guess keys or use `ALL`.
- Claim a cancellation once, durably, before sending; never resend it. If its reply fails strict validation, close the ledger only from independent read evidence: the item is gone from the pending list AND date-scoped execution results (every date since the request) show zero own or same-key executions. Unreadable evidence keeps the reservation.
- Preflight with a read call that the guarded transport actually allows; a blocked preflight looks like a transport error, not readiness.
- Preserve an allowlisted provider business code separately from the local validation code when a real successful response fails identity or amount checks. Revalidate an already captured response without financial retransmission; retain strict ACK guards and release only through independent scoped evidence.
- Freeze execution-date iterables before validation and reuse that same nonempty tuple for queries. Test a generator with positive execution evidence and an empty generator so validation cannot silently consume the query scope. Require callers to cover every observed request-to-absence date and document any legacy timestamp gap.
- Choose response-size limits per exact endpoint in both transport reads and parser checks. Keep authentication and cancellation at their normal bounds while permitting bounded larger daily-result bodies; test overlapping calls with deterministic barriers so shared global limit changes cannot leak.
- Persist the returned error code, failure stage and allowlisted failed-field names before reducing outcomes to an unknown recovery state. Exclude identifiers, secrets, financial response values and exception text. Test that this diagnostic survives reopening without another write.
- Separate missing diagnostic evidence from the underlying provider failure. A generic unknown result cannot establish a response-field mismatch; correct any unsupported claim and state which original evidence was lost.
- Keep preflight failures actionable: ensure its read endpoint is allowed and stop before a financial write when the preflight fails. A preflight return value that is ignored provides no readiness guarantee.
- Copy the private ledger owner-only and exclusively before the first real recovery write.

## Pitfalls

- A storage layer that translates SQL between SQLite and a secondary backend (e.g. Postgres, `?`→`%s`, `ORDER BY rowid`→`ORDER BY _ordinal`) only covers the literal patterns it was built to translate. A new query that orders by bare `rowid` on a table that was never given an explicit ordinal column passes every SQLite test and fails only on the real secondary backend with a column-not-found error, surfaced as a generic 'storage unavailable'. If that backend deliberately rejects live DDL migrations (schema/catalog hash validated per request), do not add a column to fix it — order by an existing append-only sequence column already present and identically shaped on both backends (e.g. a correlated join to an events/audit table's own autoincrement `seq`). Verify any new ordering/paging query against the real secondary backend before calling it portable; an SQLite-only test suite cannot catch this class of bug.
- Provider acceptance is not final payout success.
- Missing provider records after an uncertain write do not authorize resubmission.
- A shared demo balance is not a confirmed customer deposit.
- Test-provider markers identify trusted adapters; they are not a sandbox for arbitrary code.
- For a live probe after editing adapter types, use a fresh interpreter or reload every dependent bridge/recovery import together. A partially reloaded dataclass can fail an `isinstance` guard and turn a valid captured provider read into a local adapter error; retain funds, inspect safe diagnostics, and repeat only authorized reads.
- Local SQLite durability is not remote provider or real-money verification.
