---
name: production-admin-api-operations
description: "Use when writing production admin API batches."
---

# Production Admin API Operations

Use for authenticated registry batches and narrowly scoped runtime configuration changes. This skill adds API-specific execution and verification steps.

## Procedure

1. Parse the approved target list and settings. Resolve contradictory activation values before writes; the chosen value changes production behavior.
2. Read the route dispatcher, authentication handler, request model, upsert implementation, and runtime resolution. Derive endpoint paths and response envelopes from the actual contract before calling them.
3. Verify cloud identity with the project's isolated authentication configuration and explicit subscription. Retrieve only the required credential into process memory; print sanitized verification fields.
4. GET existing rows and global defaults. Distinguish registry enabled, SDK enabled, background enabled, automatic-refresh enabled, and URL availability; independent gates can leave execution disabled after registration.
5. Apply supported per-target overrides when needed for requested activation. Preserve global defaults and unrelated targets, because shared defaults affect apps outside the approved batch.
6. Set behavioral fields explicitly, preserve literal identifiers and requested omissions, and account for nested-object replacement semantics.
7. Write each approved target once, recording identity and status. GET the exact target before recovering from an ambiguous response; a timeout can follow persistence, so blind retries can exceed an exactly-once request budget.
8. GET the registry again and assert exactly one row per composite identity with every requested field matching. Fetch each target's public runtime config and verify effective activation, URL availability, and interval.
9. Compare defaults and unrelated rows with pre-write snapshots before reporting preservation. Derive totals from parsed results.
10. Report briefly: verified target count, effective settings, generated-content availability, and concrete unverified execution stages. Keep registration, server config readiness, content generation, and device execution distinct; successful config fetch establishes server readiness.

Read [Authenticated batches](references/authenticated-batches.md) for the Azure CLI recipe and assertion checklist.
