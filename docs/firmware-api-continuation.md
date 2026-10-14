# Firmware serial and buffer API continuation

October 14, 2026. Authoritative task: https://github.com/bardphysicslab/bardbox/issues/31.

One maintained serial/base draft: [firmware-base-and-serial-api.md](firmware-base-and-serial-api.md).
One maintained optional buffer API draft: [firmware-buffer-api.md](firmware-buffer-api.md).
This consolidates the serial draft from codex/usb-provisioning-standard at ab83ab3
without deleting the provenance branch. The old branch is a historical snapshot;
future API changes belong in these documents. Storage framing remains covered by
the pending compact-storage proposal (PR #16); no competing format is introduced.

## Checkpoint

- Repository: bardphysicslab/bardbox; canonical checkout used, owner Codex / serial firmware discussion.
- Baseline: da62d8dd9c151a53e56388a1ced354d8ca01cf97.
- Feature: codex/serial-buffer-api; exact handoff commit is recorded in the GitHub issue/PR after commit.
- Shared guidance: bardphysicslab/engineering-standards@28e2dceb882d1de0e4948ca7b11f7322e792284d.
- Scope: documentation only, pending review; no implemented shared API, migration, merge or deployment.
- Evidence: Markdown relative links and whitespace checked. Existing CESH queue fault test re-run: 1 passed with simulated LittleFS and sanitizers; no physical power-loss/retention test.
- Consumers checked: CESH 345b6bb7b18bd3d7eb7eb33b3bc7550a69021110; RKC 0c4f9238a7c85f282a69d92f4142c6eea06f184e.
- Preservation: feature commit/remote branch to be recorded in the task issue. Earlier proposal branch is retained; no legacy checkout retired.

## Next step and open decisions

Kornelis reviews the two APIs; then resolve wire grammar/types, metadata compatibility,
access policy, temporary overrides, partial aggregate windows, saturation policy,
operation-history bounds and schema rollback before implementation. Build independent
sensorless/BME280 and individual/aggregate queue consumers before project migrations.
Time synchronization remains a separate discussion; supplied validity crosses the interface.

CESH already saves FIFO records before delivery and removes them after acknowledgement;
new public API names/tokens/tickets are proposals. RKC intends to preserve individual
readings through network outages; this is not yet implemented. CESH aggregation remains
project-owned. Physical storage capacity, power loss, wear and outage recovery remain
separate acceptance gates. No device operation authorized.

The agreed platform board remains pending existing-work/Trello reconciliation. Existing
#11/PR #21 proposes synchronization, which conflicts with the current GitHub-authoritative
migration direction; do not enable it silently. Retain historical references. This API
issue remains discoverable through README/AGENTS even before board setup.

No skills changed; no template implementation changed. Template integration and CESH/RKC
adoption are deferred until reviewed contracts. Next checkpoint: maintainer design review;
check status at the next firmware task. Unmerged proposal branch is retained for review.
