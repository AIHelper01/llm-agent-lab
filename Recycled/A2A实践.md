# Python 快速入门教程：构建一个 A2A Agent

欢迎来到 Agent2Agent 快速入门教程！

在本教程中，您将使用 Python SDK 探索一个简单的“回声”A2A server。这将向您介绍A2A server的基本概念和组件。之后，您将查看一个集成了大语言模型的更高级示例。

本实践指南将帮助您理解：

- A2A协议背后的基本概念。
- 如何使用SDK为A2A开发设置Python环境。
- Agent技能和Agent Card如何描述一个Agent。
- A2A server如何处理任务。
- 如何使用client与A2A server交互。
- 流式能力和多轮交互如何工作。
- 如何将LLM集成到A2A agent中。

完成本教程后，您将对A2A agent有一个实用的理解，并为构建或集成符合A2A标准的应用程序打下坚实的基础。

**教程章节**

本教程分为以下步骤：

1. **简介**
2. **设置**：准备您的Python环境和A2A SDK。
3. **Agent技能与Agent Card**：定义您的Agent能做什么以及它如何描述自己。
4. **Agent执行器**：了解Agent逻辑是如何实现的。
5. **启动Server**：运行Helloworld A2A server。
6. **与Server交互**：向您的Agent发送请求。
7. **流式与多轮交互**：通过LangGraph示例探索高级能力。
8. **后续步骤**：探索A2A的更多可能性。

让我们开始吧！





## **环境设置步骤**

**1. 前提条件**

在开始之前，请确保您的系统满足以下要求：

- **Python 3.10 或更高版本**。
- 能够访问终端或命令提示符。
- 已安装 **Git**，用于克隆代码仓库。
- （推荐）安装一个代码编辑器，例如 Visual Studio Code。

**2. 克隆代码仓库**

如果您尚未获取代码，首先需要克隆包含示例的A2A Samples仓库。在终端中执行以下命令：

```
git clone https://github.com/a2aproject/a2a-samples.git -b main --depth 1
cd a2a-samples
```

这个命令会克隆`a2a-samples`仓库的`main`分支（`--depth 1`参数可以只克隆最新的提交，速度更快），然后进入项目目录。

**3. Python 环境与 SDK 安装**

我们推荐为Python项目使用虚拟环境。虽然A2A Python SDK使用`uv`进行依赖管理，但您也可以使用标准的`venv`配合`pip`。

- **创建并激活虚拟环境**

  - **在 Mac/Linux 系统上**：

    ```
    python -m venv .venv
    source .venv/bin/activate
    ```

  - **在 Windows 系统上**：

    ```
    python -m venv .venv
    .venv\Scripts\activate
    ```

    执行成功后，您的命令提示符前会出现`(.venv)`标识，表示已进入虚拟环境。

- **安装所需依赖**

  安装必要的Python依赖包，包括A2A SDK及其依赖：

  ```
  pip install -r samples/python/requirements.txt
  ```

**4. 验证安装**

安装完成后，您可以在Python解释器中导入`a2a`包来验证环境是否配置正确：

```
python -c "import a2a; print('A2A SDK imported successfully')"
```

如果这条命令运行无误，并打印出成功消息，就说明您的环境已正确设置。

好的，我们来详细拆解“3. Agent Skills & Agent Card”这一节的内容。这是A2A Agent开发的基础，定义了Agent能做什么以及如何被外界发现。

## Agent Skills & Agent Card

在A2A Agent能够执行任何操作之前，它需要明确定义两件事：

1. **它能做什么**：这由**Agent Skill**来描述。
2. **其他Agent或Client如何发现它的这些能力**：这由**Agent Card**来公开。

例子位于 `a2a-samples/samples/python/agents/helloworld/`目录中。

### Agent Skill (Agent技能)

**Agent Skill** 描述的是Agent能够执行的**一项具体能力或功能**。它是一个基础构建块，用于告诉Client这个Agent擅长处理哪类任务。

在Python SDK中，`AgentSkill`类在 `a2a.types`中定义，其主要属性包括：

