---
name: omh-report-package
description: "[omh] Periodic report for executives: weekly/monthly reports, executive briefs, PPT-ready outlines, and upload packages."
---
# Report Package

This is a Hermes-native `report-package` workflow skill.

## Executive development-status workflow

Apply these steps to product development reports since a previous update, including company Loop pages. Write for an executive who needs to know what the product now does, what changed, which actual requests succeeded and what remains.

1. **Read the baseline first.** Read the previous published report and cutoff, then inventory subsequent reports, execution records, scenario registries and relevant Git history across product repositories. Include adoption decisions and newly built capabilities; a recent-session summary can omit major changes.
2. **Map claims to evidence.** For each item identify previous behavior, actual change, reason, concrete scenario result and verification boundary. Inspect code or diffs when the cause is unclear. Separate code deployment from a successful user request. Never generalize one failed example into the whole product's previous behavior.
3. **Group by product capability.** Merge browser interaction, execution environment, condition entry, result reading, citations, evidence saving/reopening and associated search corrections into one feature section. Group mail lookup, background analysis and mail-status changes together. Keep a new provider identifiable. Preserve exhaustive changes within these groups rather than numbering every helper or correction separately.
4. **Lead with the capability.** Explain what became possible before supporting implementation. Distinguish a newly built browser interaction feature from improved text collection. Preserve the actual trigger: describe automatic tool selection when the product decides the lookup method. Explain model-selected actions, server-enforced access rules and supervisor-enforced termination separately when relevant.
5. **Write concrete Korean.** Use exact product feature names: write `판단` for a feature named `판단`. Replace '흐름 보완', '지원 범위', '조건과 근거 범위' and '직접 답하는 수정' with an actual action, missing input, changed screen or named unfinished test. Explain the question and reason before mentioning dates or values. Use '메일 내용' or '문서 내용'; reserve '원문' for a meaningful contrast with summaries or fresh retrieval. Explain technical limits in ordinary language, such as mail analysis using all concurrent AI calls and leaving questions waiting.
6. **Describe data fixes precisely.** Distinguish changing lookup order from introducing a new kind of mail content. Distinguish sending the updated evidence list from introducing evidence delivery for the first time. For display cleanup, name the phrase deleted or sentence replacement removed. Keep cause and change short and factual.
7. **Use measured scenario comparisons.** Retrieve both executions when before/after times are requested. Keep server time, first-answer time, completed-screen observation and substage duration separate. Include slower and failed outcomes. Omit unmeasured cases and empty metric columns from executive prose while retaining consequential failures and concrete follow-up checks. Follow [scenario timing comparison](references/scenario-timing-comparison.md).
8. **Rewrite and deliver the artifact.** Apply corrections across related sections, summaries and tables. Preserve evidence links; validate figures programmatically. Present the finished rewrite rather than another outline or promise. A turn ending does not continue drafting unless a real background task was started.

Before delivery, test each section: What feature changed? What can the user do? Which real question demonstrated it? What remains to make that question work? Merge repeated subitems and remove sentences needing a second explanation.

## Why This Exists

`report-package` exists to make reporting a first-class operations surface: Hermes can produce clean report and slide outlines while keeping approvals, delivery, and binary deck export as separate evidence.

## Do Not Use When

- The user needs SLO, incident, or error-budget review; use `reliability-review`.
- The user asks for a live `.pptx` deck file rather than a PPT-ready outline.
- The request is meeting minutes, scrum history, or action-item tracking.

## Examples

Good example:

- Prompt: report-package 월간 리더십 보고서 PPT outline 만들어줘.
- Expected behavior: Prepare a report package with sections, assumptions, missing inputs, and Markdown/JSON outline scope.
- Why: The request is packaging known information for reporting, not reliability validation or code work.

Bad example:

- Prompt: report-package prove our SLO passed and close the incident.
- Expected behavior: Route to `reliability-review` and require metric or incident evidence.
- Why: Report packaging cannot satisfy reliability closure evidence.

## Completion Checklist

- The reporting window, inputs, audience, narrative, and evidence gaps are named.
- Draft report, generated package, approval, and delivery are separate states.
- The next action says whether to gather evidence, generate, revise, approve, or deliver.

## Recovery Notes

- If a material product result lacks evidence, name the concrete unfinished verification. Omit unmeasured metrics and incidental observation gaps from executive prose; retain them in evidence records. Never fabricate a report claim.
- If delivery or attachment is unavailable, keep the report package prepared_not_observed.

## Workflow Lane

- Current lane: **Materials and visual summaries** (`design-orchestration`, `apple-design`, `design-quality-gate`, `award-bar-score`, `frontend`, `accessibility-audit`, `visual-qa`, `content-operator`, `+6 more`) - web, accessibility, visual QA, files, and packages.
- If intent belongs to another lane, hand back to `oh-my-hermes` or name the adjacent workflow.
- Shared product, routing, compatibility, and evidence rules: `omh-routing/references/skill-common-rail.md`.

## Use When

Use when Hermes should turn supplied inputs into a report, executive brief, PPT-ready outline, or upload package without claiming presentation delivery.

    Strong routing signals: `report-package`, `report package`, `weekly report`, `monthly report`, `executive report`, `exec brief`, `leadership deck`, `status package`, `ppt outline`, `presentation outline`, `slide outline`, `upload package`, `PPT`, `보고서 패키지`, `주간 보고서`, `월간 보고서`, `경영진 보고`, `리더십 보고`, `피피티`, `슬라이드`, `발표자료`, `업로드 패키지`

## Catalog Metadata

Category: `reporting`
Phase: `package-outline`
Hermes role: `operator`
Quality tier: `report-gated`
Reasoning demand: `standard`

Quality bar:

- Name audience, reporting period, sections, supplied facts, assumptions, and missing data.
- Keep report packaging independent from reliability review unless explicitly requested.
- Export only Markdown/JSON outlines unless a separate presentation tool produces a binary deck.

Handoff policy:

Keep report narrative, sectioning, and Markdown/JSON outline packaging in Hermes; do not require reliability evidence unless the user asks for a reliability review.

Required inputs:

- audience
- reporting period or scope
- supplied facts
- missing data or assumptions

Expected outputs:

- report package
- PPT-ready Markdown or JSON outline
- assumptions and missing-input list
- optional achievements badge section sourced from `omh achievements export --format md` when requested

Artifact expectations:

- operation_artifact/v1 report-package artifact when a wrapper or CLI records it

Safety rules:

- Do not claim source review completion from a prepared report package.
- Do not claim stakeholder approval or presentation delivery without observed evidence.
- Do not couple report packages to SLO, incident, or error-budget evidence by default.

## Runtime Evidence

Preferred harness for this skill: `report-package`.

```sh
omh runtime record --skill report-package --harness report-package --status started
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

