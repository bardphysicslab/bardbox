# Channel Names

BardBox channel names are canonical API identifiers used by device headers,
drivers, API responses, logs, and dashboards.

Rules:

- lowercase
- underscores between components
- no spaces
- no vendor aliases
- unit is defined by the standard, not embedded in ad hoc names

## Registered Channels

| Channel | Description | Unit |
| --- | --- | --- |
| `temp_c` | Air temperature | deg C |
| `rh_pct` | Relative humidity | % |
| `press_pa` | Barometric pressure | Pa |
| `pm1_std` | PM1.0 standard concentration | ug/m3 |
| `pm25_std` | PM2.5 standard concentration | ug/m3 |
| `pm10_std` | PM10 standard concentration | ug/m3 |
| `pm1_env` | PM1.0 environmental concentration | ug/m3 |
| `pm25_env` | PM2.5 environmental concentration | ug/m3 |
| `pm10_env` | PM10 environmental concentration | ug/m3 |
| `c03` | Particles >= 0.3 um | count/ft3 |
| `c05` | Particles >= 0.5 um | count/ft3 |
| `c10` | Particles >= 1.0 um | count/ft3 |
| `c25` | Particles >= 2.5 um | count/ft3 |
| `c50` | Particles >= 5.0 um | count/ft3 |
| `c100` | Particles >= 10.0 um | count/ft3 |
| `door_open` | Door open state | boolean |
| `voltage_v` | Voltage | V |
| `current_a` | Current | A |
| `power_w` | Electrical power | W |
| `load_resistance_ohm` | Applied electronic-load resistance | ohm |

Use `null` when a declared channel is unavailable, stale, or invalid.

## Adding Channels

Add new channels here before using them in firmware, drivers, APIs, or
dashboards. Existing project repos should not invent alternate names when a
standard channel already exists.
