# GPT Instructions for BardBox

This is a concise GPT-facing summary of the BardBox standards. Use the detailed
docs in this repo when implementation detail is needed.

## Repo Roles

- `bardbox` is the standards/specification repo.
- `bardbox-project-template` is the reference implementation and GitHub template.
- Project repos inherit from `bardbox-project-template`.

## Update Workflow

1. Document protocol, architecture, or UI standard changes in `bardbox` first.
2. Implement those changes in `bardbox-project-template` second.
3. Update project repos third, such as GoLab, RKC, Solar, and CESH Air.

## Node UID Standard

New node UIDs use:

```text
bb-<site>-<type>-<instance>
```

Example: `bb-gol-air-001`

Rules:

- `site` is exactly 3 lowercase letters.
- `type` is exactly 3 lowercase letters.
- `instance` is exactly 3 digits.
- Legacy IDs are supported for existing deployments but deprecated.

## Firmware Standard

- Use VS Code + PlatformIO.
- Arduino framework is allowed through PlatformIO.
- Arduino IDE is not the BardBox standard.
- Firmware supports `INFO`, `HEADER`, and `READ`.
- `START` and `STOP` are only required for session or streaming devices.

## Reading and Status Standard

Statuses:

- `ok`: fresh valid reading.
- `stale`: last valid reading exists but is older than the freshness timeout.
- `error`: device responded with invalid, malformed, or unparseable data.
- `node_unavailable`: device could not be reached or did not respond.

Stale, error, and unavailable values are `null` in API responses. Dashboards
render `null` as `—`. Never show cached values as live.

## Driver Standard

- Pi/backend determines freshness.
- Drivers track `last_seen` and last valid reading where applicable.
- Transport failure maps to `node_unavailable`.
- Parse failure maps to `error`.
- API responses use normalized new UIDs, including when legacy UIDs are aliased.

## UI Standard

RKC Monitor dark theme is the BardBox visual standard:

- compact cards
- status badges
- Bard logo/header
- `system-ui, sans-serif`
- dark background and panel styling
- red error/unavailable states

## Time Standard

- Pi time must be valid before trusted logging or session start.
- Use UTC timestamps in APIs and logs where possible.
- Local time display is fine on dashboards.

## Future GPT Rule

When helping with BardBox, follow these standards unless the user explicitly
says they are changing the standard. If a project repo conflicts with `bardbox`,
treat `bardbox` as authoritative and recommend updating the project/template.
