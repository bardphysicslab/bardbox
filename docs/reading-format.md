# BardBox Standard 01 — Reading Format

Every BardBox API reading is normalized by the Raspberry Pi/backend before it
reaches dashboards, logs, exports, or alerts.

```json
{
  "uid": "bb-gol-air-001",
  "timestamp": "2026-04-03T14:32:10Z",
  "status": "ok",
  "message": "Fresh valid reading",
  "data": {
    "temp_c": 22.4,
    "rh_pct": 41.2
  },
  "extended": {
    "last_seen": "2026-04-03T14:32:10Z",
    "rssi_dbm": -62
  }
}
```

Implementations may also include bounded `raw` debug payloads, but application
logic must not depend on `raw`.

## Required Fields

- `uid`: stable BardBox device identifier using `bb-<site>-<type>-<instance>`.
- `timestamp`: UTC ISO 8601 timestamp for this API reading.
- `status`: one of `ok`, `stale`, `error`, `node_unavailable`.
- `message`: short human-readable status detail.
- `data`: canonical channel names mapped to numeric, boolean, string, or `null` values.
- `extended`: operational metadata such as `last_seen`, `rssi_dbm`, firmware, host, port, location, or diagnostics.

## Status Rules

- `ok`: fresh valid reading.
- `stale`: a last valid reading exists, but it is older than the configured freshness timeout.
- `error`: the device responded, but returned invalid, malformed, or unparseable data.
- `node_unavailable`: the device could not be reached or did not respond.

Dashboards must not show stale readings as if they are current. When status is
`stale`, `error`, or `node_unavailable`, declared channel values in `data` must
be `null`. The previous successful timestamp may be shown separately as
`extended.last_seen`.

The Pi/backend is responsible for freshness detection. Firmware and devices
report readings and protocol errors; they do not decide stale vs unavailable.

## Data Rules

`data` contains only canonical channel names from `channel-names.md`.

Rules:

- Include every declared channel for the node.
- Use `null` when a declared channel is unavailable.
- Do not use vendor names or UI aliases.
- Do not encode units into values; units live in the capability/channel definition.

## Extended Rules

`extended` is for operational metadata, not canonical measurements. Common
fields include:

- `last_seen`
- `rssi_dbm`
- `uptime_s`
- `firmware_version`
- `host`
- `port`
- `location`
- `stale_after_s`

## Wire Protocol vs API Object

Devices may use compact wire responses such as:

```text
HDR,v1,temp_c,rh_pct,press_pa
DAT,22.27,39.02,101096
```

The Pi driver converts those responses into normalized BardBox API readings.
Devices do not need to emit JSON.

## UID Format

New node UIDs must follow:

```text
bb-<site>-<type>-<instance>
```

Examples include `bb-gol-air-001`, `bb-rkc-frz-014`, and `bb-sol-sol-001`.
Legacy IDs like `bb-0001`, `bb-0002`, and `bb-0003` remain supported for
existing deployments, but are deprecated. All new deployments must use the new
format.

If a deployment config maps a legacy device-reported UID to a canonical UID,
API readings must use the canonical UID. Existing historical logs keep whatever
UID they were originally written with.
