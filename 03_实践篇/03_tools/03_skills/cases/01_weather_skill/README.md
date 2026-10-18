[English](../../../english/03_skills/cases/01_weather_skill/README.md) | 简体中文

# 案例：用 Skill 查询天气，对比 MCP

同样问“南京明天天气怎么样”，这个案例通过 **Skill 指令 + 本地脚本直接调用 OpenWeather**，
与旁边的 `w-OpenWeatherMCP` 做对比。两个实现均支持实时天气、5 天 / 3 小时预报、城市或坐标、中英文。
Skill 入口为 [w-openweather/SKILL.md](w-openweather/SKILL.md)，脚本为 [weather.py](w-openweather/scripts/weather.py)。

## 目录

```text
01_weather_skill/
  README.md
  english/README.md
  test_weather_skill.py
  w-openweather/
    SKILL.md
    scripts/weather.py
```

说明和测试放在案例目录，Skill 包内只保留执行所需的指令与脚本。脚本不导入 MCP SDK、不连接 MCP 服务、不导入 MCP 服务端实现。
它是独立的教学实现，返回更精简的字段；不声称与 MCP 的所有诊断字段、错误细节完全相同。

## 运行 Skill 脚本

使用 Python 3.12，安装运行依赖：

```bash
python -m pip install requests python-dotenv
```

在环境变量中配置 `OPENWEATHER_API_KEY`，或在当前工作目录/祖先目录的 `.env` 配置。
兼容 `API_KEY_OPENWEATHER`，不要将密钥写入 Skill 或命令参数。
`OPENWEATHER_BASE_URL`、`BASE_URL_OPENWEATHER`、`OPENWEATHER_FORECAST_URL` 的含义与 MCP 案例一致；
标准实时地址的 `/weather` 会推导为 `/forecast`。
超时沿用 `WEATHER_MCP_TIMEOUT_SECONDS`，这是共享的历史变量名，不表示脚本通过 MCP 执行。

以下命令在本案例目录执行，不需要先启动天气 MCP：

```bash
python -B w-openweather/scripts/weather.py current --location "Nanjing,CN" --language en
python -B w-openweather/scripts/weather.py forecast --location "Nanjing,CN" --date tomorrow --language zh
python -B w-openweather/scripts/weather.py forecast --latitude 32.06 --longitude 118.78 --date tomorrow --language en --include-periods
```

返回 JSON，成功退出码 0，API/配置/数据失败为 1，命令语法错误为 2。
预报日期支持 today、tomorrow、all 或 YYYY-MM-DD，明天按地点 UTC 偏移计算。
温度范围是分时采样范围，最大分时降水概率不等于全天概率；边界日期可能只有部分采样。

## 让 Agent 按 Skill 执行

将 `w-openweather/` 按所用 Agent 宿主的约定注册为 Skill，再发送：

```text
Use $w-openweather to forecast tomorrow's weather in Nanjing, China, in English.
```

或：

```text
用 $w-openweather 查询南京明天的天气，中文回答。
```

仅把目录放进仓库不意味着任何客户端都会自动发现它。本案例不修改用户的全局技能目录。
尚未注册时，也可明确让 Agent 阅读本目录下的 SKILL.md，再按其中指令执行；这验证指令和脚本流程，
不等于验证了特定宿主的自动发现或自动选择。

## 同一请求的两条执行路径

```text
Skill:
用户 -> Agent 读取 SKILL.md -> 执行本地 weather.py -> OpenWeather -> JSON -> 回答

本例 MCP:
用户 -> Agent 选择 get_forecast 工具 -> MCP HTTP 服务 -> OpenWeather -> 工具结果 -> 回答
```

MCP 对应调用：

```text
get_forecast(location="Nanjing,CN", forecast_date="tomorrow", language="en", include_periods=false)
```

| 对比点 | 本例 Skill | 本例 MCP |
| --- | --- | --- |
| 提供给 Agent 的入口 | SKILL.md 的元数据、指令及脚本 | 服务发现的工具描述、参数 schema 与调用结果 |
| 谁决定流程 | Agent 按指令选择命令、读取结果 | Agent 选择工具，服务端执行函数 |
| 如何得到数据 | Agent 的执行环境直接运行 Python 访问 API | MCP 服务进程访问 API |
| 依赖 | 执行工具、Python、requests、python-dotenv | MCP 客户端；服务端有 Python、MCP SDK 及 API 依赖 |
| 是否启动服务 | 不需要 MCP 服务 | 本例使用已启动的 HTTP 服务；其他 MCP 也可由客户端启动 stdio 进程 |
| 密钥在哪里 | 脚本执行环境 | MCP 服务端环境；远程客户端不必持有 OpenWeather 密钥 |
| 校验在哪里 | CLI 参数及脚本内部；Skill 指令不能替代校验 | MCP 参数 schema 加服务端校验 |
| 更新方式 | 更新 Skill 指令或脚本；宿主可能需要重新加载 | 更新服务并按需刷新工具定义 |
| 调试线索 | 执行命令、退出码、JSON | MCP 工具输入输出及服务日志 |
| 本例侧重 | 给 Agent 可复用的操作方法 | 给不同客户端提供一致的工具调用接口 |

Skill 可以包含可执行代码，MCP 也可以提供 prompts/resources；两者不是简单的“提示词 vs 代码”。
它们可以组合：Skill 规定如何选择日期和组织回答，数据获取交给 MCP 工具。
权限由宿主、操作系统和服务部署决定，不因使用其中一种方式自动更安全。
本案例未测量耗时或 token，不能据此宣称谁必然更快、更便宜。

格式与协议依据：[Agent Skills 官方说明](https://agentskills.io/home)、[MCP 架构](https://modelcontextprotocol.io/docs/learn/architecture)。
天气 API 依据：[OpenWeather 当前天气](https://openweathermap.org/api/current)、[预报](https://openweathermap.org/forecast5)。

## 验证

案例测试额外需要 MCP SDK，用于交叉核对，不是 Skill 脚本的运行依赖：

```bash
python -m pip install "mcp>=1.12,<2"
python -B test_weather_skill.py
```

测试使用同一个本地模拟 OpenWeather 服务，覆盖中英文 CLI 子进程、地点日期跨日、失败退出码和密钥不泄漏。
MCP 对照通过 SDK 的内存内工具分发执行；相同预报夹具的日期、采样数量、温度范围与最大分时降水概率一致。
不比较不同时间发出的真实 API 请求是否逐字相同，也不宣称两个 JSON schema 完全相同。

Skill 格式另通过 skill-creator 的 quick_validate 校验。测试不会停止已运行的 MCP 服务、修改技能安装配置或使用真实 API 配额。
实际 Skill 脚本的实时调用记录与模拟测试结果应分别标注；自动发现及模型选择行为未纳入这些脚本测试。

### 标注日期的真实验证

2026-10-17，在仅安装 requests、python-dotenv 的独立环境中，脚本直接查询南京 10 月 18 日预报成功。
另行检查确认 `MCP SDK installed: False`。返回八个采样，温度 17.04..23.64°C，小雨/中雨。
这是固定时间的验证记录，不应在之后复用为天气预报。已有 MCP 服务保持运行，脚本没有连接它。
真实验证使用已配置的服务商密钥，与不消耗配额的夹具测试分别记录。未注册全局 Skill，也未验证宿主自动发现。
