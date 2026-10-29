# Firmware design continuation

Current entry. The dated October 14–16 checkpoints, source-to-final mapping and
earlier open-decision list are archived unchanged in
[archive/firmware-api-continuation-2026-10-14-to-16.md](archive/firmware-api-continuation-2026-10-14-to-16.md).
GitHub ([bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31)) is
authoritative for status; this file does not embed its own commit hash.

## October 29, 2026 — Access Control in the server diagram (latest)

[ACCESS-CONTROL-DIRECTION-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6500637310): the maintained server
drawing names the existing authentication owner **Access Control** (conceptual;
the `software/app/authentication/` layout name stays) and shows human access
enforced at page endpoints, Queries/read APIs and Controls/write APIs, with
Rendering only reflecting permissions. Login adapters are replaceable (for example an existing basic/password
login where present; Bard Google later, proposed); membership is project-approved, not implied by sign-in.
Device and partner credential relationships are unchanged. The role matrix,
sessions, enforcement failure and API stay PROPOSED / TBD under D6. Documentation
only on branch `claude/access-control-docs` from `fb0c4c9`; the handoff is
[coordination/CLAUDE-HANDOFF.md](../coordination/CLAUDE-HANDOFF.md). The entries below are history.

## October 22, 2026 — Display units and the proposed JSON display configuration (history)

