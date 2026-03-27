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

| Channel | Description | Unit | Source |
|---|---|---|---|
| `c03` | Particle count ≥ 0.3 µm | particles/m³ | GT-521S |
| `c05` | Particle count ≥ 5.0 µm | particles/m³ | GT-521S |
| `temp` | Air temperature | °C | BME280 |
| `hum` | Relative humidity | % RH | BME280 |
| `pres` | Barometric pressure | hPa | BME280 |

## Adding a new channel

1. Choose a short name that doesn't conflict with existing entries
2. Add it to the table above with description, unit, and source sensor
3. Update the relevant driver `README.md` and device `README.md`
