"""Offline reliability and bilingual protocol tests. No live weather requests."""

import asyncio
import importlib.util
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import httpx
import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parent
WEATHER = ROOT / "01_weather-mcp-server/w-openweather_mcp_server.py"
DEMO = ROOT / "00_mcp-server-demo/w-mcp_demo_server.py"
CLOCK = ROOT / "00_mcp-server-demo/w-time_mcp_server.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


weather = load("weather_review", WEATHER)
demo = load("demo_review", DEMO)
clock = load("clock_review", CLOCK)


def fixture(description="clear sky"):
    return {
        "cod": 200,
        "name": "Test City",
        "weather": [{"main": "Clear", "description": description}],
        "main": {"temp": 20, "humidity": 50},
        "coord": {"lat": 39.9, "lon": 116.4},
    }


def response(data=None, status=200, raw=None, headers=None):
    value = requests.Response()
    value.status_code = status
    value.url = "https://example.invalid/weather?appid=secret-key"
    value._content = json.dumps(data).encode("utf-8") if raw is None else raw
    value._content_consumed = True
    value.headers.update(headers or {})
    return value


class WeatherTests(unittest.TestCase):
    def setUp(self):
        config = patch.object(
            weather,
            "_openweather_config",
            return_value=("secret-key", "https://example.invalid/weather"),
        )
        config.start()
        self.addCleanup(config.stop)

    def test_provider_http_errors_localized_and_redacted(self):
        expected = {
            401: "invalid_api_key",
            403: "access_denied",
            404: "location_not_found",
            429: "rate_limited",
            500: "provider_unavailable",
            302: "openweather_error",
        }
        for language in ["en", "zh"]:
            for status, code in expected.items():
                with patch.object(
                    weather.requests,
                    "get",
                    return_value=response(
                        {"message": "secret-key"}, status, headers={"Retry-After": "12"}
                    ),
                ):
                    result = weather.get_weather("London", language)
                self.assertEqual(result["error"], code)
                self.assertNotIn("secret-key", json.dumps(result))
                self.assertTrue(
                    any(ord(c) > 127 for c in result["message"])
                    if language == "zh"
                    else result["message"].isascii()
                )
                if status == 429:
                    self.assertEqual(result["retry_after_seconds"], 12)

    def test_invalid_json_and_response_shapes(self):
        for language in ["en", "zh"]:
            with patch.object(
                weather.requests, "get", return_value=response(raw=b"{bad")
            ):
                self.assertEqual(
                    weather.get_weather("London", language)["error"], "invalid_json"
                )
            for data in [
                None,
                [],
                {"cod": 200},
                {**fixture(), "weather": []},
                {**fixture(), "wind": []},
                {**fixture(), "main": {"temp": float("nan")}},
                {**fixture(), "main": {"temp": 10**1000}},
                {**fixture(), "wind": {"speed": float("inf")}},
                {**fixture(), "coord": {"lat": "not a number"}},
            ]:
                with patch.object(weather.requests, "get", return_value=response(data)):
                    self.assertEqual(
                        weather.get_weather("London", language)["error"],
                        "invalid_response",
                    )

    def test_network_errors_do_not_echo_request_urls(self):
        for language in ["en", "zh"]:
            for exception, code in [
                (
                    requests.ConnectionError(
                        "https://example.invalid?appid=secret-key"
                    ),
                    "request_failed",
                ),
                (requests.Timeout("secret-key"), "timeout"),
            ]:
                with patch.object(weather.requests, "get", side_effect=exception):
                    result = weather.get_weather("London", language)
                self.assertEqual(result["error"], code)
                self.assertNotIn("secret-key", json.dumps(result))

    def test_coordinates_languages_and_opt_in_raw(self):
        for language in ["en", "zh"]:
            data = fixture("晴" if language == "zh" else "clear sky")
            data["debug"] = "secret-key"
            with patch.object(
                weather.requests,
                "get",
                side_effect=lambda *args, _data=data, **kwargs: response(_data),
            ) as request:
                result = weather.get_weather_by_coordinates(39.9, 116.4, language)
                self.assertTrue(result["ok"], result)
                self.assertNotIn("raw", result)
                params = request.call_args.kwargs["params"]
                self.assertEqual((params["lat"], params["lon"]), (39.9, 116.4))
                self.assertEqual(params["lang"], "zh_cn" if language == "zh" else "en")
                self.assertFalse(request.call_args.kwargs["allow_redirects"])
                result = weather.get_weather("北京", language, include_raw=True)
                self.assertEqual(result["raw"]["debug"], "[redacted]")
                self.assertEqual(result["query"], "北京")

    def test_invalid_inputs_never_make_a_request(self):
        with patch.object(weather.requests, "get") as request:
            for language in ["en", "zh"]:
                self.assertEqual(
                    weather.get_weather("", language)["error"], "invalid_location"
                )
                self.assertEqual(
                    weather.get_weather("a" * 201, language)["error"],
                    "invalid_location",
                )
                for lat, lon in [
                    (91, 0),
                    (0, 181),
                    (float("nan"), 0),
                    (0, float("inf")),
                ]:
                    self.assertEqual(
                        weather.get_weather_by_coordinates(lat, lon, language)["error"],
                        "invalid_coordinates",
                    )
            request.assert_not_called()

    def test_config_diagnostics_and_missing_key(self):
        for language in ["en", "zh"]:
            with patch.object(
                weather,
                "_openweather_config",
                return_value=(None, "https://example.invalid/weather"),
            ):
                self.assertFalse(weather.check_config(language)["ok"])
                self.assertEqual(
                    weather.get_weather("London", language)["error"], "missing_api_key"
                )
            with patch.object(
                weather,
                "_openweather_config",
                return_value=(
                    "secret-key",
                    "https://user:secret-key@example.invalid/weather?appid=secret-key",
                ),
            ):
                self.assertFalse(weather.check_config(language)["ok"])
                self.assertNotIn(
                    "secret-key", json.dumps(weather.check_config(language))
                )
                self.assertNotIn("secret-key", json.dumps(weather.ping()))
                self.assertEqual(
                    weather.get_weather("London", language)["error"], "invalid_config"
                )


