# Bard Box Normalized Channel Names

This is the authoritative list of normalized channel names for Bard Box.

All drivers and devices must use these names. Do not invent alternate names 
for existing channels.

To add a new channel name, submit a pull request to this repo with a clear 
description of the sensor and unit.

---

## Environmental

| Channel | Unit | Description |
|---------|------|-------------|
| `temp_c` | C | Temperature in Celsius |
| `rh_pct` | % | Relative humidity |
| `press_pa` | Pa | Atmospheric pressure |
| `co2_ppm` | ppm | CO2 concentration |
| `lux` | lux | Light level |

---

## Particle Counts — Standard

| Channel | Unit | Description |
|---------|------|-------------|
| `pm1_std` | count | PM1.0 standard count |
| `pm25_std` | count | PM2.5 standard count |
| `pm10_std` | count | PM10 standard count |

---

## Particle Counts — Environmental

| Channel | Unit | Description |
|---------|------|-------------|
| `pm1_env` | count | PM1.0 environmental count |
| `pm25_env` | count | PM2.5 environmental count |
| `pm10_env` | count | PM10 environmental count |

---

## Particle Counts — Per Cubic Foot

| Channel | Unit | Description |
|---------|------|-------------|
| `c03` | count/ft³ | 0.3µm particles per cubic foot |
| `c05` | count/ft³ | 0.5µm particles per cubic foot |
| `c10` | count/ft³ | 1.0µm particles per cubic foot |
| `c25` | count/ft³ | 2.5µm particles per cubic foot |
| `c50` | count/ft³ | 5.0µm particles per cubic foot |
| `c100` | count/ft³ | 10µm particles per cubic foot |
