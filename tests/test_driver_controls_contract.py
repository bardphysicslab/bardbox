"""Contract examples for optional BardBox state-changing driver controls."""

from __future__ import annotations

from typing import Any

import pytest


VALID_CONTROL_OUTCOMES = {"applied", "rejected", "failed", "state_unknown"}


def assert_control_outcome(result: dict[str, Any], expected: str) -> None:
    assert set(result) >= {"outcome", "message"}
    assert result["outcome"] in VALID_CONTROL_OUTCOMES
    assert result["outcome"] == expected
    assert isinstance(result["message"], str)
    assert result["message"]


class MinimalReadOnlyDriver:
    def get_info(self) -> dict[str, str]:
        return {"uid": "bb-tst-ins-001", "transport": "serial", "protocol": "fake"}

    def get_capabilities(self) -> dict[str, Any]:
        return {"channels": {"voltage_v": {"label": "Voltage", "unit": "V"}}}

    def get_reading(self) -> dict[str, Any]:
        return {
            "uid": "bb-tst-ins-001",
            "timestamp": "2026-09-03T12:00:00Z",
            "status": "ok",
            "message": "Fresh valid reading",
            "data": {"voltage_v": 12.0},
            "extended": {},
            "raw": None,
        }


class FakeControllableLoad(MinimalReadOnlyDriver):
    def __init__(self, behavior: str = "applied") -> None:
        self.behavior = behavior
        self.device_interactions = 0
        self.applied_current_a = 0.0

    def get_capabilities(self) -> dict[str, Any]:
        capabilities = super().get_capabilities()
        capabilities["controls"] = {
            "load_current_setpoint": {
                "value_type": "number",
                "unit": "A",
                "minimum": 0.0,
                "maximum": 2.0,
                "readback": True,
                "safety": "energizing",
            }
        }
        return capabilities

    def set_load_current(self, current_a: float) -> dict[str, Any]:
        declaration = self.get_capabilities()["controls"]["load_current_setpoint"]
        if not isinstance(current_a, (int, float)) or isinstance(current_a, bool):
            return {"outcome": "rejected", "message": "Current must be numeric"}
        if not declaration["minimum"] <= current_a <= declaration["maximum"]:
            return {"outcome": "rejected", "message": "Current is outside declared bounds"}
        if self.behavior == "failed":
            return {"outcome": "failed", "message": "Transport was unavailable before transmission"}

        self.device_interactions += 1
        if self.behavior == "rejected":
            return {"outcome": "rejected", "message": "Device explicitly rejected the request"}
        if self.behavior == "state_unknown":
            # Simulates loss after transmission. The driver does not replay.
            return {"outcome": "state_unknown", "message": "Readback was unavailable after transmission"}

        self.applied_current_a = float(current_a)
        return {
            "outcome": "applied",
            "message": "Requested current was confirmed by readback",
            "readback": {"value": self.applied_current_a, "unit": "A"},
        }


def test_driver_without_writable_controls_remains_valid() -> None:
    driver = MinimalReadOnlyDriver()

    assert "controls" not in driver.get_capabilities()
    assert set(driver.get_info()) >= {"uid", "transport", "protocol"}
    assert driver.get_reading()["status"] == "ok"


def test_writable_capability_can_declare_validation_and_safety_metadata() -> None:
    control = FakeControllableLoad().get_capabilities()["controls"]["load_current_setpoint"]

    assert control == {
        "value_type": "number",
        "unit": "A",
        "minimum": 0.0,
        "maximum": 2.0,
        "readback": True,
        "safety": "energizing",
    }


def test_verified_control_reports_applied() -> None:
    driver = FakeControllableLoad()

    result = driver.set_load_current(1.0)

    assert_control_outcome(result, "applied")
    assert result["readback"] == {"value": 1.0, "unit": "A"}
    assert driver.device_interactions == 1


@pytest.mark.parametrize(
    ("behavior", "expected", "expected_interactions"),
    [("rejected", "rejected", 1), ("failed", "failed", 0)],
)
def test_known_control_failures_have_unambiguous_outcomes(
    behavior: str, expected: str, expected_interactions: int
) -> None:
    driver = FakeControllableLoad(behavior)

    result = driver.set_load_current(1.0)

    assert_control_outcome(result, expected)
    assert driver.device_interactions == expected_interactions


def test_ambiguous_post_command_loss_reports_unknown_without_replay() -> None:
    driver = FakeControllableLoad("state_unknown")

    result = driver.set_load_current(1.0)

    assert_control_outcome(result, "state_unknown")
    assert driver.device_interactions == 1


@pytest.mark.parametrize("invalid_value", [-0.1, 2.1, "1.0", True])
def test_invalid_control_value_is_rejected_before_device_interaction(invalid_value: object) -> None:
    driver = FakeControllableLoad()

    result = driver.set_load_current(invalid_value)  # type: ignore[arg-type]

    assert_control_outcome(result, "rejected")
    assert driver.device_interactions == 0


def test_existing_required_driver_methods_are_unchanged() -> None:
    driver = FakeControllableLoad()

    assert set(driver.get_info()) == {"uid", "transport", "protocol"}
    assert driver.get_capabilities()["channels"] == {
        "voltage_v": {"label": "Voltage", "unit": "V"}
    }
    assert driver.get_reading()["data"] == {"voltage_v": 12.0}
