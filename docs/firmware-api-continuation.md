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

## October 15 documentation audit checkpoint

Owner: Codex in the documentation-audit chat, manually relayed by Kornelis.
No implementation-thread messages, checkout switches or runtime changes.

- Governing remote main heads resolved: engineering-standards
  `28e2dceb882d1de0e4948ca7b11f7322e792284d`; BardBox
  `da62d8dd9c151a53e56388a1ced354d8ca01cf97`.
  Required shared files, BardBox root guidance and relevant published standards read.
  Institutional PDF/service guidance consulted without changing or determining
  hosting/authentication policy.
- Reused PR #32, branch `codex/serial-buffer-api`, prior head
  `cb4fd1a0a9643fc47c69c40f245f5e6607c3efcd`; exact new head is recorded in
  the PR/checkpoint comment after publication. No new checkout/worktree/feature
  branch. Remote documentation edits leave the canonical checkout at its existing
  head; its owner must reconcile later without resetting anyone's work.
- Observed canonical checkouts: BardBox clean at cb4fd1a; engineering-standards
  on codex/webctrl-reference at 7f1ce9f; Firmware Tools on
  claude/8-usb-provisioning at 9177881 with active uncommitted UI edits;
  CESH on codex/cleanup-cesh-hardware-2026-10-09 at 345b6bb with unrelated
  hardware edits/untracked files. All left untouched.
- Current remote main: Firmware Tools
  `52d4b8ed7d7127e2932e0131bf6b15ebf135b896` (Check device #39 merged;
  merge alone does not establish deployment); CESH
  `15f959479478b7347223f862d75d39355727d50b`.
- Reviewed CESH #48 `b2718891132da66b36ca8f7dd5f12eaf6e858a23` and #50
  `24c2305ff1834368a0a86a90592bb71faba91d65`, latest discussions and Codex
  correction. Source/synthetic evidence distinguishes reset metadata from NEW;
  exact pinned-bootloader startup acceptance remains open in #25/#49.
  Previously reported CI and host results remain attributed historical evidence,
  not tests rerun for this documentation audit.
- Provisioning source observation: Firmware Tools 9177881
  `packages/usb-browser/provisioning/{fields,record,session,provisioning}.js`;
  device record/store/commands at CESH 24c2305. The #8 scope supersedes older
  registry and MAC instructions. App UI edits were observed only as active work,
  not accepted or tested.
- OTA history: BardBox PR #16 remains open/draft at
  `7b947be081d1d1fb646849c15e9491fbdce1297b`; the file first appears in local
  retained history at f4aeea3 and never appears in governing main. Existing
  PR #32 pinned links resolve to the draft. No replacement OTA standard created.
  CESH's three stale path references are identified in the USB document;
  its active writer owns their correction via Kornelis.

### Gap assessment and dispositions

| Boundary | Finding and bounded disposition |
| --- | --- |
| USB metadata/startup | Corrected blanket install/rollback assumptions with the source matrix in the USB document; blueprint holds the pending handoff/health proposal. Exact bootloader/config/OTA-state combinations remain #25 work. |
| Provisioning | Corrected stale integrated-Flash, field-provider, registry/MAC and hardware-dropdown assumptions; existing DC1 and uncertain-commit semantics retained. No new schema. |
| Identity/authentication | Existing UID including instance is current scope. Factory base MAC is deferred lookup only. Naming-standard/deployed-CESH mismatch flagged, no migration. Real receiver/trust inputs and authentication acceptance remain project work. |
| Diagnostics/degraded operation | Check device is uninterpreted INFO text, independent of installer safety. Link existing recovery/queue rules; blueprint proposes only the missing independent-channel continuity clarification and notes serial/payload compatibility. |
| OTA authority | PR #16 is a pending draft, not a missing adopted main standard. Consumer references need their owner to pin/status-label it; adoption remains separate. |
| Tracking | Existing #31/#33/#32 own shared design/consolidation; #5/#8 own host work; #25/#49 own CESH acceptance; #41/project 5 own deferred registry. No duplicate workstream. Prior #31 checkpoint says BardBox board/Trello reconciliation remains pending. |

Board verification limit: the connected GitHub tools expose issues/reviews but no
Projects operations. The supplied registry-board URL returned a signed-out 404 in
the available browser; live membership/status and migration completeness were
not independently verified. Do not infer absence, recreate boards, migrate Trello
or claim board synchronization. Kornelis supplies authenticated board access or
relays the board reconciliation when resuming; this documentation task starts no
runtime implementation.

### Review and preservation

