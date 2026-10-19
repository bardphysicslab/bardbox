# BardBox Implementation Guide (redirect)

Consolidated on October 19, 2026
([bardbox#31 decision entry](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991)).
This guide described the earlier Raspberry-Pi-as-hub polling design and named a
`capabilities-schema.md` that does not exist. Its content now lives in one home
each:

| Former section | Current home |
| --- | --- |
| Core architecture, design principles, what to avoid | [ARCHITECTURE.md](../ARCHITECTURE.md) and the [Architecture Map](architecture-map.md) |
| Starting a new project | [ARCHITECTURE.md, "Starting a new project"](../ARCHITECTURE.md#starting-a-new-project) |
| Software identity, App ID and instance ID | [Node naming standard](node-naming-standard.md#application-identity) |
| UID meaning | [Node naming standard, identity layers](node-naming-standard.md#identity-layers) |
| Device wire protocol | [Device instructions](device-instructions.md) |
| Driver interface and capabilities | [Pi driver instructions](pi-driver-instructions.md) and [data source drivers](data-source-drivers.md) |
| Polling, sampling and freshness | [Data source drivers](data-source-drivers.md) and [reading format](reading-format.md) |
| Network access | [Network access](network-access.md) |
| Location and coordinates | Server Registry ([Architecture Map](architecture-map.md#project-server-template)); never firmware |
| Dashboard conventions | [Web UI standard](web-ui-standard.md) |

The earlier text remains in Git history at
`31100b88958299560b672d88030bc8e11585d2dd`.
