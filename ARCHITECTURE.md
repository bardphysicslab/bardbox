# BardBox Architecture

This is the architectural entry point for BardBox. `AGENTS.md` defines how to
make changes. Topic-specific standards below define technical contracts; they
are not parallel general-purpose checklists. The former BardBox Change Skill
is consolidated into these two root documents.

## Ownership and project composition

`bardbox` owns shared standards and specifications. `bardbox-project-template`
is the reference implementation and project starting point. Project repositories
own their scientific/hardware configuration, application coordination, and
project-specific behavior. Shared implementation belongs in a maintained
component with a documented source and version, consumed through its interface.
A template is not permission to create permanent independent copies of shared
behavior. Promotion evaluates standards, shared code, and template integration;
consumer adoption can be staged.

Classify material behavior as:

- **Project-specific:** scientific or operational behavior particular to a
  project, such as a CESH dual-PM confidence algorithm. Keep it there unless a
  concrete reusable boundary emerges.
- **Optional capability:** reusable behavior such as OTA updates. Only projects
  that need it consume it; projects may deliberately use documented versions.
- **BardBox standard:** foundational contracts such as identity, reading format,
  health, applicable transport behavior, and platform requirements.

## Independently reusable capabilities

Kornelis calls these application capabilities “skills.” They are distinct from
coding-agent instruction skills. Each owns cohesive behavior and a public
interface defining relevant commands/operations, data, status, errors,
permissions, configuration, compatibility, and lifecycle/recovery expectations.

A capability must be usable and testable outside its original application
without copying implementation code or importing that application's
orchestration, UI, globals, credentials, or deployment assumptions. Projects
supply explicit configuration and integration. Demonstrate reuse with a minimal
independent consumer and controlled-dependency tests, without requiring another
production deployment.

Choose the smallest suitable form: application/service, package, firmware
library, or UI template. Separate repositories, containers, and network APIs
are decisions to justify, not universal requirements. Reuse does not require a
shared running instance: projects may have separate data, credentials, and
deployments. Consider existing tools before building new ones.

Dependencies flow from project composition to capability interfaces. Composition
selects concrete providers; shared behavior does not depend on the parent
project. Each capability enforces its own rules and permission boundary.
Applications coordinate intent and review; deterministic code owns validation,
authorization, consequential state transitions, and safety. Provider-specific
implementation stays behind the relevant interface.

## Firmware, backend, and tooling boundaries

Devices acquire measurements. Drivers translate transport/vendor details into
normalized readings. The backend owns application policy, freshness, durable
records, APIs, and coordination. Application session state belongs to the
application layer even where an existing implementation keeps it in `main`;
entry points should evolve toward assembly rather than accumulating policy.
Safety and recovery remain with the responsible runtime component, not a browser.

For network-pushing nodes, acquisition, persistent delivery queues, and upload
remain independent. Transport failure must not stop sampling or silently discard
unacknowledged records. Recovery is bounded, observable, and limited to what the
actual hardware supports. Node delivery storage is not backend historical logging.

Intended reusable boundaries include:

| Capability | Owned behavior | Project supplies |
| --- | --- | --- |
| USB flashing | Discovery, flashing, progress, verification, structured failure handling | Supported target, image, connection/configuration, authorization |
| OTA updates | Update lifecycle, compatibility checks, interruption handling and documented recovery | Device/image compatibility, delivery configuration, rollout policy |
| Wi-Fi firmware library | Connection behavior, bounded recovery, connectivity diagnostics | Credentials through protected configuration and project network policy |
| Serial diagnostics | Logging/diagnostic interface and configurable verbosity without corrupting protocol traffic | Project diagnostic fields and selected output/configuration |

Wi-Fi should have a documented library inclusion/configuration experience
analogous to including `wifi.h`. These are intended boundaries, not claims that
all four already exist as independently distributable components. OTA success
must distinguish transfer, installation, and healthy running firmware. Preserve
firmware/protocol version distinctions and existing command/payload contracts.

## Default UI templates

The shared template owns device/project identity, health, sensor QA, navigation,
and consistent styling. A defined readings extension point accepts project data
and presentation choices. RKC uses compact door-state/temperature readings;
CESH uses expandable sections per sensor. Projects select/configure a template
or extend supported slots/variants instead of copying the whole screen.

Document template inputs, extension points, supported versions, and compatibility.
Test representative RKC and CESH configurations when shared changes affect them.
Shared improvements must remain reusable while preserving project presentation.
Critical health/alarm status remains visible; stale data must never appear live.
`docs/web-ui-standard.md` supplies the detailed web visual requirements.

