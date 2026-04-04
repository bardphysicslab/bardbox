# gt521s_driver

Bard Box Pi driver for the **GT-521S optical particle counter**.

## Sensor overview

The GT-521S measures airborne particle concentrations in up to six size channels. It communicates via USB serial using a simple ASCII command protocol.

## Channels

| Channel | Description | Unit |
|---|---|---|
| `c03` | Particle count ≥ 0.3 µm | count/ft³ |
| `c50` | Particle count ≥ 5.0 µm | count/ft³ |

## Serial configuration

| Parameter | Value |
|---|---|
| Interface | USB serial (CP2102 USB-UART bridge) |
| Baud rate | 9600 |
| Line termination | `\r` (carriage return) |
| Count units | count/ft³ (`CU 0`) |

## Key commands

| Command | Description |
|---|---|
| `CU 0` | Set count units to count/ft³ (Bard Box standard) |
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

Count values are in whatever unit is active — always send `CU 0` before starting a run.

## Driver interface

`GT521SDriver` implements the Bard Box driver interface:

| Method | Returns | Description |
|---|---|---|
| `get_info()` | `dict` | Sensor name, serial config, count units |
| `get_capabilities()` | `list` | Channel names, descriptions, units |
| `get_reading()` | `dict` or `None` | Latest parsed reading, or `None` if no data yet |
| `start()` | — | Open serial, send setup commands, start reader thread |
| `stop()` | — | Stop sampling, stop reader thread |

## Used by

- `device/golab_sensor_01` (`bb-0001`, GoLab Monitor)
