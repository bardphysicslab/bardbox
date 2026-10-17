# USB device configuration and selection standard

Status: proposed, 2026-10-16. Scope: two device-side interfaces shared by the BardBox USB
installer (Firmware Tools) and ESP32 project firmware (CESH first). It does not define
network OTA, which remains a separate draft (bardbox PR #16), registration, MAC handling or
credential issuance.

Ownership: BardBox owns these definitions. Firmware Tools writes them. Readers follow the
architecture's rule for shared implementation: a maintained component with a documented
source and version, consumed through its interface. CESH firmware is the first consumer;
other projects adopt it in stages and record the version they use. A change to either format
is a BardBox change first.

## 1. USB selection marker

ESP-IDF stores each boot selection as a 32-byte `esp_ota_select_entry_t`: `ota_seq` (u32),
`seq_label[20]`, `ota_state` (u32), `crc` (u32). The CRC covers `ota_seq` only (ESP-IDF
v4.4.7 `bootloader_common_ota_select_crc`); the bootloader ignores `seq_label`.

When the installer selects an image in the other application slot (update, reinstall of the
same image, or re-selection of a stored image), it writes that entry `NEW` with:

```
seq_label = "BBU1" | ota_seq (u32 little-endian, equal to the entry's own ota_seq)
          | first 12 bytes of the selected image's appended SHA-256 validation hash
```

An image without an appended hash is selected without a marker. First installation and
recovery erase the boot record instead and write no marker.

Readers must:

- choose the active entry as the bootloader does (`bootloader_common_get_active_otadata`),
  and require that it names the running slot and is `PENDING_VERIFY`;
- match all 20 bytes, comparing the hash prefix with `esp_partition_get_sha256` of the
  running partition (which re-verifies the image), because the label is not CRC-protected;
- treat a missing, torn or non-matching marker as no marker.

Acceptance: a marked, pending image may be confirmed only when the device verifiably has no
OTA configuration (stores opened, no DC1 record): it is unprovisioned, or holds only the
DB1 basic record. Such a device has OTA disabled, so no network-OTA candidate can exist on
it. Unprovisioned, the image then runs in USB-maintenance mode until provisioned, the same
state a first installation produces; with DB1 it keeps its stored settings and queue. In
every other case the project's existing validation and rollback apply unchanged; in
particular a marker never substitutes for network-OTA candidate validation.

Stale markers: ESP-IDF selection (`esp_ota_set_boot_partition`) keeps a reused sector's label
but always writes a higher `ota_seq`, so an inherited marker cannot match. Firmware that
reads markers also erases the sector it is about to select into before a network selection;
power loss there leaves the running entry intact.

## 2. Device configuration records

Records are stored in NVS namespace `bb-device`, each under its own key, and are immutable:
an existing different record is never overwritten; an identical retry succeeds (recovery
after a lost acknowledgement). Transfer is the existing USB `PROVISION_BEGIN/DATA/COMMIT`
sequence; firmware dispatches on the record's 3-byte magic.

Strings are UTF-8, each prefixed by its byte length (u16 little-endian); records end with a
CRC-32 (zlib, little-endian) over all preceding bytes.

### DC1 (existing, key `config`)

Unchanged: identity, Wi-Fi, telemetry and OTA settings plus the installed image's size and
hash, under the existing field rules (for example the telemetry token is optional and an
empty Wi-Fi password means an open network). Existing DC1 devices keep their behaviour;
nothing migrates or erases them.

### DB1 basic record (key `basic`)

`"DB1"`, then `uid`, `name`, `wifi_ssid`, `wifi_password`, `telemetry_url`,
`telemetry_token`, `telemetry_ca`, then the CRC.

Field rules are DC1's for the same fields: `uid` 1-48 of `[A-Za-z0-9_.-]`; `name` 1-64 bytes,
no comma; SSID 1-32 bytes; password empty (open network) or 8-63 bytes; `name`, SSID,
password and token contain no NUL, DEL or other control characters; `telemetry_url` an `https://host[:port]/path` without query, fragment or user info
(≤512 bytes); `telemetry_token` optional (≤256 bytes); `telemetry_ca` a PEM X.509
certificate (≤4096 bytes) that anchors TLS to the telemetry endpoint. The CA is public
trust material, not a credential. Whether a receiver needs a token is that receiver's
policy; the record carries one only if supplied.

The whole record is at most 8192 bytes. A record with a wrong magic or CRC, a truncated or
oversized field, or any bytes after the last field is rejected as a whole.

A DB1 is refused when a DC1 exists, and a DC1 is refused when a DB1 exists.

Firmware loads DC1 when present, otherwise DB1. With DB1 only, identity, Wi-Fi and
telemetry work and OTA is unavailable (disabled, which never rolls back a confirmed image);
services that use the OTA channel are unavailable too.

### Extension boundary: optional OTA record (not defined yet)

OTA settings for a DB1 device will be a separate immutable record under its own key, bound
to the DB1 `uid`, carrying the OTA origin, device token, trust and signing material and the
installed image identity. Its format and lifecycle are not defined by this standard.

## 3. Device settings over USB

Line commands on the device's USB serial port, answered with one reply line. They are
available before provisioning. Tools must read limits and capabilities from the device
and must not hard-code firmware values.

### Reporting interval

The reporting interval is the aggregation window and upload cadence, as seen on the
dashboard. It is not sensor polling and not queue catch-up. The firmware owns its default
and supported range. An override is a mutable setting, separate from the immutable records,
and applies at the next start.

| Command | Reply |
| --- | --- |
| `REPORT_INTERVAL_STATUS` | `REPORT_INTERVAL,default_s=<n>,active_s=<n>,override_s=<n\|none>,min_s=<n>,max_s=<n>,activation=next_boot` |
| `REPORT_INTERVAL_SET <s>` | `REPORT_INTERVAL_SET_OK,override_s=<s>,activation=next_boot`, or `ERR,REPORT_INTERVAL_RANGE` / `ERR,REPORT_INTERVAL_STORE` |
| `REPORT_INTERVAL_CLEAR` | `REPORT_INTERVAL_CLEAR_OK,activation=next_boot`, or `ERR,REPORT_INTERVAL_STORE` |

The firmware validates every value. A stored value outside the range is ignored in favour of
the default. Changing the interval must not touch identity, Wi-Fi, telemetry settings or the
measurement queue.

### Queue catch-up

Catch-up uploads buffered readings, oldest first, once the device is online. It runs in bursts:
one request at a time, ending after a maximum number of readings, when a time budget has
elapsed, or at the first failure. The next burst starts after a pause. These three values are
one setting, read and written together as `pause_s:max_uploads:budget_ms`. Like the reporting
interval, the firmware owns the defaults and supported ranges, an override is a mutable setting
separate from the immutable records, and it applies at the next start. Buffer capacity is
firmware-owned and is not a setting.

| Command | Reply |
| --- | --- |
| `CATCHUP_STATUS` | `CATCHUP,fields=pause_s:max_uploads:budget_ms,default=<p:u:b>,active=<p:u:b>,override=<p:u:b\|none\|invalid>,min=<p:u:b>,max=<p:u:b>,activation=next_boot` |
| `CATCHUP_SET <p> <u> <b>` | `CATCHUP_SET_OK,override=<p:u:b>,activation=next_boot`, or `ERR,CATCHUP_RANGE` / `ERR,CATCHUP_STORE` |
| `CATCHUP_CLEAR` | `CATCHUP_CLEAR_OK,activation=next_boot`, or `ERR,CATCHUP_STORE` |

- `override=invalid` means a stored value that cannot be read or is out of range. The firmware
  ignores it in favour of the defaults. A malformed command answers `ERR,CATCHUP_COMMAND`.
  Firmware without catch-up settings answers as for any unknown command; tools report it as
  unsupported and send no catch-up write.
- The budget only decides whether another request may start. A request already under way
  is not interrupted, so a burst can overrun the budget by one request, bounded by the
  firmware's HTTP timeouts. It is not a hard network deadline.
- Measurement continues during a burst. Catch-up yields to USB: the firmware starts no
  further request in a burst once a USB command is waiting, and starts no burst for a while
  after the last complete USB command (CESH: 60 s, restarted by every command, so a tool that
  polls more often keeps catch-up paused while it runs). This reduces, but does not bound,
  USB reply delay: a request already under way and the device's other network work still come
  first. A tool therefore starts each read and each save with one read-only command that may
  wait longer than the largest supported budget. No reply means unknown, not unsupported, and
  nothing is written.
- Cross-field effects: readings per burst and the budget together limit a burst, and the
  pause spaces bursts out. A firmware should not offer ranges whose upload caps alone cannot
  keep up with its fastest reporting interval (CESH checks its caps at compile time). That is
  not a drain guarantee: how fast a backlog clears depends on request time, that is on the
  network, the server, the payload size and the load from other devices.
- Changing catch-up must not touch identity, Wi-Fi, telemetry settings or the queue.
- A tool writes `CATCHUP_SET` only after validating all three values against the limits the
  device reported, and treats a confirmation echoing other values as uncertain.

### Wi-Fi selection

| Command | Reply |
| --- | --- |
| `WIFI_CAPABILITIES` (read-only) | `WIFI_CAPABILITIES,select=<0\|1>,apply=<0\|1>`; firmware without it answers `ERR,WIFI_COMMAND` |
| `WIFI_STAGE_BEGIN/DATA/COMMIT` (existing) | stages one record: SSID length, SSID, password length, password |
| `WIFI_SELECT` | `WIFI_SELECT_OK,ssid=<ssid>`, or `ERR,WIFI_SELECT,reason=no_staged_config\|store` |
| `WIFI_APPLY` (existing, unchanged) | trial connection with fallback to the previous network |

A tool must read `WIFI_CAPABILITIES` before staging. Unless it reports `select=1`, the tool
stages nothing.

`WIFI_SELECT` makes the staged network active without a connection trial or fallback. An
unavailable network stays selected. Measurement, buffering and USB commands continue, and the
device keeps trying to reconnect. Selecting a reachable network again lets buffered readings
upload. Every write is reviewed and confirmed by the operator, on the board that was read.

## 4. Release defaults

A firmware release may carry public defaults for the setup form, in a bundle input of their
own. The approval binds them like any other input, as digest `release_metadata`. Bundles
without them are unchanged.

```json
{"schema": "bardbox.release-defaults/1",
 "firmware_sha256": "<SHA-256 of the exact application image>",
 "firmware_defaults": {"report_interval_s": {"value": 120, "source": "<how the build resolved it>",
                                              "source_commit": "<40-hex source commit>"}},
 "operator_defaults": {"wifi_ssid": {"value": "<SSID>", "approved_by": "<approver>"},
                       "open_network": {"value": true, "approved_by": "<approver>"}}}
```

- **Canonical bytes** (sorted keys, no whitespace) are approved, stored and checked, and the
  document must name the exact application image. A mismatch refuses publication, or makes
  the bundle unavailable when it is read.
- **Firmware defaults** record what the build compiled in. The project's release step emits
  them from the effective build configuration of the named source commit (the environment's
  flags and sources at that commit, not a working tree; CESH: `scripts/release_metadata.py`).
  No tool parses source code to recover them later. Each firmware default is optional.
  Besides `report_interval_s`, the allowlist holds `catchup_pause_s`, `catchup_max_uploads`
  and `catchup_budget_ms`, in the same form. They appear only for firmware that has catch-up
  settings, so metadata for an earlier release is unchanged.
- **Operator defaults** are approved proposals for the form, each naming its approver. They
  are not firmware behaviour, and their origin stays distinct from firmware defaults.
- **Allowlist:** only the keys above are accepted. Identities, passwords, tokens and private
  configuration never appear.
- **How tools use them:** the form proposes values from the selected approved release, taken
  from the same verified bundle snapshot that would be installed. The connected board still
  reports its current state, capabilities and supported limits. A proposed value the board
  does not accept is not offered, and is never copied from older firmware or app settings.
  Operator edits are never overwritten.