| 属性                              | 说明                                                         |
| --------------------------------- | ------------------------------------------------------------ |
| **`id`**                          | 技能的**唯一标识符**。                                       |
| **`name`**                        | 人类可读的技能名称。                                         |
| **`description`**                 | 关于技能功能的更详细解释。                                   |
| **`tags`**                        | 用于分类和发现的关键词列表。                                 |
| **`examples`**                    | 示例提示或用例列表，帮助理解如何使用此技能。                 |
| **`input_modes`/ `output_modes`** | 技能支持的**输入和输出的媒体类型**（例如，`”text/plain“`, `”application/json“`）。 |
| **`security_requirements`**       | 使用此技能所需的**安全方案**。                               |

**代码示例 (`__main__.py`):**

```
skill = AgentSkill(
    id='hello_world',
    name='Returns hello world',
    description='just returns hello world',
    tags=['hello world'],
    examples=['hi', 'hello world'],
)
```

这个“helloworld”示例中的技能非常简单：它的ID是 `hello_world`，名字是“返回hello world”，主要处理文本交互。它没有显式指定`input_modes`/`output_modes`，因此会使用Agent Card中定义的默认值。

### Agent Card (Agent名片)

**Agent Card** 是一个**JSON文档**，由A2A Server提供，通常发布在 `.well-known/agent-card.json`这样的端点。它就相当于Agent的**数字名片**。

在Python SDK中，`AgentCard`类也在 `a2a.types`中定义，其关键属性包括：

| 属性                                              | 说明                                                         |
| ------------------------------------------------- | ------------------------------------------------------------ |
| **`name`, `description`, `version`**              | Agent的基本身份信息。                                        |
| **`icon_url`**                                    | 代表Agent的图标URL。                                         |
| **`supported_interfaces`**                        | 一个**有序列表**，列出了可以访问此A2A服务的**端点地址和协议**。 |
| **`capabilities`**                                | Agent支持的A2A高级功能，例如流式传输或扩展Agent Card。       |
| **`default_input_modes`/ `default_output_modes`** | Agent默认的**输入和输出媒体类型**。                          |
| **`skills`**                                      | 一个`AgentSkill`对象列表，列出了此Agent提供的**所有技能**。  |

**代码示例 (`__main__.py`):**

```
public_agent_card = AgentCard(
    name='Hello World Agent',
    description='Just a hello world agent',
    icon_url='/',  # 此处为示例，实际应为有效图标URL
    version='1.0.0',
    default_input_modes=['text'],  # 默认接收文本
    default_output_modes=['text'], # 默认输出文本
    capabilities=AgentCapabilities(
        streaming=True,              # 支持流式响应
        extended_agent_card=True     # 支持扩展的、需认证的Agent Card
    ),
    supported_interfaces=[
        AgentInterface(
            protocol_binding='JSONRPC',  # 使用JSON-RPC协议
            url='',               # 服务URL（启动服务器时会填充）
        )
    ],
    skills=[skill],  # 包含之前定义的hello_world技能
)
```

这张Agent Card传达的信息是：

- **身份**：名为“Hello World Agent”。
- **通信方式**：通过**JSONRPC**协议提供服务（URL在服务器启动时确定）。
- **交互类型**：支持文本输入/输出。
- **技能**：提供 `hello_world`技能。
- **高级能力**：支持**流式传输**，并且有一个**需要认证才能获取的扩展配置**。

**总结与重要性**

理解Agent Skill和Agent Card至关重要，因为这是Client**发现一个Agent、了解其能力、并学会如何与之安全、有效交互**的标准化方式。Agent Card是A2A生态系统中**服务发现和自描述**的核心机制。







## The Agent Executor（Agent执行器）

 Agent Executor”（Agent执行器）A2A Agent的“大脑”，负责核心逻辑的处理。

### 核心概念概述

一个A2A Agent如何处理请求并生成响应或事件的核心逻辑，是由一个**Agent Executor**来负责的。A2A Python SDK提供了一个抽象基类 `a2a.server.agent_execution.AgentExecutor`，您需要实现这个类。

### AgentExecutor 接口

`AgentExecutor`类定义了两个主要方法：

| 方法                                                         | 功能描述                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **`async def execute(self, context: RequestContext, event_queue: EventQueue)`** | 处理**传入的请求**。它处理用户的输入，并使用`event_queue`发送回`Message`、`Task`、`TaskStatusUpdateEvent`或`TaskArtifactUpdateEvent`等对象。 |
| **`async def cancel(self, context: RequestContext, event_queue: EventQueue)`** | 处理**取消正在运行的任务**的请求。                           |

