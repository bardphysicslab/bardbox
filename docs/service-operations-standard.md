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
| Central MCP/query boundary | REQUIRED architectural boundary |

## Safe configuration synchronization

`raspi/config/app_config.example.json` is the sanitized, version-controlled
schema and default-value template. It must contain no real credentials.
`raspi/config/app_config.json` contains local or production values, including
secrets, and must be ignored by Git.

Every repository using this pattern must carry the canonical
`scripts/sync_app_config.py`. A deployment is not complete until the
synchronizer reports both:

```text
Added keys: none
Added node fields: none
```

After every `git pull`, and before restarting the service, run the explicit
deployment check:

```bash
python3 scripts/sync_app_config.py --check
```

The check is a dry run: it must never modify the ignored live configuration.
It exits non-zero when deployable keys or fields on matching node UIDs are
missing. Operators must review those additions and apply them when appropriate:

```bash
python3 scripts/sync_app_config.py --write
```

The synchronizer validates both JSON inputs, recursively adds fields introduced
by the example, preserves deployment values and unknown local fields, matches
configured nodes by UID without creating new enabled deployments, creates a
timestamped backup, and atomically replaces the live file. Example files use
empty secret placeholders; real secrets are never copied into Git.

Example-only and production-only node UIDs are deliberately not merged. A
local-only production node may therefore need an explicit, reviewed migration
when the example introduces a new node field. Production/site-specific values
must never be overwritten automatically.

The required deployment sequence is:

```text
git pull
config sync --dry-run/check
review/apply required config additions
confirm Added keys: none
confirm Added node fields: none
restart service
health check
smoke test
```

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

## Read-only historical Data API

Services with a clean historical readings root expose:

```text
GET /api/data/files
GET /api/data/files/{path:path}
```

The canonical CESH Air router is the reference. Requirements:

- a dedicated token in ignored `app_config.json`; empty or missing means 503;
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
must be separate from application code and configured by a deployment-local
environment file. The reusable lifecycle is:

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

## Data access and MCP boundary

```text
Monitoring service
    -> authenticated read-only Data API
    -> bardbox-mcp
    -> bardbox-query / MCP client / analysis tools
```

Service repositories expose generic files. The central local project
`~/Code/bardcollege/bardbox-mcp` retrieves and packages them. MCP tools, dataset
merging, statistics, filtering, plots, and analysis must not be duplicated in
monitoring servers. `bardbox-query` is a retrieval/packaging tool, not an
analysis engine.

## Declared runtime drift checks

Projects may declare exact expected Python and installed Python distribution
versions plus SHA-256 hashes of deployed driver/service/executable files under
`[runtime]` in `bardbox.toml`. Shared BardBox Tools audits report mismatches and
unavailable files as failures. Missing expectations preserve older audit behavior
and provide no runtime verification; they must not be represented as a clean
runtime inventory.

Run the audit with the deployed service's Python interpreter on the Pi. An audit
of a checkout on a workstation does not inspect a remote Pi or the running
process. File hashes verify bytes on disk, not loaded code, active systemd state,
drop-in precedence, enabled timers or successful backups. Inspect those separately
before signing off a reconciliation. Capture the effective unit and drop-ins
privately: they can contain credentials and must not be published in reports.

The manifest never supplies executable commands. Audits do not install packages,
copy service files, restart/enable units, upgrade rclone or modify measurements.
Use a reviewed maintenance change to reconcile drift, preserving deployment
values and rollback copies; then repeat the audit and relevant operational checks.
Only inventory files approved for inspection; audit output includes status, not
file contents. Per-file reads are limited to 32 MiB and reject nonregular files.

Shared tooling is the implementation owner. The template documents opt-in
expectations; existing projects adopt their actual approved versions separately.
No guessed watchdog/rclone versions are promoted into CESH or RKC. Existing AI
skill instructions already require drift checks; no skill change is needed.
