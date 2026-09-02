# BardBox Transport Recovery Standard

## Purpose

BardBox deployments are expected to run unattended and must recover cleanly from routine transport and device faults. A transport/session object is disposable runtime state; the configured device identity and safety policy are persistent.

This standard applies to directly attached devices and buses such as USB serial, UART/RS-232/RS-485, I2C, and similar local transports. Device-specific drivers may add stricter recovery behavior, especially for actuators or programmable loads.

## Common Recovery Model

Drivers that own transport state should follow this sequence when communication fails:

1. classify the failure as transport/device availability rather than valid measurement data;
2. invalidate the current transport/session object;
3. close/release it if possible;
4. never reuse an object known to have failed;
5. retry only according to bounded, operation-specific policy;
6. preserve the last valid reading as historical/stale state rather than synthesizing zeros;
7. report recovery state separately from measurement values;
8. require a new successful communication before returning the source to `ok`.

Recovery must not create concurrent access to a single physical transport. Polling, reconnect logic, user commands, and sweeps/control operations must share the same serialization/locking boundary.

## USB / Serial Recovery

Persistent serial handles may become invalid after device power cycles, USB unplug/replug, host USB resets, CH340/FTDI re-enumeration, or operating-system transport faults. Typical symptoms include write/read failures such as macOS `OSError: [Errno 6] Device not configured`.

For a serial transport failure:

- close the serial object if possible;
- discard the cached serial object unconditionally;
- mark the transport disconnected/unavailable;
- on the next operation, create a fresh serial connection rather than reopening/reusing the failed object;
- use bounded reconnect attempts/backoff rather than a busy loop.

Read-only/idempotent operations may reconnect and retry once when safe. State-changing commands must not be blindly replayed after an ambiguous transport failure.

Where practical, drivers should verify device identity after reconnect (for example with an instrument identity query) before accepting the connection as the configured source. Port rediscovery by stable USB identity/serial number may be added when device paths are not stable, but simple close/discard/reopen of the configured port is the required baseline behavior.

## I2C Recovery

I2C failures are different from stale serial handles because the sensor or bus itself may be wedged. A driver should treat repeated I2C read/write failure as a recoverable device/bus fault rather than returning invalid or zero-valued measurements.

Recovery should proceed in bounded stages supported by the platform/device:

1. retry the failed transaction only a small bounded number of times;
2. recreate/reinitialize the sensor driver object;
3. recreate/reinitialize the I2C bus object where supported;
4. use a hardware reset or controllable sensor power-cycle when available and explicitly designed for;
5. if recovery fails, remain unavailable and retry later with backoff.

A device should not be marked healthy again until at least one fresh, validated reading succeeds. Projects may require multiple sane readings before restoring `ok` for sensors known to produce invalid values immediately after reset.

Drivers must not synthesize zeros for failed I2C reads. The last valid measurement may be retained for diagnostics/history but must not be presented as a fresh reading.

## Safety-Critical / State-Changing Devices

Automatic communication recovery does not imply automatic experiment or actuator recovery.

For devices that can energize, switch, heat, move, charge, discharge, or otherwise change physical state:

- never automatically replay an enable/start command after ambiguous communication loss;
- if an OFF/disable command fails, do not claim OFF unless the state is subsequently confirmed;
- latch an explicit unconfirmed/disconnected safety state when the physical state cannot be verified;
- after reconnect, establish a known safe state before allowing another explicit activation;
- do not automatically resume fixed-load, sweep, continuous-run, or equivalent active modes after reconnect.

Device-specific drivers/controllers may impose stronger rules.

## Availability and UI Semantics

Transport recovery state is distinct from measurement validity. Runtime/UI layers should be able to distinguish at least:

- connected
- disconnected
- reconnecting
- fault / recovery failed

These states complement the normalized reading statuses in `data-source-drivers.md`; they do not replace them.

A transport outage must not be represented by zero-valued sensor data. If cached data is shown for context, it must be clearly stale/historical.

Raw operating-system error text should be retained in logs/diagnostics, while user-facing messages should prefer concise descriptions such as `USB disconnected`, `Reconnecting`, or `I2C sensor unavailable`.

## Testing Requirements

Drivers or transport helpers that implement recovery should include deterministic tests for the relevant failure modes. Depending on transport/device this includes:

- stale handle/session is discarded after failure;
- next operation creates a fresh connection/session;
- bounded retry behavior;
- successful recovery returns fresh validated data;
- failed recovery does not synthesize zeros;
- last valid reading is not misrepresented as live;
- concurrent poll/reconnect/control access is prevented;
- state-changing commands are not blindly replayed;
- safety-critical devices require a known safe state after ambiguous disconnect;
- I2C driver/bus reinitialization behavior where implemented.

Use fake transports/clocks/devices for recovery timing tests rather than relying on real sleeps or physical disconnects in the automated suite.
