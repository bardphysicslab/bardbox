# Pi Runtime Instructions

> This document defines the behavior of the main Pi application (commonly implemented as `main.py`).

## Goal

Define the standard structure and behavior for the main Raspberry Pi application (`main.py`) in a Bard Box deployment.

The Pi app is the runtime layer. It connects drivers to the frontend and ensures all data is normalized, validated, and consistently exposed.

---

## Core Role

The Pi app is the system orchestrator.

It must:

* load configuration
* load and manage drivers
* collect normalized readings
* maintain validated application state
* expose data to the frontend
* serve the monitor/dashboard interface

It must NOT:

* parse raw device protocols
* depend on sensor-specific implementations
* contain hardware-specific logic
* expose raw vendor data

---

## Core Rule

The Pi app consumes only normalized driver output.

All hardware-specific behavior must be handled inside drivers.

The Pi app must never communicate with hardware directly. All hardware interaction occurs inside drivers.

---

## Device Command Conventions

When a driver sends text commands to a device, commands must be newline-terminated (`\n`).

The Pi app must not send device-specific commands directly.
All device communication must go through drivers.

Drivers must not depend on carriage return behavior (`\r`), vendor-specific line endings, or serial monitor defaults.

---

## App Identity

Each deployment must define an App ID.

```python
APP_ID = "bb-golab-dashboard"
```

### Naming Rules

The App ID describes the **role of the system in its deployment context**.

It should answer:

> “What does this system do here?”

Do NOT describe:

* specific sensors (`pms`, `bme`, etc.)
* wiring or transport
* internal implementation details

Examples:

* `bb-golab-dashboard`
* `bb-cleanroom-monitor`
* `bb-gallery-display`

Rules:

* lowercase
* hyphen-separated
* human-readable
* stable across deployments
* describe system role, not components

---

## Configuration

The Pi app MUST be driven by configuration, not hardcoded values.

Minimum required fields:

```json
{
  "app_id": "bb-golab-dashboard",
  "mode": "sensor_monitor",
  "poll_interval_ms": 1000,
  "drivers": [
    {
      "driver": "gt521s",
      "uid": "bb-0001",
      "config": {
        "port": "/dev/ttyUSB0",
        "baud": 9600
      }
    }
  ]
}
```

Rules:

* no hardcoded UIDs
* no hardcoded device paths
* deployment-specific values must live in config

---

## Driver Model

A driver represents a single data source.

A data source may be:

* a direct sensor or instrument
* a microcontroller node aggregating multiple sensors

The Pi app MUST treat all drivers identically through the driver interface.

The Pi app interacts with drivers only through the defined interface and optional control methods.

---

## Driver Interface Enforcement

Each driver MUST implement:

```python
get_info() -> dict
get_capabilities() -> dict
get_reading() -> dict
```

### Startup Validation

On startup, the Pi app MUST:

* verify all required methods exist
* call `get_info()` and validate required fields
* call `get_capabilities()` and validate structure

If any driver fails validation:
→ **startup MUST fail**

---

## Driver Output Validation

The Pi app MUST validate all readings returned by drivers.

### Required `get_reading()` structure

```json
{
  "uid": "bb-0001",
  "timestamp": "2026-03-27T18:00:00Z",
  "status": "ok",
  "data": { ... },
  "extended": { ... },
  "raw": null
}
```

### Validation Rules

The Pi app MUST enforce:

* `uid` exists and matches driver
* `timestamp` exists and is ISO 8601
* `status` is one of: `ok`, `stale`, `error`
* `data` is an object
* all keys in `data` match declared channel names from `get_capabilities()`
* all declared channels must appear in `data` (use `null` if unavailable)
* `extended` must exist and be a dict (may be `{}`)
* `raw` must exist (may be `null`)

If validation fails:

* discard the reading
* mark driver as `error`
* log the failure

---

## Internal Data Model

The Pi app MUST maintain normalized, validated in-memory state.

Example:

