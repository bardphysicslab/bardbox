# Optional BardBox firmware buffer API

Status: design proposal, October 14, 2026; merged with PR #32 on October 16 as a
proposal. October 19 accepted direction ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991) items 6–7) changes the default and
the preferred full-buffer policy below; neither is implemented. No shared library, build, adoption,
hardware acceptance or deployment is claimed. Existing required behavior is in
[Web Node Protocol](web-node-protocol.md); serial integration is in the
[firmware/serial proposal](firmware-base-and-serial-api.md).

## Responsibility

One maintained module owns durable records, FIFO order, recovery,
capacity accounting and removal after delivery acknowledgement. Acquisition,
aggregation, time synchronization, serialization policy, networking and server
archival storage remain separate. Use CESH's existing implementation as evidence
and an extraction candidate, not parser/storage code copied into each main.cpp.

RKC supplies individual temperature/door readings so averages do not hide
excursions. CESH supplies completed aggregate records. Reporting less frequently
does not inherently require averaging; aggregation remains CESH's chosen policy.
Recording defaults ON for every device running BardBox firmware, including
serial-connected nodes, so this module is part of the default base; a project
may only omit it deliberately. Vendor instruments not running BardBox firmware
are outside this requirement. Boards with little or no spare flash (for example
current RKC firmware, which has no queue) need a capacity and wear assessment
before adopting it; the default does not by itself make every board capable.

## Proposed C++ interface

`BardBoxBuffer buffer;` creates an instance with one queue owner and one active
delivery consumer. Calls run when invoked; no automatic background thread.

| Operation | Contract |
| --- | --- |
| begin(storage, options) | Open/recover existing storage; no automatic format; explicit startup/recovery status |
| append(record) | Admit an immutable bounded record for durable saving; return operation ticket or explicit rejection |
| poll(nowMs) | Progress storage operations in bounded steps; document hardware blocking limits |
| operationStatus(ticket) | Pending, durably completed or failed, with structured error; covers append, acknowledge and clear |
| peekOldest() | Copy oldest durably saved record with its generation/record token; does not remove or hold a lock during network work |
| acknowledge(token) | Request durable removal of exactly that head after protocol acceptance; return ticket/result |
| status() | Pending count, configured limit, bytes used/available, health, quarantined bytes, pending operations and loss counters |
| clear(maintenanceAuthorization) | Explicit destructive asynchronous discard under injected authorization policy |

Asynchronous tickets allow honest bounded service; accepting append is not a
durability guarantee. Project/template retains the record until durable success
and handles admission failure. Pending RAM must be bounded and cannot silently
drop records. Queue operations are serialized; acquisition can submit new records
while delivery sends a copied head. Exact types/header and memory limits are next
implementation decisions, not supplied by this document.

## Record envelope

Each record contains a stable ID, acquisition-time UID, record/schema version,
record kind (individual or aggregate), bounded payload and supplied time metadata
with validity. Preserve original values and attribution through retries, restarts,
config/UID changes and decoder upgrades. The buffer does not invent UTC. Storage
framing has its own explicit version/integrity check; it is distinct from scientific
schema and wire-protocol versions. Credentials are not part of stored measurements.

## Delivery and replay

Save durably before first normal delivery; peek a durable record; send via the
separate delivery module; acknowledge only on the configured successful server
response; verify durable removal before proceeding. Failed/ambiguous delivery
keeps the record. Failed cursor commit also keeps it eligible for retry. Only
accepted archival delivery acknowledges a record; the optional
[live-preview path](web-node-live-preview.md) never removes history.

Tokens include queue generation and stable record ID. Stale/mismatched tokens
cannot delete a different head, including after clear/reinitialization. A repeated
acknowledgement has an explicit already-completed outcome. Repeating an append
with the same ID/content must resolve the prior outcome or report duplicate;
conflicting contents fail. Retry/status history is bounded: define its retention,
and report unknown expired outcomes rather than claiming infinite idempotence.
Server-side stable-ID deduplication is separately required to avoid duplicate
historical rows when acceptance responses are lost.

## Recovery, fullness and maintenance

Flush/commit success means durable according to the documented storage adapter.
Interrupted appends preserve verified complete records; incomplete/corrupt frames
are reported/quarantined, never treated as valid. Preserve cursor before deleting
consumed chunks. Failed mount never formats existing data. Recovery scanning
has bounded service behavior and reports when the queue is not yet ready.

**Preferred saturation policy (accepted direction):** keep the oldest
unacknowledged record as an anchor and evict the oldest *unprotected* record to
admit the newest; retained records still deliver oldest-first. Eviction is loss:
never an acknowledgement, never ordinary upload-failure recovery. Keep a bounded
durable loss count (the `status()` loss counters) and report it to the server's
central error log when communication permits; no new loss UI. Eviction must not
invalidate an in-flight delivery token. Token safety, power-loss recovery, tiny
capacities and an explicitly blocked FIFO head still need engineering detail;
the existing blocked-head behavior remains the safe initial rule and no
automatic skip is authorized. RejectNew, CESH's current implementation, is no
longer the preferred monitoring default but remains documented existing
behavior until migrated. Physical space
and logical record limits are independent; quarantine and failed deletion consume
space. Capacity changes cannot silently truncate a queue. No fixed retention-day
promise without record size/cadence and real filesystem measurements.

