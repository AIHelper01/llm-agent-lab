English | [Simplified Chinese](SHOWCASE.zh-CN.md)

# w-OpenWeather MCP: bilingual weather queries

This showcase separates reproducible fixture checks from dated live verification.
Automated checks use a local fixture provider and a real HTTP MCP server/client;
they do not consume an OpenWeather key or quota. The final section records a
separate live verification after enabling forecasts.

## Scenario

1. Call `ping` and `check_config` to check the server and configuration.
2. Call `get_weather(location="London,GB")` for default English output.
3. Repeat with `language="zh"` for Chinese descriptions and messages.
4. Call `get_weather_by_coordinates(latitude=39.9, longitude=116.4)` to avoid
   ambiguity in city-name resolution.
5. Request `include_raw=true` only when provider diagnostics are needed.

English example:

```json
{"latitude":39.9,"longitude":116.4,"language":"en","include_raw":false}
```

The success response has stable English field names, Celsius temperature and
meters-per-second wind values. Input locations are not translated. Local fixture
descriptions are predetermined; they are not current real-world observations.

## Failure scenarios

| Input or provider condition | Expected result |
| --- | --- |
| Empty/overlong city or out-of-range/non-finite coordinates | Localized validation error; no request |
| Missing key or malformed endpoint | Localized configuration error; no weather request |
| HTTP 401 / 403 / 404 / 429 | invalid_api_key / access_denied / location_not_found / rate_limited |
| Timeout or connection exception containing a secret URL | Localized error without echoing the URL or key |
| HTTP 200 with invalid JSON, an array, missing weather fields or NaN | invalid_json or invalid_response |
| Provider reflects the configured key in raw data | The configured key is redacted |

All statuses are tested with `en` and `zh`; JSON keys and error codes stay stable.
The fixture HTTP integration checks successful city/coordinate queries and a
missing-location response in both languages.

## Improvements and limits

The service now has a single `w-` entry, coordinate lookup, secret-safe errors,
response validation, opt-in raw output and closed HTTP responses. No automatic
retry, automatic live-key validation or cache was added. A socket timeout is
not a total-operation deadline. Real city coverage and key eligibility still
depend on the provider. Coordinate parameters follow the
[official API](https://openweathermap.org/api/current).

From the parent `mcp` directory:

```bash
python -B -m unittest -v test_weather_demo test_bilingual_tools
python -B -m unittest -v test_forecast
```

Validated on Windows/Python 3.12. Linux/macOS were not executed in this session.

## Forecast workflow and live verification

The added `get_forecast` and `get_forecast_by_coordinates` tools use the
[OpenWeather forecast API](https://openweathermap.org/forecast5), with the same key.

```text
get_forecast(location="Nanjing,CN", forecast_date="tomorrow", language="en", include_periods=false)
get_forecast_by_coordinates(latitude=32.06, longitude=118.78, forecast_date="tomorrow", language="zh")
```

Use `today`, `tomorrow`, `all` or an ISO date. Relative dates follow the provider's
location UTC offset. Summaries use 3-hour samples; they are not official daily
extrema or a daily precipitation probability. Out-of-coverage dates return an
explicit error and available dates. Raw data remains opt-in.

Live MCP verification on October 17, 2026, at approximately 15:27 UTC succeeded
in both languages using the configured real API key. For Nanjing's October 18
forecast it returned eight samples, sampled temperatures 17.04..23.64 Celsius,
light/moderate rain, maximum period precipitation probability 1.0 and maximum
sampled wind 4.92 m/s. These are a dated verification result, not a forecast that
should be reused later. The upgraded background server exposes six tools.
