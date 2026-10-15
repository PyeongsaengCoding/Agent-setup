---
name: mobile-app-portfolio-delivery
description: "Use when building a mobile app portfolio through beta."
---

# Mobile app portfolio delivery

Use alongside a mobile-release workflow for store preparation and a backend/API design workflow for service contracts. This companion owns the user's cross-app sequencing and persistence decisions; those skills supply detailed release and API methods.

## When to Use

Apply when coordinating several mobile apps, advancing a pilot into closed testing, or deciding app-specific persistence alongside a shared operational service. For one app's store mechanics, use the mobile-release workflow; for endpoint and schema detail, use the backend/API design workflow.

## 1. Establish the next deliverable

Read the active task, latest app checkpoint and relevant project instructions. Recover platform, package, signing and test evidence before asking questions.

Choose the requested milestone: local test package, closed-test availability, qualifying tester participation, production-access application or public release. Define its completion evidence and external-write scope separately.

For this user's portfolio, finish the pilot through the requested testing-preparation milestone, then advance the remaining apps sequentially. Track qualifying waiting periods and production-only decisions independently so other app development can proceed. Keep privacy, security and policy requirements attached to every testing track where they apply.

When the user changes the milestone, update the active task and downstream handoff/dependencies before dispatch. Reuse existing checks and reassess blockers against the new deliverable, because a stale public-release dependency can stall unrelated implementation.

## 2. Decide persistence per app

Inspect actual features and reference behavior. Record the data owner, storage location and recovery expectations for user records, identity, backup/restore, device replacement, synchronization, sharing and remotely maintained content.

Include an app-specific backend and datastore whenever required product behavior needs server persistence. Preserve the required capability when choosing infrastructure, and pass the backend decision into the implementation handoff.

Choose local-only storage when it meets the intended use. Explain verified behavior after app-data deletion, reinstall and device replacement. Distinguish local persistence, OS-managed backup and implemented cloud restore.

Keep shared affiliate/runtime configuration and operational reporting within their established service boundary. Give each product backend its own data ownership, authentication, authorization and deletion/retention lifecycle. Verify isolation across apps and across users.

Separate the logical app-specific service/data boundary from physical resource allocation. Inspect hosting quotas, expected use, account and cost permissions before selecting cloud resources; verify free-tier limits before using them for sizing.

## 2a. Apply the runtime SDK as instructed

The user's instruction for every app is to apply the shared runtime SDK as designed, including its background execution, affiliate runs and the permissions it requires (overlay, battery-optimization exemption). Keep the banner and the support opt-in flow too.

- Never disable SDK workers or remove SDK permissions on your own initiative or on a predecessor coordinator's or reviewer's recommendation. Policy-risk findings are information for the user, not changes to make.
- When a prior session left a pending "approval" question, rewrite it before relaying it. State concretely what would be removed or disabled and what SDK function is lost, and present keeping the SDK unchanged as the default. A question that hides what gets stripped makes the user's "approve" mean something they never chose.
- Scope worker file searches to the card workspace or known build-output paths (e.g. `android/app/build/outputs/bundle`). A whole-disk `find /` from a background worker touches iCloud Drive and other apps' data, and macOS then shows permission prompts to the user.
- Never copy a decision made for one app into other apps' card bodies until the user confirms it portfolio-wide. One wrong line in a template card spreads to every later app.

## 3. Deliver and verify one app

Follow the project's reference research, design and build sequence. Preserve evidence for each named app and stage; report the inspected subset explicitly.

For server-backed features, exercise an app-originated write and exact-target readback, unauthorized access, persistence after restart and required restore/sync behavior. Classify local implementation, deployed service and real client flow separately.

For local-only features, exercise save/reopen, storage failure, deletion and relevant lifecycle behavior. Reuse unchanged passing test/build evidence and add checks for changed behavior.

Keep findings and test results in the app's project records. Keep current product decisions in its existing documentation; this skill stores reusable procedure.

## 4. Prepare the store milestone

Use the mobile-release workflow and its applicable method. Check current official rules and actual Console account eligibility separately.

