---
name: desktop-app-provisioning
description: Install macOS apps from vendor installers and migrate or clean up browser profiles (e.g. Aside) safely.
---

# Desktop app provisioning

Use for authorized app installation and browser-profile migration. Read official installation instructions and verify the OS and architecture first.

1. Check existing apps and profiles. Do not replace an app, close a user's browser or change its default without permission.
2. Use the vendor's installer and verify its signature before running it.
3. Map every requested source profile to a separate destination profile. Use the destination browser's supported import UI rather than copying credential databases.
4. Let the user handle login, Keychain and OS permission prompts. Never ask for secrets in chat.
5. Verify installed, imported, authenticated and agent-connected states separately. Keep a per-profile completion list.
6. Preserve the active app, keyboard target and cursor. Stop when an operation requires foreground access the user has not allowed.

Use the destination browser's supported import UI for profile migration. Page interaction after migration uses the aside-browser skill (`aside repl`). For native app GUI steps, use the executor's computer-control tool when it is available; otherwise list the exact clicks for the user.

## Aside profile rename and removal

- Identify the retained and removed profiles by stable profile directory and account IDs before acting, because display names can collide. Preserve the retained profile's login and owned tabs, then verify the same browser account can still attach to those tabs.
- Remove an authorized duplicate through the native profile picker. Read the confirmation's full profile name before pressing Delete, then verify that exact entry disappeared from `profile.info_cache` in Aside's `Local State`. Check filesystem deletion separately when it is an acceptance criterion.
- Rename the retained profile through its picker card's rename text field (Korean UI: `프로필 이름 바꾸기`). Accessibility `set_value` can report unverified while the change succeeded; re-capture and check the card label and `Local State` before another input.
- The Profiles menu's add-profile entry creates a profile. Use the profile-management entry for cleanup; if this workflow created a temporary profile, remove that exact empty profile and verify the original profiles remain.
- Re-capture when an accessibility tree is temporarily empty. Use the computer-control tool's element index when available and follow the fresh capture's coordinate space for pixel input. Get permission before bringing an app to the foreground.
