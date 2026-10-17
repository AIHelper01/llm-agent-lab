# Function Calling

[English](README.md) | 简体中文

[中文教程](01_fc-practice.zh-CN.ipynb) | [英文教程](01_fc-practice.ipynb)

中英文 Notebook 均只使用 `my_qwen3.8_flash_next`，所有模型调用直接读取根目录 `.env` 中的
`vLLM_QWEN_BASE_URL`、`vLLM_QWEN_API_KEY`、`vLLM_QWEN_MODEL_ID`。
已移除其他提供方配置、旧模型名及重复的备用调用示例。

请从仓库目录内运行 Notebook，保证 `find_dotenv(usecwd=True)` 能找到根目录 `.env`。
密钥不写入 Notebook；天气调用仍需要 OpenWeather 配置。

环境、示例和测试见[专题入口](../README.zh-CN.md)。
