# BardBox Service Operations Standard

This standard defines reusable operations for long-running BardBox services.
Project-specific sensor, alert, and analysis logic does not belong here.

## Classification

| Component | Classification |
| --- | --- |
| Config synchronization | REQUIRED where `app_config` is used |
| Process restart and application watchdog | REQUIRED for FastAPI/Uvicorn web services |
| Read-only Data API | REQUIRED WHEN APPLICABLE |
| Verified archive backup and retention | REQUIRED WHEN local historical data is retained and pruned |
| Tailscale remote administration | RECOMMENDED for Raspberry Pi deployments |
| Central BardBox Tools / MCP boundary | REQUIRED architectural boundary |

## Safe configuration synchronization

A repository using deployment-local `app_config` must keep a sanitized,
version-controlled example/schema file and an ignored live runtime file. The
exact paths may vary by project and should ultimately be declared in
`bardbox.toml` rather than hard-coded into shared tooling.

Typical monitor paths are:

```text
raspi/config/app_config.example.json
raspi/config/app_config.json
```

The example file must contain no real credentials. The live runtime file may
contain deployment-specific values and secrets and must be ignored by Git.

The **canonical config comparison and synchronization logic belongs in shared
BardBox tooling**, not in separately maintained copies in every project repo.
During migration, repositories may retain thin compatibility wrappers such as
`scripts/sync_app_config.py`, but those wrappers should call the shared
implementation rather than fork its behavior.

A deployment is not complete until the config check reports no deployable keys
or node fields missing from the live configuration.

The required behavior is:

- validate both example and live JSON;
- recursively add fields introduced by the example;
- preserve deployment values and unknown local fields;
- match configured nodes by UID rather than list order;
- do not create new enabled deployments merely because an example contains a
  new node;
- create a timestamped backup before modifying live config;
- atomically replace the live file;
- never copy real secrets into Git;
- provide a dry-run/check mode that never modifies the live configuration;
- exit non-zero when reviewed config migration is still required.

Example-only and production-only node UIDs are deliberately not merged. A
local-only production node may therefore need an explicit, reviewed migration
when the example introduces a new node field. Production/site-specific values
must never be overwritten automatically.

The required deployment sequence is:

```text
git pull
bardbox config check
review/apply required config additions
confirm config check passes
restart service
health check
smoke test
```

Until the shared CLI command is available in a migrated repository, its
compatibility wrapper may provide the equivalent check/write workflow.

## Two independent availability layers

Every long-running FastAPI/Uvicorn service must recover from both process exits
and application hangs.

### Layer 1: process recovery

The systemd service must include:

```ini
Restart=always
RestartSec=5
```

This covers crashes, unexpected exits, and operating-system termination.

### Layer 2: application health watchdog

The application must expose an inexpensive, side-effect-free endpoint:

```text
GET /health
200 {"status":"ok"}
```

It must not access devices, databases, filesystems, or networks. An independent
oneshot service and timer must call the loopback endpoint once per minute,
count consecutive failures, and restart the application service after three
failures. A success resets the count. Project-specific alerts and sensor checks
must not be embedded in this watchdog. This layer is required because a live
Uvicorn process can remain running while the application no longer responds.

A project may also expose a richer application-health endpoint, but it must be
kept separate from the inexpensive liveness endpoint when it performs device,
filesystem, network, freshness, or other operational checks.

## Read-only historical Data API

Services with a clean historical readings root expose:

```text
GET /api/data/files
GET /api/data/files/{path:path}
```

The canonical CESH Air router is the current reference. Requirements:

- a dedicated token in ignored runtime config; empty or missing means 503;
- Bearer authentication with constant-time comparison before filesystem work;
- recursive `.csv` and `.csv.gz` listing using relative paths only;
- canonical-path confinement; reject traversal, outside symlinks, directories,
  missing files, absolute paths, and other file types;
- `FileResponse` streaming, with `.csv.gz` bytes unchanged;
- `Cache-Control: no-store` on successful listing and downloads;
- read-only behavior: no write, shell, admin, config, service, or analysis API.

This standard is conditional. Do not point it at a tree that mixes readings
with alert, audit, credential, or configuration data. RKC's `data/logs/` is an
example of a mixed tree that must not be exposed wholesale.

## Verified backup and safe retention

When local historical readings are archived and later pruned, the backup job
must be separate from application code and configured by deployment-local
settings. The reusable lifecycle is:

```text
discover new/changed stable file
  -> non-destructive archive copy
  -> batch verification
  -> atomically record exact path + size + mtime
  -> delete after retention only on an exact manifest match
```

Runs must use a non-blocking lock. Upload or verification failure leaves the
manifest unchanged and deletes nothing. Actively growing daily CSV files may be
copied but must not be verified or retained until stable; compressed files are
closed candidates. Changed files invalidate older manifest versions. Archive
destinations use copy semantics, never sync semantics that delete remote
history. Services without local historical archives do not need this component.

A project may create a stable local snapshot before network transfer when its
writer needs that separation, but the remote archive still must obey the
non-destructive copy and verified-retention invariants above.

Generic backup verification/manifest logic should move toward a shared BardBox
implementation or a manifest-driven deployment component rather than diverging
shell implementations in each repo. Project-specific source locking or snapshot
hooks may remain local when necessary.

## Data access and BardBox Tools / MCP boundary

```text
Monitoring service
    -> authenticated read-only Data API
    -> bardbox-tools deterministic core
       -> bardbox CLI / bardbox-query
       -> MCP tools / AI clients
       -> downstream analysis/reporting
```

Monitoring service repositories expose generic operational data and
project-specific behavior. Shared dataset discovery, retrieval/packaging,
config comparison, Git inspection, project audits, protocol checks, and similar
cross-repository engineering functions belong in `bardbox-tools` rather than
being duplicated in monitoring servers.

CLI and MCP interfaces should call the same deterministic implementation.
MCP should remain a narrow interface over approved BardBox capabilities rather
than providing arbitrary shell execution.

The repository/distribution is `bardbox-tools`. Transitional executable names
such as `bardbox-mcp` or `bardbox-query` may remain for compatibility while the
package migration is completed, but new documentation and architecture should
not treat the former `bardbox-mcp` repository/path as the canonical home.

## Source of truth and production drift

Git is the source of truth for code, deployment assets, schemas, and templates.
Production hosts may contain ignored deployment config, credentials, data,
logs, manifests, caches, and other runtime state, but they should not accumulate
unique source code or unique infrastructure behavior.

Production inspection should therefore be read-only by default. Drift should be
reported, fixed in Git, reviewed, and then deployed through the repository
workflow rather than repaired first by editing the production host.

As `bardbox-tools` matures, deployment/service inspection should be
manifest-driven so a contributor or AI agent can obtain a deterministic report
without needing unrestricted production shell access.
