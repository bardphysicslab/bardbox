"""
tests/test_driver_contract.py

Generic Bard Box driver compliance test suite.

This suite validates that a driver correctly implements the Bard Box driver
interface defined in docs/pi-driver-instructions.md. It is hardware-agnostic
and does not require a live device.

-----------------------------------------------------------------------
Driver discovery (resolved in this order)
-----------------------------------------------------------------------

1. BARDBOX_DRIVER env var — explicit module path and class name:

       BARDBOX_DRIVER=drivers.gt521s_driver.gt521s_driver:GT521SDriver

   Format: <importable.module.path>:<ClassName>
   ClassName defaults to SensorDriver if the colon and class are omitted.

2. BARDBOX_DRIVER_NAME env var — key into the registry below:

       BARDBOX_DRIVER_NAME=gt521s pytest tests/test_driver_contract.py

3. First entry in DRIVER_REGISTRY (default fallback).

-----------------------------------------------------------------------
Registry format
-----------------------------------------------------------------------

Each entry may supply:

  "module"   str   importable module path (required)
  "class"    str   class name (default: SensorDriver)
  "kwargs"   dict  passed to the constructor (default: {})
  "factory"  callable  used instead of cls(**kwargs) when present

-----------------------------------------------------------------------
Running
-----------------------------------------------------------------------

   # default (first registry entry)
   pytest tests/test_driver_contract.py

   # named registry entry
   BARDBOX_DRIVER_NAME=gt521s pytest tests/test_driver_contract.py

   # arbitrary driver outside the registry
   BARDBOX_DRIVER=my.module.path:MyDriver pytest tests/test_driver_contract.py

   # verbose
   pytest tests/test_driver_contract.py -v

See docs/testing-guide.md for full usage instructions.
"""

import importlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

# ---------------------------------------------------------------------------
# Driver registry
# ---------------------------------------------------------------------------

DRIVER_REGISTRY: Dict[str, Dict[str, Any]] = {
    "gt521s": {
        "module": "drivers.gt521s_driver.gt521s_driver",
        "class": "GT521SDriver",
        # "kwargs": {},
        # "factory": None,
    },
}

# ---------------------------------------------------------------------------
# Contract constants
# ---------------------------------------------------------------------------

# Physical connection descriptors — valid values for get_info()["transport"]
VALID_TRANSPORTS = {"serial", "i2c", "usb", "spi", "uart", "can"}

# Physical bus names that must NOT appear in get_info()["protocol"]
PHYSICAL_BUS_NAMES = {"serial", "i2c", "spi", "usb", "uart", "can", "rs485", "rs232"}

# Valid values for get_reading()["status"]
VALID_STATUSES = {"ok", "stale", "error"}

# ISO 8601 prefix pattern — YYYY-MM-DDTHH:MM:SS or with space separator
_ISO_8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")

# Maximum acceptable size for raw payloads
_RAW_MAX_STR_LEN = 10_000
_RAW_MAX_LIST_LEN = 1_000

# Required top-level keys in each interface method's return value
_INFO_REQUIRED_KEYS = {"uid", "transport", "protocol"}
_CAPS_REQUIRED_KEYS = {"channels"}
_READING_REQUIRED_KEYS = {"uid", "timestamp", "status", "data", "extended", "raw"}

# Required keys in each channel entry inside get_capabilities()["channels"]
_CHANNEL_ENTRY_REQUIRED_KEYS = {"channel", "unit"}

# ---------------------------------------------------------------------------
# Driver discovery
# ---------------------------------------------------------------------------

def _repo_root() -> Path:
    return Path(__file__).parent.parent


def _ensure_repo_on_path():
    root = str(_repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)


def _load_driver():
    _ensure_repo_on_path()

    env = os.environ.get("BARDBOX_DRIVER")
    if env:
        if ":" in env:
            module_path, class_name = env.rsplit(":", 1)
        else:
            module_path, class_name = env, "SensorDriver"
        mod = importlib.import_module(module_path)
        return getattr(mod, class_name)()

    name = os.environ.get("BARDBOX_DRIVER_NAME") or next(iter(DRIVER_REGISTRY))
    if name not in DRIVER_REGISTRY:
        raise KeyError(
            f"Driver '{name}' not found in DRIVER_REGISTRY. "
            f"Available: {sorted(DRIVER_REGISTRY)}"
        )
    entry = DRIVER_REGISTRY[name]
    factory = entry.get("factory")
    if factory:
        return factory()
    mod = importlib.import_module(entry["module"])
    cls = getattr(mod, entry.get("class", "SensorDriver"))
    return cls(**entry.get("kwargs", {}))


# ---------------------------------------------------------------------------
# Pytest fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def driver():
    return _load_driver()


