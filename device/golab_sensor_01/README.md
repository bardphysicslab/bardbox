# golab_sensor_01

**Bard Box UID:** `bb-0001`
**Project:** GoLab Monitor
**Location:** Go Lab, Bard College Physics Department
**Status:** Active

## Sensors

| Sensor | Channels | Interface | Notes |
|---|---|---|---|
| GT-521S | `c03`, `c05` | USB serial (CP2102) | Particle counter, counts in particles/m³ |
| BME280 | `temp`, `hum`, `pres` | I²C | Temperature, humidity, pressure |
| PMS | TBD | UART | Particulate matter sensor |

## Channel map

| Channel | Description | Unit |
|---|---|---|
| `c03` | Particle count ≥ 0.3 µm | particles/m³ |
| `c05` | Particle count ≥ 5.0 µm | particles/m³ |
| `temp` | Air temperature | °C |
| `hum` | Relative humidity | % RH |
| `pres` | Barometric pressure | hPa |

## Serial configuration

- Baud rate: 9600
- Line termination: `\r\n`
- Count units: particles/m³ (`CU 3` sent at run start)

## Hardware notes

- GT-521S connects via USB (Silicon Labs CP2102 USB-UART bridge)
- Serial device path: `/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_Y10162-if00-port0`
- Pi gateway: `golab-pi` at `10.60.10.59`

## Firmware

See [`golab_sensor_01.ino`](golab_sensor_01.ino) — placeholder, not yet implemented.
The GT-521S is currently driven directly from the Pi via `drivers/gt521s_driver`.