When the Console requests business registration, inspect the exact notice and page. Classify developer verification, country-specific disclosure, paid-app/in-app-purchase settings and payment-profile requirements before proposing a change. Preserve the approved free/affiliate-funded model while checking applicable conditions.

Track signed artifact, store submission, test availability, tester opt-in continuity, elapsed qualifying time and production approval as separate states. Start a qualifying-time claim from observed participation evidence.

Ask for the minimum missing decision blocking the current milestone. Carry independent work forward within its approved scope.

### Public identity, contact and policy hosting

Before proposing a store contact, policy URL or developer name, apply the user's settled identity rules:

- Change only the Play **developer display name** away from the owner's personal brand to a neutral studio name — the user's GitHub ties that name to their identity. Offer ~5 candidates with one recommendation; the name also becomes the policy's operator field, so policy publication waits on it.
- Keep the owned `<owned-domain>` and existing `com.<owner>.*` package IDs. Do not propose new domains (no purchases until revenue) or package-ID migrations. Package IDs are visible in Play URLs and immutable after first upload — inventory upload state per app before suggesting any ID change.
- One developer account groups all apps under one name regardless of naming; say so plainly instead of implying a name hides app-to-app links. Separate accounts cost $25 each plus separate verification and 14-day tests.
- Contact: per-app addresses `<app>@<owned-domain>` via Cloudflare Email Routing into ONE inbox (recipient address shows the source app). Never make the user manage one mailbox per app; never copy another app's contact automatically.
- Policy pages must live on a real public website, never a GitHub file/repo page. Host per-app at `<app>.<owned-domain>/privacy` on Cloudflare Pages (DNS already on Cloudflare). Inventory existing apps' policy URLs (search store-listing metadata, `dig`/`curl` the hosts) and migrate any that are repo-only.
- State documented free-tier caps instead of "unlimited": Cloudflare Pages Free 100 projects/account; Email Routing free, 200 rules/domain; Azure Static Web Apps Free only 10 apps/subscription (too few for per-app policy sites).
- After the hosted policy page is live and the store listing points to it, delete the repo-only policy copies (drafts, `PRIVACY.md`). Confirm the deletion list with the user first. Deleting before publishing leaves the store URL with nothing to link to.
- If the user worries Cloudflare is slow from Korea, measure instead of arguing. `curl -s https://<host>/cdn-cgi/trace` shows the serving colo; free-plan Korean traffic often lands on a US/JP colo. Compare TTFB with `curl -w` against an Azure-hosted page; for a static policy page the gap was a few hundred ms.
- Keep the policy URL and operator/contact in one app config constant so the value changes in one place once decided.
- Turn each approved Console scope into an explicit card statement (e.g. create app → closed track allowed, tester invites only after a roster is supplied). When an identity decision changes mid-run, comment the correction on running cards and hold/release signed-AAB generation accordingly.

## 5. Handoff and report

Pass the next app a short handoff: accepted features, persistence decision, implementation boundaries, reusable checks, remaining inputs and milestone acceptance criteria.

When asked to relay a correction to another session, verify receipt at that exact destination before claiming delivery. Describe a saved task comment as a task update and a destination acknowledgement as received communication; these establish different states.

When a standing persistence or boundary rule arrives mid-run, add it verbatim as a comment on the running card and require it in every later card body; workers read card bodies and comments, so relaying it to an idle chat session changes nothing.

When the user cannot see a coordinator or worker session and asks to continue in the current chat, take over coordination here: recover prior session messages and the project board's live task states first (recipe: `references/coordinator-session-recovery.md`), then report per-app state from the board rather than from the last chat summary.

When the user rejects something already dispatched, first stop every affected running card and hold the queued ones (recipe in `references/coordinator-session-recovery.md`). Then report exactly what already changed, and in which artifact, versus what was stopped before it changed. Ask before reverting. Never resume or re-dispatch until the user answers.

Lead progress reports with the milestone actually reached, the app covered and the next blocker or running task. Keep architecture proposals separate from implementation already observed.
