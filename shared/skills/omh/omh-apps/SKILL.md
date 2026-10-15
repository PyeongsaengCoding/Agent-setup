---
name: omh-apps
description: "[omh] Email, Slack, or Jira action to perform: external app actions - email, Slack, Discord, Notion, Linear, Jira, CRM, and similar providers, scoped with auth, payload, confirmation, and result-evidence gates."
---
# Connector Operator

This is a Hermes-native `connector-operator` workflow skill.

## Why This Exists

`connector-operator` exists so Hermes users can ask for this workflow in chat and get a structured, checkable answer instead of an improvised one.

## Do Not Use When

- The request is already handled by a narrower explicit skill with stronger evidence.
- The user asks OMH to secretly run external platforms, connectors, schedulers, file exports, or runtime agents.
- The only safe answer is to ask for missing authority, credentials, target, or observed evidence first.

## Examples

Good example:

- Prompt: connector-operator draft an email to the customer and prepare a confirmation gate before sending.
- Expected behavior: Produce `prepare_connector_operator_card` with required context, wrapper actions, and not-evidence boundaries.
- Why: The prompt names a real workflow surface that Hermes can orchestrate without hiding execution.

Bad example:

- Prompt: connector-operator send the Jira update with hidden credentials and claim it was delivered.
- Expected behavior: Report the missing observed evidence or authority instead of claiming the external step happened.
- Why: Prepared OMH guidance is not platform, runtime, connector, file, memory, or delivery evidence.

## Customer follow-up email drafting
1. When the user references a sent message, verify the requested mailbox account and read the exact subject/thread before writing. Use the observed latest relevant message to establish recipient titles, To/CC, prior commitments and what the customer has already been told. Scope page reads to the target conversation to avoid loading unrelated mail.
2. Redact login passwords, tokens and unrelated signature/contact details before printing or saving mail snapshots. Retain only the addressing and message context needed for the draft; an earlier email can contain credentials inside ordinary body text.
3. Reconcile the proposed update with current work evidence. Separate existing production features, new local development, local acceptance/storage tests, actual source comparisons and remaining implementation. Attribute a sample's match count to that sample and field scope; do not turn it into a company-wide accuracy or full-compatibility claim.
4. For generated test inputs, explain that they came from the independent submitted input and were compared with separate evidence. Identify material fields still absent from the test input; successful workflow tests do not cover those fields.
5. Recommend replying in the existing thread with its observed recipients as the default, while preserving any recipient changes the user explicitly requests. Draft only the new information, concrete verified results and next work or decisions; avoid repeating earlier access instructions or adding delivery dates and completion promises without support.
6. For a request to suggest wording without sending, present one ready-to-use draft in chat. Keep mailbox state unchanged unless the user explicitly requests saving an Outlook/provider draft. Sending remains a separate authorized action. Avoid automatically attaching internal logs, raw customer evidence or engineering reports; prepare a customer-facing summary when an attachment is requested.
7. Apply the relevant humanizer to the draft, keep Korean business wording direct and reader-focused, and give only a short framing recommendation outside the email. State accurately whether a provider draft was saved or the text exists only in chat.

## Completion Checklist

- Provider, target object, allowed action, payload summary, authority, confirmation policy, and stop condition are explicit.
- Credentials, missing connector setup, external writes, sends, ticket mutations, calendar invites, CRM updates, and webhook delivery are gated or marked missing.
- Message ids, ticket ids, provider responses, delivery receipts, and API effects are reported only from observed connector evidence.

## Recovery Notes

- If the connector, credentials, or permission is missing, route to toolbelt-readiness before preparing action success claims.
- If the request is only chat thread delivery policy for Discord, Slack, or Telegram, route to gateway-intent-card instead.
- If the external app action would create, send, invite, mutate, or delete provider state, require an explicit confirmation gate.

## Workflow Lane

- Current lane: **Automation and status** (`achievements`, `workspace-audit`, `production-audit`, `live-incident-response`, `automation-blueprint`, `github-event-ops`, `github-issue-intake`, `buzz`, `+39 more`) - schedules, status, health, and ops review.
- If intent belongs to another lane, hand back to `oh-my-hermes` or name the adjacent workflow.
- Shared product, routing, compatibility, and evidence rules: `omh-routing/references/skill-common-rail.md`.

## Use When

Use when Hermes should prepare or supervise a provider-backed external app action without claiming connector availability, credentials, API mutation, delivery, or success.

    Strong routing signals: `connector-operator`, `connector operator`, `external app action`, `external connector action`, `saas action`, `api action`, `send email`, `email customer`, `gmail draft`, `gmail send`, `create linear ticket`, `create linear issue`, `linear ticket`, `linear issue`, `update linear`, `jira ticket`, `jira issue`, `create jira issue`, `open jira ticket`, `create jira`, `notion page`, `update notion`, `crm update`, `salesforce update`, `hubspot update`, `create calendar event`, `calendar invite`, `google calendar`, `send slack dm`, `slack dm`, `discord dm`, `post to discord`, `post to slack`, `discord post`, `slack post`, `connector action`, `linear ticket`, `이메일 보내`, `이메일 발송`, `메일 보내`, `gmail 초안`, `linear 티켓`, `linear 이슈`, `jira 티켓`, `jira 이슈`, `notion 페이지`, `노션 페이지`, `캘린더 초대`, `외부 앱`, `외부 커넥터`, `커넥터 액션`

## Catalog Metadata

Category: `connector`
Phase: `connector-task`
Hermes role: `guide`
Quality tier: `workflow-surface-gated`
Reasoning demand: `standard`

Quality bar:

- Name the user-facing workflow objective, required context, next action, and stop condition.
- Separate prepared guidance from observed platform, runtime, connector, file, memory, or delivery evidence.
- Expose missing tools, credentials, targets, or observations as user-visible gaps.

Handoff policy:

Keep this as Hermes-facing orchestration guidance first. Prepare executor, connector, gateway, or host-runtime handoff only when the user accepts that next step and observed evidence can be recorded.

Required inputs:

- user request
- target context
- delivery or status expectation
- known missing evidence

Expected outputs:

- connector_task_card/v1
- connector_scope/v1
- connector_auth_boundary/v1
- connector_confirmation_gate/v1 when mutating or sending
- connector_result_manifest/v1 when observed
- next action
- prepared-vs-observed boundary

Artifact expectations:

- connector_task_card/v1 metadata-only wrapper card when prepared
- connector_scope/v1 with provider, target object, allowed action, payload summary, and stop condition
- connector_auth_boundary/v1 separating missing connector, missing credentials, user-supplied authority, and credential-use prohibition
- connector_confirmation_gate/v1 for sending, ticket mutation, external write, webhook delivery, CRM/database update, or irreversible provider action
- connector_result_manifest/v1 only when provider response, message id, ticket id, API transcript, or delivery receipt is observed

Safety rules:

- A connector operator card is not connector availability, credential validation, API call, message send, ticket creation, ticket update, database/CRM mutation, external write, webhook delivery, or provider success evidence unless observed connector-result evidence records it.
- Do not claim connector, gateway, runtime, file generation, memory mutation, or host automation evidence from prepared guidance.

## Runtime Evidence

Preferred harness for this skill: `connector-operator`.

```sh
omh runtime record --skill connector-operator --harness connector-operator --status started
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

