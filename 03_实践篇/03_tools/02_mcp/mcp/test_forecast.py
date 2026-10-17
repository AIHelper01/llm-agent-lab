"""Forecast tests with fixed clocks and a local OpenWeather fixture; no live quota."""

import asyncio
import json
import os
import threading
import unittest
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from test_weather_demo import (
    WEATHER,
    free_port,
    ready,
    response,
    server_process,
    weather,
)

NOW = datetime(2026, 10, 17, 0, tzinfo=UTC)


def forecast_fixture(language="en", offset=28800, start=NOW):
    periods = []
    for index in range(40):
        periods.append(
            {
                "dt": int((start + timedelta(hours=3 * index)).timestamp()),
                "main": {
                    "temp": 20 + index / 10,
                    "temp_min": -50,
                    "temp_max": 70,
                    "humidity": 70,
                },
                "weather": [
                    {"description": "小雨" if language == "zh" else "light rain"}
                ],
                "wind": {"speed": 2},
                "pop": 0.4,
                "rain": {"3h": 0.5},
            }
        )
    return {
        "cod": "200",
        "city": {
            "name": "Nanjing",
            "country": "CN",
            "timezone": offset,
            "coord": {"lat": 32.06, "lon": 118.78},
        },
        "list": periods,
    }


class ForecastTests(unittest.TestCase):
    def setUp(self):
        for item in [
            patch.object(
                weather,
                "_openweather_config",
                return_value=("secret-key", "https://example.invalid/weather"),
            ),
            patch.object(weather, "_utc_now", return_value=NOW),
            patch.dict(os.environ, {"OPENWEATHER_FORECAST_URL": ""}),
        ]:
            item.start()
            self.addCleanup(item.stop)

    def test_tomorrow_in_both_languages_and_sampled_extrema(self):
        for language in ["en", "zh"]:
            with patch.object(
                weather.requests,
                "get",
                return_value=response(forecast_fixture(language)),
            ) as request:
                result = weather.get_forecast("Nanjing,CN", language=language)
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["requested_date"], "2026-10-18")
            self.assertEqual(result["period_count"], 8)
            summary = result["summaries"][0]
            self.assertTrue(summary["has_eight_3h_samples"])
            self.assertGreater(summary["sampled_temperature_min_celsius"], -50)
            self.assertLess(summary["sampled_temperature_max_celsius"], 70)
            self.assertEqual(summary["max_period_precipitation_probability"], 0.4)
            self.assertIn(
                "小雨" if language == "zh" else "light rain",
                summary["weather_descriptions"],
            )
            self.assertEqual(
                request.call_args.args[0], "https://example.invalid/forecast"
            )
            self.assertEqual(
                request.call_args.kwargs["params"]["lang"],
                "zh_cn" if language == "zh" else "en",
            )
            self.assertNotIn("raw", result)

    def test_tomorrow_uses_location_date_across_utc_midnight(self):
        for language in ["en", "zh"]:
            with (
                patch.object(
                    weather,
                    "_utc_now",
                    return_value=datetime(2026, 10, 17, 20, tzinfo=UTC),
                ),
                patch.object(
                    weather.requests,
                    "get",
                    return_value=response(forecast_fixture(language)),
                ),
            ):
                result = weather.get_forecast("Nanjing,CN", language=language)
            self.assertEqual(result["location_today"], "2026-10-18")
            self.assertEqual(result["requested_date"], "2026-10-19")
            with patch.object(
                weather.requests,
                "get",
                return_value=response(forecast_fixture(language, -18000)),
            ):
                result = weather.get_forecast("Test City", language=language)
            self.assertEqual(result["location_today"], "2026-10-16")
            self.assertEqual(result["requested_date"], "2026-10-17")

    def test_all_specific_date_partial_day_and_coordinates(self):
        for language in ["en", "zh"]:
            with patch.object(
                weather.requests,
                "get",
                side_effect=lambda *args, _lang=language, **kwargs: response(
                    forecast_fixture(_lang)
                ),
            ):
                all_days = weather.get_forecast_by_coordinates(
                    32.06, 118.78, "all", language, include_periods=False
                )
                self.assertEqual(all_days["period_count"], 40)
                self.assertNotIn("periods", all_days)
                self.assertFalse(all_days["summaries"][0]["has_eight_3h_samples"])
                result = weather.get_forecast("Nanjing,CN", "2026-10-18", language)
                self.assertTrue(
                    all(
                        item["date_local"] == "2026-10-18" for item in result["periods"]
                    )
                )
                result = weather.get_forecast("Nanjing,CN", "2030-01-01", language)
                self.assertEqual(result["error"], "forecast_date_unavailable")
                self.assertIn("2026-10-18", result["available_dates"])

    def test_invalid_inputs_do_not_call_provider(self):
        with patch.object(weather.requests, "get") as request:
            for language in ["en", "zh"]:
                for value in ["bad", "2026-02-30", "20261018"]:
                    self.assertEqual(
                        weather.get_forecast("Nanjing", value, language)["error"],
                        "invalid_date",
                    )
                self.assertEqual(
                    weather.get_forecast("", language=language)["error"],
                    "invalid_location",
                )
                self.assertEqual(
                    weather.get_forecast_by_coordinates(91, 0, language=language)[
                        "error"
                    ],
                    "invalid_coordinates",
                )
            request.assert_not_called()

    def test_invalid_payloads_and_missing_timezone(self):
        bad_items = []
        for key, value in [("list", []), ("list", [None]), ("city", {})]:
            bad_items.append({**forecast_fixture(), key: value})
        for invalid in [None, 100000, "28800"]:
            value = forecast_fixture()
            value["city"]["timezone"] = invalid
            bad_items.append(value)
        for key, value in [
            ("pop", 2),
            ("dt", 10**30),
            ("wind", []),
            ("rain", {"3h": -1}),
        ]:
            item = forecast_fixture()
            item["list"][0][key] = value
            bad_items.append(item)
        item = forecast_fixture()
        item["list"][1]["dt"] = item["list"][0]["dt"]
        bad_items.append(item)
        for language in ["en", "zh"]:
            for payload in bad_items:
                with patch.object(
                    weather.requests, "get", return_value=response(payload)
                ):
                    result = weather.get_forecast("Nanjing", language=language)
                self.assertEqual(result["error"], "invalid_response", result)

    def test_shared_errors_secrets_and_explicit_endpoint(self):
        for language in ["en", "zh"]:
            for status, expected in [
                (401, "invalid_api_key"),
                (429, "rate_limited"),
                (500, "provider_unavailable"),
            ]:
                with patch.object(
                    weather.requests,
                    "get",
                    return_value=response({"message": "secret-key"}, status),
                ):
                    result = weather.get_forecast("Nanjing", language=language)
                self.assertEqual(result["error"], expected)
                self.assertNotIn("secret-key", json.dumps(result))
            payload = forecast_fixture(language)
            payload["debug"] = "secret-key"
            with (
                patch.dict(
                    os.environ,
                    {"OPENWEATHER_FORECAST_URL": "https://proxy.invalid/custom"},
                ),
                patch.object(
                    weather.requests, "get", return_value=response(payload)
                ) as request,
            ):
                result = weather.get_forecast(
                    "Nanjing", language=language, include_raw=True
                )
                self.assertEqual(
                    request.call_args.args[0], "https://proxy.invalid/custom"
                )
                self.assertEqual(result["raw"]["debug"], "[redacted]")


