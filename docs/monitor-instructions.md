# Monitor and UI Standard

RKC Monitor is the current BardBox visual reference.

## Required Visual Language

- dark theme
- `system-ui, sans-serif`
- sticky Bard header with Bard logo
- compact cards with 8px border radius
- consistent card sizing and spacing
- status badges for `ok`, `stale`, `error`, and `node_unavailable`
- red unavailable/error state
- muted secondary text
- `—` for `null` values

Reference colors:

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

## Data Display Rules

- Do not display stale readings as current.
- Render `null` channel values as `—`.
- Show unavailable/error badges prominently.
- Show `last_seen` separately when useful.
- Human-readable names and locations come from deployment config, not firmware.

## Layout Rules

Use a shell similar to:

```css
.shell {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 20px 40px;
}
```

Cards should be compact operational units for nodes, instruments, or grouped
measurements. Avoid large white/light-theme cards in BardBox dashboards.
