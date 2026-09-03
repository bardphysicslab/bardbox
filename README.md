# BardBox

`bardbox` is the BardBox standards and specification repo.

It defines the protocol, reading format, driver boundaries, UI standard,
naming conventions, time rules, and design decisions shared by BardBox monitor
projects.

## Role

This repo is the source of truth for:

- device protocol rules
- normalized reading format
- channel names
- Raspberry Pi driver responsibilities
- monitor/dashboard visual standards
- time synchronization rules
- testing expectations
- architecture and naming decisions

It is not the project template and should not be copied directly for new
monitor deployments.

## Repo Roles

`bardbox` is the standards/specification repo.

`bardbox-project-template` is the reference implementation/template repo.

Workflow:

1. Protocol or UI rule changes are documented first in `bardbox`.
2. Then they are implemented in `bardbox-project-template`.
3. New monitor repos are created from `bardbox-project-template`.
4. Existing monitor repos like GoLab, RKC, Solar, and CESH Air should be updated from the template standard when practical.
5. Project-specific repos should not invent protocol behavior unless it is promoted back into `bardbox` and `bardbox-project-template`.

Goal: one documented standard, one reference implementation, many project instances.

## Current Standards

- Node statuses: `ok`, `stale`, `error`, `node_unavailable`
- Node UIDs use `bb-<site>-<type>-<instance>`, for example `bb-gol-air-001`
- Legacy reported UIDs may be aliased to canonical UIDs during migration
- Stale or unavailable API values are `null`
- Dashboards render `null` as `—`
- Pi/backend owns freshness detection
- Base protocol devices report readings and protocol errors; Web Nodes also
  own documented delivery, retry, queue, and communication-diagnostic state
- Standard device commands: `INFO`, `HEADER`, `READ`
- Optional device commands: `START`, `STOP`, `PING`
- RKC Monitor is the current visual reference for BardBox dashboards
- CESH Air and RKC jointly define the BardBox web UI reference
- FastAPI/Uvicorn services require process restart and application watchdog layers
- Historical Data APIs are read-only and enabled only for clean readings roots
- Firmware development uses VS Code + PlatformIO

## Key Docs

- [Reading format](docs/reading-format.md)
- [Node naming standard](docs/node-naming-standard.md)
- [Device instructions](docs/device-instructions.md)
- [Web Node protocol](docs/web-node-protocol.md)
- [Pi driver instructions](docs/pi-driver-instructions.md)
- [Optional driver controls](docs/driver-controls.md)
- [Monitor/UI instructions](docs/monitor-instructions.md)
- [Channel names](docs/channel-names.md)
- [Time sync standard](docs/time-sync-standard.md)
- [Testing guide](docs/testing-guide.md)
- [Service operations standard](docs/service-operations-standard.md)
- [Web UI standard](docs/web-ui-standard.md)
- [Remote/network access](docs/network-access.md)
- [Promotion governance](docs/promotion-governance.md)

## Standards Classification

| Standard | Classification |
| --- | --- |
| Safe config synchronization | REQUIRED where `app_config` is used |
| `/health`, systemd restart, and watchdog | REQUIRED for web services |
| Read-only Data API | REQUIRED WHEN APPLICABLE |
| Verified backup/retention | REQUIRED WHEN local historical data is retained and pruned |
| Tailscale remote administration | RECOMMENDED for Pi deployments |
| Central Data API/MCP boundary | REQUIRED architectural boundary |
| BardBox web layout | REQUIRED for web applications |

## Promotion Rule

When reusable infrastructure or UI is proven in a production BardBox
repository, completion includes evaluating it for promotion into this standard
and `bardbox-project-template`. See the governance document for the full rule.

## Current Deployments

| Project | Department | Description | Status |
| --- | --- | --- | --- |
| GoLab Monitor | Physics | Air quality monitoring in GoLab | Active |
| RKC Monitor | Physics | Freezer monitoring and alerts | Active |
| Solar Monitor | Physics | Solar/environment monitoring | Active |
| CESH Air Monitor | CESH | Local simulated air monitor demo | Demo |

## Maintained By

Bard College Physics Department
