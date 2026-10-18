English | [Simplified Chinese](../../../../02_mcp/cases/00_mcp-server-demo/SHOWCASE.md)

# w-MCP Demo and w-Time MCP showcase

These reproducible examples are covered by protocol tests, not a fabricated
conversation transcript. HTTP and stdio remain separate teaching examples.

## HTTP: tools, resources and prompts

Start `python w-mcp_demo_server.py`, then connect to its configured MCP URL.

| Step | Call | Expected result |
| --- | --- | --- |
| Health check | ping() | server=w-MCPDemo, transport=streamable-http |
| Addition | add(a=-1, b=5) | 4 |
| Default resource | greeting://Alice | Hello, Alice! |
| Localized resource | greeting://Alice/zh | A Chinese greeting preserving the name Alice |
| English prompt | greet_user(name="Alice", language="en") | English writing instructions |
| Chinese prompt | greet_user(name="Alice", language="zh") | Chinese writing instructions |
| Invalid name | A whitespace-only name or more than 200 characters | Validation error |

Unknown prompt styles fall back to friendly. The returned prompt is an
instruction for a model, not a model-generated response. Real HTTP tests cover
addition, resources and prompts in both languages.

## Stdio: aware time and conversion

Configure the client to launch `w-time_mcp_server.py` using an absolute Python
path. Stdio is the protocol channel; ordinary logging must not use stdout.

```text
get_current_time(timezone_name="UTC", language="en")
get_current_time(timezone_name="Asia/Shanghai", language="zh")
convert_time(iso_time="2026-10-17T12:00:00+08:00", to_timezone="UTC")
```

The conversion returns `2026-10-17T04:00:00+00:00`. Current-time results include
an aware ISO-8601 value, Unix timestamp and UTC offset, while retaining the
legacy `current_time` field. With no zone, the clock uses the server machine's
local zone. IANA zones require system timezone data or the `tzdata` package.

Naive times require `from_timezone`. Unknown zones, missing source zones,
conflicting offset/source-zone inputs, ambiguous repeated DST times and
nonexistent DST times produce localized errors with stable codes. Unit tests
cover these cases; a real stdio client checks time and conversion in both
languages. No client timezone is guessed.

## Run checks

From the parent `mcp` directory, with the dependencies described in README:

```bash
python -B -m unittest -v test_weather_demo test_bilingual_tools
```

Validation platform: Windows/Python 3.12. Linux/macOS were not executed.
Old startup scripts have been removed; update existing launch configurations.
