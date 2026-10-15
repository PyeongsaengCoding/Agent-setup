# Connected knowledge selection and discovery

Use when an assistant should accumulate reusable knowledge and answer with useful information whose location or existence the person may not know. Review generation and retrieval independently: an input can require existing knowledge while contributing no new graph item. Review the actual product first and keep architecture changes proposed until authorized.

## 1. Define the observable answer goal

Write examples where an unstated fact changes the answer: a deadline in mail, a constraint in a document, or a relevant balance/status in an approved database view. Include public-only questions and unrelated private facts. Judge discovery by useful answer changes and accurate evidence use, because retrieval alone can add irrelevant personalization.

Preserve explicit source exclusions and permissions. Treat a named source as a scope instruction; evaluate unknown-source questions separately so a source-name heuristic does not become the discovery policy.

## 2. Trace discovery separately from detailed reads

Follow the production entry through context preparation, tool definitions, model selection, search, original reading and final answer. Record whether initial discovery is automatic, model-selected, or restricted to selected attachments/snapshots.

Inspect the existing search adapter before proposing another classifier. Record lexical/vector search, embedding work, semantic reranking, returned fields, candidate and canonical limits, authorization filtering and refill behavior. Check whether candidate handles include enough text for relevance assessment; identifiers alone cannot establish semantic usefulness.

Separate structural omission risk from reproduced failure. A direct-answer branch proves discovery is optional; the actual model's source-miss rate requires controlled questions and known relevant sources.

## 3. Build a source coverage matrix

For each source family, trace ingestion and refresh -> index/catalog discovery -> detailed reader -> current authorization -> provider input and citation -> saved reopening.

Keep indexed connector data, selected saved DB results, and live structured DB reads in separate rows. A selected snapshot reaching the model proves that selection path. Inspect catalog discovery and the default query consumer before claiming automatic database coverage.

Reuse approved views, columns and parameterized filters for structured reads. Identify catalog candidates first and fetch rows needed by the question. Preserve row limits, observation time, partial results and immutable result references.

## 4. Compare discovery designs

Compare the current caller with a bounded initial-discovery candidate and, when requested, a candidate-aware classifier variant. Treat these as experimental choices; decide which utterances require discovery from evaluated product goals.

An initial-discovery candidate should reuse authorized indexes/catalogs, preserve the question and conversation referents, return compact evidence handles, and let the main model choose detailed reads. Keep empty results, partial coverage, provider failure and unavailable source classes distinct.

Schedule independent work concurrently after scope admission. If private information determines the public target, resolve it first. Apply privacy checks to the actual outbound query.

## 5. Qualify a classifier or judge

Trace the state it receives and what its result changes. Public-passages-only input supports content-type assessment; question relevance requires the question and context, while source existence requires observed evidence.

Define actionable relevance, supporting context, uncertainty and unrelated content. Preserve abstention, the main model's ability to request another read, and the existing path on timeout or invalid output. Assess uncertain and false-negative decisions before adopting pruning thresholds.

Determine whether the evaluator replaces a step or adds a sequential call. Compare against existing semantic reranking. Measure the complete question including wait and fallback, because a fast individual model can still lengthen the critical path.

Verify the approved external data boundary before sending private excerpts or schema details. Existing public-only integration does not establish private-data consent. Minimize inputs, preserve bindings and keep permission enforcement on the server.

## 6. Evaluate and deliver

Use the same corpus, exact questions and answer-affecting settings for variants. Include hidden useful facts, public-only and mixed-source questions, follow-up references, stale/conflicting values, denied sources, empty results and search failure.

Set expected useful sources independently. Measure discovery, actual answer use, unsupported claims, irrelevant personalization, first substantive answer, final completion, model/tool calls and cost. Separate simulated tests from real-model and deployed-flow evidence.

Adopt a classifier or discovery change when comparison supports its quality/latency tradeoff. Keep local and deployed behavior equivalent and compare runtime configuration during rollout. Retain authority and replay controls; candidates remain discovery hints until their original/value and current access are checked.

## 7. Select generated knowledge by information unit

Trace producer -> extraction -> assessment -> admission -> storage -> map/search publication -> consumer, then name the insertion point before editing. Specify existing-knowledge retrieval, new accumulation, judgment-record preservation/reuse, and ontology extension independently.

