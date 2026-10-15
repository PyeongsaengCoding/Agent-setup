# REPL recipes and site notes

Observed behaviour of the Aside REPL engine and of common sites. Re-check against the installed `aside guide repl` when a recipe fails.

## REPL environment

- Only `console.log` output comes back; a bare `return` value is dropped. Top-level `const`/`let` names persist across calls in the same session, so reuse `var` or fresh names. `snapshot()` returns an object with `tree` and `refs`; check its shape, then print it or slice `tree`.
- `require()` is unavailable. `fs` (promise API) and `path` are globals; `crypto` is undefined in REPL scope, so hash inside `page.evaluate` with `window.crypto.subtle`. `location` is also undefined in REPL scope; read URLs inside `page.evaluate`.
- `fs` is sandboxed to the session directory: reading a host scratch path fails with `Path escapes Project and session roots`. The session directory is printed at REPL start (host copy under `~/.aside/u/<account>/sessions/<id>/artifacts/`). Create `./artifacts` with `fs.mkdir('./artifacts', {recursive: true})`, copy inputs there, and read `./artifacts/<file>`.
- `openTab()` returns the page object directly. There is no `waitForTimeout`; use `await new Promise(r => setTimeout(r, ms))`. `openTab(url, {background: true})` can print "set it active" while `listBrowserTabs()` still shows the user's tab as active; trust the readback. `page.setViewportSize` is unavailable on real tabs; use the iframe harness in [responsive viewport QA](responsive-viewport-qa.md).
- Save captures with `page.screenshot({path: './artifacts/x.png'})`. A 1440x900 CSS viewport yields a 2880x1800 PNG.
- `page.reload()` and `goto()` discard in-page wrappers such as a patched `window.fetch`; install wrappers after load and trigger the read through a UI click.
- `page.goBack()` can time out on a pushState SPA route even though the route changed; use `page.evaluate(() => history.back())` and poll visible route controls.
- Korean text written as `\u` escapes is easy to mis-encode. Load exact prompts from a JSON file, fill, read the input value back, and compare it (and its hash) with the source before submitting.
- When a facade is disposed, run `listBrowserTabs()` in the verified profile and `attachBrowserTab(observedTargetId)` if the exact tab is still live. Persist each accepted submission's target id, result URL and receipt in the session artifacts, and read an existing receipt before submitting again.

## Locators and controls

- When an accessible-name locator fails for a visible control, take a fresh snapshot and click its ref with `page.locator('e…').click()`, or use a verified CSS attribute locator from the inspected DOM. Snapshot roles such as `main` or `dialog` can come from implicit semantic elements or custom components.
- A chained `>> text=…` locator can resolve to a text node (`Node is not an Element`). Find the element in `page.evaluate`, tag it with a data attribute, then click `page.locator('[data-x="1"]')`. If an SPA ignores the first click, `scrollIntoView` plus `page.mouse.click` at the measured centre is a reliable retry.
- React Aria checkboxes with a visually hidden native input can ignore locator clicks, DOM clicks and Space. A raw `page.mouse.click(x, y)` at the bounding-rectangle centre toggles them; read `.checked` back.
- A toggle click can report `Checkbox click did not change checked state` while the service saves asynchronously. Read a fresh snapshot before retrying and re-open the settings URL to verify.
- A native select's accessible name can come from a wrapping label. Inspect the element or match an observed option value before setting it. Fill React inputs with the native value setter (`Object.getOwnPropertyDescriptor(proto, 'value').set`) and dispatch `input`/`change`.
- `offsetParent !== null` misses `position:fixed` dialogs. Test visibility with `getBoundingClientRect()`, viewport intersection, computed visibility and `aria-hidden` ancestors. SPAs can keep a previous route's hidden `<main>`; scope reads to the visible element with a nonzero rectangle.
- A scoped `[role="dialog"]` snapshot can read only the first of nested dialogs. Inspect all dialog labels or take a full snapshot before concluding a popup failed. When a modal leaves only the page title in the snapshot, read `document.body.innerText` (credential-safe) and take a screenshot.
- Collapsed accordion content can be in the DOM yet absent from `innerText`; read `document.body.textContent` around the heading.
- React can replace a button after submission while keeping its label, dropping injected attributes. Re-find and re-tag the current element before retrying.
- Use a native locator click for buttons that open popups, because popups can require a user gesture. Bind the popup to a named page variable after verifying its URL.

## Reading pages when extraction fails

Open the official page in an owned background tab, read `document.body.innerText`, slice around a keyword, then `closeTab(page)`. Fetch observed image URLs and inspect pixels when visual details matter.

## Files, downloads and uploads

