# Function Calling

English | [Simplified Chinese](../../01_function-calling/README.md)

[English tutorial](01_fc-practice.ipynb) | [Chinese tutorial](../../01_function-calling/01_fc-practice.ipynb)

Both notebooks use only `my_qwen3.8_flash_next`. Configure these existing variables
in the repository-root `.env`:

```dotenv
vLLM_QWEN_BASE_URL=<your OpenAI-compatible endpoint>
vLLM_QWEN_API_KEY=<your API key>
vLLM_QWEN_MODEL_ID=my_qwen3.8_flash_next
```

All model calls read these variables directly. No alternate provider configuration
or hardcoded model fallback is included. Run the notebook from this repository so
`find_dotenv(usecwd=True)` can locate the root `.env`. Model execution may consume
your server's compute; weather calls also require the OpenWeather configuration.

The notebook in this directory was executed with the `env_agent_uv` kernel (Python 3.12) on
2026-10-18 and the outputs are saved. Every code cell is followed by an **Expected output:**
block, so the real results stay readable after Clear All Outputs. Model wording and live weather
values change between runs.

See the [topic index](../README.md) for setup, runnable examples and tests.