| Content | Selection target | Authority and scope |
| --- | --- | --- |
| Greeting, thanks, generic explanation/translation/calculation request | Source/conversation context | Preserve history and independently select useful assertions in mixed input |
| Explicit goal, preference, budget, deadline or change | User-condition candidate | Preserve speaker, purpose, applicability and change history |
| External fact or another person's statement | Attributed source candidate | Preserve provenance, polarity, modality, conditions and valid time |
| Open question, hypothetical fact or role-play | Execution context | Preserve hypothetical meaning and separate actual self-statements |
| AI interpretation or recommendation | Answer/judgment record | Link original evidence and establish actual user acceptance separately |
| Explicit actual choice or outcome | Choice/outcome candidate | Link the relevant judgment and occurrence time |
| Completed judgment | Versioned judgment record | Preserve original inputs and evaluate later reuse against current conditions |
| Meaning outside existing types/relations | Ontology-extension candidate | Apply the existing review/publication authority |
| Unclear speaker, meaning or required applicability | Held candidate | Preserve the reason and ask only consequential clarifications |

Prefer returning selection from an existing extraction or semantic-assessment call. Keep fidelity checks independently truthful for unselected content: a faithful quotation can still have low reference value. Require positive selection plus the existing kind, attribution, ontology, endpoint, time and access checks before downstream use. Keep selected user conditions on their proper owner-condition route; coercing them into eligible source claims loses their authority and scope.

Preserve source/history/search retention when withholding graph materialization. A post-extraction gate controls storage and consumption; candidate-production cost and omissions remain governed by the extractor. State that distinction when the requested design includes extraction-time selection.

## 8. Evolve selection and recovery contracts together

Search across implementation, tests and evaluation scripts for shared check/version symbols and fields such as `CHECKS`, `policy_version`, `evaluator_version`, `record_hash` and `format_recovery`. Include persisted validators and version-equality branches in the consumer list, because they control serving eligibility and paid retry authorization.

1. Bind the selection instructions and check set into the assessment request hash. Store its version and decision with the source revision and candidate identity, include the new metadata in the persisted integrity hash, and enforce eligibility again in publication/read paths.
2. Preserve genuinely historical records under their recorded read contract when migration is outside the approved scope. Test historical reads alongside removal/mutation of new metadata; conditional hash fields can preserve old records while protecting new ones.
3. Inspect what a schema-version constant authorizes before incrementing it. Keep format-only recovery fencing separate from semantic/evaluator versions when their responsibilities differ; a blanket bump can disable an approved recovery or authorize an extra paid attempt.
4. Regenerate evaluation packets and compare fingerprints after instruction/check changes. Keep prior fingerprint approval scoped to its original request and apply the applicable approval gate to the changed packet.
5. Run schema, recovery and completed-replay tests together. Assert call counts and unchanged completed records to preserve spend fencing as well as response shape.

## 9. Verify generation in increasing scope

1. Specify expected retention and forbidden promotions independently of the classifier. Cover mixed input, hypothetical versus real statements, other-party versus self statements, bounded versus permanent conditions, recommendation versus actual choice, repetition and explicit change.
2. Run a focused contract regression with `.venv/bin/python -m pytest -q -p no:cacheprovider tests/<selection_test>.py` and observe the intended failure before implementing enforcement.
3. Exercise the actual worker and persisted reader with protocol doubles and a controlled store. Check both retained and excluded relations through Workspace/map consumers, original source preservation, metadata integrity and endpoint eligibility.
4. Replay completed work with callbacks that fail if called. Assert zero additional extraction/assessment calls and unchanged stored decisions.
5. Run adjacent fidelity, identity, temporal, conflict, schema and recovery tests before broadening the suite. Evaluate real-model classifications against the content cases separately; protocol pass counts establish enforcement, while semantic recall and false promotions establish classification quality.
6. If a broad run exposes a suspected unrelated failure, rerun the exact failing cases with the changed boundary's pre-change implementation in an isolated process or worktree, preserving the user's dirty files. A targeted module loaded from `git show <base>:<module>` can establish a boundary-level control when its import graph permits it; report that limited control distinctly from a whole-repository baseline.
7. Fix attributable regressions and rerun their focused tests. Report broad-suite termination, later focused success, independently reproduced failures, real-provider evidence and user-flow QA as separate results. Keep configuration blockers as current evidence and leave unexecuted semantic or user-flow checks pending.
