# Node Naming Standard

BardBox node UIDs identify the platform, site, node type, and deployment
instance at a glance.

## Format

```text
bb-<site>-<type>-<instance>
```

Examples:

- `bb-gol-air-001`
- `bb-gol-air-002`
- `bb-rkc-frz-001`
- `bb-rkc-frz-014`
- `bb-sol-sol-001`
- `bb-csh-air-001`
- `bb-heg-snd-001`

## Rules

- Prefix is always `bb`.
- Site code is exactly 3 lowercase letters.
- Type code is exactly 3 lowercase letters.
- Instance is exactly 3 digits with leading zeros.
- Use hyphens only.
- UID must be immutable once deployed.

Regular expression:

```text
^bb-[a-z]{3}-[a-z]{3}-[0-9]{3}$
```

## Site Codes

| Code | Site |
| --- | --- |
| `gol` | GoLab |
| `rkc` | RKC |
| `sol` | Solar |
| `csh` | CESH |
| `heg` | Hegeman |
| `jst` | JustAir |

## Type Codes

| Code | Type |
| --- | --- |
| `air` | air monitor |
| `frz` | freezer monitor |
| `sol` | solar sensor |
| `snd` | sound monitor |
| `wtr` | water monitor |
| `pwr` | power monitor |
| `tmp` | temperature monitor |
| `dor` | door monitor |
| `wth` | weather monitor |

## Legacy UIDs

Legacy IDs like `bb-0001`, `bb-0002`, and `bb-0003` remain supported for
existing deployments, but are deprecated. All new deployments must use
`bb-<site>-<type>-<instance>`.

## Runtime Aliasing

During migration, a device may still report an old UID such as `bb-0001`,
`rkc-01`, or `spn1-0001`. The Pi/backend may map those legacy reported IDs to
the canonical new UID in configuration:

```json
{
  "uid": "bb-gol-air-001",
  "legacy_uids": ["bb-0001"]
}
```

Rules:

- API responses must expose the canonical new UID.
- Dashboard cards must show the canonical new UID.
- New logs must use the canonical new UID.
- Historical logs must be left untouched and not rewritten.
- Firmware should be updated to report the canonical UID when practical.
