---
name: backend-independent-rereview
description: Re-review a fixed local Python backend with real probes.
---

# Independent re-review of a corrected local backend

Do not re-run the author's tests and call it a review. Write a separate probe script that hits the real seams, fix findings RED→GREEN, validate on two interpreters.

## Probe checklist (real loopback TCP, port 0, scratch DBs)
- Event loop: hold a SQLite `BEGIN IMMEDIATE` from another connection, then call a DB route **and** a no-DB route; also send a half-finished body and check other requests still answer.
- Worker pool saturation: queue more DB-bound requests than the anyio default (40) while locked, then probe health with a short timeout. Sync `def` endpoints **and sync dependencies** both consume pool threads — make pure in-memory ones `async`.
- Integer bounds on every query/path int that reaches SQLite: values > 2^63-1 raise `OverflowError` (not `sqlite3.Error`) → surfaces as 500 unless bounded with `le=`.
- Typed-error contracts: monkeypatch the provider to raise a *different* exception with the same message and confirm it does not take the typed path.
- Strict UTF-8: BOM, UTF-16, encoded surrogates, overlong bytes, duplicate `charset`, extra params, duplicate Content-Type headers (raw socket), missing Content-Type.
- Dedupe/concurrency: same conflicting body from 8 threads → row count must not grow.
- Legacy schema file: hash bytes before/after open attempt.
- `grep -rn '/opt/homebrew\|/usr/local/bin/python' tests` — "use sys.executable" fixes often miss one file; add a scanning test (build the pattern by string concat so the test itself does not match).

## PostgreSQL trial checks
- Separate mocked SQL-adapter tests from live TLS, advisory-lock, trigger and restart evidence; a SQLite transport cannot prove PostgreSQL behavior.
- Prefer catalog/has_table_privilege reads for permission checks. Distinguish reviewer-assigned limits from the user's actual authorization; do not label an agent-imposed limit as a user prohibition. When the user authorizes credential rotation, perform it on the exact role, atomically update private app configuration, verify fresh connections and data preservation, and never expose secret values. Respect any explicit user restriction on credential changes.
- Derive runtime DML grants from actual INSERT/UPDATE/DELETE call sites. Revoke unused DELETE and UPDATE, protect bootstrap metadata/identity writes, then reconnect as the runtime role to verify grants and exercise a fresh synthetic payout through reconciliation.
- For file-based hex secrets, reject a token equal to the secret's hex spelling as well as the decoded secret bytes. Keep the regression test on the actual configuration-loading boundary.
- Retest after permission hardening using existing-state-safe HTTP checks. Label those separately from the initial full clean-fixture smoke; never reset an existing ledger merely to rerun a smoke test.
- Derive reconciliation expectations from the existing ledger/provider snapshot, unresolved payouts and holds. A deliberately uncertain fixture can correctly keep a merchant blocked; do not erase it or expect balanced unconditionally. For a new hosted success/failure trial, use separate test schemas with the same minimum runtime grants, verify the exact deployment binding switched via settings and authenticated balance, restore the original binding in finally, then compare original table counts/content hashes and unknown reservations before claiming completion.

## Hosted-edge (Azure App Service) checks
- An exact-`Host` gate can reject platform warm-up pings if they do not carry the public hostname. Probe `/healthz` with an internal Host locally and inspect the configured accepted warm-up status codes; a 403 can block readiness only when 403 is not accepted. Do not infer actual probe Host or process liveness merely from a silent startup timeout. Preserve the public Host/Origin gate where possible: explicitly accepting `200,403` for internal warm-up is a verified alternative to code exemptions or removing settings, but separately prove readiness with authenticated storage requests. Revalidate stale no_ship findings against the final deployed artifact and timestamp.
- `az webapp log download --log-file x.zip` is read-only and gives `LogFiles/*_docker.log` + `StartupLogs/*_failure.log`; distinguish "process exited (fixed JSON line present)" from "process alive, probe rejected (no output)". Delete the zip afterwards: Kudu traces embed auth headers.
- Exercise the real `main()` with `run=` swapped for a 127.0.0.1:0 uvicorn runner so startup config, DB opening and `BIND` are observed without binding 0.0.0.0.
- h11 rejects duplicate `Host`, NUL bytes and non-numeric `Content-Length` with 400 before any middleware; count those as fail-closed, not as app behavior. `bytes.fromhex` ignores ASCII whitespace; FastAPI query ints are lax (`+1`, `1_0`, `1.0`).

## Fix discipline
Add the failing test to the review test module first, observe nonzero exit, then change code. Never widen expectations.

## Durable observer and recovery reviews
- Keep transport hints separate from durable state. Reproduce a dropped hint and a crash between checkpoint persistence and notification using real producer, claim, CAS/fence, and committed private-body reads; prove later recovery without repeating a paid provider step.
- Inject only the model/observer/storage boundary needed for an offline probe. Preserve authority checks before and after those boundaries; a notification failure must never turn an awaiting checkpoint into a partial-answer fallback.
- Normalize a conditional test store's observed ETag mismatch to its real protocol error at the test boundary when the fixture uses assertions. Never catch AssertionError in production to make a conflict test pass.
- Retry only bounded metadata contention. Preserve the original job ETag, lease/fence, deadline, and source-authority snapshot; re-read only the contended turn, and prove ownership/revision changes still reject publication.
- Count pending-poll reads, writes, ledger documents, and provider calls separately. A bounded poll backoff can reduce invocation growth while paid-call replay protection alone leaves DB accounting growth intact.
- Capture full-suite JUnit and compare exact failing identities as well as failure class against a prior receipt. Ordering-sensitive cases can move between runs; report the observed identity delta rather than asserting the failed set is identical.
- Honor repository interpreter bounds and explicit installation/network restrictions. Record an unavailable second supported interpreter as a verification gap instead of installing dependencies or testing an unsupported runtime.

## Multi-interpreter validation
`python3.X -m venv $TMPDIR/<name>-venv && pip install -e '.[extras]'`; run suite with `-W default` and `-X tracemalloc=25` to locate warnings. Python ≥3.13 emits `ResourceWarning: unclosed database` for `with sqlite3.connect() as db:` (commits, never closes) — fix with `with contextlib.closing(sqlite3.connect(p)) as db, db:`. Record `fastapi/starlette/pydantic/uvicorn.__version__` by importing inside each venv; `pip list` from a kernel with another venv active can lie.

## Docs
Keep "minimum supported" (`requires-python`) separate from "documented dev runtime". When a design decision was written as if it were a user-agreed universal rule, relabel it as a temporary implementation decision and list exactly which provider facts are still unverified instead of inventing policy.