## Current versus intended structure

The repository already documents shared protocol, normalization, driver, UI,
transport-recovery, and operational contracts. Existing guidance also describes
copying/synchronizing reference implementations into projects. The intended
architecture is maintained shared capabilities and configurable templates with
independent-consumer evidence; internal modularity alone is insufficient.

This documentation consolidation does not establish conformance of RKC, CESH,
the project template, or shared tooling, and does not create new runtime
components. Check each authoritative implementation before planning an
extraction. Record gaps separately and improve one bounded capability at a time;
do not make active project deadlines depend on an unrelated broad migration.

## Detailed standards: read those applicable to the task

| Area | Canonical documents |
| --- | --- |
| Device/firmware contracts | [Device instructions](docs/device-instructions.md), [Web Nodes](docs/web-node-protocol.md), [transport recovery](docs/transport-recovery-standard.md) |
| Drivers and readings | [Pi drivers](docs/pi-driver-instructions.md), [reading format](docs/reading-format.md), [channels](docs/channel-names.md) |
| Identity and time | [Node naming](docs/node-naming-standard.md), [time synchronization](docs/time-sync-standard.md), [sessions](docs/session-model.md) |
| Web presentation | [Web UI standard](docs/web-ui-standard.md) |
| Verification | [Testing guide](docs/testing-guide.md) |
| Configuration and operation | [Config/report workflow](docs/config-report-workflow.md), [service operations](docs/service-operations-standard.md), [network access](docs/network-access.md) |
| Historical-data access | [Data API/MCP boundary](docs/data-api-mcp-boundary.md) |
| Promotion | [Promotion governance](docs/promotion-governance.md) |

Preserve the authenticated read-only historical-data boundary, separate
configuration/control paths, internal network restrictions, deployment-specific
configuration, verified backup/retention, and all existing operational approval
requirements. Shared reuse does not authorize cross-environment access or a
source-of-truth change. Detailed technical gaps require resolution before work
that depends on them; this consolidation does not invent missing schemas.

## Decision: consolidate guidance without merging every technical standard

The former change skill and GPT summary both directed agent behavior, while
architecture reasoning lived separately without root entry points. Requiring
all three made it harder to identify the current working rules. The chosen
structure puts change discipline in `AGENTS.md`, architecture in this file,
and protocol/operational details in the existing task-specific standards.

An alternative was one large file containing all rules and technical contracts.
That reduces navigation but makes a small task carry unrelated specifications
and increases duplicated text. Two entry points with a targeted reference index
fit the current multi-project platform. Reconsider if the index itself becomes
ambiguous or maintaining links proves harder than maintaining the documents.
The old agent/principle paths remain redirects so existing references still work.

This is the course's evidence-and-tradeoff approach applied to documentation;
it does not claim that moving prose has removed runtime coupling.

## Design reasoning

The following existing principles, including the local small-pilot addition,
are preserved here from `docs/architecture-principles.md`. They are design
heuristics; the explicit ownership and reuse requirements above reflect the
confirmed direction. They do not require retroactive broad refactoring.

## 1. Put knowledge in the right place

Good architecture is largely about deciding which component should know what.

For every component, ask both:

- What is the minimum this component needs to know to do its job?
- What should this component explicitly *not* know?

Keeping unnecessary knowledge out of a component reduces coupling and makes failures, testing, replacement, and maintenance easier to reason about.

## 2. Give components clear, narrow responsibilities

Sampling, communication, storage, alarm policy, notification delivery, UI rendering, and other concerns should not become one tangled responsibility.

Example: a sensor sampler should collect readings and make them available. It should not need to know whether Wi-Fi is connected, whether the server is healthy, or whether an SMS provider is available.

A communication component can independently decide whether a reading can be sent upstream or must be buffered. Thus sampling can continue even while communications are degraded.

This principle applies at several scales: functions, modules, drivers, services, and state machines.

Each piece of authoritative state has a named owning component that performs its mutations and enforces its invariants; other components read it or request changes through that owner.

## 3. Prefer independent state machines for independent concerns

Do not force unrelated concerns into one large state machine simply because they occur in the same product.

Example: sampling state and communications state can evolve independently. Loss of Wi-Fi should not imply that sampling has stopped.

Also distinguish **state** from **context/input**. For example, in a freezer alarm system, door-open status may be useful context explaining a temperature excursion without necessarily being an alarm state itself.

