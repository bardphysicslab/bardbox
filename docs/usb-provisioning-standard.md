# USB flashing and provisioning (proposed)

Status: proposed shared contract, audited October 15, 2026. Source observations
and maintainer scope below are not adoption of a new protocol. No consumer
conformance, physical acceptance or operational authorization is implied.
Design owner: [BardBox #31](https://github.com/bardphysicslab/bardbox/issues/31).
Implementation/evidence owners: [Firmware Tools #5](https://github.com/bardphysicslab/firmware-tools/issues/5),
[provisioning #8](https://github.com/bardphysicslab/firmware-tools/issues/8),
[CESH integration #25](https://github.com/bardphysicslab/cesh-air-monitor/issues/25).
Entry point: [firmware blueprint](firmware-blueprint.md).

Provenance: imported October 14 from `codex/usb-provisioning-standard` at
`ab83ab376475d7ef8adea57aa720b67726857340` (October 9). The historical
coordinator evidence below is preserved; its registry and single-Flash design
does not define the current milestone.

## Current scope and separate outcomes

Firmware Tools main at `52d4b8ed7d7127e2932e0131bf6b15ebf135b896`
has Set up device and Check device. Provisioning is separate work in #8.
Do not describe one integrated flash/provision/healthy-boot operation as delivered.

Report these separately: approved write/read-back verification, selected image,
observed running firmware, local health confirmation, provisioning readiness,
receiver acknowledgement and OTA commissioning. A verified write or an INFO reply
alone proves none of the later outcomes. Saving settings is not evidence of
restart persistence, network access, fresh measurements or authenticated admission.

Check device sends INFO once and displays received text without required fields,
field validation or pass/fail interpretation. It can display legacy CESH output,
errors and unrelated text. Silence/disconnection is not proof of unsupported
provisioning. Installer identity/security/layout/image/write-range checks remain
independent of interpreting this readout. See maintained
[adapter source](https://github.com/bardphysicslab/firmware-tools/blob/52d4b8ed7d7127e2932e0131bf6b15ebf135b896/packages/usb-browser/adapters/serial-info.js).

## Provisioning milestone

The [latest maintainer scope](https://github.com/bardphysicslab/firmware-tools/issues/8#issuecomment-6204491290)
uses one reusable provisioning module, one shared field-definition file and the
existing device record/commands. Projects supply supported values/configuration;
mandatory project-specific field providers or an extension framework are not
required. New form fields do not extend firmware storage or wire formats.
The implementation and operating instructions belong in Firmware Tools, with
CESH owning device support and acceptance.

Initial DC1 commissioning uses PROVISION_BEGIN/DATA/COMMIT. CESH validates
the record, trust material and running-image length/hash, then stores it for
next-boot activation. Existing different/corrupt records are not overwritten;
an identical record can be retried. Later Wi-Fi-only changes use the separate
WIFI_* override flow, preserving UID and immutable DC1 rather than recommissioning
the whole device. General settings/identity maintenance remains a proposal in the
[serial/base API](firmware-base-and-serial-api.md#runtime-settings-and-new-wire-commands).

A commit reply lost after transmission leaves an uncertain outcome; even a
device-reported commit error does not prove no durable bytes were written.
PROVISION_STATUS loaded/stored flags do not identify the saved record. Reconcile
uncertainty with the identical retained record only, without blind replay,
replacement, token regeneration or automatic erase. A fresh session observing
stored configuration must not propose a new initial record. Keep secret values
out of readouts, logs and persistence on the host; mask review values.
These boundaries follow the existing device store and
[provisioning review](https://github.com/bardphysicslab/firmware-tools/issues/8#issuecomment-6204390412);
they introduce no new command.

## Identity, registry and replacement

Current provisioning enters or preserves the existing BardBox node UID including
its instance. It does not generate a new identity scheme. Preserve existing CESH
identifiers; the deployed CESH naming and the published
[node naming standard](node-naming-standard.md) differ, so do not silently
normalize existing IDs or rewrite historical records.

No MAC integration, allocator, registry/reservation or credential-management
implementation belongs in #8. Required existing trust/token fields still need
valid compatible inputs; this is not permission to create real credentials.

The full factory-programmed base MAC is a candidate physical-board lookup key for
the deferred [Device registry #41](https://github.com/bardphysicslab/firmware-tools/issues/41)
and its [planning board](https://github.com/users/bardphysicslab/projects/5).
It is neither an authentication credential nor sensor/wiring evidence nor a
replacement for the application UID. Runtime interface MACs and USB vendor/product
filters do not establish that factory identity. Registry authority, replacement,
issuance/revocation and admission enforcement stay in that deferred workstream;
the existing registration component is implementation evidence, not proof of
production authority or completed integration.

## Write boundaries and OTA compatibility

Source matrix at Firmware Tools `52d4b8e`: `workflows/setup.js` dispatches
install/recover/recover-layout to `flashOpenSession` using `flash-plan.js`;
update/reinstall-same use `slot-update.js`. These are USB paths, not network OTA.

| USB path | Planned writes and selection metadata | Limits |
| --- | --- | --- |
| Verified-erased install | Approved bootloader, partition table, fallback app0 and 8192-byte all-FF otadata reset for this dual-slot recipe | No NEW entry written; erased fallback is not proof of application health; blank-device end-to-end physical acceptance remains unverified |
| Older/different/unreadable-layout recovery (recover-layout) | Same approved install plan, including all-FF otadata reset | Explicit data-loss confirmation; old settings/queued records may overlap new writes or become inaccessible |
| Same-layout recovery (recover) | Same approved install plan, including all-FF otadata reset | NVS/data regions remain outside writes and reachable under the same table; retained schema compatibility and saved OTA lifecycle still need checking |
| Inactive-slot update, including Install again | Write/read back inactive app, then selection entry NEW; an erased starting record also gets an UNDEFINED record for the prior app | Preserves the selected app bytes; NEW/PENDING_VERIFY health confirmation and lifecycle compatibility remain separate |

The installer writes no NEW selection entry in the first three rows. A compatible
rollback-enabled bootloader can transition NEW to PENDING_VERIFY on startup;
this must not be generalized to erased metadata. The
[upstream ESP-IDF v4.4.7 source](https://github.com/espressif/esp-idf/blob/v4.4.7/components/bootloader_support/src/bootloader_utility.c)
distinguishes erased fallback and writes its initial selection VALID. That is
source reference evidence, not verification of the exact pinned CESH bootloader
binary or proof it passed the application's checks. VALID can also be created by that erased-fallback bootloader path; it does not
by itself prove application-level health checks or current sensor health.

At CESH `24c2305ff1834368a0a86a90592bb71faba91d65`,
`CeshOTA.cpp` defers framework acceptance with verifyRollbackLater().
rollbackOnce() attempts rollback only when sdkPending() is true. A pending
USB-selected image without matching PendingBoot/Validating lifecycle state is a
real integration gap. Unprovisioned shared firmware stops normal acquisition
independently of whether boot metadata is pending. All-FF install alone proves
neither unavoidable rollback nor commissioned OTA. Follow the
[corrected source review](https://github.com/bardphysicslab/cesh-air-monitor/pull/50#issuecomment-6204677421).

Verify all padded write ranges and explicit metadata writes by read-back; image
identity hashes exclude padding. Never whole-chip erase as normal recovery.
Check the complete approved bootloader region, layout, selected image/history,
security and fingerprint again before allowing the exact confirmed ranges.
Preservation claims apply to the inspected layout, not arbitrary old layouts.
The one memory map stays in the
[blueprint](firmware-blueprint.md#5-flash-memory-one-8-mib-esp32-s3-recipe).

The substantive shared health/commissioning decision remains
[proposed in the blueprint](firmware-blueprint.md#boot-validation-and-rollback-compatibility).
Do not disable OTA or accept an unexpected pending image to make a demo work.

## OTA document authority

`docs/ota-update-standard.md` is absent from BardBox main `da62d8d`.
Its actual maintained proposal is
[PR #16 at 7b947be](https://github.com/bardphysicslab/bardbox/blob/7b947be081d1d1fb646849c15e9491fbdce1297b/docs/ota-update-standard.md),
not an adopted main standard. Keep one draft there; do not create a replacement.
CESH main's firmware README, device-provisioning and ota-readiness documents
still name the absent main path. Their writer should replace those references
with this pinned draft/status and preserve the owning implementation's evidence.
Adoption/compatibility with the USB contract needs independent review.

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


## Next step

Independent review of the factual corrections and the bounded startup proposal
in PR #32. CESH #25/#49 own the exact pinned-bootloader startup matrix and project
acceptance; Firmware Tools #8 owns current provisioning. Kornelis relays any
implementation coordination. The older coordinator's review/physical trial is
historical unfinished work, not the next authorized milestone.
