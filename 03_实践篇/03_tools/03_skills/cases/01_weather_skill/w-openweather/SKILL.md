---
name: w-openweather
description: Query current weather or 5-day/3-hour forecasts directly from OpenWeather using the bundled Python CLI. Use for weather requests when a local script workflow is appropriate, including English or Chinese output. Follow an explicit request to use MCP instead of switching to this workflow.
---

# OpenWeather through a local script

Use `scripts/weather.py` relative to this skill directory. It calls OpenWeather
directly; it does not connect to an MCP server or require the MCP SDK.
The runtime needs Python 3.12, `requests`, and `python-dotenv`.

## Choose the request

- Use `current` for current observations and `forecast` for future weather.
- Reuse the location from the conversation when clear. Otherwise ask for the
  location. Do not infer the user's location from the computer's timezone.
- Pass a city with country code, or both latitude and longitude. Preserve the
  supplied city name. Prefer supplied coordinates when city names are ambiguous.
- Use `--language en` or `--language zh` to match the request.
- For forecasts, `--date tomorrow` is the default. Other values are `today`,
  `all`, or `YYYY-MM-DD`. Relative dates use the provider's location UTC offset.

Examples (replace `<skill-dir>` with this skill's actual absolute directory):

```text
python -B "<skill-dir>/scripts/weather.py" current --location "Nanjing,CN" --language en
python -B "<skill-dir>/scripts/weather.py" forecast --location "Nanjing,CN" --date tomorrow --language zh
python -B "<skill-dir>/scripts/weather.py" forecast --latitude 32.06 --longitude 118.78 --date tomorrow --language en
```

`OPENWEATHER_API_KEY` is read from the environment; `API_KEY_OPENWEATHER` is a
fallback. A `.env` in the working directory or an ancestor is also supported.
Read only the variable's presence when diagnosing configuration; never print
keys or put them in command arguments. Endpoint and timeout environment variables
match the MCP case. Credentials are required in the script execution environment.

## Interpret the result

The script writes JSON to stdout. Exit 0 means success; exit 1 means an API,
configuration, or data error. Invalid command syntax exits 2. Check `ok` before
describing the weather. A missing key, timeout, unsupported date, invalid location,
or provider error must be reported; do not silently substitute web search or an
MCP call. Do not automatically retry quota or authentication failures.

Forecast summaries use returned 3-hour samples. Report sampled temperature ranges
and maximum **period** rain probability, not official daily extremes or a daily
rain probability. Partial days are identified by their sample count. Include
the requested local date in the answer; label current observations as current.
The fixed UTC offset does not predict DST changes. Use `--include-periods` when
the user wants a time breakdown. Missing samples are not forecasts of clear skies.

This skill does not install dependencies, register itself with the host, start
services, or change user configuration automatically. Run the script using the
host's available execution tool and existing permissions.
