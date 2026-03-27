# Pi Driver Instructions

A Bard Box Pi driver is a Python module that reads data from a device node (over serial or USB) and makes it available to the FastAPI app.

## Driver location

Each driver lives in `drivers/<driver_name>/`:

```
drivers/
  gt521s_driver/
    gt521s_driver.py   ← driver module
    README.md          ← sensor description, channels, serial config
```

## Driver interface

Every driver exposes:

- A class or set of functions to open the serial connection
- A reader loop (typically in a background thread) that parses incoming lines
- Shared state: `latest_reading`, `session_data`, `run_active`
- Start/stop methods callable from FastAPI endpoints

## Serial configuration

Drivers must document:
- Serial port path (by-id path preferred for stability)
- Baud rate
- Line termination expected (`\r`, `\n`, or `\r\n`)

## Adding a new driver

1. Create `drivers/<driver_name>/`
2. Copy the structure from an existing driver (e.g. `gt521s_driver`)
3. Implement the reader loop and shared state
4. Write `README.md` with sensor info and channel map
5. Integrate into the FastAPI `main.py`

## Checklist before deploying

- [ ] Driver reads from correct serial port
- [ ] Parses all expected channels correctly
- [ ] Handles serial errors gracefully (timeouts, disconnects)
- [ ] Thread-safe access to shared state (use `threading.Lock`)
- [ ] Integrated with `/gt/start`, `/gt/stop`, `/gt/latest`, `/state` endpoints
- [ ] `README.md` written with channel map and serial config
