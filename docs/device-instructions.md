# Device Instructions

BardBox devices are data sources. They read sensors and answer a compact,
deterministic protocol. They do not implement dashboards, logging, freshness
policy, or deployment-specific backend behavior.

Network-connected nodes that upload and buffer measurements must also follow
the canonical [BardBox Web Node Protocol](web-node-protocol.md). That document
adds delivery, acknowledgment, retry, persistent-buffering, and quiet
background-operation requirements without changing the compact commands below.
Its persistent delivery queue is transport state, not a replacement for
backend historical logging.

## Development Environment

Firmware development standard:

- VS Code
- PlatformIO
- `software/firmware/` per the [repository layout](repository-layout.md)
  (older projects use a top-level `firmware/` root): `platformio.ini`,
  `src/main.cpp`, `include/`, and `lib/` when needed

Arduino libraries are allowed when used through PlatformIO. New examples should
not be Arduino IDE `.ino` sketches as the primary source of truth.

## Identity

Each device must have a stable UID using the current BardBox node naming
standard:

```cpp
static const char *DEVICE_UID = "bb-gol-air-001";
static const char *FW_VERSION = "1.0.0";
```

UID format:

```text
bb-<site>-<type>-<instance>
```

The site and type codes are exactly 3 lowercase letters, and the instance is
exactly 3 digits. See `node-naming-standard.md`.

Human-readable names and installation locations belong in server Registry
configuration. UIDs are immutable once deployed; the monitored entity's identity
is separate from the node's ([identity layers](node-naming-standard.md#identity-layers)).
All absolute device timestamps are UTC.

Devices running BardBox firmware record persistently by default, including
serial-connected nodes; `READ` serves the latest sample and never drains or
acknowledges recorded data ([firmware blueprint](firmware-blueprint.md)).

Legacy IDs like `bb-0001`, `bb-0002`, and `bb-0003` remain supported for
existing deployments, but are deprecated. All new deployments must use
`bb-<site>-<type>-<instance>`.

During migration, the Pi/backend may alias a device-reported legacy UID to the
canonical new UID. API responses, dashboards, and new logs must use the
canonical UID; historical logs are not rewritten.

## Standard Commands

Required for BardBox protocol nodes:

- `INFO`
- `HEADER`
- `READ`

Optional:

- `START`
- `STOP`
- `PING`

`START` and `STOP` are only required for session-style or streaming devices.
Simple polled environmental nodes can implement `INFO`, `HEADER`, `READ`, and
optionally `PING`.

Web Nodes may additionally implement the optional `UPLOAD`, `PAYLOAD`, and
`BUFFER` diagnostic/maintenance commands. `BUFFER_CLEAR`, when present, is a
destructive maintenance command because it discards unacknowledged readings.
It must never be used automatically for upload recovery. `TRACE` and
`CATCHUP_TRACE` are not standard commands.

## Response Forms

```text
OK INFO uid=bb-gol-air-001 fw=1.0.0 sensors=BME280,PMS
HDR,v1,temp_c,rh_pct,press_pa
DAT,22.27,39.02,101096
PONG
OK START
OK STOP
ERR SENSOR_FAIL
ERR UNKNOWN_CMD
```

Rules:

- Responses are single-line text.
- `INFO` reports `uid`, `fw` and `sensors`. Devices with two firmware slots may
  add `slot=<running application partition label>` before `sensors`. Example:
  `OK INFO uid=bb-gol-air-001 fw=1.0.0 slot=app1 sensors=BME280,PMS`.
  The value must come from the partition the firmware is actually running from,
  never from a build setting, so one binary reports correctly in either slot.
  `slot` is optional. Readers must accept INFO with or without it and must ignore
  INFO fields they do not recognise.
- `HEADER` returns the ordered schema for `DAT`.
- `READ` returns one `DAT,...` sample or an `ERR ...` line.
- `START` begins continuous `DAT` streaming only for streaming devices.
- `STOP` stops streaming only for streaming devices.
- Debug output must not be mixed into the protocol stream.
- Automatic network upload and catch-up activity must remain quiet by default;
  verbose network diagnostics are operator-requested or development-only.

## Freshness

Firmware does not decide whether a node is stale or unavailable. It only reports
current readings or immediate protocol errors. The Pi/backend tracks last
successful communication, last valid reading, freshness timeout, and API status.