@pytest.fixture(scope="module")
def info(driver):
    return driver.get_info()


@pytest.fixture(scope="module")
def capabilities(driver):
    return driver.get_capabilities()


@pytest.fixture(scope="module")
def reading(driver):
    return driver.get_reading()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _declared_channel_names(capabilities: dict) -> set:
    """Return the set of channel names declared in get_capabilities()."""
    return {ch["channel"] for ch in capabilities.get("channels", [])
            if "channel" in ch}


def _skip_if_no_reading(reading):
    if reading is None:
        pytest.skip(
            "get_reading() returned None — driver has not yet received data. "
            "Run against a live or simulated device to exercise reading tests."
        )


# ---------------------------------------------------------------------------
# TestGetInfo
# ---------------------------------------------------------------------------

class TestGetInfo:
    """Validates the contract for get_info()."""

    def test_method_exists(self, driver):
        assert callable(getattr(driver, "get_info", None)), \
            "Driver must implement get_info()"

    def test_returns_dict(self, info):
        assert isinstance(info, dict), \
            f"get_info() must return a dict, got {type(info).__name__}"

    def test_required_keys_present(self, info):
        missing = _INFO_REQUIRED_KEYS - info.keys()
        assert not missing, \
            f"get_info() is missing required keys: {sorted(missing)}"

    def test_uid_is_nonempty_string(self, info):
        uid = info.get("uid")
        assert isinstance(uid, str) and uid.strip(), \
            f"get_info()['uid'] must be a non-empty string, got: {uid!r}"

    def test_transport_is_physical_descriptor(self, info):
        transport = str(info.get("transport", "")).lower()
        assert transport in VALID_TRANSPORTS, (
            f"get_info()['transport'] must be a physical connection descriptor "
            f"(one of {sorted(VALID_TRANSPORTS)}), got: {transport!r}. "
            f"transport describes how the sensor is physically connected to the Pi."
        )

    def test_protocol_is_nonempty_string(self, info):
        protocol = info.get("protocol")
        assert isinstance(protocol, str) and protocol.strip(), \
            f"get_info()['protocol'] must be a non-empty string, got: {protocol!r}"

    def test_protocol_is_not_a_physical_bus_name(self, info):
        protocol = str(info.get("protocol", "")).lower()
        assert protocol not in PHYSICAL_BUS_NAMES, (
            f"get_info()['protocol'] must be a logical descriptor "
            f"(e.g. 'vendor', 'bardbox', 'modbus', 'nmea'), "
            f"not a physical bus name. Got: {protocol!r}. "
            f"Physical bus names belong in 'transport', not 'protocol'."
        )


# ---------------------------------------------------------------------------
# TestGetCapabilities
# ---------------------------------------------------------------------------

class TestGetCapabilities:
    """Validates the contract for get_capabilities()."""

    def test_method_exists(self, driver):
        assert callable(getattr(driver, "get_capabilities", None)), \
            "Driver must implement get_capabilities()"

    def test_returns_dict(self, capabilities):
        assert isinstance(capabilities, dict), \
            f"get_capabilities() must return a dict, got {type(capabilities).__name__}"

    def test_required_keys_present(self, capabilities):
        missing = _CAPS_REQUIRED_KEYS - capabilities.keys()
        assert not missing, \
            f"get_capabilities() is missing required keys: {sorted(missing)}"

    def test_channels_is_a_list(self, capabilities):
        channels = capabilities.get("channels")
        assert isinstance(channels, list), \
            f"get_capabilities()['channels'] must be a list, got {type(channels).__name__}"

    def test_channels_is_not_empty(self, capabilities):
        assert len(capabilities.get("channels", [])) > 0, \
            "get_capabilities()['channels'] must declare at least one channel"

    def test_each_channel_entry_has_required_keys(self, capabilities):
        for i, ch in enumerate(capabilities.get("channels", [])):
            missing = _CHANNEL_ENTRY_REQUIRED_KEYS - ch.keys()
            assert not missing, (
                f"Channel entry [{i}] {ch!r} is missing required keys: "
                f"{sorted(missing)}. Each channel must have 'channel' and 'unit'."
            )

    def test_channel_names_are_nonempty_strings(self, capabilities):
        for ch in capabilities.get("channels", []):
            name = ch.get("channel")
            assert isinstance(name, str) and name.strip(), \
                f"Channel 'channel' field must be a non-empty string, got: {name!r}"

    def test_extended_fields_is_list_if_declared(self, capabilities):
        ef = capabilities.get("extended_fields")
        if ef is not None:
            assert isinstance(ef, list), (
                f"get_capabilities()['extended_fields'] must be a list "
                f"if present, got: {type(ef).__name__}"
            )


