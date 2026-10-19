# Monitor and UI Standard (redirect)

Consolidated into the [BardBox Web UI standard](web-ui-standard.md) on
October 19, 2026 ([bardbox#31 decision entry](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991)).
That standard is the single maintained UI guidance; CESH Air and RKC jointly
define its reference.

- Palette tokens, dark theme and card geometry moved there unchanged.
- The data display rules (no stale data shown as current, `—` for nulls,
  separate `last_seen`, names from server configuration) moved there.
- This file's earlier 1440px shell example conflicted with the Web UI standard's
  1400px shell; the Web UI standard governs.
- Its claim that RKC alone is the visual reference is superseded by the joint
  CESH/RKC reference.

The earlier text remains in Git history at
`31100b88958299560b672d88030bc8e11585d2dd`.
