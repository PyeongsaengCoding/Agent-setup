---
name: omh-backend
description: "[omh] Designing an API, server, or data-layer change: prepare server, API, and data-layer contracts — auth boundary, error paths, response shape, and schema/migration discipline — before implementation."
---
# Backend

This is a Hermes-native `backend` workflow skill.

## Why This Exists

`backend` gives OMH a first-class server-side workflow so Hermes can prepare auth boundaries, error paths, response shapes, and migration order without becoming the hidden runtime that executes them.

## Do Not Use When

- The work is the database itself -- a slow query and the index that fixes it, DDL that locks a live table, N+1 queries, or when to partition or shard; use `relational-db`, which owns the lock behaviour and rollback of each statement.
- The request is about web UI, layout, or a design system; use `frontend`.
- The request is a security posture or threat review rather than a service design; use `security-safety-review`.
- The request is to run or judge the verification of an already-built service; use `verification-gate`.
- The request is a Rust-language change whose risk is compiler, ownership, or `unsafe` discipline; use `rust`.
- The work is a batch or streaming job's rerun, backfill, duplicate rows, or a warehouse table's downstream readers; use `data-pipelines`.

## Examples

Good example:

- Prompt: Design a REST API with a Postgres schema and migrations for the billing service.
- Expected behavior: Prepare backend_service_contract/v1, auth_boundary_map/v1, error_path_table/v1, response_shape_contract/v1, and schema_migration_plan/v1, then hand off with the per-stack reference named.
- Why: The request is server-side design across an endpoint surface and its storage, before any code exists.

Bad example:

- Prompt: The migration is written, so mark the schema as migrated and the API as live.
- Expected behavior: Mark migration application, integration runs, and deployment as not_observed and name the smallest observed proof for each.
- Why: A prepared migration plan is not an applied migration, and a contract is not a running service.

## Completion Checklist

- The surface, its callers, and each caller's trust level are named.
- The auth_boundary_map/v1 states where trust changes and which check enforces it on every path.
- The error_path_table/v1 covers each failure mode with status, body shape, retryability, and redaction rule.
- The response_shape_contract/v1 is consistent across endpoints rather than per-endpoint improvisation.
- Storage changes carry an expand/backfill/switch/contract order with a rollback point per step.
- A change to an existing contract carries its consumer list or an explicit `consumers_not_enumerable`, plus the compatibility window, migration path, and sunset date.
- The handoff names the executor, the stack, and the per-stack reference to load first.
- Implementation, migrations, integration runs, and deployment stay observed-only.

## Recovery Notes

- For a new model-provider connection, verify the configured model against the authenticated account's current model listing before a paid smoke. Documentation examples can name versions outside that account's offered list. Record the validated response model separately from the requested alias in provider usage evidence.
- Verify the provider from the process-scoped runtime composition and approved secret-injection path. Keep live transport evidence distinct from fixture inputs, in-memory journal stores, user-account UI flows and production activation.
- If the stack or datastore is unknown, prepare the contract stack-neutral and name the stack as the one blocking input.
- If the auth model cannot be established, stop at the auth boundary gap instead of designing endpoints that assume a trust level.

## Workflow Lane

- Current lane: **Coding handoff** (`idea-to-deploy`, `llm-app-dev`, `cto-loop`, `deploy-and-monitor`, `code-review`, `build-failure-triage`, `verification-gate`, `security-safety-review`, `+28 more`) - coding owners, handoffs, review, CI, and merge evidence.
- If intent belongs to another lane, hand back to `oh-my-hermes` or name the adjacent workflow.
- Shared product, routing, compatibility, and evidence rules: `omh-routing/references/skill-common-rail.md`.

## Use When