- **`RequestContext`**： 提供传入请求的相关信息，例如用户的消息和任何现有的任务详情。
- **`EventQueue`**： 执行器通过这个队列将事件发送回client。

### Helloworld 示例的 Agent Executor

让我们看看 `agent_executor.py`中的实现。它定义了 `HelloWorldAgentExecutor`。

- **The Agent (业务逻辑对象: `HelloWorldAgent`)**:

  这是一个简单的辅助类，封装了实际的“业务逻辑”。

  ```
  class HelloWorldAgent:
      """Hello World Agent."""
  
      async def invoke(self) -> str:
          """Invoke the Hello World agent to generate a response."""
          return 'Hello, World!'
  ```

  它有一个简单的 `invoke`方法，固定返回字符串 `“Hello, World!“`。在真实场景中，这里会是调用模型、处理数据等复杂逻辑。

- **The Executor (执行器: `HelloWorldAgentExecutor`)**:

  这个类实现了 `AgentExecutor`接口。

  1. **`__init__`(初始化)**:

     ```
     class HelloWorldAgentExecutor(AgentExecutor):
         """Test AgentProxy Implementation."""
     
         def __init__(self) -> None:
             self.agent = HelloWorldAgent()  # 实例化业务逻辑对象
     ```

  2. **`execute`(执行)**:

     这是核心方法。当一个请求进来时（在这个简化示例中，无论是 `message/send`还是 `message/stream`请求都由它处理），会执行以下步骤：

     ```
     async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
         """Execute the agent process and enqueue the final response."""
         # 1. 获取当前任务或创建新任务，并将其作为第一个事件放入队列
         task = context.current_task or new_task(context.message)
         await event_queue.enqueue_event(task)
     
         # 2. 放入一个“任务状态更新”事件，告知client：Agent已开始处理（状态为“工作中”）
         await event_queue.enqueue_event(
             TaskStatusUpdateEvent(
                 task_id=context.task_id,
                 context_id=context.context_id,
                 status=TaskStatus(
                     state=TaskState.TASK_STATE_WORKING,
                     message=new_agent_text_message('Processing request...'),
                 ),
             )
         )
     
         # 3. 执行真正的业务逻辑（此处是调用HelloWorldAgent的invoke方法）
         result = await self.agent.invoke()
     
         # 4. 放入一个“任务产物更新”事件，将处理结果（文本“Hello, World!”）发送给client
         await event_queue.enqueue_event(
             TaskArtifactUpdateEvent(
                 task_id=context.task_id,
                 context_id=context.context_id,
                 artifact=new_text_artifact(name='result', text=result),
             )
         )
     
         # 5. 放入一个最终的“任务状态更新”事件，告知client：任务已完成
         await event_queue.enqueue_event(
             TaskStatusUpdateEvent(
                 task_id=context.task_id,
                 context_id=context.context_id,
                 status=TaskStatus(state=TaskState.TASK_STATE_COMPLETED),
             )
         )
     ```

     这个流程清晰地展示了A2A如何通过**事件驱动**的模型来管理任务的生命周期。

  3. **`cancel`(取消)**:

     Helloworld 示例的 `cancel`方法只是简单地抛出一个异常，表明这个基础的Agent不支持取消操作。

     ```
     async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
         """Raise exception as cancel is not supported."""
         raise Exception('cancel not supported')
     ```

     在更复杂的Agent中，您需要在这里实现清理资源、停止子进程等逻辑。

### 总结

`AgentExecutor`充当了**A2A协议**（由请求处理器和服务器应用管理）与**您Agent的特定业务逻辑**之间的**桥梁**。它接收关于请求的上下文信息，并使用一个事件队列将结果或进度更新发送回去。这种设计分离了协议处理和业务逻辑，使得代码结构更清晰，也更易于测试和维护。



好的，我来为您详细讲解“5. Starting the Server”（启动服务器）这一节。

## 启动A2A服务器

这是将我们定义的Agent技能、Agent Card和Agent Executor组合起来，让Agent真正运行起来的关键步骤。

现在我们已经有了Agent Card和Agent Executor，接下来可以设置并启动A2A服务器了。A2A Python SDK提供了`A2AStarletteApplication`类，它简化了运行一个符合A2A标准的HTTP服务器的过程。它使用**Starlette**作为Web框架，通常与**Uvicorn**这样的ASGI服务器一起运行。

