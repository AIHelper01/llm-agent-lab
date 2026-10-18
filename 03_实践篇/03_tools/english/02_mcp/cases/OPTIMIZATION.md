# MCP Optimization Record

English | [Simplified Chinese](../../../02_mcp/cases/OPTIMIZATION.md)

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

## English-default documentation migration (superseded)

This section describes the layout at the time. The `.zh-CN` suffix is no longer used; see the
Chinese-master migration record at the end of this file.

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

## Chinese-master migration and live verification (2026-10-18)

The topic is Chinese-first: unsuffixed files are the master editions and every English file now
lives under `english/` at the same relative path. All 18 pairs (36 Markdown and notebook files)
moved with `git mv` so history is preserved. Servers, tests, sample files, images and `SKILL.md`
stay in place as single language-neutral copies, so CI working directories and the `w-` naming
are unchanged.

Relative links follow the new depth: 80 links rewritten plus 18 `<img src>` prefixes repaired in
the English notebooks. All 178 relative links and images in the topic resolve, with none broken.
`scripts/check_bilingual_parity.py` (standard library only, non-zero exit on failure) checks
legacy suffixes, the one-to-one mapping, exemption reasons and counterpart links, and runs in the
`offline-tests` workflow.

Environment: a new uv project `env_agent_uv` on Python 3.12.12, with a Jupyter kernel of the same
name. Dependencies match the repository lock (`mcp==1.28.0`, `openai==2.43.0`, `httpx`, `uvicorn`,
`python-dotenv`, `requests`, `tzdata`). From the documented working directories the offline
regression suite ran in that environment: 26 weather and bilingual checks, 21 file-workbench
checks and 4 Skill comparisons, 51 in total, all passing.

All four MCP services were exercised end to end. `w-MCPDemo` answered `ping`, `add(29,13)=42` and
the `greeting://` resource over HTTP. `w-TimeMCP` returned the current Shanghai time and converted
`2026-10-18T18:30+08:00` to `2026-10-18T06:30-04:00` over stdio. `w-FileWorkbenchMCP` exposed 18
tools and read the shipped sample files with `list_files` and `read_file`. `w-OpenWeatherMCP`
exposed 6 tools and reported `missing_api_key` from `check_config` when no key is configured.
The `w-openweather` Skill script ran in the same environment as the direct-CLI comparison: without a
key, `current` (Chinese) and `forecast` (English) both reported `missing_api_key` and exited with
code 1, matching the diagnostics on the MCP path. With the repository-root `.env` configured, both Function Calling notebooks were executed end to end
with the `env_agent_uv` kernel: the model self-introduction, a live OpenWeather call, the None-FC
comparison (`tool_calls` is `None`, matching the lesson text) and two weather answers that go
through a tool call. Outputs are saved and every code cell is followed by an **Expected output:**
block. The English edition stayed fully English while the Chinese code cells kept their Chinese.
The MCP practice notebooks contain no runnable code, so each gained a verification record with the
51 offline checks and the real values returned by the four services.
