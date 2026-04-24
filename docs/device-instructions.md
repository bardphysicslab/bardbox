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
* implement deterministic command responses
* support streaming, polling, or both, depending on the device class
* output clean CSV only as defined by the active command
* remain responsive at all times
* never print debug output to the serial stream
* use non-blocking logic

---

## Device Behavior Classes

Bard Box supports both:

* session/stream-oriented instruments
* slow polled sensors

Streaming is preferred where continuous acquisition is intrinsic to the
instrument. Polling is preferred where periodic single-sample acquisition is the
natural behavior, such as fridge temperature or door-state nodes.

A device may support:

* streaming only
* polled only
* both streaming and polling

---

## Required State Model

```cpp
bool running = false;
```

Rules:

* default is `false`
* streaming devices may set `running == true` after `START`
* polled devices may leave `running == false` and still answer `READ`
* `running == false` means continuous streaming is not active; it does not mean the device cannot acquire a single sample

---

## Loop Behavior

The main loop must:

* continuously check for serial input
* process commands immediately
* for streaming devices, send periodic data only when `running == true`
* for polled devices, send one data line only in response to `READ`
* avoid long blocking operations
* use `millis()` or equivalent timing instead of `delay()`

---

## Bard Box Serial Protocol

### Commands

Commands are newline-terminated text:

```
INFO
PING
STATUS
HEADER
READ
START
STOP
```

---

### Responses

Responses must be exact:

```
OK START
OK STOP
OK STATUS RUNNING
OK STATUS STOPPED
HDR,v1,<field1>,<field2>,<field3>,...
DAT,<value1>,<value2>,<value3>,...
PONG
OK INFO uid=bb-0001 fw=1.0 sensors=PMS,BME280
```

Rules:

* `INFO` must include UID and firmware version
* `sensors` describes connected sensor types
* Responses must be single-line and deterministic
* `INFO`, `PING`, `STATUS`, and `HEADER` are valid for both streaming and polled devices
* `HEADER` returns exactly one `HDR,v1,...` line
* `HEADER` may be called at any time
* `HEADER` does not start streaming and does not change device state
* `READ` returns one `DAT,...` data line only; it does not return `OK READ`
* `START` on a streaming device returns `OK START`, followed by `HDR,v1,...`, then `DAT,...` lines

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

`READ` may return `ERR SENSOR_FAIL` if the device cannot acquire a sample.

---

## Data Output Rules

### Header Format

```
HDR,v1,<field1>,<field2>,<field3>,...
```

Rules:

* Streaming devices send header immediately after `START`
* The `HEADER` command returns exactly one `HDR,v1,...` line
* `HEADER` may be called at any time
* `HEADER` does not start streaming and does not change device state
* Header defines structure of all subsequent data lines
* Header field names must match canonical channel names defined in `channel-names.md`
* Header fields must correspond exactly to channels declared in driver capabilities
* Header fields must match subsequent `DAT` lines exactly, in both count and order

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

For `READ`:

* Device takes one fresh sample
* Device returns exactly one `DAT,...` line matching the current header
* Device must not enter continuous streaming mode
* Device must not emit additional `DAT` lines unless another `READ` is received

For `START` / `STOP`:

* Streaming devices use `START` to begin continuous output
* Streaming devices use `STOP` to end continuous output
* Polled-only devices may return `ERR UNKNOWN_CMD` for `START` and `STOP`

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
  * `READ`

---

## Code Structure

### Setup

* initialize serial communication
* initialize sensors
* initialize required interfaces

### Loop

* read and process serial commands
* for streaming devices, send data when running
* for polled devices, send data only when `READ` is handled
* use non-blocking timing

### Helper Functions

* `handleCommand(...)`
* `checkSerial()`
* `sendHeader()`
* `sendInfo()`
* `sendStatus()`
* `sendData()`
* `readSingleSample()` for polled devices

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
