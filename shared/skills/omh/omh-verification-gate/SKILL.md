---
name: omh-verification-gate
description: "[omh] Proof a change is done before merge: define and record build, lint, typecheck, test, security, docs, generated-output, and CI evidence before completion or merge."
---
# Verification Gate

This is a Hermes-native `verification-gate` workflow skill.

## Why This Exists

`verification-gate` gives OMH a deterministic evidence surface before done/merge claims, inspired by ECC-style gates but rebuilt around OMH's prepared-versus-observed contract.

## Do Not Use When

- The user asks for visual render QA; use `visual-qa`.
- The user asks for production release readiness beyond verification commands; use `production-audit`.
- The user wants a bug-first code review of a diff; use `code-review`.

## Examples

Good example:

- Prompt: verification-gate 이 PR 머지 전에 build/lint/test/docs/CI 증거를 정리해서 PASS 가능한지 봐줘.
- Expected behavior: Prepare verification_matrix/v1, record observed_check_results/v1, and issue PASS/HOLD/BLOCK with missing evidence.
- Why: The user asks for claim verification across command and CI evidence.

Bad example:

- Prompt: verification-gate 테스트 안 돌렸지만 준비됐다고 해줘.
- Expected behavior: Return HOLD/BLOCK and list missing or stale checks instead of claiming readiness.
- Why: A verification gate is useful only if planned checks and observed results stay separate.

## Completion Checklist

- The scenario, expected behavior, observed result, and pass/fail basis are named.
- Proposed fixes are separated from observed QA evidence.
- Missing or failed verification routes back to plan, fix, or a narrower test.

## Recovery Notes

- If the expected behavior is unclear, route back to plan before running adversarial checks.
- If verification fails, return to fix or research with the failed signal instead of advancing.

## Workflow Lane

- Current lane: **Coding handoff** (`idea-to-deploy`, `llm-app-dev`, `cto-loop`, `deploy-and-monitor`, `code-review`, `build-failure-triage`, `verification-gate`, `security-safety-review`, `+28 more`) - coding owners, handoffs, review, CI, and merge evidence.
- If intent belongs to another lane, hand back to `oh-my-hermes` or name the adjacent workflow.
- Shared product, routing, compatibility, and evidence rules: `omh-routing/references/skill-common-rail.md`.

## Use When

Use when Hermes must turn a change, PR, release, or claim into a concrete evidence checklist and PASS/HOLD/BLOCK verdict.

    Strong routing signals: `verification-gate`, `verification gate`, `quality gate`, `release gate`, `test gate`, `build lint test`, `lint typecheck tests`, `verify before merge`, `merge readiness gate`, `generated file`, `generated artifact`, `generated output`, `source of truth`, `regenerate instead of editing`, `検証ゲート`, `品質ゲート`, `マージ前の検証`, `リリース前チェック`, `검증 게이트`, `품질 게이트`, `테스트 게이트`, `머지 전 검증`, `빌드 린트 테스트`, `验证门禁`, `质量门禁`, `合并前验证`, `发布前检查`

## Catalog Metadata

Category: `verification`
Phase: `verification-gate`
Hermes role: `reviewer`
Quality tier: `verification-gated`
Reasoning demand: `standard`

Quality bar:

- Tie every completion claim to the smallest check that proves it, then broaden for shared surfaces.
- When a diff touches a declared generated path, name its source of truth and regeneration command before the edit rather than after a byte gate rejects it; a diff touching a generator and its output together is the correct shape, not a violation — load `references/generated-artifact-provenance.md` for the declaration and reporting rules.
- Record every field the `observed_check_results/v1` artifact expectation below names, for each observed result; a field left out is a gap in the record, not a shorter record.
- For native `omh_todo` checkpoints, load the todo-checklist closing recipe; `record` then `recall` this verification declaration. Stored declarations are not proof.
- When the change answers to a written spec, plan, or issue, load `references/requirement-coverage-map.md` and map requirement to task to evidence under stable ids before claiming coverage.
- Return PASS only when required checks pass and stale or missing evidence is resolved.
- Keep fixes, reruns, review, CI, and merge as separate observed states. Name each substituted boundary in connected tests, including storage, control-plane snapshots, host execution, and external targets; real TLS sockets with a fixture browser establish transport integration. For unattended-runtime claims, require exact installed service-entry execution and two consecutive user jobs without manual preparation, followed by host and deployed-product evidence for their respective gates.
- When resuming provider or worker QA, compare the latest saved receipts with current source before choosing the next gap; an older design statement can predate an existing integration or fix.
- Keep routine progress replies short and conversational. Put formal verdicts, matrices, and internal categories in durable evidence or a requested report; state the observed result and remaining check in chat.
- For bounded live-provider quality checks, paired answer evaluation, post-bind source replay, and worker admission-window diagnostics, follow `references/provider-worker-qa.md`.
- For answer-quality work, preserve the user's established benchmark and distinguish ordinary chat from explicitly requested formal judgment. Evaluate explanations, comparisons, recommendations and follow-up context in ordinary chat; test processor invocation separately from answer quality.
- Judge naturalness against the requested depth, format and conditions. Keep necessary explanation and useful clarification; inspect rendered evidence before attributing copied table/card fragments to the product. A prompt-transmission test proves policy delivery, while actual regenerated answers establish semantic improvement.
- Freeze hard-constraint acceptance before judging a conditional recommendation. Verify that the displayed title and body name the unmet condition and require actual compliance or explicit user approval before action; keep current feasibility separate from a preferred option under changed conditions.
- For launch work, anchor the gate to the production runtime and deployment path before adding QA cases. Mark each check as launch-critical or follow-up and give it a stop condition; repeated harness refinement can consume the delivery budget while production wiring remains missing. Record harness-supplied capabilities, identity evidence, and alternate conversation paths explicitly, then require the default product path to supply those dependencies before promoting the result.
- Include this user's final browser behavior and UI/UX review in the launch gate: question submission, progress, cancellation, failure/retry, cited-original opening, same-conversation follow-up, and refresh/reopen, plus mobile and keyboard behavior. Route rendered verification to `omh-visual-qa`, bind captures to the deployed revision, and rerun failed journeys after fixes; test/API totals alone leave the user-flow gate open.
- When a QA credential or transport recovery blocks a live check, keep that specific evidence gap open and assess the smallest production-aligned validation route. Preserve required authority, storage, and failure-cleanup checks while progressing implementation tasks that have independent evidence.

