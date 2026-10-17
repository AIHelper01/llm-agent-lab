# 本轮 MCP 优化思路与落地

[English](OPTIMIZATION.md) | 简体中文

沿用文件 MCP 这轮实际迭代顺序：从自然语言任务暴露缺口，先保证执行与数据可靠，再补工具、验证中英文、整理 showcase，最后统一 w- 命名并清理过时文件。

| 思路 | 文件服务 | 天气服务 | 基础与时间示例 |
| --- | --- | --- | --- |
| 从使用场景查工具缺口 | 删除恢复、快照、批量预览 | 坐标查询，避免城市歧义 | 健康检查、时区和时间转换 |
| 先修失败路径 | 暂存发布、哈希、历史回滚 | 不回显含密钥的异常，校验状态及响应 | 输入校验，拒绝时区歧义 |
| 控制返回内容 | 分页和分段读取 | 原始响应改为按需返回 | 返回明确的时区、偏移和时间戳 |
| 中英文兼容 | 内容不翻译，提示可切换 | 地点不翻译，提示与天气描述可切换 | 资源 URI 选语言，提示及错误可切换 |
| 用协议测试验收 | 实际 HTTP、故障注入及并发 | 本地模拟上游 + 实际 HTTP MCP | 实际 HTTP tools/resources/prompts 与 stdio |
| 文档可复现 | 保留真实对话历史及限制 | 不把模拟数据说成实时天气 | 不把演示流程说成真实用户对话 |
| 命名与清理 | 单个 w- 主入口 | 单个 w- 主入口 | 两种传输各一个 w- 主入口 |

不为追求统一而给天气/基础示例增加文件事务、复杂缓存、重试框架或抽象层。保留各自教学重点。

## 当前入口

- `00_mcp-server-demo/w-mcp_demo_server.py`：w-MCPDemo，HTTP。
- `00_mcp-server-demo/w-time_mcp_server.py`：w-TimeMCP，stdio。
- `01_weather-mcp-server/w-openweather_mcp_server.py`：w-OpenWeatherMCP，HTTP。
- `02_file-mcp-server/w-file_workbench_mcp_server.py`：w-FileWorkbenchMCP，HTTP。

旧入口不再保留，旧客户端启动路径需要更新。现有文件恢复数据不删除；Notebook 保留原教学历史，不自动重写。

## 验证

父级 mcp 环境需安装 mcp>=1.12,<2、python-dotenv、requests、tzdata：

```bash
python -B -m unittest -v test_forecast test_weather_demo test_bilingual_tools
python -B -m unittest discover -s 02_file-mcp-server -p "test_file_*.py" -v
```

天气使用本地模拟上游，不读取或消耗真实密钥配额。本轮在 Windows/Python 3.12 验证；Linux/macOS 未实测。
英文 showcase 保持英文文件名与参数示例，原始用户数据的语言保持可用。

## 本轮结果

| 验证 | 结果 |
| --- | --- |
| 天气、基础与时间新增测试 | 12 项通过，含实际 HTTP MCP、本地天气上游及 stdio |
| 后续预报扩展 | 7 项通过，覆盖中英文及地点当地日期；另完成南京真实中英文调用 |
| 原有联合中英文回归 | 7 项通过 |
| 文件服务回归 | 21 项通过 |
| 合计 | 47 项全部通过 |
| 静态检查 | Ruff 通过 |
| 英文 showcase | 两个新增英文版本均通过 ASCII-only 检查 |

天气目录的旧缓存和 Notebook 检查点，以及本轮产生的共享 Ruff 缓存，已移至系统临时备份目录，未丢弃原内容。
两个目录只保留当前 w- 主脚本、中英文 README 和 showcase，不保留旧启动包装脚本。

## 英文默认版迁移验收（2026-10-18）

专题目录调整为 `03_tools/01_function-calling`、`02_mcp`、`03_skills`。默认英文教程与 Notebook 已补齐，中文版本使用 `.zh-CN` 后缀。当前版本同步修复本地链接、图片及测试路径；英文 Notebook 清除历史输出。原课件图片保留，图片内可能有中文。

MCP 47 项、Skill 4 项，共 51 项回归通过；36 份文档与 Notebook 的本地链接、图片及源码语言检查通过，另补充测试记录中文版。Python 语法和 Ruff 核心错误检查通过。全仓规则扫描仍有原教学 Notebook 的导入排序等风格告警，本轮未批量格式化。天气服务已从新目录重启并验证 6 个工具及中英文配置检查。
