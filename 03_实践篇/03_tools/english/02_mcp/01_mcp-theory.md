# Model Context Protocol: Theory and Engineering

English | [Simplified Chinese](../../02_mcp/01_mcp-theory.md)

## Purpose and boundaries

MCP connects an AI application to external capabilities through a shared protocol.
A host can reuse a server's tools, resources and prompts without writing a custom
integration for every operation. Servers can wrap local functions, files, databases
or remote APIs. The host still controls model interaction, permission and presentation.
Protocol interoperability does not by itself provide authentication, isolation or
correctness of the underlying operation.

The ecosystem includes SDKs, hosts, server implementations and deployment services.
Compatibility depends on the negotiated protocol version, transport and capabilities.
Check those properties before assuming that two products can interoperate.

This repository runs the official Python SDK 1.x (`mcp>=1.12,<2`). Its
`mcp.server.fastmcp.FastMCP` is distinct from the separately distributed `fastmcp`
package. Both use the name FastMCP, but features, CLI commands and release schedules
differ. Do not combine imports or installation instructions indiscriminately.

## Host, client and server

The host owns the application experience and model context. A client represents a
connection to one server. Multiple clients let a host compose capabilities from
several servers while retaining a common conversation.

For example, a travel host could connect to weather, mapping and booking servers.
Weather tools return conditions, mapping resources provide location context, and a
booking tool creates a reservation. The host determines the sequence and requests
confirmation for consequential operations according to its policy. Each server can
remain focused on its own domain.

## Protocol layers and lifecycle

The data layer defines JSON-RPC messages, initialization, capability negotiation,
operations and notifications. The transport layer carries them between processes
or over a network. Stdio is useful for a local subprocess; Streamable HTTP is useful
for an independently running service. Legacy HTTP+SSE is covered for comparison.

For the SDK generation used here, the lifecycle is:

1. Establish the transport and send `initialize`.
2. Negotiate a supported protocol version and capabilities.
3. Send the initialized notification.
4. Discover supported tools, resources and prompts as needed.
5. Exchange calls, reads, results and supported notifications.
6. Close the session and release transport resources.

An illustrative tool exchange follows. It omits request identifiers and envelopes
for readability; actual wire messages are JSON-RPC messages.

```json
{"method":"tools/list","params":{}}
{"method":"tools/call","params":{"name":"add","arguments":{"a":2,"b":3}}}
```

The server advertises schemas and returns content for tool calls. The application
decides how to convert schemas into model definitions and how to handle failures.
A notification has no response identifier. A server may advertise list-change
notifications so clients know when to rediscover capabilities. Clients should not
assume every optional operation is supported.

## Server primitives

### Tools

Tools perform operations and expose names, descriptions and argument schemas.
Descriptions help a host or model decide when a call is appropriate. Schemas make
arguments explicit, while server-side validation enforces actual constraints.
Return concise results, stable machine-readable fields and actionable errors.
Do not expose API keys through exception messages or request URLs.

In travel planning, `search_flights` and `reserve_hotel` represent different effects.
Describe those effects clearly. A read-only query and a booking operation should
not be indistinguishable to the host. Results are external data, not new instructions
that override the user's request.

### Resources

Resources expose readable contextual data through URIs. A client can list available
resources or templates and read the selected item. A project document, city guide
or itinerary can be a resource. URI templates express parameterized resources;
completion support, where implemented, can suggest valid argument values.

Resources are not automatically injected into every model conversation. The host
chooses what to read and include. Subscription and change notifications are optional
and capability-dependent.

### Prompts

Prompts expose reusable message templates with documented arguments. For example,
a trip-planning prompt can ask for destination, dates and budget. It provides a
starting structure rather than bypassing user or host controls. A server can offer
prompts alongside tools and resources without being a model service itself.

## Client-provided capabilities

### Elicitation

Where supported, a server can request additional input through the client. A travel
workflow might ask for an airport preference before continuing. The host presents
the request and reports the user's response according to the negotiated capability.
Handle declined or cancelled requests explicitly. Do not assume a background client
has an interactive user available.

### Roots

Roots identify client-provided workspace boundaries, commonly file URIs. A travel
project could identify the directory containing plans and receipts. Roots communicate
scope; the server must still validate file paths and enforce its own access policy.
They are not a filesystem sandbox or an authorization grant to read arbitrary files.

### Sampling

Sampling lets a server request a model interaction through a capable client. A server
could ask for a summary of flight options after retrieving structured results. The
client controls the model, context and approval policy. Support is optional, and
servers should handle unavailable or rejected sampling instead of depending on it
for a basic deterministic operation.

