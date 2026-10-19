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
- Never reuse a retired UID; check the project registry before assigning one.
- Physically label devices with their UID whenever possible.

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
| `jst` | JustAir (historical entry; JustAir is an external data consumer, not a BardBox site; do not assign for new nodes) |

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

## Identity layers

Accepted October 19, 2026 ([decision entry](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991), item 4).
The UID grammar above is unchanged.

| Identity | Identifies | Owner |
| --- | --- | --- |
| Node UID | A BardBox node definition (the hardware data source) | Project Registry |
| Monitored entity | The thing or place measured, such as a freezer or Stevenson Roof; stable across hardware replacement | Project Registry (entity association) |
| Application ID | The deployed software system and what it provides | Project configuration |

- Settings and history that belong to the entity (for example alarm settings and
  thresholds) persist through hardware replacement. Historical records keep
  their original node attribution and are never rewritten.
- Exact entity IDs, effective-time binding and how replacement hardware is
  attributed remain contract work. No automatic pilot migration is accepted.
  Customer claiming, MAC integration and consumer keys remain deferred
  ([firmware-tools#41](https://github.com/bardphysicslab/firmware-tools/issues/41),
  [bardbox#10](https://github.com/bardphysicslab/bardbox/issues/10)).
- A UID is not an authentication credential; writing one to a board does not
  register it ([USB provisioning](usb-provisioning-standard.md#identity-registry-and-replacement)).

### Registry status values

The project Registry records each UID as **Active** (deployed and in use),
**Reserved** (assigned, not yet deployed) or **Retired** (no longer used; the
UID stays reserved). There is no maintained shared UID spreadsheet; the former
placeholder in `uid-registry.md` was retired on October 19, 2026. A shared
allocation service remains the deferred registry workstream linked above.

## Application identity

Moved from the former implementation guide on October 19, 2026.

The App ID names the deployed system's role, not its hardware:

```text
bb-{app-name}
```

- Describe what the system measures or provides (`bb-golab-air-quality`,
  `bb-cleanroom-air-quality`, `bb-gallery-environment`), not sensors, wiring or
  transport (avoid `bb-monitor`, `bb-pms-bme-arduino`).
- Lowercase, hyphen-separated, human-readable, stable across deployments and
  specific enough to distinguish systems.
- An optional instance ID `{app-id}-{host-or-location}` (for example
  `bb-golab-air-quality-pi01`) helps logging and multi-instance deployments.

The legacy Pi runtime's `app_id` field ([Pi runtime instructions](pi-runtime-instructions.md#app-identity))
uses this format.