### Helloworld 示例中的服务器设置

让我们再次查看`__main__.py`文件，看看服务器是如何初始化和启动的。我将为您详细拆解这段代码。

```python
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)
from agent_executor import (
    HelloWorldAgentExecutor,  # 引入我们之前定义的执行器
)

if __name__ == '__main__':
    # 第一部分：定义技能
    skill = AgentSkill(
        id='hello_world',
        name='Returns hello world',
        description='just returns hello world',
        tags=['hello world'],
        examples=['hi', 'hello world'],
    )
    
    extended_skill = AgentSkill(
        id='super_hello_world',
        name='Returns a SUPER Hello World',
        description='A more enthusiastic greeting, only for authenticated users.',
        tags=['hello world', 'super', 'extended'],
        examples=['super hi', 'give me a super hello'],
    )

    # 第二部分：定义Agent Card
    # 公开的Agent Card（所有人可见）
    public_agent_card = AgentCard(
        name='Hello World Agent',
        description='Just a hello world agent',
        icon_url='',  # 此处为示例，实际应为有效图标URL
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,              # 支持流式传输
            extended_agent_card=True     # 支持扩展Agent Card
        ),
        supported_interfaces=[
            AgentInterface(
                protocol_binding='JSONRPC',
                url='',  # 运行时由uvorn自动填充
            )
        ],
        skills=[skill],  # 只包含基础技能
    )

    # 需认证的扩展Agent Card（仅认证用户可见，包含额外技能）
    specific_extended_agent_card = AgentCard(
        name='Hello World Agent - Extended Edition',
        description='The full-featured hello world agent for authenticated users.',
        icon_url='',  # 此处为示例，实际应为有效图标URL
        version='1.0.1',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,
            extended_agent_card=True
        ),
        supported_interfaces=[
            AgentInterface(
                protocol_binding='JSONRPC',
                url='',  # 运行时由uvorn自动填充
            )
        ],
        skills=[skill, extended_skill],  # 包含基础和扩展技能
    )

    # 第三部分：创建请求处理器
    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),  # 我们的执行器
        task_store=InMemoryTaskStore(),           # 内存任务存储
    )

    # 第四部分：创建A2A服务器应用
    server = A2AStarletteApplication(
        agent_card=public_agent_card,              # 公开Agent Card
        http_handler=request_handler,              # 请求处理器
        extended_agent_card=specific_extended_agent_card,  # 扩展Agent Card
    )

    # 第五部分：启动服务器
    uvicorn.run(server.build(), host='', port=9999)
```

让我们逐步分解这段代码：

### 核心组件解析

| 组件                                   | 作用               | 说明                                                         |
| -------------------------------------- | ------------------ | ------------------------------------------------------------ |
| **`DefaultRequestHandler`**            | **请求处理器**     | 这是SDK提供的默认请求处理器。它接收您的`AgentExecutor`实现（这里是`HelloWorldAgentExecutor`）和一个`TaskStore`（这里是`InMemoryTaskStore`）。它负责将传入的A2A RPC调用路由到您执行器的适当方法（如`execute`或`cancel`）。 |
| **`TaskStore`**                        | **任务存储**       | 用于管理任务的整个生命周期，特别是有状态交互、流式传输和重新订阅。即使您的执行器很简单，处理器也需要一个任务存储。这里使用内存存储`InMemoryTaskStore`。 |
| **`A2AStarletteApplication`**          | **A2A服务器应用**  | 这个类用`agent_card`、`request_handler`（在其构造函数中名为`http_handler`）和可选的`extended_agent_card`来实例化。 1. **`agent_card`**：在`/.well-known/agent-card.json`端点公开，用于公共发现。 2. **`request_handler`**：处理所有传入的A2A方法调用，与您的`AgentExecutor`交互。 3. **`extended_agent_card`**：为认证用户提供额外的能力和技能，通过`GetExtendedAgentCard`RPC方法公开。 |
| **`uvicorn.run(server.build(), ...)`** | **启动HTTP服务器** | `A2AStarletteApplication`有一个`build()`方法来构建实际的Starlette应用。然后使用`uvicorn.run()`运行此应用，使您的Agent可通过HTTP访问。 - **`host=''`**：使服务器**仅可从本地机器访问**。 - **`port=9999`**：指定监听的端口，这与Agent Card中`supported_interfaces`定义的端点一致。 |

