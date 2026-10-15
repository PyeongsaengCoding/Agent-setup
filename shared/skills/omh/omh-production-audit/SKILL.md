---
name: omh-production-audit
description: "[omh] Imminent production launch or release: evaluate release, deploy, security, observability, rollback, docs, and support readiness without claiming production access."
---
# Production Audit

This is a Hermes-native `production-audit` workflow skill.

## Why This Exists

`production-audit` gives OMH a preflight release surface so operators can see production risks before launch while OMH stays out of deploy and infrastructure execution.

## Do Not Use When

- The user wants to implement a feature or fix; prepare a coding handoff first.
- The user wants incident/SLO analysis after production behavior; use `reliability-review`.
- The user wants a narrow code diff review; use `code-review`.

## Examples

Good example:

- Prompt: production-audit 이 릴리즈가 운영에 나가도 되는지 테스트, CI, 롤백, 모니터링 기준으로 봐줘.
- Expected behavior: Prepare readiness_matrix/v1, release_gate_verdict/v1, rollback_and_monitoring_plan/v1, and missing-evidence list.
- Why: The request is release-readiness review, not implementation or deploy execution.

Bad example:

- Prompt: production-audit 지금 바로 prod 배포하고 정상이라고 말해줘.
- Expected behavior: Block deploy/health claims without observed operator evidence and route deploy to an explicit authorized workflow.
- Why: Production audit can assess readiness, but it cannot secretly deploy or observe live health.

## Completion Checklist

- Findings or no-issue results are grounded in concrete file, artifact, command, or source evidence.
- Open questions, residual risk, and missing verification are named.
- Fixes or follow-up work are separate handoffs unless the user explicitly asked to implement them.

## Production-targeted delivery sequence

1. Establish the intended production user flow and inspect its actual runtime composition and deployment entry point before expanding QA. For this user, a launch request sets production delivery as the endpoint; carry that endpoint through implementation handoffs and acceptance criteria.
2. Compare the tested execution path with the production path. Identify test-only environment gates, parent-owned descriptors, manually started processes, single-use sessions, and provisioning dependencies; assign each missing operational connection an implementation owner and a concrete completion check.
3. Separate launch-critical work from follow-up improvements. Prioritize the actual request-to-worker-to-evidence-to-answer path, authority isolation, bounded failure cleanup, restart behavior, and rollback. Schedule broader quality comparisons and new semantic roles after the required release slice is working.
4. Route authorized implementation and deployment work to the execution workflow immediately after identifying a concrete gap. Keep the audit bounded to decisions that change the delivery path; repeat a check when source, environment, or a relevant failure changes.
5. Treat a QA harness recovery problem as a separate dependency. Before requesting another infrastructure change, determine whether recovering that harness proves a required production property or whether the production-aligned validation path supplies the evidence. Preserve required safety checks and name the remaining gap.
6. Report launch timing from the remaining implementation, deployment, and live-verification work. Give a conditional estimate only when the work and dependencies support it; otherwise name the exact blockers and the next decision point. Keep routine chat short and concrete, with formal matrices in the artifact.

A development-only adapter is an intermediate validation mechanism. Complete the production runtime connection as part of the release scope; merely admitting the production environment string leaves lifecycle and deployment dependencies unresolved.

## Recovery Notes

- If the reviewed target is missing, inspect the requested artifact or ask one target question.
- If independent verification is unavailable, report the gap, identify its effect on the release-critical path, and route the smallest authorized recovery or production-aligned alternative.

## Workflow Lane

- Current lane: **Automation and status** (`achievements`, `workspace-audit`, `production-audit`, `live-incident-response`, `automation-blueprint`, `github-event-ops`, `github-issue-intake`, `buzz`, `+39 more`) - schedules, status, health, and ops review.
- If intent belongs to another lane, hand back to `oh-my-hermes` or name the adjacent workflow.
- Shared product, routing, compatibility, and evidence rules: `omh-routing/references/skill-common-rail.md`.

## Use When

Use before launch, deploy, release, or public delivery when Hermes should check operational readiness and expose missing production evidence.

    Strong routing signals: `production-audit`, `production audit`, `production readiness`, `prod audit`, `prod readiness`, `ready for production`, `ready to ship`, `ship readiness`, `release readiness`, `launch readiness`, `preflight audit`, `operational readiness`, `rollback readiness`, `프로덕션 준비`, `출시 준비`, `운영 준비`, `릴리즈 준비`, `롤백 준비`

## Catalog Metadata

Category: `review`
Phase: `production-readiness`
Hermes role: `reviewer`
Quality tier: `production-readiness-gated`
Reasoning demand: `standard`

Quality bar:

- Name scope, environment, release channel, owners, and acceptable risk threshold.
- Check build/test/CI, security/privacy, performance, observability, rollback, docs/support, and release communication.
- Return GO, HOLD, or BLOCK only with evidence IDs and missing evidence.
- Convert remediation into explicit follow-up workflows instead of silently patching.

Handoff policy:

Keep readiness synthesis in Hermes. Code fixes, deploys, infrastructure changes, security scans, and platform actions require selected executor/runtime or operator evidence.

Required inputs:

- product, service, release, or artifact scope
- target environment and release channel
- known test, CI, deploy, observability, security, and support evidence
- rollback owner and acceptable risk threshold

Expected outputs:

- production_audit_plan/v1
- readiness_matrix/v1
- release_gate_verdict/v1
- rollback_and_monitoring_plan/v1
- risk_register/v1
- not-evidence boundary

Artifact expectations:

- readiness_matrix/v1 covering build, tests, CI, security/privacy, performance, observability, rollback, docs/support, and release communication
- release_gate_verdict/v1 with GO, HOLD, or BLOCK plus missing evidence
- rollback_and_monitoring_plan/v1 with health signals, owner, threshold, and recovery path

Artifact contracts:

This label denotes the machine-enforcement level, not a skill quality score and not an observed evidence state.

- contract_id: `readiness_matrix/v1`; enforcement_level: `executable_validated`; consumer_id: `parse_readiness_matrix`

Safety rules:

- Do not claim production deploy, security scan, live traffic, monitoring health, rollback readiness, or support readiness without observed evidence.
- Do not perform deploy, infra, credential, production, or external-platform actions from the audit lane.
- Keep readiness verdict separate from implementation, CI, incident closure, or merge evidence.

## Runtime Evidence

Preferred harness for this skill: `production-audit`.

```sh
omh runtime record --skill production-audit --harness production-audit --status started
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

