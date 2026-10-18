# Function Calling

[English](../english/01_function-calling/README.md) | 简体中文

[中文教程](01_fc-practice.ipynb) | [英文教程](../english/01_function-calling/01_fc-practice.ipynb)

中英文 Notebook 均只使用 `my_qwen3.8_flash_next`，所有模型调用直接读取根目录 `.env` 中的
`vLLM_QWEN_BASE_URL`、`vLLM_QWEN_API_KEY`、`vLLM_QWEN_MODEL_ID`。
已移除其他提供方配置、旧模型名及重复的备用调用示例。

请从仓库目录内运行 Notebook，保证 `find_dotenv(usecwd=True)` 能找到根目录 `.env`。
密钥不写入 Notebook；天气调用仍需要 OpenWeather 配置。

本目录 Notebook 已用 `env_agent_uv` 内核（Python 3.12）实跑并保存输出，运行日期 2026-10-18；每个代码单元下方内嵌「**预期输出：**」，清空输出后仍可查看当次真实结果。模型回复与实时天气会随运行变化。
环境、示例和测试见[专题入口](../README.md)。
