# BardBox Project Manifest

BardBox project repositories may declare their platform-facing structure in a root-level `bardbox.toml` file.

The manifest is intentionally small. Its purpose is to let contributors, CI, and `bardbox-tools` discover the important project contracts without guessing repository layout.

## Minimal manifest

```toml
project = "solar-monitor"
project_type = "monitor"
bardbox_protocol = "0.3"

[tests]
command = "pytest"
```

## Common fields

### Root fields

- `project` — canonical project/repository identifier.
- `project_type` — broad BardBox project class such as `monitor`, `instrumentation`, `tooling`, or `template`.
- `bardbox_protocol` — BardBox protocol/specification version the project is approved against.

### Configuration

Projects with runtime/example configuration may declare paths:

```toml
[config]
runtime = "raspi/config/app_config.json"
example = "raspi/config/app_config.example.json"
```

These paths are repository-relative. Runtime configuration may be absent from Git when it contains deployment-specific values; the manifest still records its expected location.

### Tests

```toml
[tests]
command = "pytest"
```

`command` is the canonical project verification command intended for contributors and CI. It should be deterministic and non-destructive.

### Deployment

Projects with a deployed service may declare its expected identity:

```toml
[deployment]
service = "solar-monitor.service"
```

The presence of a deployment section does not authorize tooling or AI agents to restart, modify, or deploy the service.

## Example

```toml
project = "solar-monitor"
project_type = "monitor"
bardbox_protocol = "0.3"

[config]
runtime = "raspi/config/app_config.json"
example = "raspi/config/app_config.example.json"

[tests]
command = "pytest"

[deployment]
service = "solar-monitor.service"
```

## Validation rules

The initial `bardbox-tools` implementation should treat these as errors:

- missing `project`;
- missing `project_type`;
- missing `bardbox_protocol`;
- malformed TOML;
- declared repository-relative paths that escape the repository root.

Optional sections may be omitted when they do not apply.

Tools should report unknown fields rather than silently interpreting them as platform standards. During early development, unknown fields may be warnings rather than hard failures so the schema can evolve deliberately.

## Relationship to BardBox standards

`bardbox.toml` does not replace BardBox protocols, ADRs, `AGENTS.md`, or detailed standards. It is a machine-readable pointer that tells tooling which standards and project resources apply.

A project manifest must not redefine BardBox-wide protocol behavior. If a project requires behavior that conflicts with BardBox standards, follow the governance/conflict process in `AGENTS.md` rather than encoding a private exception in the manifest.

## Intended tooling

The manifest will be consumed by commands such as:

```text
bardbox doctor
bardbox audit
bardbox config-check
```

It will also provide structured project metadata for CI and the BardBox MCP interface.
