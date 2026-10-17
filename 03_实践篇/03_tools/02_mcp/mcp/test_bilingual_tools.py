"""Offline bilingual regression checks. Run: python -B test_bilingual_tools.py."""

import asyncio
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

from mcp.server.fastmcp.exceptions import ToolError


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


files = load_module("bilingual_files", "02_file-mcp-server/w-file_workbench_mcp_server.py")
weather = load_module(
    "bilingual_weather", "01_weather-mcp-server/w-openweather_mcp_server.py"
)
demo = load_module("bilingual_demo", "00_mcp-server-demo/w-mcp_demo_server.py")
clock = load_module("bilingual_clock", "00_mcp-server-demo/w-time_mcp_server.py")


class BilingualToolsTests(unittest.TestCase):
    def test_file_round_trip_and_restore_in_both_languages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(files, "HISTORY_FILE", root / "history.json"):
                for language, folder in [("en", "notes"), ("zh", "资料")]:
                    with self.subTest(language=language):
                        path = root / folder / "会议 meeting.txt"
                        created = files.create_file(
                            str(path), "Hello / 你好 🌍", language=language
                        )
                        self.assertTrue(created["ok"])
                        self.assertEqual(
                            created["message"],
                            "文件创建成功"
                            if language == "zh"
                            else "File created successfully",
                        )
                        self.assertEqual(
                            files.read_file(str(path))["content"], "Hello / 你好 🌍"
                        )
                        self.assertEqual(
                            files.list_files(str(path.parent))["items"][0]["name"],
                            path.name,
                        )
                        self.assertEqual(
                            files.get_file_info(str(path))["info"]["name"], path.name
                        )
                        renamed = files.rename_file(
                            str(path), "renamed 已改名.txt", language=language
                        )
                        self.assertTrue(renamed["ok"])
                        self.assertEqual(
                            files.view_rename_history(str(path.parent))["count"], 1
                        )
                        self.assertTrue(
                            files.restore_last_rename(
                                str(path.parent), language=language
                            )["ok"]
                        )
                        self.assertEqual(
                            path.read_text(encoding="utf-8"), "Hello / 你好 🌍"
                        )
                        self.assertEqual(files.view_rename_history()["count"], 0)

    def test_english_default_and_stable_error_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.txt")
            english = files.read_file(missing)
            chinese = files.read_file(missing, language="zh")
            self.assertEqual(english["error"], chinese["error"])
            self.assertEqual(english["error"], "not_found")
            self.assertTrue(english["message"].startswith("File not found:"))
            self.assertTrue(chinese["message"].startswith("文件不存在:"))
            self.assertTrue(
                files.list_allowed_roots()["message"].startswith("This server")
            )
            self.assertIn("本 MCP", files.list_allowed_roots(language="zh")["message"])
            for name in ["CON.txt", "../other.txt", "bad?.txt", ""]:
                self.assertIsNotNone(files._validate_new_filename(name))
                self.assertIsNotNone(files._validate_new_filename(name, "zh"))
            self.assertIsNone(files._validate_new_filename("会议 meeting.txt"))
            with patch.object(files.platform, "system", return_value="Linux"):
                self.assertIn(
                    "Windows absolute path", files._resolve_path("E:/资料")[1]
                )
                self.assertIn(
                    "Windows 绝对路径", files._resolve_path("E:/资料", language="zh")[1]
                )

    def test_no_overwrite_and_localized_directory_messages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(
                files.create_directory(str(root / "资料"))["message"],
                "Directory created successfully",
            )
            self.assertEqual(
                files.create_directory(str(root / "资料"), language="zh")["message"],
                "目录已存在",
            )
            path = str(root / "notes.txt")
            files.create_file(path, "original 原文")
            self.assertEqual(
                files.create_file(path, "replacement")["error"], "target_exists"
            )
            self.assertEqual(Path(path).read_text(encoding="utf-8"), "original 原文")
            self.assertTrue(
                files.create_file(path, "new 新内容", overwrite=True, language="zh")[
                    "ok"
                ]
            )

    def test_multibyte_encodings_and_truncation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "中文.txt"
            for encoding, content, limit, expected in [
                ("utf-8", "Hello 中文", 8, "Hello "),
                ("utf-8", "中文", 4, "中"),
                ("utf-8", "🌍你好", 5, "🌍"),
                ("gb18030", "中文记录", 3, "中"),
            ]:
                with self.subTest(encoding=encoding, limit=limit):
                    path.write_bytes(content.encode(encoding))
                    with patch.dict(
                        files.os.environ, {"FILE_MCP_MAX_READ_BYTES": str(limit)}
                    ):
                        result = files.read_file(str(path))
                    self.assertTrue(result["ok"])
                    self.assertTrue(result["truncated"])
                    self.assertEqual(result["encoding"], encoding)
                    self.assertEqual(result["content"], expected)
            path.write_bytes("中文记录".encode("gb18030"))
            self.assertEqual(files.read_file(str(path))["content"], "中文记录")

    def test_weather_language_and_unmodified_city_input(self):
        with patch.object(
            weather,
            "_openweather_config",
            return_value=("test-key", "https://example.invalid/weather"),
        ):
            for city, language in [
                ("London,GB", "en"),
                ("北京", "en"),
                ("北京", "zh"),
                ("Beijing,CN", "zh"),
            ]:
                with self.subTest(city=city, language=language):
                    description = "晴" if language == "zh" else "clear sky"
                    data = {
                        "cod": 200,
                        "name": city,
                        "weather": [{"description": description}],
                        "main": {"temp": 20},
                    }
                    with patch.object(
                        weather.requests, "get", return_value=Mock(json=lambda: data)
                    ) as request:
                        result = (
                            weather.get_weather(city, include_raw=True)
                            if language == "en"
                            else weather.get_weather(city, language="zh", include_raw=True)
                        )
                    self.assertEqual(request.call_args.kwargs["params"]["q"], city)
                    self.assertEqual(
                        request.call_args.kwargs["params"]["lang"],
                        "zh_cn" if language == "zh" else "en",
                    )
                    self.assertEqual(result["query"], city)
                    self.assertEqual(result["weather"], description)
                    self.assertEqual(result["raw"], data)
            self.assertEqual(
                weather.check_config()["message"], "OpenWeather configuration loaded."
            )
            self.assertEqual(
                weather.check_config("zh")["message"], "OpenWeather 配置已加载。"
            )

    def test_weather_errors_are_localized_without_network_calls(self):
        with patch.object(weather.requests, "get") as request:
            self.assertEqual(
                weather.get_weather("")["message"],
                "Provide a city name, for example London or Beijing.",
            )
            self.assertIn("请传入", weather.get_weather("", "zh")["message"])
            with patch.object(
                weather, "_openweather_config", return_value=(None, "unused")
            ):
                self.assertEqual(weather.check_config()["has_api_key"], False)
                self.assertIn("Missing", weather.check_config()["message"])
                self.assertEqual(
                    weather.get_weather("London")["error"], "missing_api_key"
                )
                self.assertIn("请在", weather.get_weather("北京", "zh")["message"])
            request.assert_not_called()
        with patch.object(
            weather, "_openweather_config", return_value=("test-key", "https://example.invalid/weather")
        ):
            for language in ["en", "zh"]:
                with patch.object(
                    weather.requests, "get", side_effect=weather.requests.Timeout
                ):
                    result = weather.get_weather("London", language)
                    self.assertEqual(result["error"], "timeout")
                    self.assertIn(
                        "超时" if language == "zh" else "timed out", result["message"]
                    )

    def test_demo_and_mcp_contracts(self):
        self.assertEqual(demo.add(2, 3), 5)
        self.assertEqual(demo.get_greeting("小明"), "Hello, 小明!")
        self.assertEqual(demo.get_localized_greeting("Alice", "zh"), "你好，Alice！")
        self.assertIn("Please write", demo.greet_user("小明"))
        self.assertIn("请写", demo.greet_user("Alice", language="zh"))
        self.assertRegex(
            clock.get_current_time()["current_time"],
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
        )

        async def check_contracts():
            for server in [files.mcp, weather.mcp]:
                tools = await server.list_tools()
                for tool in tools:
                    if tool.name == "ping":
                        continue
                    schema = tool.inputSchema
                    self.assertEqual(schema["properties"]["language"]["default"], "en")
                    self.assertEqual(
                        schema["properties"]["language"]["enum"], ["en", "zh"]
                    )
                    self.assertNotIn("language", schema.get("required", []))
            # Exercise dispatch and serialization, not only direct Python calls.
            for language in ["en", "zh"]:
                result = await weather.mcp.call_tool(
                    "get_weather", {"location": "", "language": language}
                )
                content = result[0] if isinstance(result, tuple) else result
                payload = json.loads(content[0].text)
                self.assertFalse(payload["ok"])
                self.assertIn(
                    "请传入" if language == "zh" else "Provide", payload["message"]
                )
            with self.assertRaises(ToolError):
                await weather.mcp.call_tool(
                    "get_weather", {"location": "", "language": "fr"}
                )
            prompt = await demo.mcp.get_prompt(
                "greet_user", {"name": "Alice", "language": "zh"}
            )
            self.assertIn("请写", prompt.messages[0].content.text)
            resource = await demo.mcp.read_resource("greeting://Alice/zh")
            self.assertIn("你好", list(resource)[0].content)

        asyncio.run(check_contracts())


if __name__ == "__main__":
    unittest.main(verbosity=2)
