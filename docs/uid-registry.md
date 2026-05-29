# BardBox UID Registry

Every BardBox device must have a unique immutable identifier.

## UID Format

New UIDs use:

```text
bb-<site>-<type>-<instance>
```

Examples:

- `bb-gol-air-001`
- `bb-rkc-frz-014`
- `bb-sol-sol-001`

Rules:

- Prefix is always `bb`.
- Site code is exactly 3 lowercase letters.
- Type code is exactly 3 lowercase letters.
- Instance is exactly 3 digits with leading zeros.
- Use hyphens only.
- UID must not change after deployment.

See `node-naming-standard.md` for site and type code examples.

## Legacy IDs

Legacy IDs like `bb-0001`, `bb-0002`, and `bb-0003` remain supported for
existing deployments, but are deprecated. Do not assign legacy-format IDs to new
devices.

## Source of Truth

The authoritative UID registry is maintained in Google Sheets:

**[INSERT UID REGISTRY LINK HERE]**

Always check the registry before assigning a new UID, and do not reuse retired
UIDs.

## Where the UID Lives

Programmable devices store the UID in firmware:

```cpp
#define DEVICE_UID "bb-gol-air-001"
```

Non-programmable instruments should have their UID assigned in Raspberry Pi
driver configuration.

Physically label devices with their UID whenever possible.

## Example Entries

| UID | Description | Project | Status |
| --- | --- | --- | --- |
| `bb-gol-air-001` | Air monitor node | GoLab Monitor | Active |
| `bb-rkc-frz-001` | Freezer monitor node | RKC Monitor | Active |

Status values:

- **Active**: currently deployed and in use.
- **Retired**: no longer in use, UID remains reserved.
- **Reserved**: assigned but not yet deployed.
