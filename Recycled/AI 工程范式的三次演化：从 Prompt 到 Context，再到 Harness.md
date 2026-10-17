# AI 工程范式的三次演化：从 Prompt 到 Context，再到 Harness

### （一）Prompt Engineering 时代（2023-2024）

当我们第一次接触 ChatGPT 和 Claude 时，所有人都在问同一个问题：**“怎么说给 AI 听”**（How to talk to AI）

这个时代的核心假设是：如果你能找到完美的提示词，AI 就能完成你想要的任何事。

代表性技术包括：

| 技术                    | 用途                 | 时代 |
| ----------------------- | -------------------- | ---- |
| CoT（Chain of Thought） | 让 AI 展示推理过程   | 2023 |
| Few-shot Learning       | 给几个示例让 AI 学习 | 2023 |
| System Prompt 设计      | 在对话开始时设定角色 | 2024 |

**核心痛点：** 提示词的**不可复用性**。你在某个对话中找到的完美提示词，换个场景、换个模型、甚至换个话题，效果就大打折扣。

### （二）Context Engineering 时代（2025）

2025 年，业界开始意识到问题不在于”怎么说”，而在于”给 AI 看什么”。**Context Engineering**（上下文工程）应运而生。

这个时代的核心问题变成了：**“在关键时刻让 AI 看到什么信息”**（What information to show AI）

代表性技术包括：

| 技术                | 用途                     | 时代 |
| ------------------- | ------------------------ | ---- |
| RAG（检索增强生成） | 从知识库检索相关信息     | 2025 |
| Context Window 优化 | 管理有限的上下文窗口     | 2025 |
| AGENTS.md           | 为 AI Agent 提供项目地图 | 2025 |

