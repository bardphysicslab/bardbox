# BardBox firmware blueprint (proposed)

Status: **design proposal**, consolidated 2026-10-14. Documentation only; it
governs nothing until merged to `main`. It does not establish that any repository
conforms, and it does not authorize building, flashing, publication or deployment.
Tracker: [firmware API design #31](https://github.com/bardphysicslab/bardbox/issues/31);
dispositions: [branch and proposal autopsy #33](https://github.com/bardphysicslab/bardbox/issues/33).

Provenance: sections 2 to 8 come from `docs/firmware-blueprint.md` on
`claude/firmware-blueprint` at `69795b588e56b31fdafa64c02e272e6cd4d68d33`
(2026-10-12, reference CESH `software/firmware/esp32-air-node` 0.8.6). Section 5
also absorbs the flash-layout section of the serial proposal at `f9e4e39`, so the
layout has one maintained copy. Edits on 2026-10-14 separate existing CESH behaviour
from the newer proposed base contract; they do not change any published standard.
Source governing commits: engineering-standards `3bf9c600b35f73322e8f610baffec2b682bdcc77`,
BardBox `da5132a648d21989a984e00fa1fd02760bcdf4f7`.

**Existing** marks behaviour that exists today in the named repository, at the
revision and date stated. **Proposed** marks the intended BardBox pattern. Neither
label means implemented in a shared library, tested on hardware, merged or deployed.

## 1. Firmware documentation map (entry point)

Read in this order before firmware, serial-driver, USB-assembly or delivery-buffer
work. Published standards are authoritative; proposals are pending design contracts.

| Topic | Document | Status |
| --- | --- | --- |
| Device commands and response forms | [Device instructions](device-instructions.md) | Published standard |
| Network delivery, ACK, buffer diagnostics | [Web Node protocol](web-node-protocol.md) | Published standard (`web-node-v0.2`) |
| Source tree, build/runtime split, lifecycle, flash layout, release | This blueprint | Proposal |
| Base firmware, serial module, settings, beginner API | [Serial/base API](firmware-base-and-serial-api.md) | Proposal |
| Optional durable delivery queue | [Buffer API](firmware-buffer-api.md) | Proposal |
| USB flash, provisioning and boot verification | [USB flashing and provisioning](usb-provisioning-standard.md) | Proposal |
| Compact record storage format | [compact-record-storage.md at PR #16 head `7b947be`](https://github.com/bardphysicslab/bardbox/blob/7b947be081d1d1fb646849c15e9491fbdce1297b/docs/compact-record-storage.md) | Pending review, not adopted |
| OTA lifecycle and validation | [ota-update-standard.md at PR #16 head `7b947be`](https://github.com/bardphysicslab/bardbox/blob/7b947be081d1d1fb646849c15e9491fbdce1297b/docs/ota-update-standard.md) | Pending review, not adopted |
| Continuation, decisions and handoff | [Firmware API continuation](firmware-api-continuation.md) | Dated record |

The [PR #16](https://github.com/bardphysicslab/bardbox/pull/16) documents remain
owned by that review; they are linked at an exact commit rather than copied, so
there is one storage format and one OTA draft. Other pending topics (repository
layout and config filenames, Wi-Fi recovery, live previews, campus access, Drive
documentation home, tracker policy) keep their own reviews and dispositions in
[#33](https://github.com/bardphysicslab/bardbox/issues/33).

## 2. Source tree

**Existing (CESH 0.8.6, 2026-10-12).** One PlatformIO project per firmware
product, under `software/firmware/<project>/`. The template keeps a single project
directly in `software/firmware/`. [Device instructions](device-instructions.md)
still name the older `firmware/` root; the layout change is pending in
[PR #23](https://github.com/bardphysicslab/bardbox/pull/23).

```text
software/firmware/<project>/
  platformio.ini            board, framework, partitions, build environments
  partitions_*.csv          flash layout per environment (see section 5)
  src/main.cpp              composition: setup/loop, command dispatch, wiring
  src/config.example.h      tracked placeholders for a per-device local build
  src/config.shared.h       tracked hardware-only defaults for shared images
  src/config.h              ignored; local values, or a shim to config.shared.h
  src/BardBox*.h            reusable capabilities (see below)
  src/<Project>*.{h,cpp}    project adapters and policy (e.g. CeshOTA.cpp)
  src/<Sensor>*.{h,cpp}     drivers (e.g. THPGSensor.cpp, CheckedBme280.h)
  include/                  shared reliability helpers (BardBoxSensorHealth.h …)
  test/host, test/pilot     host-compiled C++ tests of pure logic
```

Repository-level `tests/` drive the host C++ tests and partition and version
checks, and a firmware-version CI job builds every environment.

**Proposed separation.** A target, not a refactor requirement:

- **Composition.** `main.cpp` only wires components; command parsing and dispatch
  belong to the shared serial module ([serial/base API](firmware-base-and-serial-api.md)).
- **Reusable capabilities.** Serial module, settings store, provisioning transfer,
  acquisition schedule, record queue, OTA state/verification/writer and sensor
  health. Each has an explicit interface, is host-testable and has no project
  globals. Acquisition scheduling, serial, settings, time, buffering and delivery
  have separate owners.
- **Adapters.** ESP32 storage, HTTPS, USB CDC/UART transports and sensor drivers
  implement those interfaces.
- **Project policy.** Sampling intervals, record content (individual or aggregate),
  payload fields and sensor selection.

CESH still holds much policy and wiring in its 3,058-line `main.cpp` (2026-10-12).
Extracting it is separate work and is not part of adoption.

## 3. Build-time hardware versus runtime settings

| Concern | Owner | Mechanism |
| --- | --- | --- |
| Board, flash size, partition layout, pins | Build | `platformio.ini` environment and partition CSV |
| Sensor drivers and models (e.g. BME680 or BME280; PMS5003 or PMS6003) | Build | `-D` flags and `config.shared.h` defaults; one compiled image per hardware combination |
| Firmware version | Build | Mandatory build metadata; placeholders rejected ([serial/base API](firmware-base-and-serial-api.md#registration-and-startup)) |
| UID, display name, Wi-Fi SSID/password, telemetry URL and token, OTA origin/device token/CA, signing key ID and public key, initial image length/hash | Per device, at runtime | **Existing (CESH `BardBoxDeviceConfig.h` at `345b6bb`):** DC1 record written over USB serial (`PROVISION_*`) into NVS. **Proposed:** typed settings with temporary/persistent scope ([settings](firmware-base-and-serial-api.md#operational-settings)) |
| Acquisition, streaming and reporting intervals; supported retry, buffer and time settings | **Existing:** build. **Proposed:** per device, at runtime | **Existing:** compile-time constants (CESH `REPORT_INTERVAL_S` in `config.shared.h`/`config.h`); DC1 encodes no interval. **Proposed only:** operational settings ([settings](firmware-base-and-serial-api.md#operational-settings)); changing intervals at runtime is not implemented by current CESH provisioning |
| Location, ownership, coordinates, display metadata | Server | Never in firmware |

- `config.example.h` holds tracked placeholders for a per-device local build.
- `config.h` is ignored, private and per device.
- `config.shared.h` holds tracked hardware-only defaults for shared images, with
  placeholder identity (`uncommissioned`, an `.invalid` server).

Secrets are writable but never echoed publicly; settings read-back reports only
their presence. Build defaults and runtime settings must share one schema and
precedence rule rather than two unrelated sets of settings.

**Existing limits (CESH 0.8.6):**

- Shared builds set `BARDBOX_REQUIRE_DEVICE_CONFIG=1` and stay non-operational
  until a valid DC1 record loads.
- Assembly dropdowns select a compiled bundle; DC1 cannot change compiled sensor
  drivers. There is no single binary for every hardware choice.
- CESH `THPGSensor.cpp` includes `config.h` unconditionally, so shared builds need
  an ignored `config.h` shim that only includes `config.shared.h`. A hermetic fix
  is CESH follow-up work.

## 4. Lifecycle

### Existing CESH 0.8.6 behaviour (2026-10-12)

1. **Unprovisioned start.** The shared image boots and reports
   `ERR,DEVICE_NOT_PROVISIONED`. It handles only `PROVISION_*`, `WIFI_*` and
   `OTA_*` serial commands; `INFO` and the others return that error. It
   initializes no sensors, creates no records and contacts no server.
2. **USB flash.** An explicit, operator-selected port, a fresh identity and
   security check, bounded writes, and read-back of every written byte (section 5).
3. **Serial provisioning.** The host sends DC1 (`PROVISION_BEGIN/DATA/COMMIT`).
   The firmware verifies its trust material and that the running image matches
   the record's initial length and hash, then stores the record in NVS. The record
   is immutable: an identical re-commit succeeds, and different bytes are refused.
4. **Deliberate reset and boot verification.** The record activates on the next
   boot. The host checks loaded status, UID, firmware version and telemetry URL.
   Native USB re-enumerates on reset, so the operator reselects the port.
5. **OTA commissioning.** Separate and explicit (`OTA_COMMISSION BENCH_VERIFIED`),
   after layout, bootloader and recovery validation. Installation does not
   commission OTA.

Existing limits: there is no DC1 maintenance or rekey contract. Reflashing a
provisioned device with a different app image keeps its DC1 initial hash, which
then no longer matches the running image and breaks OTA identity (firmware-tools
review finding S1).

These blocked-INFO and immutable-record rules describe current CESH limitations.
They are evidence of existing state, not requirements for future firmware.

### Proposed base lifecycle

- **Unprovisioned INFO remains usable.** `INFO`, `HEADER` and `READ` answer before
  registration, with explicit sentinel values and the physical MAC for host
  binding ([required information](firmware-base-and-serial-api.md#required-information-and-reading-contract)).
- **Explicit coordinated maintenance.** UID, settings and credentials can be
  changed by an explicit maintenance action through revision-checked settings
  transactions and the registry; ordinary operation and reflash preserve them
  ([ID changes](firmware-base-and-serial-api.md#id-changes-and-registry-ownership)).
- **Separate outcomes.** Flash, provisioning and boot verification are reported
  separately ([USB flashing and provisioning](usb-provisioning-standard.md)).
- **Initial-image identity is not device identity.** Release identity and mutable
  per-device settings are separate; an old immutable image hash is not retained
  as identity after the app bytes change.
- **OTA commissioning stays separate** from installation and is governed by the
  pending OTA proposal.

Migrating CESH from DC1 to the proposed settings contract needs its own reviewed
plan; existing DC1 records must remain readable until then.

## 5. Flash memory: one 8 MiB ESP32-S3 recipe

These are exact capacities for **one recipe**, CESH `partitions_8mb_dual.csv` on
the Feather ESP32-S3 (8 MiB). They are not universal BardBox constants; other
boards declare their own. On 2026-10-12 the generated table in candidate
`d3c1c76b4364` matched the CSV exactly.

| Region | Offset | Size | Purpose | Written by USB install? |
| --- | --- | --- | --- | --- |
| bootloader | 0x000000 | up to 0x8000 (image 15104 B, write 0x4000) | Start and select firmware | yes |
| partition table | 0x008000 | 0x1000 (image 3072 B) | Generated memory map, sector-sized write | yes |
| nvs | 0x009000 | 0x5000 (20 KiB) | Persistent device configuration and module state. Existing CESH namespaces: DC1 record (`bb-device`), Wi-Fi override (`bb-wifi-ovr`), OTA state (`bb-ota`) | **never** |
| otadata | 0x00e000 | 0x2000 (8 KiB) | Slot selection/validation metadata, not URLs or keys | existing CESH plan: reset to 0xFF; see open decision below |
| app0 (ota_0) | 0x010000 | 0x200000 (2 MiB) | Firmware slot A | yes |
| app1 (ota_1) | 0x210000 | 0x200000 (2 MiB) | Firmware slot B | no (OTA writes it) |
| data (`spiffs` label, LittleFS) | 0x410000 | 0x3e0000 (3.875 MiB) | Optional measurement queue/storage | **never** |
| coredump | 0x7f0000 | 0x10000 (64 KiB) | Explicit platform diagnostics policy | no |

Rules for this recipe:

- **Bootloader at 0x0.** The ESP32-S3 ROM loads the second-stage bootloader from
  offset 0. The partition table sits at 0x8000 and must not be overlapped. The
  actual bootloader image length is checked separately.
- **CSV and binary table agree.** The CSV and the generated binary table must
  agree exactly and fit actual flash capacity.
- **Filesystem label.** The historical CSV labels the data partition `spiffs`; the
  intended runtime uses LittleFS. A label is not proof of filesystem compatibility.
- **Protected ranges.** NVS and the data partition lie outside every write plan
  and are preserved across initial install, reinstall and OTA unless an explicit
  migration or format is authorized. The planner refuses any image sector that
  crosses another partition. No whole-chip erase.
- **Buffering is optional** even though space is reserved. Retention depends on
  record size, cadence and storage overhead.
- **Hashes versus padding.** Writes are padded with 0xFF to 4 KiB sectors, and
  read-back covers each full padded range, including any otadata reset. Image
  identity uses the unpadded app bytes: initial length/hash and the bundle's
  SHA-256 never include sector padding. Example: app 1102928 B is written as
  1105920 B.
- **Board recipe.** The Feather's PlatformIO recipe appends TinyUF2 at 0x2d0000,
  inside app1. Installation recipes exclude it, and UF2 is out of scope.

### Write plans: initial install, reinstall and OTA

| Plan | Writes | Boot selection |
| --- | --- | --- |
| Initial USB install | bootloader, partition table, app0; otadata reset | Blank otadata makes the bootloader boot the first OTA slot, app0 |
| USB reinstall of a previously installed device | **Existing CESH bench plan:** same ranges as initial install, including otadata reset to select app0 | **Open decision** below |
| OTA update | Inactive application slot only | Update/boot-validation contract records the switch in otadata, with OTA state in NVS |

A reinstall is not an OTA update. Every plan reads back every planned written byte
and never writes NVS or the data partition.

**Open decision: otadata during USB reinstall.** The sources disagree, and no
universal rule is adopted here:

- the blueprint at `69795b5` and the existing CESH/firmware-tools plan reset
  otadata on every USB install, including reinstall, so the just-written app0 boots;
- the USB proposal at `ab83ab3` allows a first-install reset but says a later
  update "must not blindly reset" otadata, since that can select an old or
  unwritten application;
- the serial proposal at `f9e4e39` says initial/reinstall "can reset otadata
  deliberately".

To decide: for a device that has run an OTA-installed image from app1, does a
supported USB reinstall (a) write app0 and reset otadata, or (b) inspect the
running slot and existing OTA metadata and write a different plan? The decision
must state how NVS OTA state (`bb-ota`) that refers to the previous slot is
reconciled, what the rollback target is afterwards, and which physical evidence
supports it. Existing evidence: the dry-run plan for `d3c1c76b4364` (never
flashed) and the USB flash verification recorded in
[firmware-tools #5](https://github.com/bardphysicslab/firmware-tools/issues/5).
Until decided, a reinstall onto an OTA-updated device is not a supported path.

### Boot validation and rollback compatibility

OTA runtime may be disabled, but validate the actual bootloader configuration,
dual slots, first-boot validation and rollback policy now. Metadata alone does
not implement rollback. A successful boot marks the new image valid under
documented base health criteria; no sensor or network requirement may be invented
for the sensorless USB base. Optional modules later supply additional validation.

Configuration and record schemas must stay readable by fallback firmware, or use
an explicit reversible migration, so rollback does not strand the device. Retain
old queue decoders until old records drain ([buffer API](firmware-buffer-api.md#compatibility-and-cesh-evidence)).

## 6. Build, release and approval

- **Ownership.** The project repository owns source, environments and partition
  CSVs. firmware-tools owns validation, packaging, publication and installation.
- **Release.** Build, then validate with firmware-tools `build_manifest` against
  the profile and a clean board recipe, then sign approval over the input digests,
  then publish with `BundlePublisher` as the one current bundle for that hardware
  profile. Building is not approval.
- **Retention.** Keep an immutable copy of every candidate and approved bundle
  outside source Git and temporary directories, with a SHA256SUMS manifest. A
  source bundle does not preserve binaries.
- **Reproducibility (existing, 2026-10-12).** Not bit-reproducible:
  `FIRMWARE_BUILD_ID` embeds `__DATE__`/`__TIME__`, and CESH pins neither the
  platform nor library versions. Record resolved versions with each candidate;
  pinning is follow-up work.
- **Versioning.** Firmware, protocol (`web-node-v0.2`), settings/DC1 schema and
  queue schema versions are independent. Firmware version is mandatory. A
  behaviour change requires the project's firmware-version check.

## 7. USB identity

The same board presents different USB identities in different modes. ROM
download mode presents USB JTAG/serial `303A:1001`. The connected CESH spare
running firmware was observed (2026-10-12) as TinyUSB CDC `239A:8113`. Its
PlatformIO board definition lists `239A:811B`, `239A:011B` and `239A:811C`, so the
observed value, not the board file, belongs in assembly configuration.

USB vendor and product filters identify a board type, not a physical device.
Existing CESH `INFO` does not report the MAC; the proposed base INFO does.

## 8. Template adoption plan (proposed)

**Existing (template `main` at `9b46574`, 2026-10-12):** `software/firmware/` has
a 65-line esp32dev simulator with fixed `DEVICE_UID`/`FW_VERSION`, a single
`example_node` environment, the reliability headers, and no partition CSV,
runtime settings, OTA or host tests. Gaps: no shared/local config split, no
runtime identity, no partition recipe, no firmware CI, and two divergent
`BardBoxSensorHealth.h` copies (`firmware/include` and `software/firmware/include`).

Adoption steps, each a bounded template PR. Do not copy CESH acquisition logic.

1. Resolve layout ([PR #23](https://github.com/bardphysicslab/bardbox/pull/23)),
   then point [device instructions](device-instructions.md) at `software/firmware/`.
2. Add `config.example.h`/`config.shared.h` and an ignored `config.h` to the
   example. Keep the simulator's sensor code.
3. Add an optional `shared_<env>` environment with an explicit partition CSV and
   a documented flash table. A layout is board-specific.
4. Promote host-tested shared components for the reviewed serial module and
   settings store, with a sensorless consumer. Evaluate CESH's DC1 record/store and
   provisioning-transfer headers as extraction candidates against the proposed
   settings contract. Choose one maintained home and do not copy them per project,
   following [promotion governance](promotion-governance.md).
5. Add host tests and a firmware CI job that builds every environment.
6. Keep buffering and OTA optional, adopted only after their reviews and bench gates.

## 9. Evidence and limits

Historical evidence from `69795b5` (2026-10-12): CESH candidate
`cesh-shared_ota_bme680` 0.8.6, app SHA-256
`d3c1c76b43643826fcba8ce9a41ec457111504f801726da3ee9d709a44071e0a`, an
**unapproved TEST candidate**: built, validated by firmware-tools and dry-run
planned, never flashed. 30 firmware host tests passed then (local host tests,
not re-run for this consolidation). There is no hardware, sensor, network or OTA
acceptance of this document or candidate.
