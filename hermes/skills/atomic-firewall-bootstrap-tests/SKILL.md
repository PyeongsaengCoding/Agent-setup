---
name: atomic-firewall-bootstrap-tests
description: "Use when fixing firewall bootstrap scripts offline."
---

# Offline firewall bootstrap security tests

## When to Use

Use for scoped security fixes to root bootstrap scripts when tests must stay offline and cloud/kernel acceptance belongs to a separate operator.

## Procedure

- Write a behavioral RED before implementation: execute the real shell entry point with isolated command stubs and root-only paths under the configured scratch directory; capture nonzero output for the missing control.
- Model live firewall state independently from staged restore state. Apply staged operations to a copy and publish only at a single table COMMIT; inject parse/commit failures and inspect every live event. A modeled transaction validates shell ordering, while real kernel atomicity remains a deployment check.
- Preserve legacy deny rules and unrelated shared-chain rules during migration. Insert a deny-only guard and switch only a dedicated owned chain through iptables-restore --noflush. Never flush a live shared chain.
- Use one bounded advisory lock across all bootstrap mutations, including stop, pull and identity invalidation. Test concurrent rebuilds, concurrent starts and lock failure before any credential or runtime mutation; close the inherited descriptor for the transient workload launcher.
- Check goto versus jump return semantics when preserved legacy deny rules remain below the owned hook. Collect DROP snapshots from the active owned chain; legacy shared-chain counters can remain unchanged after migration.
- Validate the operator-supplied own public IPv4 with ipaddress; runtime metadata unreachability must never remove its DROP. Keep metadata discovery in the trusted installation phase.
- Enumerate owned firewall policy with a successful full-table read before staging cleanup; treat a failed listing as an error, because confusing inspection failure with chain absence can retain an old exception while claiming a disabled snapshot.
- Place a retained deny-only hook for an optional host proxy before baseline ESTABLISHED/RELATED acceptance after disable or client-IP change. Rebuild its owned chain atomically and enumerate exact owned-comment hooks for duplicate cleanup; separately terminate the proxy process to close host sockets and reverse-direction buffers.
- Distinguish detached endpoint responses from unreachable or unexpected HTTP codes. A control-plane fallback requires externally produced, fresh root-owned 0600 evidence with no symlink/hardlink, bounded reads and exact VM, image, bootstrap and pull-session bindings. Bootstrap must never manufacture the operator assertion.
- Emulate privileged file ownership only in the isolated test harness on an unprivileged host; retain real file mode, link and freshness checks, and leave production validation unchanged.
- Require positive endpoint controls or matching active-chain DROP deltas before reporting blocked traffic. Legacy connection failures remain reachability observations with an INCONCLUSIVE verdict.
- Verify absolute executable handling for transient-unit post-stop container removal, preserve sandbox flags and embedded policy hashes, then run the complete scoped pytest suite, Ruff and bash syntax checks.
- Hand off actual Linux restore/flock/systemd behavior, endpoint liveness, cleanup and host-path DNS validation separately; offline shell tests provide no cloud acceptance or permission to enable public traffic.
