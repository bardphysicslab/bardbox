# BardBox Agent Instructions

This is the canonical working guide for BardBox changes. It incorporates the
former `BARDBOX_CHANGE_SKILL.md` (v0.1); that separate checklist is no longer
required. `ARCHITECTURE.md` owns architectural direction. Detailed standards
remain authoritative for their subjects and are read when the task touches them.

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

Use **Design → Decompose → Define done → Generate → Verify → Commit** for
meaningful new work. Keep changes small enough for human review, with durable
notes and verified recovery checkpoints. Course reference:
[CMU Agentic Software Development](https://github.com/CMU-17-214/f2026).
Consult relevant material before attributing a rule to it; the course is a
learning reference, not an additional mandatory rulebook.

Apply the course to proposed updates, rather than citing it decoratively:

- Before an architecture recommendation, map the current data, operations, and
  dependencies; trace a representative request to where its invariant is enforced.
- Locate each proposed correction in actual files and explain a concrete failure
  or costly change. For material boundary decisions, compare two plausible
  decompositions, their costs, and the condition that would change the choice.
- Specify preserved invariants and externally observable behavior before a
  refactor. Distinguish additive contract evolution from breaking changes and
  state the compatibility/deprecation path.
- Keep a concise evidence/decision record so later agents can compare intended
  design with reality, without inventing another general-purpose rulebook.

Sources consulted for this consolidation (2026-09-25): course
[learning goals](https://github.com/CMU-17-214/f2026/blob/main/learninggoals.md)
and [Lab 3: Find the Design Gap](https://github.com/CMU-17-214/f2026/blob/main/labs/lab03.md).
These rules are our application of that material; classroom submission and
transcript-publication requirements do not become BardBox requirements.

For material decisions: flag the issue, explain evidence and consequences,
compare reasonable options and effort, recommend an approach, obtain the
maintainer's decision where needed, and record it. Existing task authorization
covers routine choices; do not ask again for already authorized work.

Existing systems with deadlines improve incrementally. Record deferred
architecture or verification debt and follow-up triggers. Do not make an
unrelated refactor a release prerequisite or waive safety/data-integrity checks
because of a deadline. Repeated failed fixes are a reason to reassess scope and
the recovery checkpoint, not to continue generating ever-larger changes.

## Verification and documentation

- Run relevant existing tests; identify changed assumptions and credible gaps in
  the tests themselves. Recommend additional checks with their purpose. Verify
  actual behavior and review the diff, including unexpected files and weakened
  tests. Green tests or an agent summary alone are insufficient evidence.
- Cover relevant failures, boundaries, interactions, hardware limits, data
  integrity, timing, offline operation, recovery, permissions, and compatibility.
  Use controlled dependencies for component tests. Distinguish local, simulated,
  hardware, and deployed evidence. Do not claim hooks enforce rules unless such
  checks actually exist.
- Perform a concise blind-spot scan for changes that can break behavior: include
  configuration, security, observability, maintenance, historical data,
  cross-project effects, versioning, migration, rollout, and recovery where
  relevant. Skip a formal scan for genuinely trivial changes.
- Flag expensive, destructive, or unusual tests for a scope/authorization
  decision; do not run them automatically. Broaden tests when a concrete risk
  warrants it, not as an unbounded ritual.
- Every material change checks documentation impact, including an explicit
  “no documentation change required” result when appropriate. Update affected
  user guidance, architecture/data flow, setup/maintenance instructions,
  derived-metric definitions, decision records, and platform standards.
  These are required topics, not a mandate for a separate file for each topic.
- Explain derived values plainly to users. Document mathematical methods and
  thresholds where relevant: formula, implementation, and tests must agree.
  Record meaningful decisions with their reason, alternatives, and consequences.

## Architectural self-check

Scale the check to the change: a sentence or two for a small, local fix; the
full list below for a multi-module refactor, a boundary or source-of-truth
change, or an explicit request to assess a design. When the task is an
assessment, report rather than implement. When implementation is already
authorized, the check informs that work; it is not an additional approval step.

1. Re-examine earlier decisions, including your own; prior authorship or
   approval is not evidence. Cite the files and functions involved.
2. Trace a normal path and a relevant failure path through the behavior being
   changed, including its most recent change.
3. Check against the project's `ARCHITECTURE.md` (or
   `docs/architecture-principles.md` where a project has none):
   - each module has a cohesive responsibility: related operations that change
     for the same reason;
   - each piece of authoritative state has a named owner that performs its
     mutations and enforces its invariants;
   - business rules are separate from UI, storage, network and hardware code;
   - controllability: a test can supply the inputs, initial state, time and
     dependency responses (including failures) the rule needs;
   - observability: a test can see the outcome (return value, state change,
     emitted event or recorded effect), including failures.
4. Name the boundaries worth keeping and, for each weakness, its practical
   consequence.
5. Recommend continue, small repair first, or clarify a requirement, and end
   with one bounded next step and the checks that show it is done.

## Refactoring with little test coverage

- Refactor in small steps that leave the application working. Where practical,
  keep structural changes (extract, move, rename, rewire) in separate commits
  from behavior or business-rule changes; when they must be combined, say so
  and name the behavior that changed.
- Before a structural step, pin the behavior it touches with the smallest useful
  check: a characterization test, or a written manual/bench scenario (setup,
  action, expected observation). A full suite is not a prerequisite.
- A characterization test records current behavior, not intended behavior. If
  current behavior looks wrong or conflicts with a requirement, label it and
  report it rather than changing it inside the refactor.
- Make a dependency explicit (a parameter, or an injected clock, transport or
  store) when a concrete test needs to control it. Do not add interfaces,
  frameworks or layers for flexibility nobody has asked for; a plain function or
  concrete class is often enough.

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

## Completion

Report proportionally: what changed; scope classification; standards/template/
shared-component impact; tests and new coverage; unverified behavior and testing
blind spots; documentation and decisions; deployment/validation and recovery
status; consumers checked; and remaining risks, deferred work, or migrations.
Do not call locally implemented or tested work deployed, and do not claim
completion while required work is unacknowledged.
