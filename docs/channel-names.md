# Channel Names

Bard Box uses standardised short channel names to identify sensor measurements. Channel names are used in serial output, driver code, API responses, and dashboards.

## Naming convention

Channel names are lowercase, alphanumeric, no spaces. Typically 2–6 characters.

Prefer names that reflect the physical quantity:

| Prefix | Meaning |
|---|---|
| `t` | Temperature |
| `h` | Humidity |
| `p` | Pressure |
| `c` | Particle count |
| `co2` | CO₂ concentration |
| `pm` | Particulate matter (mass) |
| `v` | Voltage |

## Registered channels

### Particle count channels (GT-521S and compatible)

| Channel | Particle size | Unit | Notes |
|---|---|---|---|
| `c03` | ≥ 0.3 µm | count/ft³ | |
| `c05` | ≥ 0.5 µm | count/ft³ | |
| `c10` | ≥ 1.0 µm | count/ft³ | |
| `c25` | ≥ 2.5 µm | count/ft³ | |
| `c50` | ≥ 5.0 µm | count/ft³ | |
| `c100` | ≥ 10.0 µm | count/ft³ | |

### Environmental channels (BME280 and compatible)

| Channel | Description | Unit | Source |
|---|---|---|---|
| `temp_c` | Air temperature | °C | BME280 |
| `rh_pct` | Relative humidity | % RH | BME280 |
| `press_pa` | Barometric pressure | hPa | BME280 |

## Adding a new channel

1. Choose a short name that doesn't conflict with existing entries
2. Add it to the table above with description, unit, and source sensor
3. Update the relevant driver `README.md` and device `README.md`
