# w-MCP Demo and w-Time MCP

English | [Simplified Chinese](../../../../02_mcp/cases/00_mcp-server-demo/README.md)

Keep the two transports explicit: `w-mcp_demo_server.py` demonstrates tools,
resources and prompts over HTTP; `w-time_mcp_server.py` supplies timezone-aware
time tools over stdio. These are the only entries; old script names are removed.

## Setup

Requirements: Python 3.12 and `mcp>=1.12,<2`; `w-time_mcp_server.py` also needs `tzdata`.

### Option 1: pip into an existing environment

```bash
python -m pip install "mcp>=1.12,<2" tzdata
```

`tzdata` supplies IANA timezone data on systems without a timezone database,
including many Windows installations. UTC and server-local time do not need it.

### Option 2: uv ephemeral run, no installation (recommended for class)

Nothing touches the current Python interpreter:

```bash
# HTTP demo server (tool / resource / prompt)
uv run --no-project --with "mcp>=1.12,<2" python w-mcp_demo_server.py

# stdio time server
uv run --no-project --with "mcp>=1.12,<2" --with tzdata python w-time_mcp_server.py
```

### Option 3: uv with a pinned virtual environment

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python "mcp>=1.12,<2" tzdata
uv run --python .venv/bin/python w-mcp_demo_server.py
```

To reuse the companion course kernel environment, replace `.venv/bin/python` with
that environment's absolute path, for example
`uv pip install --python <your-path>/env_agent_uv/.venv/bin/python "mcp>=1.12,<2" tzdata`.

## HTTP demonstration

```bash
python w-mcp_demo_server.py
```

Server name: `w-MCPDemo`. Default URL: `http://127.0.0.1:8000/mcp`.
`DEMO_MCP_HOST` defaults to `0.0.0.0`; set it to `127.0.0.1` for local-only use.
`DEMO_MCP_PORT` defaults to 8000; invalid values fall back to 8000.
Keep-alive and graceful-shutdown timeouts are one and two seconds.
Host/Origin checks follow FastMCP's defaults; no authentication is added.

| Capability | Behavior |
| --- | --- |
| Tool `ping()` | Server identity, transport and port |
| Tool `add(a, b)` | Add integers; returns a language-neutral integer |
| Resource `greeting://Alice` | English greeting |
| Resource `greeting://Alice/en`, `greeting://Alice/zh` | Select the greeting language explicitly |
| Prompt `greet_user(name, style="friendly", language="en")` | Friendly, formal or casual greeting instructions; unknown styles fall back to friendly |

Names retain their original text and must contain a non-whitespace character,
with a maximum length of 200 characters. Validation errors are reported by MCP.
The language is part of localized resource URIs because template variables must
match function parameters. Prompts are instructions, not generated greetings.

## Time tools over stdio

```bash
python w-time_mcp_server.py
```

Server name: `w-TimeMCP`. Let an MCP client launch it and own its standard streams.
Do not use stdout for extra logging.

| Tool | Behavior |
| --- | --- |
| `get_current_time(timezone_name="", language="en")` | Server-local time by default, or UTC/IANA zone; aware ISO-8601, Unix timestamp, UTC offset and legacy current_time field |
| `convert_time(iso_time, to_timezone="UTC", from_timezone="", language="en")` | Convert an ISO-8601 timestamp; naive input requires a source zone |

An explicit UTC offset and `from_timezone` cannot be combined. Ambiguous or
nonexistent daylight-saving local times are rejected: supply an explicit offset
when selecting one of the repeated instants. Invalid zones return a localized
error and may indicate that timezone data needs installation. The server clock
belongs to the server machine, not necessarily the client's timezone.

## Configure in an agent

The two servers differ: `w-MCPDemo` is a long-running HTTP server that must be
started before connecting, while `w-TimeMCP` is a stdio server that the agent
launches and supervises itself, so it never needs to be started by hand.

### Codex

Add the Streamable HTTP server in one line and confirm with `codex mcp list`:

```bash
codex mcp add w-MCPDemo --url http://127.0.0.1:8000/mcp
codex mcp list
```

Alternatively edit `~/.codex/config.toml` directly. Codex uses `url` for
Streamable HTTP and `command` plus `args` for stdio:

```toml
[mcp_servers.w-MCPDemo]
url = "http://127.0.0.1:8000/mcp"

[mcp_servers.w-TimeMCP]
command = "uv"
args = [
  "run", "--no-project",
  "--with", "mcp>=1.12,<2", "--with", "tzdata",
  "python", "/absolute/path/w-time_mcp_server.py",
]
startup_timeout_sec = 20
```

Restart Codex after editing the config so tool lists reload. To expose only some
tools, add `enabled_tools = ["ping", "add"]`.

### Cherry Studio

Open Settings → MCP Servers → Add Server.

- `w-MCPDemo`: choose type **Streamable HTTP**, set the server URL to
  `http://127.0.0.1:8000/mcp`, save, then switch it on.
- `w-TimeMCP`: choose type **STDIO**, set the command to `uv` and enter the `args`
  list above line by line. The script path must be absolute.

Cherry Studio reads the remote endpoint from `baseUrl` (older builds also accept
`url`). JSON form:

```json
{
  "mcpServers": {
    "w-MCPDemo": {
      "name": "w-MCPDemo",
      "description": "Teaching demo: tool / resource / prompt over MCP",
      "type": "streamableHttp",
      "baseUrl": "http://127.0.0.1:8000/mcp",
      "isActive": true
    },
    "w-TimeMCP": {
      "name": "w-TimeMCP",
      "description": "Timezone-aware time tools",
      "type": "stdio",
      "command": "uv",
      "args": [
        "run", "--no-project",
        "--with", "mcp>=1.12,<2", "--with", "tzdata",
        "python", "/absolute/path/w-time_mcp_server.py"
      ],
      "isActive": false
    }
  }
}
```

Bind the server to an agent before its tools become available in chat. No
authentication or production access policy is included in these teaching
examples. Restart the server and refresh client tool lists after entry renames.

## Validation

From the parent `mcp` directory, install `python-dotenv requests` as well for the
combined weather/file regression suite, then run:

```bash
python -B -m unittest -v test_weather_demo test_bilingual_tools
```

Tests cover both languages, live HTTP MCP tools/resources/prompts, stdio time
calls, UTC/IANA conversion and daylight-saving boundaries. They use local
fixtures rather than live weather data. See [Showcase](SHOWCASE.md).
