# Recovering portfolio coordination state

Use when continuing multi-app work whose coordinator ran in other agent sessions or task-board workers.

## Session transcripts

Read the executor's session store (session list with id, title, source, message count, end time, and the per-session messages). Read the user turns plus the last 1-2 assistant texts of each session id with a short script. Skip tool rows to keep context small. Board-worker sessions hold the real progress.

## Board state

Locate the project's own board store; a root or default board can be empty, so an empty query there does not mean the project board is empty.

List tasks ordered by creation time (newest first) with status, completion time, worker PID, session id and last failure error. Read the body of the running and blocked cards. Confirm live workers with `ps`.

A task's result field is often empty. The worker's completion summary usually lives in the run record; the board's run listing may show a truncated version.

## Acting on the board

- Comment with the board's comment command, then show the task to confirm the event.
- Create a card: write the body to a scratch file and pass it as a body file, together with the app workspace, project, skill and maximum runtime.
- Before adding a new rule, check whether the relevant card bodies already contain it. Report which cards already had it and which ones you updated.
- A session that only answered questions needs nothing relayed once coordination moves to the current chat.

## Stopping dispatched work

A dispatcher typically re-queues reclaimed cards and spawns new workers for ready ones. To fully stop a card, do all three steps, then verify:

1. Reclaim the card with a reason: this releases the claim, but the card goes back to `ready`.
2. Block every affected ready card too, including children whose bodies carry the same wrong instruction.
3. `kill <worker_pid>`: reclaiming does not kill the worker process.

Confirm all of the following:

- `ps -p <pid>` shows the worker is gone.
- No board-worker process remains.
- The board shows the cards as `blocked`.
- Files the worker touched were checked: run `find <app> -newermt "<start time>"`, then grep for the specific change, because app folders may lack git.

After the user decides, edit the card body and only then unblock it.
