# Bard Box Standard — Monitor Instructions

## Purpose

Define the layout and visual requirements for Bard Box sensor dashboards.

This document covers frontend presentation standards only. It does not define
backend behavior, data formats, or sensor logic — see `pi-runtime-instructions.md`
and `reading-format.md` for those.

---

## Required Header Elements

Every Bard Box dashboard must include a page header containing:

1. **Bard College logo** — use an approved logo from the `static/Bard-Web-Logos/`
   directory. The red logo (`bard-logo-red.png`) is recommended for dark
   backgrounds.
2. **System title** — a clear, human-readable name describing the deployment
   context. This should identify the lab or location, not the hardware.

Example:

```
[Bard logo]  Gravitational-wave Optics Lab Environmental Monitor
```

Rules:
- Logo and title must appear together on the same line
- Title must not describe specific sensors or hardware (e.g. not "GT-521S Monitor")
- Hardware identity belongs inside the relevant instrument section, not the header
- Header must remain visible at all times — it must not scroll off-screen in primary views

---

## Recommended Header Elements

- **Clock** — a live display of the Raspberry Pi system time (local timezone).
  Recommended but not required. Useful for operators to confirm the dashboard
  is live and that system time is correct.

---

## Layout Principles

### Instrument sections

Each physical instrument or sensor group should have its own clearly labeled
section. The section title should identify the instrument (e.g.
"GT-521S Particle Counter", "Environment Node").

Group related controls and data displays together within one section — do not
split an instrument's settings and graphs into separate disconnected cards.

### Data display

- Show live readings prominently with units clearly labeled
- Use consistent units throughout — do not mix unit systems on the same dashboard
- Null or unavailable values must display as `—`, not zero
- Status indicators (`ok`, `stale`, `error`) should be visually distinct

### Threshold display

- Threshold lines on charts must reflect the currently active threshold
- If a threshold is not defined for a channel, omit the threshold line entirely
- Do not display a default or placeholder threshold line when none is configured

### Responsive behavior

Dashboards should be usable on both desktop and tablet. A single-column
fallback at narrow viewport widths is acceptable.

---

## Branding

- Use Bard College logo assets from `static/Bard-Web-Logos/`
- Do not modify or distort the logo
- Available variants: red, black, gray, white (with and without "College" wordmark)
- Choose the variant appropriate for the background color

---

## Out of Scope

This document does not define:
- Specific frontend frameworks or libraries
- Color schemes or visual themes beyond the requirements above
- Data export or print layouts
- Authentication or access control
