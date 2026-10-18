# w-OpenWeather MCP

English | [Simplified Chinese](../../../../02_mcp/cases/01_weather-mcp-server/README.md)

Current-weather and 5-day/3-hour forecast tools with English or Chinese output. The only entry is
`w-openweather_mcp_server.py`; server name: `w-OpenWeatherMCP`.
Old entry scripts are not retained. Existing API-key variable aliases still work.

## Setup

Requirements: Python 3.12, `mcp>=1.12,<2`, `python-dotenv`, `requests`.

### Option 1: pip into an existing environment

```bash
python -m pip install "mcp>=1.12,<2" python-dotenv requests
python w-openweather_mcp_server.py
```

### Option 2: uv ephemeral run, no installation (recommended for class)

```bash
uv run --no-project \
  --with "mcp>=1.12,<2" --with python-dotenv --with requests \
  python w-openweather_mcp_server.py
```

The uv environment is ephemeral: nothing is written into the repository and the
current interpreter stays clean. Dependencies download on first run, then cache.

### Option 3: uv with a pinned virtual environment

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python "mcp>=1.12,<2" python-dotenv requests
uv run --python .venv/bin/python w-openweather_mcp_server.py
```

### Key and endpoint

Set `OPENWEATHER_API_KEY` in the environment or `.env` before launching.
`API_KEY_OPENWEATHER` is a fallback. `.env` is discovered by walking up from the
script directory, so placing it at the repository root works. Do not commit keys.
No key is printed by `ping` or `check_config`. Connect to `http://127.0.0.1:16681/mcp`.

## Tools

| Tool | Purpose |
| --- | --- |
| `ping()` | Server and transport diagnostics without a provider request |
| `check_config(language="en")` | Validate key presence and endpoint shape without a provider request |
| `get_weather(location, language="en", include_raw=false)` | Current metric weather by city, optionally city,country |
| `get_weather_by_coordinates(latitude, longitude, language="en", include_raw=false)` | Current metric weather at latitude -90..90 and longitude -180..180 |
| `get_forecast(location, forecast_date="tomorrow", language="en", include_periods=true, include_raw=false)` | Forecast by city for a location-local date |
| `get_forecast_by_coordinates(latitude, longitude, forecast_date="tomorrow", language="en", include_periods=true, include_raw=false)` | Forecast by coordinates for a location-local date |

