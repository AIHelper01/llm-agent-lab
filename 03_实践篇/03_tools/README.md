# Tools: Function Calling, MCP and Skills

English | [Simplified Chinese](README.zh-CN.md)

Learn how a model requests a function call, how MCP exposes reusable capabilities,
and how a Skill packages instructions and scripts into a repeatable workflow.
English is the default throughout this topic. Chinese editions use `.zh-CN`.

| Module | English | Simplified Chinese |
| --- | --- | --- |
| Overview | [Agents and tools](overview.md) | [Overview](overview.zh-CN.md) |
| Function Calling | [Practice notebook](01_function-calling/01_fc-practice.ipynb) | [Practice notebook](01_function-calling/01_fc-practice.zh-CN.ipynb) |
| MCP | [Theory](02_mcp/01_mcp-theory.md), [Practice](02_mcp/02_mcp-practice.ipynb) | [Theory](02_mcp/01_mcp-theory.zh-CN.md), [Practice](02_mcp/02_mcp-practice.zh-CN.ipynb) |
| Skills | [Theory](03_skills/skills-theory.md) | [Theory](03_skills/skills-theory.zh-CN.md) |
| Weather Skill vs MCP | [Runnable comparison](03_skills/cases/01_weather_skill/README.md) | [Comparison](03_skills/cases/01_weather_skill/README.zh-CN.md) |

## Runnable MCP examples

- [Basic and time tools](02_mcp/mcp/00_mcp-server-demo/README.md)
- [OpenWeather current weather and forecasts](02_mcp/mcp/01_weather-mcp-server/README.md)
- [File Workbench](02_mcp/mcp/02_file-mcp-server/README.md)
- [Optimization notes](02_mcp/mcp/OPTIMIZATION.md)

Run examples from their documented working directories. Use Python 3.12 and
`mcp>=1.12,<2`, `python-dotenv`, `requests`, and `tzdata`. Repository users can
run `uv sync` from the repository root. For an isolated environment:

```bash
python -m pip install "mcp>=1.12,<2" python-dotenv requests tzdata
```

From `02_mcp/mcp`, run the offline regression suite:

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
python -B -m unittest discover -s 02_file-mcp-server -p "test_file_*.py" -v
```

From `03_skills/cases/01_weather_skill`, run `python -B test_weather_skill.py`.
These tests mock OpenWeather and use temporary files; they consume no real API quota.
Notebook model/API calls are interactive exercises and require your own credentials.
Their example responses are illustrative, not live weather.

## Language and migration

Tool descriptions and messages default to English. Pass `language="zh"` for Chinese
or `language="en"` explicitly. JSON keys and error codes stay stable. User file names,
content and city inputs retain their language; the option does not translate user data.
OpenWeather controls city resolution and localized weather descriptions.

The topic is now `03_tools`, with `01_function-calling`, `02_mcp`, and `03_skills`.
Update launch paths and notebook bookmarks that used the previous directory names.
All primary MCP scripts and client configuration keys use `w-`. File recovery data
and sample files are retained. The installed `w-openweather` Skill is self-contained
and does not depend on the repository directory name.

Tutorial figures retained from the original course may contain Chinese labels;
English text and captions explain their meaning. The `.zh-CN` editions preserve
the original detailed Chinese teaching material.
