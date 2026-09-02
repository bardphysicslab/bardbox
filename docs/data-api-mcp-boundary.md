# BardBox Data API and MCP Boundary

BardBox uses a central, read-only data-access boundary for historical measurement data. Individual monitor projects own acquisition and recording; downstream AI and tool clients should retrieve historical data through the standard BardBox Data API and the shared `bardbox-mcp` bridge rather than through direct machine access or project-specific MCP implementations.

## Responsibilities

### Monitor project repositories

Projects such as Solar Monitor, CESH Air, RKC Monitor, and GoLab are responsible for:

- acquiring measurements from their hardware;
- validating and recording local/project data;
- maintaining project-specific services and hardware control;
- exposing historical data through the standard authenticated BardBox Data API when remote historical-data access is applicable.

A project should not embed its own MCP server merely to make its historical measurements available to ChatGPT or another tool client.

### BardBox Data API

The Data API is the authenticated, read-only network boundary for historical measurement data. It should expose only approved clean readings roots and should not provide shell, service-control, configuration-write, or hardware-control capabilities.

Project data made available to downstream tools should first cross this API boundary rather than being read through SSH or direct VPS filesystem access.

### `bardbox-mcp`

`bardbox-mcp` is the shared read-only bridge between MCP clients and BardBox historical measurement data. Its role is retrieval and packaging, not acquisition, configuration, deployment, hardware control, or scientific analysis.

The current implementation began with CESH Air data. The architectural direction is to generalize the shared BardBox data-access layer as additional BardBox projects require MCP access, rather than creating separate MCP bridges per project.

Reusable query/discovery logic should remain centralized where practical so projects do not independently reimplement daily-file discovery, time-window retrieval, timestamp normalization, source selection, or related transport behavior.

## Required separation

Keep these workflows separate:

```text
Project acquisition / recording
        |
        v
Historical readings
        |
        v
Authenticated BardBox Data API
        |
        v
bardbox-mcp
        |
        v
ChatGPT / MCP clients / downstream analysis
```

Configuration and development diagnostics use a different path:

```text
Project development / configuration
        |
        +-- sync_app_config.py
        +-- generate_reports.py
        +-- config_sync_report.txt
        +-- git_diff.txt
        `-- configured report destination (for example rclone/Google Drive)
```

Do not route configuration synchronization, deployment diagnostics, service management, or hardware-control commands through `bardbox-mcp`.

## Security boundary

MCP-facing historical-data access should remain read-only. In particular:

- no SSH or direct VPS filesystem access;
- no arbitrary URL or path retrieval;
- no service restart or administration commands;
- no configuration writes;
- no hardware enable/disable/start/stop commands;
- no credentials exposed to downstream clients;
- bounded requests and explicit failures rather than silent truncation where practical.

Credentials and authentication mechanisms belong at the API/MCP transport boundary and should not be embedded in project data or reports.

## New and existing projects

When a new BardBox project is created, design its historical data and Data API behavior so that it can be exposed through the shared BardBox data-access boundary if needed later. The project does not need an MCP implementation merely because it is a BardBox project.

When an existing project's historical data needs AI/tool access:

1. Verify that its historical readings are suitable for the standard read-only Data API boundary.
2. Add or align the project's Data API support using the BardBox/project-template standard.
3. Extend the central `bardbox-mcp` data-access/query layer to support that project when necessary.
4. Keep analysis downstream: retrieval tools should not silently average, interpolate, resample, or scientifically reinterpret the source data.

The preferred architecture is one BardBox standard, project Data APIs following that standard, and one shared MCP/data-access layer.