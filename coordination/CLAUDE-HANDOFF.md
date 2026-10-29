# Claude handoff: per-workflow application services (amendment to the server-diagram PR)

- **Event:** `WORKFLOW-SERVICES-DOCS` (WORKFLOW-SERVICES-DIRECTION-1), October 29, 2026. **Status:** complete, ready for Codex independent exact-head review. Documentation only.
- **Same PR, separate amendment:** [bardbox#74](https://github.com/bardphysicslab/bardbox/pull/74), branch `claude/access-control-docs`. The Access Control commits are preserved unchanged: `f41e6ef`, `cbd69ae`, `be55eb5` (author head, PASS) and `8a3130e` (Codex review). The amendment content commit is `c7e9e65`; this handoff is the next commit. Not merged; Claude does not self-merge.
- **Accepted scope:** [bardbox#31 comment 6501064832](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6501064832), after the [Claude](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6500893028) and [Codex](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6500908431) evaluations.
- **Guidance:** engineering-standards `91a2d7c`; BardBox baseline `fb0c4c9`.
- **Contract inventory** (read-only, next-step recommendation): [bardbox#31 comment 6501149067](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6501149067).
- **Previous handoff** (ACCESS-CONTROL-DOCS): archived at [archive/CLAUDE-HANDOFF-ACCESS-CONTROL-DOCS.md](archive/CLAUDE-HANDOFF-ACCESS-CONTROL-DOCS.md). Only its one relative link changed. Codex's review in `coordination/CODEX-REVIEW.md` (PASS at `be55eb5`) is left unchanged.

## What changed in `c7e9e65`

1. **`docs/architecture-map.md`, server diagram:**
   - **Delivery acceptance workflow** (a per-use-case application service; API PROPOSED / TBD; no authoritative state). It sits between the normalized Communications output and the owners:
     - it takes the Registry's consistent snapshot and duplicate context, then calls the pure `validate(record, delivery, registry_snapshot)` and gets its result back;
     - it sends archive records to Archive and receives back a durable acceptance or a known duplicate;
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

## Checks

- **Mermaid:** all three diagrams parse and render with mermaid 10.9.1. The rendered server SVG contains the new workflow, ACK, snapshot, revision, outcome and Composition labels. Visual check page, outside the repository: `/private/tmp/claude-501/-Users-kornelispoort-Documents-Codex-2026-09-17-i-w-work-bardbox-slack-bot/af9e9a17-9f20-4ce0-9119-f53f69d29f2b/scratchpad/bardbox-access-control-mermaid/index.html`. Serve that folder over loopback HTTP; it loads mermaid 10.9.1 from jsDelivr.
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
