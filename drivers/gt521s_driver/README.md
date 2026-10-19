# gt521s_driver

> **Legacy, non-conforming example (October 19, 2026).** This driver predates the
> current driver contract and does not conform to it: `get_info()` lacks
> `uid`/`transport`/`protocol`, `get_capabilities()` returns a list, readings are
> not normalized and use the instrument's naive clock. Keep it as historical
> GoLab reference only; do not copy it. Code, tests and fixtures are unchanged;
> their drift is tracked in [bardbox#49](https://github.com/bardphysicslab/bardbox/issues/49).
> Archived prompts that produced it: [archive/legacy/refactor](../../archive/legacy/refactor/README.md).

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
| Count units | count/ft³ (`CU 0`), the documented compatibility unit for particle-count channels |

## Key commands

| Command | Description |
|---|---|
| `CU 0` | Set count units to count/ft³ (the channel's documented compatibility unit) |
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

This driver predates the current driver contract and is not a model module: it mixes serial I/O, threading and parsing and keeps serving its last value after a serial error. Use the standards, not this driver, as the example.

`GT521SDriver` implements the Bard Box driver interface:

| Method | Returns | Description |
|---|---|---|
| `get_info()` | `dict` | Sensor name, serial config, count units |
| `get_capabilities()` | `list` | Channel names, descriptions, units |
| `get_reading()` | `dict` or `None` | Latest parsed reading, or `None` if no data yet |
| `start()` | — | Open serial, send setup commands, start reader thread |
| `stop()` | — | Stop sampling, stop reader thread |

## Example deployment

Canonical UID example: `bb-gol-air-001`.

Historical GoLab Arduino IDE notes were moved under `archive/legacy/` and are
not current implementation guidance.
