# USB flashing and provisioning (proposed)

Status: proposed shared USB assembly contract. Documentation only; this does not
establish consumer conformance or authorize hardware operations.
Tracker: [firmware-tools #5](https://github.com/bardphysicslab/firmware-tools/issues/5);
design entry point: [firmware blueprint](firmware-blueprint.md).

Provenance: imported 2026-10-14 from `docs/usb-provisioning-standard.md` on
`codex/usb-provisioning-standard` at `ab83ab376475d7ef8adea57aa720b67726857340`
(written 2026-10-09). That branch's serial proposal was already consolidated into
[firmware-base-and-serial-api.md](firmware-base-and-serial-api.md) and is not
repeated here. Edits on 2026-10-14 mark the immutable DC1 record as existing CESH
behaviour, point the otadata question to its single open decision and label the
implementation evidence as historical. Source governing commits:
engineering-standards `3bf9c600b35f73322e8f610baffec2b682bdcc77`, BardBox
`da5132a648d21989a984e00fa1fd02760bcdf4f7`.

## One assembly operation, distinct results

The assembly interface has one primary **Flash** action using the current
approved bundle for the selected supported hardware profile. It has no firmware
catalog or arbitrary file picker. The intended sequence is:

1. Identify the connected board and check target compatibility and security state.
2. Flash the approved binary and verify the complete planned write ranges.
3. Provision per-device settings over USB into persistent configuration storage
   (ESP32 NVS), separate from the firmware image, OTA metadata and measurement queue.
4. Verify the stored configuration without exposing passwords or keys.
5. Deliberately restart and check the running firmware and reported identity.

Report flash verification, provisioning verification and boot verification
separately. Successful writing alone is not proof of a healthy running device.
If provisioning fails, say that firmware was written but setup is incomplete;
retry the unfinished step rather than silently repeating the entire operation.
A registry reservation is not proof that hardware was successfully provisioned.

Use a shared approved binary; do not patch its bytes with identity, Wi-Fi or
credentials. Runtime settings are loaded from persistent storage. Board and
sensor selections that change compiled drivers select a matching approved
build; provisioning cannot turn an incompatible binary into another build.

Physical binding after reset uses the MAC reported by the running firmware;
USB vendor/product filters identify only the board type
([USB identity](firmware-blueprint.md#7-usb-identity)). The proposed base INFO
reports MAC and unprovisioned state; existing CESH INFO does not.

## Configuration and assembly choices

Project engineering configuration owns the project label, fixed UID prefix,
server endpoint, supported boards, sensor choices, defaults and compatible
bundle mappings. Keep this configurable for CESH, RKC and future consumers.
Firmware config.h defines configurable fields and build defaults; USB provisioning
supplies supported per-device runtime values. Their schema and precedence must
agree, rather than maintaining two unrelated sets of settings. The proposed
device-side settings contract is in the
[serial/base API](firmware-base-and-serial-api.md#runtime-settings-and-new-wire-commands).

Assembly chooses the instance number and Wi-Fi SSID/password, plus configured
hardware choices. An empty Wi-Fi password means an open network; derive the
firmware's password-present flag from that value. Assembly cannot edit the UID
prefix or server endpoint. Location, coordinates and ownership remain server-owned.

The CESH pilot uses project CESH-AIR and prefix bb-cesh-air-. It offers ESP32-S3,
BME280 (default) or BME688, and a single paired choice of two PMS5003 (default)
or two PMS6003. Mixed PM pairs are excluded. An offered choice requires a matching
approved bundle before hardware flashing is enabled. These are project settings,
not mandatory hardware for every BardBox project.

Existing CESH identifiers are preserved. This proposal does not change the
[node naming standard](node-naming-standard.md) or invent a new naming migration.

## Identity, registry and replacement

The registry service owns availability and credential lifecycle through an API;
the application does not issue database queries. A database adapter isolates
storage choice. SQLite is the isolated pilot implementation, not a mandate for
all deployments. Offline devices remain assigned. Check availability and reserve
atomically; do not automatically allocate a new number in this pilot. Firmware
has no registry client; it validates, saves and reports the supplied UID
([ID changes and registry ownership](firmware-base-and-serial-api.md#id-changes-and-registry-ownership)).

A normal reflash retains the device's identity and supported persistent settings.
Reflashing an already used device does not require a backup or a new-device-only
baseline. Firmware updates must not silently erase provisioning or queued data.
An explicitly approved storage migration needs its own preservation decision.

Replacing an occupied instance requires a clear warning, additional engineer
credential verification and a check that the registry revision has not changed.
Keep the UID and historical measurements/metadata; update the current hardware
assignment/configuration and revoke the previous device credential. Issue and
provision a new device credential through an explicit service operation. Never
claim that deleting the previous key automatically creates a replacement key.

Initial provisioning must not overwrite a different existing configuration.
Intended direction: explicit, coordinated UID, settings and credential maintenance
through revision-checked settings transactions; secrets are set-only and never
echoed. **Existing:** CESH DC1 is immutable and has no maintenance contract, so
registry replacement alone cannot change a provisioned device's record today.
Legacy keyless access, if temporarily needed, requires explicit per-device policy.

## Write boundaries and OTA compatibility

Keep image length distinct from sector-rounded write length. Verify every byte
of each planned write range, including padding and any explicit metadata reset,
by reading it back and comparing it with the intended bytes. This verifies the
written regions, not untouched flash or boot health. Avoid a whole-chip erase.

Review existing partition layout, OTA metadata and selected boot slot before
writing. A first-install plan may reset otadata to select app0. Whether a USB
reinstall onto a device that has run an OTA-installed image may reset otadata is
an [open decision](firmware-blueprint.md#write-plans-initial-install-reinstall-and-ota);
this draft's caution that a later update must not blindly reset it, since that can
select an old or unwritten application, is one input to it. Write only the approved
plan's ranges and keep NVS and measurement storage out of those ranges. A
partition-layout change requires a separate migration plan. The one maintained
flash table is in the [firmware blueprint](firmware-blueprint.md#5-flash-memory-one-8-mib-esp32-s3-recipe).

Preserve the existing engineering bench and its physical installation,
comparison, restoration and full-read evidence. Adapt its reviewed implementation;
do not recreate the installer or repeat hardware acceptance solely for UI changes.
The engineering bench, inspection-only assembly page and current-bundle simulation
are different tools and must be labelled accordingly.

Related pending OTA/storage proposal: [PR #16](https://github.com/bardphysicslab/bardbox/pull/16)
(`ota-update-standard.md` at `7b947be`) contains the OTA lifecycle and a reference
USB configuration record. It is pending, not merged authority. Reconcile this USB
contract with that proposal before promoting their shared configuration or
maintenance interfaces.

## Historical implementation evidence (2026-10-09)

Recorded at `ab83ab3`; not re-run for this consolidation.

- The firmware-tools TEST assembly coordinator was implemented and software-tested
  at firmware-tools commit `bacc8842a2c906be6058cd76f4af6bd1f5223b25`. On
  2026-10-14 that commit was present in the local firmware-tools clone but on no
  firmware-tools remote branch. Its preservation is outside this BardBox task.
- It reused the existing Flash executor and the preserved DC1 protocol, with
  configured current bundle mapping, atomic one-time credential issuance and
  separate flash/provisioning/boot outcomes.
- A served page/API simulation passed initial setup and a second reflash retaining
  settings/key. This is **simulated** evidence; the hardware handoff/reset
  composition still needs its narrow physical integration trial.
- Existing USB flash verification and separate CESH provisioning have physical
  evidence recorded in firmware-tools #5, preserved for their original scope.
- The TEST replacement operation stages the assignment and removes old
  credentials; new key issuance and physical provisioning remain separate work.
- Production registry/key enforcement and OTA commissioning are not established.

Behaviour of that coordinator with existing DC1: issued/activated devices can
retain configuration on reflash, but a newly staged replacement cannot be
commissioned by accepting an old stored record. An explicit retry reuses identical
in-memory record bytes; lost key responses/reload do not automatically rotate
credentials. In the isolated TEST record, one random token is supplied to OTA and
telemetry fields; production credential purpose and server enforcement remain
separate integration work.

## Next steps (unchanged from the source, still pending)

Independent code review of the coordinator, then an explicitly authorized physical
integration trial on a compatible unprovisioned spare. Keep production integration
and record maintenance in separate approved steps. Template and other-consumer
adoption are deferred pending contract review; CESH is the pilot, RKC requires
project-specific configuration and validation. No runtime code, deployment,
service restart or hardware operation is included in this documentation.
