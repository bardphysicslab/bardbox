# Optional Web Node live previews

Status: proposed optional capability `live-preview-v1`; not evidence of deployed support.

## Compatibility and acknowledgment boundary

The base protocol remains `web-node-v0.2`: archival uploads still drain FIFO and HTTP 2xx on the archival endpoint acknowledges durable acceptance. This optional capability adds a distinct preview operation; its 2xx acknowledges preview receipt only and NEVER authorizes queue deletion. Existing firmware and servers remain supported without this capability. Any incompatible change to the base archival contract requires separate protocol version review.

Deploy the compatible server before enabling nodes. Projects must document capability discovery, dedicated preview routing, authentication and explicit preview acknowledgment. Never send a preview to a legacy archival endpoint. Unsupported capability/endpoint responses disable previews with bounded retry/backoff; ordinary FIFO archival continues. Merely receiving arbitrary 2xx from a catch-all route does not establish preview support.

## Node responsibilities

Persist every immutable completed measurement record before making it eligible for either path. During backlog recovery send the newest completed record promptly as a preview, while continuing bounded oldest-first archival. Schedule both paths without starving acquisition, persistence, previews or history. After catching up, ordinary archival uploads serve current readings and redundant previews stop; the acknowledged queue can become empty.

Assign stable record identity before persistence, preserved across retries and reboots. A durable sequence or persisted boot/session identity plus sequence can work; timestamps alone cannot identify records. A live preview and its later archival delivery carry the same identity. Legacy records lacking IDs require a documented migration/deduplication policy; never discard distinct equal-timestamp observations.

## Server and display responsibilities

Separate three independently ordered states:
- latest valid measurement, ordered by trusted measurement time with explicit tie/clock handling;
- operational status captured at send time, with session/sequence ordering to reject delayed status;
- durable archival progress.

Previews update only the current measurement view. They do not append measurement CSVs or advance archival confidence, scoring or aggregation. Archive the record once when FIFO reaches it, even if already previewed. Durable deduplication must survive lost acknowledgments and crashes, including a crash between CSV append and deduplication-state update. Document reconciliation or transactional journaling rather than claiming exactly-once from an in-memory set.

Historical uploads cannot replace newer displayed measurements. Report current buffer count/capacity, catch-up state and upload progress separately from diagnostics frozen inside historical records. Status freshness must expire: a disconnected node is not indefinitely shown as actively catching up. Maintain existing stale/null API behavior. Define restart recovery for latest previews; recovered history must not be presented as fresh.

## Archive ordering and backups

Use one ordered archival writing stream. Live previews wait in the durable node queue for their archival turn. Preserve original measurement and receipt times. FIFO preserves acquisition order, not necessarily timestamp order after clock changes. Document invalid-clock, clock rollback, reboot, equal-timestamp and UTC-day partition behavior without silently rewriting source timestamps.

Do not require SQLite or whole-file rewrites per reading. Preserve existing CSV/API consumers and explicitly document any exception to timestamp ordering.

For deployments deferring backups during catch-up, coordinate file eligibility with archive writers using locks, immutable snapshots or equivalent version boundaries. A stale status or missing fields on legacy nodes must not cause indefinite silent deferral. Other nodes remain eligible; completed daily files may be backed up only when their stability is established, not merely because their date is old. Surface prolonged deferral and provide a bounded fallback that backs up a consistent partial archive without permitting unsafe retention.

When catch-up completes, all changed files, including prior days, become eligible at the next scheduled backup. Copy and verify the exact selected version. Manifest/retention eligibility applies only to that version; subsequent mutation invalidates eligibility. Pausing backup alone neither sorts files nor removes writer/copy races. Drive scripts and scheduling remain deployment-specific.

## Required conformance scenarios

Test mixed legacy/new nodes and servers; unsupported preview endpoint; multi-hour outage; continuing acquisition; non-starvation; latest display plus changing buffer progress; delayed historical diagnostics; live/history overlap; lost ACK; restart at append/deduplication boundaries; cross-day backfill; invalid/rolled-back/equal timestamps; preview expiry and server restart; backup during append and catch-up completion; exact-version verification and retention; prolonged deferral.

Record software tests separately from physical one-node outage/soak evidence. Bump firmware versions for behavior changes. Optional capability support must be advertised only after implementation and validation.
