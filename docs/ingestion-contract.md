# Ingestion contract

Status: proposed shared contract for the separate server template. Documentation
only; adoption requires independent engineering review and consumer migration.
The [approved consolidated draft](https://github.com/bardphysicslab/bardbox-project-template/issues/15#issuecomment-6226274159)
and its recorded approval settle the product direction. This document resolves
the remaining engineering details without reopening those decisions.

## Ownership and operation

Check against the [BardBox Architecture Map](architecture-map.md).
Communications authenticates, enforces finite framing/size/rate/work limits,
decodes the supported transport, and captures `received_at` when the complete
message arrives. A source adapter translates documented wire fields and units.
Ingestion validates the translated observation against authenticated identity
and registry definitions, without owning transport, persistence or display.

The operation is `validate(record, delivery, registry_snapshot)`. It returns
`record`, `delivery`, and `errors`; `record` is null for envelope rejection.
`errors` is an array of `{code, path}` objects; paths use dotted field names.
An accepted result has an empty `errors` array. Channel faults are inside the
accepted record, not envelope errors. No validation result is a durable ACK.

Registry owns identity bindings, stable archive device keys, configured link type
(`wifi` or the explicitly registered non-Wi-Fi link), device names, locations,
latitude/longitude, registered channel definitions, required versus optional
channels, validators and per-device cadence configuration. Link type comes from
Registry, not an adapter name or untrusted payload, and determines the Wi-Fi RSSI
requirement. Ingestion reads one consistent snapshot. Archive owns durable
storage, conflict detection and
deduplication. Latest state, health, science, alarms and query/rendering consume
accepted records through their respective interfaces. Display configuration is
separate from registration; incoming fields never add card rows.

User-entered settings enter through the authorized control API, not measurement
ingestion. Registry validates, persists and applies device names, locations and
coordinates; queries read that descriptive metadata from Registry by UID. The
persistent configuration owner validates, persists and applies project settings,
including project cadence defaults and backup policy. Reject invalid edits before
changing stored or active values. Rendering may provide early feedback but cannot
replace server validation. Query/rendering joins server-managed descriptive
metadata to readings by UID; a renamed freezer keeps its device identity.

Ingestion has no persistent state or external writes. Rejected input cannot
update validated latest measurements or scientific/alarm inputs. Communications
may record bounded rejection/contact diagnostics separately. For archival input,
publication follows archive acceptance; preview publication follows validation
under the separate [preview contract](web-node-live-preview.md), without an
archive ACK or archival science side effects.

## Diagnostic logging independent of rendering

Ingestion-detected errors and faults must be available in the shared central
application log for maintainer investigation, independently of dashboard or
Health rendering. Preserve `validate(record, delivery, registry_snapshot)` as a
pure operation with no external writes: it returns structured errors and fault
annotations; the calling application layer reports those outcomes through the
shared logging interface. Logging is not another responsibility of the validator.

Record rejected-envelope errors and accepted channel/metadata fault outcomes with
available event time, reporting component, processing stage, structured reason and
usable device/record identity. Keep unavailable identity/time explicitly unknown;
do not invent values. Bound entries and avoid credentials or unnecessary raw
payloads. Optional-channel `not_reported` annotations and ignored unregistered
channels do not by themselves require error entries. The precise logging API and
severity mapping remain implementation choices to review before coding.

Operational modules report failures they detect through the same interface; the
application caller reports failed operations returned to it. A module need not
know whether another module or the UI displays its failure. The logging facility
owns collection, output/storage configuration and retention; ingestion owns none
of those. This is a shared application facility, not a separate per-module store
or a requirement to select an external logging service.

Diagnostic entries do not establish durable acceptance, update validated latest
measurements, authorize an ACK or replace Archive's protected rejection ledger.
Logging also does not itself prescribe retry, recovery or alarm escalation.
Central log availability must not turn validation rejection or failed archival
acceptance into success. These boundaries apply when callers handle logging
failures as well as ingestion outcomes.

Start with useful diagnostic coverage. Occasional duplicate entries are acceptable;
error-reporting ownership and correlation across propagated failures are a deferred
refinement, not a prerequisite for initial logging. Do not introduce custom
error-deduplication machinery without demonstrated need and a scoped decision.

Future implementation acceptance includes an invalid envelope and a partial-channel
fault producing useful diagnostic entries without any rendering consumer; unchanged
validation results with logging enabled; and a logging failure never creating an
archival ACK. These are required future evidence, not tests already performed.
Decision discussion: [ingestion design issue](https://github.com/bardphysicslab/bardbox-project-template/issues/15#issuecomment-6243326846).

## Exact normalized fields

This is the server interface, not a requirement that every device emit JSON.
Adapters document their wire mappings and supported existing `protocol_version`
values. No additional schema-version field is introduced.

An accepted normalized record uses the existing reading object's `uid`,
`timestamp`, `status`, `message`, `data` and `extended` fields:

| Field | Meaning and representation |
| --- | --- |
| `uid` | Canonical registered UID; retain the claimed device UID on every upload. Explicit registry aliases are permitted. |
| `timestamp` | Original measurement time as UTC ISO 8601, or null when unknown/invalid. Never receipt time by fallback. |
| `status` | `ok` when no channel is faulty; `error` when one or more are faulty. At ingestion this describes validity, not freshness. |
| `message` | Bounded human-readable summary; applications use structured faults, not this text. |
| `data` | Every registered channel, canonical name to typed valid value or null. Unregistered channels are ignored. |
| `extended.record_id` | ASCII string of 1–128 characters matching `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`, required for queued archival push; optional for other observations. Unique for the lifetime of the logical device's canonical UID, including reboot, reflash, recovery, queue clear and hardware replacement preserving that identity. Assigned before queue persistence, unchanged on retry/reboot/preview. |
| `extended.reported_uid` | Original claimed UID before an explicit registry alias. |
| `extended.firmware_version` | Device-reported firmware that produced the record, not assigned or available firmware. Nonempty string. |
| `extended.protocol_version` | Supported protocol of the original record. Nonempty string, independently checked from firmware. |
| `extended.rssi_dbm` | Original Wi-Fi diagnostic: finite number in dBm or explicit null with a metadata fault. Required presence for Wi-Fi devices, absent for other transports unless reported. |
| `extended.time_source` | `device` for a usable reported measurement time; `unknown` otherwise. |
| `extended.clock_quality` | `unknown` when quality/policy is absent or insufficient, `reported_unsynced` for an explicit unsynchronized-clock indication, or `project_accepted` when declared project clock-quality checks pass. This is not an independent clock-accuracy certification. |
| `extended.time_fault` | Null, `missing`, `invalid`, `clock_unsynced`, or `outside_project_bounds`; unknown time does not invalidate otherwise usable channels. |
| `extended.observed_at` | Trusted UTC ISO 8601 server observation time captured by Communications/source adapter on completing a live poll/serial observation; otherwise null. Does not claim exact sensor sampling time. |
| `extended.channel_faults` | Map from each null channel to `{code}`; valid channels have no entry. |
| `extended.metadata_faults` | Map of unavailable/invalid diagnostic metadata to `{code}`. Separate from channel faults. |
| `extended.expected_report_interval_ms` | Positive integer effective reporting interval resolved below. |
| `extended.reported_report_interval_ms` | Original reported reporting cadence converted to milliseconds, or null when absent; separate from configured effective cadence. |
| `extended.cadence_source` | `device_config`, `reported`, or `project_config`. |

Firmware wire aliases such as CESH `fw_version` map to
`extended.firmware_version`. An adapter accepting aliases must reject conflicting
simultaneous values with `metadata_conflict`, rather than choose silently.
Channel aliases and unit conversions are adapter mappings, not new canonical
channel names. Preserve bounded explicitly reported diagnostics separately;
never infer a disconnected sensor from a null value.

Record-ID generation must survive erased counters and replacement hardware.
Use a durable never-reused namespace plus sequence, or a random identifier with a
documented collision budget; a resettable counter alone is insufficient. CESH's
two 32-bit random words are an existing scheme to assess, not a proof of uniqueness
for arbitrary device lifetime/volume. Server conflict checks remain necessary.
Adapters explicitly map legacy IDs through the compatibility path rather than
silently truncating, rewriting or accepting out-of-contract IDs.

`delivery` is a separate trusted-context object, never merged into immutable
record metadata. It contains `received_at` (UTC ISO 8601 captured by
Communications), `authenticated_uid` (identity binding established by
Communications), `kind` (`archive`, `preview`, or `observation`), and `transport`
(adapter identifier). Optional `diagnostics` contains current sender-reported
`firmware_version`, `protocol_version`, `rssi_dbm`, `buffer_count`, and
`buffer_max_records`. Optional `buffer_mounted` and `catchup_active` are booleans;
`last_buffer_error` is a bounded diagnostic string. Each keeps its send-time
meaning and is not a substitute
for original record metadata. Sender diagnostics are authenticated reports,
not independently verified hardware facts. Missing optional diagnostics remain
absent; counters, when supplied, are nonnegative integers with count no greater
than capacity. Invalid optional delivery diagnostics are omitted and recorded
in `delivery.diagnostic_faults` as `{field: {code: "invalid"}}`.

During replay the record's original firmware, protocol, RSSI, timestamp, cadence
and values stay unchanged, even after a firmware/configuration update. Current
sender firmware, RSSI and queue progress belong in `delivery.diagnostics`.
Archive retains the first accepted delivery context separately from the record;
later attempts cannot overwrite it. Contact health may use each new authenticated
receipt; measurement freshness may not. Delivery diagnostics describe that
attempt only: delayed replay must not overwrite newer current diagnostic state
without a separately documented ordering rule. Receipt time alone cannot prove
when a diagnostic was sampled. SSID remains optional protected diagnostics.

The source adapter in Communications computes source comparison before engineering
unit conversion, using the wire profile defined under Archive comparison below.
It supplies `delivery.source_comparison_profile` and `delivery.source_digest_sha256`
as trusted server context, never as trusted device-supplied hashes. For a known
device key/record ID, Archive first exposes the originally stored profile to the
adapter for that retry; for a new ID, use the configured supported wire profile.
Archive verifies the profile/digest context, owns storage and decides duplicate
versus conflict. Thus duplicate comparison precedes current ingestion validation
without making ingestion persist data or reconstruct source tokens from normalized
values. JSON comparison requires token-preserving decoding; ordinary numeric
conversion must not erase the original numeric tokens before this step.

## Measurement time and observation freshness

A reported device time must parse as an explicit UTC ISO 8601 instant. When no
project clock policy is declared, retain a parseable reported instant with
`time_source=device`, `clock_quality=unknown` and no time fault, but Health must
not use it for measurement-time freshness. Projects enabling that freshness basis
configure clock-quality criteria, earliest-valid-time bounds and a finite maximum
future skew before activation. Apply declared bounds when present. A parse failure is `invalid`; an explicit
unsynchronized-clock indication is `clock_unsynced`; violation of those bounds is
`outside_project_bounds`. Store null measurement time with that reason and preserve
the original input as bounded source evidence; do not reject healthy channels.
A 1970 RTC date is outside bounds when the project's earliest valid time excludes
it; no universal earliest date is imposed. A future timestamp must never extend
freshness beyond the configured skew allowance. No device timezone guessing or
automatic clock-offset correction is performed. Clock quality not reported by
the device remains unknown; project policy decides whether that suffices.

CESH `clock_unsynced=1` maps to `clock_unsynced` regardless of the timestamp text;
`0` means no explicit unsynchronized indication, not certified accuracy; null or
absence means unknown clock quality. Preserve the original flag. CESH's project
contract must supply its stricter window/time criteria and bounds.
An explicit unsynchronized indication sets `clock_quality=reported_unsynced`;
otherwise quality stays `unknown` until the configured project checks accept it.

Health may use trusted `observed_at` for `delivery.kind=observation` under an
explicit project policy, labeled `observation` as the freshness basis. This covers
live RKC polling and directly attached serial observations even with null actual
measurement time. Expire freshness against that observation time and the project's
cadence/timeout; do not relabel it as device sampling time. Archived observations
replayed later keep their original observation time and cannot become fresh from
a new receipt. Archive and preview pushes cannot use receipt time as observation
time. This exception does not turn unknown-time push records into fresh readings.

## Channel and aggregate faults

Validate channels independently using registry types, units and validators.
Boolean values are not numeric measurements. Canonical serialized values must
never contain NaN or infinity. For registered channels:

| Input | `data[channel]` | Fault code |
| --- | --- | --- |
| Valid value | Original normalized value | No entry |
| Missing required channel | null | `missing_required` |
| Missing optional channel | null | `not_reported` |
| Explicit null | null | `unavailable` |
| Wrong type | null | `invalid_type` |
| Non-finite value exposed by a supported adapter | null | `non_finite` |
| Registry validity check fails | null | `validation_failed` |
| Explicit device invalid indication for that channel | null | `device_reported_invalid` |

`not_reported` is an availability annotation, not a fault that forces aggregate
`error`. Other listed channel codes do force `error`. A documented device fault
applies only to its declared channel scope; it cannot clear independent healthy
channels. An unscoped device error is retained as diagnostics and each channel
is still validated; if no values can be decoded, reject the malformed envelope.
Scientific alarm thresholds are not ingestion validity limits.

For example, valid door state and non-finite temperature produce:

```json
{
  "status": "error",
  "data": {"temp_c": null, "door_open": true},
  "extended": {
    "channel_faults": {"temp_c": {"code": "non_finite"}}
  }
}
```

This is a fragment; required identity/metadata fields still apply. The archive
stores validated values with the fault reason. If original input is retained
for investigation, it is bounded protected raw evidence, never a validated
measurement, and normal application logic does not depend on it.

Aggregate `error` no longer means every channel is invalid in this target
contract. `stale` and `node_unavailable` remain health projections for current
views: unavailable/stale channel values are null there, without rewriting
historical archive values. Health owns these projections and per-channel
freshness. A recent replay receipt cannot make an old or unknown-time push record
fresh. Live `observation` freshness follows the explicit rule above. Unknown
measurement time remains distinguishable in archive, latest, queries and rendering.
No universal RTC
or precision requirement is added.

## Envelope rejection and durable acceptance

| Condition | Outcome / error code |
| --- | --- |
| Missing required UID, original firmware or original protocol; missing queued archival record ID; absent required Wi-Fi RSSI field | Reject, `missing_metadata`, with field path. |
| Empty/invalid identity, version or ID field | Reject, `invalid_metadata`. Firmware/protocol sentinel `unknown` does not satisfy the requirement. |
| Conflicting simultaneous metadata aliases | Reject, `metadata_conflict`, identifying the conflicting field. |
| Missing/invalid required trusted receipt context, including an invalid server clock | Temporary server failure, `receipt_context_unavailable`; HTTP 503, not a device metadata fault. |
| Present null/non-finite/wrong-type Wi-Fi RSSI | Keep usable measurements; normalize RSSI to null with `metadata_faults.rssi_dbm.code` = `unavailable` for null or `invalid` otherwise. No invented signal strength. |
| Unsupported original or explicitly reported current delivery protocol | Reject, `unsupported_protocol`; never guess a nearest supported version. |
| Unregistered UID or authenticated identity not bound to claimed UID through explicit registry mapping | Reject, `identity_mismatch`. A UID allowlist alone is not authentication. |
| Undecodable/framing error, duplicate JSON keys, wrong envelope/container shape, or ambiguous required metadata | Reject, `malformed_message`. No partial salvage from structurally ambiguous input. |
| Extra unregistered measurement channel | Ignore it; no registry/display mutation and no envelope rejection. |
| Missing/invalid measurement time | Accept usable channels with null timestamp and a time fault. |
| Reporting cadence cannot be resolved | Reject, `cadence_unknown` or `invalid_cadence` as specified below. |

Authentication failure, oversize input and exhausted rate/work budgets are
Communications rejections before ingestion. JSON NaN/Infinity tokens are malformed
JSON, whereas a supported non-JSON adapter can report an individual non-finite
channel as a channel fault. For multiple envelope errors return deterministic
field-path/code order; do not echo unbounded input or credentials.

The target archival HTTP route accepts exactly one record per request. Reject
arrays/batches as `malformed_message` before processing any member; no member is
accepted or ACKed. The base protocol permits batching generally, but this route
does not support it until a separately reviewed per-record result/ACK contract
exists. A caller cannot interpret one success as accepting an unexamined batch.

Archive keys deduplication by `(archive_device_key, record_id)`, using an immutable
server-side device key assigned by Registry and retained across canonical UID
renaming or alias changes. This key is internal, not a new device payload field.
At first registration Registry binds canonical and reported identities to that
key. It must preserve accepted bindings and reject alias moves that would split
or merge historical deduplication namespaces without a separately reviewed archive
migration. A retry resolved through an updated alias map uses the original key
and retains its original reported UID/content; historical rows retain their
original canonical UID. Newly authorized replacement hardware
using the same logical UID also inherits its ID-uniqueness obligations.

Compare immutable source content before engineering unit conversion, registry
filtering/channel nulling, or time validation. Include original reported identity, original metadata,
timestamp (including invalid/missing distinctions), all supplied measurements
(including ignored channels), and record diagnostic/fault indications. Exclude
delivery context, current delivery diagnostics, and server-derived validation,
cadence and health projections. This avoids configuration changes manufacturing
conflicts or different bogus inputs becoming identical after nulling.

Each supported wire contract has a documented source-comparison profile. For JSON,
compare a deterministic structural encoding of original immutable fields with
sorted object keys: key order/insignificant whitespace are immaterial; decoded
strings, types, null/absence, array order and original numeric tokens are preserved.
Exclude only delivery fields explicitly named by that wire profile. Do not compare
values after unit conversion or sensor validation. For non-JSON profiles document
the exact immutable byte segment or equivalent deterministic encoding. Archive
stores `source_digest_sha256` (the SHA-256 digest) and the server-private
`source_comparison_profile` identifier with
first acceptance; lookup must use that original profile, not today's adapter
normalizer. Retain the original profile implementation across upgrades while any
retry is possible. Missing profile support is `comparison_unavailable`/503, never
a guessed conflict or duplicate. New profiles apply only to new records and require
documented compatibility checks; they add no wire schema/protocol-version field.

Communications configures finite maximum message bytes and record bytes before
enabling a route, rejects oversize work before acceptance, and streams/bounds
comparison work within those limits. Archive stores fixed-size digests; optional
raw evidence has a configured finite byte budget and protected access. Truncating
raw debug evidence must never change the full-source digest. Malformed messages
without a usable record ID are diagnostic events, not invented archival records.

An identical accepted duplicate returns `duplicate`; conflicting immutable
content returns `record_id_conflict`, preserves the original and does not publish
the conflicting data. Concurrent submissions and restart between persistence
and deduplication must be atomic or recoverably journaled by Archive. An in-memory
ID set is insufficient. Serialization must cover all workers/processes writing
the same device key, with unique-key enforcement and commit/journal recovery;
process-local locks alone are insufficient. A retry after uncertain archive failure is safe and uses
the same ID. A known accepted identical duplicate remains ACK-eligible under its
original acceptance; later registry changes do not erase durable acceptance.
Identity authentication/binding and supported decoding still apply before lookup.

Archive deduplication state must outlive every possible retry, including records
on offline nodes and explicit legacy paths. Pruning measurement rows must retain
acceptance tombstones containing device key, record ID, source digest/profile and
acceptance result. No time-based expiry is safe while retries are unbounded.
Retire a namespace only after explicit reconciliation that makes further retries
impossible. Capacity exhaustion is visible and fails closed without advancing ACK.
Backup/restore must reconcile archive commits, deduplication state and identity-key
bindings as one consistent checkpoint/journal recovery. Mismatched or missing state
blocks new archival acceptance with 503 until reconciled; never silently rebuild
deduplication from incomplete pruned history. Restore validation includes a lost-ACK
retry and a known conflicting ID before reopening writes.

For retry handling the application first supplies authenticated, bounded, decoded
source identity/content to Archive's duplicate lookup. An accepted exact duplicate
can return its original acceptance without reinterpreting it under today's registry
validators. New records go through current ingestion validation before Archive
acceptance. Duplicate lookup grants no publication of new measurements and does
not bypass authentication, UID binding or protocol support. A rejected new record
does not reserve its ID; only durable acceptance establishes deduplication state.

Only Archive `accepted` or known accepted `duplicate` permits an archival ACK
and dequeue. Partial channel faults may be durably accepted with their nulls and
reasons; envelope rejection, conflict or archive failure cannot be ACKed.
For HTTP archival routes, preserve the existing rule that every 2xx is an ACK:
use non-2xx for all non-acceptance outcomes, including asynchronous pending work.
Suggested mappings are 400 malformed, 403 identity, 422 metadata (including
`metadata_conflict`)/protocol/cadence, 409 ID conflict, and 503 archive failure,
unavailable receipt context or unavailable comparison profile. Preview 2xx
acknowledges preview receipt only on its dedicated route. Non-2xx archival
responses carry a bounded JSON object with `errors` (the `{code, path}` array,
including Archive/Communications errors) and `failure_class` (`temporary_server`,
`server_repairable`, or `immutable_content` as classified below). Never echo source
values or credentials. Use `path="delivery.received_at"` for unavailable receipt
context, `path="extended.record_id"` for ID conflicts, and the applicable field
path otherwise; whole-message errors use `path="record"`. Node diagnostics use the
structured code/class, since status 422 alone cannot distinguish repairability.
Malformed, missing or oversized error bodies remain failed attempts with unknown
error detail; they never acknowledge or dequeue a record. Existing archival 2xx
ACK semantics remain unchanged and do not require parsing a success body.

### Rejected FIFO records and operator disposition

Separate temporary server faults (receipt clock, storage or comparison unavailable:
503), server-repairable admission failures (unknown identity binding, unsupported
protocol, or missing configured cadence: 403/422), and immutable-content failures
(missing/invalid original metadata, malformed record, conflicting metadata,
invalid reported cadence, or conflicting record ID: 400/409/422). “Server-repairable”
means an authorized correction or validated compatibility adapter may help; it is
not permission to weaken authentication or invent original metadata. Node behavior
must not assume all 422 errors can be fixed merely by retrying.

All failures retain the original record. Use bounded per-attempt timeouts and
capped backoff; retries continue while that record remains retained, without a
busy loop. A per-attempt deadline is not an expiry or permission to give up and
delete queued data.
A permanently rejected head record intentionally stalls FIFO archival delivery;
this is a visible recovery state, not successful drain. Acquisition continues
within documented queue capacity/overflow limits. A compatible preview path may
continue validated live monitoring but never bypasses FIFO archival acceptance.
Node diagnostics and server Health must expose `archive_blocked`, blocked record
ID if usable, error code, first/last failure time and retry/queue progress. This
operational status is distinct from channel measurement validity and connection
health. Legacy nodes lacking these diagnostics are an explicit migration gap;
server-side rejection reporting is still required before strict adoption.

Archive owns a separate protected rejection ledger for authenticated, identity-bound
submissions with a usable ID: device key, original ID, full-source digest/profile,
error codes and first/last receipt context (null with clock-failure diagnostics
when trusted time is unavailable), plus source content within a configured
finite evidence budget. A truncated source must be labeled. Aggregate repeated
identical rejections; impose per-device entry/byte limits and a retention budget.
On evidence-budget exhaustion keep bounded blocked-state/digest diagnostics and
surface the limitation; no success ACK results. Anonymous/malformed input without
a bound identity/usable ID goes only to rate-limited Communications diagnostics.
Ledger entries are not acceptance tombstones, reserve no ID and authorize no dequeue.

Current safe disposition is to retain and visibly block. An operator can correct
server configuration/support, or investigate using preserved source evidence.
Re-uploading altered content under the old ID and automatic queue clearing are
forbidden. This proposal does not authorize dropping, skipping or ACKing rejected
records. A future terminal disposition (such as supported export then selective
removal) needs an explicit maintainer decision and a separately reviewed node/server
recovery contract before strict rollout to a project that requires automatic drain.
No such recovery feature is claimed implemented. Record the affected node/ID,
evidence location and next operator action in its migration tracker; never hide an
unresolved permanent head record behind a conformance claim.

## Reporting cadence

Resolve `expected_report_interval_ms` in this order: explicit per-device server
configuration, valid original record-reported metadata, explicit project default.
Configuration owner validates all configured values before activation; invalid
configuration cannot silently fall through. Effective cadence and its source are
stored with first acceptance and are not recomputed on replay. Reporting means
completed-record cadence; acquisition and upload retry/catch-up are independent.
If configuration changes while a record is queued but before its first acceptance,
the effective cadence uses that new configuration. Preserve the record-reported
cadence separately; the configured effective value is not a claim about historical
device acquisition. Later duplicates retain the original acceptance's resolution.

Canonical cadence is an integer in `[1, 2147483647]` milliseconds, inclusive.
Projects may impose narrower bounds. This is a representational bound, not a
promise that every adapter or service sustains 1 ms reports. Reject booleans,
strings, non-finite values, zero, negatives, overflow and sub-millisecond results;
never clamp or truncate. Legacy explicitly numeric seconds multiply by 1000
using exact decimal conversion, and must yield an integral millisecond value.
For example, 0.125 s becomes 125 ms; 0.0005 s is invalid.

CESH `expected_upload_interval_s` maps to reporting milliseconds; its documented
legacy `upload_interval_s` alias is used only if the primary field is absent.
`sample_interval_ms` stays acquisition cadence and
`upload_catchup_interval_ms` stays retry/catch-up cadence; neither is a reporting
fallback. Conflicting simultaneous cadence aliases reject with `invalid_cadence`.
An explicitly supplied invalid reporting value also rejects with `invalid_cadence`,
even when configuration has precedence. Missing reporting metadata is allowed
when configuration supplies it; without any source reject `cadence_unknown`.
A valid report differing from configured cadence is retained as reported
metadata but cannot overwrite configuration. Historical reports never update
current device cadence settings. Health's stale/offline policy remains separate.

## Compatibility, evidence and migration

Changing the meaning of aggregate `error` and allowing null measurement time are
semantic compatibility changes. Additional fault fields alone cannot make old
consumers safe. Preserve the legacy reading projection for existing callers:
legacy `error`, `stale` and `node_unavailable` still null all declared channels.
Keep a labeled legacy response timestamp if required, but never copy it into an
unknown historical measurement time. The target interface exposes unknown time
directly; do not silently send it through a legacy timestamp contract.

Adoption must explicitly select the target interface through server composition
and documented endpoint/consumer configuration, before producing these objects.
No runtime auto-detection from a payload's extra fields. Inventory and test
archive, latest, health, query/render and alarm consumers before switching.
Reuse existing protocol support declarations; any incompatible wire change needs
its normal protocol-version review. This proposal allocates no new protocol value
and does not claim legacy `web-node-v0.2` senders meet the stricter metadata rules.

| Consumer/source inspected | Gap and future migration |
| --- | --- |
| CESH `345b6bb7b18bd3d7eb7eb33b3bc7550a69021110`, `software/app/main.py:store_upload` | Combines validation, latest/contact, science and archive; substitutes receipt time when measurement time fails; ID-only duplicate checks cannot detect content conflict. Extract interfaces in development and preserve unknown time, archive acceptance and content-aware durable deduplication. |
| CESH firmware at that revision, `software/firmware/esp32-air-node/src/main.cpp` | Aggregate JSON is frozen at window completion. `withCurrentUploadStatus` appends `current_*` queue diagnostics and `catchup_active` at send time: map them to `delivery.diagnostics`, exclude them from original-source comparison, and retain bounded fields under their declared meaning. Legacy CSV rows are rebuilt with current protocol and `fw_version:"unknown"`; they need the labeled legacy path, not invented original metadata. Disconnected Wi-Fi stores RSSI `0`; this documented sentinel maps to null/`unavailable`, not valid signal strength. Map `clock_unsynced` as above. Explicit cadence units and sensor aliases require adapter conversion. Existing aggregate record IDs use two random 32-bit words; assess lifetime collision risk before claiming target uniqueness. |
| RKC `0c4f9238a7c85f282a69d92f4142c6eea06f184e`, `software/app/drivers/esp32_door_temp_driver.py` | TCP polling assigns server timestamps, firmware is cached optional INFO metadata, RSSI appears in data, and partial temperature failure already preserves door/RSSI. Preserve that behavior in its legacy view; target polling adapters distinguish observation from unknown measurement time. Queued push needs a separate future identity/metadata/ID/ACK migration. |
| Project Template `4ea41e23de66e875253789f8429b375c9b3907e0` | Reference implementation remains future work: independent ingestion module, registry test interface and simulated air/freezer fixtures, then archive/latest/health/query/render integration. No firmware-template work in this slice. |

Development CESH adoption comes first with alarms disabled, then RKC with its
alarm/escalation contracts, feeding gaps back into the shared implementation.
Running pilots and historical files remain separate and unchanged. Legacy queued
records must drain through their documented supported path or an explicitly
reviewed migration; strict validation must not strand them during rollout.
Stage compatible servers before nodes, retain the legacy path for rollback, and
never rewrite historical unknowns as precise timestamps. Firmware-template work
stays paused until validated project firmware supplies the evidence.

Authentication is an adoption prerequisite, not existing evidence: the inspected
CESH upload path's UID allowlist does not demonstrate verified per-device binding.
A shared optional token, if configured elsewhere, also does not establish that
binding on its own. Credential
issuance remains deferred work (Firmware Tools issue 41). Development simulations
may inject explicit test identities; real-service strict adoption requires a reviewed
credential/binding plan before activation. This contract does not choose an issuance
scheme, relax identity checks or claim those credentials already exist.

Acceptance scenarios for the future implementation: mixed valid/faulty channels;
required/optional/unknown channels; malformed envelope versus invalid value;
missing metadata/null RSSI; supported/unsupported protocols; explicit UID alias
and identity mismatch; unknown/invalid time; changed firmware/RSSI/queue during
replay; cadence precedence, aliases, conversion and boundary values; identical
duplicate versus changed invalid/ignored content; concurrent/lost-ACK/crash
deduplication across processes; alias changes and replacement/reset IDs; immutable
source comparison across adapter upgrades; archive pruning and mismatched restore;
batch rejection with no member accepted; invalid server clock returning 503;
permanent FIFO rejection with visible blocked state and bounded evidence; future
device time/clock-quality bounds; observation-based polling freshness; and
legacy/target rendering without false freshness. Use synthetic
fixtures and injected registry/clock/archive results. These are required future
evidence, not tests claimed to pass by this documentation change.

Architecture review: Communications → ingestion → Archive/Latest/Health remains
the server boundary. The firmware and USB flasher maps require no arrow changes;
their queue/ACK invariants are retained. Keep diagrams only in the Architecture
Map. Registry/display separation and authentication ownership remain intact.
Affected coordination skills need no rule changes; implementation remains a
separate bounded milestone with independent review.