Clear requires a deliberate maintenance capability, records discarded count and
outcome, and invalidates pending delivery tokens. Its power-loss semantics must
be specified/tested before exposing the command. Formatting is separate from
clearing and is not part of this API proposal.

## Compatibility and CESH evidence

CESH uses compact lossless chunks, integrity framing, legacy CSV read support,
metadata recovery and FIFO acknowledgements. It caps records and rejects new
ones when full. Corrupt chunks retain verified prefix/damaged bytes; six-digit
chunk numbering has an exhaustion guard. Production extraction must address
sequence longevity, metadata-write wear and physical filesystem timing.

Reviewed source: CESH 345b6bb7b18bd3d7eb7eb33b3bc7550a69021110; RKC
0c4f9238a7c85f282a69d92f4142c6eea06f184e. Existing CESH production queue
fault test re-run October 14: 1 passed using simulated LittleFS and compiler
sanitizers. No new physical power-loss/retention/outage evidence. See the owning
[compact-storage evidence](https://github.com/bardphysicslab/cesh-air-monitor/blob/main/docs/compact-storage-validation.md).

**Append reference** (accepted modeling baseline,
[FW-BUFFER-REF-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6289854963), October 20, 2026). Source: CESH
`3913ca9f6837c252f1e73494bf7466c1f66eb765`,
`software/firmware/esp32-air-node/src/main.cpp`.
- `appendReadingToBuffer(csvLine)` runs under the buffer mutex and returns `bool`.
- It rejects with `lastBufferError` set for a full queue (`buffer_full`, by
  record count or free space), an invalid record size and an exhausted chunk
  sequence.
- It appends the framed bytes (delta-encoded after a chunk's first record),
  flushes and closes the file, then updates and saves the queue metadata. It
  returns `true` only after that metadata save succeeds.
- The acquisition task increments `windowsDropped` when it returns `false`.
- Delivery and acknowledgement are separate operations.

This is the existing reference implementation to model and extract around. The
interface above (append ticket, `operationStatus`, durable completion) remains
the proposed target. This record does not adopt a boolean over it, a universal
preserve-or-drop rule, a generic extraction or physical power-loss acceptance.
Concrete gaps between the reference and that target:

- One `bool` merges admission rejection (full, invalid size, exhausted
  sequence) with write and metadata failures, and has no pending outcome. The
  proposed ticket and `operationStatus` keep admission, pending and durable
  completion apart.
- A short write, or a metadata save that fails after the frame was written,
  returns `false` and marks metadata for rescan. In the second case a record the
  caller counts as dropped may still be found on rescan (inferred from the
  source, not verified on hardware). The target needs an explicit uncertain or
  failed outcome rather than an implied drop.
- In `appendReadingToBuffer` itself, the delta-encode and framing failure
  returns do not set a new `lastBufferError`, so the reported reason can be stale.
- `flush()` and `close()` success means durability only as far as the LittleFS
  adapter guarantees it; physical power-loss behavior is unproven.
- CESH's caller counts a failed append as a dropped window. Whether a failure is
  preserved, retried or dropped is caller/project policy and is not settled here.

Firmware updates/rollback must check supported queue formats and retain old
decoders until old records drain, or use an explicitly reversible migration.
Preserve the data partition during normal firmware installs. Serial responsiveness
also needs bounded delivery: CESH's synchronous HTTP calls currently precede serial
service and can delay it despite separate acquisition. Do not import that limitation
into the shared buffer interface.

## Acceptance and next step

Implement one independent maintained component and two synthetic consumers
(individual and aggregate). Verify original data/order, append/ACK failure and
retry, partial writes, restart, mount failure without format, full policy/loss
visibility, stale tokens, concurrent append while sending, schema upgrade/rollback,
bounded service, and simulated-clock tests. Then measure physical flash behavior,
power interruption, heap/timing/endurance and achievable retention separately.
No CESH/RKC migration or hardware operation is authorized by saving this proposal.
Exact API types and scheduling limits remain open for implementation review.

Tracker: [API design](https://github.com/bardphysicslab/bardbox/issues/31); entry point:
[firmware blueprint](firmware-blueprint.md). The
[compact storage proposal](https://github.com/bardphysicslab/bardbox/blob/7b947be081d1d1fb646849c15e9491fbdce1297b/docs/compact-record-storage.md)
(merged October 16 as a draft, not adopted) owns the proposed binary framing,
recovery scan and ACK-cursor rules; this API links to it and does not define a
competing format. Current copy: [compact record storage](compact-record-storage.md).
