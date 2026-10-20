# Minimal BardBox firmware: base and serial module API

Status: design proposal, updated 2026-10-14. This specifies the generic implementation
requested by Kornelis; the C++ API below is not an existing library. No claim of
build, hardware validation, adopted protocol extension or deployment is made.
Canonical existing wire commands come from [Device instructions](device-instructions.md).
This proposal extends them; it does not silently substitute a project's protocol.
Tracker: [Serial and buffer API design](https://github.com/bardphysicslab/bardbox/issues/31); dependency: [USB work](https://github.com/bardphysicslab/firmware-tools/issues/5).
Entry point and flash layout: [firmware blueprint](firmware-blueprint.md); host-side
assembly: [USB flashing and provisioning](usb-provisioning-standard.md).

Shared guidance: bardphysicslab/engineering-standards@3bf9c600b35f73322e8f610baffec2b682bdcc77.
BardBox governing commit: da5132a648d21989a984e00fa1fd02760bcdf4f7.

## One serial module, two interfaces

External interface: documented single-line commands and responses over USB CDC
or UART. Internal interface: typed providers and settings operations used by the
application. One maintained module owns parsing, framing, mandatory fields,
validation and command dispatch. Projects register data providers; they do not
copy the parser or build response strings in main.cpp.

Every base includes serial communication and durable local device settings.
Persistent recording defaults ON for BardBox firmware, including serial-only
nodes ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991) item 6). Sensors, Wi-Fi connection, network delivery and OTA updater
are separately configured capabilities. USB is a transport for the serial contract;
serial command handling is separate from the bootloader's flashing transport.
The minimal test image can report no attached sensors without fabricated data.

## Required information and reading contract

| Command | Module owns | Application supplies |
| --- | --- | --- |
| INFO | OK INFO framing; uid from settings; fw from build metadata; registered sensor list; safe provisioning/capability state | Supported sensor names and optional typed status fields |
| HEADER | HDR framing, schema version, ordered column names | One stable reading schema with types and documented units |
| READ | DAT framing matching HEADER, or explicit ERR result | A bounded current reading snapshot and its validity result |

The existing forms remain OK INFO uid=... fw=... sensors=..., HDR,v1,...,
and DAT,... or ERR SENSOR_FAIL. Existing PING can return PONG. Project extensions
must not replace uid, fw or sensors, break framing, or expose secrets. New fields
are additive and follow an explicit version/compatibility rule. The base INFO
proposes unprovisioned state. Current provisioning uses the existing node UID
including its instance.

Device metadata in every record (accepted direction, [BB-006](DECISIONS.md),
[FW-MAC-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289751206), [FW-METADATA-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289777348),
October 20, 2026; this replaces the earlier blanket deferral of MAC reporting):
every measurement record on both serial and Wi-Fi/network delivery carries the
complete agreed non-secret device metadata, including UID, hardware MAC,
firmware and protocol versions, and time and validity fields as applicable. The
shared implementation supplies it; student code does not construct it. It never
includes credentials, tokens, passwords or private configuration, and absent
hardware identity, time or validity is never fabricated. UID and hardware MAC
are distinct. Neither alone is authentication, authorization or Registry
binding; Registry binding, including factory-base-MAC lookup, remains separate
future design.

Still open (design work):

- the exact bounded field set, representation and applicability, including
  explicit unavailable values;
- which hardware interface supplies the MAC, and its representation;
- versioned, backward-compatible placement on each interface, with host support.

Current versus target: today serial identity is in INFO and DAT follows
HEADER's reading schema, so UID and the complete metadata are not yet in every
serial reading. Existing network records carry UID, which is not the complete
target metadata. The existing INFO/HEADER/READ forms, payloads and deployed
parsers stay unchanged until a compatible versioned contract is designed,
adopted and tested. Any future omission or compression needs measured
size/throughput evidence and an explicit reviewed contract revision; no
transport silently drops metadata or substitutes a handshake.

