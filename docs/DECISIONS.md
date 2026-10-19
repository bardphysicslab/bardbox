# BardBox decision index

Shared platform architecture and contracts live in BardBox. Existing issue
threads remain the authoritative discussion, including historical design threads
in the project-template repository. Do not move or duplicate their full reasoning.
Decision status is separate from implementation or deployed conformance.

| ID | Accepted choice | Decision status | Reasoning / acceptance | Design and adoption |
| --- | --- | --- | --- | --- |
| BB-001 | Validate channels independently, retaining healthy values when another channel fails; preserve unknown measurement time | Accepted target contract | [Ingestion discussion](https://github.com/bardphysicslab/bardbox-project-template/issues/15); [timestamp decision](https://github.com/bardphysicslab/bardbox-project-template/issues/15#issuecomment-6225994960); [reviewed contract merge](https://github.com/bardphysicslab/bardbox/pull/39) | [Ingestion contract](ingestion-contract.md); template implementation is future work under [implementation issue](https://github.com/bardphysicslab/bardbox-project-template/issues/16), not deployed behavior |
| BB-002 | Report ingestion errors through shared central diagnostics independently of rendering; pure validator returns faults and its caller logs them | Accepted target contract | [Dated discussion](https://github.com/bardphysicslab/bardbox-project-template/issues/15#issuecomment-6243326846); [contract merge](https://github.com/bardphysicslab/bardbox/pull/46); [table review/merge](https://github.com/bardphysicslab/bardbox/pull/47) | [Diagnostic contract](ingestion-contract.md#diagnostic-logging-independent-of-rendering), [server map](architecture-map.md#project-server-template); runtime implementation not claimed; duplicate reduction deferred |
| BB-003 | October 19 platform direction: minimum instance with required Registry and Processing; metric/UTC with labelled display; entity identity distinct from hardware; module-owned configuration; firmware recording ON with saturation anchor; server history ON and Drive backup OFF by default; central-log-only loss reporting; read-only partner pull; entity-led UI with standard status meanings | Accepted direction (dated decision) | [Dated decision entry](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991); supplements: [UI clarification](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269649488), [buffer estimates](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269868018), [UI amendment](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270151957), [card refinement](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270321987), [active-alarm outline](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270510607), [alarm switch](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6270769043) | [ARCHITECTURE.md](../ARCHITECTURE.md#accepted-platform-direction-october-19-2026), [Architecture Map](architecture-map.md); documentation reconciliation only; no runtime implementation, adoption or deployment |

These IDs are assigned for discoverability now, not represented as identifiers
used in the earlier conversations. They index only verified recent decisions,
not a complete historical inventory. New or superseding decisions follow the
[shared workflow](https://github.com/bardphysicslab/engineering-standards/blob/main/development-workflow.md#idea-to-accepted-work)
and link a dated accepted issue entry. Remaining unverified historical rationale
is a gap, not reconstructed approval. Shared engineering process decisions remain
in the [engineering index](https://github.com/bardphysicslab/engineering-standards/blob/main/docs/DECISIONS.md).
