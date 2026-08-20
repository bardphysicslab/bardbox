# BardBox Web UI Standard

**Classification: REQUIRED for BardBox web applications.** This visual system
is derived from the mature CESH Air and RKC dashboards. It standardizes product
structure, not project-specific sensor content.

## Foundation

- Use the native system sans-serif stack and the shared dark palette: near-black
  page, dark panels, light text, muted secondary text, Bard red accent, green
  healthy, amber warning, and soft red failure.
- Use a centered content shell no wider than 1400px, with 16-20px desktop
  padding and 14-16px mobile padding.
- Use a sticky top header with Bard logo and application title on the left and
  compact local/UTC time or primary navigation on the right.
- Use 26px page titles (22px mobile), 18px section headings, 17-18px card
  titles, 11-14px labels, and 18-24px live values.

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
  Standard wording is `LIVE`/`OK`, `STALE`/`WARNING`, `OFFLINE`/`ERROR`, and
  `ALARM` where applicable. Never use color as the only signal.
- Missing values render as `—`. Labels precede values; units are visually muted
  and never fused into field names. Timestamps explicitly identify UTC or local
  time and unavailable timestamps render as `—`.

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
