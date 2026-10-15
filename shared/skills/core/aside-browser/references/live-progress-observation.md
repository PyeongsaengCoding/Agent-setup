# Live progress observation

Use this procedure when reproducing a reference product's streaming, research, synchronization, or long-running task experience.

## Capture the interaction

1. Resolve the service-specific profile and account, then attach the observed tab or open an owned background tab. For a chat probe, use an owned temporary conversation where available and record the visible mode and personalization setting.
2. Read a fresh snapshot and locate the visible conversation root, input, current-status control, and completion control. Confirm nonzero bounding rectangles and the accepted prompt; retained hidden roots can produce an empty or unrelated recording.
3. Before submission, install an in-page `MutationObserver` on the inspected conversation root. Record `performance.now()` with changed rendered text, deduplicate consecutive identical states, and bound the retained record count and text size. Keep the observer page-local so short REPL calls can retrieve states without missing brief transitions.
4. Submit once through the observed control. Read a fresh snapshot to prove acceptance and execution. Inspect recorded transitions with short calls while performing other required inspection; use an explicit observation deadline and the actual completion control as the stopping condition.
5. Capture distinct current activities: generic waiting, contextual task intent, query or target changes, tool outcomes, and final-answer onset. Preserve exact observed text in private evidence when needed. Distinguish interface text from the product's unexposed model, transport, and internal reasoning mechanism.
6. After completion, expand the observed duration/history control. Read its summary and actual counts, then inspect screenshots of the expanded and collapsed arrangements. Check whether task history remains separate from the final answer.
7. Disconnect the observer, clear retained page variables, close only owned tabs, and verify the remaining inventory.

## Turn observations into implementation criteria

- Derive contextual activities from current public task intent and actual tool events; preserve generic waiting states as truthful fallbacks when detail is unavailable.
- Keep intent, attempt, verified result, and failure distinct. A planned search does not prove that a site was read, and a changing label does not prove work completed.
- Define the completed summary, elapsed time, expandable history, and reload behavior alongside live updates. Test at least two different user goals so a fixed sequence cannot satisfy the acceptance criteria accidentally.
- Protect private source text and detailed reasoning. Expose only the approved public task summary and safe tool metadata.

## Read saved failure diagnostics without flooding context

1. Open the exact reported record and verify the application's own identity and workspace.
2. Inspect response keys first, then return an allowlist of status, quality/completeness, failure boundary, timing, and safe source metadata. Keep a full response in page memory only when necessary and clear it after extraction.
3. Compare transport failure, stored execution status, answer completeness, and rendered content separately; a partial-answer fallback can make a failed generation look completed in storage.
4. Treat successful direct Aside form actions and the application's own browser-worker support as separate observations. Check the worker's supported target and input contract before attributing a failure to the external site.

## UI regression acceptance

- Number actionable feedback items and keep those numbers through investigation, clarification and QA results so the person can refer back to individual items.
- When the person names an existing interface as the reference, inspect its actual interaction first and compare coordinate order, marker meaning, visibility toggles and shared controls with the changed view. Include the existing control flow of an extended feature in that comparison.
- For AI progress interfaces, specify question-specific public task intent and actual execution updates, including changing query or target, outcome, completed duration and expandable saved history. Test different questions and reload behaviour, because a fixed sequence can look active while missing contextual behaviour.
- For a chat-triggered long operation, test consent, continuation of existing data, actual progress, required-data readiness, failure and return to the original question as one flow, including repeated clicks, navigation, reload, cancellation and access changes.
