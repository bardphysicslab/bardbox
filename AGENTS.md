# BardBox Agent Instructions

This is the canonical working guide for BardBox changes. It incorporates the
former `docs/ai/bardbox-change-skill.md` (v0.1); that separate checklist is no longer
required. `ARCHITECTURE.md` owns architectural direction. Detailed standards
remain authoritative for their subjects and are read when the task touches them.

## Shared guidance

Before planning, proposing, reviewing, delegating or implementing changes,
read the shared guidance. Your tool does not load it automatically.

1. Resolve `main` once per task: `git fetch origin main`, then
   `git rev-parse origin/main`. If the fetch fails, use the existing
   `origin/main` and say it may be stale.
2. Read these files at that SHA with `git show <sha>:<path>`:
   - `docs/engineering/README.md`
   - `docs/engineering/development-workflow.md`
   - `docs/engineering/agent-practice.md`
   - `docs/engineering/checkouts-and-worktrees.md`
3. The guidance at that SHA governs the task, including a task that changes
   this file or `docs/engineering/`. If your working-tree `AGENTS.md` differs
   from `git show <sha>:AGENTS.md`, read that SHA's version too: it governs.
   Your branch's edits are proposals. Review them with
   `git diff <sha> -- AGENTS.md CLAUDE.md docs/engineering`; they take effect
   only after merge to `main`. If `docs/engineering/` does not exist at that
   SHA, that SHA's `AGENTS.md` is the complete governing guidance.
4. Record `Shared guidance: bardphysicslab/bardbox@<sha>` once in the task's
   durable evidence.

Copies (desktop files, chat project sources, memory) do not substitute for
the governing SHA. If a required file that exists at the resolved SHA cannot
be read, do read-only investigation only, and report it. Do not implement,
commit, push, deploy or end checkouts unless the maintainer explicitly says
to proceed without it.

## Before work

1. Identify the target repository, checkout, scope, and existing local changes.
   Read its root `AGENTS.md`, `ARCHITECTURE.md` when present, and all documents
   required for the task. For this standards repository, read `ARCHITECTURE.md`
   and `README.md`, then the relevant standards linked by the architecture.
2. If required guidance is missing, ambiguous, or contradictory, stop and ask
   rather than guessing. Explicitly authorized documentation repairs can resolve
   the identified gap; they do not authorize unrelated implementation work.
3. Inspect existing implementation and tests. For material work, define the
   intended behavior, component owner, allowed scope, acceptance evidence, and
   recovery checkpoint before generating code.
4. Check the relevant baseline: identity/configuration, architecture/data flow,
   user and maintenance guidance, derived metrics, tests, decision records, and
   applicable shared standards. Fix small, safe omissions within authorized
   scope; flag substantial gaps with impact, effort, and a fix-now/backlog
   recommendation. Do not turn a bounded task into a platform cleanup.

## Scope and reuse

- Classify material behavior as project-specific, an optional shared capability,
  or a BardBox standard using `ARCHITECTURE.md`. Explain consequential choices;
  the maintainer may override the classification.
- Look for an existing implementation before building one. Consume shared code
  through supported interfaces and explicit configuration. Do not copy capability
  implementations or import a parent application into a shared component.
- Define operations, data, status, errors, permissions, compatibility, and
  applicable recovery behavior. Demonstrate independent reuse with a minimal
  separate consumer and focused tests; interfaces alone do not prove reuse.
- Customize UI through the shared template's supported configuration/extension
  points. Avoid whole-screen forks; document a concrete incompatibility and
  obtain a scope decision before introducing an alternative shared structure.
- For shared changes, check every known consumer for applicability, including
  RKC and CESH when relevant. Evaluate effects on platform standards, the
  reference template, shared implementation, and migrations. Record deliberate
  version differences and reasons for deferral. Do not automatically change all
  consumers or add optional capabilities to projects that do not need them.
- Follow `docs/promotion-governance.md` when promoting proven infrastructure or
  UI. Security, reliability, protocol, and compatibility fixes require an
  explicit assessment of whether other consumers need migration.

## Decisions and proportional workflow

Moved unchanged to [`docs/engineering/agent-practice.md`](docs/engineering/agent-practice.md#decisions-and-proportional-workflow). It applies to BardBox changes; read it there.

## Verification and documentation

Moved unchanged to [`docs/engineering/agent-practice.md`](docs/engineering/agent-practice.md#verification-and-documentation). It applies to BardBox changes; read it there.

## Architectural self-check

Moved unchanged to [`docs/engineering/agent-practice.md`](docs/engineering/agent-practice.md#architectural-self-check). It applies to BardBox changes; read it there. This heading remains because other repositories refer to it.

## Refactoring with little test coverage

Moved unchanged to [`docs/engineering/agent-practice.md`](docs/engineering/agent-practice.md#refactoring-with-little-test-coverage). It applies to BardBox changes; read it there. This heading remains because other repositories refer to it.

## Operational boundaries

- Preserve existing identity, authorization, human review, audit, source-of-truth,
  environment-isolation, and deployment-approval requirements. A component must
  enforce its boundary; caller intent or model output is not permission.
- Keep DEV, TEST, and production data, credentials, targets, and state separate.
  Do not test against live systems, change authoritative external data, deploy,
  flash devices, restart services, or perform destructive actions without
  explicit authorization covering that action. Documentation changes grant none.
- Keep secrets and workstation-specific credentials/configuration out of source
  control and reports. Preserve historical data and configured authorities;
  migrations require reconciliation, validation, and a recovery plan.
- Before substantive configuration/deployment work, verify the applicable
  config/report tooling and follow `docs/config-report-workflow.md` and
  `docs/service-operations-standard.md`. Preserve deployment values; never
  replace live config wholesale with an example. Reports must redact secrets.
  Report upload is an external action and requires authorization.
- For deployable changes, document the known-good baseline, narrow rollout,
  validation/monitoring, failure detection, rollback/recovery, migration
  reversibility, and risk of inaccessible field hardware. Obtain required
  approval before deployment; passing tests is not deployment approval.
- Preserve UID, payload, command, and firmware/protocol compatibility by default.
  Firmware behavior changes require the project's firmware-version procedure;
  protocol versions change only when their contract changes.

## Git identity

Before creating/amending commits or pushing, verify `git remote -v`,
`git config --get user.name`, and `git config --get user.email`. Confirm the
`bardphysicslab` remote and approved Bard Physics author identity. If unexpected,
stop and correct repository-local configuration; do not change global identity.
SSH transport identity does not determine commit authorship. Never publish
personal account names, email addresses, SSH aliases, key filenames, or other
account-specific workstation details in this repository.

## Skill and governance synchronization

When an agent skill or playbook changes, assess whether it changes engineering
rules, architecture, documentation requirements, or governance. Keep those rules
aligned with this canonical repository; update the project template when its
starting state or reference implementation is affected. Pure interaction guidance
need not change platform standards; record that determination. Conversely, when
standards change, check affected skills for drift. Apply changes within the
authorized scope and report any remaining synchronization work. Written skills
are guidance, not mechanical enforcement.

## Completion

Report proportionally: what changed; scope classification; standards/template/
shared-component impact; tests and new coverage; unverified behavior and testing
blind spots; documentation and decisions; deployment/validation and recovery
status; skill/governance synchronization; consumers checked; and remaining risks, deferred work, or migrations.
Do not call locally implemented or tested work deployed, and do not claim
completion while required work is unacknowledged.
