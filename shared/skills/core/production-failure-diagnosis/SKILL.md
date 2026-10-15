---
name: production-failure-diagnosis
description: "Use when tracing causes of saved production failures."
---

# Production Failure Diagnosis

Companion to `diagnosing-bugs` for existing failed conversations, jobs and result URLs. Keep its hypothesis and observed-evidence discipline; inspect the original saved execution before commissioning another run.

## Procedure

1. Inspect the exact reported result under the approved application identity and workspace. Recover the original question and its requested conditions, then retrieve its execution identity and owner-authorized diagnostics through read-only requests. When the user asks why a tool was skipped, compare those conditions with the tool's recorded use and deployed admission contract before explaining the choice.
2. Form hypotheses covering remote service failure, local timeout/admission, and validation/storage failure. Read original provider-attempt receipts to distinguish these boundaries.
3. Reconstruct the actual timeline and effective limits: attempt start/end, remaining budget, reserved tail, admitted timeout and outbound timeout. Inspect the policy that applied them. Use a calculation tool for derived values and account for overlapping stages.
4. Trace the original exception through catch/fallback, returned outcome, terminal-state writer, API projection and UI. Establish why processing stopped and why its failure was hidden as separate causal chains.
5. Compare relevant source with deployed or committed revision; separate dirty local changes from historical execution evidence.
6. Lead the explanation with the confirmed mechanism and the few measurements that prove it. State the precise deeper unknown when evidence ends there. Continue available authorized read-only investigation before settling for a generic timeout explanation.
7. Prepare changes or a fresh execution within the user's requested scope, carrying the observed failure into regression coverage. When the user asks to add the reported question to scenarios, recover its exact saved prompt and follow-up conditions, inspect the current registry before choosing a unique identifier, and register purpose-level acceptance criteria with the diagnosis reference. Preserve the original benchmark set in place, append user-requested extensions in its existing extension collection, and keep historical failure and future rerun status separate.

## Standing rules

- Treat a question about why a result failed as a request for the causal mechanism; an HTTP code, stage name or fallback message alone leaves that request open.
- Prefer durable evidence before paid or state-changing replay, because another run can change timing, incur cost and obscure the original failure.
- Read original exception metadata before attributing a 504 to the remote server, because adapters can assign that code to local timeouts.
- Inspect effective outbound timeout, because earlier work and reserved finalization time can sharply reduce the final operation's allowed duration.
- Distinguish saved-content preservation from question completion, because a fallback can enter the normal completion writer and clear the user-visible error.
- Keep source-quality defects separate from the stopping cause, because source contamination and transport failure can coexist.
- Explain visible foreign-language fragments by tracing their origin and delivery path: distinguish acquired source prose, access-challenge text and model output, because a source-only fallback can expose untranslated material that never became an answer.
- Verify browser capability through the deployed target allowlist, supported condition fields, tool exposure and saved call records, because an enabled browser transport alone leaves the requested user flow unproven. State the missing capability and the observed execution separately.
- Separate model-selected calls, durable tool bookkeeping and actual external dispatch. Inspect dependency-deferred results and their start/transport evidence before treating a completed row or an attempted flag as executed research; a locally deferred call can otherwise hide the missing acquisition step.
- Trace the actual data dependency behind public-search admission. Compare a reformulated query with the authorized public scope rather than requiring literal inclusion in the user's question, because translation and normal search expansion can falsely defer independent research. Preserve privacy preparation and genuine dependencies on newly discovered private targets or citation IDs.
- Check earlier user instructions before treating a timeout or call limit as approved policy; distinguish the user's decision, an implementation record and the current code, because a restriction left in one path can look like a later user request.
- For an approved timeout-policy change, trace execution admission, model loops, stream delivery, recovery and child operations together, because a second deadline can recreate the removed cutoff. Preserve independently scoped per-operation limits and authority checks.
- Keep the answer anchored to the user's immediate question and confirmed mechanism; after a correction, retrieve the missing causal evidence rather than repeat the status summary.
- Load `references/provider-timeouts-and-terminal-state.md` for timing, terminal-state analysis, capability checks, timeout-policy changes and read-only Azure receipt retrieval.