**核心发现：** [Vercel](https://zhida.zhihu.com/search?content_id=271817298&content_type=Article&match_order=1&q=Vercel&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzUzMDU4NjEsInEiOiJWZXJjZWwiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzE4MTcyOTgsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.HIfMpQUfyhZ-r9eioCO7w-UA_rD10OapFW7R4YkUEwc&zhida_source=entity) 的实证研究显示，**被动上下文**（把信息准备好让 AI 自己读）比**主动检索**（AI 主动查询）效果更好。

### （三）Harness Engineering 时代（2026-至今）

2026 年初，Mitchell Hashimoto 创造了 “Harness Engineering” 这个术语。它标志着范式的根本性转变：

> **从”优化输入”转向”优化系统环境”**

这个时代的核心问题是：**“如何构建可靠的 AI 系统”**（How to build reliable systems）

**核心隐喻：** AI Agent 是”强大但难以驾驭的马”，Harness 是让马可靠可控工作的”马具系统”。

为什么叫”马具”（Harness）？

- 马本身很强壮，但没有马具就无法被人类有效利用
- 马具限制了马的活动范围，但也让马的力量可以被引导
- 好的马具让马和人类形成协同，而不是对抗

### 演进路径总结

```text
Prompt Engineering      →  Context Engineering  →  Harness Engineering
（2023-2024）                （2025）                    （2026-至今）
     ↓                           ↓                            ↓
 "怎么说给AI听"              "给AI看什么信息"            "如何构建可靠的AI系统"
 优化输入指令                管理上下文信息              围绕Agent构建工程环境
```

如果说 Prompt Engineering 关注“单次指令”，Context Engineering 关注“每次决策所需的上下文”，那么 Harness Engineering 关注的就是：

**如何为 Agent 搭建一个能持续、稳定、高质量运行的完整控制系统。**

可以把三者理解为三层递进关系：

| 阶段                | 关注点         | 解决的问题                                |
| ------------------- | -------------- | ----------------------------------------- |
| Prompt Engineering  | 指令设计       | 如何让模型更好地回答一次问题              |
| Context Engineering | 上下文构建     | 如何让模型在决策时拥有正确的信息          |
| Harness Engineering | 运行时控制系统 | 如何让 Agent 长时间、稳定、可控地完成任务 |

一个非常形象的比喻是：

- Prompt Engineering 像是在教人怎么写一封好邮件；
- Context Engineering 像是在发邮件前把相关附件都准备好；
- Harness Engineering 则像是在搭建整个办公室：流程、权限、反馈机制、规范、协作方式、治理结构，全都要到位。



# Harness六大组件全解析



裸模型有四大硬伤：无记忆、不能执行代码、知识过时、无工作环境。Harness 六大组件逐一补救——文件系统管存储与版本；沙箱赋予代码自验证；AGENTS.md 无需训练即可注入知识；Web Search+MCP 打破知识截止；上下文工程对抗信息腐烂；编排+Hooks 保障多 Agent 协同质量。System Prompt 贯穿始终，是整套系统的神经中枢。

一句话摘要： 模型提供智能，Harness 让智能变得有用。如果你不是模型本身，那你就是 Harness 的一部分。

2025 年底，一位创业者在社交媒体上发了一条动态，迅速引爆了技术圈的讨论——

> “我花了三个月调 Prompt，模型回答质量提升了 20%。然后我花了两周搭 Harness，整体任务完成率从 35% 飙到了 82%。”



这条动态下面，点赞最高的评论只有四个字：方向错了。

过去两年，几乎整个行业都在追逐更大的模型、更强的推理能力、更长的上下文窗口。从 GPT-4 到 Claude 3.5，从 Gemini Ultra 到 DeepSeek-V3，参数规模一路狂飙，基准测试分数不断刷新。每一次新模型发布，社交媒体上都会涌现一波"AGI 要来了"的狂欢。

但一个令人尴尬的事实是：绝大多数真实业务场景中，用户并没有感受到与基准分数相匹配的能力提升。

为什么？因为大家盯错了地方。

模型就像一颗强大的引擎，但引擎本身不是汽车。一颗裸露的引擎放在地上，它不能载人，不能转向，不能刹车，甚至不能自己启动。你需要底盘、变速箱、方向盘、仪表盘、油路系统……这一整套让引擎"变得有用"的东西，在 AI Agent 的世界里，有一个越来越被重视的名字——Harness。

Agent = Model + Harness。 模型提供智能，Harness 让智能变得有用。

这不是一个新概念，但它正在成为 2026 年 AI 工程领域最核心的共识。本文将从"裸模型的四个硬伤"出发，逐一拆解 Harness 的六大组件——文件系统、Bash + 沙箱、记忆（AGENTS.md）、Web Search + MCP、上下文工程、编排 + Hooks——带你看清 AI Agent 真正的竞争壁垒，不在模型层，而在 Harness 层。

读完这篇文章，你将重新理解一件事：你写的每一行 System Prompt、搭的每一个工具链、设计的每一套编排逻辑，都是在构建 Harness。 如果你不是模型本身，那你就是 Harness 的一部分。



## 01Agent = Model + Harness：一个被忽视太久的公式



在正式拆解 Harness 之前，我们需要先厘清一个最基础的认知框架。

### 什么是 Agent？

"Agent"这个词在 2024 年被用滥了。每一个能调用 API 的聊天机器人都自称 Agent，每一个加了 RAG 的问答系统都宣称自己是 Agent。但如果我们回到最朴素的定义——

Agent 是一个能够自主感知环境、做出决策、执行行动并从结果中学习的智能体。

注意这里的四个关键动词：感知、决策、执行、学习。裸模型能做到哪个？严格来说，它只能做"决策"这一步——给定输入，产出输出。它不能主动感知外部世界（没有眼睛和耳朵），不能真正执行行动（没有手和脚），更不能持久化地学习（没有长期记忆）。

所以，一个真正的 Agent 必须是这样的结构：

Agent = Model + Harness

Model 是大脑，负责"想"。Harness 是大脑之外的一切——感官系统、运动系统、记忆系统、能量系统——负责让"想"变成"做"。



### Harness 到底是什么？



Harness 这个词的英文原意是"挽具"，就是套在马身上、让马的力量转化为拉车动力的那套装备。类比非常精准：模型是马，Harness 是挽具，Agent 是马+挽具+车的整体系统。



更技术化地说，Harness 是模型之外的一切工程基础设施。它包括但不限于：

- 模型如何接收输入（上下文构建）
- 模型的输出如何被解析和执行（工具调用、代码执行）
- 模型如何获取外部信息（搜索、API）
- 模型如何记住之前发生的事（记忆机制）
- 模型如何与其他模型或子系统协作（编排）
- 以及贯穿所有环节的安全、格式、质量约束（Hooks）



Harness 不是一个单一的组件，而是一个系统。这也是为什么搭建一个真正好用的 Agent 如此之难——你不是在调一个参数，你是在设计一整套工程架构。



下面这张架构图展示了 Model 与 Harness 的关系，以及 Harness 内部六大组件的整体布局：



![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr57tW42CvLpibjQZEfhewbicTHRVIvnIFy7icoGl5Fw5stAAWvqyHdFshd42wMHVLCicSoHGI1nvH8vSibzeYgcq92pIruztYGKzgLY/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)



这张图传达了三个关键信息：第一，Model 处于中心，但它被 Harness 包围和支撑；第二，六大组件各司其职，但彼此协同；第三，System Prompt 贯穿所有组件，它是 Harness 的"神经系统"。







## 02裸模型的四个硬伤：为什么光有聪明的大脑远远不够



要理解 Harness 的价值，我们必须先直面一个残酷的现实：裸模型（Raw Model）有四个致命的硬伤。



所谓"裸模型"，就是没有任何外部工具、没有文件系统、没有搜索能力、没有持久化记忆的纯粹大语言模型。你可以把它想象成一个被关在密闭房间里的天才——智商极高，但看不见外面的世界，记不住昨天的对话，说了话也没人去执行。



### 硬伤一：无法维持跨会话状态



这是最容易被感知的痛点。你跟一个裸模型聊了两个小时，讨论了一个复杂的系统架构，画了流程图，定了技术方案。然后你关掉窗口，第二天回来——它什么都不记得了。



这不是"记忆力差"的问题，这是根本没有记忆机制的问题。裸模型的每一次对话都是一个全新的开始，前一轮的所有上下文在会话结束的瞬间灰飞烟灭。



对于简单的问答场景，这无所谓。但对于任何需要持续推进的工作——写一本书、开发一个项目、管理一个流程——这个硬伤是致命的。你需要每次都从头解释背景，每次都重新建立共识，每次都把之前的结论手动灌进去。这不是在用 AI 协作，这是在训练一个每天都失忆的实习生。



### 硬伤二：无法执行代码



裸模型可以"写"代码，但它不能"跑"代码。它可以生成一段 Python 脚本，但它无法验证这段代码是否能正确运行。它可以告诉你算法的时间复杂度，但它不能在真实数据集上跑一遍来证明自己的分析。



这意味着什么？意味着裸模型的代码输出没有自我验证能力。它可能写出语法正确但逻辑错误的代码，可能忽略边界条件，可能对库的版本做出错误假设。而这一切错误，只有在人类手动复制粘贴到本地环境运行之后才会暴露。



更深层的问题是：没有代码执行能力，模型就失去了"写→跑→看→修→再来"的自我验证循环。而这个循环恰恰是优秀程序员最核心的工作方式。一个不能运行自己代码的 AI 编程助手，就像一个只能在纸上画图纸但从来不去工地的建筑师——理论上无懈可击，实践中漏洞百出。



### 硬伤三：无法获取实时知识



大语言模型的知识有一个"截止日期"。截止日期之后发生的一切——新发布的 API 文档、最新的安全漏洞、上周刚更新的框架版本、今天的新闻——它统统不知道。



在技术领域，这个问题尤其严重。前端框架半年一个大版本，云服务商每季度更新一次产品线，开源库的 Breaking Change 防不胜防。你问裸模型"React 19 的 use() Hook 怎么用"，它可能给你一个基于 React 18 的回答，甚至虚构一个根本不存在的 API。



这就是所谓的"幻觉"（Hallucination）的一个重要来源：不是模型"故意"胡说，而是它的知识库里根本没有正确答案，于是它基于过时信息或模式匹配"推理"出了一个看起来合理但实际上错误的答案。



### 硬伤四：无法搭建工作环境



裸模型没有文件系统，没有工作空间，没有项目目录。它不能创建文件，不能组织代码结构，不能管理依赖，不能运行构建工具。



这意味着它无法完成任何"工程级"的任务。写一个单独的函数？可以。搭建一个完整的项目脚手架、配置 CI/CD 流水线、管理多个微服务之间的依赖关系？不可能。



工程不是写代码，工程是在正确的位置写正确的代码，并确保它与其他代码正确协作。没有工作环境，"工程"就无从谈起。



**四个硬伤的本质**



如果你仔细看这四个硬伤，会发现它们恰好对应了一个完整智能体所需的四种基础能力：

| **硬伤**           | **缺失的能力** | **Harness 的对应组件**       |
| :----------------- | :------------- | :--------------------------- |
| 无法维持跨会话状态 | 长期记忆       | 文件系统 + 记忆（AGENTS.md） |
| 无法执行代码       | 行动能力       | Bash + 沙箱                  |
| 无法获取实时知识   | 感知能力       | Web Search + MCP             |
| 无法搭建工作环境   | 环境操控       | 文件系统 + 上下文工程 + 编排 |



每一个"不能"，都是 Harness 里的一个组件。 Harness 不是锦上添花，它是对裸模型致命缺陷的系统性补救。没有 Harness 的 Model，就像没有身体的大脑——它可以思考，但无法存在于这个世界。







## 03组件一：文件系统——最基础的原语



在 Harness 的六大组件中，文件系统排在第一位，不是因为它最炫酷，恰恰相反——它最朴素，也最基础。基础到很多人压根没意识到它是一个"组件"。



但正是这个最朴素的组件，决定了 Agent 能力的上限。



### 为什么文件系统是"最基础原语"？



想一想人类程序员是怎么工作的。打开电脑，第一件事是什么？打开 IDE，加载项目目录。所有的代码文件、配置文件、文档、测试用例、构建脚本……都以文件的形式存在于一个结构化的目录树中。



文件系统是一切工程活动的地基。没有文件系统：

- 代码无处存放
- 中间结果无法持久化
- 多步骤任务无法衔接
- 多 Agent 之间无法协作



对于 AI Agent 来说，文件系统的意义甚至比对人类更大。因为人类有大脑记忆，可以"记住"一些中间状态。但 Agent 的上下文窗口是有限的——即使是 200K token 的上下文，对于一个真实项目来说也远远不够。文件系统就是 Agent 的"外部大脑"，是它突破上下文窗口限制的唯一途径。



### 文件系统的三大核心能力



第一，工作空间与中间结果存储。



Agent 在执行复杂任务时，会产生大量的中间产物——分析报告的草稿、代码的半成品、数据处理的中间结果、与用户确认的决策记录。这些中间产物需要一个地方存放，以便后续步骤引用。



没有文件系统，Agent 必须把所有中间产物都塞进上下文窗口——这既浪费 token，又容易超出上下文长度限制。有了文件系统，Agent 可以把中间产物写入文件，需要时再读取，实现"按需加载"。



第二，Agent 协作的基础。



当一个任务复杂到需要多个 Agent 协同工作时，文件系统就成了它们之间的"共享白板"。Agent A 把分析结果写入文件，Agent B 读取文件并在此基础上继续工作。这种基于文件的异步协作模式，简单、可靠、可追溯。



第三，版本追踪与错误回滚。



这一点经常被忽略，但它可能是文件系统最有价值的能力之一。当文件系统与 Git 集成后，Agent 的每一步操作都可以被记录、追溯、回滚。



为什么这很重要？因为 Agent 会犯错。它可能在重构代码时引入 Bug，可能在修改配置时破坏了系统。如果没有版本追踪，错误就像雪球一样越滚越大，直到系统彻底崩溃。有了 Git，Agent（或者监督它的人类）可以随时回到之前的"安全状态"，甚至可以开分支做实验——失败了就丢弃分支，成功了就合并。



以下是文件系统在 Agent 工作流中的角色示意：



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr4AgTu0o27nLnOojTcLKbibEzNRR0IE9gskGu19IZ3ZjXpUFeNiajFwyfJsfnLFd8iaR6Y0GSLA4vXHTxAht59vmoe9AHkxUs3ibfE/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)



这里有一个关键洞察：文件系统 + Git 给了 Agent "试错"的能力。 没有这个能力，Agent 只能小心翼翼地一步步走，不敢冒险。有了这个能力，Agent 可以大胆尝试——反正随时可以回滚。这极大地释放了模型的创造力。



### 文件系统的设计原则



在实际工程中，为 Agent 设计文件系统需要注意几个原则：



目录结构要清晰且约定俗成。 Agent 不擅长处理混乱的文件组织。使用标准化的目录结构（如前端项目的 src/components、src/utils 约定）能显著降低 Agent 的认知负担。



文件粒度要适中。 太大的文件（几千行代码）会超出 Agent 的处理能力；太小的文件（每个函数一个文件）会增加文件管理的复杂度。一般来说，一个文件对应一个"模块"或"职责单元"是比较好的粒度。



元数据要丰富。 文件名要有意义，目录要有 README，关键决策要有 ADR（Architecture Decision Records）。这些元数据是 Agent 理解"为什么这样组织"的线索。







## 04组件二：Bash + 沙箱——让 Agent 从"说"到"做"



如果说文件系统给了 Agent 一个"工作台"，那么 Bash + 沙箱就给了它一双"手"。



