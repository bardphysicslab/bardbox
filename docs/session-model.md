# Session Model

## General Rule

Session state (session_id, status, start_time, end_time, metadata, summary, data)
is owned by the application layer (`main.py`), not the driver.

Drivers expose normalized readings via `get_reading()`. The application decides
when a session starts, what it records, and when it ends.

---

## Exception: `start_session()` in Hardware-Sequenced Drivers

Some hardware protocols require a complex, ordered command sequence that must be
executed atomically before sampling can begin. For these drivers, a `start_session()`
convenience method is acceptable inside the driver.

### When this exception applies

A driver may implement `start_session(settings, on_sample)` when:
- The hardware requires a specific sequence of commands before it will produce data
- The sequence is hardware-specific and cannot be split across layers without risk
- The method manages **hardware state only** — not application session state

### Boundary requirements

`start_session()` in the driver:
- Opens the serial port
- Wakes the device
- Sends all configuration commands in the required order
- Starts sampling
- Verifies device status
- Starts the background reader thread
- Calls `on_sample({"c03": ..., "c50": ...})` per received sample — normalized fields only

`start_session()` must NOT:
- Store or return a `session_id`
- Record `start_time`, `end_time`, or `metadata`
- Call into `SessionManager` or any application-layer object
- Pass vendor-internal field names (e.g. `_device_ts`, `_raw_line`) through `on_sample`

Application session state — `session_id`, `start_time`, `metadata`, `summary`, `data` —
is created and managed by `SessionManager` in `main.py`, called after `start_session()`
returns successfully.

### Reference implementation

`GT521SDriver.start_session()` in `golab-monitor/gt521s_driver.py` is the reference
implementation of this pattern. It owns the full GT-521S hardware start sequence
(open → wake → stop → configure → start → verify OP → ensure reader) while keeping
all application session tracking in `main.py`.

---

## `on_sample` Callback Contract

The `on_sample` callback is the boundary between driver and application.

The driver calls it with a normalized dict containing only Bard Box channel fields:
```python
on_sample({"c03": 1452, "c50": 87})
```

The driver must not pass:
- Raw serial bytes
- Vendor field names (`_device_ts`, `_raw_line`, etc.)
- Parsed vendor structures

The application callback decides what the sample means: threshold checks,
session data recording, alerting, etc.
