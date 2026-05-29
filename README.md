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
- Devices report readings and protocol errors only
- Standard device commands: `INFO`, `HEADER`, `READ`
- Optional device commands: `START`, `STOP`, `PING`
- RKC Monitor is the current visual reference for BardBox dashboards
- Firmware development uses VS Code + PlatformIO

## Key Docs

- [Reading format](docs/reading-format.md)
- [Node naming standard](docs/node-naming-standard.md)
- [Device instructions](docs/device-instructions.md)
- [Pi driver instructions](docs/pi-driver-instructions.md)
- [Monitor/UI instructions](docs/monitor-instructions.md)
- [Channel names](docs/channel-names.md)
- [Time sync standard](docs/time-sync-standard.md)
- [Testing guide](docs/testing-guide.md)

## Current Deployments

| Project | Department | Description | Status |
| --- | --- | --- | --- |
| GoLab Monitor | Physics | Air quality monitoring in GoLab | Active |
| RKC Monitor | Physics | Freezer monitoring and alerts | Active |
| Solar Monitor | Physics | Solar/environment monitoring | Active |
| CESH Air Monitor | CESH | Local simulated air monitor demo | Demo |

## Maintained By

Bard College Physics Department