- Register `page.waitForEvent('download')` before the download action, await `download.path()`, and verify the file. Check the destination after `saveAs()`; if missing, copy the verified download and compare hashes instead of downloading again.
- Upload files must be inside the REPL session directory. Copy the approved file to `./artifacts`, register `page.waitForEvent('filechooser')`, click the observed upload button, then `chooser.setFiles('./artifacts/name.png')`. Verify the application's rendered filenames and counts; a handler can clear the native input while keeping files in state. Confirm previous selections are cleared before the next batch.

## Authenticated local and API checks

- Separate loopback health, SDK account/token readiness and browser request delivery. For approved API reads, read the token inside one `page.evaluate`, return only allowlisted fields, and null the variable afterwards.
- Origin-scoped SDK sessions belong to the exact origin. Serve the current app on the existing origin when it is free; another port creates another origin without the session. Verify account and workspace admission before submitting.
- Send the workspace identifier the app actually stores (read it from local storage keys), because a shortened form can be rejected.
- For refresh checks of saved answers, poll for the expected visible answer count on the exact route, then compare the settled DOM with the pre-refresh text and stored content.
- Record job completion, stored projection state and detail-page rendering as separate verdicts; a UI can show a completed result while the status endpoint still reports pending.
- After a deploy, a page loaded earlier can hit stale route chunks and fall back to a full reload. Re-test on a freshly loaded page of the served revision before calling it an app defect.

## Read-only latency diagnosis

1. Reproduce the exact approved read-only action. Use `performance.getEntriesByType('resource')` to separate route loading from the detail request.
2. Install a page-local fetch wrapper and a `MutationObserver` after navigation and before the click. Record request start, header arrival, completed resource duration and the first visible nonempty content node separately with `performance.now()`.
3. Scope the content selector to the visible dialog, because hidden retained DOM can produce false first-render times. Return paths, status and timing only.
4. Compare a first open, a repeat open and one adjacent item. Before reopening, confirm the previous dialog has closed and re-arm the observer.
5. Report client-observed latency. Attribute backend stages only with runtime traces or verified deployed-source parity. Preserve permission, revocation and audience checks in any optimization proposal.
6. Lead with the dominant measured interval and the strongest supported explanation, then the remaining attribution gap. Clear auth-bearing variables, disconnect observers and close owned tabs.

## Chat products (latency and baselines)

- Verify reply selectors against the current DOM before timing. Locate the visible `main` and composer by nonzero rectangles, because hidden earlier roots can remain. Start a page-local clock right before submit, keep the first answer mutation, and record completion when the observed stop control disappears.
- Before using a temporary chat as an unpersonalized baseline, inspect its personalization control; temporary chats can keep memories and custom instructions. Report the visible mode label separately from an unexposed model identifier.

## Email-based onboarding

- If account helper lists are empty, verify the intended mailbox in the browser and use the observed `/u/{n}/` index. A Gmail redirect to `AddMailService` means the Google identity has no Gmail mailbox; check the organization's mail provider in the same profile.
- Check the recipient of each verification email before opening its link. Parse links in the REPL, validate hostname and path, navigate, then clear message/link variables.
- After a magic-link navigation, wait only while the observed page is loading and avoid resubmitting a pending signup. Verify email forwarding, email verification, service onboarding and organization membership separately.

## Microsoft Loop reports

1. Confirm workspace, parent page and child title in the live navigation tree before reading; repeated date titles need their parent.
2. Read scoped `main`/canvas text first. Save `data:image/png;base64,...` images into `./artifacts` with `Buffer.from(src.split(',')[1], 'base64')` and inspect them as images instead of printing base64.
3. Paste approved reports as HTML and plain text through the real macOS pasteboard and `keyboard.press('Meta+V')`; synthetic paste events can be ignored. Preserve and restore the previous pasteboard only while its change count still belongs to the task.
4. For whole-body replacement, click the canvas, press `Meta+A` twice and confirm the title is outside the selection. Avoid multi-line `keyboard.type`. Convert emoji checkboxes into native `[role="checkbox"]` items through the editor and read `aria-checked` back.
5. Compare headings, tasks and table cells with the approved payload, reload, and compare again.

## Notion records

Read the Aside built-in Notion skill and select the exact workspace first. After `collection.addRow()`, invalidate the client cache and read back title, date and body. Repair missing titles through `set('properties.title', [[title]])`; for property IDs with punctuation use the page's own date picker. Avoid retry loops on HTTP 400 and leave the collection schema unchanged. Notion virtualizes off-screen property cells; scroll the table into view before clicking and verify persistence after refresh.

## Cloudflare DNS records

- The record Type field is a custom `button[role=combobox]`; open it and choose from `[role=option]`. Name/target inputs render after the type is selected.
- Locate the Proxy status checkbox by its row text ("Proxied" / "DNS only").
- For CNAME-validated custom domains, set DNS only before the platform validates the domain, and enable the proxy after the platform reports the hostname ready.