[DISPLAY-UNITS-1 + DISPLAY-JSON-REVIEW-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6342348125):
a neutral Units section (Metric/Imperial, Celsius/Fahrenheit) above the
Dashboard and Device settings sets one saved application-wide display
preference, metric/Celsius by default. Values show one decimal; stored values
keep canonical units and full precision; edits carry their captured unit and
untouched limits keep their exact stored value; drafts are never reinterpreted
or discarded by a Units change; unsupported quantities keep their declared
units. Rendering owns the versioned JSON preference, Processing the pure
conversion; shipped defaults stay separate from the installation's saved file.
Reference implementation [PR27](https://github.com/bardphysicslab/BardBox-Reference/pull/27), merged `85cc96c`. The Web UI
standard's YAML layout sketch is replaced by a PROPOSED JSON illustration with
open design notes; the layout engine stays future. Module trackers:
[Rendering #71](https://github.com/bardphysicslab/bardbox/issues/71), [Registry #10](https://github.com/bardphysicslab/bardbox/issues/10). Documentation only on branch
`claude/display-units-docs` from `936fc73`; merged as `fb0c4c9` ([bardbox#72](https://github.com/bardphysicslab/bardbox/pull/72)); its handoff is archived at
[coordination/archive/CLAUDE-HANDOFF-DISPLAY-UNITS-DOCS.md](../coordination/archive/CLAUDE-HANDOFF-DISPLAY-UNITS-DOCS.md).

## October 22, 2026 — Shared adoption principle, card groups and BNG room examples (history)

[Shared-module adoption principle](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6340809622): improve shared modules once
and adopt them easily per instance while preserving configuration, data and
project behaviour; stable interfaces and explicit tested migrations; not
automatic rollout. Now near the top of [ARCHITECTURE](../ARCHITECTURE.md).
[CONFIG-CARD-GROUPS-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6340973552): Name, Location, ordered featured
measurement/range rows (one per row), full-width switches, then automatic group
folders; modules declare logical groups; visibility and featuring are
presentation configuration; featuring moves fields; all Reference folders kept.
A small configuration example is documented as PROPOSED only; a configuration
engine and display-selection page remain future.
[BNG-ROOM-DASH-1 + SHARED-CARD-RULES-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6340776600): the Reference standalone
freezer page is replaced by registered simulated BNG rooms on the main
dashboard with a separate persisted example provider; range and Alerts are
shared between the card and Device settings; push-button Edit/Save/Cancel
([PR26](https://github.com/bardphysicslab/BardBox-Reference/pull/26), merged `ee5477c`). No RKC/CESH runtime adoption, production
Alarm, auth, hardware, firmware or deployment; Registry identity review kept;
Archive placement unresolved. Documentation merged as `936fc73`
([bardbox#70](https://github.com/bardphysicslab/bardbox/pull/70)); its YAML layout sketch is replaced by the
PROPOSED JSON illustration above.

## October 22, 2026 — Card order, colour meanings and Device settings direct Save (history)

[Card refinement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6339948902): card header Name/Location left and status
right; featured values before controls, two per row, each value beside its
allowed range and kept with its unit; each featured switch a full-width row
after the values; folders full-width below; labels, values and controls only;
semantic colours with state labels; Device settings Edit → Save/Cancel (the
Review/Confirm step superseded); card editing retained; the alarm switch's
in-section-only placement superseded for featured controls, with Alarm keeping
ownership. Reference shows the card order only as a simulated freezer example
([PR25](https://github.com/bardphysicslab/BardBox-Reference/pull/25), merged `c4f044a`); no RKC/CESH runtime adoption
and no Alarm provider. Archive placement remains unresolved. Documentation
merged as `764473c` ([bardbox#69](https://github.com/bardphysicslab/bardbox/pull/69)); "two per row" is refined by
CONFIG-CARD-GROUPS-1 above, and the freezer example is replaced by BNG rooms.

## October 21, 2026 — Device settings comparison and featured once (history)

[Combined acceptance](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6326655979): a Device settings table page with the
Registry table's Edit → Review → Confirm pattern for Name, Location, Owner and
coordinates (UID first, read-only; no Add/Archive), kept alongside label-free
dashboard editing for comparison on the same Registry values; featured Name and
Location appear only at the card top, no longer in Identity. Reference app
merged in [PR24](https://github.com/bardphysicslab/BardBox-Reference/pull/24) at `2fd900e` after independent review.
Documentation only on branch `claude/device-settings-docs` from `86a8b69`; the
handoff is [coordination/archive/CLAUDE-HANDOFF-DEVICE-SETTINGS-FEATURED-ONCE-DOCS.md](../coordination/archive/CLAUDE-HANDOFF-DEVICE-SETTINGS-FEATURED-ONCE-DOCS.md). The entries below are history.

## October 21, 2026 — Save feedback without visible edit controls (history)

[EDIT-SAVE-FEEDBACK-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6323916487): no visible Edit/Save/Cancel or status
labels and no icons; a changed draft is amber until the server confirms the
save, a confirmed change flashes green then returns white with the frame gone;
Escape and an unchanged Enter write nothing; refusals keep the amber draft;
uncertain outcomes are re-read, never shown as saved; saved values are unframed
at rest while empty ones keep a framed label. Reference app merged in
[PR23](https://github.com/bardphysicslab/BardBox-Reference/pull/23) at `386271d` after independent review. Documentation
only on branch `claude/edit-save-feedback-docs` from `5207bda`; the handoff is
[coordination/archive/CLAUDE-HANDOFF-EDIT-SAVE-FEEDBACK-1-DOCS.md](../coordination/archive/CLAUDE-HANDOFF-EDIT-SAVE-FEEDBACK-1-DOCS.md). The entries below are history.

## October 21, 2026 — Editable frames and Owner (history)

[EDITABLE-FRAMES-OWNER-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6323356438) (also [bardbox#10](https://github.com/bardphysicslab/bardbox/issues/10#issuecomment-6323356061)):
editable values are framed, unassigned editable values are empty frames with a
visible label, read-only unavailable values keep `—`; Owner is optional and
edited in place in Identity; new registrations assume no owner (superseding the
CESH/RKC default); no inline UID Registry link. Reference app merged in
[PR22](https://github.com/bardphysicslab/BardBox-Reference/pull/22) at `59b6b7e`. Documentation only on branch
`claude/editable-frames-owner-docs` from `d93491c`; the handoff is
[coordination/archive/CLAUDE-HANDOFF-EDITABLE-FRAMES-OWNER-1-DOCS.md](../coordination/archive/CLAUDE-HANDOFF-EDITABLE-FRAMES-OWNER-1-DOCS.md). The entries below are history.

## October 21, 2026 — Registry and rendering documentation reconciliation (history)

Owning [issue #64](https://github.com/bardphysicslab/bardbox/issues/64); plan
[6322957422](https://github.com/bardphysicslab/bardbox/issues/64#issuecomment-6322957422) (Codex-approved) under the
[accepted reconciliation](https://github.com/bardphysicslab/bardbox/issues/64#issuecomment-6322822102), which authorizes
publication and supersedes the local-only next action of the checkpoint below.
Branch `claude/registry-rendering-docs` builds on that checkpoint's local
commits (`28d97a3`, kept as ancestors; its branch ref is unchanged) and carries
the documentation commits of [PR52](https://github.com/bardphysicslab/bardbox/pull/52) by cherry-pick with
provenance (alarm switch inside Alarm with a read-only card indicator; owner-
declared editable fields, save/readback, drafts and failures). PR52's
coordination records stay on its own branch.

Reconciled: in-place editing ([TRUE-INPLACE-EDIT-1](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6322820690)) superseding
the single edit-home / display-only heading rule for featured Name/Location;
first-pass ten card sections with dashes; future display selection, Featured
and auto-hide; future Alarm-outside preference; contact state versus `LIVE`;
the inline Registry list (Add row, in-row identity Edit/review, Archive,
archived-reuse warning) with transitional UID/MAC corrections and deferred
permanence. One consolidated Registry paragraph lives in the architecture map;
ARCHITECTURE keeps a linked summary; the decision index adds the Reference
follow-up rows. Documentation only; no runtime, hardware or deployment claim.
The app part, [BardBox-Reference#20](https://github.com/bardphysicslab/BardBox-Reference/pull/20), is merged at `cc8808f`
([delivery](https://github.com/bardphysicslab/BardBox-Reference/issues/9#issuecomment-6323058396)). Exact head and review status of this
documentation PR are recorded in #64; the handoff is archived at
[coordination/archive/CLAUDE-HANDOFF-DOCS-RECONCILE.md](../coordination/archive/CLAUDE-HANDOFF-DOCS-RECONCILE.md).

## October 21, 2026 — Registry identity documentation checkpoint (history)

Owning [issue #64](https://github.com/bardphysicslab/bardbox/issues/64),
accepted discussion [#10](https://github.com/bardphysicslab/bardbox/issues/10).
Canonical BardBox checkout; Codex chat `01a15df1-50d4-7ec2-abd6-64d14f69d85a`,
branch `codex/registry-identity-docs`, baseline
`641b5c04cc87edc5a4513fd889741101ce9ff7fb`. Shared guidance:
`engineering-standards@91a2d7c0d4afd3eac55ec612be9866f46fb3a11d`.

Decision index and architecture/map now describe accepted project authority,
permanent board identity, mutable dated assignments and deferred enforcement.
The destructive reassignment purge task is cancelled, not implemented. Existing
experimental configuration and original-UID backlog remain compatible.
Latest accepted flow REG-UI-FLOW-1: registration UID/optional MAC only; automatic
dashboard card and descriptive edits there via Controls/Registry, with project
owner default and archival preserving history. Health owns Not yet seen/offline;
server metadata sync to devices is future discussion. REG-MANAGE-1 adds the
identity management list/forms (Reference PR12 merged a6f8b8d); dashboard
descriptive editing remains separate. Prior form placement is
superseded; no demo Ingestion or runtime change.
Documentation only; no runtime/hardware/deployment verification claimed.
Exact commit, local checks and review status are recorded in #64.
Next owner/action: Codex preserves the reviewable local revision; maintainer
authorizes independent review/publication/merge separately. Historical schema,
effective-time and late-record rules remain open in #10.

## October 19, 2026 — OCT19-DOCS-1 documentation reconciliation

- **Decisions applied:** [BB-003 accepted direction](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991),
  its [UI clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269649488)
  and [buffer-estimate note](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269868018);
  engineering companion [ENG-003](https://github.com/bardphysicslab/engineering-standards/issues/17#issuecomment-6269649466).
- **Scope:** documentation only. No firmware, server, driver, test or script
  change; no pilot, access, deployment, merge, cleanup or history rewrite.
- **Baselines:** Shared guidance: bardphysicslab/engineering-standards@2cb958318b5b603b2b250c351425212e10a64fed.
  BardBox baseline: bardphysicslab/bardbox@31100b88958299560b672d88030bc8e11585d2dd.
- **Work:** branch `codex/oct19-architecture-reconciliation` in the canonical
  BardBox checkout; Claude implements, Codex independently reviews the exact head
  named in the pull request; merge is separately authorized. Companion branch
  `codex/module-checkout-guidance` in engineering-standards.
- **Findings and dispositions:** [October 19 review dispositions](reviews/2026-10-19-documentation-review-dispositions.md).
- **Firmware status after reconciliation:** recording defaults ON for BardBox
  firmware (including serial); the preferred saturation policy is the
  oldest-unacknowledged anchor with oldest-unprotected eviction; the PR #16
  storage and OTA documents are merged drafts, not adopted.

### Open firmware contracts (unchanged by documentation)

1. Serial historical retrieval and acknowledgement.
2. Saturation engineering: token safety, power-loss recovery, tiny capacities,
   compact-chunk representation and interaction with a blocked FIFO head.
3. Exact wire grammar and types, sample metadata placement, STATUS versus INFO.
4. Write/maintenance access policy for production devices.
5. Temporary-override expiry and precedence; partial aggregate windows after
   interval changes.
6. Configuration and queue schema rollback; DC1-to-settings migration.
7. Physical capacity, power-loss, wear and outage evidence.
8. USB startup/OTA reconciliation under the
   [proposed startup contract](firmware-blueprint.md#boot-validation-and-rollback-compatibility).

### Related follow-ups

- Legacy GT-521S driver, contract tests, fixtures and tooling drift:
  [bardbox#49](https://github.com/bardphysicslab/bardbox/issues/49).
- Unpublished PCB template work in the template's canonical checkout (one local
  commit on no remote branch plus untracked fabrication files; not preserved
  off-machine at inventory time; no cleanup authorized):
  [bardbox-project-template#33](https://github.com/bardphysicslab/bardbox-project-template/issues/33).
  Next owner/action: maintainer decides preservation (bundle plus a durable copy
  of untracked files) and whether to publish through a hardware PR.

**Next:** Codex reviews the exact pull-request heads; the maintainer decides merge.