```json
{
  "app_id": "bb-golab-dashboard",
  "mode": "sensor_monitor",
  "status": "ok",
  "drivers": {
    "bb-0001": {
      "info": { ... },
      "capabilities": { ... },
      "latest": {
        "uid": "bb-0001",
        "timestamp": "2026-03-27T18:00:00Z",
        "status": "ok",
        "data": { ... },
        "extended": {},
        "raw": null
      }
    }
  }
}
```

Rules:

* state must only contain validated data
* no raw protocol artifacts
* must be serializable and deterministic

---

## Time Authority and Logging Gate

The Pi app MUST use the operating system clock as the application time
authority. It must not read the RTC directly. The RTC provides boot/offline
holdover for the system clock only.

The app MUST expose a `/time` endpoint and include time health in `/state`.
Required time states are:

* `ntp` — valid and currently NTP-synchronized
* `rtc_holdover` — valid RTC-backed/offline holdover
* `invalid` — not acceptable for recording

The dashboard UI SHOULD show visible clock/time status. Start/logging controls
MUST be disabled or rejected when time is `invalid`.

All logged timestamps MUST be UTC ISO 8601 strings.

---

## Session and Export Storage

The Pi app SHOULD use the standard storage layout:

```text
~/golab-monitor/data/
~/golab-monitor/data/sessions/
~/golab-monitor/data/env_daily_averages.jsonl
```

When removable storage is supported, the app must use mounted filesystem paths,
not raw USB or serial-device scans. Standard mounted targets are under:

```text
/media/<user>/...
```

Session target selection affects future session/test recording paths only.
For USB targets, session files SHOULD be written under:

```text
/media/<user>/<target>/golab-monitor/sessions/
```

Exports are separate copy actions. Daily averages remain local and may be copied
to:

```text
/media/<user>/<target>/golab-monitor/exports/
```

Exporting must not move, clear, or change the live daily-average logging path.
This session/export scaffolding should be part of the standard main Pi app
template for Bard Box dashboards.

---

## Polling

The Pi app MUST collect readings on a configured interval.

Rules:

* interval defined in config
* polling must not block the app
* one driver failure must not affect others

Behavior:

* success → update latest state
* temporary failure → mark `stale`
* repeated failure → mark `error`

---

## Status Model

### Driver status

* `ok`
* `stale`
* `error`

### App status

* `ok` — all required drivers healthy
* `degraded` — partial failure
* `error` — system cannot function

---

## API Requirements

The Pi app MUST expose stable, normalized endpoints.

Required endpoints:

```
GET /app/info
GET /app/health
GET /drivers
GET /readings/latest
```

Rules:

* responses must be machine-readable
* must contain normalized data only
* must not expose raw device data
* must not expose transport or protocol details

---

## Monitor Mode

The primary deployment mode is:

```
sensor_monitor
```

Rules:

* mode is defined in config
* Pi app must provide all data required by the monitor
* layout rules belong in `monitor-instructions.md`

---

## Logging

The Pi app MUST log:

* startup
* configuration loading
* driver loading
* validation failures
* runtime driver errors
* recovery events

Logs MUST include:

* timestamp
* app_id
* driver UID (if applicable)

Do NOT log:

* raw sensor payloads by default
* unnecessary debug noise

---

## Concurrency

The Pi app must ensure:

* no race conditions
* consistent state reads
* driver calls do not block the server

Use the simplest reliable model (threading or async).

---

## What To Avoid

Do NOT:

* hardcode deployment-specific values
* parse device protocols in `main.py`
* leak hardware details to the frontend
* skip validation of driver output
* silently ignore failures
* mix UI logic with backend logic

---

## Startup Sequence

On startup, the Pi app MUST:

1. load configuration
2. validate configuration
3. load drivers
4. validate driver interfaces
5. validate driver metadata and capabilities
6. initialize state
7. start polling loop
8. start API/server

If any critical step fails:
→ **fail clearly and stop**

---

## Final Requirement

The Pi app must:

* be deployment-agnostic
* enforce the driver contract strictly
* maintain validated, normalized state
* expose stable APIs
* support sensor monitor deployments

Return complete, working code when implementing.

Do not return pseudocode.
