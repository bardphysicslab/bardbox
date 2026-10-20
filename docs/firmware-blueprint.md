# BardBox firmware blueprint (proposed)

Status: **design proposal**, consolidated 2026-10-14 and merged to `main` on
2026-10-16 (PR #32) as a proposal, not an adopted or implemented design. October
19 accepted direction ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991)) updates recording and saturation below. It does not establish that any repository
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

The [BardBox Architecture Map](architecture-map.md) links the updated student-facing
firmware and server template drawings and the one maintained [USB flasher layers
and firmware/server boundaries](architecture-map.md#usb-flasher)
implementation map in the same BardBox document. That tooling diagram labels proposed
extensions and does not replace the shared contracts below.

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
| Compact record storage format | [Compact record storage](compact-record-storage.md) | Draft contract merged October 16 (PR #16); not implemented or adopted |
| OTA lifecycle and validation | [OTA update standard](ota-update-standard.md) | Draft contract merged October 16 (PR #16); not implemented or adopted |
| Continuation, decisions and handoff | [Firmware API continuation](firmware-api-continuation.md) | Current entry; dated history archived |

PR #16 merged on October 16, so its storage format and OTA draft are maintained
on `main` (one copy each); merging did not adopt or implement them. Other pending topics (repository
layout and config filenames, Wi-Fi recovery, live previews, campus access, Drive
documentation home, tracker policy) keep their own reviews and dispositions in
[#33](https://github.com/bardphysicslab/bardbox/issues/33).

## 2. Source tree

**Existing (CESH 0.8.6, 2026-10-12).** One PlatformIO project per firmware
product, under `software/firmware/<project>/`. The template keeps a single project
directly in `software/firmware/`, as the merged
[repository layout](repository-layout.md) specifies; [device instructions](device-instructions.md)
follow that layout and note that older projects still use a top-level `firmware/` root.

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

- **Composition.** `main.cpp` is the student's start file and holds sensor setup,
  reads and facade calls; it is not limited to wiring. Command parsing and dispatch
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

**Accepted starting layout ([FW-LAYOUT-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290294824), October 20, 2026; role README
scaffold created, nothing implemented).** One PlatformIO project,
`bardbox-project-template/software/firmware/`, holds the student start file and
the BardBox core libraries as `lib/` siblings of `src/` and `include/`.
Authoritative architecture and contracts stay in `bardbox/docs`; bardbox keeps
no duplicate firmware core under `bardbox/software/`. Superseded: the earlier
single `BardBoxCore/src` example tree, the split-home recommendation (core in
`bardbox/software/`, starter in the template) recorded at
[FW-CHECKPOINT-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6290013749),
and the briefly scaffolded `src/application/` and `src/application/sensors/`
folders, removed by the user's simplification: students start in
`src/main.cpp` and split a larger project later, only when needed.

Actual tree on [`codex/firmware-starter-scaffold`](https://github.com/bardphysicslab/bardbox-project-template/tree/codex/firmware-starter-scaffold/software/firmware)
(not merged); every README is new except the root one, which gained a layout map:

```text
bardbox-project-template/software/firmware/
  README.md                 existing; layout map added
  platformio.ini            existing; unchanged
  src/README.md             start file, config convention, current vs target
  src/main.cpp              existing simulator; unchanged; the start file
  include/README.md         folder purpose; the two existing helpers
  include/BardBoxSensorHealth.h, BardBoxTransportRecovery.h   existing; unchanged
  lib/BardBoxInterface/README.md facade contract overview (no code)
  lib/BardBoxSerial/README.md    serial owner contract overview (no code)
  lib/BardBoxNetwork/README.md   network owner contract overview (no code)
  lib/BardBoxBuffer/README.md    Buffer owner contract overview (no code)
  test/README.md            host and integration test home (no tests yet)
```

Configuration follows the [repository layout](repository-layout.md#firmware-configuration)
convention: tracked `src/config.example.h` and ignored `src/config.h`, added
only when a variant needs per-device build values; the simulator needs neither,
so neither exists. Accepted: colocation and this starting layout. The facade library
and class name `BardBoxInterface` is accepted (replacing the `BardBoxDevice`
candidate). Still proposed: the other library names, per-library layout, every API, result and durability
choice, test wiring and any versioning. Each library gets `include/`, `src/` or
tests only when needed; drivers and platform adapters only when a consumer
needs them. A compile of `example_node` from cached packages produced a
byte-identical image before and after the scaffold (checked at template `27d7358`; later commits are README-only). The interfaces are drafted
in the [proposed student contract](firmware-base-and-serial-api.md#proposed-student-contract-draft-for-review).

## 3. Build-time hardware versus runtime settings

**October 16 current-source reconciliation.** CESH 0.11.0 at `34ff50a` and
Firmware Tools `5142b97` implement the
[USB device configuration and selection standard](usb-device-configuration-standard.md):
DB1 basic provisioning alongside unchanged DC1, mutable reporting-interval
overrides, capability-checked Wi-Fi selection and release-default metadata.
The dated 0.8.6 observations below are historical evidence. Inherited limits
such as blocked unprovisioned INFO and immutable records remain current at
`34ff50a` unless an explicit current-source change below says otherwise.


| Concern | Owner | Mechanism |
| --- | --- | --- |
| Board, flash size, partition layout, pins | Build | `platformio.ini` environment and partition CSV |
| Included sensor drivers, pins and supported hardware | Build | A firmware image can select among included drivers at runtime; provisioning cannot add a driver absent from the image. CESH PR #50 includes both environmental-sensor families; particle selection remains project configuration. |
| Firmware version | Build | Mandatory build metadata; placeholders rejected ([serial/base API](firmware-base-and-serial-api.md#registration-and-startup)) |
| UID, display name, Wi-Fi and telemetry; optional OTA trust/image identity | Per device, at runtime | **Existing (CESH `34ff50a`):** immutable DB1 basic or DC1 including OTA inputs, written via `PROVISION_*` into NVS, mutually exclusive. Separate supported mutable settings do not replace these records. [USB configuration records](usb-device-configuration-standard.md#2-device-configuration-records). General revisioned identity/settings maintenance remains proposed. |
| Reporting interval | Firmware default at build; supported override per device | **Existing (CESH 0.11.0 at `34ff50a`):** `REPORT_INTERVAL_STATUS/SET/CLEAR`; override stored separately from immutable DB1/DC1 and active at next boot. Reporting/aggregation cadence is not sensor polling or catch-up. See the [USB standard](usb-device-configuration-standard.md#3-device-settings-over-usb). |
| Acquisition/streaming intervals and retry, buffer and time policy | Project build/runtime policy | General typed operational settings remain proposed; do not infer that the implemented reporting override makes every interval mutable. |
| Installation location, ownership, coordinates, display metadata | Server Registry | Not firmware configuration; GPS position measured by a mobile node is observation data ([map](architecture-map.md#location-metadata-and-observed-position)) |

- `config.example.h` holds tracked placeholders for a per-device local build.
- `config.h` is ignored, private and per device.
- `config.shared.h` holds tracked hardware-only defaults for shared images, with
  placeholder identity (`uncommissioned`, an `.invalid` server).

Secrets are writable but never echoed publicly; settings read-back reports only
their presence. Build defaults and runtime settings must share one schema and
precedence rule rather than two unrelated sets of settings.

**Inherited limits (observed in CESH 0.8.6; still current at `34ff50a` where noted):**

- Shared builds set `BARDBOX_REQUIRE_DEVICE_CONFIG=1` and stay non-operational
  until a valid DC1 or DB1 record loads (current `34ff50a`; 0.8.6 accepted DC1 only).
- DC1 cannot add compiled sensor drivers. CESH PR #50 at `24c2305` now includes
  both environmental-sensor drivers and identifies the fitted family at runtime;
  particle models remain build choices. That was pushed/unmerged source at the dated observation. CESH 0.11.0 now
  includes the change; source/CI does not itself establish hardware acceptance.
- The 0.8.6 wrapper needed a local `config.h` shim. PR #50's wrapper removes
  that include; do not describe the old wrapper defect as current at `24c2305`.

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

Blocked unprovisioned INFO and immutable DB1/DC1 remain current at CESH `34ff50a`.
The commands allowed before that gate now also include `REPORT_INTERVAL_*`,
alongside provisioning, Wi-Fi and OTA maintenance. Usable unprovisioned INFO and
general identity/settings transactions below are proposals, not implemented
behavior. The dated lifecycle above must not be generalized beyond its snapshot.

### Current USB configuration and selection boundary

At CESH `34ff50a`, shared firmware can load DB1 (identity/Wi-Fi/telemetry, no OTA)
or DC1 (including OTA trust and image identity). Neither is a general mutable
settings record. Supported Wi-Fi selection and reporting interval changes are
separate operations, not identity replacement or automatic OTA commissioning.
The [USB standard](usb-device-configuration-standard.md) defines exact fields,
exclusion rules, retry semantics, capabilities and activation behavior.

A USB-selected NEW entry may carry BBU1 bound to selection sequence and image
validation hash. A matching pending image may be confirmed through that path only
when the device verifiably has no DC1/OTA configuration; DB1-only and unprovisioned
cases do not authorize accepting a network-OTA candidate. All other cases retain
the project's existing validation and rollback. First install/recovery write no
marker. Do not generalize this bounded marker to a universal health approval.

### Proposed base lifecycle

- **Unprovisioned INFO remains usable.** `INFO`, `HEADER` and `READ` answer before
  registration, with explicit sentinel values ([required information](firmware-base-and-serial-api.md#required-information-and-reading-contract)).
- **Explicit coordinated maintenance.** UID, settings and credentials can be
  changed by an explicit maintenance action through revision-checked settings
  transactions; ordinary operation and reflash preserve them. Registry integration
  is deferred separately from current provisioning
  ([ID changes](firmware-base-and-serial-api.md#id-changes-and-registry-ownership)).
- **Separate outcomes.** Flash, provisioning and boot verification are reported
  separately ([USB flashing and provisioning](usb-provisioning-standard.md)).
- **Initial-image identity is not device identity.** Release identity and mutable
  per-device settings are separate; an old immutable image hash is not retained
  as identity after the app bytes change.
- **OTA commissioning stays separate** from installation and is governed by the
  OTA draft contract.

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
| app1 (ota_1) | 0x210000 | 0x200000 (2 MiB) | Firmware slot B | not in initial install; USB inactive-slot update or OTA can write it |
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
- **Protected ranges.** NVS/data are outside these approved same-layout plans.
  An older/different-layout recovery may overwrite prior data or make it
  inaccessible; it requires the explicit data-loss warning. Schema readability
  remains separate from untouched bytes. The planner checks approved partition
  boundaries; that alone does not prove preservation under a foreign table.
  No whole-chip erase.
- **Recording defaults ON** for BardBox firmware, including serial-connected
  nodes ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991) item 6); the data partition holds it. Retention depends on record
  size, cadence and storage overhead; no unlimited retention is promised.
- **Hashes versus padding.** Writes are padded with 0xFF to 4 KiB sectors, and
  read-back covers each full padded range, including any otadata reset. Image
  identity uses the unpadded app bytes: initial length/hash and the bundle's
  SHA-256 never include sector padding. Example: app 1102928 B is written as
  1105920 B.
- **Board recipe.** The Feather's PlatformIO recipe appends TinyUF2 at 0x2d0000,
  inside app1. Installation recipes exclude it, and UF2 is out of scope.

### Write plans: initial install, reinstall and OTA

The [USB path matrix](usb-provisioning-standard.md#write-boundaries-and-ota-compatibility)
is the maintained description of blank install, older-layout recovery,
same-layout recovery and inactive-slot update at Firmware Tools `5142b97`.
Install/recovery reset metadata to all-FF; inactive-slot updates select NEW with
BBU1 when an appended validation hash is available, per the [USB selection marker](usb-device-configuration-standard.md#1-usb-selection-marker).
Network OTA writes the inactive slot with its own lifecycle state. USB transport
alone does not identify the metadata or confirmation path.

The earlier sources at `69795b5`, `ab83ab3` and `f9e4e39` disagreed about
general USB reinstall policy. Existing host choices are now observable; their
presence is not acceptance of every CESH configuration/OTA-state combination.
Document any overwritten selected/fallback image; preserve it on inactive-slot
updates and verify an explicit recovery plan for destructive reinstalls. Preserve
prior queue/configuration under compatible layouts and verify exact writes. An old DC1 initial-image hash or saved bb-ota state
can disagree with newly written bytes even when NVS is untouched.

### Boot validation and rollback compatibility

**Proposed remaining health/lifecycle contract, not adopted policy.** This narrows
the previously open reinstall question; it does not change CESH validation or
the [OTA draft contract](ota-update-standard.md).

1. Installer evidence states exact image identity, layout/bootloader, write ranges,
   before/after metadata and preserved or lost fallback/data. Read-back completion
   is installation evidence, not boot/health/commissioning success.
2. The bootloader owns slot selection and SDK pending/valid/rollback transitions.
   The app owns bounded local acceptance. Never infer application health from
   erased fallback or a displayed INFO reply.
3. USB-selected pending candidates need a deliberate, durable authorization and
   identity handoff accepted by the application, or the installer stops that
   unsupported path. Preserve fail-closed handling of unexpected pending images.
   The existing BBU1 marker is defined in the [USB standard](usb-device-configuration-standard.md#1-usb-selection-marker);
   preserve its narrowly bounded no-DC1 acceptance conditions. Do not invent a
   different marker, auto-create idle OTA state, bypass network-OTA validation
   or disable OTA to make an unsupported configuration work.
4. Local confirmation requires valid configuration and recovered persistent
   storage, progressing acquisition and a newly persisted reporting window under
   an explicit compatible time/failure budget where those capabilities apply.
   A sensorless base needs its own explicit health policy. Known degraded sensors
   do not alone invalidate firmware; network availability is a separate result.
   These checks retain the pending OTA draft's substance, not a weaker demo gate.
5. Provisioning readiness and OTA commissioning are distinct. An unprovisioned
   image can expose provisioning without proving acquisition readiness or OTA
   eligibility. If required local checks cannot run before provisioning, choose
   and review a bounded compatible startup path rather than auto-confirming it.
6. Configuration/queue schemas and identity must remain readable by fallback
   firmware or use an explicitly reviewed reversible migration. Never clear the
   queue or rewrite immutable DC1 to satisfy startup.

**Compatibility and decisions:** The existing BBU1 format and no-DC1 acceptance
path are governed by the [USB standard](usb-device-configuration-standard.md);
they are not newly proposed here. It does not reconcile arbitrary saved DC1/OTA
lifecycle state with new image bytes. Unsupported combinations still stop or
follow existing rollback; never fabricate an OTA assignment. Remaining work is
the exact source/synthetic startup matrix against the pinned bootloader, followed
by separately scoped physical acceptance for the unresolved combinations.
Preserve fallback, configuration and queue compatibility throughout.

### Diagnostics and degraded operation

Existing [transport recovery](transport-recovery-standard.md#i2c-recovery) already
requires bounded local recovery, unavailable state after exhausted retries, no
fabricated zeros and a fresh validated read before healthy status.
[Web Nodes](web-node-protocol.md) already preserve unacknowledged records and keep
sampling during catch-up; architecture separates acquisition, queue and delivery.

**Proposed clarification for review:** a failed sensor leaves the node running,
preserves queued records, and permits healthy independent channels to progress
with unavailable-state diagnostics for failed channels. This adds no universal
sensor model or wire field. Decide partial-channel representation in each
payload's compatibility contract; a generic serial DAT schema may need an error
or versioned partial-sample representation. CESH PR #50 reuses its existing nulls,
health flags and counters with bounded recovery; its exact drivers/models belong
in CESH, not this shared requirement. These source/host checks do not establish
hardware, outage or restart acceptance.

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
  pinning is follow-up work for that historical snapshot. CESH PR #48 at
  `b271889` pins the two-slot toolchain/direct libraries; single-slot environments
  and transitive dependencies remain distinct. Preserve resolved build evidence.
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
Existing CESH `INFO` does not report the factory base MAC. Earlier mandatory MAC
binding in the base proposal is deferred by the current provisioning scope;
see [identity and registry](usb-provisioning-standard.md#identity-registry-and-replacement).
No MAC handling is required for the current milestone.

## 8. Template adoption plan (proposed)

**Existing (template `main` at `9b46574`, 2026-10-12):** `software/firmware/` has
a 65-line esp32dev simulator with fixed `DEVICE_UID`/`FW_VERSION`, a single
`example_node` environment, the reliability headers, and no partition CSV,
runtime settings, OTA or host tests. Gaps: no shared/local config split, no
runtime identity, no partition recipe, no firmware CI, and two divergent
`BardBoxSensorHealth.h` copies (`firmware/include` and `software/firmware/include`).

Adoption steps, each a bounded template PR. Do not copy CESH acquisition logic.

1. Follow the merged [repository layout](repository-layout.md),
   then reconcile [device instructions](device-instructions.md) at `software/firmware/`.
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
6. Recording defaults ON (accepted direction) but the shared recording component
   is adopted only after its review and bench gates; OTA stays optional.

## 9. Evidence and limits

Historical evidence from `69795b5` (2026-10-12): CESH candidate
`cesh-shared_ota_bme680` 0.8.6, app SHA-256
`d3c1c76b43643826fcba8ce9a41ec457111504f801726da3ee9d709a44071e0a`, an
**unapproved TEST candidate**: built, validated by firmware-tools and dry-run
planned, never flashed. 30 firmware host tests passed then (local host tests,
not re-run for this consolidation). There is no hardware, sensor, network or OTA
acceptance of this document or candidate.
