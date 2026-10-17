# 欢迎使用 FastMCP

> 快速、Pythonic 的方式来构建 MCP Server、客户端和应用程序。

**FastMCP 是构建 MCP 应用程序的标准框架。** [模型上下文协议](https://modelcontextprotocol.io/)（MCP）将 LLM 连接到工具和数据。FastMCP 为你提供从原型到生产所需的一切 —— 构建暴露功能的Server，将客户端连接到任何 MCP 服务，并为你的工具提供交互式 UI：

```python {1} theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP

mcp = FastMCP("演示 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """两数相加"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

## 超越基础 MCP

FastMCP 开创了 Python MCP 开发，FastMCP 1.0 于 2024 年被并入[官方 MCP SDK](https://github.com/modelcontextprotocol/python-sdk)。**这是 FastMCP 2.0，** 当前积极维护的版本，远超基础协议实现。虽然 SDK 提供核心功能，但 FastMCP 2.0 提供生产所需的一切：高级 MCP 模式（服务器组合、代理、OpenAPI/FastAPI 生成、工具转换）、企业级认证（Google、GitHub、Azure、Auth0、WorkOS 等）、部署工具、测试框架和完整的客户端库。准备开始构建？从我们的[安装指南](https://fastmcp.wiki/zh/getting-started/installation)开始，或直接跳转到[快速开始](https://fastmcp.wiki/zh/getting-started/quickstart)。FastMCP 由 [Prefect](https://www.prefect.io/) 用 💙 制作。

## 什么是 MCP？

模型上下文协议允许您构建服务器，以安全、标准化的方式向 LLM 应用程序公开数据和功能。它经常被描述为”AI 的 USB-C 接口”，提供了连接 LLM 与其可用资源的统一方式。您可以将其视为一个 API，但专门为 LLM 交互而设计。MCP 服务器可以：

- 通过 `Resources` 公开数据（可以将其视为类似 GET 端点；用于将信息加载到 LLM 的上下文中）
- 通过 `Tools` 提供功能（类似 POST 端点；用于执行代码或产生副作用）
- 通过 `Prompts` 定义交互模式（LLM 交互的可重用模板）
- 以及更多！

FastMCP 提供了一个高级、Pythonic 的接口来构建、管理和与这些服务器交互。

## 为什么选择 FastMCP？

FastMCP 处理所有复杂的协议细节，让您专注于构建。在大多数情况下，装饰一个 Python 函数就是您所需要的 — FastMCP 处理其余部分。🚀 **快速**: 高级接口意味着更少的代码和更快的开发🍀 **简单**: 以最少的样板代码构建 MCP 服务器🐍 **Pythonic**: 对 Python 开发者来说感觉自然🔍 **完整**: 生产所需的一切 — 企业级认证（Google、GitHub、Azure、Auth0、WorkOS）、部署工具、测试框架、客户端库等FastMCP 提供从想法到生产的最短路径。可以本地部署、使用 [FastMCP Cloud](https://fastmcp.cloud/)（个人服务器免费）部署到云端，或部署到您自己的基础设施。



# 安装

> 安装 FastMCP 并验证你的设置

## 安装 FastMCP

我们建议使用 [uv](https://docs.astral.sh/uv/getting-started/installation/) 来安装和管理 FastMCP。

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
pip install fastmcp
```

或使用 uv：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
uv add fastmcp
```

### 可选依赖

FastMCP 为特定功能提供可选的额外依赖。例如，要安装后台任务额外依赖：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
pip install "fastmcp[tasks]"
```

有关任务系统的详细信息，请参阅[后台任务](/servers/tasks)。

### 验证安装

要验证 FastMCP 是否正确安装，你可以运行以下命令：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp version
```

你应该看到类似以下的输出：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
$ fastmcp version

FastMCP 版本:                           3.0.0
MCP 版本:                               1.25.0
Python 版本:                            3.12.2
平台:            macOS-15.3.1-arm64-arm-64bit
FastMCP 根路径:            ~/Developer/fastmcp
```

### 依赖许可

FastMCP 依赖 Cyclopts 实现 CLI 功能。Cyclopts v4 包含 docutils 作为传递依赖，其许可复杂，可能会触发某些组织的合规审查。

如果这是一个问题，你可以安装移除此依赖的 Cyclopts v5 alpha：

  ```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
pip install "cyclopts>=5.0.0a1"
  ```

或者，等待稳定的 v5 版本发布。详情请参阅 [此问题](https://github.com/BrianPugh/cyclopts/issues/672)。


## 升级

```
pip install --upgrade fastmcp
```



# 快速入门

欢迎！本指南将帮助你快速设置 FastMCP，运行你的第一个 MCP Server。

## 创建 FastMCP Server

FastMCP Server是工具、资源和其他 MCP 组件的集合。要创建Server，首先实例化 `FastMCP` 类。

创建一个名为 `my_server.py` 的新文件并添加以下代码：

```python my_server.py theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
```

就是这样！你已经创建了一个 FastMCP Server，尽管是一个非常无聊的Server。让我们添加一个工具让它更有趣。

## 添加工具

要添加一个返回简单问候语的工具，请编写一个函数并用 `@mcp.tool` 装饰它以向Server注册：

```python my_server.py {5-7} theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## 运行Server

运行 FastMCP Server的最简单方法是调用其 `run()` 方法。你可以在不同的传输方式之间选择，例如用于本地Server的 `stdio`，或用于远程访问的 `http`：
my_server.py (stdio) 
```python {"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```
my_server.py (HTTP) 
```python 
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

这让我们可以用 `python my_server.py` 运行Server。stdio 传输是将 MCP Server连接到客户端的传统方式，而 HTTP 传输支持远程连接。
为什么我们需要 `if __name__ == "__main__":` 块？

  `__main__` 块建议用于保持一致性和兼容性，确保你的Server与所有将Server文件作为脚本执行的 MCP 客户端一起工作。将专门使用 FastMCP CLI 运行Server的用户可以省略它，因为 CLI 直接导入Server对象。


### 使用 FastMCP CLI

你还可以使用 `fastmcp run` 命令来启动Server。请注意，FastMCP CLI **不会**执行Server文件的 `__main__` 块。相反，它导入你的Server对象并用你提供的任何传输和选项运行它。

例如，要使用默认的 stdio 传输运行此Server（无论你如何调用 `mcp.run()`），你可以使用以下命令：

```bash
fastmcp run my_server.py:mcp
```

要使用 HTTP 传输运行此Server，你可以使用以下命令：

```bash
fastmcp run my_server.py:mcp --transport http --port 8000
```

## 调用你的Server

一旦你的Server使用 HTTP 传输运行，你可以使用 FastMCP 客户端或任何支持 MCP 协议的 LLM 客户端连接到它：

`my_client.py`

```python my_client.py theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))
```

请注意：

* FastMCP 客户端是异步的，因此我们需要使用 `asyncio.run` 来运行客户端
* 我们必须在使用客户端之前进入客户端上下文（`async with client:`）
* 你可以在同一个上下文中进行多个客户端调用

## 为你的工具提供 UI

工具通常返回文本，但任何工具都可以返回交互式 UI。在你的工具装饰器中添加 `app=True` 并返回一个 [Prefab](https://prefab.prefect.io) 组件 —— 主机将其渲染为图表、表格、表单或对话中的任何其他视觉元素。这需要 `apps` 额外依赖（`pip install "fastmcp[apps]"`）。

`app=True` 标志告诉 FastMCP 自动连接渲染器和协议元数据。该工具仍然像任何其他 MCP 工具一样工作 —— 它接收参数并返回结果 —— 但结果是一个组件树，主机以视觉方式显示而不是纯文本。

`my_server.py`

```python my_server.py theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text, Badge, Row
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool(app=True)
def greet(name: str) -> PrefabApp:
    """Greet someone with a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Hello, {name}!")
        with Row(gap=2, align="center"):
            Text("Status")
            Badge("Greeted", variant="success")

    return PrefabApp(view=view)
```

你可以使用 `fastmcp dev apps my_server.py` 在本地预览应用程序工具 —— 不需要 MCP 主机。有关完整指南，包括状态管理、表单、图表和Server连接交互性。

## 部署到 Prefect Horizon

[Prefect Horizon](https://horizon.prefect.io) 是由 [Prefect](https://www.prefect.io) 的 FastMCP 团队构建的企业级 MCP 平台。它为 MCP Server提供托管、认证、访问控制和可观测性。


Horizon **对个人项目免费**，并为团队提供企业治理。

要部署你的Server，你需要一个 [GitHub 账户](https://github.com)。一旦你有了，你可以通过三个步骤部署你的Server：

1. 将你的 `my_server.py` 文件推送到 GitHub 仓库
2. 使用你的 GitHub 账户登录 [Prefect Horizon](https://horizon.prefect.io)
3. 从你的仓库创建一个新项目，并输入 `my_server.py:mcp` 作为Server入口点

就是这样！Horizon 将构建并部署你的Server，使其在类似 `https://your-project.fastmcp.app/mcp` 的 URL 上可用。你可以与其聊天以测试其功能，或从任何支持 MCP 协议的 LLM 客户端连接到它。



# FastMCP Server专题

> 用于构建 MCP 应用程序的核心 FastMCP Server类

`FastMCP` 类是每个 FastMCP 应用程序的核心部分。它充当你的工具、资源和提示的容器，管理与 MCP 客户端的通信并协调整个Server生命周期。

## 创建Server

最简单的情况下，FastMCP Server只需要一个名称。其他一切都有合理的默认值。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP

mcp = FastMCP("MyServer")
```

说明帮助客户端（以及它们背后的 LLM）了解你的Server做什么以及如何有效使用它。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
mcp = FastMCP(
    "DataAnalysis",
    instructions="Provides tools for analyzing numerical datasets. Start with get_summary() for an overview.",
)
```

## 组件

FastMCP Server向客户端暴露三种类型的组件，每种在 MCP 协议中扮演不同的角色。

**Tools**是客户端调用以执行操作或访问外部系统的函数。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b
```

**Resources***暴露客户端可以读取的数据 —— 被动数据源而非可调用的函数。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
@mcp.resource("data://config")
def get_config() -> dict:
    return {"theme": "dark", "version": "1.0"}
```

**Prompts**是可重用的消息模板，用于指导 LLM 交互。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
@mcp.prompt
def analyze_data(data_points: list[float]) -> str:
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"
```

每种组件类型都有详细的文档：[工具](/servers/tools)、[资源](/servers/resources)（包括[资源模板](/servers/resources#resource-templates)）和[提示](/servers/prompts)。

## 运行Server

通过调用 `mcp.run()` 启动你的Server。`if __name__` 守卫确保与将Server作为子进程启动的 MCP 客户端兼容。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

FastMCP 支持多种传输方式：

* **STDIO**（默认）：用于本地集成和 CLI 工具
* **HTTP**：用于使用 Streamable HTTP 协议的 Web 服务
* **SSE**：传统 Web 传输（已弃用）

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
# Run with HTTP transport
mcp.run(transport="http", host="127.0.0.1", port=9000)
```

Server也可以使用 FastMCP CLI 运行。有关传输和部署的详细信息，请参阅[运行你的Server](/deployment/running-server)。

## 配置参考

`FastMCP` 构造函数接受分为四类的参数：身份、组合、行为和处理器。

###  Identity身份

这些参数控制你的Server如何向客户端展示自己。

- "name" type="str" default="FastMCP"：Server的可读名称，显示在客户端应用程序和日志中

- "instructions" type="str | None"：描述如何与此Server交互。客户端显示这些说明以帮助 LLM 理解Server的用途和可用功能

- "version" type="str | None"：Server的版本字符串。如果未提供，默认为 FastMCP 库版本

- "website_url" type="str | None"：指向包含有关Server更多信息的网站的 URL。显示在客户端应用程序中

- "icons" type="list[Icon] | None"：Server的图标表示列表。有关详细信息，请参阅[图标](/servers/icons)




### 组合

这些参数控制你的Server由什么构建 —— 其组件、中间件、提供程序和生命周期。

- "tools" type="list[Tool | Callable] | None"：要在Server上注册的工具。当你需要以编程方式添加工具时，作为 `@mcp.tool` 装饰器的替代方案

- "auth" type="OAuthProvider | TokenVerifier | None"：用于保护基于 HTTP 的传输的认证提供程序。有关配置，请参阅[认证](/servers/auth/authentication)

- "middleware" type="list[Middleware] | None"：拦截和转换流经Server的每个 MCP 消息的[中间件](/servers/middleware) —— 双向的请求、响应和通知。用于横切关注点，如日志记录、错误处理和速率限制
- "providers" type="list[Provider] | None"：动态提供工具、资源和提示的[提供程序](/servers/providers)。提供程序在请求时查询，因此它们可以从数据库、API 或其他外部源提供组件

- "transforms" type="list[Transform] | None"：应用于所有组件的Server级[转换](/servers/transforms/transforms)。转换修改工具、资源和提示如何呈现给客户端 —— 例如，[搜索转换](/servers/transforms/tool-search)用按需发现替换大型目录
- "lifespan" type="Lifespan | AsyncContextManager | None"：Server启动和停止时运行的Server级设置和拆卸逻辑。有关可组合的生命周期，请参阅[生命周期](/servers/lifespan)
  


### 行为

这些参数调整Server如何处理请求以及与客户端通信。

- "on_duplicate" type="Literal[&#x22;warn&#x22;, &#x22;error&#x22;, &#x22;replace&#x22;, &#x22;ignore&#x22;]" default="warn"：如何处理重复的组件注册
- "strict_input_validation" type="bool" default="False"：当为 `False`（默认）时，FastMCP 使用 Pydantic 的灵活验证来强制兼容输入（例如 `"10"` → `10` 用于 int 参数）。当为 `True` 时，在调用函数之前根据确切的 JSON Schema 验证输入，拒绝类型不匹配。有关详细信息，请参阅[输入验证模式](/servers/tools#input-validation-modes)
- "mask_error_details" type="bool | None"：当为 `True` 时，将工具/资源响应中的内部错误详细信息替换为通用消息，以避免向客户端泄露实现细节。默认为 `FASTMCP_MASK_ERROR_DETAILS` 环境变量
- "list_page_size" type="int | None" default="None"：列表操作（`tools/list`、`resources/list` 等）每页的最大项目数。当为 `None` 时，所有结果在单个响应中返回。有关详细信息，请参阅[分页](/servers/pagination)
- "tasks" type="bool | None" default="False"：启用后台任务支持。当为 `True` 时，工具和资源可以返回 `CreateTaskResult` 以异步运行工作，同时客户端轮询结果
- "client_log_level" type="LoggingLevel | None"：通过 `context.log()` 发送到 MCP 客户端的消息的默认最小日志级别。设置后，低于此级别的消息将被抑制。各个客户端可以使用 MCP `logging/setLevel` 请求按会话覆盖此设置。其中之一为 `"debug"`、`"info"`、`"notice"`、`"warning"`、`"error"`、`"critical"`、`"alert"` 或 `"emergency"`
- "dereference_schemas" type="bool" default="True"：自动解引用从复杂 Pydantic 模型生成的 JSON schema 中的 `$ref` 指针。大多数客户端需要没有 `$ref` 的扁平 schema，因此这通常应保持启用
  


### 处理器和存储

这些参数为 MCP 功能提供自定义处理器，并为会话状态提供持久存储。

- "sampling_handler" type="SamplingHandler | None"：MCP 采样请求（Server发起的 LLM 调用）的自定义处理器。有关详细信息，请参阅[采样](/servers/sampling)

- "sampling_handler_behavior" type="Literal[&#x22;always&#x22;, &#x22;fallback&#x22;] | None" default="fallback"：当为 `"fallback"` 时，仅当不存在特定于工具的处理程序时才使用采样处理程序。当为 `"always"` 时，此处理程序用于所有采样请求
- "session_state_store" type="AsyncKeyValue | None"：跨请求持久化的会话状态的键值存储。默认为内存存储。提供自定义实现以在Server重启时持久化



## 基于标签的过滤

标签让你可以对组件进行分类并选择性地暴露它们。这对于为不同环境或用户类型创建Server的不同视图很有用。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
@mcp.tool(tags={"public", "utility"})
def public_tool() -> str:
    return "This tool is public"

@mcp.tool(tags={"internal", "admin"})
def admin_tool() -> str:
    return "This tool is for admins only"
```

过滤逻辑如下：

* **使用 `only=True` 启用**：切换到允许列表模式 —— 仅暴露至少有一个匹配标签的组件
* **禁用**：隐藏具有任何匹配标签的组件
* **优先级**：后续调用覆盖先前的调用，因此在允许列表后调用 `disable` 以排除


要确保组件永远不会被暴露，你可以在组件本身上设置 `enabled=False`。有关详细信息，请参阅特定于组件的文档。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
# Only expose components tagged with "public"
mcp = FastMCP()
mcp.enable(tags={"public"}, only=True)

# Hide components tagged as "internal" or "deprecated"
mcp = FastMCP()
mcp.disable(tags={"internal", "deprecated"})

# Combine both: show admin tools but hide deprecated ones
mcp = FastMCP()
mcp.enable(tags={"admin"}, only=True).disable(tags={"deprecated"})
```

此过滤适用于所有组件类型（工具、资源、资源模板和提示），并影响列表和访问。

## 自定义路由

当使用 HTTP 传输运行时，你可以使用 `@custom_route` 装饰器在 MCP 端点旁边添加自定义 Web 路由。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    mcp.run(transport="http")  # Health check at http://localhost:8000/health
```

自定义路由对于健康检查、状态端点和简单的 Webhook 很有用。对于更复杂的 Web 应用程序，请考虑[将 MCP Server挂载到 FastAPI 或 Starlette 应用程序中](/deployment/http#integration-with-web-frameworks)。



# FastMCP 客户端专题

> 通过类型安全、Pythonic 的接口与 MCP Server交互的编程客户端。

`fastmcp.Client` 类提供了一个用于与任何 MCP Server交互的编程接口。它自动处理协议细节和连接管理，让你专注于要执行的操作。

FastMCP 客户端设计用于确定性、受控的交互，而非自主行为，使其成为开发期间测试 MCP Server、构建需要可靠 MCP 交互的确定性应用程序，以及为代理或基于 LLM 的客户端创建具有结构化、类型安全操作的基础的理想选择。


  这是一个需要显式函数调用并为所有 MCP 操作提供直接控制的编程客户端。将其用作更高级系统的构建块。

## 创建客户端

你提供Server源，客户端自动推断适当的传输机制。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
import asyncio
from fastmcp import Client, FastMCP

# In-memory server (ideal for testing)
server = FastMCP("TestServer")
client = Client(server)

# HTTP server
client = Client("https://example.com/mcp")

# Local Python script
client = Client("my_mcp_server.py")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        # Execute operations
        result = await client.call_tool("example_tool", {"param": "value"})
        print(result)

asyncio.run(main())
```

所有客户端操作都需要使用 `async with` 上下文管理器进行正确的连接生命周期管理。

## 选择传输方式

客户端根据你传递给它的内容自动选择传输方式，但不同的传输方式具有对你的用例很重要的不同特性。

**内存传输**直接连接到同一 Python 进程内的 FastMCP Server实例。用于测试和开发，你希望消除子进程和网络复杂性。Server共享你进程的环境和内存空间。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import Client, FastMCP

server = FastMCP("TestServer")
client = Client(server)  # In-memory, no network or subprocess
```

**STDIO 传输**将Server作为子进程启动并通过 stdin/stdout 管道进行通信。这是 Claude Desktop 等桌面客户端使用的标准机制。子进程在隔离环境中运行，因此你必须显式传递Server所需的任何环境变量。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import Client

# Simple inference from file path
client = Client("my_server.py")

# With explicit environment configuration
client = Client("my_server.py", env={"API_KEY": "secret"})
```

**HTTP 传输**连接到作为 Web 服务运行的Server。用于Server独立运行并管理其自身生命周期的生产部署。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import Client

client = Client("https://api.example.com/mcp")
```

有关详细配置选项，包括认证头、会话持久性和多Server配置，请参阅[传输方式](/clients/transports)。

## 基于配置的客户端

从 MCP 配置字典创建客户端，其中可以包含多个Server。虽然没有 MCP 配置格式的官方标准，但 FastMCP 遵循 Claude Desktop 等工具使用的既定约定。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather-api.example.com/mcp"
        },
        "assistant": {
            "command": "python",
            "args": ["./assistant_server.py"]
        }
    }
}

client = Client(config)

async with client:
    # Tools are prefixed with server names
    weather_data = await client.call_tool("weather_get_forecast", {"city": "London"})
    response = await client.call_tool("assistant_answer_question", {"question": "What's the capital of France?"})

    # Resources use prefixed URIs
    icons = await client.read_resource("weather://weather/icons/sunny")
```

## 连接生命周期

客户端使用上下文管理器进行连接管理。当你进入上下文时，客户端建立连接并与Server执行 MCP 初始化握手。此握手交换功能、Server元数据和说明。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import Client, FastMCP

mcp = FastMCP(name="MyServer", instructions="Use the greet tool to say hello!")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

async with Client(mcp) as client:
    # Initialization already happened automatically
    print(f"Server: {client.initialize_result.serverInfo.name}")
    print(f"Instructions: {client.initialize_result.instructions}")
    print(f"Capabilities: {client.initialize_result.capabilities.tools}")
```

对于需要精确控制初始化发生时间的高级场景，禁用自动初始化并手动调用 `initialize()`：

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import Client

client = Client("my_mcp_server.py", auto_initialize=False)

async with client:
    # Connection established, but not initialized yet
    print(f"Connected: {client.is_connected()}")
    print(f"Initialized: {client.initialize_result is not None}")  # False

    # Initialize manually with custom timeout
    result = await client.initialize(timeout=10.0)
    print(f"Server: {result.serverInfo.name}")

    # Now ready for operations
    tools = await client.list_tools()
```

## 操作

FastMCP 客户端与三种类型的Server组件交互。

**工具**是客户端可以使用参数执行的Server端函数。使用 `call_tool()` 调用它们并接收结构化结果。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
async with client:
    tools = await client.list_tools()
    result = await client.call_tool("multiply", {"a": 5, "b": 3})
    print(result.data)  # 15
```

有关详细文档，包括版本选择、错误处理和结构化输出，请参阅[工具](/clients/tools)。

**资源**是客户端可以使用 URI 读取的数据源，可以是静态的或模板化的。使用 `read_resource()` 访问它们。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
async with client:
    resources = await client.list_resources()
    content = await client.read_resource("file:///config/settings.json")
    print(content[0].text)
```

有关详细文档，包括模板和二进制内容，请参阅[资源](/clients/resources)。

**提示**是可以接受参数的可重用消息模板。使用 `get_prompt()` 检索渲染的提示。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
async with client:
    prompts = await client.list_prompts()
    messages = await client.get_prompt("analyze_data", {"data": [1, 2, 3]})
    print(messages.messages)
```

有关详细文档，包括参数序列化，请参阅[提示](/clients/prompts)。

## 回调处理器

客户端支持用于高级Server交互的回调处理器。这些让你响应Server发起的请求并接收通知。

```python  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
from fastmcp import Client
from fastmcp.client.logging import LogMessage

async def log_handler(message: LogMessage):
    print(f"Server log: {message.data}")

async def progress_handler(progress: float, total: float | None, message: str | None):
    print(f"Progress: {progress}/{total} - {message}")

async def sampling_handler(messages, params, context):
    # Integrate with your LLM service here
    return "Generated response"

client = Client(
    "my_mcp_server.py",
    log_handler=log_handler,
    progress_handler=progress_handler,
    sampling_handler=sampling_handler,
    timeout=30.0
)
```

每种处理器类型都有自己的文档：

* **[采样](/clients/sampling)** - 响应Server LLM 请求
* **[引出](/clients/elicitation)** - 处理用户输入的Server请求
* **[进度](/clients/progress)** - 监控长时间运行的操作
* **[日志记录](/clients/logging)** - 处理Server日志消息
* **[根目录](/clients/roots)** - 向Server提供本地上下文


FastMCP 客户端被设计为基础工具。直接用于确定性操作，或在其可靠、类型安全的接口之上构建更高级别的代理系统。



# CLI

> fastmcp 命令行界面

`fastmcp` CLI 随 FastMCP 自动安装。它是从终端运行、测试、安装和与 MCP Server交互的主要方式。

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp --help
```

## 命令一览

| 命令                                                         | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`run`](/cli/running)                                        | 运行Server（本地文件、工厂函数、远程 URL 或配置文件）        |
| [`dev apps`](/cli/running#previewing-apps)                   | 启动基于浏览器的 Prefab App 工具预览 UI                      |
| [`dev inspector`](/cli/running#development-with-the-inspector) | 在 MCP Inspector 中启动Server以进行交互式测试                |
| [`install`](/cli/install-mcp)                                | 将Server安装到 Claude Code、Claude Desktop、Cursor、Gemini CLI 或 Goose |
| [`inspect`](/cli/inspecting)                                 | 将Server的工具、资源和提示打印为摘要或 JSON 报告             |
| [`list`](/cli/client)                                        | 列出Server的工具（以及可选的资源和提示）                     |
| [`call`](/cli/client#calling-tools)                          | 使用参数调用单个工具                                         |
| [`discover`](/cli/client#discovering-configured-servers)     | 在编辑器和工具中查找配置的 MCP Server                        |
| [`generate-cli`](/cli/generate-cli)                          | 从Server的工具模式搭建独立的类型化 CLI                       |
| [`project prepare`](/cli/running#pre-building-environments)  | 将依赖项预安装到可重用的 uv 项目                             |
| [`auth cimd`](/cli/auth)                                     | 创建和验证 OAuth 的 CIMD 文档                                |
| `version`                                                    | 打印版本信息（`--copy` 复制到剪贴板）                        |

## Server目标

大多数命令需要知道*要与之通信的*Server。你传递一个"Server规范"作为第一个参数，FastMCP 自动解析正确的传输方式。

**URL** 连接到正在运行的 HTTP Server：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list http://localhost:8000/mcp
fastmcp call http://localhost:8000/mcp get_forecast city=London
```

**Python 文件**直接加载 —— 不需要 `mcp.run()` 样板。FastMCP 在文件中查找名为 `mcp`、`server` 或 `app` 的Server实例，或者你可以显式指定一个：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list server.py
fastmcp run server.py:my_custom_server
```

**配置文件**也可以 —— FastMCP 自己的 `fastmcp.json` 格式和带有 `mcpServers` 键的标准 MCP 配置文件：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp run fastmcp.json
fastmcp list mcp-config.json
```

**Stdio 命令**连接到任何通过标准 I/O 通信的 MCP Server。使用 `--command` 而不是位置参数：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list --command 'npx -y @modelcontextprotocol/server-github'
```

### 基于名称的解析

如果你的Server已在编辑器或工具中配置，你可以按名称引用它们。FastMCP 扫描来自 Claude Desktop、Claude Code、Cursor、Gemini CLI 和 Goose 的配置：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list weather
fastmcp call weather get_forecast city=London
```

当同一名称出现在多个配置中时，使用 `source:name` 形式来明确：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list claude-code:my-server
fastmcp call cursor:weather get_forecast city=London
```

运行 [`fastmcp discover`](/cli/client#discovering-configured-servers) 以查看你机器上可用的内容。

## 认证

当针对 HTTP URL 时，CLI 默认启用 OAuth 认证。如果Server需要它，你将通过流程进行引导（通常会打开浏览器）。如果不需要，设置是无操作。

要完全跳过认证 —— 对本地开发Server很有用 —— 传递 `--auth none`：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp call http://localhost:8000/mcp my_tool --auth none
```

你还可以直接传递持有者令牌：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list http://localhost:8000/mcp --auth "Bearer sk-..."
```

## 传输覆盖

FastMCP 默认为 URL 目标使用 Streamable HTTP。如果Server仅支持Server发送事件（SSE），请强制使用旧传输：

```bash  theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
fastmcp list http://localhost:8000 --transport sse
```
