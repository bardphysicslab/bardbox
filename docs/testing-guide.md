# Testing Guide

## Overview

Bard Box uses a two-layer test approach for drivers:

1. **Driver contract tests** — hardware-agnostic compliance checks that every driver must pass before merge. These live in `tests/test_driver_contract.py` and are the gate for all driver PRs.

2. **Fixture tests** — driver-specific unit tests that validate parsing and normalization logic against sample data. These live alongside the fixture files in `tests/fixtures/`.

---

## Layer 1: Driver Contract Tests

The contract test suite (`tests/test_driver_contract.py`) validates that a driver correctly implements the Bard Box driver interface defined in `docs/pi-driver-instructions.md`. It is hardware-agnostic and does not require a live device.

### What it checks

- `get_info()` returns a dict with `uid`, `transport`, `protocol`
- `transport` is a valid physical connection descriptor (`serial`, `i2c`, `usb`, `spi`, `uart`, `can`)
- `protocol` is a logical name — not a physical bus name
- `get_capabilities()` returns a dict with a non-empty `channels` list
- Each channel entry has `channel` and `unit` keys
- `get_reading()` returns a dict or `None`
- When a reading is available: required keys are present, `uid` matches `get_info()`, timestamp is ISO 8601, status is valid, `data` keys exactly match declared channels, `extended` is always a dict, `raw` is bounded

### Running

```bash
# default driver (first entry in DRIVER_REGISTRY)
pytest tests/test_driver_contract.py

# named registry entry
BARDBOX_DRIVER_NAME=gt521s pytest tests/test_driver_contract.py

# arbitrary driver outside the registry
BARDBOX_DRIVER=my.module.path:MyDriver pytest tests/test_driver_contract.py

# verbose
pytest tests/test_driver_contract.py -v
```

### Driver discovery order

1. `BARDBOX_DRIVER` env var — full module path and class name:
   ```
   BARDBOX_DRIVER=drivers.gt521s_driver.gt521s_driver:GT521SDriver
   ```
2. `BARDBOX_DRIVER_NAME` env var — key into `DRIVER_REGISTRY` in the test file
3. First entry in `DRIVER_REGISTRY` (default fallback)

### When `get_reading()` returns None

Tests that require a reading are automatically skipped with a clear message. This is expected when running without a live or simulated device. The contract test is still considered passing — `None` is a valid return when no data has been received yet.

To exercise reading tests, run against a live device or write a mock driver that returns a static reading.

---

## Layer 2: Fixture Tests

Fixture files live in `tests/fixtures/<driver>/` and contain:

- **Sample input** — raw output from the device (serial CSV, stream data, register dumps)
- **Expected reading** — the normalized `get_reading()` dict the driver should produce

These tests are written per-driver and validate that parsing and normalization logic is correct without hardware.

### Fixture file locations

```
tests/fixtures/
  gt521s/
    sample_output.csv          # raw GT-521S serial output lines
    expected_reading.json      # expected normalized reading from the last line
  bme280/
    expected_reading.json      # expected normalized reading
  bardbox_node/
    sample_stream.txt          # sample Bard Box serial stream (HDR + INFO + DAT lines)
    expected_reading.json      # expected normalized reading from the last DAT line
```

### Adding fixture tests for a new driver

1. Add sample input and expected output files to `tests/fixtures/<source_type>/`
2. Write a test file `tests/test_<source_type>_driver.py` that:
   - Reads sample input from the fixture file
   - Calls the driver's parsing logic directly (no serial port needed)
   - Asserts the output matches `expected_reading.json`
3. Fixture tests do not replace contract tests — both must pass

---

## Merge Requirements

Every driver PR must pass the contract test suite before merge. This means:

- `pytest tests/test_driver_contract.py` must pass with no failures (skipped reading tests are acceptable when no device is available)
- The driver must be added to `DRIVER_REGISTRY` in `test_driver_contract.py`

Fixture tests are strongly recommended but not currently required for merge.

---

## Note for Students

The contract test suite was designed to be the first check you run on a new driver. If your driver fails contract tests, fix those before writing fixture tests. Contract failures mean the backend will not be able to consume your driver's output.

If `get_reading()` returns `None` during contract testing, that is expected — it means no serial data has been received. The reading tests will be skipped automatically. You can verify reading structure by running against a live device or by writing a simple mock driver.
