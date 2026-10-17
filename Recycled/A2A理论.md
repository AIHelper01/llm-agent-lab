# 什么是A2A？

A2A协议是一种开放标准，能够实现无缝通信， AI Agent之间的协作。它为构建的Agent提供了一种通用语言 采用多样化的框架和不同供应商，促进互操作性 打破壁垒。Agent是自主的问题解决者，能够行动 独立于他们的环境中。A2A允许来自不同Agent 开发者，基于不同的框架，属于不同的组织 团结起来，共同努力。

A2A解决了AIAgent协作中的关键挑战。它提供 一种为Agent间互动提供标准化方法。

### A2A解决的问题

考虑用户请求AI助手来规划国际旅行。就是这样 任务涉及协调多个专业Agent，例如：

- 机票预订Agent
- 酒店预订Agent
- 本地旅游推荐Agent
- 货币兑换Agent

没有A2A，整合这些多样化的Agent存在若干挑战：

- **Agent Exposure **Agent曝光：开发者通常将智能体包装为工具，以便向其他智能体公开，类似于在多智能体控制平台中公开工具的方式（MCP）。然而，这种方法效率不高，因为智能体的设计初衷是直接进行协商。将智能体包装为工具会限制其能力。A2A允许智能体以其原始形式公开，无需进行此类包装。
- **Custom Integrations** 定制化集成：每次交互都需要专门的端到端解决方案，这会带来巨大的工程开销。
- **Slow Innovation**创新缓慢：为每次新集成进行定制开发会拖慢创新速度。
- **Scalability Issues**可扩展性问题：随着智能体和交互数量的增加，系统变得难以扩展和维护。
- **Interoperability**互操作性受限：这种方法限制了互操作性，阻碍了复杂人工智能生态系统的自然形成。
- **Security Gaps**安全漏洞：临时搭建的通信通常缺乏一致的安全措施。

A2A协议通过建立AI智能体之间的互操作性，使其能够可靠、安全地进行交互，从而应对这些挑战。

### A2A 示例情景

本节通过一个示例场景，旨在说明在AI智能体间进行复杂交互时，采用A2A（Agent2Agent）协议的诸多益处。

#### 用户的复杂请求

用户向AI助手提出了一个复杂的请求，例如“计划一次国际旅行”。

![image-20260401221333944](E:\ai-showcase\3.4大模型-Agent\assets\image-20260401221333944.png)



#### 协作的必要性

AI助手收到请求后，意识到需要调用多个专业化的Agent来完成任务。这些Agent包括机票预订Agent、酒店预订Agent、货币兑换Agent和本地旅游活动Agent。

![image-20260401221352900](E:\ai-showcase\3.4大模型-Agent\assets\image-20260401221352900.png)

