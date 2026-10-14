# Firmware design continuation

October 14, 2026. Authoritative tasks: [firmware API design #31](https://github.com/bardphysicslab/bardbox/issues/31)
and the consolidation authorized in
[#33](https://github.com/bardphysicslab/bardbox/issues/33#issuecomment-6168631286).
Review: [PR #32](https://github.com/bardphysicslab/bardbox/pull/32). GitHub is
authoritative; this file is the dated design continuation, not a task ledger.

Entry point: [firmware blueprint](firmware-blueprint.md), whose document map links
every maintained firmware document. One maintained copy per topic:

- [serial/base API](firmware-base-and-serial-api.md);
- optional [buffer API](firmware-buffer-api.md);
- [USB flashing and provisioning](usb-provisioning-standard.md);
- source tree, build/runtime split, lifecycle, flash layout and release in the
  [blueprint](firmware-blueprint.md);
- compact storage format and OTA lifecycle stay in pending
  [PR #16](https://github.com/bardphysicslab/bardbox/pull/16), linked at head `7b947be`.

All are proposals. None is implemented, simulated-tested, hardware-tested, merged
or deployed as a shared BardBox component; existing project behaviour and test
results are cited with their revision, date and evidence level.

## Checkpoints

**Serial/buffer drafts (Codex, 2026-10-14).** Head `f9e4e391099d6fc18c6ba969271fe6c81d5e64bb`
on `codex/serial-buffer-api`, baseline `da62d8dd9c151a53e56388a1ced354d8ca01cf97`.
Consolidated the serial draft from `codex/usb-provisioning-standard` at `ab83ab3`.
Evidence then: relative links and whitespace checked; existing CESH queue fault test
re-run, 1 passed with simulated LittleFS and sanitizers (simulated, historical; no
physical power-loss/retention test). Consumers checked: CESH
`345b6bb7b18bd3d7eb7eb33b3bc7550a69021110`, RKC `0c4f9238a7c85f282a69d92f4142c6eea06f184e`.

**Documentation consolidation (Claude, 2026-10-14).**

- Repository `bardphysicslab/bardbox`, canonical checkout, branch
  `codex/serial-buffer-api`, starting head `f9e4e39` (clean, equal to remote).
  Owner: Claude, consolidation task relayed by Kornelis; Codex reviews.
- Shared guidance: bardphysicslab/engineering-standards@28e2dceb882d1de0e4948ca7b11f7322e792284d.
- BardBox standards: bardphysicslab/bardbox@da62d8dd9c151a53e56388a1ced354d8ca01cf97.
- Scope: documentation only. No firmware, tests, builds, device operation, merge,
  branch deletion, review closure or worktree retirement.
- Evidence: Markdown links, anchors and fences checked; `git diff --check`; source
  diff reviewed for lost unique material. No firmware tests or builds run; every
  test result cited is historical and labelled with its level.
- No skills or template implementation changed.
- The exact handoff commit is recorded in issue #31 and PR #32 after push.

## Source-to-final mapping

Blueprint: `claude/firmware-blueprint` at `69795b588e56b31fdafa64c02e272e6cd4d68d33`,
`docs/firmware-blueprint.md`.

| Source section | Final location | Change |
| --- | --- | --- |
| Header, Existing/Proposed labels | [blueprint](firmware-blueprint.md) header | Status, provenance and evidence levels updated |
| Related pending proposals | Blueprint §1 document map | Became the entry point; #16 linked at exact head |
| §1 Source tree | Blueprint §2 | Composition now names the serial module and separate owners |
| §2 Build-time versus runtime identity | Blueprint §3 | DC1 marked existing; proposed settings linked; firmware version mandatory |
| §3 Lifecycle | Blueprint §4 | Split into existing CESH 0.8.6 and proposed base lifecycle |
| §4 Flash memory table and rules | Blueprint §5 | Merged with the serial draft's storage section; one table |
| §4 "Reinstall selects app0" | Blueprint §5 write plans | Kept as existing CESH plan; generalisation became an open decision |
| §5 Build, release and approval | Blueprint §6 | Unchanged apart from dated existing-state labels |
| §6 USB identity | Blueprint §7 | MAC sentence states existing versus proposed |
| §7 Template adoption plan | Blueprint §8 | Step 4 adds the serial/settings component; DC1 and transfer headers become extraction candidates |
| §8 Evidence and limits | Blueprint §9 | Labelled historical local host tests, not re-run |
| ARCHITECTURE/README links | Firmware design row; README Key Docs and entry point | Re-created on current text |

USB: `codex/usb-provisioning-standard` at `ab83ab376475d7ef8adea57aa720b67726857340`,
`docs/usb-provisioning-standard.md`.

| Source section | Final location | Change |
| --- | --- | --- |
| One assembly operation, distinct results | [USB doc](usb-provisioning-standard.md) same section | MAC binding cross-reference added |
| Configuration and assembly choices | Same section | Link to proposed device settings |
| Identity, registry and replacement | Same section | Immutable DC1 marked existing; intended maintenance stated |
| Write boundaries and OTA compatibility | Same section | otadata wording points to the one open decision; flash table linked |
| Implementation and continuation | Historical evidence and next steps | Dated, simulated/physical levels separated; `bacc884` not on a firmware-tools remote at 2026-10-14 |
| `docs/firmware-base-and-serial-api.md` | Already in serial/base API at `f9e4e39` | Not copied again |
| ARCHITECTURE "USB assembly" row; README Key Docs | Firmware design row; README Key Docs | Re-created |
| Stray serial links appended to ARCHITECTURE/README ends | Not imported | Superseded by the entry-point sections |

Serial draft at `f9e4e39`, section "OTA-ready storage on the initial 8MiB S3
recipe": moved to blueprint §5, leaving a pointer. PR #16 at
`7b947be081d1d1fb646849c15e9491fbdce1297b`: not copied; linked at that commit from
the blueprint map, the buffer API and the USB doc. GitHub retains PR head commits,
so the pinned links remain readable while #16 is pending.

Not imported: either branch's root instructions or other files, any Trello
references, the PR #16 operator page, and topics assigned elsewhere in #33.

## Decisions preserved

- INFO/HEADER/READ required; PING and START/STOP optional; Web Node
  UPLOAD/PAYLOAD/BUFFER/BUFFER_CLEAR diagnostics where applicable.
- READ returns the latest valid sample immediately with repeated-sample identity
  and age; no acquisition on demand.
- Beginner template exposes typed metadata/schema/sample APIs and hides framing
  and parsing. Firmware version is mandatory. API names remain proposed.
- Acquisition scheduling, serial, settings, time, buffering and delivery have
  separate owners. No clock synchronization inside serial; supplied time
  validity crosses the interface, and time synchronization remains separate.
- Temporary debug overrides and explicit persistent configuration; secrets are
  writable but never echoed.
- Unprovisioned base INFO remains usable; explicit coordinated UID, settings and
  credential maintenance is intended. CESH's blocked INFO and immutable DC1 are
  existing limitations, recorded as such (blueprint §4).
- Latest serial samples and durable delivery records are distinct. RKC intends to
  save individual readings through outages (not implemented); CESH keeps
  project-selected aggregates. Buffering is optional.
- Save before delivery; retain until accepted; inspect/remove exact records by
  stable ID. Tokens, tickets and bounded operation history are proposals. CESH
  already saves FIFO records before delivery and removes them after ACK.
- Data/config partitions, record-schema readability and rollback compatibility
  are preserved; initial install, reinstall and OTA write plans are distinct.

## Open decisions

1. **otadata on USB reinstall** after an OTA-installed image ran: reset to select
   app0, or a slot-aware plan; how NVS OTA state and the rollback target are
   reconciled; which physical evidence supports it
   ([blueprint §5](firmware-blueprint.md#write-plans-initial-install-reinstall-and-ota)).
2. Exact wire grammar and types, sample metadata placement and compatibility,
   STATUS versus INFO.
3. Write/maintenance access policy for production devices.
4. Temporary-override expiry and precedence.
5. Partial aggregate windows after interval changes (CESH).
6. Full-buffer policy, especially RKC; operation-history bounds.
7. Configuration and queue schema rollback.
8. DC1-to-settings migration for existing CESH devices.
9. Adoption of the PR #16 storage format and OTA lifecycle; consistency of its
   reference USB configuration record with the USB doc.
10. Physical capacity, power-loss, wear and outage evidence (separate gates).

After review, build independent sensorless/BME280 and individual/aggregate queue
consumers before any project migration.

## Recommendations for Kornelis (not actions taken)

- Treat `docs/firmware-blueprint.md` and `docs/usb-provisioning-standard.md` on
  this branch as the maintained copies. If this review merges, the copies on
  `claude/firmware-blueprint` (`69795b5`) and `codex/usb-provisioning-standard`
  (`ab83ab3`) are superseded and become provenance only. Retire those branches
  and worktrees only through a separate approved closeout after preservation checks.
- PR #16 stays the owner of storage format and OTA. Its later disposition should
  update the blueprint map's pinned links to the merged location, or record a
  superseding decision.
- Pending topics stay in their own reviews per #33: layout/config naming (#23),
  Wi-Fi recovery (#19), live previews (#15), campus access (#18), Drive home (#17),
  tracker policy (#21), electrical channels and the platform roadmap branches.
  The platform board awaits existing-work/Trello reconciliation; GitHub stays
  authoritative and synchronization is not enabled.

## Next step

Codex independently reviews the exact consolidation commit recorded in #31/PR #32.
Kornelis then decides merge and branch/worktree retirement separately. After that,
resolve open decisions 1 and 2 before any reference implementation. No board setup,
synchronization, consumer migration or device operation is authorized here.
