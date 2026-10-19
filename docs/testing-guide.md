# Testing Guide

BardBox tests should prove both driver contracts and runtime freshness behavior.

The coverage below is the legacy reading projection. The
[ingestion contract](ingestion-contract.md) target (per-channel faults, unknown
time) needs its own acceptance scenarios listed there. Timestamps are UTC with an
explicit `Z` or offset. The repository's own legacy driver, contract test and
fixtures do not yet meet this guide; see
[bardbox#49](https://github.com/bardphysicslab/bardbox/issues/49).

## Required Contract Coverage

Drivers and template apps should test:

- fresh reading returns `ok`
- no device response returns `node_unavailable`
- malformed/unparseable response returns `error`
- stale timeout returns `stale` or `node_unavailable` according to transport model
- stale/unavailable/error readings have `null` data values
- APIs do not present cached readings as live after communication failure
- every declared channel appears in `data`
- timestamps are UTC ISO 8601

## Fixture Tests

Driver-specific tests should include raw protocol samples and expected
normalized readings. Fixture tests are the right place to validate parsing,
channel normalization, and error handling without live hardware.

## Dashboard Checks

Dashboard checks should verify:

- `null` values render as `—`
- unavailable/error nodes show red status
- stale nodes do not display old metric values as current
- `last_seen` appears separately when shown

## Isolated and clean Linux validation

Follow [reproducible development and Linux validation](reproducible-development.md)
for repository-owned environments, Dev Container applicability, CI parity and the
separation between portable software tests and physical hardware evidence.
