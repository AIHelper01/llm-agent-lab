English | [Simplified Chinese](README.zh-CN.md)

# Weather through a Skill: comparison with MCP

Ask the same question, "What is tomorrow's weather in Nanjing?", using a
**Skill plus a local script calling OpenWeather directly**. Compare that path
with the neighboring `w-OpenWeatherMCP` service. Both examples support current
weather, 5-day/3-hour forecasts, city/coordinate input, and English/Chinese output.

The Skill entry is [SKILL.md](w-openweather/SKILL.md); its executable helper is
[weather.py](w-openweather/scripts/weather.py). The helper has no MCP imports,
server connection, or dependency on the MCP server implementation. It is a
separate teaching implementation with compact output, not an exact copy of all
MCP response fields and diagnostics. Case documentation and tests stay outside
the Skill package.

## Run the script

Use Python 3.12 and install:

```bash
python -m pip install requests python-dotenv
```

Configure `OPENWEATHER_API_KEY` in the execution environment, or `.env` in the
working directory or an ancestor. `API_KEY_OPENWEATHER` is a fallback. Do not
put keys into the Skill or command arguments. Endpoint variables match the MCP
case: `OPENWEATHER_BASE_URL`, `BASE_URL_OPENWEATHER`, `OPENWEATHER_FORECAST_URL`.
A final `/weather` is changed to `/forecast` when no explicit forecast URL is set.
The shared historical variable `WEATHER_MCP_TIMEOUT_SECONDS` controls the socket
timeout; its name does not imply that the script uses MCP.

From this case directory, without starting an MCP server:

```bash
python -B w-openweather/scripts/weather.py current --location "Nanjing,CN" --language en
python -B w-openweather/scripts/weather.py forecast --location "Nanjing,CN" --date tomorrow --language zh
python -B w-openweather/scripts/weather.py forecast --latitude 32.06 --longitude 118.78 --date tomorrow --language en --include-periods
```

The script prints JSON. Exit codes: 0 success, 1 API/configuration/data failure,
2 command syntax error. Dates are `today`, `tomorrow`, `all`, or `YYYY-MM-DD`;
relative dates use the location's provider UTC offset. Forecast ranges use
returned samples, not official daily extrema. Maximum period rain probability
is not daily rain probability; boundary days may have fewer samples.

## Use it as a Skill

Register the `w-openweather/` folder according to the host agent's Skill-loading
conventions, then request:

```text
Use $w-openweather to forecast tomorrow's weather in Nanjing, China, in English.
```

Keeping a folder in a repository does not guarantee automatic discovery by every
host. This case does not alter the user's global Skill configuration. Before
registration, explicitly ask the agent to read this case's SKILL.md and follow
it. That exercises the instruction/script workflow, not automatic discovery or
automatic selection by a particular host.

## Same task, two paths

```text
Skill:
User -> Agent reads SKILL.md -> local weather.py -> OpenWeather -> JSON -> answer

This MCP example:
User -> Agent selects get_forecast -> MCP HTTP server -> OpenWeather -> tool result -> answer
```

Equivalent MCP call:

```text
get_forecast(location="Nanjing,CN", forecast_date="tomorrow", language="en", include_periods=false)
```

| Aspect | This Skill | This MCP service |
| --- | --- | --- |
| Agent entry | Metadata, instructions and a bundled script | Discoverable tool description, parameter schema and call result |
| Workflow | Agent follows instructions and chooses a command | Agent selects a tool; server executes its function |
| Data retrieval | Python runs in the agent's execution environment | API requests run in the MCP server process |
| Dependencies | Execution tool, Python, requests, python-dotenv | MCP client; server-side Python, MCP SDK and API dependencies |
| Process lifecycle | No MCP server required | This case uses an HTTP server; other MCP services may use client-launched stdio |
| Provider credentials | Script environment | Server environment; remote clients need not hold the OpenWeather key |
| Validation | CLI arguments and script checks; instructions are not enforcement | Tool schema and server-side checks |
| Updates | Skill instructions/scripts; host reload behavior may vary | Server update and tool-definition refresh when needed |
| Debugging | Command, exit status and JSON | Tool inputs/results and server logs |
| Emphasis | Reusable operational guidance | A consistent tool-call interface for clients |

Skills may include code, and MCP may also expose prompts/resources. They are
not simply "prompts versus code". They can work together: a Skill can prescribe
date selection and answer formatting while calling an MCP tool for data.
Permissions remain a host/OS/deployment concern. No latency or token benchmark
was performed, so neither approach is claimed to be inherently faster or cheaper.

References: [Agent Skills](https://agentskills.io/home),
[MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture),
[OpenWeather current weather](https://openweathermap.org/api/current),
[OpenWeather forecast](https://openweathermap.org/forecast5).

## Validation

Tests additionally need the MCP SDK for comparison, not for running the Skill:

```bash
python -m pip install "mcp>=1.12,<2"
python -B test_weather_skill.py
```

Tests use one local provider fixture for both implementations. They cover English
and Chinese CLI subprocesses, date rollover, failure exit codes and secret
redaction. MCP comparison uses in-process SDK tool dispatch. Shared fixture
dates, sample counts, sampled temperature ranges and maximum period rain
probabilities agree; complete JSON schema equality is not claimed.

The Skill also passes skill-creator's quick_validate format check. Tests do not
stop the live MCP service, install the Skill globally, or use real API quota.
Record live script checks separately from fixture checks. Host discovery and
model routing behavior are not established by these script tests.

### Dated live check

On October 17, 2026, the script queried Nanjing's October 18 forecast in a
standalone environment with only requests and python-dotenv. A separate import
check confirmed `MCP SDK installed: False`. The direct API request succeeded:
eight samples, temperatures 17.04..23.64 Celsius, and light/moderate rain.
This is a recorded verification result, not weather data to reuse later.
The existing MCP service was left running; the script did not connect to it.
The live check used the configured provider key, separately from quota-free
fixture tests. No host Skill registration or automatic discovery was performed.
