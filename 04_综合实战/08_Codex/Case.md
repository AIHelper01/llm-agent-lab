



# Codex使用样例

官网：https://learn.chatgpt.com/use-cases

![image-20260922133755788](E:\llm-agent-lab\04_综合实战\08_Codex\assets\ccc1.png)

在每个usecase里都会提及到两个关键词： Skills & Plugins  以及  Starter Prompt

以下为示例： 

![image-20260922135224858](E:\llm-agent-lab\04_综合实战\08_Codex\assets\ccc2.png)

# Skills & Plugins

## Plugins

将ChatGPT和Codex扩展为可重复使用的技能和外部服务的连接。发布一次到通用插件目录。

![image-20260922135321445](E:\llm-agent-lab\04_综合实战\08_Codex\assets\ccc3.png)

# 插件架构

理解插件如何结合技能、MCP服务器和可选界面。

插件是人们发现、安装、分享和发布的软件包 ChatGPT和Codex。一个插件可以包含：

- **这些技能**为模型提供可重复的指令和资源 工作流程。
- **一个MCP服务器**，可以暴露工具并连接到外部系统。
- **技能和MCP服务器**在模型需要工作流程指导时 服务器支持的功能。
- 生命周期**钩子在**Codex中配置的节点执行命令 运行时，包括 ChatGPT Work 和 Codex。

ChatGPT 和 Codex 共享一个通用插件目录。当你发布 公开插件，人们可以在支持的表面上发现相同的列表 无论哪种产品。单个能力仍可能针对表面特定;对于 例如，钩子脚本必须在执行环境中可用。 在网页上安装插件并不会部署这些脚本。请参阅[捆绑钩子](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks)中的设置和信任要求。

MCP服务器可以返回结构化数据和模型可读文本，而无需 自定义界面。当任务受益于视觉交互时，服务器也可以 返回一个UI资源。

```
Plugin
├── Skills
└── MCP server (optional)
    ├── Tools and structured results
    └── UI resources (optional)
```



从支持你使用场景的最小形状开始。你可以添加一个MCP 服务器或UI后用，而不改变插件的用途。

## 技能

技能是一个包含文件的文件夹，并在需要时提供支持文件 脚本、参考、模板或资源。技能描述何时使用 工作流程、应遵循的步骤以及成功结果应有的样子。`SKILL.md`

当说明和模型已有的工具 足以完成任务。插件可以打包一个技能或与团队相关的技能 技能融合成一个可安装的体验。

例如，会议后续插件可能包含以下独立技能 起草总结、确定行动事项并准备客户邮件。

