# Claude handoff: Access Control in the server diagram

- **Event:** `ACCESS-CONTROL-DOCS` (ACCESS-CONTROL-DIRECTION-1), October 29, 2026. **Status:** Codex review corrections applied; ready for Codex exact-head re-review. Documentation only.
- **Content head:** `f41e6ef` on `claude/access-control-docs`, from clean `main` `fb0c4c9` (verified against the remote before branching). This handoff is the next commit on the same branch; the PR head is that commit, pushed. Not merged; Claude does not self-merge.
- **Accepted scope:** [bardbox#31 comment 6500637310](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6500637310). D6 stays open.
- **Guidance:** engineering-standards `91a2d7c`; BardBox baseline `fb0c4c9`.
- **Previous handoff** (DISPLAY-UNITS-DOCS, PR #72, merged as `fb0c4c9`): archived at [archive/CLAUDE-HANDOFF-DISPLAY-UNITS-DOCS.md](CLAUDE-HANDOFF-DISPLAY-UNITS-DOCS.md). Only its one relative link changed (to the sibling archive file).

## What changed

1. **`docs/architecture-map.md`, server diagram:**
   - **The existing `Auth` node** is now **Access Control (existing authentication owner)**: authentication identifies the person, device or partner; authorization decides permitted project pages, data and actions. Roles, sessions and the contract/API are marked **PROPOSED / TBD**. The node moved out of the Communications-and-ingestion box, because it covers more than device intake. There is no second auth node.
   - **New nodes:**
     - **People:** approved project members only; a sign-in or link grants no membership.
     - **Server page endpoints:** feed Rendering.
     - **Login adapters (PROPOSED contract):** replaceable; for example an existing basic/password login where present, Bard Google later.
   - **Edges:** `enforce: pages`, `enforce: reads` (Queries) and `enforce: writes` (Controls).
   - **Labels:** Rendering "reflects permissions, never authorizes"; Controls "routes authorized requests to owners".
   - **Kept, now labelled:** `device credentials (unchanged)` to Communications, and `partner keys (unchanged)` to the Partner API.
2. **`docs/architecture-map.md`, text:**
   - **New "Access Control" section** under the diagram. It separates the accepted conceptual direction from the PROPOSED contract, API and runtime adoption, and covers:
     - the three enforcement boundaries
     - owner validation
     - replaceable login adapters, with membership not implied by sign-in
     - the RKC viewer and manager/admin example, with no freezer-power switching
     - unchanged machine and partner boundaries (D7, D10)
     - the same contract in every project, with no provider required now
     - the open D6 items
   - **The `software/app/authentication/` layout name** is kept as the current name.
   - **Row 15 owner** now names Access Control at the page, read and write boundaries. **D6** records the accepted conceptual direction and its remaining open items.
3. **`docs/DECISIONS.md`:** one new row, ACCESS-CONTROL-DIRECTION-1, linking the acceptance. Earlier rows are kept.
4. **`docs/firmware-api-continuation.md`:** a new latest entry. The previous entry becomes history and records its merge (`fb0c4c9`, bardbox#72).

**Unchanged:**
- the node and USB flasher diagrams. The flasher's "Operator authentication" belongs to the USB application server and is consistent.
- `repository-layout.md`, `network-access.md` (linked, not edited) and the other standards
- runtime code, folders, providers and deployed access
- RKC and CESH runtimes

## Review corrections (Codex, `cbd69ae`)

These are applied in the commit after `cbd69ae` on this branch. They change wording only; the diagram structure is unchanged.
1. **Layout name:** `software/app/authentication/` is called the **documented layout name**, an architectural folder name, not evidence of an implemented Access Control API.
2. **Credentials (16) note:** this note sits in "Server data inventory and module operations". It no longer says "operator login in Controls". It now says Access Control verifies people and their permissions at the server page, Query/read and Controls/write boundaries, and that this grants no other module access to secrets. The device (Communications), historical Data API (Query), partner-key and provider credential rules are kept.
3. **Login adapters:** basic/password is an example of an existing login where a project has one (RKC's environment admin login today), not a universal current runtime. Bard Google stays proposed. The diagram node, the section text, the DECISIONS row and the continuation entry all use this wording.

## Checks

- **Mermaid:** all three diagrams in `architecture-map.md` parse and render with mermaid 10.9.1. The rendered server SVG contains every new node and edge label. A visual check page, outside the repository, renders all three diagrams: `/private/tmp/claude-501/-Users-kornelispoort-Documents-Codex-2026-09-17-i-w-work-bardbox-slack-bot/af9e9a17-9f20-4ce0-9119-f53f69d29f2b/scratchpad/bardbox-access-control-mermaid/index.html`. Serve that folder over loopback HTTP and open it; it loads mermaid 10.9.1 from jsDelivr.
- **Fences:** balanced (6 code fences).
- **Links and anchors:** local links and `#` anchors in the four changed files resolve, including `network-access.md#optional-authenticated-campus-dashboards` and `architecture-map.md#server-data-inventory-and-module-operations`.
- **Whitespace:** `git diff --check` is clean.
- **Runtime tests:** none, because no code changed.

## Limits

- **Conceptual only:** this is a conceptual direction. No role matrix, admin scope, session store, provider, API or enforcement behaviour is selected or implemented.
- **Deployed access:** RKC and CESH access is unchanged.
- **Review status:** the Access Control wording is not yet independently reviewed.

## Next step and owner

1. **Codex** reviews the PR at its exact head and writes `coordination/CODEX-REVIEW.md`. Corrections go on this branch.
2. **Kornelis** decides on merging.
