---
name: future-effective-memory-tdd
description: Use when fixing future-effective memory updates.
---

# Future-effective memory updates

## When to Use

Use as a focused testing companion to `semantic-knowledge-lifecycle` for scheduled replacement bugs in persisted owner memories. Load that class-level skill first and consult its lifecycle-invariants reference for shared deletion, owner correction, scheduled values and atomic replay.

## Workflow

- Reproduce the future-update gap through the real recording workflow before changing production code; an isolated time predicate cannot prove lifecycle correctness.
- Inspect canonical identity, revision, source proof, retention, and frozen-input consumers before choosing a representation; each consumer must resolve the same effective value.
- Retain the earlier source-bound value until the replacement starts, and enforce the earlier value's own expiration; selecting an expired replacement must never fall back to an older value.
- Keep the current canonical id/revision authoritative when projecting an earlier effective value, and bind lifecycle snapshots to the same atomic recording event; do not synthesize source authority from display text.
- Write and run one failing end-to-end behavior at a time: recording/capsule, decision cutoff/validation, pending selection, owner edits, collision guards, and release-fence source rechecks.
- Keep pending future values visible to the selection model while withholding them from current-use readers; reject re-add collisions both during admission and at the canonical write boundary.
- Clear effective-value metadata on owner edits and honor deletion/clear/source withdrawal before resolving historical values; inherited snapshots must not undo current controls.
- Refuse an overflow that would discard still-needed effective versions, and report that bound explicitly; completed intervals can be pruned without losing current applicability.
- Control both source-message timestamps and consumer clocks, using UTC-aware instants; test exact inclusive start, exclusive end, repeated schedules, and cold-store reopening.
- Fail an owner batch before writes and replay the persisted selection with an observed zero-extra-provider-call assertion; verify unchanged canonical usage and the shared item/event/settings transaction.
- Keep shared command parsing in a lower-level policy module imported by both recording and suppression, preserving supported caller imports when moving the helper. Run the architecture check alongside behavioral tests, because a reverse suppression-to-recording import creates a cycle that Ruff and runtime imports can miss.
- Distinguish isolated store/synthetic transport evidence from real account, model semantics, browser, and deployment verification.
