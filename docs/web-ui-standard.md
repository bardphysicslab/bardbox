# BardBox Web UI Standard

**Classification: REQUIRED for BardBox web applications.** This visual system
is derived from the mature CESH Air and RKC dashboards. It standardizes product
structure, not project-specific sensor content.

October 19, 2026 accepted direction ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991) item 10, [UI clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269649488), [buffer-estimate note](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269868018)) is included
below as documentation; no runtime UI change is implied.

## Foundation

- Use the native system sans-serif stack and the shared dark palette: near-black
  page, dark panels, light text, muted secondary text, Bard red accent, green
  healthy, amber warning, and soft red failure.
- Use a centered content shell no wider than 1400px, with 16-20px desktop
  padding and 14-16px mobile padding.
- Every BardBox dashboard uses a sticky top header with shared Bard branding
  (logo) and the project title on the left, and shows the current time. Absolute
  times are UTC internally; the header may show local time with an explicit
  timezone label. Primary navigation may share the right side of the header.
- Use 26px page titles (22px mobile), 18px section headings, 17-18px card
  titles, 11-14px labels, and 18-24px live values.
- Avoid large white or light-theme cards in BardBox dashboards.

Reference palette tokens (moved from the former monitor instructions):

```css
:root {
  --bg: #050505;
  --panel: #111111;
  --panel-border: #2f2f2f;
  --text: #f5f5f5;
  --muted: #a7a7a7;
  --ok: #52d273;
  --warn: #ffcf5c;
  --bad: #ff7b7b;
  --bard-red: #c9232d;
}
```

## Page structure and navigation

Multi-view applications use a simple landing page of linked project/view cards,
following CESH Air. Detail pages use the RKC/CESH operational hierarchy:

1. header and navigation;
2. concise service summary;
3. current status and primary values;
4. identity and health;
5. configuration and secondary details;
6. tables and historical charts;
7. quiet footer with application identity/version where useful.

Navigation belongs in the header or directly below it and must remain usable at
mobile widths. Do not hide critical status behind navigation.

## Cards, status, and information grouping

- Use an 8px radius, 1px neutral border, dark panel, and 16px card padding.
- Use responsive grids: four columns on wide operational screens, three below
  1200px, two below 900px, and one below 600px. `auto-fit` is acceptable when
  card counts vary, but cards must retain a practical minimum width.
- Keep identity at the top-left and status badges at the top-right.
- Status badges are compact uppercase pills with a border in the status color.
  Never use color as the only signal. Standard meanings and labels are below.
- Availability of a field never implies its display: projects select the
  original and derived values a card shows.
- Missing values render as `—`. Labels precede values; units are visually muted
  and never fused into field names. Timestamps explicitly identify UTC or local
  time and unavailable timestamps render as `—`.
- Never display stale readings as current. Show unavailable and error states
  prominently, and show the last successful time (`last_seen`) separately when
  useful.
- Configured display metadata (human-readable names and installation
  locations) comes from the server Registry, not firmware. Observed GPS
  coordinates from mobile or moving nodes are measurements and are shown as
  such, with their time and units, not as configured location.

### Card top area

Accepted direction; exact remaining fields and placement are deferred to a
representative RKC/CESH review. Every entity card shares one rough top structure:

1. **Entity heading and status.** The entity's familiar display name comes
   first, with its location beneath it ([UI amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270151957)). Name and location are separate
   fields, several entities may share a location, and the name need not equal
   the location. The stable entity ID and the hardware UID are distinct and need
   not be shown in the heading. Contributing hardware identity and health sit
   beneath, normally in a foldout.