### 运行 Helloworld 服务器

1. **导航到正确目录**：在终端中，确保您位于`a2a-samples`目录下，并且您的虚拟环境已激活。

2. **运行服务器**：执行以下命令：

   ```
   python samples/python/agents/helloworld/__main__.py
   ```

3. **验证运行**：您应该看到类似以下的输出，表明服务器正在运行：

   ```
   INFO: Started server process [xxxxx]
   INFO: Waiting for application startup.
   INFO: Application startup complete.
   INFO: Uvicorn running on http://:9999 (Press CTRL+C to quit)
   ```

**恭喜！**您的A2A Helloworld Agent现在已经在线并正在监听请求了。在下一步中，我们将学习如何与它进行交互。



## 与服务器交互

现在服务器已经在运行，我们将学习如何使用SDK提供的客户端（`A2AClient`）向它发送请求

Helloworld A2A服务器正在运行，让我们向它发送一些请求。SDK包含一个客户端（`A2AClient`），可以简化这些交互。

### 运行测试客户端

`test_client.py`脚本展示了如何：

1. 从服务器**获取Agent Card**。
2. 创建一个`A2AClient`实例。
3. 发送**非流式**和**流式**请求。

**操作步骤**：

1. 打开一个新的终端窗口，激活虚拟环境，并导航到`a2a-samples`目录。

2. 激活虚拟环境：

   ```
   # 在 Mac/Linux 上：
   source .venv/bin/activate
   ```

3. 运行测试客户端：

   ```
   # 确保在 a2a-samples 目录下
   python samples/python/agents/helloworld/test_client.py
   ```

### 理解客户端代码

让我们看看`test_client.py`的关键部分：

- **获取Agent Card**：

  ```
  base_url = ''
  
  async with httpx.AsyncClient() as httpx_client:
      # 初始化 A2ACardResolver
      resolver = A2ACardResolver(
          httpx_client=httpx_client,
          base_url=base_url,
      )
  ```

  `A2ACardResolver`是一个便利类，它首先从服务器的`/.well-known/agent-card.json`端点获取Agent Card，然后用它来初始化客户端。

- **初始化客户端并发送非流式消息**：

  ```
  # 使用获取到的Agent Card创建客户端
  async with ClientFactory.create_client(resolver) as client:
      # 构造用户消息
      message = Message(
          role=Role.ROLE_USER,
          parts=[Part(text="Say hello.")],
      )
      request = SendMessageRequest(message=message)
  
      # 发送消息（非流式）
      async for chunk in client.send_message(request):
          print(chunk)
  ```

  `ClientFactory`根据获取到的卡片创建一个**非流式**客户端。然后构造一个`Message`对象，包含用户角色和内容。将其包装在`SendMessageRequest`中，并通过客户端的`send_message`方法发送。该方法返回一个异步生成器，按顺序产生Agent返回的一系列`Task`事件。

- **初始化客户端并发送流式消息**：

  ```
  # 创建流式客户端
  async with ClientFactory.create_client(
      resolver, 
      config=ClientConfig(streaming=True)
  ) as client:
      # 再次发送相同的消息，但这次是流式传输
      request = SendMessageRequest(message=message)
  
      async for chunk in client.send_message(request):
          print(f"Response chunk:\n{chunk}")
  ```

  一个新的**流式**客户端通过`ClientFactory`创建，配置了`streaming=True`。再次调用`send_message`（这个方法名相同，但会根据`ClientConfig`和Agent的能力来处理流式或非流式）。响应会动态地生成`Task`事件，因为它们通过网络流式传输。

### 预期输出

当您运行`test_client.py`时，您会看到以protobuf文本格式输出的：

1. **非流式响应**：一个最终的任务日志，详细记录了历史记录、状态和包含“Hello, World!”文本的生成产物。
2. **流式响应**：多个离散的事件，包括初始任务、状态更新和包含“Hello, World!”文本的最终产物更新。

输出中的`id`字段每次运行都会不同。

**非流式响应示例**（已格式化以便阅读）：

