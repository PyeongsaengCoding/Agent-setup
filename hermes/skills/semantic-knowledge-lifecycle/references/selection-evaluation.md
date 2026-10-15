# Selection evaluation and attribution

Prepare expected results before invoking the model. Use naturally worded inputs and independently inspect the returned proposal, stored record and consumer input. Keep a fixed regression set plus paraphrases from topics outside the initial examples; the set is a quality instrument, not the feature's supported-topic list.

## Coverage matrix

| Input variation | Check |
|---|---|
| Greeting or generic explanation request | Preserve history; avoid inventing persistent identity/preference. |
| Explanation plus a real self-statement | Retain the useful information unit while still answering the explanation request. |
| Short real goal, preference or constraint | Judge utility from meaning/context, not length or a fixed phrase. |
| Open purchase/choice question | Preserve question context; do not infer ownership, purchase or confirmed preference. |
| Hypothetical identity plus a separate real condition | Keep the hypothetical within execution context and evaluate the real condition independently. |
| Third-party or quoted preference | Preserve attribution; do not attach it to the current owner. |
| Assistant recommendation without user acceptance | Keep answer/decision history; do not infer an actual choice. |
| Explicit user choice/outcome | Retain actual-choice provenance and connect the relevant prior decision without rewriting that decision. |
| Same condition restated | Reuse/reconfirm the matching item under the existing identity/revision contract. |
| Explicit changed value | Update the identified purpose/subject; retain change history and historical decision inputs. |
| Same deleted quotation with changed key/purpose | Suppress automatic recreation independently of model-generated identity, including within a mixed request. |
| Owner correction of selected memory | Replace stale selection authority with the owner-edit contract; verify ordinary answer use and explicit scoped-condition use separately. |
| Future-effective replacement | Serve the prior value before start, the replacement from inclusive start to exclusive end, and retain the original cutoff of frozen decisions. |
| Pending replacement restated as a new add | Keep the pending value in selection context and reject collisions again at the canonical write boundary. |
| Purpose-limited or relative-time statement | Preserve the limitation, keep unsupported absolute time unknown and verify later use honors scope. |
| Ambiguous referent or purpose | Hold the persistent update or ask only the necessary clarification; preserve conversational context. |
| Existing-source question | Retrieve the existing source independently of retention and avoid duplicate generation. |
| Schema/type expression gap | Keep a bounded extension candidate; do not silently publish a shared meaning or relabel content to obtain admission. |
| Completed-work replay | Verify unchanged stored result and zero additional extraction/assessment calls. |

## Diagnose the failing layer

For each case, record whether information was proposed, semantically selected, structurally accepted, canonically committed, retrievable and actually supplied to the next answer/decision. A missing item can originate in an upstream receipt gate, model extraction, semantic fidelity, use policy, write fencing or the reader; change the failing layer rather than weakening all admission checks.

When a statement is selected but held, inspect its exact content kind and failed dimensions. A missing absolute date and an omitted purpose qualifier require different remedies. Check whether the representation is an entity mention, source-reference statement, attributed claim or owner condition before interpreting a temporal-fidelity failure.

## Evidence reuse

Store input, prompt/contract version, configured deployment, provider-reported identity, source/request binding, returned evaluation dimensions and downstream observations together. Reuse a captured evaluation only under its original matching binding. Record any unavailable dimension rather than supplying a plausible default. A prompt or schema change invalidates reuse for the changed request; unaffected cases remain reusable when their contracts and inputs are unchanged.

Treat a real-model run with synthetic sources and an in-memory store as evidence for that model/pipeline boundary. Authenticated account rendering, next-answer use and production configuration require their own observations; gather them in the same coordinated QA process rather than rerunning a duplicate complete test suite for each reporting label.
