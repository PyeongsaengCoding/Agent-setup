---
name: desktop-app-provisioning
description: Install macOS desktop apps from the vendor installer and migrate Chrome/Edge browser profiles into another browser (such as Aside) without copying credential databases.
version: 1.0.0
license: MIT
platforms: [macos]
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