INFO must work before registration. For the generic sensorless example,
uid=unassigned and sensors=none are explicit proposed sentinel values (not valid
assigned UIDs); state=unprovisioned identifies the condition. HEADER advertises
an empty schema; READ returns proposed ERR NO_SENSOR. An attached but failed
sensor returns ERR SENSOR_FAIL; a sample not yet ready returns proposed
ERR SAMPLE_NOT_READY. These additions must be adopted in the device standard
and tested in the host before being presented as established protocol behavior.

A schema specifies exact column order and types, and documents units separately.
A reading provider returns typed values in that order; it never returns arbitrary
CSV. The module checks count/type/bounds before writing a response. Rejected or
unavailable readings do not become a valid DAT line. Concurrent acquisition must
not modify a snapshot midway through serialization.

## Proposed beginner-facing application API

Updated October 14, 2026. This replaces the earlier four-argument
BardBoxSerial/provider sketch in this proposal. Names below are proposed,
not existing C++ symbols or a compiling implementation.

`BardBoxInterface device;` creates one beginner-facing facade (accepted name
`BardBoxInterface`, October 20, 2026, replacing the earlier `BardBoxDevice`
candidate; its methods and results remain proposed and unimplemented). It runs when
called, not automatically in a background task. The underlying serial module
owns framing/parsing; settings, acquisition scheduling, time, storage and
network delivery have their own owners. The facade wires their interfaces
without importing a project's main.cpp. USB CDC/UART remain injected Arduino
transports. Projects do not write serial response strings.

Accepted direction ([BB-005](DECISIONS.md), [FACADE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289589216),
October 20, 2026): the student uses only this one beginner-facing entry and
supplies named, typed readings with declared units. BardBox coordinates the
enabled Serial, Wi-Fi/network delivery and Buffer owners internally; the student
makes no separate Wi-Fi, uploader or Buffer service calls. Those owners stay
separate, sensor acquisition stays independent, and serial responsiveness stays
bounded, so network work must not monopolize serial service. How that internal
progress is scheduled, and the exact method names and signatures, remain
proposed; the facade is not implemented.

### Registration and startup

Register descriptors before begin. Registration returns explicit errors for
duplicate/reserved names, invalid units/types/bounds, oversized schemas and
unsafe fields. Descriptors are stable after successful begin.

| Proposed method | Meaning |
| --- | --- |
| setFirmwareVersion(version) | Required build metadata; the template rejects missing/placeholder versions at build time |
| addSensor(name) | Declare a project sensor; initialization/health are separate |
| addFloatField(name, unit) | Declare an ordered floating-point measurement |
| addIntegerField(name, unit) | Declare an ordered integer measurement |
| addBooleanField(name) | Declare an ordered boolean measurement |
| addInfoField(name, provider) | Register a bounded typed public status provider |
| addCapability(module) | Attach an optional capability's descriptors and handlers |
| begin(transport, settingsStore) | Validate the complete registration and load settings; return initialization result |

Firmware/protocol versions are distinct immutable build metadata. The shared
module supplies adopted protocol version, physical hardware identity and required
safe fields; device UID comes from settings, not an unexplained global.
Sensorless startup is valid and cannot manufacture a zero-valued measurement.

### Loop service and samples

| Proposed method | Meaning |
| --- | --- |
| poll(nowMs) | The one beginner service entry: bounded progress of the internal Serial, network delivery and Buffer owners, so the student makes no separate transport calls. It does not read sensors, set acquisition cadence or choose the averaging/reporting interval. "Poll" here means servicing those internal owners, not sensor polling; no rename is adopted. Keeping network work from blocking serial responsiveness is a target whose scheduling bound is unproven (see the network boundary below) |
| isStreaming() | Inspect START/STOP state; normally unnecessary for project code |
| newSample(acquiredAtMs) | Create a typed candidate snapshot at acquisition time |
| sample.set(field, value) | Supply a declared value; reject wrong types/unknown fields |
| sample.setTime(stamp) | Attach optional UTC/validity from the separate time module |
| publishSample(sample) | Validate the sample (required fields, declared types and rules, and the generic checks below), copy coherently and assign sample identity; return result |
| setReadingNotReady() | Explicit no-usable-sample state; also initial state |
| setSensorFailure(code) | Mark acquisition failed; older data is not silently served as current valid data |

