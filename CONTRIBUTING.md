# Contributing

This repository combines course notes, notebooks and runnable agent examples.
Keep changes focused and describe the problem, resulting behavior and validation.

## Local setup

Use Python 3.12. Copy `.env.example` to `.env` and configure only the services
required by the example you are running. Never commit API keys, private endpoints,
notebook execution output containing credentials, or local MCP recovery state.

The full course dependency set is in `pyproject.toml` and `uv.lock`. Standalone
examples also document their smaller dependency sets. The trip-planner application
has separate backend and frontend setup instructions.

## Documentation and naming

- In `03_实践篇/03_tools` the unsuffixed file is the Chinese master and `english/`
  mirrors it one directory deep. Keep each pair and their relative links aligned.
- New MCP service names, client keys and primary server scripts use the `w-` prefix.
- Preserve user data and document migration steps when changing persisted state.
- Clearly label fixtures and illustrative responses; do not present them as live data.
- Clear notebook outputs before submitting, and keep secrets in environment variables.

## Offline checks

Install `mcp>=1.12,<2`, `python-dotenv`, `requests` and `tzdata` in Python 3.12.
From `03_实践篇/03_tools/02_mcp/cases`:

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
python -B -m unittest discover -s 02_file-mcp-server -p "test_file_*.py" -v
```

From `03_实践篇/03_tools/03_skills/cases/01_weather_skill`:

```bash
python -B test_weather_skill.py
```

These checks use mock weather providers and temporary files. They require no API
keys and do not consume live provider quota. Windows and Linux CI run these checks;
other course integrations require separate validation and provider credentials.

Before opening a pull request, check `git diff --check`, relevant tests and the
staged file list. Explain any validation that could not be performed.
