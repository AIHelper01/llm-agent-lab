# LLM Agent Lab · 大语言模型智能体学习实验室

一个系统化的 **LLM 智能体（Agent）学习与实践仓库**，涵盖从理论入门、通信协议、核心专题实践到综合项目实战的完整学习路径。内容以中文教程（Markdown + Jupyter Notebook）为主，配合可运行的代码示例，帮助读者从零理解并动手构建智能体系统。

## 内容结构

```
llm-agent-lab/
├── 00_图速览/          # 核心概念一图速览（智能体、MCP-Skills 等）
├── 01_理论篇/          # 智能体理论基础
├── 02_协议篇/          # 智能体通信协议（MCP / A2A / ANP / Agent Skills）
├── 03_实践篇/          # 核心专题动手实践
├── 04_综合实战/        # 多平台综合项目实战
├── 05_拓展篇/          # 进阶拓展
├── assets/             # 教程图片资源
├── Recycled/           # 历史/草稿文档归档
├── 模型统一配置说明.ipynb  # 各家模型 API 的统一调用配置示例
├── pyproject.toml      # uv 项目配置（Python ≥ 3.12，全量课程依赖）
├── uv.lock             # uv 依赖锁文件（版本完全锁定）
├── .python-version     # uv 固定使用 Python 3.12
└── requirements.txt    # pip 依赖清单（与 pyproject 同版本，供 conda/pip 使用）
```

### 01 · 理论篇

| 章节 | 内容 |
| --- | --- |
| 01 | 初识智能体 |
| 02 | 智能体发展史 |
| 03 | 大语言模型基础 |
| 04 | 智能体经典范式构建 |
| 05 | 智能体工程范式的演进 |

### 02 · 协议篇

| 章节 | 内容 |
| --- | --- |
| 01 | 智能体通信协议总览（MCP / A2A / ANP） |
| 02 | Agent Skills 解读 |
| 03 | Agent Skills 补充 |

### 03 · 实践篇

- **[工具专题](03_实践篇/03_tools/README.md)**：Function Calling、MCP 和 Skills；中文为主，英文版在 `english/` 目录下，含天气和文件服务及 Skill 对比案例。
- **记忆专题**：记忆与检索、当代 Agent 记忆系统入门，以及 Mem0 / Letta / GBrain 三个记忆项目的快速上手实战
- **上下文工程**：上下文工程的方法与实践

### 04 · 综合实战

- **实战范式**：基于低代码平台 vs 基于开发框架的智能体搭建
- **Dify**：Dify 构建智能体一页纸速通，附多个可直接导入的 DSL 工作流（`yml/`：路线规划、A 股分析、ECharts 可视化、SEO 博客生成等）
- **OpenClaw**：OpenClaw（小龙虾）安装调试一页纸
- **LangChain**：LangChain 1.0 Agent 实践（Notebook，含 MCP 集成）
- **综合案例**：`helloagents-trip-planner` 智能旅行助手 —— FastAPI 后端 + Vue 前端的全栈 Agent 应用（接入高德地图、Unsplash 等服务）

### 05 · 拓展篇

- 从零构建你自己的 Agent 框架（HelloAgents）
- 智能体性能评估

## 快速开始

### 1. 环境准备
- Python 3.12
- Jupyter Notebook 或 JupyterLab
- VSCode

推荐使用 Python 3.12，并为项目创建独立虚拟环境。根目录的 `pyproject.toml`、`uv.lock`、
`.python-version` 共同定义唯一环境，以下两种方式任选其一。

```bash
git clone https://github.com/AIHelper01/llm-agent-lab.git
cd llm-agent-lab
```

### 方式一：uv（推荐）

`uv sync` 会读取 `.python-version` 自动准备 Python 3.12，并在根目录生成 `.venv/`（已忽略，不提交）。
仓库内所有 Python 命令都用 `uv run` 前缀执行，无需手动激活环境。

```bash
uv sync --locked        # 严格按 uv.lock 安装全部课程依赖

uv run python main.py   # 验证环境可用，输出 Hello from 3-4llm-agent!

uv run ipython kernel install \
--user \
--name env_agent \
--display-name "Python 3.12 (env_agent)"
```

依赖升级流程：`uv add <包>` 或 `uv lock --upgrade-package <包>`，随后提交更新后的 `pyproject.toml` 与 `uv.lock`。

### 方式二：Conda + pip

```bash
conda create --name env_agent python=3.12 -y

conda activate env_agent

pip install -r requirements.txt

python -m ipykernel install \
--user \
--name=env_agent \
--display-name "Python 3.12 (env_agent)"
```

### 2. 配置模型 API (示例)

在项目根目录创建 `.env` 并填入你的密钥，支持多家 OpenAI 兼容接口：

复制根目录 [`.env.example`](.env.example) 为 `.env`（Windows 可使用 `Copy-Item .env.example .env`），再填写自己的配置：

```dotenv
vLLM_QWEN_BASE_URL=http://127.0.0.1:8000/v1
vLLM_QWEN_API_KEY=
vLLM_QWEN_MODEL_ID=my_qwen3.8_flash_next
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5/weather
OPENWEATHER_API_KEY=
TAVILY_API_KEY=
```

`03_实践篇/03_tools` 统一读取 `vLLM_QWEN_*` 配置。其他课程章节若使用独立服务，
请按各自教程补充本地环境变量。真实 `.env`、缓存、Notebook 检查点与 MCP 恢复状态均不提交。
密钥留空时，相关在线示例需要配置后才能运行。

各家接口的统一调用方式（含代理冲突处理）见根目录的 [`模型统一配置说明.ipynb`](模型统一配置说明.ipynb)，建议动手前先运行一遍验证连通性。

### 3. 开始学习

- 纯理论章节直接阅读对应 Markdown 文档即可；
- 含 `.ipynb` 的章节需启动 Jupyter 运行：

```bash
uv run jupyter lab   # 或 jupyter notebook
```

推荐学习顺序：`00 图速览` → `01 理论篇` → `02 协议篇` → `03 实践篇` → `04 综合实战` → `05 拓展篇`。

## 说明

- 部分 Notebook 会清除本地代理环境变量（`HTTP_PROXY` 等）以避免网络冲突，如遇 API 连接问题请先检查代理设置。
- `Recycled/` 目录为历史草稿归档，仅供翻阅，不属于正式学习路径。
- `04_综合实战/07_综合实战-案例/helloagents-trip-planner/` 是独立的全栈项目，有其自己的 README 与依赖，请进入该目录单独安装运行。


## 测试与贡献

工具专题的离线测试覆盖中英文、天气预报、文件恢复及 Skill/MCP 对比，不需要真实 API Key。
运行方式见 [CONTRIBUTING.md](CONTRIBUTING.md)，GitHub Actions 配置在 Windows 和 Linux 上运行这些检查。
全量课程的在线模型、第三方平台和综合项目不在该离线 CI 的覆盖范围内。

贡献前请阅读 [贡献指南](CONTRIBUTING.md) 和 [安全说明](SECURITY.md)。本项目沿用 [MIT License](LICENSE)；
引用的第三方资料、图片与案例仍应遵循其原作者的许可和署名要求。