READ returns the latest accepted valid snapshot immediately. Repeated reads
keep the same identity. Sample identity includes reboot distinction; sequence
alone is insufficient. Age and acquisition-time metadata must be specified
without silently changing existing HEADER/DAT compatibility. Publish is a
snapshot update, not automatic network upload or unsolicited serial output.
Late acquisition is distinct from a failed sensor: the application/driver owns
freshness policy and must be able to inspect sample age.

Generic sample checks (accepted direction, [FW-VALIDATION-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289980118),
October 20, 2026): when a sample is published, the shared facade checks numeric
finiteness, declared types, required fields and declared validity bounds, so
application code does not import `cmath`/`isfinite` or repeat those checks. It
reports explicit per-channel invalid or failed outcomes and keeps healthy
independent channels where the governing contracts permit. It never turns NaN,
missing or invalid values into zero, clamps them, or presents them as valid
measurements. Sensor reads, readiness, calibration and sensor-specific fault
detection stay with the sensor adapter and application. These checks do not
replace or weaken server validation or trust checks.

Open, and not settled by this direction:

- the exact result types and API;
- whether a record whose channels are all null is accepted;
- atomic versus partial (per-channel) publication;
- how per-channel outcomes reconcile with the whole-snapshot wording in this
  proposal: READ's single validity result, a rejected reading not becoming a
  valid DAT line, and the illustrative loop below treating any rejected publish
  as a sensor failure.

Until that reconciliation is designed, those statements describe the current
proposal and existing serial behavior, not a per-channel serial format.
Recommended choices for each of these are drafted below; none is adopted.

### Proposed student contract (draft for review)