Use when Hermes should shape a server, API, or data-layer change before implementation: authentication boundary, contract error paths, response consistency, schema and migration discipline, and the per-stack reference the executor loads first.

    Strong routing signals: `backend`, `back-end`, `back end`, `backend skill`, `server side`, `server-side`, `api design`, `api contract`, `rest api`, `graphql api`, `grpc service`, `endpoint design`, `auth boundary`, `authentication flow`, `authorization rules`, `idempotency key`, `pagination contract`, `database schema`, `postgres schema`, `schema migration`, `db migration`, `orm mapping`, `connection pool`, `message queue`, `webhook handler`, `openapi`, `openapi spec`, `deprecate endpoint`, `deprecate this endpoint`, `deprecation window`, `sunset date`, `sunset schedule`, `api versioning`, `breaking api change`, `バックエンド`, `エンドポイント設計`, `認証フロー`, `スキーマ移行`, `백엔드`, `서버 개발`, `서버 api`, `api 설계`, `인증 흐름`, `권한 체크`, `디비 스키마`, `db 스키마`, `스키마 마이그레이션`, `엔드포인트 설계`, `后端`, `後端`, `接口设计`, `认证流程`, `数据库迁移`

## Catalog Metadata

Category: `planning`
Phase: `backend-design`
Hermes role: `planner`
Quality tier: `backend-contract-gated`
Reasoning demand: `standard`

## Existing editing and semantic-data review procedure

1. Trace the real editor payload through its route and domain mutation to storage, change history, projection invalidation, and the next consuming request. Identify each record's authoritative owner and revision; a save callback or refresh request proves only its own stage.
2. Classify edits before selecting a command: label/identity changes, instance relationship changes, personal condition values and scope/time, and shared schema or ontology extensions. Reuse the current owner for each class rather than duplicating a condition inside a relationship label, because duplicate stores can diverge.
3. Keep natural-language input at the change-draft boundary. Bind the proposed target and base revision, operation, before/after meaning, scope, validity and provenance to a server-validated canonical command. Resolve only material ambiguities and show the actual change for confirmation; connect structured and sentence editors to the same mutation contract.
4. Inspect composed mutations for partial success. An exclude-then-create sequence needs durable completion, idempotency and recovery of the combined operation; test failure after the first write and a repeated submission before claiming an atomic edit.
5. Trace consumer eligibility explicitly: automatic selection versus explicit selection, feature gates, scope/time, authorization and frozen input revision. Preserve source statements, user corrections and historical decisions separately, because a displayed edit can coexist with an unchanged or ineligible model input.
6. Exercise focused existing contracts, then specify the connected acceptance case: edit, save, projection, refresh/reentry, next relevant answer or decision, and withdrawal. Report implementation, local behavior and deployed behavior separately. When only a design review was approved, return the gaps and smallest complete implementation slice without changing runtime gates or production data.

7. For a knowledge-generation lifecycle review, enumerate connected-source imports, live user messages, assistant outputs, completed decisions and manual edits separately. Trace each through extraction, admission, persistence, projection and later consumption; distinguish instance generation from ontology/schema evolution, because different producers can share a screen while retaining different authority and rollout gates. Compare inspected code with the serving revision and read narrowly allowlisted runtime configuration before describing a path as active. Follow the generation audit in `references/consumer-impact.md`.
8. When the user asks to settle one stage first, inspect that stage's existing owner-scoped diagnostics and one actual authorized record before proposing another tracking system. Separate completed work, admitted entities, admitted relations, held candidates, publication and observed use. Inspect exclusion reasons and classified meanings before widening an admission policy, because a successful job or empty blocker field can coexist with no usable relationships. Keep bounded-list totals and sample coverage explicit.

For consumer and projection details, extend the existing review with `references/consumer-impact.md`.

Quality bar:

- Name the surface, its callers, and their trust level before any endpoint or table is designed.
- Load `references/service-contract.md` and fill the auth boundary, error-path table, and response-shape rules from it rather than improvising a per-endpoint shape.
- When the change touches storage, load `references/schema-migration.md` and order the migration as expand, backfill, switch, contract, with the rollback point named per step.
- Hold the `api` product-family expectations — authentication boundary, contract error paths, response consistency — as the standing bar for every prepared endpoint.
- When an existing contract changes, name who consumes it before designing the change: each identified consumer with what breaks for it, then the compatibility window, migration path, and sunset date — the skill that owns a surface owns its evolution. Load `references/consumer-impact.md` for the enumeration sources and the window rules.
- Name the per-stack reference the executor must read first; the stack is a routing input, not a detail discovered mid-implementation.
- Keep implementation, migration application, integration runs, load testing, and deployment as observed-only evidence.