<svg id="__mermaid_1" width="100%" xmlns="http://www.w3.org/2000/svg" class="flowchart" style="max-width: 545.6875px;" viewBox="0 0 545.6875 475.9573669433594" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="__mermaid_1_flowchart-v2-pointEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="__mermaid_1_flowchart-v2-pointStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="__mermaid_1_flowchart-v2-circleEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="__mermaid_1_flowchart-v2-circleStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="__mermaid_1_flowchart-v2-crossEnd" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="__mermaid_1_flowchart-v2-crossStart" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><g class="root"><g class="clusters"><g class="cluster" id="subGraph0" data-look="classic"><rect style="" x="227.6875" y="8" width="310" height="459.95738983154297"></rect><g class="cluster-label" transform="translate(314.9815368652344, 8)"><foreignObject width="135.41192626953125" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table-cell; white-space: nowrap; line-height: 1.5;"><span class="nodeLabel" style="fill: rgb(51, 51, 51); color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;"><p style="margin: 0px; color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif; background-color: transparent;">Specialized Agents</p></span></div></foreignObject></g></g></g><g class="edgePaths"><path d="M111.15,204.985L126.406,182.487C141.662,159.989,172.175,114.992,191.598,92.494C211.021,69.996,219.354,69.996,229.112,69.996C238.871,69.996,250.054,69.996,255.646,69.996L261.237,69.996" id="L_AI_Assistant_FBA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_AI_Assistant_FBA_0" data-points="W3sieCI6MTExLjE0OTgzNzczMzYzOTQ5LCJ5IjoyMDQuOTg1MDg2NDQxMDQwMDR9LHsieCI6MjAyLjY4NzUsInkiOjY5Ljk5NTczODk4MzE1NDN9LHsieCI6MjI3LjY4NzUsInkiOjY5Ljk5NTczODk4MzE1NDN9LHsieCI6MjY1LjIzNzIyMDc2NDE2MDE2LCJ5Ijo2OS45OTU3Mzg5ODMxNTQzfV0=" marker-end="url(#__mermaid_1_flowchart-v2-pointEnd)"></path><path d="M143.975,204.985L153.761,199.819C163.546,194.652,183.117,184.32,197.069,179.154C211.021,173.987,219.354,173.987,227.039,173.987C234.723,173.987,241.759,173.987,245.276,173.987L248.794,173.987" id="L_AI_Assistant_HRA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_AI_Assistant_HRA_0" data-points="W3sieCI6MTQzLjk3NTQ3NDM3MzA4OTg0LCJ5IjoyMDQuOTg1MDg2NDQxMDQwMDR9LHsieCI6MjAyLjY4NzUsInkiOjE3My45ODcyMTY5NDk0NjI5fSx7IngiOjIyNy42ODc1LCJ5IjoxNzMuOTg3MjE2OTQ5NDYyOX0seyJ4IjoyNTIuNzk0MDM2ODY1MjM0MzgsInkiOjE3My45ODcyMTY5NDk0NjI5fV0=" marker-end="url(#__mermaid_1_flowchart-v2-pointEnd)"></path><path d="M143.975,258.977L153.761,264.143C163.546,269.309,183.117,279.642,197.069,284.808C211.021,289.974,219.354,289.974,227.021,289.974C234.688,289.974,241.688,289.974,245.188,289.974L248.688,289.974" id="L_AI_Assistant_CCA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_AI_Assistant_CCA_0" data-points="W3sieCI6MTQzLjk3NTQ3NDM3MzA4OTg0LCJ5IjoyNTguOTc2NTY0NDA3MzQ4NjN9LHsieCI6MjAyLjY4NzUsInkiOjI4OS45NzQ0MzM4OTg5MjU4fSx7IngiOjIyNy42ODc1LCJ5IjoyODkuOTc0NDMzODk4OTI1OH0seyJ4IjoyNTIuNjg3NSwieSI6Mjg5Ljk3NDQzMzg5ODkyNTh9XQ==" marker-end="url(#__mermaid_1_flowchart-v2-pointEnd)"></path><path d="M109.888,258.977L125.354,283.474C140.821,307.972,171.754,356.967,191.388,381.464C211.021,405.962,219.354,405.962,230.879,405.962C242.403,405.962,257.118,405.962,264.476,405.962L271.834,405.962" id="L_AI_Assistant_LTA_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_AI_Assistant_LTA_0" data-points="W3sieCI6MTA5Ljg4NzY1ODEyNDM2MzI3LCJ5IjoyNTguOTc2NTY0NDA3MzQ4NjN9LHsieCI6MjAyLjY4NzUsInkiOjQwNS45NjE2NTA4NDgzODg3fSx7IngiOjIyNy42ODc1LCJ5Ijo0MDUuOTYxNjUwODQ4Mzg4N30seyJ4IjoyNzUuODMzODA4ODk4OTI1OCwieSI6NDA1Ljk2MTY1MDg0ODM4ODd9XQ==" marker-end="url(#__mermaid_1_flowchart-v2-pointEnd)"></path></g><g class="edgeLabels"><g class="edgeLabel"><g class="label" data-id="L_AI_Assistant_FBA_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="background-color: rgba(232, 232, 232, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel" style="fill: rgb(255, 255, 255); color: rgb(54, 70, 78); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_AI_Assistant_HRA_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="background-color: rgba(232, 232, 232, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel" style="fill: rgb(255, 255, 255); color: rgb(54, 70, 78); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_AI_Assistant_CCA_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="background-color: rgba(232, 232, 232, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel" style="fill: rgb(255, 255, 255); color: rgb(54, 70, 78); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_AI_Assistant_LTA_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="background-color: rgba(232, 232, 232, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel" style="fill: rgb(255, 255, 255); color: rgb(54, 70, 78); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node default" id="flowchart-FBA-0" transform="translate(382.6875, 69.9957389831543)"><rect class="basic label-container" style="" x="-117.45027923583984" y="-26.99573802947998" width="234.9005584716797" height="53.99147605895996"></rect><g class="label" style="" transform="translate(-87.45027923583984, -11.99573802947998)"><rect></rect><foreignObject width="174.9005584716797" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel" style="fill: rgb(51, 51, 51); color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;"><p style="margin: 0px; color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;">✈️ Flight Booking Agent</p></span></div></foreignObject></g></g><g class="node default" id="flowchart-HRA-1" transform="translate(382.6875, 173.9872169494629)"><rect class="basic label-container" style="" x="-129.89346313476562" y="-26.99573802947998" width="259.78692626953125" height="53.99147605895996"></rect><g class="label" style="" transform="translate(-99.89346313476562, -11.99573802947998)"><rect></rect><foreignObject width="199.78692626953125" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel" style="fill: rgb(51, 51, 51); color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;"><p style="margin: 0px; color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;">🏨 Hotel Reservation Agent</p></span></div></foreignObject></g></g><g class="node default" id="flowchart-CCA-2" transform="translate(382.6875, 289.9744338989258)"><rect class="basic label-container" style="" x="-130" y="-38.99147605895996" width="260" height="77.98295211791992"></rect><g class="label" style="" transform="translate(-100, -23.99147605895996)"><rect></rect><foreignObject width="200" height="47.98295211791992"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table; white-space: break-spaces; line-height: 1.5; max-width: 200px; text-align: center; width: 200px;"><span class="nodeLabel" style="fill: rgb(51, 51, 51); color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;"><p style="margin: 0px; color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;">💱 Currency Conversion Agent</p></span></div></foreignObject></g></g><g class="node default" id="flowchart-LTA-3" transform="translate(382.6875, 405.9616508483887)"><rect class="basic label-container" style="" x="-106.85369110107422" y="-26.99573802947998" width="213.70738220214844" height="53.99147605895996"></rect><g class="label" style="" transform="translate(-76.85369110107422, -11.99573802947998)"><rect></rect><foreignObject width="153.70738220214844" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel" style="fill: rgb(51, 51, 51); color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;"><p style="margin: 0px; color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;">🚌 Local Tours Agent</p></span></div></foreignObject></g></g><g class="node default" id="flowchart-AI_Assistant-4" transform="translate(92.84375, 231.98082542419434)"><rect class="basic label-container" style="" x="-84.84374618530273" y="-26.99573802947998" width="169.68749237060547" height="53.99147605895996"></rect><g class="label" style="" transform="translate(-54.843746185302734, -11.99573802947998)"><rect></rect><foreignObject width="109.68749237060547" height="23.99147605895996"><div xmlns="http://www.w3.org/1999/xhtml" style="display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel" style="fill: rgb(51, 51, 51); color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;"><p style="margin: 0px; color: rgb(54, 70, 78); font-family: &quot;Google Sans&quot;, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, sans-serif;">🤖 AI Assistant</p></span></div></foreignObject></g></g></g></g></g></svg>

#### 互操作性挑战

核心问题：由于每个Agent都采用独立的开发和部署模式，它们无法协同工作。

缺乏标准化协议的后果是，这些Agent不仅无法相互协作，甚至无法发现彼此的功能。各个Agent之间是彼此孤立的。

#### “With A2A”的解决方案

A2A协议为Agent之间的通信提供了标准方法和数据结构，使其无论底层实现如何都能相互通信。因此，相同的Agent可以作为互连系统使用，通过标准化协议进行无缝通信。

此时，AI助手充当协调者，从所有支持A2A协议的Agent那里接收到统一的信息。随后，它将生成一个完整、统一的旅行计划，作为对用户初始请求的无缝响应。

![显示用户、A2A客户端（客户端Agent）和A2A服务器（远程Agent）的A2A演员](E:\ai-showcase\3.4大模型-Agent\assets\a2a-actors.png)

### A2A的核心优势

实施A2A协议为整个AI生态系统带来显著优势：

- **安全协作**：缺乏标准时，难以确保Agent间的通信安全。A2A采用HTTPS进行安全通信，并保持操作的封装性，确保在协作过程中Agent无法窥探其他Agent的内部运作。
- **互操作性**：A2A打破了不同AI Agent生态系统间的壁垒，使来自不同供应商和框架的Agent能够无缝协同工作。
- **Agent自主性**：A2A允许Agent在与其他Agent协作时，保持其独立能力和自主实体的特性。
- **降低集成复杂度**：该协议标准化了Agent间的通信，使团队能够专注于其Agent所提供的独特价值。
- **支持长时运行操作**：该协议支持长时运行操作以及基于服务器发送事件的流式传输和异步执行。

### A2A的关键设计原则

A2A的开发遵循优先考虑广泛采用、企业级能力和面向未来的原则。

- **简洁性**：A2A利用HTTP、JSON-RPC和服务器发送事件等现有标准。这避免了对核心技术的重复开发，并加速了开发者的采用。
- **企业就绪**：A2A解决了关键的企业需求。它与标准的网络实践保持一致，具备强大的身份验证、授权、安全性、隐私保护、追踪和监控能力。
- **异步性**：A2A原生支持长时间运行的任务。它能处理Agent或用户可能不会保持持续连接的场景，并使用流式传输和推送通知等机制。
- **模态无关性**：该协议允许Agent使用多种内容类型进行通信。这使得交互不仅能超越纯文本，还能实现丰富和灵活的交互。
- **不透明执行**：Agent之间在无需暴露其内部逻辑、内存或专有工具的情况下，就能进行有效协作。交互依赖于声明的能力和交换的上下文。这既保护了知识产权，也增强了安全性。

### 理解Agent栈：A2A、MCP、Agent框架与模型

A2A是更广泛的Agent堆栈中的一环，该堆栈包括：

**A2A**： 标准化部署在不同组织、使用不同框架开发的Agent之间的通信。

**MCP**： 将模型与数据及外部资源连接起来。

**框架**： 提供构建Agent的工具包。

**模型**： Agent进行推理的基础，可以是任何大语言模型。

![ADK与MCP](E:\ai-showcase\3.4大模型-Agent\assets\agentic-stack.png)

#### A2A和MCP

在更广泛的AI通信生态系统中，您可能已了解一些旨在促进Agent、模型和工具间交互的协议。其中，模型上下文协议（MCP）是一个新兴标准，专注于将大语言模型与数据和外部资源连接起来。

Agent2Agent（A2A）协议则旨在标准化AI Agent之间的通信，特别是部署在外部系统中的Agent。A2A旨在与MCP形成互补，解决Agent交互中一个不同但相关的方面。

- **MCP的核心目标**：降低Agent与工具及数据连接的复杂性。工具通常是无状态的，并执行特定的、预定义的功能。

- **A2A的核心目标**：使Agent能够以其原生模式进行协作，允许它们以Agent的身份进行通信，而不是被限制在类似工具的交互中。这支持了复杂、多轮的交互，使Agent可以进行推理、规划和任务委派。

![ADK + MCP](E:\ai-showcase\3.4大模型-Agent\assets\a2a-mcp-readme.png)

#### A2A和ADK[¶](https://a2a-protocol.org/latest/topics/what-is-a2a/#a2a-and-adk)

 [Agent Development Kit](https://google.github.io/adk-docs/) 是一款由Google开发的开源智能体开发工具包。A2A是一种用于智能体之间通信的协议，它使得不同开发框架构建的智能体能够进行通信。ADK是一个灵活、模块化的框架，用于开发和部署AI智能体。虽然它为Gemini AI和Google生态系统进行了优化，但ADK本身是模型无关、部署无关的，并旨在兼容其他框架。

### A2A 请求生命周期

A2A请求生命周期是一个详细描述请求所遵循的四个主要步骤的序列：Agent发现、身份验证、API请求和API响应。下图深入展示了操作流程，说明了客户端、A2A服务器和认证服务器之间的交互。

![image-20260401221441963](E:\ai-showcase\3.4大模型-Agent\assets\image-20260401221441963.png)



# A2A的核心概念与组成部分

A2A 采用一套核心概念来定义Agent之间的交互方式。理解这些核心构建模块，对于开发或集成符合A2A标准的系统至关重要。

![显示用户、A2A客户端（客户端Agent）和A2A服务器（远程Agent）的A2A演员](E:\ai-showcase\3.4大模型-Agent\assets\a2a-actors2.png)

## A2A交互中的核心参与者

- **User**: 最终用户，可以是人类操作员或自动化服务。用户发起请求或定义一个需要由一个或多个AI Agent协助达成的目标。
- **A2A Client(Client Agent)**: 代表用户行事的应用程序、服务或另一个AI Agent。客户端使用A2A协议发起通信。
- **A2A Server(Remote Agent)**: 一个实现了A2A协议的HTTP端点的AI Agent或智能体系统。它接收来自客户端的请求，处理任务，并返回结果或状态更新。从客户端的视角看，远程Agent就像一个不透明的（黑盒）系统，意味着其内部运作、内存或工具均不对外暴露。

## 基本沟通要素

下表描述了A2A中的基本通信要素：

| 要素       | 描述                                                         | 核心用途                                                   |
| ---------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| Agent Card | 描述Agent身份、能力、端点、技能和认证要求的JSON元数据文档。  | 使Client能够发现Agent，并了解如何安全、有效地与其交互。    |
| Task       | 由Agent发起的、有状态的、带有唯一ID和定义生命周期的**工作单元**。 | 便于跟踪长时间运行的操作，并支持多轮交互与协作。           |
| Message    | client与Agent之间的一次对话回合，包含内容和一个角色。        | 传达不一定是正式产物的指令、上下文、问题、答案或状态更新。 |
| Part       | 在Message和Artifact中使用的基本**内容容器**。一个Part可包含：文本内容、文件引用或结构化数据。 | 为Agent在消息和产物中交换各种内容类型提供了灵活性。        |
| Artifact   | 在Task执行过程中由Agent生成的有形输出。                      | 交付Agent工作的具体成果，确保输出是结构化的且可检索的。    |

****


## 交互机制

A2A协议支持多种交互模式，以适应不同的响应性和持久性需求。这些机制确保了无论任务的复杂程度或持续时间如何，Agent之间都能高效可靠地交换信息：

- **Request/Response (Polling)请求/响应**：client发送请求，server返回响应。对于长时间运行的任务，client会定期向server轮询更新。

- **Streaming with Server-Sent Events (SSE)流式传输**：client发起一个流，通过一个开放的HTTP连接，从server实时接收增量结果或状态更新。

- **Push Notifications推送通知**：对于运行时间极长的任务或client可能离线的场景，当任务有重要更新时，server可以主动向client提供的webhook发送异步通知。、

  

## Agent Card

Agent Card是一个JSON文档，充当一张数字名片，用于初始发现和交互设置。它提供了关于一个Agent的基本元数据。client会解析这些信息，以判断某个Agent是否适合给定的任务、如何构建请求以及如何进行安全通信。关键信息包括身份、服务端点、A2A能力、认证要求和技能列表。

## Message 与 Part

一个Message代表了client与Agent之间的一次对话回合。它包含一个角色和一个唯一的messageId。其内容由**一个或多个**Part对象构成，这些Part是承载实际内容的**细粒度容器**。这种设计使得A2A能够与内容形态无关。

Part对象是一个灵活的容器，它通过一种“多选一”的结构，可以包含不同类型的内容。**一个Part必须包含且仅包含以下其中一个内容字段**：

- `text`： 包含纯文本内容的字符串。
- `raw`： 包含二进制文件数据的字节数组。
- `url`： 引用外部文件内容的字符串URI。
- `data`： 用于机器可读数据的结构化JSON值。

此外，**每个Part都可以包含以下可选字段**：

- `mediaType`： 内容的MIME类型。
- `filename`： 文件或内容的可选名称。
- `metadata`： 用于附加上下文的键值对映射。

## Artifact

一个Artifact代表远程Agent在任务处理过程中生成的有形输出或具体成果。与普通的Message不同，Artifact是实际交付物。一个Artifact具有唯一的artifactId、一个人类可读的名称，并且由一个或多个Part对象构成。Artifact与任务的**生命周期紧密关联**，并且可以以增量流式的方式传输给client。

## Agent 响应：Task 或 Message

Agent的响应可以是一个新的Task，也可以是一个Message。

- 当Agent需要执行一个**长时间运行的操作**时，它会返回一个新的Task。
- 当Agent能够**立即响应**时，它会直接返回一个Message。





## 其他重要概念



- **Context (contextId):**： 一个由server生成的标识符，可用于逻辑上将多个相关的Task对象分组，从而为一**系列交互**提供上下文。
- **Transport and Format传输与格式**： A2A通信通过HTTP进行。**JSON-RPC 2.0**被用作所有请求和响应的**有效负载格式**。
- **Authentication & Authorization认证与授权**： A2A依赖标准的网络安全实践。认证要求在Agent Card中声明，凭证（如OAuth令牌、API密钥）通常通过HTTP标头传递，与A2A协议消息本身分开。更多信息，请参阅**企业就绪特性**。
- **Agent Discovery Agent 发现**： client通过此过程来查找Agent Card，以了解可用的A2A Server及其能力。更多信息，请参阅**Agent 发现**。
- **Extensions扩展**： A2A允许Agent在其AgentCard中声明自定义协议扩展。更多信息，请参阅**扩展**。

# A2A中的发现Agent

为了使用A2A协议进行协作，AI Agent首先需要找到彼此并了解对方的能力。A2A通过**Agent Card**标准化了Agent的自我描述。然而，发现这些Agent Card的具体方法因部署环境和需求而异。

Agent Card定义了一个Agent能提供什么。有多种策略可供**client Agent**用来发现这些卡片。策略的选择取决于部署环境和安全要求。

## Agent Card的作用

Agent Card是一个JSON文档，充当A2A Server的数字“名片”。它对于Agent发现和交互至关重要。Agent Card中包含的关键信息如下：

- **Identity身份**： 包括名称、描述和提供商信息。
- **Service Endpoint服务端点**： 指定A2A服务的URL。
- **A2A Capabilities A2A 能力**： 列出支持的功能，例如流式传输或推送通知。
- **Authentication认证**： 详细说明所需的认证方案。
- **Skills技能**： 使用`AgentSkill`对象描述Agent的能力，包括其ID、名称、描述、输入模式、输出模式和示例。

client Agent使用Agent Card来判断一个Agent是否适合某项任务、如何构建请求以及如何确保通信安全。

## 发现策略

client Agent发现远程Agent Card的常见策略：

**1. Well-Known URI**

此方法推荐用于公共Agent或在特定领域内需要广泛发现的Agent。

- **机制**： A2A Server通过在其域上托管一个标准化的、众所周知的URI来使其Agent Card可被发现。标准路径是 `https://{agent-server-domain}/.well-known/agent-card.json`，遵循 RFC 8615 的原则。
- **过程**：
  1. client Agent通过程序化方式获知或发现潜在的A2A Server域名。
  2. client向此路径发起HTTP GET请求。
  3. 如果Agent Card存在且可访问，server将其作为JSON响应返回。
- **优点**：
  - 易于实现
  - 遵循标准
  - 便于自动化发现
- **注意事项**：
  - 最适合开放或受控域内的发现场景。
  - 如果提供的Agent Card包含敏感细节，其服务端点需要认证。

**2. 托管注册中心**

此方法应用于企业环境或公共市场，其中Agent Card通常由中央注册中心管理。托管注册中心充当中央存储库，允许client根据“技能”或“标签”等条件查询和发现Agent。

- **机制**： 一个中介服务维护着一个Agent Card的集合。Client查询此注册中心，根据各种条件查找Agent。
- **过程**：
  1. A2A Server将其Agent Card发布到注册中心。
  2. client Agent调用注册中心的API，并根据特定技能等条件进行搜索。
  3. 注册中心返回匹配的Agent Card或其引用。
- **优点**：
  - 集中的管理和治理。
  - 基于能力的发现。
  - 支持访问控制和信任框架。
  - 适用于私人和公共市场。
- **注意事项**：
  - 需要部署和维护注册中心服务。
  - 当前A2A规范并未为托管注册中心规定标准API。

**3. 直接配置 / 私有发现**

此方法用于紧密耦合的系统、私有Agent或开发目的，其中client被直接配置了Agent Card信息或URL。

- **机制**： Client应用程序利用硬编码的详细信息、配置文件、环境变量或专有API进行发现。
- **过程**： 该过程特定于应用程序的部署和配置策略。
- **优点**： 在已知的、静态关系中建立连接非常简单。
- **注意事项**：
  - 对于动态发现场景不灵活。
  - Agent Card信息的变更需要client重新配置。
  - 基于专有API的发现也缺乏标准化。



## 保护 Agent Card

Agent Card包含敏感信息，例如：

- 内部或受限Agent的URL。
- 敏感技能的描述。

**保护机制**

为降低风险，应考虑以下保护机制：

- **认证的Agent Card**： 我们建议对包含敏感信息或提供更详细版本的Agent Card使用**经过认证的扩展Agent Card**。
- **安全的端点**： 在提供Agent Card的HTTP端点上实施访问控制，方法包括：
  - TLS
  - 网络限制
  - HTTP认证
- **注册中心选择性披露**： 注册中心根据client的身份和权限返回不同的Agent Card。

任何包含敏感数据的Agent Card都必须通过认证和授权机制进行保护。A2A规范强烈建议使用带外动态凭据，**而不是**在Agent Card中嵌入静态密钥。

## 缓存注意事项

Agent Card描述了一个Agent的能力，其内容通常不常改变。遵循标准的HTTP缓存实践可以减少不必要的网络请求，同时确保client最终能获得更新信息。

**服务器指引**

托管Agent Card端点的server应在响应中包含HTTP缓存头。使用适当的`max-age`指令的`Cache-Control`头部，允许client和中间件在指定时间内缓存Agent Card。包含一个基于Agent Card的`version`字段或内容哈希值生成的`ETag`头部，能使client发起**条件请求**，避免重新下载未更改的Agent Card。

**客户端指引**

获取Agent Card的client应遵循标准的HTTP缓存语义。当缓存的Agent Card过期时，client应使用条件请求，而不是无条件地重新获取完整的Agent Card。当server没有提供缓存头时，client可以应用一个合理的默认缓存时间。

对于**扩展Agent Card**，client也应遵循规范中描述的基于会话范围的缓存指引。

规范性要求请参阅规范的第8.6节。

**未来考虑**

A2A社区正在探索如何标准化注册中心交互或高级发现协议。



# 附：A2A与MCP：详细比较

在AI智能体开发领域，出现了两种关键协议类型以促进互操作性。一种连接智能体与工具和资源，另一种则实现智能体之间的协作。Agent2Agent协议和Model Context Protocol分别满足这些不同但高度互补的需求。

## **Model Context Protocol**

MCP 定义了AI Agent如何与单个工具和资源交互及使用它们。

该协议提供以下能力：

- 标准化AI模型和Agent如何连接并与工具、API和其他外部资源交互。
- 定义了一种结构化方式来描述工具能力，类似于大语言模型中的函数调用。
- 将输入传递给工具并接收结构化输出。
- 支持常见用例，例如LLM调用外部API、Agent查询数据库，或Agent连接到预定义函数。

## **Agent2Agent Protocol**

A2A协议侧重于使不同的Agent能够相互协作以实现共同目标。

该协议提供以下能力：

- 标准化独立的、通常不透明的AI Agent之间如何作为对等节点进行通信和协作。
- 为Agent提供一种应用层协议，用于相互发现、协商交互、管理共享任务以及交换对话上下文和复杂数据。
- 支持典型用例，包括客户服务Agent将查询委托给计费Agent，或旅行Agent与航班、酒店和活动Agent进行协调。

## 为何需要不同协议？

MCP和A2A协议对于构建复杂的AI系统都至关重要，它们解决的是不同但高度互补的需求。A2A与MCP之间的区别取决于Agent与之交互的对象。

**工具与资源（MCP）**：

- **特点**： 这些通常是具有明确定义、结构化输入和输出的**原语**。它们执行特定的、通常是无状态的功能。例如计算器、数据库查询API或天气查询服务。
- **目的**： Agent**使用**工具来收集信息和执行离散功能。

**Agent(A2A)**：

- **特点**： 这些是更具**自主性**的系统。它们会推理、计划、使用多种工具、在较长的交互中维护状态，并进行复杂、通常是多轮的对话，以实现新颖的或不断变化的任务。
- **目的**： Agent与其他Agent**协作**，以处理更广泛、更复杂的目标。





### A2A ❤️ MCP：智能体系统的互补协议

一个Agentic应用程序可能主要使用A2A协议来与其他Agent进行通信。而每个独立的Agent在其内部，则使用MCP协议与其特定的工具和资源进行交互。

![A2A和MCP协同工作的示意图。用户通过A2A与AgentA交互。AgentA通过A2A与AgentB交互。AgentB使用MCP与工具1和工具2交互。](E:\ai-showcase\3.4大模型-Agent\assets\a2a-mcp.png)

一个Agentic应用程序可能使用A2A与其他Agent通信，而每个Agent在内部则使用MCP与其特定的工具和资源进行交互。

**示例场景：汽车维修店**

设想一家由自主AI Agent“机械师”组成的汽车维修店。这些机械师使用专用工具（如车辆诊断扫描仪、维修手册和升降平台）来诊断和修复问题。维修过程可能涉及大量的对话、研究以及与零件供应商的互动。

- **客户交互**： 客户通过A2A协议与“门店经理”Agent进行沟通。例如，客户可能会说：“我的车发出咔嗒咔嗒的异响。”
- **多轮诊断对话**： 门店经理Agent使用A2A协议进行多轮诊断对话。例如，经理可能会问：“您能发送一段异响的视频吗？”或“我看到有些液体泄漏。这种情况持续多久了？”
- **内部工具使用**： 被门店经理指派任务的机械师Agent需要使用其专业工具来诊断问题。机械师Agent通过MCP协议与其专业工具交互，例如调用车辆诊断扫描工具、维修手册数据库工具或升降平台工具。
- **供应商交互**： 机械师Agent确定需要某个特定零件。它通过A2A协议与“零件供应商”Agent沟通来订购零件。例如，机械师Agent可能会问：“你们是否有丰田凯美瑞2018款的零件#12345库存？”
- **订单处理**： 同样符合A2A协议的零件供应商Agent会做出回应，可能会促成一份订单。

在此示例中：

- **A2A协议**促进了客户与维修店之间，以及维修店Agent与外部供应商Agent之间更**高层级、会话式、面向任务**的交互。
- **MCP协议**使机械师Agent能够使用其**特定的、结构化的工具**来执行诊断和维修功能。

一个A2A Server可以将其部分技能公开为与MCP兼容的资源。然而，A2A的主要优势在于其支持**更灵活、有状态、协作式**的交互。这些交互超越了典型的工具调用。A2A侧重于Agent在任务上的**协作**，而MCP则侧重于Agent**使用**工具能力。

## 将A2A Agent表示为MCP资源

一个A2A Server（远程Agent）可以将其部分技能公开为与MCP兼容的资源，特别是当这些技能定义明确且能以更像工具、无状态的方式调用时。在这种情况下，另一个Agent可能会通过MCP风格的描述来“发现”这个A2A Agent的特定技能。

然而，A2A的主要优势在于其支持**更灵活、有状态、协作式**的交互，这些交互超越了典型的工具调用。A2A是关于Agent在任务上的**合作**，而MCP则更侧重于Agent**使用**能力。

通过同时利用A2A进行Agent间协作，并利用MCP进行工具集成，开发者可以构建更强大、更灵活、更具互操作性的AI系统。