October 20, 2026 draft for user and Codex review. Every name, type and choice
in this subsection is a recommendation, not an accepted API, and nothing here
is implemented. Library homes follow the
[accepted starting layout](firmware-blueprint.md#2-source-tree).

**Two student handoffs.** The facade (`BardBoxInterface`) takes two distinct
things from application code:

| Proposed call | Hands over | Goes to | Result |
| --- | --- | --- | --- |
| `publishSample(sample)` | Latest snapshot at acquisition time | Serial owner only (READ/streaming) | `PublishResult`: per-channel outcomes; replaces the latest snapshot |
| `submitRecord(record)` | Completed record the application built (raw or averaged, with window/method) | Buffer owner, then network owner | `SubmitResult`: rejection, or an admission ticket plus per-channel outcomes |
| `recordStatus(ticket)` | — (query only; no Buffer servicing) | Buffer owner | Pending, durable, uncertain or failed, with error code |

Publishing a sample never creates, queues or uploads a record, and submitting a
record never changes the latest snapshot. The facade stamps the agreed
every-record metadata ([BB-006](DECISIONS.md)) on both; application code never
builds it. Generic checks (finiteness, declared type, required field, declared
bounds) run in the facade on both handoffs.

**Per-channel outcomes.** Each declared channel ends in exactly one state:

| Outcome | Meaning | Value carried |
| --- | --- | --- |
| `valid` | Supplied and passed generic checks | The value |
| `missing` | Required channel not supplied | Null with code |
| `invalid` | Failed a generic check (`non_finite`, `invalid_type`, `out_of_bounds`) | Null with code |
| `failed` | Application marked it (`sample.setFailed(field, code)`), e.g. a sensor-specific fault | Null with the application's code |

A value of the wrong declared type is an `invalid_type` channel outcome, so one
mistyped channel never discards valid independent channels. An unknown field
name is recommended to be ignored for storage and reported as an
`unknown_field` error in the result, leaving declared channels unaffected (the
Reference Ingestion demo also ignores unknown channels). Whole rejection is
reserved for a structurally unusable sample or record: no successful `begin`,
no registered schema, a handle from another schema revision, or an oversized
envelope. No outcome turns a value into zero, clamps it or presents it as
valid.

**Durability outcomes for records.** Recommended states, extending the
proposed [Buffer ticket interface](firmware-buffer-api.md) (pending, durably
completed, failed) with one honest uncertain state; not adopted:

| State | Meaning |
| --- | --- |
| `rejected` | Not admitted (for example full queue, invalid size, exhausted sequence); nothing written; reason given |
| `pending` | Admitted, not yet durable; may be lost on restart or power loss |
| `durable` | Saved and indexed, as far as the storage adapter guarantees; physical power-loss behavior is unverified |
| `uncertain` | A write or metadata step failed after bytes may have been written; the record may or may not be recovered on rescan |
| `failed` | Not saved, only where the adapter can show nothing was written |

The [append reference](firmware-buffer-api.md#compatibility-and-cesh-evidence)
shows why `uncertain` is needed: a CESH metadata save that fails after the frame
is written returns `false`, yet the record may still be found on rescan.
`rejected` is decided before any storage I/O, and `failed` is used only where
the adapter can show nothing was written; any other write or metadata failure
is `uncertain`, which assumes no zero-byte write, dropped record or loss count.
Whether an `uncertain` or `failed` record is retried, preserved or counted as
lost is project policy and stays open (CESH's `windowsDropped` is its current
policy, not a shared rule). After `durable`, delivery belongs to the network
owner: server ACK removes the record; saturation eviction is counted data loss,
never an ACK. Students query states and diagnostics; they make no delivery or
Buffer servicing calls.

**Internal owners and the network boundary.** Serial (`BardBoxSerial`), network
delivery (`BardBoxNetwork`) and Buffer (`BardBoxBuffer`) stay separate owners
behind the facade. `poll(nowMs)` is meant to give each owner one limited step,
serving serial first; it never acquires or reads sensors, sets acquisition
cadence or chooses the reporting interval. Ordering alone cannot bound serial latency if a single
network or storage step blocks (CESH's synchronous HTTP calls currently precede
serial service). Bounded serial therefore needs every adapter step to have a
deadline or a fixed work limit, a per-poll time budget, or a separate task; that
scheduling model is unresolved, and this draft proves no runtime guarantee.
The network owner internally handles Wi-Fi connect and bounded retry, reading
oldest-first from the Buffer, delivery, server ACK and `acknowledge(token)`,
and separates send-time diagnostics from the record's own stored metadata. The
student makes no Wi-Fi, upload, retry or ACK call. Acquisition runs on the
application's own schedule and continues through network outages.

**Recommended choices (not adopted):**

1. *Exact API.* Recommend the typed result objects above (`PublishResult`,
   `SubmitResult`, ticket plus `recordStatus`) over CESH's `bool` plus
   last-error. Rationale: a `bool` cannot report per-channel outcomes or
   separate admission from durable completion.
2. *All-null acceptance.* Recommend accepting an all-null record only when every
   channel has an explicit `missing`/`invalid`/`failed` code, as a failure
   record that is never presented as a measurement; for the latest snapshot,
   serial READ keeps returning the existing `ERR SENSOR_FAIL`. Rationale: the
   failure stays visible with time and metadata on the server instead of
   becoming a silent gap. Alternative: reject all-null records and rely on
   `setSensorFailure`; simpler, but the record-level evidence is lost.
3. *Atomic versus partial publication.* Recommend partial: healthy channels are
   kept and unhealthy ones, including `invalid_type`, become coded nulls, per
   FW-VALIDATION-1; only a structurally unusable sample is rejected whole.
   Rationale: one failed sensor channel should not discard independent healthy
   ones. Serial reconciliation: existing
   `DAT` has no null form, so until a versioned per-channel serial form is
   designed and adopted, READ returns `ERR SENSOR_FAIL` whenever the latest
   snapshot has any non-valid channel. No new serial grammar is defined here.
4. *Durable handoff.* Recommend the explicit `submitRecord` above rather than
   recording every published sample automatically. Rationale: the application
   owns averaging (FW-RECORD-1), so only it knows when a record is complete;
   the ticket separates admission from durable completion. Alternative: an
   opt-in helper that submits each sample as a raw record, for projects without
   averaging. Queueing policy (RKC's no-queue versus CESH's queue) stays open.

**Reconciling the earlier whole-snapshot wording.** The single validity result
for READ, "rejected readings do not become a valid DAT line" and the
illustrative loop below are the earlier all-or-nothing proposal. Under the
recommended partial design, one bad channel does not fail the sample, and
`setSensorFailure` is kept for when no sample can be formed at all. The
illustrative loop below is kept unchanged and labelled as the historical
proposal. Until the APIs settle, the recommended shape is the ordered hand-off
below rather than a second code loop.

**Recommended hand-off sequence (not adopted).**

| Step | Owner | Hand-off |
| --- | --- | --- |
| 1 | Student code (`src/main.cpp`) | On its own acquisition schedule, read the sensors. If no sample can be formed, call `setSensorFailure(code)` and stop here |
| 2 | Student code | `newSample(acquiredAtMs)`; `set` each declared field; `setFailed(field, code)` for a sensor-specific fault |
| 3 | Facade | `publishSample`: generic checks and metadata; replace the latest snapshot; return `PublishResult` |
| 4 | Student code | Check `PublishResult` first. A whole rejection (structurally unusable sample) is reported and adds nothing to averaging. Otherwise only `valid` channel values enter averaging; coded nulls are never averaged as values |
| 5 | Student code | When its window completes, build the record with window/method metadata and call `submitRecord` |
| 6 | Facade / Buffer | Admit and return a ticket; or reject before any storage I/O; or return `backpressure` when the bounded number of outstanding tickets is reached |
| 7 | Student code | On rejection or backpressure, keep the record and retry or report it under project policy; never drop it silently. Keep each ticket in a bounded set (never overwrite an earlier one) and query `recordStatus` until it settles |
| 8 | Internal owners | `poll(nowMs)` advances Buffer persistence and network delivery; student code makes no Buffer or network calls |

The outstanding-ticket bound, the `backpressure` result and retry policy are
proposed names and choices for review.

### Operational settings

| Proposed method | Meaning |
| --- | --- |
| addSetting(spec) | Typed field, default, units, bounds, temporary/persistent support and activation rule |
| addSecretSetting(spec, consumer) | Set-only secret connected to its owning module; public access shows presence only |
| getSetting(name) | Validated effective public value |
| onSettingsChanged(handler) | Bounded notification for application/module activation |

Runtime settings include UID/name, endpoint, SSID/password, per-device upload
credential, acquisition/streaming/reporting intervals and supported retry,
buffer and time settings. Build pins, included drivers, flash layout and build
version remain build choices. A credential authenticates an assigned UID only
when the server enforces that binding; a UID alone grants no upload permission.
No generic public plaintext secret getter or secret echo in errors/logs.

**Reporting interval for application averaging** (proposed,
[FW-INTERVAL-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290622655), October 20, 2026; the exact key and result representation
remain proposal work). Application averaging reads the active reporting interval
through the existing `getSetting(name)`; there is no separate getter. The
setting declares explicit units. Proposed: the value given to application code
is in milliseconds, so it compares directly with `nowMs`; a setting declared in
seconds states its conversion. `getSetting` returns the effective (active)
value for this run. After a successful `begin` it is initialized and stays
stable for the run; before that, or after a failed `begin`, the result is an
explicit not-ready error, never zero or an unstated default. A saved override,
the active value and a pending activation are distinct: settings read-back
reports the saved value and any pending activation, and `getSetting` never
returns a saved value that has not been activated.

The interval is the completed aggregation window and reporting cadence. It is
not the sensor acquisition cadence (`AcquisitionSchedule`) and not queue
catch-up. Reference evidence, CESH `3913ca9`:

- [`CeshReportInterval.h`](https://github.com/bardphysicslab/cesh-air-monitor/blob/3913ca9f6837c252f1e73494bf7466c1f66eb765/software/firmware/esp32-air-node/src/CeshReportInterval.h): `activeReportInterval`
  chooses a stored, supported override, otherwise the build default
  `REPORT_INTERVAL_S`.
- [`main.cpp`](https://github.com/bardphysicslab/cesh-air-monitor/blob/3913ca9f6837c252f1e73494bf7466c1f66eb765/software/firmware/esp32-air-node/src/main.cpp#L3125-L3129) startup multiplies those seconds by
  1000 into `SAMPLE_INTERVAL_MS`, which drives `aggregate.due(now,
  SAMPLE_INTERVAL_MS)` (line 2024).
- `REPORT_INTERVAL_STATUS` reports `default_s`, `active_s`, `override_s`,
  `min_s`, `max_s` and `activation=next_boot`; `REPORT_INTERVAL_SET`/`CLEAR`
  store or remove an override that takes effect at the next boot.

CESH's 15–300 s supported range and its 120 s default (`config.shared.h`) are
CESH choices, not generic BardBox requirements. No live, same-run interval
change or partial-window policy is defined here; the reference activates at the
next boot, and partial-window handling for interval changes remains open (see
[Buffer and consumer integration](#buffer-and-consumer-integration)).

Temporary debug overrides disappear on restart; persistent changes require
explicit saving. Read-back distinguishes saved/effective values and pending
activation. Expiration/reset and override precedence are unresolved grammar
details. Saved Wi-Fi settings, connected Wi-Fi and accepted uploads are separate
outcomes. Unsupported fields fail, rather than pretending all config.h defines
are mutable.

### Separate acquisition scheduler

`AcquisitionSchedule acquisition;` supplies begin(intervalMs),
setInterval(intervalMs) and due(nowMs). A true due result consumes one scheduled
attempt; wraparound and changes are handled without a catch-up storm. This
replaces the earlier device.acquisitionDue suggestion. Sensor conversion
readiness and recovery remain sensor-driver responsibilities. The template
connects interval-change notifications to the scheduler.

Illustrative loop: **historical proposal** (October 14 whole-snapshot design,
superseded for review by the hand-off sequence above; proposed symbols; not a
verified build):

```cpp
void loop() {
  const uint32_t now = millis();
  device.poll(now);
  if (!sensorInitialized || !acquisition.due(now)) return;
  const uint32_t acquiredAt = millis();
  const auto reading = readBme280(); // template-provided sensor adapter
  if (!reading.valid) { device.setSensorFailure("BME_READ_FAILED"); return; }
  auto sample = device.newSample(acquiredAt);
  sample.set("temp_c", reading.temperature);
  sample.set("rh_pct", reading.humidity);
  sample.set("press_pa", reading.pressure);
  if (!device.publishSample(sample).ok())
    device.setSensorFailure("SAMPLE_REJECTED");
}
```

The working BME280 template must supply initialization, board I2C pins/address,
complete schema registration, validated settings, recovery and every referenced
object. Normal-mode sensor reads and forced conversion are different acquisition
choices; polling serial faster does not create measurements. No loop-wide delay.

### Serial command map

| Command | Meaning and status |
| --- | --- |
| PING | Existing optional PONG connectivity check; retain |
| INFO | Existing required identity/build/sensor data; extend safe discovery fields explicitly |
| HEADER | Existing required ordered reading schema |
| READ | Existing required latest snapshot or clear error; clarify repetition metadata |
| START / STOP | Existing optional streaming; stop does not stop acquisition/network delivery |
| UPLOAD | Existing optional request for bounded delivery attempt; not guaranteed acceptance |
| PAYLOAD | Existing optional payload preview, excluding secrets; does not acknowledge delivery |
| BUFFER | Existing optional queue/storage status, not historical record retrieval |
| BUFFER_CLEAR | Existing optional destructive discard, never automatic recovery |
| CONFIG_SCHEMA | Proposed settings/types/units/bounds/secret/activation discovery |
| CONFIG_GET | Proposed saved/effective public values and secret-presence flags |
| CONFIG_STATUS | Proposed revisions, transaction outcomes and pending activation |
| CONFIG_BEGIN / SET / COMMIT / ABORT | Proposed revision-checked updates, staging, atomic application and cancellation |
| STATUS | Proposed runtime diagnostics; decide whether needed separately from INFO |
| RESTART | Proposed deliberate restart after response completion; preserve saved config/data |

Exact new request/response grammar, operation IDs and metadata placement remain
to be finalized and tested on both host and firmware. START streaming and command
replies must remain distinguishable. Unknown/unsupported commands, invalid values,
timeouts, persistence failures and conflicting revisions have distinct results.
Input and output are bounded, including oversized-line discard through delimiter.
Network/storage operations cannot monopolize serial service. Production write and
maintenance access policy is unresolved and must be defined before deployment.

## Buffer and consumer integration

See the companion [buffer API proposal](firmware-buffer-api.md). Latest snapshots
for serial READ and durable recorded records are separate: READ and streaming
never drain or acknowledge recording. Recovering recorded history over serial
needs its own retrieval/acknowledgement contract, which is open; BUFFER remains
status, not retrieval. Absolute timestamps are UTC; unknown time stays explicit. RKC intends to retain
individual readings through outages; CESH retains completed aggregate records.
Each project chooses its record content; aggregation is not buffer behavior.
Averaging ownership (accepted, [FW-RECORD-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289832277), October 20, 2026): any
averaging is done by the firmware application/project sensor logic, which
produces the completed reported record. The shared firmware buffers and
transports that record without choosing or performing averaging, and server
Ingestion validates a data point the same way whether it is raw or averaged. The
record keeps semantic metadata describing the averaging window and method so the
science stays interpretable; its exact fields, representation, applicability and
schema are later contract design, and none are defined here. Not settled by this:
how latest-snapshot publication relates to durable completed-record handoff,
admission versus successful durable append and its pending/error results, and
queueing policy (RKC's no-queue versus CESH's queue).
Changing a CESH reporting interval must define partial-window handling. Queued
records preserve acquisition identity/schema/settings meaning after configuration
changes. Time synchronization/RTC policy is a separate module; serial accepts
supplied timestamps/validity and does not redefine the current time standard.

CESH already has compact storage, provisioning and Wi-Fi override implementations;
adapt supported interfaces incrementally. RKC uses latest cached readings but lacks
device historical storage. Both currently have embedded parsers/legacy response
forms, requiring characterization and host compatibility before migration.


## Runtime settings and new wire commands

Per-device runtime fields include UID, device name, applicable endpoint URLs,
keys, Wi-Fi SSID/password and supported operational settings. Build-time pins,
compiled drivers/capabilities and partition layout remain bundle choices. Empty
Wi-Fi password means an open network; the password-present flag is derived.
No Wi-Fi settings are required for a serial-only node. Server deployment metadata
such as location/owner stays server-owned unless an adopted contract requires it.

Proposed extensions, to be finalized and documented in the same canonical device
standard as implementation (not a second project-local command vocabulary):

| Operation | Proposed command family | Required behavior |
| --- | --- | --- |
| Discover configurable fields | CONFIG_SCHEMA | Version, fields/types/bounds, secret flags, enabled capability and activation rule |
| Inspect saved state | CONFIG_GET / CONFIG_STATUS | Public values, revision and secret-presence indicators only |
| Begin update | CONFIG_BEGIN | Check expected settings revision; select temporary/persistent scope; create bounded transaction |
| Supply fields | CONFIG_SET | Typed fields; unknown/unsupported/invalid fields fail explicitly |
| Save | CONFIG_COMMIT | Validate whole candidate; persist atomically; report resulting revision/activation |
| Cancel | CONFIG_ABORT | Discard pending values; leave saved settings untouched |

Specify exact bounded request/response grammar in the implementation task before
coding clients. New commands do not alter existing INFO/HEADER/READ syntax. Host
and firmware must agree on schema/transaction version; capability discovery
lets Wi-Fi/OTA add their own namespaced fields without redesigning the base.

An interrupted transaction leaves old complete settings or new complete settings,
never a half-updated configuration. Repeating a commit with its transaction ID
must return the same outcome without another credential change. A lost response
can be resolved by public revision/status read-back; it cannot retrieve a secret.
Invalid fields, stale revision, unsupported capability, no active transaction,
persistence failure and transaction expiry need distinct documented error results.
Secret fields are bounded, set-only, omitted from INFO/logs/error text and replaced
without echoing old/new values. USB access alone is not a production authorization
policy; authentication/physical-access policy remains explicit future work.

The application receives a settings-changed event or an updated safe snapshot.
Each field declares immediate application, optional-module reinitialization or
restart-required activation. Saving Wi-Fi is not proof of connection; saving an
OTA URL/key is not proof of commissioned OTA. These outcomes are reported separately.

## ID changes and registry ownership

For future registry/identity-maintenance design, B-Flash/API/registry would own
global availability, atomic reservation, actor/history
and key lifecycle ([USB flashing and provisioning](usb-provisioning-standard.md#identity-registry-and-replacement)). Firmware has no global registry client and cannot know other
assigned IDs. It validates local syntax, durably saves the supplied ID and reports
it. Initial assignment and explicit ID update are proposed, not implemented;
current DC1 provisioning preserves its immutable-record rule. Ordinary reflash
retains configuration. Registry outage blocks the host assignment/change action,
not local INFO/debug or a structurally valid serial settings operation.

This proposed requirement would change existing device-instructions.md's immutable-deployed-ID
rule. Amend that rule explicitly as a proposal alongside the implementation:
ordinary operation preserves UID; an explicit coordinated maintenance action can
change it, retaining historical attribution. Never silently rewrite historical data.
A host registration transition must handle disconnect/lost acknowledgement and
must not activate the same ID for two physical devices. A simple availability
check followed by a device write is insufficient. Do not invent offline allocation.

## Flash layout, write plans and rollback

Moved on 2026-10-14 to the [firmware blueprint](firmware-blueprint.md#5-flash-memory-one-8-mib-esp32-s3-recipe)
so the 8 MiB ESP32-S3 table, protected NVS/data ranges, initial-install/reinstall/OTA
write plans, padding-versus-hash rules and rollback compatibility have one maintained
copy. The section as it stood is preserved at `f9e4e39`. Whether a USB reinstall may
reset otadata remains an open decision recorded there.

## Acceptance and implementation status

Implement in one maintained reusable capability with a minimal independent
consumer and a reference template. Tests cover standard framing, mandatory fields,
new INFO field without parser edit, coherent HEADER/READ, no-sensor/failure behavior,
secret omission, partial/oversized lines, bounded servicing, durable settings
transactions and interrupted/repeated/stale updates. Future registry checks cover
claim/update failures and independently reviewed physical-board binding. They are
not prerequisites or implementations in current Firmware Tools #8.
Build a real sensorless USB image and staged bundle; retain exact binaries, inputs,
hashes and a verified recovery archive outside temporary folders. No approval or
hardware acceptance is implied by this document. Wi-Fi/OTA runtime and their
independent consumers need separate capability evidence when enabled.
