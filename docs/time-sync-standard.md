# Bard Box Standard — Time Synchronization and Timestamp Authority

## Purpose

Bard Box systems must maintain reliable and consistent timestamps across all
operating conditions, including network outages and power loss.

---

## Time Source Model

Bard Box uses the following hierarchy:

1. The operating system clock is the authoritative time source for all applications
2. Network Time Protocol (NTP) is used to discipline the system clock when network is available
3. A battery-backed Real-Time Clock (RTC) provides holdover time across power loss and offline startup

Applications must not read directly from the RTC.

---

## Timestamp Requirements

- All application timestamps must be generated from the system clock
- Timestamps must be recorded in UTC using ISO 8601 format
- Systems must not emit timestamps based on unsynchronized or invalid time

---

## RTC Requirements (Production Systems)

Production Bard Box nodes must:

- Include a battery-backed RTC
- Initialize system time from RTC at boot when network time is unavailable
- Periodically synchronize RTC from the system clock
- Demonstrate correct time retention across power loss

---

## Synchronization Behavior

The system must enforce the following loop:

```
RTC → system clock at boot
NTP → corrects system clock
system clock → periodically written back to RTC
```

This ensures that RTC time remains aligned with network-synchronized time.

---

## Failure Conditions

A system must be considered in a degraded or invalid state if:

- System time is incorrect at boot
- RTC does not retain time across power loss
- NTP synchronization fails and RTC drift exceeds acceptable limits

Applications should expose a visible warning if system time is invalid.

---

## Recommended Implementation

Bard Box standard implementation uses:

- `chrony` for NTP synchronization
- `hwclock` for RTC interaction
- a systemd timer (`bardbox-rtc-sync.timer`) to periodically write system time to RTC

Cron-based solutions are not recommended.

See `pi-setup.md` for the full RTC setup procedure.