```
task {
  id: "xxxxxxxx"
  context_id: "yyyyyyyy"
  status {
    state: TASK_STATE_COMPLETED
  }
  artifacts {
    artifact_id: "zzzzzzzz"
    name: "result"
    parts {
      text: "Hello, World!"
    }
  }
  history {
    message_id: "vvvvvvvv"
    context_id: "yyyyyyyy"
    task_id: "xxxxxxxx"
    role: ROLE_USER
    parts {
      text: "Say hello."
    }
  }
  history {
    message_id: "wwwwwwww"
    role: ROLE_AGENT
    parts {
      text: "Processing request..."
    }
  }
}
```

**流式响应示例**（分块输出）：

```
// 第一个响应块：初始任务
task {
  id: "xxxxxxxx-s"
  context_id: "yyyyyyyy-s"
  status {
    state: TASK_STATE_SUBMITTED
  }
  history {
    message_id: "vvvvvvvv-s"
    context_id: "yyyyyyyy-s"
    task_id: "xxxxxxxx-s"
    role: ROLE_USER
    parts {
      text: "Say hello."
    }
  }
}

Response chunk:
// 第二个响应块：状态更新（工作中）
status_update {
  task_id: "xxxxxxxx-s"
  context_id: "yyyyyyyy-s"
  status {
    state: TASK_STATE_WORKING
    message {
      message_id: "zzzzzzzz-s"
      role: ROLE_AGENT
      parts {
        text: "Processing request..."
      }
    }
  }
}

Response chunk:
// 第三个响应块：产物更新（包含结果）
artifact_update {
  task_id: "xxxxxxxx-s"
  context_id: "yyyyyyyy-s"
  artifact {
    artifact_id: "wwwwwwww-s"
    name: "result"
    parts {
      text: "Hello, World!"
    }
  }
}

Response chunk:
// 第四个响应块：最终状态更新（完成）
status_update {
  task_id: "xxxxxxxx-s"
  context_id: "yyyyyyyy-s"
  status {
    state: TASK_STATE_COMPLETED
  }
}
```

**注意**：实际的ID（如`xxxxxxxx`, `yyyyyyyy`等）每次运行都会是不同的UUID/请求ID。

这表明您的服务器正在正确处理基本的A2A交互！现在，您可以在运行`__main__.py`的终端窗口中按`Ctrl+C`来关闭服务器。





## 流式与多轮交互（LangGraph 示例）

Hello World 示例展示了 A2A 的基本机制。要了解更高级的功能，如稳健的流式传输、任务状态管理以及由大型语言模型（LLM）驱动的多轮对话，我们将转向位于 `a2a-samples/samples/python/agents/langgraph/`的 **LangGraph 示例**。

此示例展示了一个“货币 Agent”，它通过 LangChain 和 LangGraph 使用 Gemini 模型来回答货币兑换问题。

**设置 LangGraph 示例**

1. **创建 Gemini API 密钥**：如果您还没有，请创建一个。

2. **设置环境变量**：在 `a2a-samples/samples/python/agents/langgraph/`目录中创建一个 `.env`文件：

   ```
   echo "GOOGLE_API_KEY=YOUR_API_KEY_HERE" > .env
   ```

   将 `YOUR_API_KEY_HERE`替换为您实际的 Gemini API 密钥。

3. **安装依赖**：LangGraph 示例有自己的 `pyproject.toml`文件，包含了 `langchain-google-genai`和 `langgraph`等依赖项。当您从 `a2a-samples`根目录使用 `pip install -e .[dev]`安装 SDK 时，应该已同时安装了工作区示例（包括 langgraph-example）的依赖项。如果您遇到导入错误，请确保您从根目录进行的 SDK 安装是成功的。

**运行 LangGraph 服务器**

1. 在终端中，导航到 `a2a-samples/samples/python/agents/langgraph/app`目录，并确保您的虚拟环境（来自 SDK 根目录）已激活。

2. 启动 LangGraph Agent 服务器：

   ```
   python __main__.py
   ```

   这将启动服务器，通常运行在 `http://localhost:10000`。

**与 LangGraph Agent 交互**

打开一个新的终端窗口，激活您的虚拟环境，并导航到 `a2a-samples/samples/python/agents/langgraph/app`。运行其测试客户端：

```
python test_client.py
```

现在，您可以在运行 `__main__.py`的终端窗口中按 `Ctrl+C`来关闭服务器。

