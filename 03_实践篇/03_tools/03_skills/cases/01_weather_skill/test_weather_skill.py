"""Compare Skill CLI and MCP using the same local provider fixtures; no live quota."""

import asyncio
import importlib.util
import json
import os
import subprocess
import sys
import threading
import unittest
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "w-openweather/scripts/weather.py"
MCP_SCRIPT = (
    ROOT.parents[2]
    / "02_mcp/cases/01_weather-mcp-server/w-openweather_mcp_server.py"
)
NOW = datetime(2026, 10, 17, tzinfo=UTC)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


skill = load("skill_weather", SCRIPT)
mcp = load("mcp_weather_comparison", MCP_SCRIPT)


def fixture(language, forecast=False):
    current = {
        "cod": 200,
        "name": "Nanjing",
        "main": {"temp": 24, "humidity": 70},
        "weather": [{"description": "小雨" if language == "zh" else "light rain"}],
        "wind": {"speed": 2},
    }
    if not forecast:
        return current
    entries = [
        {
            **current,
            "dt": int((NOW + timedelta(hours=index * 3)).timestamp()),
            "pop": 0.4,
        }
        for index in range(40)
    ]
    return {
        "cod": "200",
        "city": {
            "name": "Nanjing",
            "country": "CN",
            "timezone": 28800,
            "coord": {"lat": 32.06, "lon": 118.78},
        },
        "list": entries,
    }


class WeatherSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Provider(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                params = parse_qs(urlsplit(self.path).query)
                location = params.get("q", [""])[0]
                status = {"missing": 404, "limited": 429}.get(location, 200)
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                data = fixture(
                    "zh" if params.get("lang") == ["zh_cn"] else "en",
                    self.path.startswith("/forecast"),
                )
                if location == "invalid":
                    self.wfile.write(b"{broken")
                else:
                    self.wfile.write(
                        json.dumps(
                            data if status == 200 else {"message": "dummy-secret"}
                        ).encode()
                    )

        cls.provider = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
        cls.thread = threading.Thread(target=cls.provider.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.provider.shutdown()
        cls.provider.server_close()
        cls.thread.join(timeout=5)

    def setUp(self):
        self.env = {
            "OPENWEATHER_API_KEY": "dummy-secret",
            "API_KEY_OPENWEATHER": "",
            "OPENWEATHER_BASE_URL": f"http://127.0.0.1:{self.provider.server_port}/weather",
            "OPENWEATHER_FORECAST_URL": f"http://127.0.0.1:{self.provider.server_port}/forecast",
        }
        for item in [
            patch.dict(os.environ, self.env),
            patch.object(skill, "utc_now", return_value=NOW),
            patch.object(mcp, "_utc_now", return_value=NOW),
        ]:
            item.start()
            self.addCleanup(item.stop)

    def cli(self, *args, environment=None):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args],
            capture_output=True,
            check=False,
            env={**os.environ, **self.env, **(environment or {})},
            timeout=20,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return result.returncode, json.loads(result.stdout.decode("utf-8"))

    def test_cli_current_and_forecast_in_both_languages(self):
        for language in ["en", "zh"]:
            code, result = self.cli(
                "current", "--location", "南京,CN", "--language", language
            )
            self.assertEqual(code, 0, result)
            self.assertEqual(
                result["weather"], "小雨" if language == "zh" else "light rain"
            )
            self.assertEqual(result["query"], "南京,CN")
            code, result = self.cli(
                "forecast",
                "--latitude",
                "32.06",
                "--longitude",
                "118.78",
                "--date",
                "2026-10-18",
                "--language",
                language,
            )
            self.assertEqual(code, 0, result)
            self.assertEqual(result["period_count"], 8)
            self.assertNotIn("periods", result)

    def test_same_fixture_same_business_result_through_mcp_dispatch(self):
        async def check():
            for language in ["en", "zh"]:
                direct = skill.run("forecast", location="Nanjing,CN", language=language)
                response = await mcp.mcp.call_tool(
                    "get_forecast",
                    {
                        "location": "Nanjing,CN",
                        "language": language,
                        "include_periods": False,
                    },
                )
                blocks = response[0] if isinstance(response, tuple) else response
                remote = json.loads(blocks[0].text)
                self.assertTrue(direct["ok"], direct)
                self.assertTrue(remote["ok"], remote)
                for field in [
                    "requested_date",
                    "location_today",
                    "period_count",
                    "timezone_offset_seconds",
                ]:
                    self.assertEqual(direct[field], remote[field])
                for field in [
                    "sampled_temperature_min_celsius",
                    "sampled_temperature_max_celsius",
                    "weather_descriptions",
                    "max_period_precipitation_probability",
                ]:
                    self.assertEqual(
                        direct["summaries"][0][field], remote["summaries"][0][field]
                    )

        asyncio.run(check())

    def test_failure_exit_codes_and_no_secret_leaks(self):
        for language in ["en", "zh"]:
            for location, expected in [
                ("missing", "location_not_found"),
                ("limited", "rate_limited"),
                ("invalid", "invalid_json"),
            ]:
                code, result = self.cli(
                    "current", "--location", location, "--language", language
                )
                self.assertEqual(code, 1)
                self.assertEqual(result["error"], expected)
                self.assertNotIn("dummy-secret", json.dumps(result))
            code, result = self.cli(
                "current",
                "--location",
                "Nanjing",
                "--language",
                language,
                environment={"OPENWEATHER_API_KEY": "", "API_KEY_OPENWEATHER": ""},
            )
            self.assertEqual(code, 1)
            self.assertEqual(result["error"], "missing_api_key")
            self.assertEqual(
                skill.run(
                    "forecast",
                    location="Nanjing",
                    forecast_date="2030-01-01",
                    language=language,
                )["error"],
                "forecast_date_unavailable",
            )

    def test_date_rollover_and_invalid_input(self):
        with patch.object(
            skill, "utc_now", return_value=datetime(2026, 10, 17, 20, tzinfo=UTC)
        ):
            result = skill.run("forecast", location="Nanjing")
            self.assertEqual(result["requested_date"], "2026-10-19")
        for language in ["en", "zh"]:
            self.assertEqual(
                skill.run("current", latitude=91, longitude=0, language=language)[
                    "error"
                ],
                "invalid_location",
            )
            self.assertEqual(
                skill.run(
                    "current",
                    location="Nanjing",
                    latitude=32,
                    longitude=118,
                    language=language,
                )["error"],
                "invalid_location",
            )
            self.assertEqual(
                skill.run(
                    "forecast",
                    location="Nanjing",
                    forecast_date="2026-02-30",
                    language=language,
                )["error"],
                "invalid_date",
            )
            payload = fixture(language, True)
            payload["city"]["timezone"] = None
            with self.assertRaises(skill.WeatherError):
                skill.forecast(payload, "tomorrow", False, language)


if __name__ == "__main__":
    unittest.main(verbosity=2)
