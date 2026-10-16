# BardBox OTA updates v1

Status: draft for implementation and bench validation. Not yet a deployed capability.
Implementation owner and acceptance tracking: https://github.com/bardphysicslab/firmware-tools/issues/10

Historical reference: the preserved template proposal and its source inventory are
linked from [Firmware Tools OTA tracking](https://github.com/bardphysicslab/firmware-tools/issues/10).
They are provenance, not an active template application or proof of an independent OTA service.

## Scope and ownership

BardBox owns the shared release, assignment, authenticity, compatibility and
recovery contracts. Firmware Tools owns the independently runnable optional OTA
application and its rollout workflow; USB flashing is a separate application.
Projects own their device installers, hardware configuration and acceptance.
A replaceable provider stores and serves artifacts. Neither USB nor OTA requires
the other application to be running; shared validation may be consumed through
explicit interfaces without importing another application's orchestration.
OTA administration is separate from historical read-only Data API/MCP access.
First reference work targets ESP32-S3 over outbound HTTPS; LoRa measurement
transport does not imply LoRa firmware delivery. Reference extraction and
independent-consumer evidence remain implementation work, not established by
merging this contract.

## Release and assignment contract

A release is immutable and identifies a component, version, exact image size,
SHA-256 digest, hardware/firmware target, partition-layout compatibility,
configuration schema compatibility, signing key identifier and signature.
The signature must bind the compatibility metadata to the image digest and size.
Specify signature algorithm, canonical encoding and test vectors before shipping.
Never treat a checksum alone as authorization to run an image.

The release SHA-256 covers the complete downloadable artifact, including any
appended platform digest. ESP32's `esp_partition_get_sha256()` may return an
appended image digest instead, so it is not a substitute for this artifact hash.
Persist candidate and previous artifact byte lengths with their hashes; hash
exactly those bytes when identifying the running image after restart.

The reference assignment parser accepts at most 4,096 bytes, exact fields without
duplicates, and positive 32-bit assignment generations. It accepts the server's
unescaped ASCII JSON values and rejects numeric coercions, escapes and unexpected
download paths. Artifact paths must equal `/ota/v1/device/artifact/<release_id>`
on the configured origin. Release IDs `.` and `..` are invalid URL path segments.

Device registrations declare component, target, partition layout, configuration
schema, queue schema and slot capacity. Require matching values on both server
and device. An image for another component is ineligible even if its target matches.

An assignment binds a registered device to an immutable release and has a unique
identifier and monotonically increasing device assignment generation. A rollback
is a new authorized assignment to a compatible older release. Do not infer
authorization from semantic version ordering. Persist the last handled generation
and failed assignment across restart; do not repeatedly install a failed release.

Commit complete assignment state before starting download or choosing a boot slot.
If a persistence outcome is uncertain, stop update actions until a verified reload.
Missing or corrupt update state must not silently become a new idle device. Initial
state creation belongs to deliberate commissioning. Reserve status-event sequences
durably before emission, including a new sequence after restart, and bound progress
report frequency to avoid excessive flash writes.

The server authenticates devices individually and derives identity from their
credentials, not a caller-supplied UID alone. Devices may read only their own
assignment and report only their own status. Artifact access must not expose
administration credentials. Use verified HTTPS, bounded requests and backoff.
Define certificate/key renewal before provisioning long-lived devices.

## Device lifecycle

Report assignment identifier, generation, release identifier, running version,
boot identifier and monotonic event sequence. Server receipt time determines status
freshness; replayed old events must not overwrite newer outcomes.

States: idle, assigned, waiting_for_transport, downloading, verifying,
pending_reboot, validating, confirmed, failed, rolled_back.
Offline/stale is a separate observation, not evidence of installation failure.
Report byte progress and bounded failure codes without credentials or raw secrets.
Assignment generations and event sequences are unsigned 32-bit values. Stop before
wraparound; never reuse a generation or sequence. A prepared event is immutable:
retry the same body after a lost response. After restart, reserve a fresh durable
sequence before creating a replacement report. HTTP 200 acknowledges a status;
retry transport errors, 408, 429 and server failures with backoff. Other 4xx needs
assignment/config reconciliation, not repeated unchanged submission.

An ESP32 installer writes only the inactive application slot. Reject oversized,
truncated, unsigned, modified or incompatible images before selecting the new slot.
Allow only approved artifact origins; redirects must not leak credentials.
Download retries are bounded and cannot monopolize sampling, storage or uploads.
Stream images to the inactive slot, not the measurement filesystem.

On planned reboot, persist completed measurements and record the update boundary.
Document partial-window handling and measure the acquisition gap. Do not clear
the queue to make an update succeed. Preserve configuration and queue compatibility
with the rollback firmware. Firmware images must not embed per-device credentials.

Verify the actual bootloader supports rollback and the application framework does
not accept the image before project validation. In Arduino ESP32, the installer
must override the weak `verifyRollbackLater()` hook with a strong C-linkage
implementation returning true; verify the linked artifact and physical behavior.
Initialize/recover persistent queue metadata before evaluating storage readiness.
Confirm a new application only
after bounded local checks show that acquisition progresses and persistent storage
and configuration work. Known degraded sensors need not make firmware invalid.
Network outages alone must not cause endless reboot/rollback cycles. Record cloud
reconnection separately from local boot validation. Define explicit timing and
failure budgets in each platform implementation and test watchdog-driven recovery.

## Operator page

Provide an authenticated Firmware updates page: upload/validate a signed release,
review compatibility, select eligible devices, explicitly assign, and inspect
current/assigned versions, last contact and outcomes. Restrict writes to an
authorized operator role; protect cookie-authenticated writes against CSRF.
Record actor, time, targets and release for each operation. Disable accidental
duplicate submission using idempotency identifiers. New devices never implicitly
join a rollout. Never display stale status as confirmed current health.

Stopping a rollout prevents pending delivery but cannot undo an already installed
image or reliably stop a device that has already downloaded its assignment.
Stage bench device, small accessible group, then explicitly promote to the rest.

## Provisioning and acceptance gates

USB preparation verifies physical board/flash size, partition layout, bootloader,
trusted keys and device configuration. Export queued measurements before any
filesystem-layout migration. Never format on mount failure as automatic recovery.
Keep USB recovery available and document the known-good build and exact toolchain.

Require automated rejection/authentication/idempotency tests plus bench evidence
for interrupted power/download, failed startup, wrong target, rollback, preserved
credentials/queue and sampling during flash writes. Measure actual record sizes,
offline retention, firmware growth headroom and reboot gap. A cached build or host
test is not evidence of successful device recovery. Record those results separately.

### Historical USB configuration reference

Current USB contracts are owned by [USB device configuration](usb-device-configuration-standard.md)
and [USB provisioning](usb-provisioning-standard.md). Their DB1/DC1 and mutable
settings boundaries govern current tools. The older reference below is historical;
it does not authorize replacing immutable records, invent current OTA commissioning
commands, or claim production credential enforcement. OTA commissioning remains
subject to its separately reviewed implementation and acceptance.

The historical ESP32 reference keeps an explicitly commissioned configuration record in its
own NVS namespace, separate from OTA lifecycle state and the measurement queue.
It contains stable UID, Wi-Fi credentials, telemetry endpoint/authentication,
verified HTTPS trust, OTA origin/device credential/signing public key, and the
known-good artifact's exact length and SHA256. Signing private keys remain off
node. The record is bounded, versioned and checked for accidental corruption;
CRC is not authentication or encryption. Physical USB access is a trusted
commissioning boundary. Never echo the record or credentials in diagnostics.

First provisioning may resume an interrupted identical write but must not replace
an existing different record or reset handled assignment state. Missing/corrupt
configuration disables OTA; it never triggers erasure or automatic reprovisioning.
Load the commissioned record at boot; serial commissioning does not silently
change the identity of a running acquisition session or reboot the device.
Legacy builds may retain their existing compiled configuration until deliberately
migrated. Shared release builds must instead require a valid commissioned record
and contain no per-device credentials. Keep rollback targets compatible with that
configuration format. Certificate/key/Wi-Fi rotation needs an explicit maintenance
flow; initial commissioning is not a general remote configuration interface.


### ESP32 local validation and restart boundary

The reference local acceptance policy requires valid persistent configuration,
healthy storage and at least one newly persisted reporting window while acquisition
continues to progress. A 150-second budget covers the CESH 120-second interval;
other reporting intervals must select an explicit compatible bound. Network
availability and individual degraded sensors do not decide firmware acceptance.
Only mark an SDK-pending candidate valid after these local checks. Unexpected
pending images or missing/corrupt lifecycle state fail closed to the SDK rollback
path rather than being implicitly accepted.

Before a planned update restart, wait for a completed window to persist and pause
acquisition at that boundary, retain an audit marker in NVS, then restart. Bound
the wait to one reporting interval plus margin; failed storage/boundary persistence
must cancel the planned restart and restore the running boot selection where
possible. Never clear the measurement queue to satisfy this gate.


Governance synchronization: the root AGENTS.md and ARCHITECTURE.md require
optional-capability classification, canonical ownership, documentation,
recovery testing and deployment gates. This contract adds no separate agent workflow.
Physical offline queue/replay, power-loss, autonomous recovery and long-term retention
acceptance remain incomplete. This document is not pilot or deployment approval.
