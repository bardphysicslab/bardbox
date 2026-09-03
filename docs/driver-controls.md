# BardBox Optional Driver Controls

## Scope

BardBox drivers may expose state-changing controls in addition to the required
`get_info()`, `get_capabilities()`, and `get_reading()` interface. Controls are
optional: a read-only driver remains fully conformant without them.

This standard covers the boundary between an application and a controllable
driver. It does not standardize vendor commands or every laboratory-instrument
operation. Vendor protocols, transports, command formatting, parsing, locking,
acknowledgments, readback, retries, and device quirks remain inside the driver.

## Capability declaration

When a driver exposes writable controls, `get_capabilities()` should declare
them under a `controls` mapping keyed by stable, semantic control names. Names
describe the operation rather than vendor syntax or a particular model.

The declaration must provide enough metadata for the application to validate a
request before device interaction. Where applicable, this includes:

- value type;
- physical unit;
- minimum and maximum values, or an allowed enumeration;
- whether resulting state can be read back; and
- safety classification, or equivalent metadata indicating that ambiguous
  execution requires conservative handling.

This document intentionally does not require one exhaustive control-entry
schema. Drivers may add device-independent metadata needed by their domain.
Applications must not infer missing bounds, units, readback, or safety
properties. Such unknowns must be handled conservatively.

Example:

```python
{
    "channels": { ... },
    "controls": {
        "load_current_setpoint": {
            "value_type": "number",
            "unit": "A",
            "minimum": 0.0,
            "maximum": 2.0,
            "readback": True,
            "safety": "energizing",
        },
        "load_enabled": {
            "value_type": "boolean",
            "readback": True,
            "safety": "energizing",
        },
    },
}
```

The example names are generic load functions, not ET5406A commands or a
required ontology for unrelated devices.

## Named semantic operations

Applications invoke explicit named driver operations. The exact Python method
organization is implementation-defined. Applications must not:

- construct or pass vendor commands;
- expose arbitrary raw-command passthrough;
- depend on serial, USB, VISA, SDK, or other transport syntax; or
- interpret vendor-specific acknowledgments.

An application must validate a requested value against declared type, range,
or enumeration metadata before invoking a control when that metadata is
available. The driver must also validate values before unsafe device
interaction; application validation is not a substitute for driver validation.

## Normalized outcome

Every named state-changing operation returns a mapping containing at least:

```python
{
    "outcome": "applied",
    "message": "Requested state was verified",
}
```

`outcome` has exactly these meanings:

- `applied` — the driver has sufficient evidence that the requested state
  change occurred.
- `rejected` — the device or driver explicitly refused the request and the
  requested state was not applied.
- `failed` — the driver knows that the change did not occur or that the request
  could not be attempted.
- `state_unknown` — the operation may have occurred, but the resulting device
  state cannot be established safely.

`message` is a bounded human-readable explanation. Drivers may add normalized,
device-independent evidence such as verified readback. Applications must not
treat absence of an exception or transport write completion alone as
`applied`.

## Verification and ambiguous failure

An `applied` outcome requires appropriate evidence: an authoritative device
acknowledgment, state readback, or another documented device-appropriate
verification mechanism.

If communication fails after a command may have reached the device, the driver
must not blindly replay the command. It must invalidate and recreate transport
state as appropriate, re-identify the device when necessary, and query or read
back state when possible. If the resulting state cannot be established, it
returns `state_unknown`.

Read-only retry behavior must not automatically be reused for state-changing
operations. A retry is permitted only when the driver can establish that the
previous attempt was not applied, or when the requested operation is explicitly
defined as fail-safe and the bounded retry cannot create a more hazardous
state.

## Conservative recovery and safe state

Recovery must never implicitly transition a device into a more hazardous
energized or enabled state. After ambiguous failure, the driver must require a
fresh explicit application request before enabling or energizing an output
unless the resulting state has been positively established.

Cleanup or safe-off operations may use bounded retries only when the operation
is explicitly fail-safe and followed by confirmation where possible. If a safe
state cannot be confirmed, the driver returns `state_unknown`; the application
must be able to stop its workflow and require operator intervention.

## Ownership boundary

The application owns run and session IDs, sequencing, limits, timing, evidence,
verdicts, abort policy, and cleanup policy. The driver owns vendor protocol,
transport state, command formatting, parsing, locking, device-specific
acknowledgment and readback, bounded recovery, and normalized outcomes.

The hardware-sequenced `start_session()` exception in `session-model.md` remains
unchanged and does not transfer application session ownership to a driver.
