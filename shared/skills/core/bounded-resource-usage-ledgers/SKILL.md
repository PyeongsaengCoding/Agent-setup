---
name: bounded-resource-usage-ledgers
description: Use when adding per-execution resource usage ledgers.
---

# Bounded resource accounting

- Inspect the actual worker wire before adding metrics; signed evidence byte counts do not imply CPU, RSS, session occupancy or site-network measurements.
- Aggregate client operation counts, monotonic durations and measured payload bytes in fixed resource/operation buckets; keep missing units absent and list missing metrics per resource.
- Persist one identity-bound invocation ledger before external work; correlate recoveries with bounded unique invocation IDs and preserve failed/unknown attempts when later attempts succeed.
- Mark delivery resources not_in_path only from the actual runtime transport; bounded database discovery does not produce Storage Queue request counts.
- Keep pure counters independent of ledger context and storage adapters so the repository architecture gate catches no new import cycle.
- Verify an actual dispatcher/private storage/question-resume flow with operation counts, lost-result outcomes and cross-workspace references; follow with focused regressions and shared-contract gates.
