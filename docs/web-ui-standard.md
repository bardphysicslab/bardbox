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
2. **Optional prominent reading.** A project may select one or more prominent
   original or derived values (RKC: a single temperature) or none.
3. **Optional buffer fill indicator.** A compact battery-style fill with a rough
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
  optional and configurable.
- Prefer one standard **Escalation** section for contacts, acknowledgement and
  next action, independent of the delivery channel (SMS, email or other), shown
  only when escalation is included. An alarm alone does not require it.
- Modules may explicitly declare displayable status, values and control
  descriptors; the project selects which are shown. Full configuration and
  secrets are never exposed automatically.
- **Alerts control.** Alarm declares the allowed range and the alerts control's
  meaning, state, permission and label; Rendering supplies the shared visual
  control and the authorized edit path (save through Alarm, then re-read). The
  accepted *target* meaning: turning alerts off pauses notifications and
  escalation while measurement and alarm evaluation continue. Existing
  implementations may differ; this is a documented target, not a runtime change.
- A future AQI or color indicator light is explicitly deferred.

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