Server instructions and tool descriptions are bilingual (Chinese first, English
second). The `language` parameter accepts `en` and `zh` and localizes returned text.
Descriptions use the requested provider language;
city names and coordinates retain their meaning, and JSON keys/error codes stay
stable. City queries are trimmed and limited to 200 characters. City resolution
is provider-dependent; coordinates avoid city-name ambiguity. The provider's
[official current-weather API](https://openweathermap.org/api/current) documents
coordinate queries, metric units, language parameters and the deprecated built-in
city-name geocoder. This service adds no automatic geocoding dependency.

Results include temperatures in Celsius, wind in meters per second, coordinates,
humidity, pressure and provider observation timestamps when supplied. Raw data
is now opt-in: use `include_raw=true` for diagnostics. Secrets reflected by an
upstream response are redacted even in raw data.

## Forecast dates and summaries

Forecasts use OpenWeather's [5-day/3-hour API](https://openweathermap.org/forecast5)
and the same API key. Endpoint eligibility depends on your provider account.
`forecast_date` accepts `tomorrow` (default), `today`, `all`, or `YYYY-MM-DD`.
Relative dates use the queried location's returned UTC offset and the current
instant, not the server's local calendar. Missing timezone data is an error.

Summaries show the min/max of returned temperature samples, not official daily
extrema. `max_period_precipitation_probability` is the maximum of the returned
period probabilities, not the probability of rain over an entire day. The
`has_eight_3h_samples` flag distinguishes full sample sets from partial dates.
Forecast boundary dates may be partial. No data is invented outside coverage;
`forecast_date_unavailable` includes `available_dates`.

Use `include_periods=false` for compact summaries; raw data stays opt-in.
Local timestamps use the provider's fixed UTC offset, not an IANA timezone or
a prediction of DST transitions. The existing current-weather tools are unchanged.

```json
{"location":"Nanjing,CN","forecast_date":"tomorrow","language":"en"}
```

## Error handling

Failures return `ok=false`, a stable `error`, and a localized `message`.

| Code | Trigger |
| --- | --- |
| `invalid_location`, `invalid_coordinates` | Invalid input; no provider request |
| `missing_api_key`, `invalid_config` | Missing key or invalid endpoint |
| `timeout`, `request_failed` | Timeout or connection failure |
| `invalid_api_key`, `access_denied` | HTTP 401 or 403 |
| `location_not_found`, `rate_limited` | HTTP 404 or 429 |
| `provider_unavailable`, `openweather_error` | Server errors or other unsuccessful HTTP/provider status |
| `invalid_json`, `invalid_response` | Invalid JSON, unexpected structure, missing required fields or invalid numeric values |
| `invalid_date`, `forecast_date_unavailable` | Invalid date selector, or no forecast samples for the requested local date |

Numeric Retry-After headers are exposed as `retry_after_seconds`, capped at one
day. Requests are not automatically retried, preventing accidental quota use.
Request exception strings and provider error bodies are never echoed because
they may contain credentials. Redirects are disabled. Responses are closed after
processing. A valid endpoint is HTTP(S) without embedded credentials, a query
string, or a fragment. HTTP is supported for local test providers; use HTTPS for
real provider credentials.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENWEATHER_API_KEY` | unset | Provider key; fallback API_KEY_OPENWEATHER |
| `OPENWEATHER_BASE_URL` | `https://api.openweathermap.org/data/2.5/weather` | Provider endpoint; fallback BASE_URL_OPENWEATHER |
| `OPENWEATHER_FORECAST_URL` | `https://api.openweathermap.org/data/2.5/forecast` for the standard endpoint | Optional forecast endpoint; otherwise derive by replacing a final /weather with /forecast; custom paths require this setting |
| `WEATHER_MCP_HOST` | `0.0.0.0` | Bind address; use 127.0.0.1 for local-only access |
| `WEATHER_MCP_PORT` | `16681` | Port; invalid high values fall back to the default |
| `WEATHER_MCP_TIMEOUT_SECONDS` | `10` | Requests socket timeout, not a total-operation deadline |
| `WEATHER_MCP_ENABLE_DNS_REBINDING_PROTECTION` | `false` | Host/Origin validation |
| `WEATHER_MCP_ALLOWED_HOSTS` | localhost and 127.0.0.1 with the configured port | Comma-separated allowed hosts |
| `WEATHER_MCP_ALLOWED_ORIGINS` | empty | Comma-separated origins |
| `WEATHER_MCP_UVICORN_TIMEOUT_KEEP_ALIVE` | `1` | Keep-alive seconds |
| `WEATHER_MCP_UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN` | `2` | Shutdown grace seconds |

The teaching defaults have no authentication or built-in rate limit. Restrict
network access; use an authenticated gateway for shared deployment. Anyone with
access can consume the configured key's quota. This service supplies current
weather and 5-day/3-hour forecasts, not historical weather. Restart and refresh client tools after upgrade.

## Configure in an agent

This is a long-running HTTP server: start it first, then add the connection in the
agent. The server process reads the API key, so the agent never needs the key.

### Codex

Add it in one line and confirm with `codex mcp list`:

```bash
codex mcp add w-OpenWeatherMCP --url http://127.0.0.1:16681/mcp
codex mcp list
```

Alternatively edit `~/.codex/config.toml`; Codex uses `url` for Streamable HTTP:

```toml
[mcp_servers.w-OpenWeatherMCP]
url = "http://127.0.0.1:16681/mcp"
tool_timeout_sec = 30
```

For a server on another machine use `http://<server-ip>:16681/mcp` and enable Host
validation as needed. Restart Codex after editing the config. For a read-only class
demo, narrow the surface with `enabled_tools = ["get_weather", "get_forecast"]`.

### Cherry Studio

Open Settings → MCP Servers → Add Server, choose type **Streamable HTTP**, set the
server URL to `http://127.0.0.1:16681/mcp`, save, switch it on, then bind it to an agent.

JSON form (Cherry Studio reads the endpoint from `baseUrl`; older builds accept `url`):

```json
{
  "mcpServers": {
    "w-OpenWeatherMCP": {
      "name": "w-OpenWeatherMCP",
      "description": "OpenWeather current weather and 5-day/3-hour forecasts",
      "type": "streamableHttp",
      "baseUrl": "http://127.0.0.1:16681/mcp",
      "isActive": true
    }
  }
}
```

Tool descriptions and server instructions are bilingual, while returned text
defaults to English; request Chinese by passing `language="zh"` in the tool call
rather than by changing client configuration.

## Validation

From the parent `mcp` directory:

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
```

Tests cover both languages, malformed responses, secret redaction, provider status
codes and real HTTP MCP dispatch to a local fixture provider. They use no real
weather key or quota. See [Showcase](SHOWCASE.md).

Forecast checks additionally cover local-date rollover, partial coverage, invalid
timestamps, missing timezone offsets, invalid probabilities and both MCP tools.
