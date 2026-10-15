# Authenticated batches

## Azure account and credential recipe

Use the project's approved authentication directory and explicit subscription:

```sh
AZURE_CONFIG_DIR=<project-auth-directory> az account show --subscription <subscription-id> --query '{user:user.name,subscription:name,id:id,tenant:tenantId}' -o json
```

Compare user, subscription, and tenant with the approved boundary before credential retrieval. Locate the exact Function App and resource group through read-only inventory.

Capture the required setting privately with a subprocess:

```sh
AZURE_CONFIG_DIR=<project-auth-directory> az functionapp config appsettings list --name <function-app> --resource-group <resource-group> --subscription <subscription-id> --query "[?name=='<admin-token-setting>'].value | [0]" -o json
```

Parse the output into process memory and use the header defined by the authentication implementation. Keep credentials out of command arguments, tool output, files, and reports. Print status and sanitized verification fields only.

## Contract and batch assertions

Read the route dispatcher for registry, default-config, and public runtime paths. Read handlers for response envelopes before parsing nested fields. Trace target override precedence; a collection-refresh flag and background execution gate can control different behavior.

Match full composite identity, such as `appKey:platform:channel`, rather than appKey alone. Retain registry and default-config snapshots before writes. After writes, assert:

- Every requested identity occurs exactly once.
- Names, package identifiers, platform, channel, runtime mode, supported flags, and activation values match.
- Omitted attribution remains empty/default after server normalization.
- Public runtime responses return the expected identity and effective SDK/background activation.
- Background URL presence and generated-link count are checked independently.
- Effective scheduling interval is recorded.
- Global defaults and unrelated rows match pre-write snapshots.

When POSTs are limited to one per target, record completed responses as they arrive and read back ambiguous targets before recovery. Preserve successful writes while resolving failures.

## Completion boundary

Lead with verified count and effective activation. Explain target-specific overrides needed for activation. State generated-link availability separately from default URL readiness. Claim Android scheduling and background execution only after observing a device run; otherwise label that stage unverified.
