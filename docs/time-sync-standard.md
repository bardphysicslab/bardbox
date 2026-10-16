# Time Synchronization Standard

The Raspberry Pi operating system clock is the authority for server receipt
and observation timestamps in BardBox applications. It does not replace unknown
original device measurement time in the proposed ingestion target.

## Time Model

- `ntp`: system time is sane and NTP synchronized.
- `rtc_holdover`: system time is sane but not currently NTP synchronized.
- `invalid`: system time is not acceptable for logging or session start.

Applications must expose time status to operators. Logging and formal sessions
must not start when time is `invalid`.

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