class ForecastHttpTests(unittest.TestCase):
    def test_real_mcp_forecast_dispatch_with_local_provider(self):
        class Provider(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                params = parse_qs(urlsplit(self.path).query)
                payload = forecast_fixture(
                    "zh" if params.get("lang") == ["zh_cn"] else "en"
                )
                self.wfile.write(json.dumps(payload).encode())

        provider = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
        thread = threading.Thread(target=provider.serve_forever, daemon=True)
        thread.start()
        port = free_port()
        environment = {
            "WEATHER_MCP_HOST": "127.0.0.1",
            "WEATHER_MCP_PORT": str(port),
            "OPENWEATHER_API_KEY": "offline-key",
            "OPENWEATHER_BASE_URL": f"http://127.0.0.1:{provider.server_port}/weather",
            "OPENWEATHER_FORECAST_URL": f"http://127.0.0.1:{provider.server_port}/forecast",
        }

        async def check(process):
            url = f"http://127.0.0.1:{port}/mcp"
            await ready(url, process)
            async with (
                streamable_http_client(url) as (read, write, _),
                ClientSession(read, write) as session,
            ):
                await session.initialize()
                names = {item.name for item in (await session.list_tools()).tools}
                self.assertTrue(
                    {"get_forecast", "get_forecast_by_coordinates"} <= names
                )
                for language in ["en", "zh"]:
                    for name, arguments in [
                        ("get_forecast", {"location": "Nanjing,CN"}),
                        (
                            "get_forecast_by_coordinates",
                            {"latitude": 32.06, "longitude": 118.78},
                        ),
                    ]:
                        result = await session.call_tool(
                            name,
                            {
                                **arguments,
                                "forecast_date": "2026-10-18",
                                "language": language,
                            },
                        )
                        self.assertFalse(result.isError)
                        payload = json.loads(result.content[0].text)
                        self.assertTrue(payload["ok"], payload)
                        self.assertEqual(payload["period_count"], 8)
                        self.assertIn(
                            "小雨" if language == "zh" else "light rain",
                            payload["summaries"][0]["weather_descriptions"],
                        )

        try:
            with server_process(WEATHER, environment) as process:
                asyncio.run(check(process))
        finally:
            provider.shutdown()
            provider.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
