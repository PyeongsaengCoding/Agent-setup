# Browser profile migration preflight and completion gates

This is an inventory and verification procedure, not a claim that a particular browser importer has completed migration. Use the destination's current supported import flow; do not copy encrypted cookie or password stores as an improvised workaround.

## 1. Inventory before creating destination profiles

For Chromium-family browsers, parse the existing `Local State` JSON and inspect `profile.info_cache`. Record the directory key, display name, and whether that directory exists. Read only metadata needed for inventory; do not emit account tokens or decrypt credential stores.

Common macOS roots:

- Chrome: `~/Library/Application Support/Google/Chrome`
- Edge: `~/Library/Application Support/Microsoft Edge`

Treat these as discovery candidates, not universal paths. Persist inventory and progress in task-local JSON with fields such as `source_browser`, `source_directory`, `source_name`, `destination_profile`, `status`, and `evidence`. Count, deduplicate, and reconcile in code.

## 2. Compare with the live importer

Capture the destination app's settings and import picker. A locally existing source profile is not proof that the destination supports importing it on this platform. Inspect the full saved accessibility tree when the displayed list is truncated; a missing option in a clipped screenshot is not evidence of absent support.

Prefer a source-to-destination mapping that preserves account isolation. Inspect existing destination profiles before adding another, because the user may already have imported or authenticated one. Preserve both source data and destination sessions; do not merge by default.

## 3. Respect the keychain boundary

An importer may display a permission explanation containing an example keychain dialog. Distinguish that image from an actual macOS authentication prompt. When authorization is needed, tell the user the exact next visible action and let them authenticate directly. Record `awaiting_user_authorization`, not `imported`.

If safely inspecting other source support while waiting would require dismissing or restarting an in-flight import, preserve the pending operation instead. Do not force unsupported imports through raw profile-file copies or browser security changes.

## 4. Verify each identity independently

After user authorization, re-capture the current state before acting. Confirm the importer finished, the destination profile identity matches its source, and the expected imported data appears. Check requested login continuity only on authorized sites, without exposing cookies or credentials.

Report separate counts for detected, attempted, completed, and verified profiles. List unsupported or still-pending sources explicitly. Creating a destination profile or clicking Import does not satisfy migration completion, and imported cookies do not prove every account remains logged in.