A simple temperature alarm model might be:

1. Normal — temperature is within bounds.
2. Pre-alarm — temperature is outside bounds and the grace timer is running.
3. Alarm — temperature has remained outside bounds longer than the configured interval.

Door state can accompany those states as context rather than unnecessarily multiplying the number of states.

## 4. Interfaces are contracts

Components should communicate through explicit, predictable interfaces. An interface states what a component promises to accept or provide without requiring its consumer to understand its internal implementation.

APIs and BardBox driver boundaries are examples of this principle.

External services should sit behind BardBox-owned interfaces where practical. For example, alarm policy should not be written in terms of Twilio. BardBox can define a notification/SMS interface and implement Twilio as one provider. Replacing Twilio should then require changing the provider implementation rather than the alarm system.

## 5. External providers execute; BardBox owns policy

Sensor nodes report facts. BardBox application logic interprets those facts and decides what actions are required. External providers execute narrowly defined actions.

For example:

- node: reports temperature and door state;
- application/alarm logic: determines whether an alarm condition exists and what notifications are required;
- notification provider: delivers an SMS or email.

An outage of one external provider should not unnecessarily stop data collection, storage, dashboards, backups, or unrelated notification channels. The system should expose a degraded condition rather than collapse as a whole.

## 6. Safety-critical behavior must not depend on the UI

The web UI should generally be a view/control surface, not the owner of operational safety.

For example, a LabCheck test runner should own the test sequence and safe-state behavior. A browser crash must not leave a power supply, load, or other instrument indefinitely in a potentially unsafe test condition.

Whether a test continues or aborts after UI loss is a test-policy decision, but either behavior must be implemented safely by the runner rather than accidentally determined by the browser's survival.

## 7. `main` should assemble and start, not become the brain

The program entry point should be intentionally boring. Its primary job is composition: load configuration, instantiate/select components, wire dependencies together, and start the application/runtime.

It should not accumulate device-specific logic, alarm policy, UI layout, or other business rules.

A useful warning sign is a `main` file filled with application-specific conditional logic.

The application layer may coordinate components, but `main` should normally call into that layer rather than *be* that layer.

## 8. Ask: can this be described instead of programmed?

If a difference between deployments can be expressed as data, strongly consider configuration rather than application-specific code.

Examples include device identity, sensor inventory, labels, locations, thresholds, ranges, and other deployment-specific choices.

This is a heuristic, not a rule that all behavior belongs in configuration. Configuration should describe the system; code should implement behavior and enforce contracts.

## 9. Shared UI belongs to BardBox; applications provide content

BardBox should move toward a shared UI/design system rather than each application independently recreating its dashboard.

Shared platform concerns can include:

- Bard branding and common header structure;
- typography and spacing;
- standard card sizing/layout rules;
- common identity, health, and hardware sections;
- common status/alarm presentation;
- reusable graph and card components.

Individual applications such as RKC or CESH should primarily provide their unique configuration, capabilities, data, and application-specific content.

Where practical, configuration should describe the monitored system and the shared UI framework should render standard structures from that description. A change to a shared BardBox component should then propagate consistently rather than require edits in every application.

## 10. Design for replacement and partial failure

A healthy architecture assumes components will change and fail.

Ask during design:

- If this provider disappears next year, what must change?
- If this component crashes, what should continue working?
- Can one subsystem enter a degraded state without taking unrelated subsystems down?
- Does the component responsible for an operation also own its cleanup/safe-state behavior?

The goal is not zero failure. The goal is understandable, bounded failure and straightforward replacement.

## 11. Promote proven ideas into standards deliberately

These design heuristics capture how we reason while developing BardBox. They are distinct from the explicit requirements elsewhere in this document and the detailed standards.

When a principle becomes sufficiently mature and specific, translate it into the appropriate BardBox standard, protocol, template requirement, tooling check, or implementation guide. This keeps exploratory architectural thinking separate from rules that every BardBox project is required to follow.

## 12. Start with the smallest useful pilot

Use a startup MVP approach when developing new BardBox capabilities. Build the smallest safe end-to-end workflow that a real user can try, make its behavior observable, and learn from the pilot before expanding it.

Do not add speculative features, optimize paths that have not shown a real problem, or create abstractions solely for imagined future use. Keep boundaries and safeguards that address concrete current needs such as hardware safety, data integrity, permissions, provider replacement, failure isolation, and reversible migration. Let observed use and user feedback determine the next refinement.
