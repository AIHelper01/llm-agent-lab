"""Standalone Skill CLI: OpenWeather directly, with no MCP imports or service."""

import argparse
import json
import math
import os
import sys
from datetime import UTC, date, datetime, timedelta, timezone
from itertools import pairwise
from urllib.parse import urlsplit

import requests
from dotenv import find_dotenv, load_dotenv

MESSAGES = {
    "invalid_location": (
        "Provide a city, or both valid coordinates.",
        "请提供城市名或完整有效的经纬度。",
    ),
    "invalid_date": (
        "Use today, tomorrow, all or YYYY-MM-DD.",
        "请使用 today、tomorrow、all 或 YYYY-MM-DD。",
    ),
    "missing_api_key": (
        "Configure OPENWEATHER_API_KEY in the execution environment.",
        "请在脚本运行环境配置 OPENWEATHER_API_KEY。",
    ),
    "invalid_config": (
        "Configure a valid HTTP(S) endpoint without credentials or query parameters.",
        "请配置不含账号密码或查询参数的有效 HTTP(S) 接口。",
    ),
    "timeout": ("The OpenWeather request timed out.", "OpenWeather 请求超时。"),
    "request_failed": ("Could not connect to OpenWeather.", "无法连接 OpenWeather。"),
    "invalid_api_key": (
        "OpenWeather rejected the API key.",
        "OpenWeather 拒绝了 API key。",
    ),
    "access_denied": ("OpenWeather denied access.", "OpenWeather 拒绝访问。"),
    "location_not_found": ("Location not found.", "未找到地点。"),
    "rate_limited": (
        "OpenWeather rate limit reached; retry later.",
        "OpenWeather 请求超限，请稍后重试。",
    ),
    "provider_unavailable": ("OpenWeather is unavailable.", "OpenWeather 暂时不可用。"),
    "openweather_error": (
        "OpenWeather rejected the request.",
        "OpenWeather 拒绝了请求。",
    ),
    "invalid_json": ("The provider returned invalid JSON.", "服务商返回了无效 JSON。"),
    "invalid_response": (
        "The provider returned invalid weather data.",
        "服务商返回了无效天气数据。",
    ),
    "forecast_date_unavailable": (
        "The forecast does not cover the requested local date.",
        "预报未覆盖请求的地点当地日期。",
    ),
}


class WeatherError(Exception):
    def __init__(self, code, **details):
        super().__init__(code)
        self.code, self.details = code, details


def number(value):
    try:
        return (
            isinstance(value, (float, int))
            and not isinstance(value, bool)
            and math.isfinite(value)
        )
    except OverflowError:
        return False


def utc_now():
    return datetime.now(UTC)


def redact(value, secret):
    if isinstance(value, str):
        return value.replace(secret, "[redacted]")
    if isinstance(value, list):
        return [redact(item, secret) for item in value]
    if isinstance(value, dict):
        return {
            redact(key, secret): redact(item, secret) for key, item in value.items()
        }
    return value


def fields(entry):
    main, conditions, wind = (
        entry.get("main"),
        entry.get("weather"),
        entry.get("wind", {}),
    )
    if (
        not isinstance(main, dict)
        or not number(main.get("temp"))
        or not isinstance(conditions, list)
        or not conditions
        or not isinstance(conditions[0], dict)
        or not isinstance(conditions[0].get("description"), str)
        or not isinstance(wind, dict)
    ):
        raise WeatherError("invalid_response")
    result = {
        "temperature_celsius": main["temp"],
        "weather": conditions[0]["description"],
        "feels_like_celsius": main.get("feels_like"),
        "humidity_percent": main.get("humidity"),
        "wind_speed_mps": wind.get("speed"),
        "wind_direction_degrees": wind.get("deg"),
    }
    if any(
        value is not None and not number(value)
        for key, value in result.items()
        if key != "weather"
    ):
        raise WeatherError("invalid_response")
    return result


