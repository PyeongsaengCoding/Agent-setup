# Reference-led motion design for product shorts

## Procedure

1. Find actual examples and primary framework documentation. Confirm ambiguous framework or model names through retrieval before treating them as established products. Record the source and the specific technique observed; distinguish accessible examples from search snippets.
2. Break each reference into opening event, shot scale, cut rhythm, masking or reveal transition, typography timing, product detail reveal, and audio synchronization. Choose techniques that communicate the product or buying reason with the existing assets.
3. Write the advertising argument before the animation plan: buying situation → desire-led opening → exact product reveal → visible differentiator → usage payoff → purchase reason → CTA. Assign each scene one new persuasive fact or desire and the asset that supports it. Then choose composition changes, detail cuts, masks, typography, and audio cues to express that argument; pacing alone leaves the purchase reason underdeveloped.
   For a motion-graphics treatment, plan a large product entrance with controlled overshoot and settling, a feature-linked mask reveal, kinetic words timed to narration emphasis, graphic elements directing attention to product details, and a readable final hero/CTA. Select effects by the scene's selling purpose. Keep packaging pixels and proportions intact, and represent real product actions with evidence-backed assets. Treat these as design choices until the exported frames have been inspected.
   Use subtle zoom and layered parallax as supporting motion. Build visual events and composition changes around new information when the user requests a full advertising treatment.
4. Reconstruct the technique with original or authorized assets. Preserve product packaging, labels, proportions, and factual claims; keep the reference's pacing principle without copying its footage, script, or branding.
5. Reuse approved images, script, and voice for a cost-free remake when that scope is requested. Preserve the accepted version and export a separately named revision. Identify which tool actually authored and rendered it; citing an Opus workflow does not establish an Opus execution.
6. Build a seekable local composition, then lint, render a draft, inspect a contact sheet and transition frames, fix artifacts, and render the delivery file. Review color at representative full-size frames: check that decorative shapes support the product silhouette, appetite appeal, and readable feature labels. A translucent yellow circle on a dark blue background can read as dull olive; inspect the composited color rather than judging the source hex value alone. Reduce competing accents, test a clear product-derived background, and compare a restrained pointer against repeated highlight rings. For feature circles and labels, sample the entrance, stable hold, and exit, then watch that interval at normal speed in a phone-sized viewport. Hold the indicator through the corresponding spoken explanation; when labels or multiple details need extra reading time, simplify the scene or extend the hold before accelerating transitions. Use warm ivory indicators on brown food textures and inspect contrast against the actual image; retain yellow subtitle accents independently. Verify dimensions, codecs, duration, and full decoding. Compare the opening against the prior version to check that the requested change is visible.

## Technique selection

| Desired result | Technique | Main check |
|---|---|---|
| Gentle camera travel | Local pan and scale | Sharp labels and sufficient image resolution |
| Depth from a still | Background/product/foreground planes moving at different rates | Clean product edges and covered background holes |
| More energetic opening | Rapid scale changes, mask reveals, detail cuts, timed typography | New visual information rather than repetitive movement |
| New physical action or unseen product surfaces | Authorized footage or approved generation | Accurate product behavior and source rights |

## Working layer recipe

On macOS, a built-in Vision foreground mask can separate a product without downloading a large segmentation model. Crop to the subject first because a full-frame mask can merge the product and supporting table. Fill the exposed background with a binary hole mask before feathering the final edges; a feathered hole mask can leak product colors into the fill. Animate the planes with different displacement or scale and apply depth blur to foreground decoration while retaining a sharp product plane.

Use a paused, seekable animation timeline with locally stored dependencies for deterministic rendering. Inspect the product outline near the largest displacement and inspect frames on both sides of every transition. Keep optional speech-recognition tooling out of the workflow when the user has excluded that verification step.
