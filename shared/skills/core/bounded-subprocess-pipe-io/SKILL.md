---
name: bounded-subprocess-pipe-io
description: "Use when Popen pipe I/O must honour a deadline."
---

# Bounded subprocess pipe I/O

## Bug class
- `select(fd)` then `proc.stdout.read(n)` on a default (buffered) Popen stream blocks until `n` bytes or EOF: a peer that writes one byte and holds the pipe open ignores every deadline.
- `BufferedReader.read(4)` reads ahead into its Python buffer; the next `select` on the raw fd never fires -> spurious timeouts even for well-behaved peers.
- `stdin.write()+flush()` blocks when the pipe is full or the child stops reading; `close()` of a BufferedWriter flushes and can block too.
- Teardown that returns `exit_code None` after kill is claiming success it cannot prove.

## Pattern
1. `Popen(..., bufsize=0)`; never touch the stream objects for data.
2. `os.set_blocking(fd, False)`; loop: compute `left` from one window converted from the injected clock exactly once (never extended); `select(..., min(left, slice))`; `os.read(fd, min(remaining, 65536))` / `os.write(fd, chunk)`; `BlockingIOError` -> re-select; EINTR is auto-retried (PEP 475).
3. Empty read -> EOF; timeout -> typed error -> conservative failure (unknown after any byte was written; no retry).
4. close(): stdin EOF, wait/terminate/kill with bounded steps; if still unreaped raise (a counted cleanup error), record facts first, and let a repeat close() re-wait bounded instead of laundering the earlier failure.
5. A duplicated connected AF_UNIX descriptor shares the endpoint with its parent copy: closing only the duplicate does not deliver EOF while the parent retains its descriptor. Require a dedicated transferred channel and shutdown the endpoint before closing on cancellation/reset, then assert host cleanup and thread teardown.

## Honest tests (why fakes hid the bug)
- A fake Popen built with `os.fdopen(fd, buffering=0)` tests a raw path production never used. Build the fake's host-side streams with the `bufsize` the engine passed (default -1 = buffered, like real Popen) and assert production passes `bufsize=0` and gets `io.RawIOBase` streams.
- Held-peer behaviours block on a `threading.Event`; a `Harness.release()` in every `finally` sets it, joins with timeout (assert dead), closes fds.
- Run engine calls via `run_bounded(fn, seconds)` on a daemon thread; assert `not thread.is_alive()` so a regression fails instead of hanging the suite. Pre-fill the pipe with non-blocking `os.write` until `BlockingIOError` to simulate backpressure.
- Finish with a scratch probe on real `subprocess.Popen` python children (`os.write(1,b'x'); sleep`) to show the production path, not only the fake.
- For dedicated inherited private channels, validate descriptor kind/direction and reject stdio aliases before taking ownership. Qualify anonymous pipes on the actual OS: macOS reports zero links; Linux reports one link and `/proc/self/fd/<fd>` must resolve exactly to `pipe:[<fstat inode>]`. Keep named FIFOs, including unlinked ones, rejected. Permissions and link counts alone cannot establish anonymous pipe identity across platforms. Verify with actual inherited subprocess pipes on the target OS, not only socketpairs or local readback fixtures.
- A parent-side client that wraps `ssh ... <launcher>` can be tested with the test file re-executing itself as `--mock-host MODE` (argv = `[sys.executable, test_file, '--mock-host', mode]`, trailing launcher arg still appended): the mock asserts runbase present / key absent in argv, speaks the frame protocol on stdin/stdout, and writes the receipt to stderr. Build synthetic signed requests that satisfy the real contract (`request_hash = sha256(canonical({url, conditions}))`, public URL) or the real verifier rejects the fixture instead of the client.
- In a two-stage prepare/READY protocol, keep idle authority bounded by the original prepared/proof expiry, anchor request I/O once to real monotonic time, and let caller timeout and authenticated lease only shorten it. Recheck UTC lease inside the output loop and withhold signed results until cleanup is confirmed.
