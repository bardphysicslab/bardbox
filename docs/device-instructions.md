# Device Generic Instructions

## Goal

Write code for a Bard Box device that sends sensor data to a Raspberry Pi.

A device may be:

* Arduino
* ESP32
* RP2040
* any microcontroller
* any system capable of sending structured data over serial

This document is hardware-agnostic.

The device's role is:
→ acquire data
→ implement the Bard Box protocol
→ send clean, structured output

---

## Core Principle

The device is a data source, not the application.

It must:

* read sensors
* implement the serial protocol
* send structured data

It must NOT:

* perform logging
* implement dashboards
* contain backend logic
* use project-specific naming

---

## Device Identity

Each device must define a stable unique ID (UID) in firmware.

```cpp
#define DEVICE_UID "bb-0001"
#define FW_VERSION "1.0"
```

Rules:

* UID must be unique across all Bard Box devices
* UID must NOT change once deployed
* UID must NOT be a project-local name like `sensor_01`
* Human-readable names are assigned on the Raspberry Pi
* UIDs are assigned from the Bard Box device registry (`uid-registry.md`)

---

## Required Behavior

The device must:

* continuously listen for serial commands
* start and stop data streaming based on commands
* output clean CSV only when running
* remain responsive at all times
* never print debug output to the serial stream
* use non-blocking logic

---

## Required State

```cpp
bool running = false;
```

Rules:

* default is `false`
* when `running == true`, device streams data
* when `running == false`, device sends no data (only command responses)

---

## Loop Behavior

The main loop must:

* continuously check for serial input
* process commands immediately
* send data only when `running == true`
* avoid long blocking operations
* use `millis()` or equivalent timing instead of `delay()`

---

## Bard Box Serial Protocol

### Commands

Commands are newline-terminated text:

```
START
STOP
STATUS
PING
HEADER
INFO
```

---

### Responses

Responses must be exact:

```
OK START
OK STOP
OK STATUS RUNNING
OK STATUS STOPPED
PONG
OK INFO uid=bb-0001 fw=1.0 sensors=PMS,BME280
```

Rules:

* `INFO` must include UID and firmware version
* `sensors` describes connected sensor types
* Responses must be single-line and deterministic

---

### Error Handling

Unknown commands must return:

```
ERR UNKNOWN_CMD
```

Optional errors:

```
ERR SENSOR_FAIL
ERR NOT_RUNNING
```

---

## Data Output Rules

### Header Format

```
HDR,v1,<field1>,<field2>,<field3>,...
```

Rules:

* Send header immediately after `START`
* Send header when `HEADER` is requested
* Header defines structure of all subsequent data lines

---

### Data Line Format

```
DAT,<value1>,<value2>,<value3>,...
```

Rules:

* Every `DAT` line must match the header exactly
* No extra fields
* No missing fields
* Consistent order
* No JSON output
* No mixed output

---

## Channel Naming

Use normalized Bard Box field names from `channel-names.md`.

Rules:

* Do NOT use vendor-specific raw names
* Do NOT invent alternate names if a standard exists
* Include units in the name where applicable (`_c`, `_pct`, `_pa`, etc.)

If introducing a new sensor:

* choose a clear normalized name
* add it to `channel-names.md` in the protocol repo

---

## Sensor Implementation

Inside the device code:

* use modular sensor abstractions
* use one module/class per sensor
* follow clean design patterns (Adafruit-style recommended)
* normalize values before output

Internal implementation may use any library.
External output must follow the Bard Box protocol.

---

## Unit Rules

All values must be normalized before output:

* temperature → °C → `temp_c`
* humidity → % → `rh_pct`
* pressure → Pa → `press_pa`

Convert units if the sensor library uses different units.

---

## Serial Parsing Rules

The device must:

* read input until newline
* trim whitespace
* ignore empty lines
* ignore carriage returns (`\r`)
* treat commands as case-sensitive

---

## Timing Rules

* Use non-blocking timing (`millis()` or equivalent)
* Do not delay command handling
* Device must always respond quickly to:

  * `STOP`
  * `STATUS`
  * `PING`
  * `HEADER`
  * `INFO`

---

## Code Structure

### Setup

* initialize serial communication
* initialize sensors
* initialize required interfaces

### Loop

* read and process serial commands
* send data when running
* use non-blocking timing

### Helper Functions

* `handleCommand(...)`
* `checkSerial()`
* `sendHeader()`
* `sendInfo()`
* `sendStatus()`
* `sendData()`

---

## Output Quality Rules

All output must be:

* machine-readable
* deterministic
* consistent
* free of debug output

Do NOT:

* print debug logs
* mix control responses with data
* add extra commas or spaces
* reorder fields
* change protocol version arbitrarily

---

## What To Avoid

Do NOT:

* hardcode project-specific names (e.g. `sensor_01`)
* use JSON over serial
* block execution with delays
* embed backend logic in the device
* write code that only works for one deployment

---

## Final Requirement

Return a complete device code file.

The file must:

* be ready to run on Arduino, ESP32, or similar
* implement the Bard Box protocol exactly
* include UID and firmware version
* produce clean CSV output

Do not include explanations.
Do not include pseudocode.
Return one complete, usable file.
