# 工具专题：Function Calling、MCP 与 Skills

[English](README.md) | 简体中文

本专题默认使用英文目录、英文文档与英文 Notebook，中文版本统一加 `.zh-CN` 后缀。

| 模块 | 中文入口 | 英文入口 |
| --- | --- | --- |
| 总览 | [智能体与工具](overview.zh-CN.md) | [Overview](overview.md) |
| Function Calling | [实战](01_function-calling/01_fc-practice.zh-CN.ipynb) | [Practice](01_function-calling/01_fc-practice.ipynb) |
| MCP | [理论](02_mcp/01_mcp-theory.zh-CN.md)、[实战](02_mcp/02_mcp-practice.zh-CN.ipynb) | [Theory](02_mcp/01_mcp-theory.md)、[Practice](02_mcp/02_mcp-practice.ipynb) |
| Skills | [理论](03_skills/skills-theory.zh-CN.md) | [Theory](03_skills/skills-theory.md) |
| 天气 Skill 与 MCP 对比 | [案例](03_skills/cases/01_weather_skill/README.zh-CN.md) | [Case](03_skills/cases/01_weather_skill/README.md) |

目录改为 `03_tools/01_function-calling`、`02_mcp`、`03_skills`，旧启动配置中的路径需要同步更新。
MCP 保持 `w-` 前缀，文件样例和恢复历史保留。已安装的天气 Skill 为自包含脚本，不依赖仓库路径。

工具提示默认英文，使用 `language="zh"` 切换中文；JSON 字段、错误码保持一致，用户数据不翻译。
天气描述由 OpenWeather 本地化，中文城市名能否解析取决于上游覆盖。

环境、启动和离线测试命令见[英文入口](README.md)及各服务 README。
原课件图片保留，图片内可能包含中文；英文正文提供相应说明。
