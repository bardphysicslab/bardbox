# BardBox Change Skill

**Version:** 0.1  
**Purpose:** A reusable working playbook for making non-trivial changes to BardBox projects without losing platform consistency, documentation, testing, or maintainability.

## Core principle

Treat every BardBox project as an instance of a larger platform, not as an isolated codebase.

For any material change, determine:

1. Does the proposed change fit the BardBox architecture and design philosophy?
2. Is it project-specific, an optional reusable BardBox capability, or a BardBox-wide standard?
3. What else is affected by the change?
4. What needs to be tested, documented, propagated, deployed, or recorded?
5. What credible blind spots might have been missed?

The agent should do this analysis automatically. The user should not have to remember to ask for it.

## Decision model

For material decisions:

**Agent flags → explains → recommends → user decides → decision is recorded.**

When flagging a decision, provide enough information to make the decision:

- What was found
- Why it matters
- Reasonable options
- Pros and cons
- Expected effort or scope
- Recommended approach
- Consequences of doing it now versus later

Do not create unnecessary decision points for trivial or routine changes.

## 1. Start with a BardBox baseline check

Before implementing a non-trivial change, check the project against the current BardBox standards.

Look for missing or outdated required elements, including:

- Project identity and configuration
- Architecture/system documentation
- User documentation
- Developer/maintenance documentation
- Data-processing and derived-metric documentation where applicable
- Tests appropriate to the project
- Decision records
- Applicable shared BardBox conventions, protocols, and capabilities

If a missing baseline item is a small, safe documentation or housekeeping fix, fix it as part of the work.

If bringing the project to baseline requires meaningful refactoring, architectural work, significant scope expansion, or more than a quick incidental fix, flag it instead. Explain the issue, estimate the effort, give pros and cons, and recommend **fix now** or **backlog**.

Do not silently turn a small requested change into a major cleanup project.

## 2. Classify the scope of the change

Classify each material new capability or behavior as one of:

### Project-specific
The feature exists because of the particular scientific, hardware, deployment, or operational requirements of one BardBox instance.

Example: a CESH-specific dual-PM confidence algorithm.

Keep it in that project unless a genuinely reusable abstraction emerges.

### Optional BardBox capability
The feature is broadly useful to multiple BardBox projects but is not required by every project.

Example: OTA firmware updating.

Projects should consume only the capabilities they actually use. Do not add unused modules merely for consistency.

Reusable capabilities should have a clear source of truth rather than being casually copied between repositories. Projects may deliberately use different versions when necessary, but that choice must be visible and documented.

### BardBox standard
The behavior or contract is foundational enough that BardBox projects should normally follow it.

Examples may include identity conventions, protocol behavior, health reporting, buffering contracts, or required project documentation.

The agent makes the initial classification and explains it when the classification has architectural consequences. The user may override it.

## 3. Check platform propagation

When a project introduces or changes something that appears reusable, explicitly ask:

- Should the BardBox platform rules/specification change?
- Should the BardBox project template change?
- Is a shared module, contract, schema, tool, or reusable implementation needed?
- Which existing BardBox projects consume this capability?
- Could those projects be affected by this change?
- Are migration tasks needed?

Do not assume that every affected repository must immediately change.

For each consumer, determine whether the changed behavior or failure mode actually applies. If not, document the reason when useful.

If applying the change elsewhere would require substantial refactoring or carries meaningful risk, flag it for discussion rather than automatically expanding scope.

A fix to a shared capability should trigger a check of all known consumers.

## 4. Documentation impact check — required

Every material change must explicitly check documentation impact, even when the result is **no documentation change required**.

Each BardBox project should work toward maintaining:

### User manual
How to operate and understand the system.

Include plain-language explanations of important derived values and behavior.

### System architecture and data-flow documentation
Show the major hardware/software components and how information, commands, storage, and external services move through the system.

Keep diagrams synchronized with actual implementation.

### Developer setup and maintenance guide
How to build, configure, test, deploy, troubleshoot, and maintain the project.

### Data processing and derived metrics
Document important transformations, formulas, thresholds, corrections, confidence calculations, averaging, filtering, calibration, and other derived values.

The technical documentation should state the actual mathematical method where appropriate. User-facing documentation should provide a comprehensible explanation.

**Formula, implementation, and tests must agree.**

### Decision log
Record meaningful architectural or technical decisions, particularly when alternatives were considered.

A decision record should briefly capture:

- What was decided
- Why
- Important alternatives considered
- Consequences or constraints created by the decision

### BardBox platform documentation
Maintain the higher-level documentation describing BardBox itself, its standards, optional capabilities, architecture, and project expectations.

