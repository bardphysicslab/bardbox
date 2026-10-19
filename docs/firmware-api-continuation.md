# Firmware design continuation

Current entry. The dated October 14–16 checkpoints, source-to-final mapping and
earlier open-decision list are archived unchanged in
[archive/firmware-api-continuation-2026-10-14-to-16.md](archive/firmware-api-continuation-2026-10-14-to-16.md).
GitHub ([bardbox#31](https://github.com/bardphysicslab/bardbox/issues/31)) is
authoritative for status; this file does not embed its own commit hash.

## October 19, 2026 — OCT19-DOCS-1 documentation reconciliation

- **Decisions applied:** [BB-003 accepted direction](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991),
  its [UI clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269649488)
  and [buffer-estimate note](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269868018);
  engineering companion [ENG-003](https://github.com/bardphysicslab/engineering-standards/issues/17#issuecomment-6269649466).
- **Scope:** documentation only. No firmware, server, driver, test or script
  change; no pilot, access, deployment, merge, cleanup or history rewrite.
- **Baselines:** Shared guidance: bardphysicslab/engineering-standards@2cb958318b5b603b2b250c351425212e10a64fed.
  BardBox baseline: bardphysicslab/bardbox@31100b88958299560b672d88030bc8e11585d2dd.
- **Work:** branch `codex/oct19-architecture-reconciliation` in the canonical
  BardBox checkout; Claude implements, Codex independently reviews the exact head
  named in the pull request; merge is separately authorized. Companion branch
  `codex/module-checkout-guidance` in engineering-standards.
- **Findings and dispositions:** [October 19 review dispositions](reviews/2026-10-19-documentation-review-dispositions.md).
- **Firmware status after reconciliation:** recording defaults ON for BardBox
  firmware (including serial); the preferred saturation policy is the
  oldest-unacknowledged anchor with oldest-unprotected eviction; the PR #16
  storage and OTA documents are merged drafts, not adopted.

### Open firmware contracts (unchanged by documentation)

1. Serial historical retrieval and acknowledgement.
2. Saturation engineering: token safety, power-loss recovery, tiny capacities,
   compact-chunk representation and interaction with a blocked FIFO head.
3. Exact wire grammar and types, sample metadata placement, STATUS versus INFO.
4. Write/maintenance access policy for production devices.
5. Temporary-override expiry and precedence; partial aggregate windows after
   interval changes.
6. Configuration and queue schema rollback; DC1-to-settings migration.
7. Physical capacity, power-loss, wear and outage evidence.
8. USB startup/OTA reconciliation under the
   [proposed startup contract](firmware-blueprint.md#boot-validation-and-rollback-compatibility).

### Related follow-ups

- Legacy GT-521S driver, contract tests, fixtures and tooling drift:
  [bardbox#49](https://github.com/bardphysicslab/bardbox/issues/49).
- Unpublished PCB template work in the template's canonical checkout (one local
  commit on no remote branch plus untracked fabrication files; not preserved
  off-machine at inventory time; no cleanup authorized):
  [bardbox-project-template#33](https://github.com/bardphysicslab/bardbox-project-template/issues/33).
  Next owner/action: maintainer decides preservation (bundle plus a durable copy
  of untracked files) and whether to publish through a hardware PR.

**Next:** Codex reviews the exact pull-request heads; the maintainer decides merge.
