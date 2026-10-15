---
name: omh-product-brief
description: "[omh] PRD or roadmap priorities to decide: turn product evidence into a decision-ready PRD, prioritization frame, and roadmap brief."
---
# Product Brief

This is a Hermes-native `product-brief` workflow skill.

## Why This Exists

`product-brief` turns product evidence into a reviewable PRD and prioritization frame before delivery planning without treating a draft as an accepted roadmap commitment.

## Do Not Use When

- The input is unprocessed feedback, bug reports, or feature asks that first need clustering and evidence boundaries; use `feedback-triage`.
- The product evidence is unvalidated, synthetic, or a founder belief and the problem gate has not returned validated; use `product-discovery-validation` before a PRD.
- The input is a growth hypothesis that still needs an experiment and readout before it becomes a product requirement; use `lifecycle-growth`.
- The user needs a company or product strategy decision across high-level options rather than a requirements or roadmap artifact; use `strategy-brief`.
- The request is an accepted, code-ready change with repository constraints and verification needs; use `ralplan` or `ultrawork` rather than recreating a PRD.
- The user asks to create or update Jira, Linear, Aha!, or a roadmap system directly; use `connector-operator` with explicit target, approval, and observed evidence.

## Examples

Good example:

- Prompt: Create a PRD and prioritization options for reducing first-time user drop-off in onboarding.
- Expected behavior: Prepare the product problem, user and metric brief, PRD, roadmap options, tradeoffs, and downstream prerequisites.
- Why: The request needs a decision-ready requirements and prioritization artifact before delivery planning.

Bad example:

- Prompt: Implement the accepted onboarding PRD and open a PR.
- Expected behavior: Route to `ultrawork` or `ralplan`, not `product-brief`.
- Why: Accepted implementation work should move into planning or delivery rather than recreate a PRD.

## Product-purpose procedure

1. Read the current product contract and implemented user actions before defining a troubled feature's purpose; this prevents proposing an existing capability as new work.
2. Define the automatic system benefit and the user-facing surface benefit separately. For knowledge or ontology products, describe what accumulated context improves in answers and decisions, then identify the concrete reason a user would voluntarily open a map or explorer.
3. Keep connection, updating, and routine cleanup with the automation when the product promises them. Offer inspection or correction as an optional user action only when a demonstrated task needs it; presenting every inferred link for review transfers the product's work to the user.
4. State one proposed definition, its supporting evidence, and its untested usefulness. Compare a graph with search, a list, or a timeline on the same user task; node counts and technical sophistication do not establish user value.
5. When the user challenges a feature's purpose, return to the unmet user task and consider retaining, reducing, making optional, or removing the surface. Propose alerts, risk discovery, and other new capabilities only when their own need and implementation scope are established; adding speculative benefits can conceal the original purpose gap.
6. Distinguish the current approved direction from discussion hypotheses before proposing defaults or implementation. Keep the user's product-specific decision workflow central and use competitor references for reusable experience patterns.
7. Attribute confirmation to the user's explicit decision and preserve its scope: a feature's agreed meaning, its implementation proposal and the whole product purpose are separate decisions. Use supplied calls, meeting notes and transcripts to interpret intent, and distinguish speakers' proposals from the user's authorization, because persuasive source material can otherwise become an unapproved product commitment.
8. Bind a short proceed instruction to the immediately preceding agreed action and completion condition. If implementation was accepted, carry the result into executable delivery rather than silently stopping at another brief; if review was accepted, report the concrete review and remaining implementation boundary. Name whether work is actually running when asked, because a document or checklist does not establish ongoing execution.

## Completion Checklist

- The plan names goals, non-goals, assumptions, acceptance criteria, and verification shape.
- Draft recommendations, accepted decisions, and executor handoffs are separate states.
- Rejected options or unresolved tradeoffs are recorded before handoff.

## Recovery Notes

- If acceptance criteria or verification are missing, route back to clarification before handoff.
- If assumptions materially affect the plan, keep them visible and avoid treating the plan as accepted.

## Workflow Lane

- Current lane: **Intent -> plan** (`oh-my-hermes`, `meta-router`, `deep-interview`, `context`, `plan`, `ralplan`, `adversarial-consensus`, `codebase-onboarding`, `+8 more`) - clarify, plan, ship, or loop goals.
- If intent belongs to another lane, hand back to `oh-my-hermes` or name the adjacent workflow.
- Shared product, routing, compatibility, and evidence rules: `omh-routing/references/skill-common-rail.md`.

## Use When

Use when a product owner needs a problem frame, user/outcome definition, PRD, prioritization/roadmap options, dependencies, acceptance shape, and decision record before delivery planning.

    Strong routing signals: `product requirements document`, `PRD`, `roadmap prioritization`, `제품 요구사항 문서`, `제품 기획서`, `로드맵 우선순위`

## Catalog Metadata

Category: `planning`
Phase: `product-brief`
Hermes role: `planner`
Quality tier: `planning-gated`
Reasoning demand: `standard`

Quality bar:

- Name problem, user, metric, goals, non-goals, requirements, dependencies, risks, and acceptance shape.
- Preserve decision owner and downstream prerequisite boundaries.

Handoff policy:

Keep domain framing, clarification, source/evidence synthesis, draft outputs, and next-work routing in Hermes. A prepared brief, review, reply, or plan is not an external action, approval, filing, send, publish, data mutation, implementation, review, CI, or merge claim. Prepare a connector, file, coding, or human-review handoff only when the user explicitly accepts that next step; report it only from observed evidence. A PRD or roadmap is prepared planning, not stakeholder acceptance, Jira or Linear mutation, implementation, test evidence, delivery, or a market commitment.

Required inputs:

- product evidence
- problem and user
- goal and non-goals
- decision owner

Expert clarification questions:
- `product evidence`
  - English: What product evidence should anchor this brief?
  - Korean: 이 브리프의 근거가 될 제품 증거는 무엇인가요?

Expected outputs:

- problem, user, evidence, metric, goal, and non-goal brief
- PRD with requirements, open questions, risks, dependencies, and acceptance shape
- prioritization/roadmap options with tradeoffs and decision owner
- explicit downstream route to ralplan, strategy-brief, or ultrawork only when its prerequisite is satisfied

Artifact expectations:

- prepared product brief or PRD when a wrapper captures it

Safety rules:

- Separate product evidence, assumptions, prioritization options, and stakeholder acceptance.
- Do not claim roadmap-system mutation, implementation, test evidence, delivery, or market commitment.

## Runtime Evidence

Preferred harness for this skill: `planning`.

```sh
omh runtime record --skill product-brief --harness planning --status started
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

