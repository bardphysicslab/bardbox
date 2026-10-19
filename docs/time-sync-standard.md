# Time Synchronization Standard

The Raspberry Pi operating system clock is the authority for server receipt
and observation timestamps in BardBox applications. It does not replace unknown
original device measurement time in the proposed ingestion target.

## Time Model

- `ntp`: system time is sane and NTP synchronized.
- `rtc_holdover`: system time is sane but not currently NTP synchronized.
- `invalid`: system time is not acceptable for logging or session start.

Applications must expose time status to operators. In existing Pi
applications (legacy projection), logging and formal sessions must not start when
the server's time is `invalid`; that formal-session requirement is preserved.
In the target recording and ingestion contracts, an unsynchronized or unknown
device clock does not stop recording or acceptance: records keep an explicit
unknown measurement time ([BB-001](DECISIONS.md)) and are never given fabricated
times. An invalid *server* clock still cannot supply trusted receipt time
([ingestion contract](ingestion-contract.md#envelope-rejection-and-durable-acceptance)).

## UTC everywhere, labelled local display

Accepted October 19, 2026 ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991) item 3). UTC is the convention for absolute time
in BardBox firmware, internal interfaces, storage and APIs. Unknown or
unsynchronized time stays explicit and is never fabricated; measurement,
observation and receipt time stay distinct. Monotonic elapsed timing remains the
right tool for intervals and deadlines. Rendering may convert to local time for
people, labelling the timezone; this supersedes earlier UTC-primary display
wording. Which timezone (site, user or server) and where that preference is
stored remain open. Instruments not running BardBox firmware keep their own
conventions until their driver normalizes them. A Pi's operating-system timezone
setting does not change this rule.

## Measurement time versus server time

For the [proposed ingestion target](ingestion-contract.md), the server clock
is authoritative for receipt/observation time, not a replacement for unknown
device measurement time. Preserve device-reported measurement time and its
provenance; validation does not certify clock accuracy. Missing or invalid
measurement time stays null while otherwise usable measurements survive.
Project contracts define precision and clock-quality needs; no universal node
RTC requirement follows. The Pi clock/session validity rules above remain
applicable. An invalid server clock cannot manufacture trusted receipt time.

The timestamp assignment rules below describe legacy driver/API behavior.
Keep a labeled compatibility projection for existing consumers; never backfill
its server-assigned timestamp into an unknown original measurement timestamp.

## Timestamp Rules (legacy driver/API projection)

- Use UTC ISO 8601 timestamps at API/log boundaries.
- Device timestamps are not authoritative.
- Drivers or backend code on the Pi assign authoritative timestamps.
- `extended.last_seen` records the timestamp of the last fresh valid reading.

## RTC

Production BardBox Pi systems should use a battery-backed RTC for offline
holdover. The RTC seeds the system clock at boot; application code still reads
the system clock, not the RTC directly.
