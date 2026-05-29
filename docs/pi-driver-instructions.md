# Pi Driver Instructions

The Raspberry Pi driver is the hardware/protocol boundary. It polls or reads
the device, parses raw responses, normalizes channel names, and returns a
structured BardBox result to the backend.

## Required Interface

```python
class SensorDriver:
    def get_info(self) -> dict: ...
    def get_capabilities(self) -> dict: ...
    def get_reading(self) -> dict: ...
```

## Driver Responsibilities

Drivers must:

- poll or read the device
- parse raw responses
- normalize all channel names to `channel-names.md`
- track last successful communication when the driver owns transport state
- track last valid reading when the driver buffers streaming data
- return structured status, data, message, timestamp, and extended fields
- return `null` values when a reading is stale, unavailable, or invalid
- never present cached values as live data

Transport failure maps to `node_unavailable`. Parse or validation failure maps
to `error`. A fresh valid response maps to `ok`.

## Reading Result Contract

```json
{
  "uid": "bb-gol-air-001",
  "timestamp": "2026-04-03T14:32:10Z",
  "status": "ok",
  "message": "Fresh valid reading",
  "data": {
    "temp_c": 22.4
  },
  "extended": {
    "last_seen": "2026-04-03T14:32:10Z"
  },
  "raw": null
}
```

Drivers may raise a timeout/transport exception if the device cannot be reached;
the backend may then normalize that to `node_unavailable`. Drivers that manage
background streaming should themselves return `stale` with null data when their
buffer is older than the freshness timeout.

## Backend Boundary

`main.py` must not construct vendor commands, parse vendor responses, or know
device quirks. It may call driver methods and apply cross-node policy such as
freshness timeout, logging, API response shaping, and dashboard routing.
