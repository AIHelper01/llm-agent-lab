# Tools: Function Calling, MCP and Skills

English | [Simplified Chinese](../README.md)

Learn how a model requests a function call, how MCP exposes reusable capabilities,
and how a Skill packages instructions and scripts into a repeatable workflow.
This topic is Chinese-first: the unsuffixed file beside each English one is the master
edition, and every file here mirrors a Chinese file at the same relative path.

| Module | English | Simplified Chinese |
| --- | --- | --- |
| Overview | [Agents and tools](overview.md) | [Overview](../overview.md) |
| Function Calling | [Practice notebook](01_function-calling/01_fc-practice.ipynb) | [Practice notebook](../01_function-calling/01_fc-practice.ipynb) |
| MCP | [Theory](02_mcp/01_mcp-theory.md), [Practice](02_mcp/02_mcp-practice.ipynb) | [Theory](../02_mcp/01_mcp-theory.md), [Practice](../02_mcp/02_mcp-practice.ipynb) |
| Skills | [Theory](03_skills/skills-theory.md) | [Theory](../03_skills/skills-theory.md) |
| Weather Skill vs MCP | [Runnable comparison](03_skills/cases/01_weather_skill/README.md) | [Comparison](../03_skills/cases/01_weather_skill/README.md) |

## Runnable MCP examples

- [Basic and time tools](02_mcp/cases/00_mcp-server-demo/README.md)
- [OpenWeather current weather and forecasts](02_mcp/cases/01_weather-mcp-server/README.md)
- [File Workbench](02_mcp/cases/02_file-mcp-server/README.md)
- [Optimization notes](02_mcp/cases/OPTIMIZATION.md)

The three HTTP servers are long-running processes; the stdio server is launched by
the agent itself.

| Server | Transport | Default endpoint | uv run without installation (inside that server directory) |
| --- | --- | --- | --- |
| `w-MCPDemo` | Streamable HTTP | `http://127.0.0.1:8000/mcp` | `uv run --no-project --with "mcp>=1.12,<2" python w-mcp_demo_server.py` |
| `w-OpenWeatherMCP` | Streamable HTTP | `http://127.0.0.1:16681/mcp` | `uv run --no-project --with "mcp>=1.12,<2" --with python-dotenv --with requests python w-openweather_mcp_server.py` |
| `w-FileWorkbenchMCP` | Streamable HTTP | `http://127.0.0.1:16682/mcp` | `uv run --no-project --with "mcp>=1.12,<2" --with python-dotenv python w-file_workbench_mcp_server.py` |
| `w-TimeMCP` | stdio | no port; started by the client | `uv run --no-project --with "mcp>=1.12,<2" --with tzdata python w-time_mcp_server.py` |

Each server README carries two sections: starting the server (pip and three uv
options) and configuring it in an agent (full Codex and Cherry Studio setups).
Codex attaches to an HTTP server in one line: `codex mcp add <name> --url <mcp-url>`;
Cherry Studio uses Settings → MCP Servers → Add Server, where the remote endpoint
field is `baseUrl`.

Run examples from their documented working directories. Use Python 3.12 and
`mcp>=1.12,<2`, `python-dotenv`, `requests`, and `tzdata`. Repository users can
run `uv sync` from the repository root. For an isolated environment:

```bash
python -m pip install "mcp>=1.12,<2" python-dotenv requests tzdata
```

From `02_mcp/cases`, run the offline regression suite:

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
python -B -m unittest discover -s 02_file-mcp-server -p "test_file_*.py" -v
```

From `03_skills/cases/01_weather_skill`, run `python -B test_weather_skill.py`.
These tests mock OpenWeather and use temporary files; they consume no real API quota.
Notebook model/API calls are interactive exercises and require your own credentials.
Their example responses are illustrative, not live weather.

## Language and migration

Server instructions and tool descriptions are bilingual, Chinese first and English
second, so clients show both languages at once. Returned messages and weather text
default to English; pass `language="zh"` for Chinese or `language="en"` explicitly. JSON keys and error codes stay stable. User file names,
content and city inputs retain their language; the option does not translate user data.
OpenWeather controls city resolution and localized weather descriptions.

The topic is now `03_tools`, with `01_function-calling`, `02_mcp`, and `03_skills`.
Update launch paths and notebook bookmarks that used the previous directory names.
All primary MCP scripts and client configuration keys use `w-`. File recovery data
and sample files are retained. The installed `w-openweather` Skill is self-contained
and does not depend on the repository directory name.

Tutorial figures retained from the original course may contain Chinese labels;
English text and captions explain their meaning. The Chinese master editions sit
one directory above and keep the original detailed teaching material.
