# BardBox Agent Instructions

The BardBox change workflow is in `docs/ai/bardbox-change-skill.md`, and
repository working rules are in `docs/gpt-instructions.md`; both still apply.
This file adds two practices for refactors and architectural assessments, in
this repository and in BardBox projects that link here.

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