def forecast(data, requested, include_periods, language):
    city, entries = data.get("city"), data.get("list")
    if (
        not isinstance(city, dict)
        or not isinstance(entries, list)
        or not 1 <= len(entries) <= 40
    ):
        raise WeatherError("invalid_response")
    offset = city.get("timezone")
    if type(offset) is not int or not -86399 <= offset <= 86399:
        raise WeatherError("invalid_response")
    zone = timezone(timedelta(seconds=offset))
    today = utc_now().astimezone(zone).date()
    target = (
        today
        if requested == "today"
        else today + timedelta(days=1)
        if requested == "tomorrow"
        else None
        if requested == "all"
        else date.fromisoformat(requested)
    )
    periods, seen = [], set()
    for entry in entries:
        if (
            not isinstance(entry, dict)
            or type(entry.get("dt")) is not int
            or entry["dt"] in seen
        ):
            raise WeatherError("invalid_response")
        seen.add(entry["dt"])
        try:
            local = datetime.fromtimestamp(entry["dt"], UTC).astimezone(zone)
        except (OSError, OverflowError, ValueError):
            raise WeatherError("invalid_response") from None
        probability = entry.get("pop")
        if probability is not None and (
            not number(probability) or not 0 <= probability <= 1
        ):
            raise WeatherError("invalid_response")
        periods.append(
            {
                "timestamp_unix": entry["dt"],
                "time_local": local.isoformat(),
                "date_local": local.date().isoformat(),
                "precipitation_probability": probability,
                **fields(entry),
            }
        )
    periods.sort(key=lambda item: item["timestamp_unix"])
    available = sorted({item["date_local"] for item in periods})
    selected = [
        item
        for item in periods
        if target is None or item["date_local"] == target.isoformat()
    ]
    if not selected:
        raise WeatherError(
            "forecast_date_unavailable",
            requested_date=target.isoformat(),
            available_dates=available,
        )
    summaries = []
    for day in sorted({item["date_local"] for item in selected}):
        samples = [item for item in selected if item["date_local"] == day]
        probabilities = [
            item["precipitation_probability"]
            for item in samples
            if item["precipitation_probability"] is not None
        ]
        speeds = [
            item["wind_speed_mps"]
            for item in samples
            if item["wind_speed_mps"] is not None
        ]
        summaries.append(
            {
                "date_local": day,
                "period_count": len(samples),
                "has_eight_3h_samples": len(samples) == 8
                and all(
                    b["timestamp_unix"] - a["timestamp_unix"] == 10800
                    for a, b in pairwise(samples)
                ),
                "sampled_temperature_min_celsius": min(
                    item["temperature_celsius"] for item in samples
                ),
                "sampled_temperature_max_celsius": max(
                    item["temperature_celsius"] for item in samples
                ),
                "weather_descriptions": list(
                    dict.fromkeys(item["weather"] for item in samples)
                ),
                "max_period_precipitation_probability": max(probabilities)
                if probabilities
                else None,
                "max_sampled_wind_speed_mps": max(speeds) if speeds else None,
            }
        )
    result = {
        "city": city.get("name"),
        "country": city.get("country"),
        "requested_date": target.isoformat() if target else None,
        "location_today": today.isoformat(),
        "timezone_offset_seconds": offset,
        "forecast_interval_hours": 3,
        "period_count": len(selected),
        "available_dates": available,
        "summaries": summaries,
        "summary_note": "Summaries use 3-hour samples, not official daily extrema or daily rain probability."
        if language == "en"
        else "汇总基于 3 小时采样，不是官方全天极值或全天降水概率。",
    }
    if include_periods:
        result["periods"] = selected
    return result