Handoff policy:

Keep the service contract, auth boundary, error-path table, and migration plan in Hermes. Record code changes, running servers, applied migrations, integration runs, and load results only from executor or wrapper observed evidence.

Required inputs:

- the service, endpoint, or data surface being changed
- callers and their trust level (public, partner, internal, machine)
- language, framework, and datastore when known
- authentication and authorization model in force
- existing schema and migration tooling
- backward-compatibility and rollout constraints
- observed integration or load evidence for completion claims

Expected outputs:

- backend_service_contract/v1
- auth_boundary_map/v1
- error_path_table/v1
- response_shape_contract/v1
- schema_migration_plan/v1 when the change touches storage
- consumer_impact_and_sunset/v1 when an existing contract changes
- backend_implementation_handoff/v1
- observed_integration_evidence/v1 when observed

Artifact expectations:

- backend_service_contract/v1 names each endpoint or job, its caller class, request and response shapes, and its idempotency and pagination rules
- auth_boundary_map/v1 states where an untrusted caller becomes a trusted one, and which check runs on each path
- error_path_table/v1 pairs every failure mode with its status/code, body shape, retryability, and log/redaction rule
- response_shape_contract/v1 keeps success and error envelopes consistent across the surface instead of per-endpoint improvisation
- schema_migration_plan/v1 orders expand, backfill, switch, and contract steps with the rollback point for each
- consumer_impact_and_sunset/v1 lists each identified consumer with what breaks for it, then the compatibility window, the migration path, and the sunset date; a consumer set that could not be enumerated is reported as `consumers_not_enumerable` with the reason, never as zero breakage
- integration runs, applied migrations, load numbers, and deployment only when observed

Safety rules:

- Do not claim implementation, a running service, an applied migration, a passing integration suite, or a deployment from a prepared backend contract.
- Require the auth boundary before endpoint work: an endpoint whose caller trust level is unnamed is not ready for handoff.
- Require the error-path table before the happy path is called complete; an unlisted failure mode is a gap, not a default.
- Treat a destructive or non-reversible migration step as a blocker until an explicit rollback point and backfill order exist.
- Report an unenumerable consumer set as `consumers_not_enumerable` with what was searched; consumers outside the repository are unknowable from it, and an empty list is a claim that nothing breaks.
- Never place secrets, tokens, or connection strings in the contract, examples, or handoff text.
- Do not call databases, HTTP services, LLM, or network endpoints from OMH core.

## Runtime Evidence

Preferred harness for this skill: `coding-handling`.

```sh
omh runtime record --skill backend --harness coding-handling --status started
```

Record observed delegation results; otherwise return `not_available` or `not_observed`.
Prepared OMH routing is not execution, review, CI, merge-readiness, or merge evidence.
- Treat wrapper memory/context summaries as advisory local context, not proof of opaque Hermes memory reads or changes.
Preserve workflow intent and stop conditions; verify before claiming completion.
Reply in the user's own words and the host's own voice: its SOUL.md persona owns reply language, tone, speech level, and sentence endings, progress updates included (where it sets no language, use the one the user wrote in), and OMH shapes structure and content only; OMH's record terms (surface, lane, wrapper, handoff, evidence boundary, not_observed) stay in records and tool calls, never in the sentence the user reads unless they ask about one; and when a stop condition or a decision the user owns ends the turn, offer the next action as a question rather than declaring what will not be done.

Use Hermes-native subagent/delegation features when available: native subagents -> Hermes delegation when available, otherwise sequential lanes.

Shared product, compatibility, topology, memory, harness, and execution rules: `omh-routing/references/skill-common-rail.md`. Load it when applicable; otherwise name an unavailable capability.

## Hermes Compatibility Contract

This skill was imported by `omh` from a local skill source.

- Keep the upstream workflow intent, but adapt runtime behavior to Hermes Agent.
- Do not require runtime features that Hermes Agent does not expose.
- Use Hermes `skills_list`, `skill_view`, file tools, terminal tools, and Hermes delegation when available.

