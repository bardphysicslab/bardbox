# BardBox OTA updates v1

Status: draft for implementation and bench validation. Not yet a deployed capability.
Tracking: https://trello.com/c/BrELvFqi

Reference service: bardbox-project-template/software/app/ota.py. Operations and
the exact signed-byte encoding are in that repository's docs/ota-operations.md.
The service is opt-in via BARDBOX_OTA_CONFIG, independently of historical APIs.

## Scope and ownership

BardBox owns release policy, device targeting and update history. A replaceable
delivery provider stores and serves artifacts. Device installers enforce local
compatibility, authenticity and recovery. First implementation: ESP32-S3 over
outbound HTTPS. Other device classes implement the same outcomes with their own
installers. LoRa measurement transport does not imply LoRa firmware delivery.

Implement the shared reference in bardbox-project-template before CESH integration.
OTA administration is separate from the historical read-only Data API and MCP.

## Release and assignment contract

A release is immutable and identifies a component, version, exact image size,
SHA-256 digest, hardware/firmware target, partition-layout compatibility,
configuration schema compatibility, signing key identifier and signature.
The signature must bind the compatibility metadata to the image digest and size.
Specify signature algorithm, canonical encoding and test vectors before shipping.
Never treat a checksum alone as authorization to run an image.

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

An ESP32 installer writes only the inactive application slot. Reject oversized,
truncated, unsigned, modified or incompatible images before selecting the new slot.
Allow only approved artifact origins; redirects must not leak credentials.
Download retries are bounded and cannot monopolize sampling, storage or uploads.
Stream images to the inactive slot, not the measurement filesystem.

On planned reboot, persist completed measurements and record the update boundary.
Document partial-window handling and measure the acquisition gap. Do not clear
the queue to make an update succeed. Preserve configuration and queue compatibility
with the rollback firmware. Firmware images must not embed per-device credentials.

Verify the actual bootloader supports rollback. Confirm a new application only
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
