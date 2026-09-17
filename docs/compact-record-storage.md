# Compact offline records (draft)

Shared reference: template firmware headers BardBoxRecordDelta.h and
BardBoxRecordChunk.h. No deployed device uses this format yet.

Store each completed immutable payload byte-for-byte. A chunk contains at most
50 records. Its first record is raw; later records independently reference that
base. Numeric values remain their original text: no precision loss or substituted
metadata when firmware changes. Unsupported scalar layouts use the general codec.

## Framing and recovery

All integers are unsigned little endian. The12-byte header consists of `BQ1\0`,
a32-bit chunk sequence, and CRC32 of the preceding8 bytes. Each frame has a16-bit
payload length, payload, and CRC32 of length plus payload. The first payload is
the base record; later payloads are versioned codec output. Lengths are bounded
before allocation. CRC is corruption detection, not authentication.

On startup, scan with a bounded read buffer under the storage lock. Track the
last complete, verified frame boundary. Report incomplete/corrupt data distinctly
from clean EOF. Never append after a damaged tail; seal that chunk and write the
next sequence. Retain damaged bytes for recovery. The reference reader deliberately
does not truncate, erase or guess where to resume after corruption.

Queue integration must durably commit ACK position before deleting a fully
acknowledged chunk. After an uncertain ACK commit, replay is preferable to loss.
If committing the ACK fails, restore the in-memory cursor and count as well: a
running device must not silently advance until the next reboot. Test both failed
temporary-file writes and failed atomic renames, including the final record in a
chunk. Failure after commit but before deletion may leave an obsolete file; reclaim
it only when durable ACK metadata proves that it has been consumed.
The server must deduplicate stable record IDs. Keep old-format files readable,
and prohibit OTA rollback to firmware that cannot read the new queue schema.
Do not format the filesystem automatically when mounting fails.

## Acceptance still required

Host tests exercise every truncation position and byte corruption in a50-record
chunk, with address/undefined-behavior sanitizers. This proves parsing properties,
not LittleFS durability. Device integration must test interrupted flushes and ACK
commits, full storage, legacy migration, acquisition timing, heap use and actual
14-day capacity including filesystem allocation overhead. Generated compression
estimates alone do not establish retention.
