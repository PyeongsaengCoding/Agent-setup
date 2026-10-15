---
name: semantic-knowledge-lifecycle
description: "Use when building LLM memory and scoped knowledge retention."
---

# Semantic knowledge lifecycle

## When to Use

Use when implementing or reviewing automatic LLM memory, knowledge-graph intake, scope-aware personal conditions or their downstream answer/decision use. Skip this skill for a one-shot answer or summary that creates no persistent knowledge.

Use this alongside the executor's general LLM application workflow for automatic memory, knowledge-graph intake and scope-aware personal conditions. It adds the semantic selection and end-to-end verification procedure; the application owns storage and authority. Load `tdd` before code changes.

## Standing requirements

- Let the LLM interpret information units in conversation/source context and return structured proposals; let code enforce provenance, permitted storage/use, current scope and consistency. Treat example topics as evaluation coverage, because a phrase/topic whitelist silently narrows a general-purpose feature.
- Separate retrieval of existing knowledge, retention of new information, reuse of historical decisions and ontology extension. A request with no new durable information can still require retrieval.
- Explain applicability through subject, purpose, duration and replacement relationship. State what the LLM proposes, what the server validates and what actually works today; vague promises to preserve wording hide missing scope or consumer integration.
- Develop and perform actual-model user-flow QA in one coordinated process, with independent review alongside it. Reuse unchanged evidence and rerun affected cases after a fix; reserve post-deployment checks for deployed code/configuration identity and operational differences.

## Procedure

1. **Trace the real lifecycle.** Locate the saved user/source event, candidate extraction, recording/job receipt, canonical write and next-answer/decision readers. Check for an upstream regex gate or whole-message equality filter before adding a broad classifier, because an unreachable selector preserves the original restriction. Give each parallel worker disjoint file ownership.
2. **Separate the semantic decisions.** Give the model enough relevant context to identify actual speaker, real assertion versus hypothesis, reusable value, content kind, purpose/scope and explicit change. Select useful information within a mixed request without storing the entire request. Keep current conversational constraints available even while persistent work is pending.
3. **Construct a scoped proposal.** Retain exact evidence and source identity; preserve relative-time and purpose qualifiers without inventing absolute timestamps. Distinguish a document-reference statement from an asserted current fact. Resolve proposed update targets against current records for the matching subject/purpose and expected revision.
4. **Use the existing canonical path.** Reuse owner conditions, source assertions and decision records according to their meaning. Put model-backed persistent work through an existing durable recording/job path where available, record the attempt before provider I/O and preserve replay fences. Apply deletion fingerprints to each selected quotation before deriving its model-generated identity, because a changed key or purpose can bypass an ID-only tombstone check. Transition owner edits to the existing owner-edit authority and clear stale selection and effective-value metadata, because inherited model proof describes the earlier statement. Prefer adding selection to existing extraction/assessment calls over adding an obligatory extra call to every request. Keep shared command parsing in a lower-level policy module used by both recording and suppression; a suppression callback into recording creates an import cycle.
5. **Prove consumption, not just storage.** Exercise selection → validated write → reread → next answer/decision input, including consumer revalidation. Preserve original decision cutoffs and inputs when current conditions change. For future-effective updates, retain the earlier source-bound value until the replacement starts and resolve the same value in answer and decision readers under the current canonical ID/revision. Keep pending replacements visible to selection while withholding them from current-use readers, because hiding them from selection permits duplicate re-adds. Keep source references restricted to their evidence role and preserve existing explicit-selection-only boundaries for confirmed owner conditions.
6. **Run integrated QA efficiently.** Start with behavioral RED and affected boundary tests, then use the application's normal model-settings loader for bounded actual-model runs. Include positive retention and false-promotion cases, drain all work windows, preserve results before process exit and assert no new calls on terminal replay. Report protocol tests, real-model synthetic runs, authenticated user flows and deployed differences by their observed coverage, while reusing stable evidence across these steps.

## Verification pitfalls

- Do not broaden content-kind admission to raise relation counts; a faithful selected candidate may still require a different canonical path or restricted use.
- Count missed useful information as well as false promotion, because successful worker status and admission totals cannot establish semantic quality.
- Require scoped replacement evidence before changing a persistent item; ambiguous purpose must not overwrite a global preference or an unrelated condition.
- Test deletion followed by the same quotation with changed semantic key and purpose inside a mixed request; require suppression independently of the new identity.
- Test ordinary owner correction through the next-answer reader and scoped correction through explicit decision compilation; require each to use its intended owner-authority path.
- Test future replacements before, exactly at, and after their boundaries, including frozen-input and release-fence revalidation; a correct initial read can still leave a stale value usable during generation.
- Compare underlying assertions with their qualifications, not their display labels alone. A relative or purpose-limited source reference can retain exact qualifications with an unknown absolute interval; a stronger permanent/current assertion needs support for that stronger meaning.
- Keep hypothetical identities and assistant recommendations separate from confirmed user facts and actual choices. Preserve the user's own stated constraints within a mixed or example-containing message.

For the reusable evaluation matrix and result attribution, read `references/selection-evaluation.md`. For deletion, owner correction, scheduled values and atomic replay probes, read `references/lifecycle-invariants.md`.
