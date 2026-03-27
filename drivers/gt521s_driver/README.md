# gt521s_driver

Bard Box Pi driver for the **GT-521S optical particle counter**.

## Sensor overview

The GT-521S measures airborne particle concentrations in two size channels simultaneously. It communicates via USB serial using a simple ASCII command protocol.

## Channels

| Channel | Description | Unit |
|---|---|---|
| `c03` | Particle count ≥ 0.3 µm | particles/m³ |
| `c05` | Particle count ≥ 5.0 µm | particles/m³ |

## Serial configuration

| Parameter | Value |
|---|---|
| Interface | USB serial (CP2102 USB-UART bridge) |
| Baud rate | 9600 |
| Line termination | `\r` (carriage return) |
| Count units | particles/m³ (`CU 3`) |

## Key commands

| Command | Description |
|---|---|
| `CU 3` | Set count units to particles/m³ |
| `ST NNNN` | Set sample time (seconds) |
| `SH NNNN` | Set hold time (seconds) |
| `SN NNN` | Set number of samples |
| `SR 1` | Set output format to CSV |
| `S` | Start sampling |
| `E` | Stop sampling |
| `OP` | Query operational status |

Commands are terminated with `\r`. The device responds with `*` when ready.

## CSV output format

```
YYYY-MM-DD HH:MM:SS, <size1>, <count1>, <size2>, <count2>, *<checksum>
```

Example:
```
2026-03-20 14:32:01, 0.3, 1452, 5.0, 87, *A3F2
```

Count values are in whatever unit is active — always send `CU 3` before starting a run.

## Current implementation

Driver logic currently lives in `golab-monitor/raspi/main.py` (the `GT521` class).
This will be refactored into a standalone importable module here.

## Used by

- `device/golab_sensor_01` (`bb-0001`, GoLab Monitor)
