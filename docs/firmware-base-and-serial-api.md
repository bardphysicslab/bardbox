# Minimal BardBox firmware: base and serial module API

Status: the student-facing direction is accepted ([BB-005](DECISIONS.md), reconciled
October 20, 2026); implementation details remain proposals. Nothing here is
implemented: the C++ API below is not an existing library, and no build, hardware
validation, adopted protocol extension or deployment is claimed.
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
| READ | DAT framing matching HEADER, or explicit ERR result | Published values via `sensor.publish`; see [normal READ and live read](#normal-read-and-live-read) |

The existing forms remain OK INFO uid=... fw=... sensors=..., HDR,v1,...,
and DAT,... or ERR SENSOR_FAIL. Existing PING can return PONG. Project extensions
must not replace uid, fw or sensors, break framing, or expose secrets. New fields
are additive and follow an explicit version/compatibility rule. The base INFO
proposes unprovisioned state. Earlier mandatory physical-MAC reporting/binding
is deferred: current provisioning uses the existing node UID including its
instance, with no MAC or registry integration. Factory-base-MAC lookup remains
future registry design, separate from authentication.

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

### Normal READ and live read

Accepted target ([CESH#59](https://github.com/bardphysicslab/cesh-air-monitor/issues/59#issuecomment-6295361501), October 20, 2026); not implemented or
hardware-verified. Normal `READ` and `READ_LIVE` are two independent one-shot
request/reply operations:

| Operation | Returns |
| --- | --- |
| Normal `READ` | The latest completed published record. For CESH this is the latest completed averaged record |
| `READ_LIVE` | The latest cached individual sensor readings |

- Neither starts a continuous stream, needs a STOP/restart cycle, forces
  acquisition or waits for the next averaging window.
- A host debugging program may alternate the two, using a bounded response
  timeout. Waiting synchronously for a serial reply can block the host caller;
  that is distinct from waiting for acquisition.
- Repeated replies keep the original measurement or sample identity and time.
  Unavailable data is explicit, never fabricated or served as current.
- Live cached readings stay distinguishable from the completed record: their
  sample identity and time are separate from the completed record's identity
  and averaging window, with a per-sensor age where sensors are acquired
  independently. The exact wire fields are still pending.
- For a project that publishes raw records, normal `READ` returns its latest
  published raw record; BardBox never invents averages. The current template
  simulator is not yet that implementation: it generates fixed example values
  when `READ` arrives and has no cached acquisition or published-record owner,
  so it needs a bounded cache and record semantics, adapted under template
  [#36](https://github.com/bardphysicslab/bardbox-project-template/issues/36).
- Averaged acquisition, the archival queue and ACK semantics are unchanged.

The single-token spelling `READ_LIVE` is [accepted](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6297449136).
Still open: response framing and fields, and their
compatibility with existing `HEADER`/`DAT` parsers; continuous live streaming
and its grammar. Current firmware does not implement this split yet (for CESH,
see its [firmware README](https://github.com/bardphysicslab/cesh-air-monitor/blob/main/software/firmware/README.md)).

<a name="proposed-beginner-facing-application-api"></a>
<a name="registration-and-startup"></a>
<a name="loop-service-and-samples"></a>

## Beginner-facing application API

Accepted direction ([BB-005](DECISIONS.md), October 20, 2026), recorded in
[FACADE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289589216), [FW-SIMPLE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290658288), [FW-MEASUREMENT-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291173701),
[FW-SENSOR-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291273464), [FW-SENSOR-2](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291413717), [FW-SENSOR-PUBLISH-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291563410)
([acceptance](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291568725)) and [FW-SERVICE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291462264) ([acceptance](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291470459)). Nothing here is
a compiling library or implemented behavior. Exact C++ signatures, types,
callbacks and the sensor handle's type and lifetime remain proposed unless
stated as accepted below.

**Accepted student-facing shape:**

- One device object, `BardBoxInterface bardbox;`, owns Serial, Wi-Fi/network
  delivery, the Buffer, the device UID and internal service. Student code makes
  no transport, storage or service calls.
- `bardbox.addSensor(name)` creates and registers a sensor once, with an
  explicit runtime name, and returns a logical sensor handle. A sensor is a
  scope only: no transport, queue, UID or authentication identity. Registering
  a sensor does not initialize hardware.
- `sensor.addMeasurement(name, unit, optionalType)` declares that sensor's
  measurements in order. Omitting the type means FLOAT; explicit types use
  constants illustrated as `MeasurementType::Integer` and
  `MeasurementType::Boolean` (spelling proposed). An integer passed to a FLOAT
  measurement is the one documented conversion and may lose precision for
  large values; an Integer channel never silently truncates fractional input.
  Separate sensors may reuse a measurement name.
- `bardbox.begin()` takes no arguments and starts BardBox, including internal
  service that continues while student code waits, for example in
  `delay(500)`. There is no student `poll`, `millis()` feeding, record builder,
  ticket or manual queue retry.
- `sensor.publish(value1, value2, ...)` hands over values the application has
  already acquired, in declared measurement order.

### Illustrative BME280 example

Not a verified build; `ProjectBme280Driver` and `bmeDriver` are placeholders for
the project's actual driver.

```cpp
#define FIRMWARE_VERSION ""        // Student: enter your application firmware version here.

BardBoxInterface bardbox;          // the one device
BardBoxSensor bme280;              // handle type and lifetime: design open
ProjectBme280Driver bmeDriver;     // placeholder for the project's real driver

void setup() {
  bme280 = bardbox.addSensor("bme280");
  bme280.addMeasurement("humidity", "%");        // FLOAT (type omitted)
  bme280.addMeasurement("temperature", "degC");
  bme280.addMeasurement("pressure", "Pa");
  bmeDriver.begin();                // hardware init stays explicit project code
  bardbox.begin();                  // no arguments; starts internal service
}

void loop() {
  float humidity = bmeDriver.readHumidity();      // acquired by the application
  float temperature = bmeDriver.readTemperature();
  float pressure = bmeDriver.readPressure();
  bme280.publish(humidity, temperature, pressure); // declared order
  delay(500);                       // BardBox service continues (target)
}
```

An explicit type would read
`bme280.addMeasurement("pressure", "Pa", MeasurementType::Integer);`
(spelling proposed); that channel then needs an integer the application derived
from a valid reading.

**Checks on publish.** BardBox checks the value count, declared type (with the
integer-to-FLOAT conversion), finiteness and declared bounds per channel. A bad
channel becomes an explicit null with a reason, never zero or a clamped value,
and healthy independent channels are kept. Swapping two values of the same type
cannot be detected, so declaration order must be clear.

**What publish does not mean.** Publishing updates the sensor's latest-reading
cache. It does not make every cache update a completed or durable record:
records are created at the [recording interval](#recording-interval-and-missing-readings)
(BB-009), and normal `READ` returns the latest completed record
([normal READ and live read](#normal-read-and-live-read)), so it does not
necessarily change on every publish. Publishing is not a network upload or
unsolicited serial output.

**Still proposed, not accepted from the facade proposal branch:**

- exact signatures, result types, callbacks, the sensor handle's type and
  lifetime, and the failure-reporting form;
- at record creation, whether records are grouped per sensor or as one coherent
  full-node record, and the matching average hand-off; how original measurement
  time and average windows attach; cache scheduling; and the raw diagnostic
  provider for averaging projects. This does not reopen BB-009: raw publishes
  update the latest cache, and records are created at the recording interval;
- the internal service mechanism. Independent service is accepted, but a
  single ESP32-S3 service task, its priority, stack, locks and admission slots
  are unaccepted candidates. The service clock is not measurement time, and a
  failed `begin()` cannot promise Serial without a designed owner;
- `READ_LIVE` response framing and wire fields, and any scheduling
  approval. Existing published commands, NVS keys and configuration macros stay
  as they are (BB-009).

Firmware/protocol versions are distinct immutable build metadata. The shared
module supplies the adopted protocol version, physical hardware identity and
required safe fields; device UID comes from settings, not an unexplained global.
Sensorless startup is valid and cannot manufacture a zero-valued measurement.
Serial framing and parsing stay inside BardBox; projects do not write serial
response strings.

Application build metadata is declared visibly at the top of `main.cpp`: the
starter leaves `FIRMWARE_VERSION` empty with a comment for the student to fill it
in ([accepted clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6297603792)).
The target build rejects missing or placeholder firmware versions. BardBox reports
the supplied version automatically; students do not call `setFirmwareVersion`.
For now, firmware version is the only required metadata blank in the student
main file. Sensor declarations, measurement names/units and driver initialization
also live in main as application code. UID, Wi-Fi, endpoints and adjustable
intervals belong in configuration/provisioning; pins belong in build configuration.
The shared core supplies the protocol version and hardware MAC (target, not yet
implemented). The target build error should say: "Please set FIRMWARE_VERSION in
main.cpp." Older incoming data with no reported version is labelled Unknown,
never an invented zero version. This example is still a proposal, not an
implementation of that build check.

Advanced registration, still proposed: `addInfoField(name, provider)` and
`addCapability(module)`. The internal wiring `begin(transport, settingsStore)`
is supplied by the template and shared core, not a second student call.

### Operational settings

Students configure values in the documented configuration/provisioning location;
they do not register settings or secrets in their main loop. An application may
optionally read an effective public setting, for example the active recording
interval when its averaging math needs it.

| Optional student operation (exact signature proposed) | Meaning |
| --- | --- |
| getSetting(name) | Read the validated effective public value, with documented units; never a password or token |

**Internal module configuration proposals — not required student calls:**

| Proposed internal method | Meaning |
| --- | --- |
| addSetting(spec) | The owning BardBox module defines a typed option, default, units, bounds, persistence support and activation rule |
| addSecretSetting(spec, consumer) | The owning module defines a protected credential input; public access reports presence only |
| onSettingsChanged(handler) | Internal notification to the owning module when an effective setting changes |

These internal methods are unimplemented design candidates, not additions to
the beginner setup/read/publish workflow.

Runtime settings include UID/name, endpoint, SSID/password, per-device upload
credential, acquisition/streaming/reporting intervals and supported retry,
buffer and time settings. Build pins, included drivers, flash layout and build
version remain build choices. A credential authenticates an assigned UID only
when the server enforces that binding; a UID alone grants no upload permission.
No generic public plaintext secret getter or secret echo in errors/logs.

Temporary debug overrides disappear on restart; persistent changes require
explicit saving. Read-back distinguishes saved/effective values and pending
activation. Expiration/reset and override precedence are unresolved grammar
details. Saved Wi-Fi settings, connected Wi-Fi and accepted uploads are separate
outcomes. Unsupported fields fail, rather than pretending all config.h defines
are mutable.

<a name="separate-acquisition-scheduler"></a>

### Acquisition timing

Acquisition timing belongs to the application. A beginner can read sensors and
call `delay()`, because BardBox service does not depend on the loop (target,
BB-005). A non-blocking helper such as the earlier proposed
`AcquisitionSchedule` (`begin`, `setInterval`, `due`) remains an optional
proposal, not a requirement. Sensor conversion readiness and recovery remain
driver responsibilities; normal-mode reads and forced conversion are different
acquisition choices, and polling serial faster does not create measurements.
The October 14 illustrative loop (`poll`, `newSample`, `publishSample`) is
superseded and remains in Git history.

### Serial command map

| Command | Meaning and status |
| --- | --- |
| PING | Existing optional PONG connectivity check; retain |
| INFO | Existing required identity/build/sensor data; extend safe discovery fields explicitly |
| HEADER | Existing required ordered reading schema |
| READ | Existing required latest snapshot or clear error; accepted target: latest completed published record ([normal READ and live read](#normal-read-and-live-read)) |
| READ_LIVE | Accepted target: one-shot latest cached individual readings; response framing and fields open; not implemented |
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
Changing a CESH reporting interval must define partial-window handling. Queued
records preserve acquisition identity/schema/settings meaning after configuration
changes. Time synchronization/RTC policy is a separate module; serial accepts
supplied timestamps/validity and does not redefine the current time standard.

CESH already has compact storage, provisioning and Wi-Fi override implementations;
adapt supported interfaces incrementally. RKC uses latest cached readings but lacks
device historical storage. Both currently have embedded parsers/legacy response
forms, requiring characterization and host compatibility before migration.

### Recording interval and missing readings

Accepted target ([BB-009](DECISIONS.md), [BB-010](DECISIONS.md);
[recording interval](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6296975652), [missing reading](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6296995202), October 20, 2026); not
implemented. Adoption is tracked in template [#36](https://github.com/bardphysicslab/bardbox-project-template/issues/36) and CESH [#59](https://github.com/bardphysicslab/cesh-air-monitor/issues/59).

**Recording interval** is the human-facing name for how often a completed
measurement record is created and admitted to persistent buffering. It is
separate from sensor acquisition cadence and from network delivery or catch-up
timing.

- **Raw readings:** the latest-reading cache is refreshed at the sensor's own
  acquisition cadence (for example every 5 s). At each recording boundary (for
  example every 100 s), the latest available reading is recorded with its
  original acquisition time. Cache updates between boundaries are not
  historical records: they are not averaged, not all enqueued, and not durable.
- **Application averages:** the application supplies the completed average with
  its actual window metadata. CESH keeps its existing coupling of averaging
  window and record creation.
- Outages do not stop recording; catch-up delivery runs independently and can
  be faster.
- Existing names stay compatible: CESH's `REPORT_INTERVAL_S` macro,
  `REPORT_INTERVAL_*` serial commands and `report_s` NVS key, and the
  [ingestion contract's reporting-cadence fields](ingestion-contract.md#reporting-cadence),
  are not silently renamed. Labels and documentation change first.

**No fresh reading at a boundary.** For each affected measurement, the record
carries an explicit no-fresh-reading result: a missing or fault status with no
numeric value. The last good measurement is never reused as new, and nothing is
zero-filled or made to look fresh. Healthy channels in the same record continue
normally. Displays show the current value as `—`
([Web UI standard](web-ui-standard.md#cards-status-and-information-grouping)) and may show the last
good value and time only as labelled stale context. Freshness limits are set
per sensor or application; there is no universal timeout.

#### Proposed boundary and cache scheduling (for review, not accepted)

These are ownership and timing proposals. They are not accepted wire, schema or
runtime behavior, and they add no public transaction API. An averaging
application may couple its averaging window to record creation (CESH does);
acquisition and network delivery stay independent of record creation either way.

**Raw-reading recorder** (channels recorded from the latest cache):

1. *Boundaries.* One recorder owns recording boundaries on a monotonic clock.
   Each boundary has a **scheduled due time** (the previous due time plus the
   interval, so drift does not accumulate) and, once taken, an **actual capture
   time** (step 3). If it falls more than one interval behind, it records once,
   skips the missed boundaries and counts the skip in diagnostics; it never
   bursts catch-up records.
2. *Cache entries.* Each channel's entry holds its value, original sample ID,
   original acquisition time (monotonic, plus UTC when valid) and the freshness
   limit declared by its sensor or application. Sensor code updates its entry
   under a short lock that only copies fixed-size values: no I/O, no allocation.
3. *Snapshot.* At or after the due time the recorder takes the same short
   lock, reads the monotonic clock as the **capture time** while holding it,
   copies all entries into a snapshot it owns, releases the lock and builds the
   record outside it. It never waits for an in-flight sensor read.
4. *Cutoff and ordering.* The cutoff is the capture time, not the due time. An
   update written before the recorder takes the lock is in this record, even if
   it was acquired after the scheduled due time; one written after belongs to
   the next boundary. Because every included entry was written before the
   capture on the same monotonic clock, its age is never negative and no
   future-time arithmetic arises. The due time and the capture lag (capture
   time minus due time) are kept only as diagnostics.
5. *Freshness.* A channel is fresh when its age, the capture time minus its
   monotonic acquisition time, is within its declared limit. Otherwise, or if it
   was never sampled, it gets an explicit no-fresh-reading result. The record
   carries each channel's original acquisition time, never the due or capture
   time as a measurement time; UTC is not used in the age arithmetic. The limit
   should be required at registration rather than given a guessed default
   (open).
6. *Same sample twice.* If a channel still holds the sample already recorded at
   the previous boundary and it is still fresh, the record repeats it with the
   **same original sample ID and time**, so it is recognizable as a repeat and
   never as a new measurement. The alternative, a no-fresh-reading result for
   any repeat, is open for review.

**Application-average producer** (CESH and other averaging projects):

7. The producer owns window close and hands over each completed record once,
   with its original window start and end metadata. The generic raw recorder does
   not run for averaged channels, so it can neither pick up a previous average
   nor record a false no-fresh-reading while the producer is closing a window.
8. CESH reuses its existing boundary ([`acquisitionTask`](https://github.com/bardphysicslab/cesh-air-monitor/blob/3d80e3fbde8211424b6ec1e7a90ab77b13d9b691/software/firmware/esp32-air-node/src/main.cpp#L2017-L2041)): under
   `sensorMutex`, `aggregate.due` → `completeWindow` → `aggregate.reset` →
   `latestCompletedPayload`, then one `appendReadingToBuffer` outside the lock.
   There is no second automatic averager and no queue of all raw samples.

**Admission and normal `READ`:**

9. Normal `READ`'s latest completed record updates when the record is created,
   before admission, and the admission outcome (accepted, backpressure,
   rejected, storage failure) is reported separately in diagnostics. A storage
   failure therefore never hides the latest completed measurement from serial,
   and it is never presented as stored. This matches CESH's current order (it
   sets `latestCompletedPayload` before appending and counts a failed append in
   `windowsDropped`); CESH's existing failure semantics are not changed.

**Live read:**

10. Publishing averages alone does not provide an individual live cache. Live
    read needs an explicit binding to a raw diagnostic provider for those
    sensors; that binding is a material gate.

Gates this proposal does not close: acceptance of the scheduling above; the
firmware wire representation of a no-fresh-reading result and of repeated
samples; when an average is handed over relative to a raw boundary in mixed
projects; duplicate-record handling and admission outcomes in the storage
contract; and the raw diagnostic provider binding for live read.


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

### Implemented candidate subset: `config/1` (template, October 20, 2026)

The reference template implements a first subset for UID, Wi-Fi SSID and Wi-Fi
password only ([template PR #47](https://github.com/bardphysicslab/bardbox-project-template/pull/47);
accepted scope: [repeatable serial settings](https://github.com/bardphysicslab/firmware-tools/issues/50#issuecomment-6303975922),
[two actions](https://github.com/bardphysicslab/firmware-tools/issues/50#issuecomment-6303999176), [visible fields](https://github.com/bardphysicslab/firmware-tools/issues/50#issuecomment-6304076785)). The commands are
`CONFIG_SCHEMA`, `CONFIG_GET`, `CONFIG_BEGIN <revision>`, `CONFIG_SET <field> <hex>`,
`CONFIG_COMMIT` and `CONFIG_ABORT`. Values are hex-encoded, and the password is set-only.
Saved values override compiled defaults at the next start and survive an ordinary
reflash. A failed save keeps the previous record, and a lost reply is resolved by
reading the revision back. Exact grammar: the template's
`software/firmware/lib/BardBoxSerial/README.md`. It is a **candidate**: no
transaction IDs, no CONFIG_STATUS, no temporary scope and no other fields yet. The
family above remains the proposal for the rest. Firmware without it answers as for an
unknown command, so tools must discover it with `CONFIG_SCHEMA`.

## ID changes and registry ownership

For future registry/identity-maintenance design, B-Flash/API/registry would own
global availability, atomic reservation, actor/history
and key lifecycle ([USB flashing and provisioning](usb-provisioning-standard.md#identity-registry-and-replacement)). Firmware has no global registry client and cannot know other
assigned IDs. It validates local syntax, durably saves the supplied ID and reports
it. Initial assignment and explicit ID update are proposed, not implemented;
current DC1 provisioning preserves its immutable-record rule. Ordinary reflash
retains configuration. Registry outage blocks the host assignment/change action,
not local INFO/debug or a structurally valid serial settings operation.

Accepted for template firmware ([firmware-tools#50](https://github.com/bardphysicslab/firmware-tools/issues/50#issuecomment-6303975922)): the UID is a
repeatable `config/1` setting, and stored records keep the UID they were recorded
with. The DC1/DB1 records below and the devices that use them keep their immutable
rule. This proposed requirement would change existing device-instructions.md's immutable-deployed-ID
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
