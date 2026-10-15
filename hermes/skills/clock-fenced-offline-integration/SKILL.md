---
name: clock-fenced-offline-integration
description: Use when checking offline clock-fenced integrations.
---

# Clock-fenced offline integration

## When to use

Use when an authenticated receiver borrows an already-prepared controller with a separate monotonic clock and tests must preserve frozen cores. Keep actual runtime activation behind its existing approval gates.

## Procedure

1. Read both real APIs and their test loaders; preserve module/type identity when reusing dynamic fixtures. Pin existing-source hashes before new writes.
2. Write and run an interface or behavioral failing test in a shell before implementing the adapter. State missing-interface RED separately from assertion RED.
3. Keep context entry, preparation and lifetime locks with the caller. Give one borrower exclusive single-use ownership; test duplicate adapters as well as concurrent grants.
4. Capture a UTC/monotonic anchor before prepared reads. Map authenticated expiries using the minimum of that original mapping and later conservative samples. Preserve stored TTL/proof bounds even when the controller refreshes its private proof.
5. Inspect reserve functions instead of adding named reserves blindly. Derive the effective minimum ceiling and account for core floor rounding and elapsed I/O.
6. Where a frozen core lacks UTC checks inside admission, install a guarded explicit offline-engine boundary before preparation. Check original bounds before and after each external open/observe and after synchronous cleanup. Keep production defaults unavailable.
7. Exercise the full existing producer, receiver, durable ledger, private writer/reader, commit and retained-consumer path. Pin source URL, applied conditions, bounded body/excerpt and digest; reject malformed or mutable engine binding.
8. Test transport exhaustion while the execution lease remains live. This distinguishes adapter publication guards from existing lease guards. Reopen unknown ledger rows only after old-slot destruction and prove zero re-observation.
9. Produce source/fixture-bound JSON receipts from actual execution. Recheck frozen hashes, adjacent tests, lint and architecture before reporting the offline result.

## Pitfalls

- Sample tolerance must never rebase or extend the original expiry mapping.
- A fresh proof may exceed stored authority; include the original stored proof in the deadline passed to the core.
- Install import-safe network guards. Optional library capability probes may attempt loopback binds; suppress those capabilities explicitly in the isolated runner while keeping audit refusal active and preserving diagnostic evidence.
- Pytest current-directory symlinks can duplicate receipt discovery; filter symlink parents before asserting totals.
- Synchronous cleanup and storage calls remain non-cancellable. Preserve uncertainty when they overrun; qualify real supervisors separately.

## Verification

Require observed connected found/empty receipts, zero actual socket/DNS/subprocess calls, zero new execution/publication on committed replay, post-cleanup deadline refusal, unchanged frozen sources, and explicit runtime/deployment HOLD gates. Distinguish target-version AST parsing from execution with that interpreter.
