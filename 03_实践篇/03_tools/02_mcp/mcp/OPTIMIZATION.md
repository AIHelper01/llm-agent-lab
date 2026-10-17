# MCP Optimization Record

English | [Simplified Chinese](OPTIMIZATION.zh-CN.md)

The iteration started from natural-language file tasks: inspect contents, suggest
names, change extensions, add a TypeScript example, delete a Go file and restore
the directory. Those tasks exposed missing operations and recovery requirements.
The same approach was then applied to weather and basic/time examples.

| Principle | File Workbench | Weather | Basic and time examples |
| --- | --- | --- | --- |
| Identify missing operations from tasks | Delete/restore, snapshots, batch preview | Coordinate queries and forecasts | Health checks, timezones and conversion |
| Fix failure paths first | Staged publication, hashes and history rollback | Validate upstream status and schema; redact secrets | Validate inputs and reject ambiguous times |
| Bound responses | Pagination and partial reads | Raw responses are opt-in | Explicit offsets and timestamps |
| Support both languages | Preserve data; localize messages | Preserve locations; localize messages and descriptions | Language-specific resources, prompts and errors |
| Test the protocol | HTTP, injected failures and concurrency | Mock provider plus HTTP MCP | HTTP tools/resources/prompts and stdio |
| Make documentation reproducible | Preserve real conversation context and limits | Distinguish fixtures from live observations | Label demonstrations as demonstrations |
| Simplify naming | One `w-` primary entry | One `w-` primary entry | A `w-` entry for each teaching transport |

Each example retains its teaching focus. File transactions, elaborate caches and
retry frameworks are not prerequisites for addition or weather queries.

## Current entry points

- `00_mcp-server-demo/w-mcp_demo_server.py`: `w-MCPDemo`, HTTP.
- `00_mcp-server-demo/w-time_mcp_server.py`: `w-TimeMCP`, stdio.
- `01_weather-mcp-server/w-openweather_mcp_server.py`: `w-OpenWeatherMCP`, HTTP.
- `02_file-mcp-server/w-file_workbench_mcp_server.py`: `w-FileWorkbenchMCP`, HTTP.

Old wrapper scripts were removed in the earlier cleanup. Update client launch
paths when migrating. Existing file history and recovery data must be retained.

## Offline regression checks

Use Python 3.12 with `mcp>=1.12,<2`, `python-dotenv`, `requests` and `tzdata`.
From this directory:

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
python -B -m unittest discover -s 02_file-mcp-server -p "test_file_*.py" -v
```

| Suite | Test count |
| --- | --- |
| Weather, basic and time reliability/protocol tests | 12 |
| Forecast extension | 7 |
| Combined bilingual regression | 7 |
| File service regression | 21 |
| Total MCP checks | 47 |

Weather tests use a local simulated provider and consume no real key quota.
Filesystem tests use temporary data. The recorded validation platform is
Windows/Python 3.12; Linux/macOS were not exercised in that run.

The neighboring [Skill comparison](../../03_skills/cases/01_weather_skill/README.md)
adds four offline checks comparing the direct CLI and MCP paths.

## English-default documentation migration

The topic now uses `03_tools/01_function-calling`, `02_mcp` and `03_skills`.
English tutorials, notebooks and operating guides use unsuffixed filenames;
Chinese editions use `.zh-CN`. References and test paths follow the new layout.
Default English notebook outputs are cleared to avoid stale execution results.
Original Chinese course material remains available in its dedicated editions.

Notebook checkpoints were archived outside the topic alongside an original-content
backup. Sample file contents and persisted recovery state were preserved.

Validation on October 18, 2026: all 51 MCP/Skill regression tests passed.
All 37 Markdown/notebook files passed local-link, image-reference and English-source
language checks. Eight notebook weather-function variants passed mocked calls in
both language editions. Python syntax and Ruff core error checks passed. The full
repository lint profile still reports existing notebook import/style warnings and
test-code findings; this migration does not claim a clean full-profile lint run.
No live model calls were made for translation validation. The weather service was
restarted from the new location and its six tools and bilingual configuration calls
were checked through MCP without an upstream weather request.

Original course figures can still contain Chinese text. A few empty directories
under the previous topic path remain locked by open editors, a notebook kernel and
the old file-service process. Their files have moved; closing those applications
will allow the remaining empty directories to be removed without losing content.
