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
hardware-verified. Normal `READ` and a live read are two independent one-shot
request/reply operations:

| Operation | Returns |
| --- | --- |
| Normal `READ` | The latest completed published record. For CESH this is the latest completed averaged record |
| Live read | The latest cached individual sensor readings |

- Neither starts a continuous stream, needs a STOP/restart cycle, forces
  acquisition or waits for the next averaging window.
- A host debugging program may alternate the two, using a bounded response
  timeout. Waiting synchronously for a serial reply can block the host caller;
  that is distinct from waiting for acquisition.
- Repeated replies keep the original measurement or sample identity and time.
  Unavailable data is explicit, never fabricated or served as current.
- A project that publishes raw records, such as the template simulator, has no
  averaging: its normal `READ` returns its latest published raw record, and
  BardBox never invents averages.
- Averaged acquisition, the archival queue and ACK semantics are unchanged.

Still open: the exact live-read command spelling and framing, and their
compatibility with existing `HEADER`/`DAT` parsers; continuous live streaming
and its grammar. Current firmware does not implement this split yet (for CESH,
see its [firmware README](https://github.com/bardphysicslab/cesh-air-monitor/blob/main/software/firmware/README.md)).

## Proposed beginner-facing application API

Updated October 14, 2026. This replaces the earlier four-argument
BardBoxSerial/provider sketch in this proposal. Names below are proposed,
not existing C++ symbols or a compiling implementation.

`BardBoxDevice device;` creates one beginner-facing facade. It runs when
called, not automatically in a background task. The underlying serial module
owns framing/parsing; settings, acquisition scheduling, time, storage and
network delivery have their own owners. The facade wires their interfaces
without importing a project's main.cpp. USB CDC/UART remain injected Arduino
transports. Projects do not write serial response strings.

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
| poll(nowMs) | Bounded input/output and operation progress; no sensor acquisition or network request |
| isStreaming() | Inspect START/STOP state; normally unnecessary for project code |
| newSample(acquiredAtMs) | Create a typed candidate snapshot at acquisition time |
| sample.set(field, value) | Supply a declared value; reject wrong types/unknown fields |
| sample.setTime(stamp) | Attach optional UTC/validity from the separate time module |
| publishSample(sample) | Validate all required fields/rules, copy coherently and assign sample identity; return result |
| setReadingNotReady() | Explicit no-usable-sample state; also initial state |
| setSensorFailure(code) | Mark acquisition failed; older data is not silently served as current valid data |

READ returns the latest accepted valid snapshot immediately. Repeated reads
keep the same identity. Sample identity includes reboot distinction; sequence
alone is insufficient. Age and acquisition-time metadata must be specified
without silently changing existing HEADER/DAT compatibility. Publish is a
snapshot update, not automatic network upload or unsolicited serial output.
Late acquisition is distinct from a failed sensor: the application/driver owns
freshness policy and must be able to inspect sample age.

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

Illustrative loop (proposed symbols; not a verified build):

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
| READ | Existing required latest snapshot or clear error; accepted target: latest completed published record ([normal READ and live read](#normal-read-and-live-read)) |
| Live read | Accepted target: one-shot latest cached individual readings; exact command spelling and framing open |
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