写技能指导时，遵循[指令遵循指导](https://developers.openai.com/plugins/build/skills#review-instruction-following)。

## MCP服务器

当你的插件必须连接到某个服务时，构建一个MCP服务器，暴露一个 可控的工具集，认证用户，或在基础设施上运行行为 你来做手术。服务器定义：

- 模型可以调用的工具。
- 这些工具的输入和输出模式。
- 认证和授权要求。
- 结构化的结果和模型可读的内容。
- 可选的用户界面资源。

MCP服务器让你控制你暴露哪些能力。它还 你可以独立更新服务器行为，并观察收到的请求 你的基础设施。

## 可选用户界面

MCP服务器不需要自定义UI。使用模型响应或结构化 当他们传达结果时，结果。

当人们需要检查、比较、编辑、确认或导航时，添加用户界面 结构化信息。例如，产品比较、可编辑的日程表， 或者地图可以受益于组件，而背景状态查询则通常如此 不。

ChatGPT 支持开放[的 MCP 应用界面 标准](https://developers.openai.com/plugins/build/chatgpt-ui#start-with-mcp-apps)。先从共享的开始 标准版，只有在UI需要时才添加可选的ChatGPT扩展 该标准未涵盖的能力。保持工具有用，没有 组件，模型可以完成无头工作流程并决定何时添加 UI。 价值。

## 选择插件形状

| 形状                  | 选择它                                              |
| --------------------- | --------------------------------------------------- |
| 仅限技能              | 说明书和现有工具足以完成整个工作流程。              |
| 仅限MCP服务器         | 插件需要MCP工具，但不需要额外的工作流程说明。       |
| 技能与MCP服务器       | 技能应引导模型通过使用MCP工具的工作流程。           |
| 带用户界面的MCP服务器 | 视觉交互在 MCP 支持的工作流程中显著改善了部分内容。 |

选定形态后，[培养技能](https://developers.openai.com/plugins/build/skills)或[MCP服务器](https://developers.openai.com/plugins/build/mcp-server)。只有在使用场景时才向[MCP](https://developers.openai.com/plugins/build/chatgpt-ui)服务器添加UI。 需要它，然后[打包插件](https://developers.openai.com/plugins/build/plugins)。

# 技能

理解技能如何为MCP工具带来可重复的工作流程。

技能是包含指令和资源的文件夹，用于教授ChatGPT和Codex 如何完成可重复的工作流程。在MCP支持的插件中，技能 通过教模型如何组合其工具来补充服务器 可识别的用户目标。

每个技能都有一个文件，内容包括：`SKILL.md`

- 一个名字。
- 描述告诉模特何时考虑该技能。
- 完成工作流程的说明。
- 可选引用、脚本、模板及其他资源。

## 技能如何补充MCP服务器

MCP服务器提供实时信息和受控操作。一项技能 提供围绕这些工具的工作流程：何时调用它们，按何顺序调用，如何调用 处理不完整的结果，以及最终输出应包含的内容。

例如，一个技能可以定义如何：

- 检索账户活动并转化为客户简报。
- 审查项目数据，识别风险，并起草状态更新。
- 将搜索和取物工具结合进有来源的研究流程。
- 将组织的写作或评论标准应用于MCP结果。

保持边界清晰：[MCP服务器](https://developers.openai.com/plugins/concepts/mcp-server)提供数据、认证、授权和操作;技能提供 可重复使用的说明、示例、模板及其他资源。技能可以 当工作流程只需打包时，也能在没有MCP服务器的情况下工作 说明和资源。

## 技能激活方式

模型首先看到技能元数据，包括名称和描述。它 当用户请求与技能匹配时，加载完整指令 用户直接调用它。

围绕用户目标和应触发的条件写描述 工作流程。在指令中详细记录步骤和输出要求 身体。

## 插件中的技能

技能是插件的工作流程层。他们可以：

- 通过插件MCP服务器暴露的工具引导模型。
- 将组织特定的流程打包，并附上可复用的模板， 参考资料。
- 当不需要实时数据或受控操作时，他们自己工作。

技能和MCP工具应有明确且互补的角色。一个技能解释 如何完成工作流程;MCP服务器提供实时信息， 强制执行受控行动。

继续进行[“构建技能](https://developers.openai.com/plugins/build/skills)以创建、测试和 打包技能。

# MCP服务器

理解MCP服务器如何为插件提供工具和外部系统的访问权限。

[模型上下文协议](https://modelcontextprotocol.io/)（MCP）是一个开放的 用于连接AI客户端与外部工具和数据的规范。一个插件 当需要读取实时信息、执行操作时，可以包含MCP服务器， 或者与其他服务整合。

MCP服务器是可选的。一个只提供指令和 资源可以仅包含[技能](https://developers.openai.com/plugins/concepts/skills)。

## MCP服务器所提供的服务

MCP服务器可以暴露：

- **工具：**模型可以通过结构化输入调用函数。
- **资源：**客户可以读取的数据或内容。
- **提示：**可重复使用的提示模板。
- **说明：**全服务器范围内的使用指导。

插件主要使用工具。每个工具都有名称、描述、输入模式， 以及可选的输出模式。这些字段帮助模型决定何时调用 工具以及如何使用其结果。

## 工具调用的工作原理

当用户请求与工具匹配的物品时：

1. 客户端发现MCP服务器暴露的工具。
2. 模型选择工具并提供与其输入模式相匹配的参数。
3. 服务器验证请求，执行操作，并返回 结果。
4. 模型利用结果继续对话。

工具结果应该不需要自定义UI也能正常使用。返回简洁文本或结构化 提供模型足够信息以回答用户的问题。一个MCP 服务器还可以为支持 [MCP 应用](https://developers.openai.com/plugins/build/chatgpt-ui#start-with-mcp-apps)的客户端返回可选的 UI 资源。

## 运输与授权

在稳定的HTTPS端点部署生产MCP服务器，使用可流媒体 HTTP 传输。如果工具访问私人数据或为用户执行操作， 保护服务器时，MCP定义的授权流程 规格。

有关协议的详细信息，请参见[MCP规范](https://modelcontextprotocol.io/specification)。[Python](https://github.com/modelcontextprotocol/python-sdk) 和 [TypeScript](https://github.com/modelcontextprotocol/typescript-sdk) 软件 开发套件提供服务器实现和辅助工具。





# 重点讲Agent Skills原理

**Agent Skills** 是 Anthropic 在 Claude 中提出并推广的一种模块化能力扩展机制。一个 Skill 通常包含描述其用途和使用方式的指令及元数据，也可以附带脚本、模板等资源。Claude 会根据任务需要发现并加载相应的 Skill。随后，Codex、OpenClaw 等 Agent 产品也支持类似机制，使特定任务的知识、操作步骤和工作流程可以被封装与复用。

**参考资料：**[Anthropic：为智能体装备真实世界的 Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## 为什么使用 Skills

Skills 是可复用的、基于文件系统的资源，为 Claude 提供特定领域的专业知识：工作流程、上下文和最佳实践，将通用智能体转变为专家。与提示词（针对一次性任务的对话级指令）不同，Skills 按需加载，无需在多次对话中反复提供相同的指导。

**主要优势**：

- **专业化 Claude**：为特定领域任务定制能力
- **减少重复**：创建一次，自动使用
- **组合能力**：组合 Skills 构建复杂工作流程

## Skills 和 Prompt 

Skills 和传统 Prompt 最大的区别是：按需加载 + 渐进式披露（只在需要时才把厚厚的 SOP 塞进上下文，极大节省 token）。

| 对比项           | 普通 Prompt              | Skills 机制                          |
| :--------------- | :----------------------- | :----------------------------------- |
| 每次都要重新描述 | 是                       | 否（只描述一次）                     |
| 上下文长度占用   | 每次全量塞入             | 渐进式加载（只在触发时才读完整内容） |
| 一致性           | 依赖每次 prompt 质量     | 高（固定 SOP + 模板）                |
| 复用性           | 手动复制粘贴             | 自动匹配 / slash 命令 / 项目共享     |
| 维护方式         | 改一次 prompt 就要重新发 | 修改 SKILL.md 文件，全局/项目生效    |

比如我们平时写文章，在没有 Skills 之前，每次都要按以下步骤重复说：

```
帮我总结文章 → 翻译 → 改成公众号风格 → 加标题 → 输出 Markdown
```

有了 Skills 之后：

你只需要一句：

```
使用「技术文章转公众号」Skill
```

AI 会自动按你设定的步骤执行。

把 AI 想象成一个**刚毕业的聪明但没经验的实习生**：

- **普通Prompt** = 你每次都要从头教他怎么做事（今天教一遍，明天还得重新教）
- **Rule / 记忆** = 你给他贴一张"公司行为守则"在工位上（一直生效，但只能管态度和格式）
- **MCP / Tools** = 你给他电脑装了一堆软件和API（他能调用外部工具，但不知道什么时候该用、怎么组合用）
- **Skills** = 你直接给他一整套**"岗位培训大礼包"**（PDF+流程图+SOP+话术模板+常用脚本），告诉他："当老板让你做这类事情时，就按这个文件夹里的方法来做"

## Skills 和 MCP

Skills 和传统 Prompt 最大的区别是：按需加载 + 渐进式披露（只在需要时才把厚厚的 SOP 塞进上下文，极大节省 token）。

**Skills 与 MCP 的区别：** Skills 用于**知识复用**，MCP 用于**能力扩展**。

### Skills

知识复用

- 知识分享：经验、最佳实践、工作流程
- 基于简单的 Markdown 文件，任何人都可以创建
- 渐进式加载，Token 使用效率高
- 无需服务器或后端设置
- 适用于 Web / Desktop / CLI

### MCP

能力扩展

- 功能扩展：连接 API、数据库、外部工具
- 需要编码能力和服务器端配置
- 启动时加载全部工具定义
- 对外部系统集成能力强
- 更高的 Token 消耗与复杂度

## Skills的本质

Skills 本质上就是教 AI 按固定流程做事的操作说明书，一旦写好，就能像函数一样反复调用。

我们可以把 Skills 看成把 **某类事情应该怎么专业做** 这件事，封装成一个可复用、可自动触发的能力模块。

Skills 以 Markdown 文件形式存在，不执行功能，而是通过按需、渐进式加载，实现高效且可复用的经验传递。

![img](https://www.runoob.com/wp-content/uploads/2026/01/skills-agent-runoob.svg)

## Skill 结构

Skills 的核心就是：**一个文件夹 + 一个 SKILL.md 文件**。

一个 Skill 本质上就是一个 Markdown 文件（文件名固定为 SKILL.md）

```
my-skill/
└── SKILL.md   （唯一必需）
```

![img](https://www.runoob.com/wp-content/uploads/2026/01/b3eb7f1a-4905-49a6-bda7-976b1415e213.png)

**每个 Skill 都需要一个带有 YAML 前置内容的 `SKILL.md` 文件，SKILL.md 文件包含：**

- 元数据（至少要有名称和描述）
- 告诉 AI 如何完成某一特定任务的指令

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
```

**必填字段**：`name` 和 `description`

**字段要求**：

`name`：

- 最多 64 个字符
- 只能包含小写字母、数字和连字符
- 不能包含 XML 标签
- 不能包含保留词："anthropic"、"claude"

`description`：

- 不能为空
- 最多 1024 个字符
- 不能包含 XML 标签

`description` 应包含 Skill 的功能以及 Claude 应何时使用它。

最小必填示例:

```
---
name: skill-name
description: 说明该 Skill 的功能以及适用场景
---
```

含可选字段示例:

```
---
name: pdf-processing
description: 从 PDF 中提取文本和表格，填写表单，并合并文档
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

| 字段          | 必需 | 说明                                                         |
| :------------ | :--- | :----------------------------------------------------------- |
| name          | 是   | Skill 名称，最长 64 字符，只能使用小写字母、数字和 `-`，且不能以 `-` 开头或结尾 |
| description   | 是   | 功能与使用场景说明，最长 1024 字符，不能为空                 |
| license       | 否   | 许可证名称或指向随 Skill 附带的许可证文件                    |
| compatibility | 否   | 环境与依赖说明（产品、系统包、网络权限等），最长 500 字符    |
| metadata      | 否   | 自定义键值对，用于扩展元数据（如作者、版本号）               |
| allowed-tools | 否   | 允许使用的工具列表（空格分隔，实验性功能）                   |

如果你需要一些参考资料，参考实例，执行脚本，可以使用更复制 Skill 的目录结构：

```
my-skill/
├── SKILL.md      # 必需：指令 + 元数据
├── scripts/      # 可选：可执行代码
├── references/   # 可选：文档资料
└── assets/       # 可选：模板、资源
```



每个 Skill 就是一个文件夹，文件夹名即技能标识（推荐 kebab-case 小写+连字符）。

### 最简结构

```
~/.claude/skills/
  └── code-comment-expert/          # 技能文件夹名
      └── SKILL.md                  # 唯一必填文件（必须全大写 + .md 小写）
```

SKILL.md 完整格式：

```
---                                 #  YAML frontmatter 开始（顶格）
name: code-comment-expert           # 必填：技能名（也是 /slash 命令名）
description: >-                     # 必填：最关键一行！Claude 靠它判断是否加载
  为代码添加专业、清晰的中英双语注释。
  适合缺少文档、可读性差、需要分享审查的代码。
  常见触发场景：加注释、注释一下、加文档、explain this、improve readability

trigger_keywords:                   # 强烈推荐（大幅提升自动触发率）
  - 加注释
  - 注释
  - 加文档
  - explain code
  - document
  - comment this
  - readability

version: 1.0                        # 可选
author: yourname                    # 可选
---                                 # ← YAML 结束

# 这里开始是正文（Markdown）—— Claude 真正执行时的指令

你现在是「专业代码注释专家」。

## 核心原则
- 只在缺少注释或可读性明显不足处添加
- 优先使用英文 JSDoc / TSDoc 风格
- 复杂逻辑 / 非明显意图处额外加一行中文解释
- 注释精炼，每行不超过 80 字符
- 绝不修改原有逻辑

## 输出格式（严格遵守）
1. 先输出完整修改后的代码块（用 ```语言 包裹）
2. 再用 diff 形式展示只改动注释的部分
3. 最后说明加了哪些注释、理由

现在直接开始处理用户提供的代码，不要闲聊。
```

### 进阶文件结构（技能变复杂时推荐）

当技能超过 500–800 行，或需要模板/脚本/参考资料时，推荐以下组织方式：

```
~/.claude/skills/react-component-review/
  ├── SKILL.md                  # 核心指令 + 元数据（建议控制在 400 行内）
  │
  ├── templates/                # 常用模板（Claude 按需读取）
  │   ├── functional.tsx.md
  │   └── class-component.md
  │
  ├── examples/                 # 优秀/反例（给 Claude 看标准）
  │   ├── good.md
  │   └── anti-pattern.md
  │
  ├── references/               # 规范、规则、禁用词表
  │   ├── hooks-rules.md
  │   └── naming-convention.md
  │
  └── scripts/                  # 可执行脚本（需开启 code execution）
      ├── validate-props.py
      └── check-cycle-deps.sh
```

在 SKILL.md 中引用方式示例：

```
Markdown需要给出标准函数组件时，参考 templates/functional.tsx.md 的结构。

如果违反 Hooks 规则，对照 references/hooks-rules.md 第 3–5 条说明。

如需校验 propTypes，可执行 scripts/validate-props.py "{代码片段}"。
```

Claude 看到路径引用后，会按需加载对应文件，而不是一次性全部塞入上下文，极大节省 token。



## Skills 的工作原理

Skills 利用 Claude 的虚拟机环境提供仅靠提示词无法实现的能力。Claude 在具有文件系统访问权限的虚拟机中运行，允许 Skills 以包含指令、可执行代码和参考材料的目录形式存在，其组织方式类似于您为新团队成员创建的入职指南。

这种基于文件系统的架构实现了**渐进式披露**：Claude 按需分阶段加载信息，而不是预先消耗上下文。

Skills用渐进式加载来高效管理上下文：

- **发现：**启动时，AI 只加载每个技能的名称和描述，只保留最基本的识别信息。
- **激活：**当任务匹配某个技能的描述时，AI 才把完整的 SKILL.md 指令读入上下文。
- **执行：**AI 按照指令执行，按需加载参考文件或运行代码。

这种设计让 AI 保持快速，同时能按需获取更多信息。

### 三种类型的 Skill 内容，三个加载级别

Skills 可以包含三种类型的内容，每种内容在不同时间加载：

### 第一级：元数据（始终加载）

**内容类型：指令**。Skill 的 YAML 前置内容提供发现信息：

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Claude 在启动时加载此元数据并将其包含在系统提示中。这种轻量级方法意味着您可以安装许多 Skills 而不会产生上下文损耗；Claude 只知道每个 Skill 的存在以及何时使用它。

### 第二级：指令（触发时加载）

**内容类型：指令**。SKILL.md 的主体包含程序性知识：工作流程、最佳实践和指导：

````markdown
# PDF Processing

## Quick start

Use pdfplumber to extract text from PDFs:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For advanced form filling, see [FORMS.md](FORMS.md).
````

当您的请求与 Skill 的描述匹配时，Claude 通过 bash 从文件系统读取 SKILL.md。只有在那时，这些内容才会进入上下文窗口。

### 第三级：资源和代码（按需加载）

**内容类型：指令、代码和资源**。Skills 可以捆绑额外的材料：

```text
pdf-skill/
├── SKILL.md (main instructions)
├── FORMS.md (form-filling guide)
├── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (utility script)
```

**指令**：包含专业指导和工作流程的额外 markdown 文件（FORMS.md、REFERENCE.md）

**代码**：Claude 通过 bash 运行的可执行脚本（fill_form.py、validate.py）；脚本提供确定性操作而不消耗上下文

**资源**：参考材料，如数据库模式、API 文档、模板或示例

Claude 仅在被引用时才访问这些文件。文件系统模型意味着每种内容类型都有不同的优势：指令用于灵活指导，代码用于可靠性，资源用于事实查询。

| 级别               | 加载时机       | Token 成本                 | 内容                                             |
| ------------------ | -------------- | -------------------------- | ------------------------------------------------ |
| **第一级：元数据** | 始终（启动时） | 每个 Skill 约 100 个 token | YAML 前置内容中的 `name` 和 `description`        |
| **第二级：指令**   | 触发 Skill 时  | 不超过 5k token            | 包含指令和指导的 SKILL.md 主体                   |
| **第三级+：资源**  | 按需           | 实际上无限制               | 通过 bash 执行的捆绑文件，不将内容加载到上下文中 |

![Anthropic：Skill 的渐进式披露](https://www-cdn.anthropic.com/images/4zrzovbb/website/a3bca2763d7892982a59c28aa4df7993aaae55ae-2292x673.jpg)

渐进式披露确保在任何给定时间，只有相关的 Skill 内容占用上下文窗口。



### Skills 架构

Skills 在代码执行环境中运行，Claude 在该环境中具有文件系统访问权限、bash 命令和代码执行能力。可以这样理解：Skills 以目录形式存在于虚拟机上，Claude 使用与您在计算机上导航文件相同的 bash 命令与它们交互。

![skill01](E:\ai-showcase\3.4大模型-Agent\assets\skill01.png)

**Claude 如何访问 Skill 内容：**

当 Skill 被触发时，Claude 使用 bash 从文件系统读取 SKILL.md，将其指令带入上下文窗口。如果这些指令引用了其他文件（如 FORMS.md 或数据库模式），Claude 也会使用额外的 bash 命令读取这些文件。当指令提到可执行脚本时，Claude 通过 bash 运行它们，只接收输出（脚本代码本身永远不会进入上下文）。

**这种架构实现了什么：**

**按需文件访问**：Claude 只读取每个特定任务所需的文件。一个 Skill 可以包含数十个参考文件，但如果您的任务只需要销售模式，Claude 只加载那一个文件。其余文件保留在文件系统上，消耗零 token。

**高效的脚本执行**：当 Claude 运行 `validate_form.py` 时，脚本的代码永远不会加载到上下文窗口中。只有脚本的输出（如"验证通过"或特定错误消息）消耗 token。这使得脚本比让 Claude 即时生成等效代码效率高得多。

**捆绑内容无实际限制**：由于文件在被访问之前不消耗上下文，Skills 可以包含全面的 API 文档、大型数据集、大量示例或您需要的任何参考材料。未使用的捆绑内容不会产生上下文损耗。

这种基于文件系统的模型使渐进式披露得以实现。Claude 像您参考入职指南的特定部分一样导航您的 Skill，精确访问每个任务所需的内容。

### 示例：加载 PDF 处理 Skill

以下是 Claude 加载和使用 PDF 处理 Skill 的方式：

1. **启动**：系统提示包含：`PDF Processing - Extract text and tables from PDF files, fill forms, merge documents`
2. **用户请求**："从这个 PDF 中提取文本并总结"
3. **Claude 调用**：`bash: read pdf-skill/SKILL.md` → 指令加载到上下文中
4. **Claude 判断**：不需要填写表单，因此不读取 FORMS.md
5. **Claude 执行**：使用 SKILL.md 中的指令完成任务

![skill02](E:\ai-showcase\3.4大模型-Agent\assets\skill02.png)

图示展示：

1. 预加载系统提示和 Skill 元数据的默认状态
2. Claude 通过 bash 读取 SKILL.md 触发 Skill
3. Claude 根据需要可选地读取额外的捆绑文件，如 FORMS.md
4. Claude 继续执行任务

这种动态加载确保只有相关的 Skill 内容占用上下文窗口。

## 如何创建 Skill：以 Anthropic 的 skill-creator 为例

前面介绍了 Skill 的文件结构与加载原理。实际创建时，可以直接编写 `SKILL.md`，也可以借助 Anthropic 提供的 **skill-creator**，让 Agent 协助完成需求梳理、初稿编写、测试和迭代。它本身也是一个 Skill：用创建 Skill 的工作流程来指导创建新的 Skill。

**参考入口：**[skill-creator 页面](https://www.skills.sh/anthropics/skills/skill-creator) · [Anthropic 官方 Skills 仓库](https://github.com/anthropics/skills)

### 1. 安装并提出需求

skill-creator 页面提供的安装命令如下（需具备 Node.js / npx，以及支持 Skills 的 Agent 环境）：

```
npx skills add https://github.com/anthropics/skills --skill skill-creator
```

安装完成后，可以直接描述目标，例如：

> 使用 skill-creator 创建一个「PPT 教材规范检查」Skill。输入是一份教学 PPT；请检查标题层级、术语一致性、图表可读性与内容完整性，输出逐页问题、依据和修改建议。不要直接改动原文件。

不同 Agent 的安装位置和调用方式可能不同；这里的命令是上述页面给出的安装方式，实际使用时以所在产品的说明为准。

### 2. 明确使用边界，再写初稿

先说清楚 **什么时候使用、需要什么输入、执行哪些步骤、产出什么结果**。skill-creator 会据此起草 Skill 文件。最小可用结构仍然是一个目录加一个 `SKILL.md`：

```
training-material-reviewer-ppt/
└── SKILL.md
```

`SKILL.md` 的开头写名称和描述，正文写执行步骤与输出要求。描述应同时说明功能和触发场景；例如“检查教学 PPT 的结构、术语、可读性与内容完整性；用户要求审查或评估课件时使用”。需要固定检查表、示例课件或验证脚本时，再分别放进 `references/`、`assets/` 或 `scripts/`，并在正文中注明何时读取或运行。

### 3. 用真实任务测试

准备几条具有代表性的测试请求，覆盖明确调用和自然表达两种情况，例如“使用该 Skill 审查这份培训 PPT”和“帮我看看这套课件有哪些规范问题”。还应加入不该触发的请求，例如“把这份 PPT 翻译成英文”，检查 Skill 是否误用。

按 skill-creator 的流程，让 Agent 在测试任务中使用草稿 Skill，查看实际输出。重点检查：是否在恰当的请求下触发、是否按步骤执行、问题定位是否具体、输出格式是否方便教师修改。若环境允许，还可以对比使用与不使用 Skill 的结果，并记录通过率、耗时和 token 用量；这些指标用于辅助判断，不能代替对内容质量的人工检查。

### 4. 根据结果反复改进

若 Skill 没有被选中，优先修改 `description`，写清适用与不适用场景；若已经触发却执行偏离，修改正文中的步骤、示例和验收标准。skill-creator 提供测试结果查看和描述优化等辅助流程，可用不同的触发与非触发请求检验描述是否准确。修改后再次运行同一批测试，再补充更多真实案例。

**完整路径可以概括为：明确目标 → 编写 Skill → 设计测试请求 → 查看结果 → 修改并复测。** 一个可用的 Skill 不只要“能被加载”，还要在该使用时被选中，并稳定产出符合预期的结果。