class DemoTimeTests(unittest.TestCase):
    def test_greeting_validation_and_language(self):
        for language in ["en", "zh"]:
            self.assertIn("Alice", demo.get_localized_greeting("Alice", language))
            for invalid in [" ", "x" * 201]:
                with self.assertRaises(ValueError):
                    demo.get_localized_greeting(invalid, language)
                with self.assertRaises(ValueError):
                    demo.greet_user(invalid, language=language)
        self.assertEqual(demo.add(-4, 8), 4)
        self.assertEqual(
            demo.greet_user("Alice", "unknown"), demo.greet_user("Alice", "friendly")
        )
        self.assertEqual(demo.ping()["server"], "w-MCPDemo")

    def test_aware_current_time_and_conversion(self):
        for language in ["en", "zh"]:
            utc = clock.get_current_time("UTC", language)
            self.assertTrue(utc["ok"])
            self.assertEqual(utc["utc_offset_seconds"], 0)
            shanghai = clock.get_current_time("Asia/Shanghai", language)
            self.assertEqual(shanghai["utc_offset_seconds"], 28800)
            value = clock.convert_time("2026-10-17T12:00:00+08:00", language=language)
            self.assertEqual(value["target_iso8601"], "2026-10-17T04:00:00+00:00")
            value = clock.convert_time(
                "2026-10-17T12:00:00", from_timezone="Asia/Shanghai", language=language
            )
            self.assertEqual(value["target_iso8601"], "2026-10-17T04:00:00+00:00")

    def test_time_errors_and_daylight_saving_boundaries(self):
        for language in ["en", "zh"]:
            self.assertEqual(
                clock.get_current_time("invalid/timezone", language)["error"],
                "invalid_timezone",
            )
            for value, kwargs, code in [
                ("bad", {}, "invalid_time"),
                ("2026-10-17T12:00:00", {}, "timezone_required"),
                (
                    "2026-10-17T12:00:00Z",
                    {"from_timezone": "UTC"},
                    "conflicting_timezone",
                ),
                (
                    "2026-11-01T01:30:00",
                    {"from_timezone": "America/New_York"},
                    "ambiguous_time",
                ),
                (
                    "2026-03-08T02:30:00",
                    {"from_timezone": "America/New_York"},
                    "nonexistent_time",
                ),
            ]:
                self.assertEqual(
                    clock.convert_time(value, language=language, **kwargs)["error"],
                    code,
                )


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@contextmanager
def server_process(script, environment):
    with tempfile.TemporaryFile() as log:
        process = subprocess.Popen(
            [sys.executable, "-B", str(script)],
            env={**os.environ, **environment},
            stdout=log,
            stderr=log,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        try:
            yield process
        except Exception:
            log.seek(0)
            print(log.read().decode("utf-8", errors="replace"))
            raise
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


async def ready(url, process):
    async with httpx.AsyncClient() as client:
        for _ in range(200):
            if process.poll() is not None:
                raise AssertionError("Server exited at startup")
            try:
                await client.get(url, timeout=0.2)
                return
            except httpx.TransportError:
                await asyncio.sleep(0.05)
    raise AssertionError("Server startup timed out")


class ProtocolTests(unittest.TestCase):
    def test_weather_http_with_local_provider(self):
        class Provider(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                params = parse_qs(urlsplit(self.path).query)
                missing = params.get("q") == ["missing"]
                self.send_response(404 if missing else 200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                data = (
                    {"cod": 404}
                    if missing
                    else fixture(
                        "晴" if params.get("lang") == ["zh_cn"] else "clear sky"
                    )
                )
                self.wfile.write(json.dumps(data).encode())

        provider = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
        thread = threading.Thread(target=provider.serve_forever, daemon=True)
        thread.start()
        port = free_port()
        env = {
            "WEATHER_MCP_HOST": "127.0.0.1",
            "WEATHER_MCP_PORT": str(port),
            "OPENWEATHER_API_KEY": "offline-test-key",
            "OPENWEATHER_BASE_URL": f"http://127.0.0.1:{provider.server_port}/weather",
        }

        async def check(process):
            url = f"http://127.0.0.1:{port}/mcp"
            await ready(url, process)
            async with (
                streamable_http_client(url) as (read, write, _),
                ClientSession(read, write) as session,
            ):
                initialized = await session.initialize()
                self.assertEqual(initialized.serverInfo.name, "w-OpenWeatherMCP")
                for language in ["en", "zh"]:
                    for name, arguments in [
                        ("get_weather", {"location": "北京"}),
                        (
                            "get_weather_by_coordinates",
                            {"latitude": 39.9, "longitude": 116.4},
                        ),
                    ]:
                        result = await session.call_tool(
                            name, {**arguments, "language": language}
                        )
                        self.assertFalse(result.isError)
                        data = json.loads(result.content[0].text)
                        self.assertTrue(data["ok"], data)
                        self.assertEqual(
                            data["weather"], "晴" if language == "zh" else "clear sky"
                        )
                    result = await session.call_tool(
                        "get_weather", {"location": "missing", "language": language}
                    )
                    self.assertEqual(
                        json.loads(result.content[0].text)["error"],
                        "location_not_found",
                    )

        try:
            with server_process(WEATHER, env) as process:
                asyncio.run(check(process))
        finally:
            provider.shutdown()
            provider.server_close()
            thread.join(timeout=5)

    def test_demo_http_tools_resources_prompts(self):
        port = free_port()

        async def check(process):
            url = f"http://127.0.0.1:{port}/mcp"
            await ready(url, process)
            async with (
                streamable_http_client(url) as (read, write, _),
                ClientSession(read, write) as session,
            ):
                initialized = await session.initialize()
                self.assertEqual(initialized.serverInfo.name, "w-MCPDemo")
                result = await session.call_tool("add", {"a": -1, "b": 5})
                self.assertEqual(json.loads(result.content[0].text), 4)
                for language in ["en", "zh"]:
                    result = await session.read_resource(f"greeting://Alice/{language}")
                    self.assertIn(
                        "你好" if language == "zh" else "Hello", result.contents[0].text
                    )
                    result = await session.get_prompt(
                        "greet_user", {"name": "Alice", "language": language}
                    )
                    self.assertIn(
                        "请写" if language == "zh" else "Please write",
                        result.messages[0].content.text,
                    )

        with server_process(
            DEMO, {"DEMO_MCP_HOST": "127.0.0.1", "DEMO_MCP_PORT": str(port)}
        ) as process:
            asyncio.run(check(process))

    def test_clock_stdio_protocol_in_both_languages(self):
        async def check():
            parameters = StdioServerParameters(
                command=sys.executable, args=["-B", str(CLOCK)]
            )
            async with (
                stdio_client(parameters) as (read, write),
                ClientSession(read, write) as session,
            ):
                initialized = await session.initialize()
                self.assertEqual(initialized.serverInfo.name, "w-TimeMCP")
                for language in ["en", "zh"]:
                    result = await session.call_tool(
                        "get_current_time",
                        {"timezone_name": "Asia/Shanghai", "language": language},
                    )
                    data = json.loads(result.content[0].text)
                    self.assertTrue(data["ok"])
                    self.assertEqual(data["utc_offset_seconds"], 28800)
                    result = await session.call_tool(
                        "convert_time",
                        {"iso_time": "2026-10-17T12:00:00+08:00", "language": language},
                    )
                    self.assertEqual(
                        json.loads(result.content[0].text)["target_iso8601"],
                        "2026-10-17T04:00:00+00:00",
                    )

        asyncio.run(check())


if __name__ == "__main__":
    unittest.main(verbosity=2)
