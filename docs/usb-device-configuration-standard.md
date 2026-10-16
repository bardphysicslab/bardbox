# USB device configuration and selection standard

Status: proposed, 2026-10-16. Scope: two device-side interfaces shared by the BardBox USB
installer (Firmware Tools) and ESP32 project firmware (CESH first). It does not define
network OTA, which remains a separate draft (bardbox PR #16), registration, MAC handling or
credential issuance.

Ownership: BardBox owns these definitions. Firmware Tools writes them; project firmware reads
them and keeps exact copies of the shared readers. A change to either format is a BardBox
change first.

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

Acceptance: a marked, pending image may be confirmed only when the device has verifiably no
stored configuration (store opened, no record). It then runs in USB-maintenance mode until
provisioned, the same state a first installation produces. In every other case the
project's existing validation and rollback apply unchanged; in particular a marker never
substitutes for network-OTA candidate validation.

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
hash, all required. Existing DC1 devices keep their behaviour; nothing migrates or erases
them.

### DB1 basic record (key `basic`)

`"DB1"`, then `uid`, `name`, `wifi_ssid`, `wifi_password`, `telemetry_url`,
`telemetry_token`, `telemetry_ca`, then the CRC.

Field rules are DC1's for the same fields: `uid` 1-48 of `[A-Za-z0-9_.-]`; `name` 1-64 bytes,
no comma or control characters; SSID 1-32 bytes; password empty (open network) or 8-63
bytes; `telemetry_url` an `https://host[:port]/path` without query, fragment or user info
(≤512 bytes); `telemetry_token` optional (≤256 bytes); `telemetry_ca` a PEM X.509
certificate (≤4096 bytes) that anchors TLS to the telemetry endpoint. The CA is public
trust material, not a credential. Whether a receiver needs a token is that receiver's
policy; the record carries one only if supplied.

A DB1 is refused when a DC1 exists, and a DC1 is refused when a DB1 exists.

Firmware loads DC1 when present, otherwise DB1. With DB1 only, identity, Wi-Fi and
telemetry work and OTA is unavailable (disabled, which never rolls back a confirmed image);
services that use the OTA channel are unavailable too.

### Extension boundary: optional OTA record (not defined yet)

OTA settings for a DB1 device will be a separate immutable record under its own key, bound
to the DB1 `uid`, carrying the OTA origin, device token, trust and signing material and the
installed image identity. Its format and lifecycle are not defined by this standard.
