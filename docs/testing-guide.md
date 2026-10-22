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

- `null` read-only values render as `—`; unassigned editable values are empty
  frames with a visible label, not `—`; saved editable values are unframed at
  rest
- inline edits show no visible Edit/Save/Cancel; a changed draft is amber,
  turns green only after a confirmed server save, then white; Escape and an
  unchanged Enter write nothing; refusals and uncertain outcomes never show
  green or the old value as saved
- a featured field (currently Name and Location) is not repeated in its section
- the Device settings table keeps UID first and read-only (visible while
  editing on phones), offers no Add/Archive, saves directly with Save (no
  Review/Confirm/Back), old Review/Back submissions from a form opened before
  that change do not write (an explicit old Confirm still saves), and shows the
  same values as the dashboard
- card order: Name, Location, then featured measurements in configured order,
  one measurement per row with its threshold/range beside it (never two
  unrelated measurements; number with unit), then each featured switch as a
  full-width row, then full-width group folders; a featured field is moved, not
  repeated, and a folder whose fields are all featured stays present and empty;
  no invented explanatory text or tooltips; amber only for warning/disabled
  protection, red for active alarm/fault, every colour with a state label
- example or project-specific providers: their settings round-trip between the
  card and Device settings with revision checks; every submitted field is
  validated before any write; a partial save says what was and was not saved;
  unavailable storage is reported, never shown as defaults; real devices are
  never reinterpreted as examples
- unavailable/error nodes show red status
- stale nodes do not display old metric values as current
- `last_seen` appears separately when shown

## Isolated and clean Linux validation

Follow [reproducible development and Linux validation](reproducible-development.md)
for repository-owned environments, Dev Container applicability, CI parity and the
separation between portable software tests and physical hardware evidence.
