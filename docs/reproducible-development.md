# Reproducible development and Linux validation

BardBox software must be testable without borrowing another repository's Python
environment or depending on a developer's personal machine configuration.
Containers support development and testing. They do not change the native/systemd
production model of Pi services or how firmware is built and flashed onto nodes.

## Applicability

- Python/server repositories and reusable Python tooling declare a supported
  Python version, their runtime/test dependencies, and an isolated test command.
  Provide a Dev Container and clean Linux validation when portable software is
  maintained or shared from the repository.
- Firmware-only repositories declare their PlatformIO board/environment and build
  procedure. Add a container only when it improves a supported build/test path;
  USB flashing and attached-sensor tests remain separate hardware checks.
- Documentation-only repositories need no artificial Python application or Docker
  image. Explain any executable document-generation or validation dependencies.
- Existing consumers may adopt in stages. Record the current gap and follow-up;
  do not imply their production runtime must be migrated into Docker.

## Repository-owned environment

Keep runtime and test dependencies explicit. A local virtual environment belongs
to one repository and is excluded from version control. Use the same supported
Python minor version and test dependency input in local instructions, Dev Container
setup and CI. Hardware-specific optional dependencies must not be silently required
for portable fixture tests.

A version range or moving image tag is repeatable setup, not an immutable release.
For a validation record, capture the commit, interpreter version, resolved package
versions, image digest, platform/architecture and exact command. Pin or lock inputs
when reproducing a release or investigating dependency drift. Deliberate updates
need fresh validation rather than claiming an older result covers them.

## Clean Linux validation

Run tests from a fresh container against an identified source revision. Do not
mount a host `.venv`, dependency cache, SSH credentials, Docker socket or hardware
by default. Prefer a tracked source archive copied into temporary container storage.
A writable developer checkout in an interactive Dev Container is convenient, but
is not evidence of a clean checkout test. Report separately if testing includes
uncommitted or untracked changes.

Build using the smallest needed context; keep credentials and private configuration
out of build contexts and image layers. Dependency installation can use the network;
tests should use fixtures where possible. A container run must not contact production
nodes/services unless that integration test was explicitly selected and authorized.
Remove temporary containers on exit. Do not prune unrelated images or volumes.

## CI and local parity

CI and the documented container command use the same test dependency manifest and
test selection. Platform-specific differences must be declared. A reusable template
change needs isolated local tests and clean Linux validation before being described
as portable. A CI badge or host-only pass is not a hardware validation result.

Record test counts and failures honestly. A failure caused by a missing declared
dependency is a repository defect; installing it only in a personal environment
does not fix portability. Keep physical sensor, offline queue, OTA rollback and
production configuration checks as additional gates where those behaviors apply.

## Adoption and audit

The project template's `chatgpt/shared-tooling-foundation` branch is the initial
reference implementation. Promote through review; do not silently merge it or copy
unrelated template application code into consumers. Known Python consumers include
BardBox Tools, CESH and RKC; each needs its own dependency and test-path assessment.

A future audit declaration should identify Python version, dependency input and
validation entrypoint. Static checks can verify files/declared alignment, but must
not claim that Docker ran, that tests passed, or that the production host matches.
Keep audit execution read-only unless the operator explicitly invokes validation.
