# Claude handoff: per-workflow application services (amendment to the server-diagram PR)

- **Event:** `WORKFLOW-SERVICES-DOCS` (WORKFLOW-SERVICES-DIRECTION-1), October 29, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Same PR, separate amendment:** [bardbox#74](https://github.com/bardphysicslab/bardbox/pull/74), branch `claude/access-control-docs`. The Access Control commits are preserved unchanged: `f41e6ef`, `cbd69ae`, `be55eb5` (author head, PASS) and `8a3130e` (Codex review). **Correction:** `c7e9e65` contains only the archive rename of the previous handoff, despite its message; the diagram, DECISIONS and continuation edits were never staged. `9cad466` added this handoff only. All of the amendment content, with the Codex ownership correction below, is in the **next commit after `9cad466`**, which is the PR head to review. Not merged; Claude does not self-merge.
- **Accepted scope:** [bardbox#31 comment 6501064832](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6501064832), after the [Claude](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6500893028) and [Codex](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6500908431) evaluations.
- **Guidance:** engineering-standards `91a2d7c`; BardBox baseline `fb0c4c9`.
- **Contract inventory** (read-only, next-step recommendation): [bardbox#31 comment 6501149067](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6501149067).
- **Previous handoff** (ACCESS-CONTROL-DOCS): archived at [archive/CLAUDE-HANDOFF-ACCESS-CONTROL-DOCS.md](archive/CLAUDE-HANDOFF-ACCESS-CONTROL-DOCS.md). Only its one relative link changed. Codex's review in `coordination/CODEX-REVIEW.md` (PASS at `be55eb5`) is left unchanged.

## What changed (amendment content, in the commit after `9cad466`)

1. **`docs/architecture-map.md`, server diagram:**
   - **Delivery acceptance workflow** (a per-use-case application service; API PROPOSED / TBD; no authoritative state). It sits between the normalized Communications output and the owners:
     - it takes the Registry's consistent snapshot and identity context (corrected at review: originally "duplicate context"), then calls the pure `validate(record, delivery, registry_snapshot)` and gets its result back;
     - it calls Archive in two steps: first the duplicate lookup for a retry, then new validated records. Archive returns a known accepted duplicate or a durable acceptance;
     - **the ACK goes out only after durable acceptance or a known duplicate**;
     - eligible accepted readings are published to Latest, with previews kept separate;
     - contact and validity evidence goes to Health.

     These edges replace the earlier direct Ingestion → Archive/Latest/Health and Archive → Push edges. Ingestion is labelled pure.
   - **Multi-owner save workflow** (for example the Reference card save): Controls sends it an authorized request that spans owners. It calls the Registry and module-owned settings through their own APIs, each with its own revision, and returns each owner's confirmed, partial or uncertain result.
   - **Controls → Alarm** is labelled as the single-owner case ("disable alerts: Alarm decides, persists, confirms").
   - **Composition** is added as "startup construction and injection only", wiring both workflows.
   - **Unchanged:** Access Control and the other nodes.
2. **`docs/architecture-map.md`, text:** a new "Per-workflow application services" section. It separates the accepted conceptual role from the PROPOSED / TBD APIs and failure policies, and covers:
   - the existing callers and Controls as the default, with injected owner interfaces
   - Composition as wiring only
   - stateless services that never write another owner's state; owners never import their callers
   - no router or event bus, and reads that bypass command services
   - the human write path and the sensor delivery path, with the unchanged ingestion contract and ACK rule, and RKC's simpler adapter
   - no rollback, transaction or retry promise
   - the current state: no Reference receiving pipeline, and no delivered services
3. **`docs/DECISIONS.md`:** one new WORKFLOW-SERVICES-DIRECTION-1 row.
4. **`docs/firmware-api-continuation.md`:** a new latest entry. The Access Control entry becomes history and points to its archived handoff.

**Unchanged:**
- the node and USB flasher diagrams (checked; no workflow or auth conflict)
- the ingestion contract and other standards
- runtime code
- CESH and RKC

## Review correction (Codex, `9cad466`)

The ownership of the duplicate lookup is fixed in the same commit, which also carries the previously unstaged amendment content. No API or schema changed.
- **Registry** supplies the consistent snapshot and **identity context**.
- **Archive** owns the duplicate lookup, the comparison and durable acceptance. The workflow asks Archive's duplicate lookup **before** today's validation, for a known accepted retry ([ingestion contract, retry rule](../docs/ingestion-contract.md#envelope-rejection-and-durable-acceptance)).
- **New records** go through pure validation, then Archive acceptance.
- **A known accepted duplicate** is ACK-eligible but never published as a new measurement.
- **Still TBD:** previews stay separate; the projection policy is unchanged.

The diagram edge labels and the "Sensor delivery" paragraph are updated. The checks below were re-run after the correction.

**Open compatibility interface (planning, not verified).** This is recorded from the [Template #36 criterion](https://github.com/bardphysicslab/bardbox-project-template/issues/36#issuecomment-6501140669) and [CESH #72](https://github.com/bardphysicslab/cesh-air-monitor/issues/72#issuecomment-6501141051). It belongs to the inventory, not to new diagram or runtime work.
- **What must fit:** next week's firmware has to fit the **current chosen USB workflow**: the board and flash size, the dual-slot layout, the build artifacts, the image size, the install manifest and selection rules, and the serial identity, settings and diagnostic commands.
- **What must be shown:** preserved identity, settings and queued readings, plus boot and read-back evidence.
- **Not the same protocol:** CESH `PROVISION_*`/`WIFI_*` is not Reference `config/1`.
- **Status:** not verified; no builds or flashing.
- **Sequence:** the pilot can launch with the existing engineer preparation, without the future student tool. The final student trial comes after compatible firmware and prepared devices.

## Checks

- **Mermaid:** all three diagrams parse and render with mermaid 10.9.1. The rendered server SVG contains the new workflow, ACK, snapshot, revision, outcome and Composition labels. The check used the author's temporary render-check page outside the repository (Mermaid 10.9.1).
- **Fences:** balanced (6).
- **Links and anchors:** local links and anchors resolve in the changed files.
- **Whitespace:** `git diff --check` is clean.
- **Runtime tests:** none, because no code changed.

## Limits

- **Conceptual only:** this is a conceptual role. No service API, outcome vocabulary, retry or partial-failure policy is selected.
- **Nothing delivered:** the Reference card save and any delivery pipeline are not delivered as services.

## Next step and owner

1. **Codex** reviews the amendment at the exact PR head. Corrections go on this branch.
2. **Kornelis** decides on merging the combined PR and picks the next contract discussion from the inventory.