### 从"生成代码"到"执行代码"的质变



裸模型只能生成代码文本。但文本不是程序——程序是被执行的文本。在"生成"和"执行"之间，存在一条巨大的鸿沟。



一个终端（Bash）环境意味着 Agent 可以：

- 运行它自己写的代码
- 安装依赖包
- 执行构建命令
- 运行测试套件
- 查看运行时错误并调试



这从根本上改变了 Agent 的工作模式。没有 Bash，Agent 是一个"提建议"的顾问；有了 Bash，Agent 是一个"动手做"的工程师。



### 自我验证循环：写→跑→看→修→再来



这是 Bash 赋予 Agent 的最核心能力——自我验证循环。



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7jcVWibzqLm3jMqvOm5zEyd7NRFw8tKAu1XowdFtWHRod4ibDdz0FaQv2CI4kvJbAG6XWkCx2iaJicQfCzQYl8jcRwUnnguq58o90/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)



这个循环看起来简单，但它的意义是革命性的。没有这个循环，Agent 的输出质量完全依赖于模型的"一次性生成"能力——模型推理正确就对了，推理错误就全错。有了这个循环，Agent 拥有了自我纠错能力，它可以从自己的错误中学习（至少在单次会话内）。



实际测试数据表明：在编程任务中，具备自我验证循环的 Agent 的任务完成率比"一次性生成"的方式高出 40%–60%。这个差距不是来自更好的模型，而完全来自 Harness 层的 Bash 能力。



### 为什么必须是"沙箱"？



有了 Bash 就够了吗？不，还需要安全隔离。