# ---------------------------------------------------------------------------
# TestGetReading
# ---------------------------------------------------------------------------

class TestGetReading:
    """Validates the contract for get_reading()."""

    def test_method_exists(self, driver):
        assert callable(getattr(driver, "get_reading", None)), \
            "Driver must implement get_reading()"

    def test_returns_dict_or_none(self, reading):
        assert reading is None or isinstance(reading, dict), \
            f"get_reading() must return a dict or None, got {type(reading).__name__}"

    def test_required_keys_present(self, reading):
        _skip_if_no_reading(reading)
        missing = _READING_REQUIRED_KEYS - reading.keys()
        assert not missing, \
            f"get_reading() is missing required keys: {sorted(missing)}"

    def test_uid_matches_get_info(self, reading, info):
        _skip_if_no_reading(reading)
        assert reading["uid"] == info["uid"], (
            f"get_reading()['uid'] ({reading['uid']!r}) must match "
            f"get_info()['uid'] ({info['uid']!r})"
        )

    def test_timestamp_is_iso8601(self, reading):
        _skip_if_no_reading(reading)
        ts = str(reading.get("timestamp", ""))
        assert _ISO_8601_RE.match(ts), (
            f"get_reading()['timestamp'] must be valid ISO 8601 "
            f"(e.g. '2026-03-30T14:32:01'), got: {ts!r}"
        )

    def test_status_is_valid(self, reading):
        _skip_if_no_reading(reading)
        status = reading.get("status")
        assert status in VALID_STATUSES, (
            f"get_reading()['status'] must be one of {sorted(VALID_STATUSES)}, "
            f"got: {status!r}"
        )

    def test_data_is_a_dict(self, reading):
        _skip_if_no_reading(reading)
        assert isinstance(reading.get("data"), dict), \
            "get_reading()['data'] must be a dict"

    def test_data_keys_exactly_match_declared_channels(self, reading, capabilities):
        _skip_if_no_reading(reading)
        declared = _declared_channel_names(capabilities)
        actual = set(reading.get("data", {}).keys())
        extra = actual - declared
        assert not extra, (
            f"get_reading()['data'] contains keys not declared in "
            f"get_capabilities()['channels']: {sorted(extra)}. "
            f"No vendor or raw field names may appear in normalized data."
        )

    def test_all_declared_channels_present_in_data(self, reading, capabilities):
        _skip_if_no_reading(reading)
        declared = _declared_channel_names(capabilities)
        actual = set(reading.get("data", {}).keys())
        missing = declared - actual
        assert not missing, (
            f"get_reading()['data'] is missing declared channels: {sorted(missing)}. "
            f"Every declared channel must appear in data (null is acceptable "
            f"when temporarily unavailable)."
        )

    def test_extended_is_a_dict(self, reading):
        _skip_if_no_reading(reading)
        extended = reading.get("extended")
        assert isinstance(extended, dict), (
            f"get_reading()['extended'] must be a dict (use {{}} if empty — "
            f"the key must always be present). Got: {type(extended).__name__}"
        )

    def test_all_declared_extended_fields_present(self, reading, capabilities):
        _skip_if_no_reading(reading)
        ef_list = capabilities.get("extended_fields") or []
        if not ef_list:
            return
        extended = reading.get("extended", {})
        for entry in ef_list:
            field_name = entry if isinstance(entry, str) else entry.get("name", "")
            assert field_name in extended, (
                f"Extended field {field_name!r} is declared in get_capabilities() "
                f"but missing from get_reading()['extended']. "
                f"Use null if temporarily unavailable."
            )

    def test_raw_is_null_or_bounded(self, reading):
        _skip_if_no_reading(reading)
        raw = reading.get("raw")
        if raw is None:
            return  # null is always acceptable
        if isinstance(raw, str):
            assert len(raw) < _RAW_MAX_STR_LEN, (
                f"get_reading()['raw'] string is {len(raw)} characters, "
                f"exceeds limit of {_RAW_MAX_STR_LEN}. "
                f"Full log dumps must not be passed through raw."
            )
        elif isinstance(raw, list):
            assert len(raw) < _RAW_MAX_LIST_LEN, (
                f"get_reading()['raw'] list has {len(raw)} entries, "
                f"exceeds limit of {_RAW_MAX_LIST_LEN}. "
                f"Unbounded log lists are not acceptable."
            )
        else:
            # dict or other structured object — check serialized size
            serialized = json.dumps(raw)
            assert len(serialized) < _RAW_MAX_STR_LEN, (
                f"get_reading()['raw'] serializes to {len(serialized)} characters, "
                f"exceeds limit of {_RAW_MAX_STR_LEN}."
            )
