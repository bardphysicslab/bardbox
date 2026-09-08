# BardBox Promotion Governance

Standards are maintained in `bardbox` and demonstrated in
`bardbox-project-template`. Production repositories validate improvements in
real deployments; they are not permanent forks of shared infrastructure.

> When a reusable infrastructure, tooling, runtime, protocol, data, testing, or UI improvement is proven anywhere in the BardBox ecosystem, the work is not considered complete until it has been evaluated against the other active BardBox implementations for promotion into the canonical BardBox standard, shared tooling/library, and project template where appropriate.

Promotion is a **cross-repository comparison**, not a rule that one production
repository becomes the reference for every concern. Different projects may
contain the strongest proven implementation of different concerns. For example,
one project may supply the best backup behavior while another supplies the best
state-machine, testing, driver, deployment, or concurrency pattern.

Every reusable finding should be classified deliberately as one of:

1. **Canonical BardBox standard** — a behavior or contract relevant projects
   should follow.
2. **Shared BardBox implementation** — reusable executable logic that should
   exist once in a central package/library, such as `bardbox-tools`.
3. **Project-template material** — scaffolding/examples showing how a project
   consumes the current standard and shared implementation.
4. **Project-specific behavior** — logic that remains intentionally local to
   the deployment.

Evaluation does not require promotion when behavior is project-specific,
security-sensitive outside its original scope, not yet proven, or would create
more coupling than value. The decision and reason should still be recorded.

Reusable executable logic should not be maintained as independent copied
versions once a stable shared implementation exists. During migration, thin
compatibility wrappers are acceptable when they call the shared implementation
without re-implementing its logic.

This rule applies to application code and to local/operations tooling, including
Python helpers, shell helpers, config migration, Git/audit utilities, deployment
inspection, backup verification, protocol checks, data-query helpers, CLI tools,
and MCP-facing tools. CLI and MCP surfaces should call the same deterministic
core implementation wherever practical.

When an operational standard depends on reusable deployment or configuration-
migration tooling, promote the tooling with the standard so the project
template demonstrates the required workflow rather than documenting it alone.

For the current ecosystem-wide comparison and migration priorities, see
`docs/cross-repo-platform-audit-2026-09-08.md`.
