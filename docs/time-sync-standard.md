# Time Synchronization Standard

The Raspberry Pi operating system clock is the timestamp authority for BardBox
applications.

## Time Model

- `ntp`: system time is sane and NTP synchronized.
- `rtc_holdover`: system time is sane but not currently NTP synchronized.
- `invalid`: system time is not acceptable for logging or session start.

Applications must expose time status to operators. Logging and formal sessions
must not start when time is `invalid`.

## Timestamp Rules

- Use UTC ISO 8601 timestamps at API/log boundaries.
- Device timestamps are not authoritative.
- Drivers or backend code on the Pi assign authoritative timestamps.
- `extended.last_seen` records the timestamp of the last fresh valid reading.

## RTC

Production BardBox Pi systems should use a battery-backed RTC for offline
holdover. The RTC seeds the system clock at boot; application code still reads
the system clock, not the RTC directly.