When a required document does not yet exist, create it during the next relevant change if doing so is a small, safe addition. If creating it is substantial work, flag it and propose a plan.

Documentation is part of completing the change, not cleanup to be deferred automatically.

## 5. Test the change — and test the tests

Do not equate **existing tests pass** with **the change is adequately tested**.

For material changes:

1. Run the relevant existing tests.
2. Identify assumptions changed by the new behavior.
3. Look for credible testing blind spots introduced or exposed by the change.
4. Recommend additional tests where warranted.
5. Explain why each proposed test matters.

The goal is not to enumerate every imaginable failure. Focus on realistic failure modes, boundary conditions, interactions, regressions, hardware behavior, data integrity, timing, networking, recovery, and operational conditions relevant to the change.

When a possible test is expensive, difficult, destructive, or unlikely to represent a real condition, flag it for the user's decision rather than automatically performing it.

## 6. Blind-spot scan

For any change that can plausibly break something, perform a concise blind-spot scan.

Consider, where relevant:

- Architecture
- Cross-repository effects
- Backward compatibility
- Hardware compatibility
- Data integrity and historical data
- Timing/concurrency
- Buffering and recovery
- Networking and offline behavior
- Security
- Configuration
- Deployment
- Rollback
- Monitoring/observability
- User workflow
- Maintenance
- Testing gaps
- Documentation drift
- Versioning/migration
- Failure and recovery states

Do not manufacture concerns merely to fill a checklist. Surface credible risks the user may not have considered and prioritize them.

Skip the formal blind-spot scan for genuinely trivial changes that cannot reasonably break behavior.

## 7. Deployment and rollback

For material deployable changes, consider:

- Whether staged rollout is appropriate
- What should be validated before wider deployment
- How to detect failure
- Whether a rollback path exists
- What the known-good state is
- Whether configuration/data migrations are reversible
- Whether field hardware could become inaccessible

The agent proposes the deployment and rollback approach. The user signs off when the risk is meaningful.

Do not deploy broadly merely because tests are green.

## 8. Shared capability drift

When changing a capability that is shared or intended to be reusable:

- Identify known consumers.
- Check whether the fix or change applies to them.
- Avoid independent copies that can silently drift when a shared implementation or contract is more appropriate.
- Track deliberate version differences.
- Flag security, reliability, protocol, or compatibility fixes that may require migration elsewhere.
- Create or recommend migration/backlog work where immediate propagation is inappropriate.

Project-specific customization may live in the project repository, but it should not silently redefine the shared capability.

## 9. Skill/governance synchronization

The reusable BardBox AI skill/playbook and the canonical BardBox GitHub standards must not silently drift apart.

Whenever a BardBox skill is added or materially changed:

- Evaluate whether the change establishes or modifies a BardBox engineering rule, workflow, documentation requirement, architectural principle, or governance expectation.
- If it does, update the canonical `bardbox` standards/specification repository as part of the same work.
- If the rule changes the expected starting state or reference implementation for projects, also update `bardbox-project-template`.
- If it is purely an AI interaction/workflow instruction and does not change BardBox engineering standards, no platform/template change is required, but make that determination explicitly.

Likewise, when the canonical BardBox standards change, check whether the reusable AI skill needs to be updated so that future agents enforce the new standard.

**The skill is an enforcement/playbook layer; GitHub remains the canonical technical source of truth.**

## 10. Completion check

Before considering a material BardBox change complete, report concisely:

- **Implementation:** what changed
- **Scope:** project-specific / optional BardBox capability / BardBox standard
- **Platform impact:** BardBox rules/template/shared components affected or not
- **Tests:** what ran and what new coverage was added
- **Testing blind spots:** credible remaining gaps
- **Documentation:** what was updated or confirmed unaffected
- **Decisions:** important decisions recorded
- **Deployment:** rollout/validation status
- **Rollback:** available path, if applicable
- **Cross-project impact:** consumers checked and any follow-up tasks
- **Skill synchronization:** whether the reusable BardBox skill and canonical GitHub standards remain aligned
- **Remaining risks or backlog:** anything intentionally deferred

Do not claim completion when required work remains unacknowledged.

## Working style

Keep the process proportional to the change.

For a trivial change, stay lightweight.

For a consequential change, think like a systems engineer: trace the effect through architecture, implementation, tests, documentation, deployment, and future maintenance.

Prefer deterministic rules, explicit contracts, and testable behavior over relying on an agent to remember conventions.

The purpose of this skill is not bureaucracy. It is to let the user state the engineering goal once while the agent reliably remembers the surrounding BardBox responsibilities.