**展示的关键功能**

LangGraph 示例展示了几个重要的 A2A 概念：

- **LLM 集成**：

  - `agent.py`定义了 `CurrencyAgent`。它使用 `ChatGoogleGenerativeAI`和 LangGraph 的 `create_react_agent`来处理用户查询。这展示了如何用真实的 LLM 驱动 Agent 的逻辑。

- **任务状态管理**：

  - 在 `samples/langgraph/__main__.py`中，使用 `InMemoryTaskStore`初始化 `DefaultRequestHandler`。

  ```
  httpx_client = httpx.AsyncClient()
  push_config_store = InMemoryPushNotificationConfigStore()
  push_sender = BasePushNotificationSender(httpx_client=httpx_client,
                  config_store=push_config_store)
  request_handler = DefaultRequestHandler(
      agent_executor=CurrencyAgentExecutor(),
      task_store=InMemoryTaskStore(),
      push_config_store=push_config_store,
      push_sender= push_sender
  )
  server = A2AStarletteApplication(
      agent_card=agent_card, http_handler=request_handler
  )
  
  uvicorn.run(server.build(), host=host, port=port)
  ```

  

  - `CurrencyAgentExecutor`（在 `samples/langgraph/agent_executor.py`中）的 `execute`方法被 `DefaultRequestHandler`调用时，会与包含当前任务（如果有）的 `RequestContext`交互。

  - 对于 `message/send`请求，`DefaultRequestHandler`使用 `TaskStore`在多个交互中持久化和检索任务状态。如果 Agent 的执行流程涉及多个步骤或产生了持久性任务，`message/send`的响应将是一个完整的 `Task`对象。

  - `test_client.py`中的 `run_single_turn_test`演示了如何获取一个 `Task`对象，然后使用 `get_task`查询它。

- **流式传输**：

  - `CurrencyAgentExecutor`中的 `execute`方法负责处理由 `DefaultRequestHandler`编排的**非流式**和**流式**请求。

  - 当 LangGraph Agent 处理请求时（可能涉及调用像 `get_exchange_rate`这样的工具），`CurrencyAgentExecutor`会将不同类型的事件放入 `EventQueue`：

    - `TaskStatusUpdateEvent`：用于中间更新（例如，“正在查找汇率...”，“正在处理汇率...”）。

    - `TaskArtifactUpdateEvent`：当最终答案准备就绪时，它被作为产物放入队列。`lastChunk`标志为 `True`。

  - 发送一个 `state=TaskState.completed`的最终 `TaskStatusUpdateEvent`来标记任务的结束，并关闭流。`test_client.py`中的 `run_streaming_test`函数会打印从服务器接收到的这些独立事件块。

- **多轮对话**：

  - `CurrencyAgent`可以要求澄清模糊的查询（例如，用户问“100 美元等于多少？”）。

  - 当发生这种情况时，`CurrencyAgentExecutor`会放入一个 `TaskStatusUpdateEvent`，其中 `status.state`是 `TaskState.input_required`，并且 `status.message`包含 Agent 的问题（例如，“您想兑换成哪种货币？”）。此事件之后流会关闭。

  - `test_client.py`中的 `run_multi_turn_test`函数演示了这一点：

    - 它发送一个初始的模糊查询。
  
    - Agent 响应一个状态为 `input_required`的 `Task`。
  
    - 客户端随后发送第二条消息，包含来自第一轮 `Task`响应的 `taskId`和 `contextId`，以提供缺失的信息（“兑换成 GBP”）。这将继续同一个任务。

**探索代码**

花些时间查看这些文件：

- **`__main__.py`**：使用 `A2AStarletteApplication`和 `DefaultRequestHandler`的服务器设置。注意 `AgentCard`定义中包含 `capabilities.streaming=True`。
- **`agent.py`**：包含 LangGraph、LLM 模型和工具定义的 `CurrencyAgent`。
- **`agent_executor.py`**：实现 `execute`（和 `cancel`）方法的 `CurrencyAgentExecutor`。它使用 `RequestContext`来理解正在进行的任务，并使用 `EventQueue`发回各种事件。
- **`test_client.py`**：演示各种交互模式，包括检索任务 ID 并将其用于多轮对话。

此示例更丰富地展示了 A2A 如何促进 Agent 之间复杂、有状态和异步的交互。