def run(
    mode,
    location="",
    latitude=None,
    longitude=None,
    forecast_date="tomorrow",
    language="en",
    include_periods=False,
):
    try:
        if mode not in {"current", "forecast"} or language not in {"en", "zh"}:
            raise WeatherError("invalid_config")
        location = location.strip()
        if location:
            if len(location) > 200 or latitude is not None or longitude is not None:
                raise WeatherError("invalid_location")
            params, query = {"q": location}, location
        elif (
            number(latitude)
            and number(longitude)
            and -90 <= latitude <= 90
            and -180 <= longitude <= 180
        ):
            params, query = (
                {"lat": latitude, "lon": longitude},
                {"latitude": latitude, "longitude": longitude},
            )
        else:
            raise WeatherError("invalid_location")
        if mode == "forecast" and forecast_date not in {"today", "tomorrow", "all"}:
            try:
                if date.fromisoformat(forecast_date).isoformat() != forecast_date:
                    raise ValueError
            except ValueError:
                raise WeatherError("invalid_date") from None
        key = (
            os.getenv("OPENWEATHER_API_KEY") or os.getenv("API_KEY_OPENWEATHER") or ""
        ).strip()
        if not key:
            raise WeatherError("missing_api_key")
        endpoint = (
            os.getenv("OPENWEATHER_BASE_URL")
            or os.getenv("BASE_URL_OPENWEATHER")
            or "https://api.openweathermap.org/data/2.5/weather"
        ).strip()
        if mode == "forecast":
            configured = os.getenv("OPENWEATHER_FORECAST_URL", "").strip()
            endpoint = configured or (
                endpoint[:-7] + "forecast" if endpoint.endswith("/weather") else ""
            )
        try:
            parts = urlsplit(endpoint)
            if (
                parts.scheme not in {"http", "https"}
                or not parts.hostname
                or parts.username
                or parts.password
                or parts.query
                or parts.fragment
            ):
                raise ValueError
        except ValueError:
            raise WeatherError("invalid_config") from None
        try:
            timeout = max(1, int(os.getenv("WEATHER_MCP_TIMEOUT_SECONDS", "10")))
        except ValueError:
            timeout = 10
        try:
            with requests.get(
                endpoint,
                params={
                    **params,
                    "appid": key,
                    "units": "metric",
                    "lang": "zh_cn" if language == "zh" else "en",
                },
                timeout=timeout,
                allow_redirects=False,
            ) as response:
                status = response.status_code
                if status != 200:
                    raise WeatherError(
                        {
                            401: "invalid_api_key",
                            403: "access_denied",
                            404: "location_not_found",
                            429: "rate_limited",
                        }.get(
                            status,
                            "provider_unavailable"
                            if status >= 500
                            else "openweather_error",
                        )
                    )
                try:
                    data = response.json()
                except ValueError:
                    raise WeatherError("invalid_json") from None
        except requests.Timeout:
            raise WeatherError("timeout") from None
        except requests.RequestException:
            raise WeatherError("request_failed") from None
        if not isinstance(data, dict):
            raise WeatherError("invalid_response")
        if str(data.get("cod")) != "200":
            raise WeatherError("openweather_error")
        if mode == "forecast":
            result = forecast(data, forecast_date, include_periods, language)
        else:
            if data.get("dt") is not None and type(data["dt"]) is not int:
                raise WeatherError("invalid_response")
            result = {
                "city": data.get("name"),
                "updated_at_unix": data.get("dt"),
                **fields(data),
            }
        return redact({"ok": True, "query": query, **result}, key)
    except WeatherError as error:
        return {
            "ok": False,
            "error": error.code,
            "message": MESSAGES[error.code][language == "zh"],
            **error.details,
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["current", "forecast"])
    parser.add_argument("--location", default="")
    parser.add_argument("--latitude", type=float)
    parser.add_argument("--longitude", type=float)
    parser.add_argument("--date", default="tomorrow", dest="forecast_date")
    parser.add_argument("--language", choices=["en", "zh"], default="en")
    parser.add_argument("--include-periods", action="store_true")
    args = vars(parser.parse_args(argv))
    load_dotenv(find_dotenv(usecwd=True))
    result = run(**args)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
