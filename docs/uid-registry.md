# UID Registry

Every Bard Box device node is assigned a unique identifier in the format `bb-XXXX`.

UIDs are assigned sequentially. Never reuse a UID, even if a device is retired.

## Registry

| UID | Device ID | Project | Sensors | Location | Status |
|---|---|---|---|---|---|
| `bb-0001` | `golab_sensor_01` | GoLab Monitor | GT-521S, BME280, PMS | Go Lab, Bard Physics | Active |

## Assigning a new UID

1. Take the next available number from this table
2. Add a row with device ID, project, sensors, location, and status
3. Commit the update to this file before writing firmware
4. Embed the UID in the device firmware