## Transports

| Transport | Process model | Typical use | Notes |
| --- | --- | --- | --- |
| stdio | Client launches a subprocess | Local tools and desktop hosts | Protocol goes to stdout; logs go to stderr |
| Streamable HTTP | Independently running HTTP service | Shared or remote services | The examples use `/mcp`; manage service lifecycle separately |
| Legacy HTTP+SSE | SSE stream plus HTTP message submission | Older integrations | Both sides must support the legacy transport |

Stdio avoids an HTTP listener but still has serialization and process overhead.
HTTP does not require token streaming from a language model: it carries MCP protocol
messages and may use streaming responses. SSE alone is one-way, whereas the legacy
MCP transport combines it with HTTP submission to support request/response exchange.
Choose a transport based on host support and deployment needs rather than claims
of universal zero latency or universal product defaults.

## Building a server with the repository SDK

Install the dependencies in an isolated Python environment:

```bash
python -m pip install "mcp>=1.12,<2" python-dotenv requests tzdata
```

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("w-MCPDemo", host="127.0.0.1", port=16680)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

Use the checked-in [basic demo](cases/00_mcp-server-demo/README.md) for resources,
prompts and the supported startup procedure. Its time companion demonstrates stdio.
The [weather server](cases/01_weather-mcp-server/README.md) adds input validation,
upstream requests and bilingual summaries. The
[file server](cases/02_file-mcp-server/README.md) adds persistence, recoverability and
concurrent-operation handling appropriate to file changes.

Avoid adding file transactions or elaborate retry frameworks to the addition demo.
The purpose of each example should remain visible.

## Clients and connection lifetime

A client opens a transport, creates a `ClientSession`, initializes it, and uses the
negotiated operations within that session. Context managers ensure cleanup.

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client("http://127.0.0.1:16680/mcp") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("add", {"a": 2, "b": 3})
            print(result)

asyncio.run(main())
```

Stdio clients instead provide a command, arguments and environment using the SDK's
stdio transport. HTTP clients connect to a running URL. A local Python filename is
not an HTTP endpoint; a host configuration must explain whether it starts a process
or connects to an existing service. Use absolute executable and script paths where
the host does not guarantee a working directory.

Callbacks for roots, sampling or elicitation must follow the client's SDK version.
Multiple servers require distinct connection lifetimes and routing by server/tool
identity. Keep credentials in the environment or host secret configuration rather
than in committed client JSON.

## The separate FastMCP package

The original course also introduces the third-party FastMCP framework. Install it
only for exercises that explicitly use `from fastmcp import FastMCP`. Review that
release's [official documentation](https://gofastmcp.com/) before using optional
dependencies, upgrade commands or deployment integrations.

Its ecosystem includes tool/resource/prompt decorators, in-memory clients, local
process and HTTP transports, server composition, filtering and deployment workflows.
Some releases expose tags, custom routes, authentication, storage or UI integrations.
These are framework features with version-specific APIs, not universal MCP methods.
The repository's official-SDK examples do not require them.

For framework CLI exercises, inspect the installed CLI's `--help` first. Check the
server target syntax, object name, transport, host/port and authentication settings.
A target such as a Python module and server object identifies code; an HTTP URL
identifies a running endpoint. CLI transport overrides and configuration-file formats
are package-specific. Managed hosting services, including the historical Prefect
Horizon example, are optional deployment choices rather than protocol requirements.

## Engineering checklist and exercises

Keep functions focused, schemas clear, error fields stable and responses bounded.
Validate city names, coordinates, timezones and file paths at the server boundary.
Treat raw upstream data as optional when a concise summary meets the task. Preserve
state when renaming or restarting a service, and update client paths during migration.

Test the protocol surface as well as direct Python functions: initialization,
discovery, actual calls, resource reads, prompt retrieval and transport shutdown.
Use mocked upstream responses to test errors and language behavior without consuming
API quota. Test real filesystem behavior with temporary directories, including
failure paths and concurrent changes for the file service.

Try the examples in order: addition, time, current weather, tomorrow's forecast,
then a file lifecycle with preview, rename, delete and restore. Compare English
defaults with `language="zh"`, retaining the same JSON keys and error codes.
See [practice](02_mcp-practice.ipynb) and the
[optimization record](cases/OPTIMIZATION.md) for runnable commands and limits.

Reference: [MCP documentation](https://modelcontextprotocol.io/docs/learn/architecture).
Match the documentation version to the negotiated SDK protocol version.
