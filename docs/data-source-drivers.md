# BardBox Data Source Driver Standard

## Core Rule

BardBox treats every instrument, sensor, node, or remote data feed as a **data source** behind a driver.

Whether a source is local or external is transport/deployment metadata, not a different application architecture.

Examples include:

- a directly attached serial instrument such as a GT-521S particle counter
- a directly attached SPN1 solar instrument
- a BardBox microcontroller node aggregating multiple sensors
- a remote/vendor source such as PurpleAir
- a remote/vendor source such as QuantAQ

The Pi/runtime application consumes normalized driver output and must not contain vendor-specific protocol, API, CSV, or transport logic.

## Driver Boundary

Each source driver follows the normal BardBox driver contract:

```python
class SensorDriver:
    def get_info(self) -> dict: ...
    def get_capabilities(self) -> dict: ...
    def get_reading(self) -> dict: ...
```

A driver may acquire data over serial, USB, HTTP/HTTPS, a vendor API, a local archive maintained by a sync process, or another explicitly configured transport. The acquisition mechanism must not change the normalized reading contract.

Source/transport identity belongs in `get_info()` or `extended`, for example:

```json
{
  "manufacturer": "PurpleAir",
  "model": "PA-II-FLEX",
  "source_type": "remote_instrument",
  "transport": "vendor_api"
}
```

## Availability Semantics

All data sources use the same semantic availability progression:

```text
LIVE -> STALE -> OFFLINE
```

Normalized driver/runtime meanings are:

- `ok` — a fresh, valid reading is available.
- `stale` — the source has previously supplied valid data, but the newest reading has exceeded that source's freshness threshold. Current metric values must be null/not presented as live.
- `node_unavailable` — the source cannot currently be reached or has exceeded its configured offline threshold. The UI presents this as OFFLINE.
- `error` — communication/data was obtained but could not be parsed or validated correctly.

A remote/vendor source must not remain `stale` indefinitely. Once its offline threshold is exceeded it becomes unavailable/OFFLINE.

## Threshold Policy

BardBox standardizes the meanings of LIVE, STALE, and OFFLINE, but does not require one numeric threshold for every source.

Thresholds must reflect the expected cadence and behavior of the source. For example, a local serial instrument polled every second and a cloud service updated every few minutes may use different thresholds.

Each driver or deployment configuration should expose enough metadata to explain its policy, including where applicable:

- expected update interval
- stale-after interval
- offline-after interval
- last successful communication / last seen timestamp

Thresholds must be monotonic: `offline_after` must be greater than `stale_after`.

## UI Rule

Dashboards must present equivalent source states consistently regardless of vendor or transport:

- `ok` / fresh -> `LIVE`
- `stale` -> `STALE`
- `node_unavailable` / offline -> `OFFLINE`
- `error` -> `ERROR`

Source badges such as `EXTERNAL`, manufacturer names, or transport labels may be shown separately, but they must not create a separate availability model.

## Migration Rule

Existing project-specific integrations that bypass the driver layer may be migrated incrementally. New integrations should use the driver model from the start. When an existing integration is touched substantially, vendor-specific freshness and availability logic should be moved toward the driver boundary rather than expanded inside `main.py`.
