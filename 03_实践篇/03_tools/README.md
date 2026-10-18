# 工具专题：Function Calling、MCP 与 Skills

[English](english/README.md) | 简体中文

本专题以中文为主：目录与文件名统一使用英文，**无后缀文件即中文母本**；英文版集中放在
`english/` 目录下，与中文树保持一对一的相对路径。服务端脚本、测试、样例文件和图片只保留一份，
中英文课件共用同一套代码与素材。

| 模块 | 中文入口 | 英文入口 |
| --- | --- | --- |
| 总览 | [智能体与工具](overview.md) | [Overview](english/overview.md) |
| Function Calling | [实战](01_function-calling/01_fc-practice.ipynb) | [Practice](english/01_function-calling/01_fc-practice.ipynb) |
| MCP | [理论](02_mcp/01_mcp-theory.md)、[实战](02_mcp/02_mcp-practice.ipynb) | [Theory](english/02_mcp/01_mcp-theory.md)、[Practice](english/02_mcp/02_mcp-practice.ipynb) |
| Skills | [理论](03_skills/skills-theory.md) | [Theory](english/03_skills/skills-theory.md) |
| 天气 Skill 与 MCP 对比 | [案例](03_skills/cases/01_weather_skill/README.md) | [Case](english/03_skills/cases/01_weather_skill/README.md) |

目录改为 `03_tools/01_function-calling`、`02_mcp`、`03_skills`，旧启动配置中的路径需要同步更新。
MCP 保持 `w-` 前缀，文件样例和恢复历史保留。已安装的天气 Skill 为自包含脚本，不依赖仓库路径。

MCP 服务说明与工具描述为中英双语（中文在前、英文在后），模型和两种语言的学员读同一份即可。返回的提示与天气描述默认英文，使用 `language="zh"` 切换中文；JSON 字段、错误码保持一致，用户数据不翻译。
天气描述由 OpenWeather 本地化，中文城市名能否解析取决于上游覆盖。

## 可直接运行的 MCP 服务

- [基础与时间工具](02_mcp/cases/00_mcp-server-demo/README.md)
- [OpenWeather 实时天气与预报](02_mcp/cases/01_weather-mcp-server/README.md)
- [文件工作台](02_mcp/cases/02_file-mcp-server/README.md)
- [优化记录](02_mcp/cases/OPTIMIZATION.md)

三个 HTTP 服务是常驻进程，stdio 服务由 Agent 自己拉起。总览如下，启动与客户端写法见各服务文档：

| 服务 | 传输 | 默认地址 | uv 免安装启动（在该服务目录内执行） |
| --- | --- | --- | --- |
| `w-MCPDemo` | Streamable HTTP | `http://127.0.0.1:8000/mcp` | `uv run --no-project --with "mcp>=1.12,<2" python w-mcp_demo_server.py` |
| `w-OpenWeatherMCP` | Streamable HTTP | `http://127.0.0.1:16681/mcp` | `uv run --no-project --with "mcp>=1.12,<2" --with python-dotenv --with requests python w-openweather_mcp_server.py` |
| `w-FileWorkbenchMCP` | Streamable HTTP | `http://127.0.0.1:16682/mcp` | `uv run --no-project --with "mcp>=1.12,<2" --with python-dotenv python w-file_workbench_mcp_server.py` |
| `w-TimeMCP` | stdio | 无端口，客户端拉起 | `uv run --no-project --with "mcp>=1.12,<2" --with tzdata python w-time_mcp_server.py` |

每份服务文档都含两节：启动服务（pip 与 uv 三种方式）和在 Agent 中配置（Codex 与 Cherry Studio
的完整写法）。HTTP 服务在 Codex 里一行即可接入：`codex mcp add <服务名> --url <MCP 地址>`；
Cherry Studio 走设置 → MCP 服务 → 添加服务器，远程地址字段是 `baseUrl`。

请在各服务文档标注的工作目录内运行示例。环境要求 Python 3.12，依赖 `mcp>=1.12,<2`、
`python-dotenv`、`requests`、`tzdata`。仓库用户可在仓库根目录执行 `uv sync`；也可以单独准备一个环境：

```bash
python -m pip install "mcp>=1.12,<2" python-dotenv requests tzdata
```

在 `02_mcp/cases` 目录运行离线回归测试：

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
python -B -m unittest discover -s 02_file-mcp-server -p "test_file_*.py" -v
```

在 `03_skills/cases/01_weather_skill` 目录运行 `python -B test_weather_skill.py`。上述测试对
OpenWeather 打桩并使用临时文件，不消耗真实 API 额度。Notebook 中的模型与 API 调用属于交互练习，
需要你自己的凭证；其中的示例响应仅作演示，不是真实天气。

## 语言与迁移

服务说明与工具描述中英双语呈现（中文在前、英文在后），客户端工具面板一次显示两种语言。返回的提示与天气描述默认英文，传 `language="zh"` 切换中文，也可显式传 `language="en"`；JSON 字段与错误码保持一致。用户文件名、正文内容和城市输入保持原语言，该开关不翻译用户数据。城市解析与天气
描述的中文化由 OpenWeather 决定。

专题目录为 `03_tools/01_function-calling`、`02_mcp`、`03_skills`，旧启动配置和 Notebook 书签中的
路径需要同步更新。MCP 服务名、客户端配置键与主脚本统一使用 `w-` 前缀；文件恢复数据和样例文件保留。
已安装的 `w-openweather` Skill 是自包含脚本，不依赖仓库目录名。

英文版整体位于 `english/`，与中文课件同名同层级，便于逐句对照。
`03_skills/cases/01_weather_skill/w-openweather/SKILL.md` 是给模型执行的功能清单，只保留单份版本。
原课件图片保留，图片内可能包含中文；英文正文提供相应说明。双语结构由
`scripts/check_bilingual_parity.py` 校验。
