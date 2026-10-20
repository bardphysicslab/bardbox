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

`BardBoxInterface bardbox;` creates one beginner-facing facade (accepted name
`BardBoxInterface`, October 20, 2026, replacing the earlier `BardBoxDevice`
candidate; its methods and results remain proposed and unimplemented). Accepted
target ([FW-SERVICE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291462264)): `begin()` starts internal BardBox service that
keeps running while student code waits (for example in `delay(500)`); this
supersedes the earlier "runs only when called" premise. The mechanism is the
[proposed internal service design](#internal-service-design-proposed) and is not
implemented. The underlying serial module
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

Accepted direction ([FW-SIMPLE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290658288), October 20, 2026): the student hands
over **one completed data point** (raw, or averaged by the application) through
**one** call. BardBox validates it, adds the agreed metadata and routes it
internally by configuration: for now to both serial and Wi-Fi/network delivery
by default, with persistent recording (the internal Buffer) on by default. A
later serial-only device disables Wi-Fi through configuration; the student's
hand-off stays the same and contains no transport-specific code. This
supersedes the unaccepted two-hand-off draft (`publishSample`, `submitRecord`,
`recordStatus` and a ticket loop). Exact method names, result types and
policies remain proposals.

### Registration and startup

Register descriptors before begin. Registration returns explicit errors for
duplicate/reserved names, invalid units/types/bounds, oversized schemas and
unsafe fields. Descriptors are stable after successful begin.

| Proposed method | Meaning |
| --- | --- |
| setFirmwareVersion(version) | Required build metadata; the template rejects missing/placeholder versions at build time |
| bardbox.addSensor(name) | Create and register a sensor in one step through the interface, with an explicit runtime name; returns its typed `BardBoxSensor` handle, which owns its measurements. There is no separate `addSensor(existingObject)`. It does not initialize hardware |
| sensor.addMeasurement(name, unit) | Declare an ordered measurement of that sensor; the optional type is omitted, so it is FLOAT |
| sensor.addMeasurement(name, unit, MeasurementType::Integer) | Declare an ordered integer measurement, for counts or a project's chosen integer representation |
| sensor.addMeasurement(name, unit, MeasurementType::Boolean) | Declare an ordered Boolean measurement (how a unitless Boolean is written is syntax design) |
| addInfoField(name, provider) | Register a bounded typed public status provider |
| addCapability(module) | Attach an optional capability's descriptors and handlers |
| begin(options) | Student startup: validate the complete registration, load settings and enable the chosen capabilities once; return initialization result. Default Serial + Wi-Fi + recording; see [student contract](#proposed-student-contract-draft-for-review) |
| begin(transport, settingsStore) | Internal wiring supplied by the template/shared core (USB CDC/UART transport, settings store); not a separate student call |

Measurement types ([FW-MEASUREMENT-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291173701), October 20, 2026): `addMeasurement`
replaces the October 14 proposed `addFloatField`/`addIntegerField`/`addBooleanField`
names. The type is declared at registration, never inferred from a reading.
Omitting the type argument selects FLOAT; "leave empty" means omit it, never an
empty string or runtime guessing. Integer is for counts and other exact
integers; Boolean is distinct. Double is not adopted as a further required
type. Passing an ordinary integer value to a FLOAT measurement is the one
documented numeric conversion; large integers may lose precision in floating
point (for example, a 32-bit float holds integers exactly only up to 2^24), so
it promises no exactness, and exact counts use Integer. Any other mismatch is
an `invalid_type` channel outcome, with no other coercion. Finiteness, declared
bounds, coded per-channel nulls and faults, and record metadata are unchanged:
nothing becomes zero or is clamped. Exact supported widths, syntax and the
representability/error policy remain contract design.

The optional type is written with a type constant, illustrated as
`MeasurementType::Integer` or `MeasurementType::Boolean`
([FW-SENSOR-2](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291413717); spelling proposed). A bare C++ `int` is a type keyword,
not a value argument. A measurement declared Integer, such as humidity a
project chooses to report in whole percent, must receive an integer value: a
fractional value is never silently truncated. The application converts
explicitly with its own rounding rule; otherwise the channel gets an explicit
invalid type or representation outcome under the final contract. There is no
default coercion.

Sensors ([FW-SENSOR-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291273464), October 20, 2026): measurements belong to sensor
instances, not to one flat set of prefixed names. There is still exactly one
device object, `BardBoxInterface bardbox`, which starts and coordinates Serial,
Wi-Fi and the Buffer once, owns the device UID and receives the one `publish`.
A sensor handle creates no transport, queue, device UID or authentication
identity, and there is no nested facade or second `begin` (for example no
`cesh.begin()`). A sensor is created and registered once, through the interface
([FW-SENSOR-2](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291413717)); its runtime name is given explicitly, never taken from a
C++ variable name, and there is no automatic global self-registration or hidden
ordering. Exact factory versus owner-constructor and lifetime syntax remain
proposed. Registering a sensor or calling `bardbox.begin()` does not
initialize hardware: driver initialization, readiness, calibration, read errors
and bounded recovery stay explicit in the driver and application. Separate
sensors may each declare the same measurement name (for example `pm25` on
PMS-A and PMS-B). `BardBoxSensor` is recommended over `BBSensor`; the class
spelling, constructor, attachment and lifetime remain proposed. The serial and
network naming of sensor-scoped measurements, and whether one record spans all
sensors or records are grouped per sensor (with its atomicity), remain open.

Firmware/protocol versions are distinct immutable build metadata. The shared
module supplies adopted protocol version, physical hardware identity and required
safe fields; device UID comes from settings, not an unexplained global.
Sensorless startup is valid and cannot manufacture a zero-valued measurement.

### Loop service and records

| Proposed method | Meaning |
| --- | --- |
| newRecord() | Create a typed candidate record for the declared fields; BardBox stamps time and validity, and metadata |
| record.set(sensor, field, value) | Supply a declared value of that sensor |
| record.setFailed(sensor, field, code) | Mark one channel failed with a sensor-specific code |
| record.setAveraging(windowMs, method) | Optional window and method metadata for an application-averaged record ([FW-RECORD-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289832277)) |
| publish(record) | **The one student hand-off** (name `publish` accepted; signature proposed): validate, add metadata, update the serial latest snapshot and route to enabled recording and network delivery; return an honest result (below) |
| setSensorFailure(code) | No record could be formed; older data is not served as current valid data |
| getSetting(name) | Effective settings, including the active reporting interval (see [Operational settings](#operational-settings)) |
| status() | Optional diagnostics (queue fill, storage and network failures, loss counts); never required in a loop |

There is no student service call: no `poll`, no `millis()` feeding, no transport
or storage maintenance, no tickets and no manual queue retry
([FW-SERVICE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291462264)). The earlier proposed `poll(nowMs)` loop line is
superseded.

Serial output keeps the published [device instructions](device-instructions.md):
`READ` returns the latest published record on request, and `START` streaming
is opt-in. Publishing never pushes unsolicited `DAT` lines or interleaves them
with command replies. Repeated reads keep the same record identity, which
includes reboot distinction. A project that averages publishes only completed
records, so `READ` shows the latest completed record, not each raw sample; a
separate live-latest path is an optional advanced capability only if a real
consumer needs it, never a required second publication.

Generic checks (accepted direction, [FW-VALIDATION-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289980118),
October 20, 2026): on `publish`, the shared facade checks numeric finiteness,
declared types (allowing only the documented integer-to-FLOAT conversion),
required fields and declared validity bounds, so application
code does not import `cmath`/`isfinite` or repeat those checks. It reports
explicit per-channel outcomes and keeps healthy independent channels. It never
turns NaN, missing or invalid values into zero, clamps them or presents them as
valid measurements. Sensor reads, readiness, calibration and sensor-specific
fault detection stay with the application. These checks do not replace or
weaken server validation or trust checks.

### Proposed student contract (draft for review)

The direction is accepted under [FW-SIMPLE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290658288); names, syntax, types and
policies below are recommendations, and nothing is implemented. The earlier
two-hand-off draft, its hand-off sequence and the October 14 illustrative loop
are superseded and were never accepted; they remain readable at
[`82030b5`](https://github.com/bardphysicslab/bardbox/blob/82030b5fa34315738083539036497f6bd6fd9400/docs/firmware-base-and-serial-api.md#proposed-student-contract-draft-for-review). Module READMEs
on template `main` (`75bf01b`) still describe that draft until separately
reconciled.

The student sees three concepts: **startup**, **one hand-off** and the
**effective interval**. There are no service calls, transport calls, tickets or
status loops. The loop reads sensors, does any math, publishes and may simply
`delay()`; sensors are read only when that loop runs.

```cpp
BardBoxInterface bardbox;                  // the one device
BardBoxSensor environment, pmsA, pmsB;     // handles, filled by addSensor below

void setup() {
  environment = bardbox.addSensor("environment");
  environment.addMeasurement("temp_c", "degC");  // type omitted: FLOAT
  environment.addMeasurement("rh_pct", "%");
  pmsA = bardbox.addSensor("pms_a");
  pmsA.addMeasurement("pm25", "ug/m3");          // same name, separate sensors
  pmsB = bardbox.addSensor("pms_b");
  pmsB.addMeasurement("pm25", "ug/m3");
  bme280.begin(); pmsPortA.begin(9600); pmsPortB.begin(9600);  // driver init: explicit
  bardbox.begin();                         // BardBox only: starts Serial, Wi-Fi, recording and internal service
}

void loop() {
  auto record = bardbox.newRecord();
  record.set(environment, "temp_c", bme280.readTemperature());
  record.set(environment, "rh_pct", bme280.readHumidity());
  record.set(pmsA, "pm25", readPm25(pmsPortA));
  record.set(pmsB, "pm25", readPm25(pmsPortB));
  const auto result = bardbox.publish(record);  // the one hand-off
  if (!result.accepted()) reportProblem(result);  // project choice
  delay(500);                              // BardBox service continues meanwhile (target)
}
```

(Proposed symbols; not a verified build. `bme280`, `pmsPortA/B` and
`readPm25` stand for the project's actual drivers; their initialization is
illustrative. The single record spanning all three sensors is illustrative
only; per-sensor grouping is open. An averaging project publishes once per
completed window with `setAveraging`, and sizes its window from `getSetting`.)

If a project chooses integer humidity instead, it declares the type and rounds
explicitly (illustrative):

```cpp
environment.addMeasurement("rh_pct", "%", MeasurementType::Integer);
// ...
record.set(environment, "rh_pct", lround(bme280.readHumidity()));  // project's rounding rule
```

Passing the unrounded fractional value to that channel would be an explicit
invalid outcome, not a truncated value.

**1. Startup: `begin(options)`.** Arduino-style: capabilities are chosen once.
A beginner calls `begin()` with no arguments: no baud argument and no required
flags. The existing BardBox serial default governs, unchanged and configurable
in the Serial section of [`include/config.h`](#operational-settings), not as an argument: template
[`main.cpp`](https://github.com/bardphysicslab/bardbox-project-template/blob/75bf01b4024233ab7cbf919963500a151b1501e6/software/firmware/src/main.cpp#L57) line 57 calls `Serial.begin(115200)`, and
[`platformio.ini`](https://github.com/bardphysicslab/bardbox-project-template/blob/75bf01b4024233ab7cbf919963500a151b1501e6/software/firmware/platformio.ini) sets `monitor_speed = 115200`. Starting a
configured Wi-Fi connection without blocking, and continuing offline, is a
proposed startup detail, not an accepted implementation. The accepted defaults are Serial, Wi-Fi/network delivery and persistent
recording on. The published base Serial interface is always present. Proposed
MVP profile (a recommendation, not a new platform rule): the simple profile
offers no recording-off option, and its only option is a future serial-only
mode that turns Wi-Fi off (for example `begin({.wifi = false})`; syntax not
adopted). Wi-Fi without Buffer durability is not offered. Recording stays
default ON as already accepted; a deliberate, assessed omission under the
[Buffer proposal](firmware-buffer-api.md) (for example a board without capacity)
remains possible, and any other disabled combination still needs contract
design. Credentials and identity come from provisioned settings, never
from `begin` flags. The existing `begin(transport, settingsStore)` row
describes the internal wiring the template and shared core supply (USB
CDC/UART transport and settings store); it is not a second student call.

**2. One hand-off: `publish(record)`.** The name `publish` is accepted from the
user's conversation; the exact signature and result types stay proposed. Every
path (raw or averaged; serial, Wi-Fi and recording) uses this one completed-record
hand-off. It returns `PublishResult`:

| Part | Values | Meaning |
| --- | --- | --- |
| Per channel | `valid`, `missing`, `invalid` (`non_finite`, `invalid_type`, `out_of_bounds`), `failed` | Non-valid channels become coded nulls; an unknown field is ignored and reported as `unknown_field` |
| Admission | `accepted` | Validated, the serial snapshot updated and the record handed to recording and enabled delivery. **Not** a promise that it is durably stored, sent or acknowledged |
| | `backpressure` | Validated, but recording cannot admit it now (bounded pending space full); not recorded, and the result says so rather than dropping silently |
| | `rejected` | Structurally unusable (no successful `begin`, unregistered schema, oversized) or refused before any storage I/O; reason given |

Republishing an older record never replaces a newer serial snapshot. All-null
is accepted only when every channel carries an explicit code, as a failure
record, never as a measurement. Healthy channels are kept; only a structurally
unusable record is rejected whole. Existing `DAT` has no null form, so `READ`
returns `ERR SENSOR_FAIL` when the latest record has any non-valid channel, until
a versioned serial form is adopted; no new serial grammar is defined.

**3. Effective interval: `getSetting(name)`.** Averaging reads the active
reporting interval as described in [Operational settings](#operational-settings).

**Internal, not student-facing.** Serial (`BardBoxSerial`), network delivery
(`BardBoxNetwork`) and Buffer (`BardBoxBuffer`) stay separate owners, and the
latest snapshot stays separate from durable records. The Buffer keeps honest
states (`pending`, `durable`, `uncertain` when a write or metadata step fails
after bytes may be written, `failed` only when provably nothing was written;
see the [append reference](firmware-buffer-api.md#compatibility-and-cesh-evidence)).
The network owner handles Wi-Fi connect, bounded retry, oldest-first delivery,
server ACK and removal. Wi-Fi disconnects, storage failures and saturation
eviction appear in optional `status()` diagnostics and loss counts (and the
server's central error log when communication permits), never as a claim that
data was sent or stored. Retry, preservation and loss-counting policy for
`backpressure`, `uncertain` or `failed` records, and queueing policy (RKC
no-queue versus CESH queue), stay open.

### Internal service design (proposed)

Accepted need ([FW-SERVICE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291462264), [acceptance supplement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6291470459)): BardBox
service continues independently of student code and its `delay()`, on the
current 8 MiB, no-PSRAM ESP32-S3 target. Everything below is a candidate
mechanism for review, not an adopted thread model, not implemented, and with
no thread-safety or timing guarantee until built and tested. No per-sensor,
per-transport or multi-board task framework.

| Topic | Candidate |
| --- | --- |
| Worker | One owned BardBox service task, created by `begin()` with a fixed stack, priority and core chosen by measurement (it must starve neither the Arduino loop task nor the Wi-Fi stack). CESH already runs an acquisition task and a buffer mutex ([append reference](firmware-buffer-api.md#compatibility-and-cesh-evidence)), which shows the platform pattern but is not this design |
| Startup and failure | `begin()` validates registration, loads settings, opens storage, starts Serial and then creates the task. If task creation or storage fails, `begin()` returns an explicit error and Serial `INFO`/diagnostics stay available where possible; there is no silent half-start. Wi-Fi connects asynchronously from the task, and being offline is a normal state. A second `begin()` is an error; stop/restart beyond reboot is open |
| Clock | The task keeps its own monotonic time; students never pass time. `newRecord()` stamps acquisition time from the same clock; UTC and validity come from the time module |
| Hand-off | `publish` runs in the student's task: it validates, stamps metadata and copies the record into one of a fixed number of statically sized admission slots (no per-record heap). It waits at most a short bounded time; if the slots are full it returns `backpressure`. The latest snapshot is replaced as a whole copy under a short lock. BardBox never keeps a reference to the student's record object |
| Ownership | Only the service task touches Serial command I/O, the Wi-Fi/HTTP client and Buffer storage. Student code touches only admission slots, the snapshot copy and settings copies, each under short locks |
| Progress | Each iteration gives every owner one bounded step: Serial (read available bytes, answer at most one command), admission (move one record into the Buffer), network (one delivery step when connected and due), then a short blocking wait so other tasks run |
| Failures | Full slots give `backpressure`; storage failures and Wi-Fi outages appear in `status()` and loss counts; records stay in the Buffer while offline. No infinite queue, no indefinite blocking and no silent loss |

**Gates a task alone does not solve.** One task cannot answer serial while it is
itself blocked inside a slow HTTP request or a flash write/erase. Bounded serial
responsiveness therefore depends on:

1. HTTP connect and response timeouts plus bounded request and response sizes
   in the network adapter;
2. a measured worst-case LittleFS append and erase time on the target;
3. Wi-Fi connect and reconnect that never blocks the task.

If measurement shows these cannot be bounded tightly enough, the review decides
between a separate small serial task and a separate network task; neither is
adopted now.

**First acceptance test (before any CESH or OTA refactor).** An independent
consumer, not CESH boilerplate: register one sensor with two measurements,
`begin()`, then loop over read, publish and `delay(500)`. It passes when:

- `INFO` and `READ` are answered during the student's delay, including while
  Wi-Fi is disconnected, within a stated bound;
- publishing continues during an outage with honest `accepted`/`backpressure`
  results, records are kept in the Buffer and delivered oldest-first after
  reconnect, and nothing is lost silently;
- `READ` shows the latest published record and `status()` shows progress and
  failures.

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
is in milliseconds, so it compares directly with millisecond timing; a setting declared in
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

**Simple configuration layout** (proposed, October 20, 2026; user intent: one
obvious place that is easy to find and edit, without a settings framework,
extra typed public APIs or many files). Build-time defaults live in one
tracked `include/config.example.h`, copied to an ignored `include/config.h`
([repository layout](repository-layout.md#firmware-configuration)). The
template's [`include/README.md`](https://github.com/bardphysicslab/bardbox-project-template/blob/75bf01b4024233ab7cbf919963500a151b1501e6/software/firmware/include/README.md#configuration-headers)
points there. It has labelled sections with units:

| Section | Example contents | Read and validated by |
| --- | --- | --- |
| Serial | Baud rate, default `115200` (bit/s) | `BardBoxSerial` |
| Network | Wi-Fi on by default; retry timing (ms). No default SSID, password or endpoint | `BardBoxNetwork` |
| Buffer | Recording on by default; capacity limits with stated units | `BardBoxBuffer` |

Each module reads and validates its own section; there is no central policy
module. The serial baud is set here, not as a `begin()` argument.
`platformio.ini` keeps board, framework, dependencies and monitor settings; its
`monitor_speed` only sets the computer's serial monitor and must match the
firmware baud, but it does not set `Serial.begin`. Private values (SSID,
password, endpoint, credentials) go only in the ignored `config.h` or runtime
provisioning, separate from public policy. The example never carries default
secrets. Accepted so far: Serial default 115200, both transports on and
recording on by default; every other default, unit and field name remains
design. The template uses no configuration today, so no header is created.

Temporary debug overrides disappear on restart; persistent changes require
explicit saving. Read-back distinguishes saved/effective values and pending
activation. Expiration/reset and override precedence are unresolved grammar
details. Saved Wi-Fi settings, connected Wi-Fi and accepted uploads are separate
outcomes. Unsupported fields fail, rather than pretending all config.h defines
are mutable.

### Separate acquisition scheduler

Optional for projects that want non-blocking acquisition timing; a beginner
can use `delay()` instead, since BardBox service no longer depends on the loop.
`AcquisitionSchedule acquisition;` supplies begin(intervalMs),
setInterval(intervalMs) and due(nowMs). A true due result consumes one scheduled
attempt; wraparound and changes are handled without a catch-up storm. This
replaces the earlier device.acquisitionDue suggestion. Sensor conversion
readiness and recovery remain sensor-driver responsibilities. The template
connects interval-change notifications to the scheduler.

The October 14 illustrative loop is superseded by the short example in the
[student contract](#proposed-student-contract-draft-for-review); see [`82030b5`](https://github.com/bardphysicslab/bardbox/blob/82030b5fa34315738083539036497f6bd6fd9400/docs/firmware-base-and-serial-api.md#separate-acquisition-scheduler) for history.

The working BME280 template must supply initialization, board I2C pins/address,
complete schema registration, validated settings, recovery and every referenced
object. Normal-mode sensor reads and forced conversion are different acquisition
choices; polling serial faster does not create measurements. A student
`delay()` pauses acquisition only, not BardBox service (target).

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
schema are later contract design, and none are defined here. The completed
record reaches the Buffer through the single `publish` hand-off
([FW-SIMPLE-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290658288)); admission is reported there and durable
outcomes are diagnostics. Queueing policy (RKC's no-queue versus CESH's queue)
remains open.
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
