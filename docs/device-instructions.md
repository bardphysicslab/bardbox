# Device Node Instructions

A Bard Box device node is a microcontroller that collects sensor data and streams it to the Pi gateway over serial (USB or UART).

## Supported platforms

- Arduino Uno / Mega
- ESP32 (preferred for Wi-Fi deployments)
- Any platform with Arduino IDE support

## Serial output format

Device nodes output CSV lines at a fixed interval over serial:

```
YYYY-MM-DD HH:MM:SS, <channel>, <value>, <channel>, <value>, ...\r\n
```

Example:
```
2026-03-20 14:32:01, c03, 1452, c05, 87
```

- Timestamp is in local time (or UTC if NTP is available)
- Channel names follow the convention in [`channel-names.md`](channel-names.md)
- Values are integers or floats depending on the sensor
- Line is terminated with `\r\n`

## Baud rate

Default: **9600**. Document any deviation in the device's `README.md`.

## Firmware structure

Each device lives in `device/<device_id>/`:

```
device/
  golab_sensor_01/
    golab_sensor_01.ino   ← main firmware sketch
    README.md             ← UID, sensors, wiring, channel map
```

## UID assignment

Every device gets a UID from [`uid-registry.md`](uid-registry.md) before firmware is written. The UID is embedded in the firmware and transmitted in the serial header or as a dedicated field.

## Checklist before deploying

- [ ] UID assigned and registered
- [ ] Sensors wired and verified
- [ ] Serial output matches expected format
- [ ] Channel names registered in `channel-names.md`
- [ ] Device `README.md` written
- [ ] Firmware flashed and confirmed streaming
