# w-MCP Demo and w-Time MCP

English | [Simplified Chinese](README.zh-CN.md)

Keep the two transports explicit: `w-mcp_demo_server.py` demonstrates tools,
resources and prompts over HTTP; `w-time_mcp_server.py` supplies timezone-aware
time tools over stdio. These are the only entries; old script names are removed.

## Setup

Python 3.12:

```bash
python -m pip install "mcp>=1.12,<2" tzdata
```

`tzdata` supplies IANA timezone data on systems without a timezone database,
including many Windows installations. UTC and server-local time do not need it.

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

```json
{
  "mcpServers": {
    "w-MCPDemo": {"url": "http://127.0.0.1:8000/mcp", "type": "streamableHttp"},
    "w-TimeMCP": {"command": "/absolute/path/to/python", "args": ["/absolute/path/to/w-time_mcp_server.py"]}
  }
}
```

Use real absolute paths. On Windows, escape backslashes in JSON or use forward
slashes. No authentication or production access policy is included in these
teaching examples. Restart/refresh clients after changing entry names.

## Validation

From the parent `mcp` directory, install `python-dotenv requests` as well for the
combined weather/file regression suite, then run:

```bash
python -B -m unittest -v test_weather_demo test_bilingual_tools
```

Tests cover both languages, live HTTP MCP tools/resources/prompts, stdio time
calls, UTC/IANA conversion and daylight-saving boundaries. They use local
fixtures rather than live weather data. See [Showcase](SHOWCASE.md).
