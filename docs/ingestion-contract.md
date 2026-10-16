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

Registry owns identity bindings, registered channel definitions, required versus
optional channels, validators and cadence configuration. Ingestion reads one
consistent snapshot. Archive owns durable storage, conflict detection and
deduplication. Latest state, health, science, alarms and query/rendering consume
accepted records through their respective interfaces. Display configuration is
separate from registration; incoming fields never add card rows.

User-entered names, locations, latitude/longitude and operational settings enter
through the authorized control API, not measurement ingestion. The persistent
configuration owner validates, persists and applies its settings; the registry
enforces validation for device configuration it owns. Reject invalid edits before
changing stored or active values. Rendering may provide early feedback but cannot
replace server validation. Query/rendering joins server-managed descriptive
metadata to readings by UID; a renamed freezer keeps its device identity.

Ingestion has no persistent state or external writes. Rejected input cannot
update validated latest measurements or scientific/alarm inputs. Communications
may record bounded rejection/contact diagnostics separately. For archival input,
publication follows archive acceptance; preview publication follows validation
under the separate [preview contract](web-node-live-preview.md), without an
archive ACK or archival science side effects.

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
| `extended.record_id` | Stable opaque nonempty string required for queued archival push; optional for other observations. Assigned before queue persistence, unchanged on retry/reboot/preview. |
| `extended.reported_uid` | Original claimed UID before an explicit registry alias. |
| `extended.firmware_version` | Device-reported firmware that produced the record, not assigned or available firmware. Nonempty string. |
| `extended.protocol_version` | Supported protocol of the original record. Nonempty string, independently checked from firmware. |
| `extended.rssi_dbm` | Original Wi-Fi diagnostic: finite number in dBm or explicit null with a metadata fault. Required presence for Wi-Fi devices, absent for other transports unless reported. |
| `extended.time_source` | `device` for a usable reported measurement time; `unknown` otherwise. |
| `extended.time_fault` | Null, `missing`, or `invalid`; unknown time does not invalidate otherwise usable channels. |
| `extended.observed_at` | UTC ISO 8601 server observation time for a polling adapter, otherwise null. Does not claim exact sensor sampling time. |
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

`delivery` is a separate trusted-context object, never merged into immutable
record metadata. It contains `received_at` (UTC ISO 8601 captured by
Communications), `authenticated_uid` (identity binding established by
Communications), `kind` (`archive`, `preview`, or `observation`), and `transport`
(adapter identifier). Optional `diagnostics` contains current sender-reported
`firmware_version`, `protocol_version`, `rssi_dbm`, `buffer_count`, and
`buffer_max_records`. Each keeps its send-time meaning and is not a substitute
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
freshness. A recent replay receipt cannot make an old or unknown-time reading
fresh. Unknown measurement time remains distinguishable in archive, latest,
queries and rendering; a project may label server observation timing for its
operational view without claiming exact device sampling time. No universal RTC
or precision requirement is added.

## Envelope rejection and durable acceptance

| Condition | Outcome / error code |
| --- | --- |
| Missing required UID, original firmware or original protocol; missing queued archival record ID; absent required Wi-Fi RSSI field | Reject, `missing_metadata`, with field path. |
| Empty/invalid identity, version or ID field; invalid required trusted receipt context | Reject, `invalid_metadata`. Firmware/protocol sentinel `unknown` does not satisfy the requirement. |
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

Archive keys deduplication by `(canonical uid, record_id)`. Compare immutable
source record content after documented wire normalization, before registry
filtering/channel nulling. Include original reported identity, original metadata,
timestamp (including invalid/missing distinctions), all supplied measurements
(including ignored channels), and record diagnostic/fault indications. Exclude
delivery context, current delivery diagnostics, and server-derived validation,
cadence and health projections. This avoids configuration changes manufacturing
conflicts or different bogus inputs becoming identical after nulling. The adapter
must define deterministic comparison: map key order/whitespace are immaterial;
types, null/absence and differing invalid values remain distinct. Retain bounded
source evidence sufficient for comparison, or a stable digest of that content.

An identical accepted duplicate returns `duplicate`; conflicting immutable
content returns `record_id_conflict`, preserves the original and does not publish
the conflicting data. Concurrent submissions and restart between persistence
and deduplication must be atomic or recoverably journaled by Archive. An in-memory
ID set is insufficient. A retry after uncertain archive failure is safe and uses
the same ID. A known accepted identical duplicate remains ACK-eligible under its
original acceptance; later registry changes do not erase durable acceptance.
Identity authentication/binding and supported decoding still apply before lookup.

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
Suggested mappings are 400 malformed, 403 identity, 422 metadata/protocol/cadence,
409 ID conflict and 503 archive failure. Preview 2xx acknowledges preview receipt
only on its dedicated route. Permanent rejection needs operator repair and bounded
retry/backoff, never automatic queue clearing or content changes under the same ID.

## Reporting cadence

Resolve `expected_report_interval_ms` in this order: explicit per-device server
configuration, valid original record-reported metadata, explicit project default.
Configuration owner validates all configured values before activation; invalid
configuration cannot silently fall through. Effective cadence and its source are
stored with first acceptance and are not recomputed on replay. Reporting means
completed-record cadence; acquisition and upload retry/catch-up are independent.

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
| CESH firmware at that revision, `software/firmware/esp32-air-node/src/main.cpp` | Flat payload uses `fw_version`, mixed cadence units and sensor aliases; payload construction can use current build/protocol information while sending stored data. Define adapter mappings and explicitly distinguish original record metadata from current delivery diagnostics. Existing queues lacking original metadata need a labeled legacy path, not invented historical versions/RSSI. |
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

Acceptance scenarios for the future implementation: mixed valid/faulty channels;
required/optional/unknown channels; malformed envelope versus invalid value;
missing metadata/null RSSI; supported/unsupported protocols; explicit UID alias
and identity mismatch; unknown/invalid time; changed firmware/RSSI/queue during
replay; cadence precedence, aliases, conversion and boundary values; identical
duplicate versus changed invalid/ignored content; concurrent/lost-ACK/crash
deduplication; and legacy/target rendering without false freshness. Use synthetic
fixtures and injected registry/clock/archive results. These are required future
evidence, not tests claimed to pass by this documentation change.

Architecture review: Communications → ingestion → Archive/Latest/Health remains
the server boundary. The firmware and USB flasher maps require no arrow changes;
their queue/ACK invariants are retained. Keep diagrams only in the Architecture
Map. Registry/display separation and authentication ownership remain intact.
Affected coordination skills need no rule changes; implementation remains a
separate bounded milestone with independent review.