Corrections are documentary/source observations. New startup handoff and degraded
channel language are explicitly unapproved proposals. Existing published
Device/Web Node/transport requirements and PR #16 remain separate authorities.
No required/recommended/conditional institutional language is changed.
No template, shared runtime component or skill rule changes; consumer adoption
is deferred to its owner.

Documentation validation checks the four-file diff, whitespace, relative
links/anchors, fences and pinned external targets. No firmware build/publication,
hardware operation, merge, deployment, credential change or migration.
Remote branch/PR preserve the reviewed files off-machine; local audit material is
a same-machine review snapshot, not another maintained contract.

**Next:** independent reviewer reviews the exact updated PR #32 head, especially
the proposed startup handoff and partial-channel compatibility. Kornelis decides
adoption/merge separately and relays CESH's source-matrix/reference corrections.
Next checkpoint: that review, before any dependent implementation.


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
| §2 Build-time versus runtime identity | Blueprint §3 | DC1 fields listed from CESH source and marked existing; runtime intervals separated as proposed only (Codex review, #31); firmware version mandatory |
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

1. **USB startup/OTA reconciliation:** actual host plans are now distinguished
   in the [USB matrix](usb-provisioning-standard.md#write-boundaries-and-ota-compatibility).
   Resolve NVS OTA/DC1 state, health confirmation and fallback under the
   [proposed startup contract](firmware-blueprint.md#boot-validation-and-rollback-compatibility);
   verify the exact pinned bootloader and separately scoped physical evidence
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

Independent review of the exact October 15 documentation-audit head in PR #32 is
next; see its checkpoint above. Earlier cb4fd1a consolidation acceptance does not
cover these new edits. Kornelis decides adoption/merge and branch/worktree
retirement separately. Resolve relevant startup and wire-compatibility decisions
before dependent implementation. No board setup,
synchronization, consumer migration or device operation is authorized here.

## October 16 architecture-map checkpoint

Owner: Codex in the modular architecture chat, at Kornelis's explicit request.
Reuses the existing documentation PR/branch, parent d77ae258fc5aeb4533a03062c3037700bd9cc486.
Remote documentation authoring leaves canonical checkouts and active writers untouched.
The existing BardBox checkout remains behind its remote; its owner reconciles it
before subsequent local work. No new checkout/worktree or competing branch.

Added the [Architecture Map](architecture-map.md) with maintained node/server Mermaid,
the flasher cross-link requested by its owner, source ownership and review evidence
expectations. Root guidance, README and blueprint point to it. Both drawings
describe targets: student publication abstraction, serial without a delivery queue,
persistent network push, registry, distinct communications/ingestion, rendering via
queries, and independent scheduled backup. RKC push migration and QuantaQ/PurpleAir
removal remain required pending work. Original detailed API/schema decisions are
not resolved by a diagram.

Firmware Tools owns its new USB drawing at 2d036ed on codex/usb-architecture-map;
the link is pinned until its merge. No edit to its active checkout or flasher
implementation. Consumer AGENTS linkage should be reconciled by that owner; the
BardBox entry point is prepared here and is not effective main guidance until merged.
No automatic guarantee of cross-chat conformance or new CI enforcement is claimed.

Shared guidance: bardphysicslab/engineering-standards@341b3ba82503eb23b786dfcf71af430cc627e2a5
BardBox standards: bardphysicslab/bardbox@143d42976fd224e8609ee90744ba490a91df1819

Validation: check changed Markdown links/anchors, Mermaid node/reference structure, whitespace and
exact remote readback. No runtime test/build or hardware/deployment action.
Next: independent review of the exact updated head, reconcile Firmware Tools'
consumer pointer, and obtain merge decision. Earlier acceptance covers earlier
heads only; exact new head and check outcomes are in the PR publication comment.

## October 16 central diagram ownership correction

Kornelis clarified that a distributed diagram index was not the intended result:
all three diagrams (node firmware, project server, USB flasher) must have one
physical maintained home in BardBox's architecture-map.md. The USB drawing and
boundary text are imported with provenance from Firmware Tools 2d036ed. Its
implementation remains owned by Firmware Tools. The consumer copy becomes a
link-only pointer; no second maintained Mermaid source remains in that PR.

This decision supersedes the preceding checkpoint's distributed-ownership
recommendation. Existing historical source commits are provenance, not editable
authorities. Future diagram changes update this document, inspect related
diagrams for consistency and identify the related code/contract revisions.
No fourth/OTA diagram was added; the existing OTA draft is a contract reference.

Publication reuses existing BardBox and Firmware Tools documentation branches,
with exact-head leases. Their canonical clean checkouts and idle prior task were
inspected; remote documentation edits leave them untouched and behind remote.
Owners reconcile before local work. Exact new heads, link checks and readback
are recorded on the existing PRs. All changes remain review candidates.