Handoff policy:

Hermes owns the gate contract and verdict narration. Running commands, CI, browser checks, external scanners, and code fixes require observed executor, wrapper, or operator evidence.

Required inputs:

- claim or change under verification
- expected behavior and risk surface
- available local commands and CI requirements
- fresh observed outputs or explicit not-run gaps

Expected outputs:

- verification_gate_plan/v1
- verification_matrix/v1
- generated_artifact_provenance/v1 when the change touches a path the repository declares generated
- observed_check_results/v1 when observed
- claim_verdict/v1
- rerun_or_blocker/v1
- not-evidence boundary

Artifact expectations:

- verification_matrix/v1 covering build, lint, typecheck, unit/integration/e2e tests, generated docs, static/security checks, diff hygiene, and CI/DCO when applicable
- observed_check_results/v1 with command (verbatim, not a description of it), source (this checkout, a CI job, or an operator report), exit status, summary (what the output said), scope (what that run covered, since a narrower run proves less), and freshness (when it ran, and whether the tree has moved since)
- claim_verdict/v1 with PASS, HOLD, or BLOCK and exact missing or failed checks
- generated_artifact_provenance/v1 with one row per touched generated path: the source of truth that produces it, the regeneration command, and the drift gate that catches it, or the single state `map_not_declared` when the repository declares no generated-artifact map

Safety rules:

- Do not treat a planned command, stale output, green local check, or prepared handoff as fresh verification evidence.
- Read generated paths from a map the repository declares; where none exists report `map_not_declared` and never infer one from filename patterns, directory names, or a generated-file header, because a false positive redirects correct work while the miss it prevents only costs a rerun.
- Do not collapse build, lint, tests, security, generated docs, review, CI, DCO, merge-readiness, or merge into one claim.
- Failed or unavailable checks must produce HOLD/BLOCK with a rerun or remediation path.
- A change touching an authentication, secrets/config, schema/migration, or payment/crypto path escalates to the thorough verification lane regardless of diff size.
- Refuse completion, do not merely report it, when the claim carries an unlinked TODO/FIXME/stub marker in changed code, a suppressed test with no linked reason, placeholder or self-referential evidence ('TBD', 'works as expected'), or a proof word ('fixed', 'verified', 'passing') with no observed evidence naming a command; each refusal names its category, the offending excerpt, and the remedy.
- Before a diff deletes a validation/refusal/sanitization/permission/allowlist check at a trust boundary, or a negative test named for it ('refuses', 'rejects', 'denies', 'blocks', 'invalid'), require a named adversarial or regression case proving the boundary still refuses what it should; a guard that only moves elsewhere in the same diff is not a deletion, but a deletion with no negative case behind it -- in the diff or named in evidence -- earns no completion claim.

## Virtualenv verification from a Python tool kernel

- When invoking a project's virtualenv interpreter from `execute_code`, check inherited `PYTHONPATH`, `PYTHONHOME`, and `PYTHONUSERBASE`; a Hermes kernel can inject its own site-packages into an otherwise correct virtualenv. Remove foreign Python paths and explicitly select the project's import path, interpreter, and approved scratch TMPDIR for the child process.
- Diagnose a suspected harness failure using the actual traceback/module paths and a clean-environment rerun. Do not mask warnings or change product dependencies merely to accommodate the tool kernel. Record the failed harness attempt separately from the verified product result.

## Mixed dirty-tree test evidence

- Invoke the test runner directly and preserve its own exit status before formatting output; a successful trailing pipeline command can conceal a test invocation failure. If a shell pipeline is essential, enable `pipefail` and capture the runner's status explicitly.
- Check runner option support with the project interpreter's help before adding plugin-specific flags. Use the execution tool's deadline for a run-level bound when no test-level timeout is configured; an unsupported flag can stop collection before any test executes. Record invocation failures separately, then rerun with supported options and require real collected-test results before reporting a pass.
- Capture full-suite JUnit XML and parse exact counts, failing test identities, and assertion locations before attributing a regression; an exit code alone cannot identify the failure surface.
- Preserve unrelated dirty authority and ordering code when a focused slice passes; report the failing full-suite gate and its observed failure class separately rather than fixing adjacent work or claiming a clean baseline.
- Record hashes as current shared-checkout bytes when changed modules also contain another owner's work; hashes prove the tested tree, not exclusive authorship.

## Runtime Evidence

Preferred harness for this skill: `verification-gate`.

```sh
omh runtime record --skill verification-gate --harness verification-gate --status started
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

