# BardBox Web Node Protocol

Protocol version: `web-node-v0.2`

This is the canonical BardBox standard for nodes that send measurements to a
remote service over a network. It extends the compact local device protocol in
[Device Instructions](device-instructions.md); it does not replace or redefine
that command/response contract.

Project repositories may document payload schemas, endpoints, hardware, and
storage implementations, but must not maintain independent BardBox-wide Web
Node standards.

## Scope

A Web Node measures, timestamps, stores, and transmits data while preserving
local diagnostics and retaining unacknowledged measurements for retry. The
standard does not mandate a sensor type, payload schema, network transport, or
persistent-storage implementation.

## Transport and payload independence

Transport and payload format are separate decisions. A Web Node may use HTTP,
HTTPS, TCP, MQTT, or another documented network transport, and may transmit
JSON, CSV, text, binary, or another documented payload. Each implementation
must document its endpoint, transport, payload schema, authentication, and
acknowledgment behavior.

When practical, field names, units, and meanings should remain consistent
across local diagnostics, local streaming, network payloads, and server
storage. Interface-specific metadata is allowed when documented.

## Device command categories

Commands and responses follow [Device Instructions](device-instructions.md).
Web Node implementations classify commands as follows.

### Core commands

All BardBox protocol nodes implement:

- `INFO` — identity, versions, capabilities, and current diagnostic state;
- `HEADER` — ordered schema for the local reading response;
- `READ` — one current reading matching `HEADER`, or a protocol error.

### Optional general commands

- `PING` — connectivity check;
- `START` — begin local streaming for devices that support it;
- `STOP` — stop local streaming.

### Optional Web Node diagnostics and maintenance

- `UPLOAD` — explicitly request an upload attempt and diagnostic result;
- `PAYLOAD` — display the current network payload without changing delivery
  state;
- `BUFFER` — display persistent queue state, including `buffer_count` and
  `buffer_max_records`.

These commands are optional because not every node owns a network uploader or
persistent queue.

### Destructive maintenance

- `BUFFER_CLEAR` — discard locally buffered, unacknowledged measurements.

`BUFFER_CLEAR` is destructive. Implementations must document that it causes
data loss and must never invoke it automatically as an error-recovery action.
It should be exposed only when deliberate local maintenance requires it.

`TRACE` and `CATCHUP_TRACE` are not standard BardBox commands. Projects must
not require them for protocol conformance.

## Quiet background operation

Automatic sampling, upload, retry, and catch-up activity must not flood or
interleave with the normal serial diagnostic/protocol stream. Production
firmware should keep per-upload success lines, HTTP response bodies, retry
traces, and catch-up summaries disabled by default.

Verbose upload diagnostics may be emitted in response to an explicit operator
diagnostic action such as `UPLOAD`, or by a deliberately enabled development
or debug build. Normal state and recent failures remain inspectable through
`INFO`, `READ`, and `BUFFER` where implemented.

## Raw-data philosophy

Nodes should transmit measurements as close to original sensor output as
practical and avoid irreversible averaging, smoothing, correction, sensor
fusion, scoring, or derived metrics unless the application explicitly requires
them. Batching original measurements is encouraged when useful; averaging them
before transmission is discouraged. Server-side processing is preferred so
algorithms can evolve without firmware replacement.

## Responsibilities

The node owns:

- measurement and timestamping;
- local persistent storage;
- network communication and retry behavior;
- local diagnostic state.

The server generally owns:

- durable archive storage;
- normalization, aggregation, and analysis;
- visualization and reporting;
- correction algorithms and derived metrics.

Servers should preserve original measurements whenever practical. Nodes should
remain as simple as reliable acquisition and delivery allow.

## Persistent buffering

A Web Node must not assume successful delivery. Whenever practical, each new
measurement should be written to nonvolatile storage before its first
transmission attempt. The buffer acts as an ordered delivery queue:

1. Append each new measurement.
2. Attempt the oldest queued measurement first.
3. Retain it until a successful protocol acknowledgment is received.
4. Remove only that acknowledged record.
5. Preserve queue order whenever practical.

Flash filesystems, SD cards, databases, append-only logs, rotating files,
fixed-size segments, or other documented mechanisms are acceptable. The
implementation should define a finite capacity and must document what happens
when that capacity is reached. Keeping newer monitoring data is generally
preferred when finite storage forces data loss.

Long-term deployments should use storage-efficient queue designs that avoid
rewriting a large archive after every acknowledgment.

## Acknowledgment semantics

A measurement is delivered only after a successful protocol-level response.
For HTTP and HTTPS implementations, any HTTP `2xx` response is an
acknowledgment. Redirects, `4xx`, `5xx`, timeouts, connection failures, TLS
failures, malformed responses, and missing responses are not acknowledgments.

A node must never remove a buffered measurement before acknowledgment. A failed
upload leaves the current record queued and updates diagnostic error state.

## Retry and catch-up

Failed transmissions should be retried. Buffered readings should be retried
oldest-first. Catch-up must not suspend normal measurement: the node continues
sampling and appending new records while older records are being delivered.

Implementations may batch requests or use bounded bursts, pauses, and backoff
to protect the node, network, server, and diagnostic interface. These controls
must not weaken acknowledgment or queue-order rules.

## Local diagnostics

Web Nodes should provide local diagnostic access through USB serial or another
documented interface. `INFO` should expose, where applicable:

- node UID, type, and model;
- firmware version and protocol version;
- transport/connectivity status;
- last communication or upload status;
- recent communication and storage errors;
- last successful upload time;
- buffer availability or mounted state;
- `buffer_count`;
- `buffer_max_records`.

`buffer_count` is the number of measurements waiting for acknowledgment.
`buffer_max_records` is the configured maximum queue capacity. When practical,
the same names and meanings should also appear in `READ`, `START`, and network
payload metadata.

## Firmware and protocol versioning

Firmware and protocol versions describe different things:

- the firmware version identifies a particular build and changes for
  deployment-relevant fixes or implementation behavior;
- the protocol version identifies the shared behavior contract and changes
  only when that contract changes.

A hardware fix, internal cleanup, or local diagnostic refinement normally
changes only the firmware version. Changes to acknowledgment, buffering, retry,
required diagnostics, metadata, transport expectations, or payload
compatibility may require a protocol-version change.

Web Nodes should report the UID, node type, node model, firmware version, and
protocol version through `INFO` and, when practical, network payload metadata.

Example:

```text
fw_version=0.3.1
protocol_version=web-node-v0.2
```

## Conformance summary

A conforming Web Node:

- follows the core BardBox commands;
- documents its transport and payload schema;
- retains measurements until acknowledged;
- treats HTTP/HTTPS `2xx` as acknowledgment;
- retries buffered records oldest-first;
- continues sampling during catch-up;
- exposes useful local diagnostics and buffer capacity;
- reports firmware and protocol versions independently;
- keeps automatic background network activity quiet in production;
- never clears buffered data automatically to recover from an upload failure.