2. **Alarm enable/disable switch (when the Alarm module is included).** A
   prominent sliding switch directly below the name, location and status and
   above the headline readings, following the RKC pilot pattern ([switch amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270769043)). It always
   shows whether the alarm is enabled or disabled. Detailed alarm settings stay
   in the expandable Alarm section. Behavior is defined under
   [alarm switch and disabled state](#alarm-switch-and-disabled-state).
3. **Optional prominent reading.** A project may select one or more prominent
   original or derived values (RKC: a single temperature) or none.
4. **Optional buffer fill indicator.** A compact battery-style fill with a rough
   percentage, as CESH does, computed only from telemetry the source actually
   reports (Web Node `buffer_count` and `buffer_max_records`). Omit it for sources
   without that telemetry; never estimate the fill itself or invent values.
   "Catching up" may appear only as a supplementary indication beside this
   indicator, never as the card's main status. Do not
   show raw record counts on the card by default; exact diagnostics stay
   available elsewhere. The indicator must not hide full, error or
   archive-blocked conditions, and it adds no loss display: capacity losses go
   only to the central error log.

**Latest value.** A card shows the newest valid measurement by trustworthy
measurement time. Older records that arrive during catch-up go to history and
never replace a newer latest value. If the newest measurement is stale it is
labelled stale; no fresh-preview or unknown-clock behavior is promised beyond the
existing contracts.

### Card sections from included modules

Accepted direction ([card refinement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270321987)); the provisional mockup is not an accepted field list,
and exact fields remain deferred.

- Sections below the top area are supplied by the modules a project includes, not
  by bespoke project sections for the same capability. Identity and Health are
  common to every card; Hardware, Sensor QA and per-sensor groups (foldouts) are
  optional and configurable; Alarm and Escalation sections are supplied by those
  modules when included.
- **Identity** combines Registry data (stable entity ID, display name, location)
  with the contributing hardware UID. **Health** combines node-reported telemetry
  (for example signal strength, firmware and buffer fill) with server-derived
  contact and freshness owned by the Health module; not all of it is node-owned.
- Prefer one standard **Escalation** section for contacts, acknowledgement and
  next action, independent of the delivery channel (SMS, email or other), shown
  only when escalation is included. An alarm alone does not require it.
- Modules may explicitly declare displayable status, values and control
  descriptors; the project selects which are shown. Full configuration and
  secrets are never exposed automatically.
- **Alarm enable/disable control.** Alarm declares the allowed range and the
  control's meaning, state, permission and label; Rendering supplies the shared
  visual switch and the authorized edit path (save through Alarm, then re-read).
  Its accepted *target* meaning is in
  [alarm switch and disabled state](#alarm-switch-and-disabled-state). Existing
  implementations may differ; this is a documented target, not a runtime change.
- A future AQI or color indicator light is explicitly deferred. Future CESH
  research may examine the PurpleAir Flex dual-PMS6003 correction, averaging and
  AQI method to evaluate matching it; no algorithm is selected or implemented.

### Where editing controls live

Accepted direction ([editable-field rule](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6274318475), a BB-003 supplement); documentation only, not runtime
adoption or authorization for any particular editor.

- **Show values where useful; edit them in one place: the UI section of the
  module that owns the setting.** For example, an entity's name and location
  are edited under Identity (Registry owns them); thresholds under Alarm;
  contacts and escalation under Escalation; display preferences under Rendering
  settings. Values may still be shown elsewhere, but not edited there.
- The card heading and location are ordinary display text. The only way to
  change them is a clearly labelled **Edit name and location** button inside
  Identity.
- **Owners decide what is editable.** Each owning module explicitly declares
  its editable fields and who may change them, and it validates, persists and
  applies changes. Only declared fields are offered: configuration, secrets,
  internal settings and read-only values are never exposed or made editable
  just because they exist.
- **Save path.** Rendering sends an authorized request through Controls, waits
  for the owner to finish saving, then reads and shows the saved values. The
  owner never calls Rendering (for example, Registry never calls Rendering).
- **Drafts and refresh.** Automatic refresh leaves an open editor, its section
  and its unfinished draft alone until Save or Cancel. A response older than a
  completed save must not overwrite the newly saved values.
- **Failures.** A rejected or failed edit keeps the old authoritative values,
  shows useful feedback and is reported centrally. When the outcome is
  uncertain (for example, no response arrived), say so rather than claiming the
  change was rolled back, and offer a way to check the saved values.
- **Exception for frequent operational controls.** A frequent, important
  operational control may stay prominent on the main card, such as the accepted
  [alarm enable/disable switch](#alarm-switch-and-disabled-state) with its
  enabled or disabled state always visible. The owner, permission, save and
  readback rules above still apply to it.
- Existing implementations may differ until adopted. Reference evidence of the
  Identity placement: [BardBox-Reference verification](https://github.com/bardphysicslab/BardBox-Reference/issues/1#issuecomment-6274298406).

### Estimated values

Processing may compute buffer estimates and Rendering shows them clearly
labelled **Estimated**, next to but distinct from the last reported actual
value: for an offline node, the time until its buffer fills (from last-known
occupancy and capacity, recording rate and elapsed time, assuming the node stays
powered and acquiring); for catch-up, the time until the backlog clears, only
when observed net drain supports it. Omit an estimate when inputs are
insufficient or the backlog is growing or not progressing; never show an
invented ETA. These help a technician judge whether a site visit is needed.

### Standard status meanings

Status meanings and labels are standard across BardBox and keep separate
dimensions separate. They reuse existing codes; future runtime adoption maps the
existing statuses explicitly and preserves legacy and target compatibility
labels. The table maps existing meanings and labels; it is not a new main-status
model. The full main-status vocabulary, its precedence and how a card combines
labels remain open.

| Meaning | Label | Legacy reading status | Target owner and representation |
| --- | --- | --- | --- |
| Fresh valid measurement | `LIVE` / `OK` | `ok` | Health freshness; accepted record without channel faults |
| Stale measurement (last valid value older than its stale-after threshold) | `STALE` | `stale` (legacy view nulls declared channels) | Health per-channel freshness; archived values unchanged |
| Node disconnected or unreachable past its offline threshold | `OFFLINE` | `node_unavailable` | Health contact projection from Communications evidence |
| Sensor fault (the source responded but a channel is invalid) | `ERROR` | `error` (legacy view nulls all channels) | Accepted record `status: error` with per-channel `extended.channel_faults`; healthy channels kept |
| FIFO archival delivery blocked by a rejected record | operational health detail | none | `archive_blocked` (Health, from Archive rejection) |
| Alarm condition | `ALARM` | not a reading status | Alarm module state |

`OFFLINE` and `ERROR` are distinct meanings, as in the
[data source drivers](data-source-drivers.md#ui-rule) UI rule. Alarm state is
shown independently of availability: healthy communications (`LIVE`) can coexist
with an active freezer `ALARM`. Project measurement content remains configurable.

### Active-alarm card outline

Accepted direction ([active-alarm outline amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270510607)), codifying the existing RKC behavior as a shared rule:

- While the Alarm module reports an active alarm for the card's entity, the card
  outline pulses red slowly (no rapid flashing) and the card keeps a persistent
  textual `ALARM` indication; color and motion are never the only signal.
- When the viewer prefers reduced motion, show a static red outline with the
  same text instead of the pulse.
- Only the Alarm-owned active alarm state triggers it. Freshness or connection
  status and air-quality or other category colors never do: an orange AQI
  category alone does not pulse. Keep the alarm outline visually distinct from
  those colors.
- This standard does not define AQI methods or thresholds, and it adds no
  escalation scope or runtime change.
- The outline also applies while the alarm is disabled but its condition is
  active (below).

### Alarm switch and disabled state

Accepted direction ([switch amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270769043)); documentation only, not a runtime change.

- **Disabled pauses delivery, not evaluation.** "Alarm disabled" immediately
  pauses notifications and escalation. Acquisition, measurement and evaluation of
  the alarm condition continue. Re-enabling is manual only; automatic re-enable
  and text-message reminders are not adopted.
- **Disabled with an active condition never looks healthy.** The active-alarm
  outline, the persistent `ALARM` text and the reduced-motion equivalent still
  apply, together with the visible disabled state.
- **Reminder when back in range.** When the alarm is disabled and its condition
  has returned within range, the card shows an on-card reminder such as
  "Within range — alarm disabled. Re-enable when ready."
- **Only truthful in-range claims.** The reminder rests on valid, fresh evidence
  for the alarm's *condition channels*. Under per-channel validity
  ([BB-001](DECISIONS.md)), a fault on an unrelated channel does not null or
  invalidate a healthy in-range condition channel. If Health cannot establish
  fresh, valid evidence for the relevant condition (including a stale or unknown
  freshness basis, an offline node or failed condition channels), the card does
  not claim it is currently within range; it shows the disabled state with the
  applicable status instead. Trusted live observations may be fresh by their
  explicitly labelled observation time under project policy even when
  measurement time is unknown, while pushed and archived records never use
  receipt time as a fallback
  ([measurement time and observation freshness](ingestion-contract.md#measurement-time-and-observation-freshness)). The precise freshness basis and gating (hold time, hysteresis) stay
  open against the existing reading, health and ingestion contracts; this
  section selects no aggregate status policy.
- **Service alarms are illustrative.** An alarm for a node going offline or
  failing (for example at CESH) would be an Alarm rule consuming Health status;
  no timeout or detection policy is settled, and this illustrative example
  imposes no requirement on CESH or other projects (RKC's existing alarm
  requirement is unchanged).
- **Open:** switch scope when an entity has several alarm rules (per entity, as
  in RKC, or per rule); whether escalation restarts or resumes when re-enabled
  during an active condition; whether switch changes are audited with actor and
  time; exact label and reminder wording.

## Foldouts, tables, charts, and controls

- Use native `<details>`/`<summary>` for secondary card information. Identity,
  health, hardware, and configuration foldouts are collapsed by default so live
  status remains scannable. Preserve a user's open state during live refreshes
  when practical.
- Tables use the panel border, left-aligned headers, compact 10-12px cell
  padding, muted headers, and horizontal scrolling on narrow screens.
- Charts follow current status and explanatory tables. Put charts in bordered
  panel containers with a title, time range, legend, units, and a clear empty
  state. Never place an unlabeled graph above an active alarm/status summary.
- Buttons follow RKC: 6px radius, neutral border, dark fill, 9px by 12px padding,
  clear focus state, disabled opacity, and Bard red only for destructive actions.

## Responsive and accessibility behavior

At mobile widths, stack cards and metrics, keep header content readable, allow
tables to scroll, and use touch targets near 40px where practical. Preserve
semantic headings, buttons, links, tables, and native disclosure controls.
Visible focus styles and textual status labels are required.

## Reference decisions

CESH Air is preferred for landing pages, responsive card breakpoints, compact
metrics, and foldouts. RKC is preferred for general controls, form/table
treatment, and alarm hierarchy. Both use the same typography, palette, sticky
header, badge language, spacing scale, and card geometry; those shared choices
form the standard.