Agent 执行的代码不一定是安全的。它可能无意中执行了 **rm -rf /**，可能下载了恶意包，可能发起了未授权的网络请求。如果 Agent 的代码执行环境是宿主机本身，后果不堪设想。



沙箱（Sandbox）提供了一个隔离的执行环境：



资源限制： CPU、内存、磁盘空间都有上限，防止死循环或内存泄漏拖垮系统。



网络隔离： 默认禁止外部网络访问，或只允许白名单内的地址，防止数据泄露或恶意攻击。



文件系统隔离： Agent 只能访问自己的工作目录，不能接触宿主机的敏感文件。



超时机制： 执行时间超过阈值自动终止，防止资源被长期占用。



沙箱不是一个可选的"安全加固措施"，它是 Bash 能力的必要前提。没有沙箱，你不敢让 Agent 执行代码；不敢让 Agent 执行代码，Agent 就失去了自我验证能力；失去了自我验证能力，Agent 的输出质量就会大打折扣。



### 沙箱技术的选择



在工程实践中，常见的沙箱方案包括：



Docker 容器： 最主流的方案，隔离性好，生态成熟，镜像管理方便。大多数 Agent 框架（如 Devin、OpenHands）都采用 Docker 作为沙箱。



gVisor / Firecracker： 更轻量的虚拟化方案，启动速度快（毫秒级），适合需要频繁创建/销毁沙箱的场景。



WebAssembly（WASM）： 在浏览器端或边缘计算场景中有潜力，但目前对系统调用的支持还不够完善。



Nix / 纯函数式环境： 通过声明式的环境定义，确保每次执行的环境完全一致，杜绝"在我机器上能跑"的问题。



选择哪种方案取决于你的具体需求，但核心原则只有一条：在保证安全的前提下，给 Agent 尽可能大的自由度。







## 05组件三：记忆（AGENTS.md）——不改权重也能给模型加知识



这是 Harness 六大组件中最容易被低估，但可能最具长期价值的一个。



### 模型的"失忆症"



我们在前文讨论过，裸模型无法维持跨会话状态。每次对话结束，所有的上下文都会消失。但在真实的工作场景中，Agent 需要"记住"大量信息：

- 项目的技术栈和架构决策
- 用户的偏好和工作习惯
- 之前犯过的错误和学到的教训
- 团队的编码规范和设计模式
- 业务领域的专有知识



传统的做法是把这些信息写进 System Prompt——但 System Prompt 的长度是有限的，塞太多信息会稀释重要指令的权重，甚至导致模型"注意力分散"。



AGENTS.md 提供了一个优雅的解决方案：把知识写入文件，在需要时自动注入上下文。



### AGENTS.md 的工作机制



AGENTS.md 的设计理念可以用一句话概括：工作中写入知识，存文件，下次自动注入。



具体来说：



写入阶段： 当 Agent 在工作过程中产生了有价值的知识（比如发现某个 API 有一个未文档化的限制，或者确定了某种架构方案的优劣），它会把这些知识以结构化的方式写入 AGENTS.md 文件。



存储阶段： AGENTS.md 文件存放在项目的文件系统中，通常是根目录或各子目录下。它本质上就是一个 Markdown 文件，人类可以直接阅读和编辑。



注入阶段： 下一次 Agent 启动或切换到新的工作上下文时，Harness 会自动读取相关的 AGENTS.md 文件，并将其内容注入到 Agent 的上下文中。



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr6GdXvt9sAmymOq00Uk9B6WVlke0g4v6xVdjL2oTia670OOxjtjUtTUhRR7m3ViaChoE2DK8vrXgO4NgAjTZl7ehbMb6lzvdSjMQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)



### "上下文注入 = 不改权重给模型加知识"



这个等式是 AGENTS.md 最深刻的洞察。



传统上，要给模型"加知识"，你需要微调（Fine-tuning）——修改模型的权重参数。这个过程成本高、周期长、且存在灾难性遗忘的风险。



AGENTS.md 提供了一条捷径：不碰模型权重，只通过上下文注入来添加知识。 模型仍然是原来的模型，但它"看到"的信息变了，因此它的行为也变了。



这就像是一种"即插即用"的知识扩展机制——今天你发现了一个新的最佳实践，写进 AGENTS.md，明天 Agent 就自动具备了这个知识。不需要重新训练，不需要等模型供应商更新，不需要任何机器学习的专业知识。



这也解释了为什么 AGENTS.md 被称为"记忆"组件——它让 Agent 拥有了跨会话的长期记忆，而且这种记忆是透明的（人类可以阅读和编辑）、可控的（可以随时增删改）、可审计的（配合 Git 可以追溯每一次知识变更）。



###  AGENTS.md 的最佳实践



在实际项目中，AGENTS.md 的组织方式通常遵循以下原则：



层次化存放。 根目录的 AGENTS.md 存放全局知识（项目概述、核心架构决策、团队规范）；子目录的 AGENTS.md 存放局部知识（该模块的特殊约定、已知问题、接口规范）。Agent 在进入某个目录工作时，会同时加载全局和局部的知识。



结构化书写。 好的 AGENTS.md 不是随意的笔记，而是有明确结构的知识库。常见的分类包括：项目架构、技术约束、编码规范、已知陷阱（Gotchas）、决策记录（ADR）等。



定期清理。 过时的知识比没有知识更危险。随着项目演进，某些早期的约束可能已经不再适用，某些技术决策可能已经被推翻。定期审查和清理 AGENTS.md 是保持其有效性的关键。



双向可编辑。 AGENTS.md 不仅是 Agent 写给自己的备忘录，也是人类与 Agent 之间的"知识契约"。人类可以直接编辑 AGENTS.md 来向 Agent 传达偏好（"我不喜欢使用三元表达式"）、约束（"所有 API 必须使用 REST 风格"）、甚至个人工作习惯（"代码审查时请重点关注错误处理"）。







## 06组件四：Web Search + MCP——突破知识的"时间牢笼"



裸模型的第三个硬伤是"无法获取实时知识"。Web Search + MCP 就是针对这个硬伤的解药。



### AGENTS.md 的最佳实践



每个大语言模型都有一个知识截止日期。这个日期之后的世界，对模型来说是一片空白。



这在日常闲聊中可能无伤大雅，但在专业工作场景中，这是一个严重的限制。想象一下这些场景：

- 你让 Agent 帮你调试一个 bug，而这个 bug 的修复方案在模型训练之后才被社区发布
- 你让 Agent 写一个集成方案，而目标 API 在上个月做了 Breaking Change
- 你让 Agent 分析竞品动态，而竞品昨天刚发布了新产品



在这些场景中，裸模型不仅帮不了你，还可能用过时的信息自信地给出错误的答案——这比"不知道"更危险。



### Web Search：打开信息的大门

Web Search 赋予 Agent 搜索互联网的能力，让它能够访问训练数据之后的新信息。这从根本上解决了"知识过时"的问题。

但 Web Search 不仅仅是"接个搜索 API"那么简单。一个好的 Web Search 组件需要解决以下问题：

查询构建： 模型的自然语言表述不一定是好的搜索查询。Harness 需要帮助模型把模糊的意图转化为精准的搜索关键词。

结果筛选： 搜索引擎返回的结果质量参差不齐。Harness 需要帮助模型过滤低质量来源，优先使用权威文档（如官方文档、RFC、知名技术博客）。

内容提取： 网页内容通常包含大量无关信息（广告、导航栏、侧边栏）。Harness 需要提取核心内容并以模型友好的格式呈现。

信息整合： 当 Agent 需要综合多个来源的信息时，Harness 需要帮助它处理信息冲突、去重、排序。



### MCP：从"搜索"到"连接"



如果说 Web Search 让 Agent 能"看"互联网，那么 MCP（Model Context Protocol）让 Agent 能"触"互联网。

MCP 是 Anthropic 在 2024 年底推出的一个开放协议，它定义了 AI 模型与外部工具、数据源之间的标准化交互方式。你可以把它理解为"AI 世界的 USB 接口"——只要工具遵循 MCP 规范，就可以即插即用地接入任何支持 MCP 的 Agent。

MCP 的意义在于：它把 Agent 的"感知范围"从公开互联网扩展到了任何可编程的数据源和服务。数据库、内部 Wiki、项目管理工具（Jira、Linear）、代码仓库（GitHub）、监控系统（Datadog、Grafana）……只要有 MCP 接口，Agent 就能直接访问。



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7OMIFLxfJ9or9cdretgU5ibWBsA5icFoBGajByrgQgzOZKD1M2icek9Gcg6PK8E9DnJvicBSicDSWx0QDsa0FY542lM0MnN6l7r3y0/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)



### Web Search + MCP 的协同效应

Web Search 和 MCP 单独使用都有价值，但它们的组合才是真正强大的。

举个例子：Agent 需要修复一个生产环境的 Bug。

1. MCP 连接监控系统 → 获取错误日志和堆栈信息
2. MCP 连接代码仓库 → 查看相关代码和最近的变更历史
3. Web Search 搜索错误信息 → 查找社区中是否有类似问题的解决方案
4. MCP 连接项目管理工具 → 检查是否有相关的已知问题
5. Agent 综合所有信息 → 生成修复方案并提交 PR



整个流程中，Agent 像一个经验丰富的 SRE（Site Reliability Engineer），在多个信息源之间穿梭，快速定位和解决问题。这种能力不来自于更强的模型，而来自于 Harness 层的 Web Search + MCP。





## 07组件五：上下文工程——对抗 AI 系统的"熵增"



如果说前四个组件是给 Agent 装上四肢和感官，那么上下文工程就是在管理它的大脑如何高效运转。



这是 Harness 中最"软"的一个组件——它不涉及具体的工具或协议，而是关于如何构建和维护模型的输入上下文。但恰恰是这个"软"组件，在实践中对 Agent 表现的影响最大。



### Context Rot：上下文的"腐烂"

在长时间运行的 Agent 会话中，一个普遍但很少被讨论的问题是 Context Rot（上下文腐烂）。

随着对话的进行，上下文窗口中会积累越来越多的信息——早期的指令、中间的讨论、工具调用的输入输出、错误信息和修复过程……这些信息像沉积物一样不断堆积，导致几个严重的问题：

- 信噪比下降。 真正重要的信息被大量冗余内容淹没。模型的注意力被分散，关键指令的执行质量下降。
- 矛盾信息累积。 早期做出的决定可能已经被推翻，但旧信息仍然留在上下文中。模型可能在新旧信息之间"摇摆不定"，产出不一致的结果。
- Token 浪费。 大量无用的历史信息占据了宝贵的上下文窗口空间，留给真正有用信息的空间被压缩。
- 推理质量退化。 研究表明，当上下文中充斥大量无关信息时，即使相关信息就在上下文中，模型的提取和推理能力也会显著下降——这就是所谓的"大海捞针"（Needle in a Haystack）问题的实践版。



Context Rot 不是一个理论问题，它是每一个长时间运行的 Agent 都会遇到的实际挑战。如果你用过 Agent 做复杂任务，你一定有过这样的体验：一开始 Agent 的表现很好，但随着对话变长，它开始"变笨"——遗忘之前的约定，重复之前犯过的错误，甚至对同一个问题给出前后矛盾的回答。这就是 Context Rot 在起作用。



### 上下文工程的核心策略



对抗 Context Rot 的技术手段统称为"上下文工程"（Context Engineering），它包含以下几个关键策略：

- 压缩（Compression）。 定期对历史上下文进行摘要压缩。把冗长的工具调用记录替换为简洁的结果摘要，把详细的讨论过程替换为最终结论。这就像是给上下文做"垃圾回收"。
- 工具输出卸载（Tool Output Offloading）。 工具调用的输出（特别是大段的代码、日志、搜索结果）是上下文膨胀的主要来源。上下文工程会把这些输出存储到文件系统中，在上下文中只保留摘要和文件引用。需要详细信息时，Agent 可以随时重新读取文件。
- Skills 渐进加载。 不同的任务阶段需要不同的知识和能力。上下文工程会根据当前任务阶段，动态加载和卸载相关的 Skill 定义。例如，在"需求分析"阶段加载产品相关知识，在"编码"阶段加载技术栈相关知识，避免一次性把所有信息都塞进上下文。
- 分层上下文结构。 把上下文分为"核心层"（System Prompt、关键约束，始终保留）、"工作层"（当前任务相关信息，按需更新）、"历史层"（已完成任务的摘要，逐渐压缩）。不同层的信息有不同的生命周期和更新策略。



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7WtbJStiamUBQfdo5Nsh4Rm8Mwd9OrREhFHfRlvLodLic9hpYjGuuIRyDVkkN5vF8QyobtN9ROOkWL4ADZgH8897g85ltKMbOms/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)



### 上下文工程是 Harness 的"元能力"



上下文工程有一个特殊的地位——它不是 Harness 的一个独立功能模块，而是影响所有其他组件的"元能力"。

文件系统的读写操作需要上下文工程来决定"读什么"和"什么时候读"。记忆的注入需要上下文工程来决定"注入多少"和"注入哪些"。Web Search 的结果需要上下文工程来决定"保留什么"和"丢弃什么"。编排中的子 Agent 通信也依赖上下文工程来构建高效的信息传递格式。

可以说，Harness 本质上就是好的上下文工程的交付机制。 Harness 的每一个组件，归根结底都是在解决同一个问题：如何在正确的时间、以正确的方式、把正确的信息送到模型面前。

这也是为什么"上下文工程"这个概念在 2025 年底开始取代"Prompt 工程"成为 AI 工程领域的核心话题。Prompt 工程关注的是"怎么写指令"，上下文工程关注的是"怎么构建模型看到的全部信息"——后者的范围大得多，影响也深远得多。



## 08组件六：编排 + Hooks——让单兵作战变成集团军



最后一个组件是编排（Orchestration）+ Hooks。如果说前五个组件是在增强单个 Agent 的能力，那么这个组件是在把多个 Agent 组织成一个协同作战的系统。



### 为什么需要编排？



当任务复杂度超过单个 Agent 的处理能力时，你需要把任务分解为多个子任务，分配给不同的"子 Agent"处理，然后把结果汇总。这就是编排。

编排解决的核心问题包括：

- 子 Agent 调度。 哪个子任务应该分配给哪个 Agent？它们之间的依赖关系是什么？哪些可以并行，哪些必须串行？
- 任务分发。 如何把一个模糊的大任务拆解为明确的小任务？如何确保每个子 Agent 得到足够的上下文来完成它的子任务？
- 模型路由。 不是所有的子任务都需要最强（也最贵）的模型。简单的格式转换可以用小模型，复杂的架构设计需要大模型。编排器需要根据任务复杂度选择合适的模型，在成本和质量之间取得平衡。
- 结果聚合。 当多个子 Agent 返回结果后，如何检查一致性、解决冲突、合并为最终输出？



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr6PQJ5V8dGWkdeKXbiaKGfxW1xDeBlxqsESBiaictZfjib1Uu3ARfNqRbYolbsxvLe7jwGiag8EZFb9qNlEgr0h9mpBGoozRr0fewHY/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)



### Hooks：注入确定性

编排解决了"谁做什么"的问题，Hooks 则解决了"做得对不对"的问题。

在软件工程中，Hook 是一种在特定事件发生时自动触发的回调机制。在 Agent Harness 中，Hooks 的作用类似——在 Agent 行为的关键节点插入确定性检查，确保输出符合预期。

Hooks 的典型应用场景包括：

- Lint 检查。 Agent 生成代码后，自动运行 linter 检查语法和风格是否符合项目规范。不符合的话，自动要求 Agent 修复。
- 续接（Continuation）。 当 Agent 的单次输出因为 token 限制被截断时，Hook 自动检测截断并触发续接请求，确保输出的完整性。
- 格式约束。 确保 Agent 的输出符合特定的格式要求——JSON Schema 验证、Markdown 结构检查、API 响应格式校验等。
- 安全过滤。 在 Agent 执行敏感操作（如文件删除、数据库写入、外部 API 调用）前，Hook 进行权限检查和安全审计。
- 成本控制。 监控 token 消耗和 API 调用频率，在接近预算上限时发出警告或限制。



Hooks 的核心价值在于：它们用确定性的规则约束了概率性的模型输出。 模型的输出本质上是概率性的——它可能生成正确的代码，也可能犯错。Hooks 在模型输出的"出口"设置了一道关卡，用确定性的规则（如 lint 规则、格式校验）把不合格的输出拦截下来，要求重新生成。

这种"概率性生成 + 确定性校验"的组合模式，是当前 Agent 工程中最有效的质量保障策略之一。它既充分利用了模型的创造力和灵活性，又通过工程手段兜住了质量底线。



### 编排模式的演进

Agent 编排的方式在过去两年经历了快速演进：

- 线性管道（Sequential Pipeline）。 最简单的编排方式，Agent A 的输出直接作为 Agent B 的输入，依次传递。适用于步骤明确、依赖关系清晰的任务。
- DAG 编排（Directed Acyclic Graph）。 用有向无环图定义任务之间的依赖关系，支持并行执行没有依赖关系的任务。比线性管道更灵活高效。
- 动态编排（Dynamic Orchestration）。 不预定义完整的任务图，而是由编排器 Agent 根据上一步的结果动态决定下一步做什么。最灵活，但也最难控制质量和成本。
- 层级编排（Hierarchical Orchestration）。 编排器本身也可以层级嵌套——一个高层编排器管理几个中层编排器，每个中层编排器又管理几个执行 Agent。适用于超大规模的复杂任务。

选择哪种编排模式，取决于任务的复杂度、确定性程度和实时性要求。但无论选择哪种模式，Hooks 都是不可或缺的质量保障机制。



## 09System Prompt：贯穿所有组件的"神经系统"



在讨论完六大组件后，还有一个贯穿始终的要素值得单独讨论——System Prompt。

System Prompt 不是 Harness 的"第七个组件"，但它是贯穿所有六个组件的"神经系统"。它在 Harness 架构中扮演着四个关键角色：

### 定义角色边界



System Prompt 告诉模型"你是谁"和"你不是谁"。这不是简单的角色扮演，而是在定义 Agent 的能力边界和行为约束。



例如："你是一个前端开发 Agent，专注于 React 生态系统。当用户提出后端相关需求时，建议他们使用专门的后端 Agent。"这样的定义帮助 Agent 聚焦在自己擅长的领域，避免在不擅长的领域产出低质量结果。



### 注入领域知识



System Prompt 是"零成本"知识注入的第一入口。项目背景、技术栈选型、核心业务逻辑——这些信息直接写在 System Prompt 中，确保 Agent 从第一轮对话开始就具备必要的领域知识。



当然，正如前文讨论的，System Prompt 的容量有限。当领域知识量超过 System Prompt 能承载的范围时，AGENTS.md 就接管了这个职责。两者是互补关系：System Prompt 装"必须知道的"，AGENTS.md 装"最好知道的"。



### 约束安全规则



System Prompt 是 Agent 安全策略的"第一道防线"。哪些操作是允许的，哪些是禁止的；哪些数据可以读取，哪些是敏感的；遇到不确定的情况应该怎么处理——这些安全规则通过 System Prompt 直接"刻"进 Agent 的行为模式。



### 贯穿所有组件



System Prompt 的影响范围不限于模型本身，它通过定义 Agent 的行为模式，间接影响了所有 Harness 组件的工作方式：

- 影响文件系统：定义文件的组织规范和命名约定
- 影响 Bash 执行：限制可执行的命令范围
- 影响记忆写入：规定知识记录的格式和标准
- 影响搜索行为：设置搜索的优先来源和可信度标准
- 影响上下文管理：定义信息的优先级和压缩策略
- 影响编排逻辑：规定任务分解的粒度和协作规范



在这个意义上，写 System Prompt 就是在设计 Harness 的行为规范。一个好的 System Prompt 就像一部好的公司章程——它不直接做任何事，但它决定了所有事怎么做。



## 10结语：你就是 Harness 的一部分



让我们回到文章开头的那个公式：

Agent = Model + Harness

如果你是一名 AI 工程师、产品经理、技术负责人——如果你不是模型本身——那你就是 Harness 的一部分。

你写的 System Prompt 是 Harness 的神经系统。你搭建的工具链是 Harness 的四肢。你设计的记忆机制是 Harness 的长期记忆。你优化的上下文策略是 Harness 的注意力管理。你编写的 Hook 规则是 Harness 的质量底线。

过去两年，行业的聚光灯一直打在模型身上——参数规模、基准分数、推理能力。但真正在生产环境中创造价值的，往往不是那个最强的模型，而是那个最好的 Harness。

模型会继续进步，但进步的速度在放缓。与此同时，Harness 的工程空间还几乎没有被充分探索。文件系统怎么设计才能最大化 Agent 的效率？上下文工程有没有最优的压缩算法？编排模式怎样才能在成本和质量之间取得完美平衡？记忆机制能否实现真正的"终身学习"？

这些问题的答案，不在模型的论文里，而在 Harness 的工程实践中。

模型决定了 Agent 能力的下限，Harness 决定了 Agent 能力的上限。

下一次当你在调试 Agent 的表现时，不要急着换一个更强的模型。先看看你的 Harness：文件系统完善吗？沙箱安全吗？记忆机制在工作吗？上下文腐烂了吗？编排合理吗？Hooks 在兜底吗？





# Claude Code 源码拆解：11 个值得参考的企业级 Agent 工程实践



## 全局架构：分层调度，不是多 Agent 对等协作

在深入各个模块之前，先通过一张全局架构图，快速盘点 Claude Code 的整体设计逻辑。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/viasnlibZqap6tichiaPbOSlpTmwYfhiapnUxS1zCcmuUlHj3r8Lsb3Mhr6TMkqACqTe60M2p7ic2wOYlnXtL3JYlUZrqgBGPw3sTZYf7d1aoy8Tg/640?wx_fmt=jpeg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

Claude Code 的源码里有 Coordinator、Worker、Fork 这些概念，乍一看像是一套多 Agent Swarm 系统。但实际读完代码之后会发现，它的架构是分层调度的，换句话说，就是有一个主循环在顶层，需要的时候往下派生子 Agent，子 Agent 干完活把结果交回来。整体是上下级关系，而不是多个 Agent 对等协作。

从架构图里可以看出几个关键点：

1、**所有模式共用同一个引擎**

不管是普通的单Agent 模式，还是 Coordinator 编排模式，还是被派生出来的 Worker，底层跑的都是同一个 QueryEngine 的 Think → Act → Observe → Repeat 循环。换句话说，Claude Code 没有为多 Agent 单独写一套运行时，Coordinator 和普通 Agent 的区别，仅仅是换了一套 System Prompt。

2、**Coordinator 本质上就是“换了个 Prompt 的普通 Agent”**

同一个QueryEngine 实例，给它注入 Coordinator 的 System Prompt，它就开始指挥别人干活；注入普通 Prompt，它就自己干活。模式切换的成本非常低。

**3、Worker 是子进程，不是对等节点**

每个 Worker 也是一个 QueryEngine 实例，跑自己的单线程循环。Coordinator 派任务下去，Worker干完之后通过 <task-notification> XML 把结果交回来。这是一个上下级的父子关系，不是多个 Agent 互相发消息的 Swarm。

**4、记忆系统独立于主循环运行**

Context Compaction（短期）、ExtractMemories（中期）、AutoDream（长期）三套记忆机制在主循环旁边各自运行，后面会逐个展开。

下面按模块再逐个拆解下。

## Agentic Loop：单线程循环跑完绝大多数任务

Claude Code 的基础是一个单线程递归循环，绝大多数任务在这个循环内就能完成，不需要启动多 Agent。Coordinator-Worker 是在这个基础上通过模式切换实现的可选扩展，而非默认架构。

### QueryEngine：核心运行引擎

QueryEngine.ts 是 Claude Code 的核心文件，管理着整个 Agent 的生命周期：会话状态、工具调用、权限检查、Token 追踪，全在这一个文件里。

循环的基本结构如下图所示：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/viasnlibZqap7Vz4RfrCahXL6hfQar2CAyH4lfEgxbmzicj5ZGhtibJI7unmmUwYnqJwYLD3WPBicm1TCdLU3JX3GZbVapYDVAatWJTkMkDm2XCQ/640?wx_fmt=jpeg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

这个循环的工程实现有几个值得注意的地方。

首先，**整套工具调度系统完全是手搓的**，没有用 LangChain、LangGraph 或者任何第三方 Agent 框架。大约 40 个 Tool 的注册、描述、参数校验、调用分发，全在 QueryEngine 里自己管。这带来的好处是完全可控，坏处是工作量不小，但对于 Anthropic 这种体量的团队来说，可控性显然比开发效率更重要。

其次，**工具调用是同步递归的**。Claude API 返回一个工具调用请求，QueryEngine 就去执行这个工具，把工具输出追加到对话历史里，然后再调一次 Claude API。整个过程是串行的，没有用异步消息队列。这种设计的优势也是简单、可控、容易调试，出了问题直接看调用栈就行。

第三，**每一轮循环都有显式的 Token 消耗追踪**。QueryEngine 会实时记录已经用了多少 Token，判断上下文窗口还剩多少空间。一旦接近上限，就会触发 Context Compaction（后面第三章会详细讲）。这个机制保证了长时间运行的任务不会因为上下文溢出而崩掉。

下面是从 query.ts（1730 行）中精简出来的核心循环骨架：

```
// query.ts — queryLoop 核心结构（精简版，省略错误处理和 fallback）async function* queryLoop(params: QueryParams) {  let state = { messages: params.messages, turnCount: 1, /* ... */ }
  while (true) {    let messagesForQuery = getMessagesAfterCompactBoundary(state.messages)
    // 1. 上下文压缩（接近 Token 上限时自动触发）    const { compactionResult } = await autocompact(messagesForQuery, /* ... */)    if (compactionResult) messagesForQuery = buildPostCompactMessages(compactionResult)
    // 2. 调用 Claude API，流式接收响应    for await (const msg of callModel({ messages: messagesForQuery, tools, systemPrompt })) {      if (msg.type === 'assistant') assistantMessages.push(msg)    }
    // 3. 没有工具调用 → 结束循环，返回结果    if (toolUseBlocks.length === 0) return { reason: 'end_turn' }
    // 4. 执行工具 → 收集结果 → 追加到对话历史 → 下一轮    const toolResults = await runTools(toolUseBlocks, canUseTool, toolUseContext)    state = { messages: [...messagesForQuery, ...assistantMessages, ...toolResults], turnCount: state.turnCount + 1 }  } // while (true)}
```

结构很直白：压缩上下文 → 调 API → 有工具调用就执行、没有就结束 → 把结果塞回对话历史 → 下一轮。整个1730行的 query.ts，本质上就是在这个骨架外面包了一层错误恢复、fallback 模型切换、流式输出、Token 预算管理等生产级的防护逻辑。

### 动态 Prompt 组装：六层拼装

Claude Code 的系统提示词不是一个写死的长字符串。context.ts 这个文件负责实时组装 Prompt，每次调用 Claude API 之前，都会从六个不同的来源拼出完整的上下文：

| 层次    | 来源                         | 内容                               | 更新频率            |
| ------- | ---------------------------- | ---------------------------------- | ------------------- |
| System  | 硬编码                       | 基础角色定义、安全规则             | 每版本更新          |
| Mode    | coordinatorMode / workerMode | Coordinator/Worker/Normal 行为规范 | 每次模式切换        |
| Tools   | 40+ 工具注册 + MCP 动态加载  | 工具描述和使用规范                 | MCP 连接时          |
| Project | CLAUDE.md                    | 项目级持久记忆                     | 用户/Agent 主动更新 |
| Git     | context.ts 实时读取          | 仓库状态快照（分支、改动文件）     | 每轮对话            |
| History | 对话历史 + Compaction 摘要   | 会话上下文                         | 每轮对话            |

这种分层组装的好处是每一层可以独立更新，互不干扰。比如用户通过 MCP 接入了一个新的工具，只需要更新 Tools 层，不影响 System 和 Project 层的内容。再比如 Agent 从普通模式切换到 Coordinator 模式，只需要替换 Mode 层的 Prompt，其他五层保持不变。

这也解释了前面说的“Coordinator 本质上是换了个 Prompt 的普通 Agent”，模式切换只动了六层里的一层。

### 单 Agent 还是多 Agent

国内外很多技术社区过去一年多都在推崇多 Agent 架构，各种 multi-agent framework 也层出不穷。但从 Claude Code 的源码层面上看，它回归到了一个很朴素的选择，默认就是**单 Agent + 丰富工具集**，只有在任务确实复杂到需要并行处理时，才通过模式切换启用 Coordinator-Worker。

这和我之前拆解 Manus 时看到的逻辑是一致的：“Less structure, more intelligence”。对于大多数实际任务，单 Agent 加丰富工具集的方案，比多个 Agent 互相通信要稳定得多。

原因其实想想也很简单，**多 Agent 通信本身就会引入额外的失败点**，比如消息丢失、状态不一致、死循环。而单 Agent 的上下文是连续的，不需要在多个 Agent 之间来回同步信息。至于扩展性，Claude Code 通过 MCP 协议支持动态加载外部工具，一个 Agent 能用的工具数量本身就没有硬性限制。

所以 Claude Code 做的事情不是不能做多 Agent，而是大多数时候没必要。下一章来聊聊，它在确实需要多 Agent 的时候是怎么做的。
 

## Coordinator-Worker：需要时才启用的多 Agent 编排

Claude Code 的 Coordinator-Worker 不是独立于 Agent Loop 的另一套系统，而是在同一个 QueryEngine 上换了一套 Prompt 就能启用的编排模式，也就是需要的时候打开，不需要的时候关掉。Coordinator 最核心的工作不是把任务分下去让别人干，而是把别人干完的结果读懂想明白、再决定下一步怎么做。

### Coordinator 的 370 行系统提示词

coordinatorMode.ts 里的 getCoordinatorSystemPrompt() 函数返回了一份超过370行的 System Prompt。这份 Prompt 本身就是一份多 Agent 编排的工程规范文档，下面摘出几个最关键的设计。

四阶段工作流。 Coordinator 的 Prompt 里定义了一张明确的分工表（coordinatorMode.ts 第 204-209 行）：

| 阶段                   | 执行者           | 职责                                 |
| ---------------------- | ---------------- | ------------------------------------ |
| Research（调研）       | Worker（可并行） | 调查代码库、定位文件、理解问题       |
| Synthesis（综合）      | Coordinator 自己 | 阅读调研结果，理解问题，撰写实施方案 |
| Implementation（实施） | Worker           | 按方案做针对性修改，提交代码         |
| Verification（验证）   | Worker           | 验证改动是否正确                     |

这里最关键的是 Synthesis 阶段——Prompt 里用了非常强硬的语气明确要求这一步必须由 Coordinator 自己做（第 255-259 行）：

> Always synthesize — your most important job. When workers report research findings, you must understand them before directing follow-up work. Read the findings. Identify the approach. Then write a prompt that proves you understood by including specific file paths, line numbers, and exactly what to change.

> 永远要做综合——这是你最重要的工作。 当 Worker 汇报调研结果后，你必须先理解这些结果，然后才能指导后续工作。读结果、分析思路、然后写一个能证明你理解了的 Prompt——里面要包含具体的文件路径、行号和修改内容。

紧接着，Prompt 里还给出了一个反面教材（第 262-268 行）：

```
// 反面教材——偷懒式委派（Anti-pattern — lazy delegation）AgentTool({ prompt: "Based on your findings, fix the auth bug", ... })
// 正面示例——综合后的精确指令AgentTool({ prompt: "Fix the null pointer in src/auth/validate.ts:42.   The user field on Session is undefined when sessions expire but the   token remains cached. Add a null check before user.id access —   if null, return 401 with 'Session expired'. Commit and report the hash.", ... })
```

这段反面教材指出了一个在实际项目中非常常见的问题，“**based on your findings, fix the bug**”（根据你的调研结果，修复这个 bug）。这种写法把理解工作推给了 Worker，而 Coordinator 自己没有做任何综合判断。正确的做法是 Coordinator 读完调研结果后，自己消化、理解，然后给 Worker 一个包含具体文件路径、行号和修改方案的精确指令。

并行是核心优势。 Prompt 的 Concurrency 部分（第 213 行）直接写道：

> Parallelism is your superpower. Workers are async. Launch independent workers concurrently whenever possible — don't serialize work that can run simultaneously.

> 并行是你的超能力。 Worker 是异步的。只要任务之间互相独立，就应该同时启动，不要把能并行的工作串行化。



同时也划了红线，就是只读任务（调研）可以随意并行，写操作（修改代码）同一组文件同一时间只能有一个 Worker 在改。

### AgentTool：Fork 和 Fresh Agent 的选择

AgentTool/prompt.ts 定义了子 Agent 的两种模式。Fork 模式继承父 Agent 的完整上下文，和父 Agent 共享 Prompt Cache，所以调用成本很低。Fresh Agent 模式从零开始，适合需要"独立视角"的场景，比如代码审查——不希望审查者带着实现者的预设来看代码。

源码里提供了一张选择决策表（AgentTool/prompt.ts 第 284-291 行），列出了几种典型场景的推荐做法：

| 场景                           | 推荐方式                    | 原因                                   |
| ------------------------------ | --------------------------- | -------------------------------------- |
| 调研结果正好覆盖了要修改的文件 | Continue（继续同一 Worker） | Worker 已有相关文件的上下文            |
| 调研范围很广但实施范围很窄     | Spawn fresh（新建 Worker）  | 避免把调研噪声带入实施上下文           |
| 纠正失败或扩展最近的工作       | Continue                    | Worker 有错误上下文，知道刚才试过什么  |
| 验证另一个 Worker 刚写的代码   | Spawn fresh                 | 验证者需要完全独立的视角，避免先入为主 |

Prompt 里还定义了两条很有意思的规范：

**1、Don't peek（不要偷看）**

 Fork 返回结果后，Coordinator 不要去读 Fork 的中间过程文件。源码原文（第 91 行）：“Reading the transcript mid-flight pulls the fork's tool noise into your context, which defeats the point of forking.”——偷看 Fork 的工作过程会把工具调用的噪声引入 Coordinator 的上下文，这和 Fork 的初衷矛盾。

**2、Don't race（不要抢跑）**

Fork 还在运行时，Coordinator 不能预测或编造结果。源码原文（第 93 行）：“Never fabricate or predict fork results in any format — not as prose, summary, or structured output.”——不要以任何形式编造 Fork 的结果。如果用户在 Fork 完成之前追问进展，Coordinator 应该说还在跑，给状态，不给猜测。


### Ultraplan：远程 Agent 编排

commands/ultraplan.tsx 还暴露了一个标记为 ant-only（Anthropic 内部使用）的功能。虽然普通用户用不到，但它背后的架构模式值得了解。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/viasnlibZqap7LEtF6DtMLH1IBc4Z4TELxWoxkhKXFrticicPUaxwbYSBu89ibqibGWwGiaAS8RxBld3priaFGMYlcOsTwDmfQCkbGhuRkj0Fcy6a9Q/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

Ultraplan 的流程是一个 **Plan → Approve → Execute** 的三阶段模型。第一步，把本地对话上下文通过"teleport"机制序列化后传送到远程 CCR（Claude Code Remote）环境，用更强的模型（Opus 级，30 分钟超时）生成规划方案。第二步，方案生成后等待人类审批，支持轮询机制。第三步，审批通过后在本地按计划执行。

这部分我觉得有两个设计值得注意，一是 Teleport 机制解决了本地资源不够做复杂规划，但不想把整套代码上传到云端的矛盾。就是只传送对话上下文，不传代码。二是计划和执行的模型分离，规划用强模型（高成本、低频），执行用快模型（低成本、高频）。

这和我在之前介绍过的售前报价 Agent 项目中设计的“**草稿生成 → 老板审核 → 下载报价单**”三阶段其实是同一个模式。



## 三层记忆系统：短期压缩、中期萃取、长期整合

Claude Code 有三套独立的记忆管理机制，分别解决短期、中期、长期记忆的问题。这部分在泄露之前是外界讨论比较多的一个话题，也是我认为这次源码泄露中技术含金量最高的部分。

### Context Compaction：9 段式结构化摘要

services/compact/prompt.ts（375 行）定义了上下文压缩的完整逻辑。当对话上下文接近 Token 上限时，Claude Code 不是简单地截断历史消息，而是用一个专门的 LLM 调用把对话历史压缩成一份结构化的摘要。

这份摘要有严格的 9 段格式要求：

```
1、Primary Request and Intent（主要需求和意图）
2、Key Technical Concepts（关键技术概念）
3、Files and Code Sections（涉及的文件和代码片段，包含实际代码）
4、Errors and fixes（遇到的错误和修复方案）
5、Problem Solving（问题解决过程）
6、All user messages（所有用户消息，逐条保留，不能遗漏）
7、Pending Tasks（待办任务）
8、Current Work（当前工作状态）
9、Optional Next Step（可选的下一步，包含原始对话的直接引用，防止任务漂移）
```

这里有两个工程细节值得展开：

第一个是 **scratchpad 机制**

摘要生成时，模型先在 <analysis> 标签里写一段分析草稿，用来梳理思路、提高摘要质量。生成完成后，formatCompactSummary() 函数会自动把这段草稿剥离掉，不让它进入正式的上下文。也就是说，用额外的 Token 消耗换取了更高质量的摘要输出，但这些额外的 Token 不会长期占用上下文窗口。

第二个是 **Partial Compaction**

Claude Code 不是把整个对话历史全部压缩成摘要，而是只压缩靠前的旧内容，保留最近几轮的原始对话（通过 recentMessagesPreserved 参数控制）。这样最近的上下文保持原貌，不会因为压缩而丢失细节，远期的上下文则变成高密度的结构化摘要。



### ExtractMemories：后台自动记忆萃取

services/extractMemories/prompts.ts 定义了一个后台运行的子 Agent，它作为主对话的分叉（Fork）独立运行，自动从对话中提取值得长期保存的信息。

这个机制有一个**前置判断**：如果主 Agent 在对话过程中已经主动写过记忆文件（通过 hasMemoryWritesSince 检测），extractMemories 就会跳过，不重复提取。只有主 Agent 没有写记忆的情况下，它才会自动介入。

在执行层面有一个严格的约束，就是 turn budget。extractMemories 要求先并行 Read 所有可能需要更新的记忆文件，再并行 Write，不允许交替读写。这个约束保证了记忆更新的原子性，避免出现读到半更新状态的问题。记忆本身也区分了 private memory（个人记忆）和 team memory（团队记忆），写入不同的文件路径。

这和我在工控知识库项目那期文章里提到的“**强制反馈 → 数据积累 → 持续优化**”闭环是同一个思路，区别在于 Claude Code 把这个闭环做到了完全自动化，用户不需要主动做任何反馈操作，系统自己就能从对话中提取有价值的信息。



### AutoDream：记忆整合

services/autoDream/consolidationPrompt.ts 定义了一个叫 Dream 的功能。简单说就是 Claude Code 在 Agent 空闲的时候，会自动对已有的记忆文件做一次整理和合并。

这个过程分四个阶段执行。Phase 1 是 **Orient（定位）**，ls 记忆目录，读取 MEMORY.md 索引文件，搞清楚当前有哪些记忆。Phase 2 是 **Gather recent signal（收集新信号）**，从最近的 session transcript 中 grep 出新产生的信息。Phase 3 是 **Consolidate（整合）**，把新信号和旧记忆合并，删除互相矛盾的旧记忆，还会把“昨天”“上周”这种相对日期转换成绝对日期，避免时间久了之后语义失真。Phase 4 是 **Prune and index（修剪和索引）**，确保 MEMORY.md 索引文件不超过 200 行或 25KB。

这个设计似乎是借鉴了认知科学中关于睡眠和记忆整合的研究，就是人在睡眠期间大脑会对白天的短期记忆做整理，把有用的转化为长期记忆，把无用的淘汰掉。Claude Code 用了一个类似的异步过程，在 Agent 不忙的时候做同样的事情，不得不说是个很好的巧思。

### 三层协同

为了方便理解，我把三层记忆系统的协同关系大致整理如下：

| 记忆层 | 机制               | 生命周期 | 触发条件                  | 数据载体         |
| ------ | ------------------ | -------- | ------------------------- | ---------------- |
| 短期   | Context Compaction | 单次会话 | 接近 Token 上限时自动触发 | 对话内摘要       |
| 中期   | ExtractMemories    | 跨会话   | 每轮对话结束后后台运行    | CLAUDE.md 文件   |
| 长期   | AutoDream          | 跨项目   | Agent 空闲时异步运行      | MEMORY.md + 索引 |

对比目前市面上的 Agent 框架，比如 LangGraph 的 Checkpointer、CrewAI 的 Memory，Claude Code 的方案在自动化程度和结构化程度上都高出不少。大多数框架的记忆功能还停留在把对话历史存起来的阶段，而 Claude Code 是做到了自动提取、自动整合、自动修剪的完整闭环。

## 工程细节：几个不起眼但很实用的设计

除了架构层面的东西，源码里还有不少细节设计，单独拿出来和各位说道说道。每一个都不算大，但放在一起就能看出 claude code 团队在生产环境中踩过多少坑，下面挑几个我觉得最有参考价值的。

### Agent 列表从内联改为 Attachment：省了 10.2% 的 Cache Token

AgentTool/prompt.ts 里有一个函数叫 shouldInjectAgentListInMessages()，专门处理 Agent 列表的注入方式。

原来的做法是把当前可用的 Agent 列表写在 AgentTool 的工具描述（tool description）里。但问题是，MCP 客户端连接、插件加载、权限变更的时候，Agent 列表会跟着变。列表一变，工具描述就变了，工具描述一变，整个 tools-block 的 Prompt Cache 就失效了。

源码注释里记录了具体的量化数据（AgentTool/prompt.ts 第 53 行 + attachments.ts 第 1482 行）：

> "The dynamic agent list was ~10.2% of fleet cache_creation tokens: MCP async connect, plugin load, permission changes all mutate the list..."



> 10.2% 的全局 cache_creation tokens，这个数字不小。解决方案是把 Agent 列表从工具描述里拿出来，改为通过 agent_listing_delta 这种 attachment 消息注入到对话中。这样工具描述变成了静态内容，Cache 不会再因为 Agent 列表的变化而失效。

这个优化思路其实是通用的，凡是用到 Prompt Cache 的场景，都应该把频繁变化的内容从 Cache 边界内移到边界外。

### Cron 调度的 Jitter 设计：避开整点

ScheduleCronTool/prompt.ts 里有一个很小但很聪明的设计。当用户说“每天早上 9 点提醒我”的时候，Claude Code 不会把 cron 表达式设成 0 9 * * *，而是会偏移几分钟，比如设成 57 8 * * * 或者 3 9 * * *。

原因很直接，全球所有用户说“9 点”都会映射到 :00，如果不做偏移，API 请求就会在整点集中爆发，给服务端造成压力峰值。Prompt 里原文是这么写的：

> "Pick a minute that is NOT 0 or 30... the user will not notice, and the fleet will."



用户不会注意到提醒是 8:57 还是 9:03 发出的，但服务端的负载曲线会平滑很多。这种用户无感但系统受益的设计，在高并发的企业级应用中非常实用。

### NO_TOOLS_PREAMBLE：防止模型在不该调工具的时候调工具

services/compact/prompt.ts 第 12-26 行有一个很有代表性的工程细节。

Context Compaction 是通过 Fork 主对话来执行的。Fork 会继承父对话的完整工具集，这是为了命中 Prompt Cache。但摘要任务本身不需要调用任何工具，只需要模型输出一段文本。

问题在于 Sonnet 4.6+ 这一代模型有时候会自作主张去调用工具，即使 Prompt 末尾已经写了不要调用工具。一旦工具调用被拒绝（因为 maxTurns: 1 限制了只有一轮机会），这一整轮压缩就失败了，只能降级到流式 Fallback 重新来。

源码注释里记录了精确的故障率（compact/prompt.ts 第 16 行）：

> "2.79% on 4.6 vs 0.01% on 4.5"

也就是说在 Sonnet 4.6 上，差不多每 36 次就有 1 次压缩会因为模型擅自调用工具而失败。解决方案是在 Prompt 的最前面（不是末尾）加一段强硬的 NO_TOOLS_PREAMBLE：

```
CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.- Do NOT use Read, Bash, Grep, Glob, Edit, Write, or ANY other tool.- Tool calls will be REJECTED and will waste your only turn — you will fail the task.
```

**把约束放在 Prompt 开头而不是末尾**，是因为模型对 Prompt 开头部分的注意力最集中。这个经验我在实际做项目的时候也经常验证到，关键的约束条件写在前面，比写在后面有效得多。

### Feature Flags 的编译时消除

Claude Code 通过 bun:bundle 提供的 feature() 函数来控制功能开关，比如 feature('VOICE_MODE')、feature('KAIROS')、feature('COORDINATOR_MODE') 等。

这套机制和一般的运行时 feature flag 不同。它是编译时的 Dead Code Elimination，也就是说如果某个 feature flag 是关闭状态，相关的代码在编译阶段就被完全移除了，构建产物里根本不会出现这部分代码。不会占内存，没有运行时判断分支的开销，开发团队可以在同一个代码仓库里并行开发多个未发布的功能，互不干扰。

从泄露的 feature flags 也能看出一些 Anthropic 尚未发布的功能方向：PROACTIVE（主动模式）、KAIROS（定时任务系统）、DAEMON（守护进程模式）、VOICE_MODE（语音交互）、MONITOR_TOOL（监控工具）等。这些功能的代码已经写好了，只是通过 feature flag 控制着不对外暴露。

## 工程视角：从 Prompt Engineering 到 Harness Engineering

整体看完 Claude Code 的源码，我最大的感受其实不是某个具体技巧有多巧，而是这套源码很好地体现了行业正在发生的一个趋势变化。

### 三个阶段的演进

个人感觉，过去三年大模型应用开发的重心经历了以下三个阶段的迁移：

23 到 24 年，市面上谈得最多的是 Prompt Engineering，也就是怎么写一条好的结构化的提示词，让模型输出更准确的结果。这个阶段的核心假设是只要 Prompt 写得够好，模型就能给出好的输出。

到了 25 年，市面上讨论 Context Engineering/上下文工程开始多了起来，核心关注的是怎么管理、压缩、保留和传递上下文信息，让模型在长时间运行中不会忘事。Claude Code 的三层记忆系统整体看下来（Compaction / ExtractMemories / AutoDream）也是这个阶段的典型产物。

到了 26 年，一个更大的概念开始被讨论，也就是最近海内外还是烂大街的 **Harness Engineering**。这个概念的核心观点是模型本身在快速进化，但模型能力的差异在缩小，真正决定一个 Agent 系统能不能在生产环境中稳定运行的，不是模型本身，而是围绕模型构建的那一整套控制系统。这套系统包括工具编排、记忆管理、错误恢复、降级兜底、权限控制、可观测性等等，行业里把它叫做 Harness（直译是缰绳，意思是控制和约束模型行为的基础设施）。

一句话总结就是：“**Agents aren't hard; the harness is hard.**”（做 Agent 不难，难的是做 Harness。）

### Claude Code 对三个阶段的覆盖

回头来看 Claude Code 的源码，它对这三个阶段的覆盖是很完整的。

**Prompt Engineering 层面**，它有精心设计的多层 Prompt 组装（System / Mode / Tools / Project / Git / History 六层动态拼装），有 Coordinator 的 370 行系统提示词，有 AgentTool 里详尽的 Fork 规范。

**Context Engineering 层面**，它有完整的三层记忆系统（Compaction 做短期压缩、ExtractMemories 做中期萃取、AutoDream 做长期整合），有 Partial Compaction 的部分保留机制，有 <analysis> scratchpad 的质量优化。

**Harness Engineering 层面**，它有NO_TOOLS_PREAMBLE 这种“**Prompt 约束 → 代码校验 → 降级兜底**”的三层防护，有 Cron 调度的 Jitter 设计，有 feature flag 的编译时消除，有 maxTurns 的硬性轮次限制，有 Prompt Cache 的精细化管理。

这三个层面不是递进替代的关系，而是同时存在、各自负责不同层面的问题。Prompt 管的是怎么跟模型说话，Context 管的是模型能记住什么，Harness 管的是模型出错了怎么办。

### 可迁移到企业场景的三个模式

最后，我想可以从这套源码中能提炼出三个通用模式，对做企业级大模型应用都有直接的参考价值。

第一个是三层防护：**Prompt 约束 → 代码校验 → 降级兜底**。 Claude Code 在每一个可能出错的环节都能看到这个模式。比如 NO_TOOLS_PREAMBLE 用 Prompt 约束模型不要调用工具，maxTurns: 1 用代码限制只有一轮机会，万一还是失败就降级到流式 Fallback 重新来。这和我在之前介绍过的售前报价 Agent 项目中设计的 SKU 校验三道防线（Prompt 强约束 → 代码事后校验 → 自动替换兜底）是同一个工程范式。不能指望 Prompt 能 100% 约束模型行为，任何关键逻辑都必须有代码层面的兜底。

第二个是**推理和执行的分离**。 Claude Code 的架构贯穿一个原则：LLM 只负责推理和决策，格式处理、计算、文件操作这些确定性的工作交给代码。Compaction 的 formatCompactSummary() 负责格式清理，Coordinator 做综合判断而 Worker 做具体执行，Cron 调度中 LLM 理解"每天 9 点"而代码负责 Jitter 偏移。这和我在报价 Agent 中坚持的"模板 + JSON 填充"原则完全一致，在严肃的生产类场景里，LLM 负责内容生成，模板负责格式约束，代码负责逻辑校验。

第三个是**无感数据飞轮**。 我在之前的很多项目里，反馈到优化的闭环需要用户主动参与，比如报价 Agent 的强制反馈才能下载，工控知识库的点赞/点踩。Claude Code 的 ExtractMemories 把这个闭环完全自动化了，不需要用户做任何额外操作，系统自己从对话中提取有价值的记忆并持久化。最好的数据收集方式，就是让用户在完成本职工作的过程中自然地贡献数据。