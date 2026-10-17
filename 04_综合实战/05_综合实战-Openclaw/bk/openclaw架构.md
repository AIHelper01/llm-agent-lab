------

# 🦞 OpenClaw Architecture Deep Dive

### — From Event Flow to Agent Execution Semantics

------

# 0️⃣ TL;DR（一句话理解系统）

> **OpenClaw = 一个由 Gateway 驱动、基于事件、通过 Tool 执行副作用的 Session 隔离型 Agent 系统**

------

# 1️⃣ 架构总览（四层 + 两条流）

```
┌─────────────────────────────────────────────────────────────┐
│                    L1: Channel (接入层)                      │
└─────────────────────────────┬───────────────────────────────┘
                              │ Event（统一输入）
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   L2: Gateway (控制中枢)                     │
└─────────────────────────────┬───────────────────────────────┘
                              │ 调度 + sessionKey
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    L3: Agent (推理层)                        │
└─────────────────────────────┬───────────────────────────────┘
                              │ Tool Calls（唯一副作用出口）
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 L4: Execution (执行层)                       │
└─────────────────────────────────────────────────────────────┘
```

------

## 🔁 两条核心流（必须理解）

### ✅ 数据流（What flows）

```
User → Channel → Gateway → Agent → Execution → Channel → User
```

------

### 🧠 控制流（Who controls）

```
Gateway（主控）
   ↓
调度 Agent.run()
   ↓
Agent 决定 Tool Calls
   ↓
Execution 被动执行
   ↓
结果返回 Agent
```

------

## 🔥 **核心思想**

- **每层只做一件事**，通过明确的接口通信
- **层间隔离**：下层变化不影响上层
- **可插拔**：Channel 可扩展、Agent 可多实例、Execution 可切换模式

------

# 2️⃣ 三大核心抽象（比分层更重要）

------

## 2.1 Session（最小状态单元）

> 系统真正的核心不是 Agent，而是 Session

```
sessionKey =
agent:<agentId>:<channel>:<type>:<peerId>
```

### 特性：

- 独立上下文（history + memory）
- 串行执行（queue lane）
- 生命周期管理（创建 / 重置 / 归档）

------

## 2.2 Event（统一输入模型）

所有输入统一为事件：

```
InboundEvent        // 用户消息
SystemEvent         // cron / heartbeat
ToolResultEvent     // 工具返回
```

👉 Agent 不关心来源，只关心：

```
input = event
```

------

## 2.3 Tool Call（唯一副作用出口）

> Agent 本身是纯函数，Tool 才能改变世界

所有副作用：

- 发消息
- 写文件
- 调 API
- 浏览器操作
- Node 控制

全部通过：

```
tool_call → execution → result
```

------

# 3️⃣ 四层架构详解



**四层架构：从消息到执行的完整链路**

## 第一层：交互层——你从哪儿跟它说话

OpenClaw最神奇的地方，就是你可以用任何聊天软件指挥它。

你在WhatsApp上给它发消息，它在飞书里给你回；你在终端敲命令，它也能听懂；甚至你在Mac的菜单栏点一下，它都能弹出对话窗口。

这一层做的事其实很“翻译官”——每个渠道都有自己的脾气：WhatsApp要扫码配对，Telegram要填Bot Token，飞书有一套复杂的卡片消息格式。交互层的工作，就是把所有这些乱七八糟的接口，翻译成OpenClaw内部统一能听懂的语言。

用大白话理解：交互层就像酒店的前台，不管你从大门进、侧门进、还是从停车场直接坐电梯上来，前台都把你登记成“客人”，然后问一句：“您好，请问找谁？”

所以当你发现“在微信上给机器人发消息没反应”，第一步要查的就是这一层——是微信没收到消息？还是收到了但翻译的时候卡住了？看日志里有没有feishu-message或者telegram-event这样的关键词，有就说明翻译成功，问题出在后面。

## 第二层：网关层——整个系统的大脑

消息翻译完了，去哪儿？去网关（Gateway）。

网关是OpenClaw最核心的组件，没有之一。它是一个常驻后台的服务（类似你电脑上一直运行的杀毒软件），所有消息、所有指令、所有定时任务，都得经过它。

网关做三件事：

第一，路由。它看一眼消息是谁发的——哦，是张三在飞书私聊我——那这条消息应该交给“张三的专属会话”处理。如果是群消息，就交给对应的群会话。

第二，排队。OpenClaw有个很聪明的设计叫“车道式队列”（Lane Queue）。你同时发三条指令，网关不会让它们一起执行（那不乱套了），而是一条一条串行处理。如果你在A群里让它写文件，同时在B群里让它查天气，这两件事不冲突，可以并行——这就是“显式并行，默认串行”。

第三，调度定时任务。你配了一个每天早上8点发日报的Heartbeat，网关就记住这个事了。到点了，哪怕你人还在睡觉，网关也会准时唤醒系统去干活。

用大白话理解：网关是公司的总机接线员。电话（消息）打进来，他看一眼要找谁（路由），然后按顺序转接（排队）。他还记得老板交代的“每天下午三点开会提醒”，到点就主动打电话（定时任务）。

网关层出问题，症状通常是：消息发过去了，机器人“已读”了，但没反应。或者定时任务压根没触发。这时候去查openclaw gateway status和日志里的scheduler关键词。

## 第三层：智能体层——真正动脑子的地方

消息被网关送到这一层，才开始真正的“思考”。

智能体（Agent）这一层又拆成三个小角色，分工明确：

1. 会话管理器（Session Manager）每个对话都有一个独立的“会话”。你和AI的聊天记录、你之前让它记住的偏好、你这次发的文件，都存在这个会话里。不同的会话之间是隔离的——张三的私聊看不到李四的秘密，群聊里的AI也不会把群消息记到你的私人记忆里。
2. 上下文组装器（Context Assembler）每次你要跟AI对话，它得知道自己是谁、能干啥、你以前说过啥。这一块就是干这个活的：把SOUL.md（人格设定）、TOOLS.md（工具有哪些）、历史聊天记录、最近的记忆，拼成一份完整的“提示词”喂给大模型。
3. 执行循环（Execution Loop）这是AI真正“动脑子”的地方。大模型看完你的指令，决定要调用什么工具——比如你说“帮我截屏”，模型说“好的，我要调用screenshot工具”。执行循环就负责：去调用截屏工具 → 拿到截图 → 再问模型“截图拿到了，然后呢？” → 模型说“发给用户” → 执行循环把图发出去。
4. 记忆系统（Memory System）OpenClaw的记忆分三层：

短期记忆：每天的对话日志，按日期存成Markdown文件。新对话开始时，自动加载今天和昨天的日志，让你觉得AI“记得昨天的事”。
近端记忆：完整的会话存档。对话太长被压缩时，关键信息存到这里。
长期记忆：MEMORY.md文件，存你明确的偏好（“我以后都用深色模式”）、重要决策、项目状态。每次私聊都会自动加载。
记忆系统还有个很酷的机制：当你说了“记住这个”，AI会自己判断该记到长期记忆里，还是只留在这天的日志里。

用大白话理解：智能体层是坐在总机后面的那个真正的助理。总机把电话转给他，他先翻翻笔记本（记忆），看看你之前说过什么，然后听你现在要干啥，想清楚需要调用什么工具，再指挥别人去干。

这一层出问题，症状通常是：AI“答非所问”，或者明明有某个技能但它就是不用。可能是上下文组装时漏了关键信息，也可能是执行循环卡在工具调用上。看日志里agent关键词，能看出它每一步在想什么。

## 第四层：执行层——真正干活的“手脚”

动脑子的是智能体，但真要干活——写文件、发邮件、截屏、点鼠标——得靠这一层。

执行层分两块：

1. 本地节点（Local Node）和网关跑在同一台机器上，负责通用技能：执行命令行、读写文件、联网搜索、查天气。这些事不需要你个人设备的特殊权限，网关自己就能干。
2. 远端节点（Remote Node）跑在你其他设备上：卧室的MacBook、随身带的iPhone、办公室的Windows电脑。它们通过WebSocket长连接和网关通信。你出差时让AI帮你截家里电脑的屏，消息就得走：手机 → 网关（可能在云服务器） → 家里MacBook → 截图回来。
3. 技能系统（Skills）技能是OpenClaw最妙的设计——它不是一个写死的功能列表，而是一个个独立的插件。每个技能就是一个.md文件，里面告诉AI这个工具怎么用、有什么参数、有什么限制。AI读了这个“说明书”，自己就知道怎么调用。

比如apple-notes技能，安装后AI就能读写你的苹果备忘录；peekaboo技能让AI能看见并操控macOS桌面——截屏、找按钮、点鼠标。

技能市场叫ClawHub，里面有社区贡献的60+官方技能。你不需要写代码，只要clawhub install 技能名，AI就学会新本事了。

用大白话理解：执行层是助理手底下的那些跑腿小弟。助理动脑子想清楚了，就喊一声：“小李，去把这个文件存一下；小王，去截个屏。”这些小弟分散在不同地方（本地、家里、办公室），接到指令就干活，干完回来交差。

这一层出问题，症状很直接：AI说“我已经帮你保存了”，但文件没出现；或者AI说“正在截屏”，然后一直没下文。可能是远端节点掉线了（WebSocket断了），也可能是技能需要的依赖没装。openclaw logs里搜node或skill能看到具体报错。

一张图总结：消息的完整旅程
假设你现在在飞书给OpenClaw发了一条指令：“帮我截一下卧室那台Mac的屏幕，看看程序跑完了没。”

交互层：飞书适配器收到消息，翻译成内部格式，传给网关。
网关层：网关看消息来源，分配给“你的主会话”；同时检查有没有定时任务冲突，放进队列。
智能体层：会话管理器加载你的历史记录和记忆；上下文组装器拼好提示词；大模型看完，决定调用peekaboo技能；执行循环开始跑。
执行层：网关查询技能路由表，发现peekaboo需要远端节点执行，通过WebSocket把指令发给你卧室的MacBook；MacBook截屏、图片回传；原路返回——执行层→智能体层（可能再做一次总结）→网关层→交互层（飞书适配器发图片给你）。
全程可能只需要几十秒，但你啥也不用干。

写在最后
说实话，我刚开始用OpenClaw的时候，也觉得“管它怎么工作呢，能用就行”。但后来遇到几次诡异的问题——消息发了不回、定时任务不跑、AI死活不调用某个工具——才意识到：不懂架构，就只能瞎蒙。

但现在你知道了：出问题先想“是哪一层”。发消息没反应？看交互层有没有收到。收到了但没回？看网关层有没有转出去。AI说干了但没效果？看执行层有没有真干活。

这个思路，比任何具体的技术命令都有用。



------

# 🧩 L1：Channel（接入层）

## 职责

- **协议适配**：对接各聊天平台的 API/协议
- **消息标准化**：将平台特定格式转为 OpenClaw 内部事件格式
- **发送消息**：将 Agent 输出转为平台特定格式发送
- **媒体处理**：图片、音频、文件的上传下载
- **Mention 检测**：识别群组中的 @提及
- **连接管理**：保持长连接（WebSocket/polling）

------

## 核心作用

👉 **把“世界”翻译成统一格式**



## 内部事件格式

```typescript
interface InboundEvent {
  type: "message" | "presence" | "read_receipt" | ...;
  channel: "whatsapp" | "telegram" | "discord" | ...;
  accountId: string;        // 多账号支持
  peer: {
    kind: "direct" | "group" | "channel";
    id: string;             // E.164 / chat_id / guild+channel
    name?: string;          // 显示名称
  };
  message?: {
    text?: string;
    media?: Media[];
    quoted?: QuotedMessage; // 回复引用
    mentions?: string[];    // 提及列表
  };
  timestamp: number;
  metadata: Record<string, any>;
}
```

## 适配器实现

| 渠道     | 技术栈                             | 特点                               |
| -------- | ---------------------------------- | ---------------------------------- |
| WhatsApp | `@whiskeysockets/baileys`          | 需 QR 登录，支持群组               |
| Telegram | `grammY` + `node-telegram-bot-api` | Bot token，支持论坛主题            |
| Discord  | `discord.js`                       | OAuth2，支持 guild/channel         |
| iMessage | `imessage-tools` (macOS 节点)      | 需 macOS 节点配对                  |
| Slack    | `@slack/bolt`                      | Bot token，支持 workspace          |
| Signal   | `signal-cli` (Rest API)            | 需 paired device                   |
| Feishu   | `@larksuiteoapi/node-sdk`          | App 凭证认证，支持群聊/机器人/审批 |

## 配置示例

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        personal: { /* Baileys 配置 */ },
        work: { /* 另一个账号 */ },
      },
      dmPolicy: "pairing",      // DM 配对策略
      groups: { "*": { requireMention: true } }, // 群组 @ 要求
    },
    telegram: {
      accounts: {
        default: { botToken: "..." }
      },
    },
  },
}
```

------

# 🧠 L2：Gateway（系统中枢）

###  核心职责

Gateway 是 OpenClaw 的**大脑中枢**，负责：

1. **路由**（Router）：决定消息去哪个 Agent
2. **认证**（Auth）：保护 WebSocket API
3. **会话管理**（Session）：会话生命周期
4. **调度**（Scheduler）：Heartbeat + Cron
5. **策略执行**（Policy）：工具权限、DM/群组规则
6. **队列管理**（Queue）：串行化 Agent 执行
7. **插件系统**（Plugins）：扩展能力

### 关键子系统

####  Router（路由）

**输入**：`{channel, accountId, peer}`  
**输出**：`agentId`（可能多个，用于 broadcast）

**规则优先级**：

1. `broadcast` 匹配 → 多个 agent 并行/串行
2. `bindings` 匹配 → 单个 agent（第一条匹配）
3. 默认 agent（`default: true`）

**示例配置**：

```json5
{
  agents: {
    list: [
      { id: "personal", default: true },
      { id: "family" },
    ],
  },
  bindings: [
    {
      agentId: "personal",
      match: { channel: "whatsapp", accountId: "personal" },
    },
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "FAMILY_GROUP_ID" },
      },
    },
  ],
  broadcast: {
    "DEV_GROUP_ID@g.us": ["linter", "security", "docs"],
  },
}
```

---

#### Auth（认证）

**目标**：防止未授权访问 Gateway API

**模式**：

| 模式            | 配置                                                         | 适用场景        |
| --------------- | ------------------------------------------------------------ | --------------- |
| `token`         | `gateway.auth.token: "random-string"`                        | 本地/私有网络   |
| `password`      | `gateway.auth.password: "..."` 或 `OPENCLAW_GATEWAY_PASSWORD` | 本地/简单共享   |
| `trusted-proxy` | 信任反向代理的身份头                                         | 公网 + 反向代理 |

**默认行为**：
- 本地（`bind: "loopback"`）允许无 auth（但建议设置）
- 非本地绑定**必须**配置 auth，否则拒绝启动

**设备配对**（Device Pairing）：
- Control UI、CLI 需先"配对"（类似 OAuth）
- 配对请求通过 WebSocket 发送，需人工 approve
- 配对后使用 device token 认证

---

#### Session Manager（会话管理）

**会话标识符**（Session Key）格式：

```
agent:<agentId>:<channel>:<type>:<peerId>
```

**类型**：
- `direct` - 私聊
- `group` - 群组
- `channel` - 频道/房间
- `topic` - Telegram 主题（附加 `:topic:<threadId>`）
- `cron` - 定时任务
- `hook` - Webhook 触发

**隔离策略**（`session.dmScope`）：

| 策略                       | 行为                        | 适用               |
| -------------------------- | --------------------------- | ------------------ |
| `main`                     | 所有 DM → `agent:<id>:main` | 单用户，跨设备连续 |
| `per-peer`                 | 按发送者隔离                | 多用户，防止交叉   |
| `per-channel-peer`         | 按渠道+发送者               | 多账号场景         |
| `per-account-channel-peer` | 按账号+渠道+发送者          | 复杂多账号         |

**生命周期**：

```
创建：首次消息到达
  ↓
使用：对话进行中（updatedAt 更新）
  ↓
重置：/new, /reset, 定时清理, idle 超时
  ↓
归档：删除但保留文件（sessions.json 移除，文件移入 .deleted）
```

---

#### Scheduler（调度器）

**两个调度器**：

1. **Heartbeat Scheduler**：
   - 固定间隔（默认 30min）
   - 运行主会话的 Agent turn
   - 检查 `HEARTBEAT.md` 清单
   - 静默 OK 或发送告警

2. **Cron Scheduler**：
   - 基于时间表达式（cron/at/every）
   - 两种执行模式：
     - `main`：systemEvent 加入主队列（等待心跳）
     - `isolated`：创建立会 `cron:<jobId>`，立即运行
   - 支持交付：`announce`/`webhook`/`none`

**调度优先级**：
- 两者独立运行，使用不同 queue lane
- Heartbeat 使用 `main` lane
- Cron isolated 使用 `cron` lane
- 可并行（受 `maxConcurrent` 限制）

---

#### Command Queue（命令队列）

**目的**：防止同一会话并发运行，控制全局并发

**Lane 设计**：

```
Lane: session:<key>    // 同会话串行
Lane: main             // inbound + heartbeats + cron(main)
Lane: cron             // cron isolated 作业
Lane: subagent         // 子代理调用
```

**配置**：

```json5
{
  messages: {
    queue: {
      mode: "collect",      // collect/steer/followup
      debounceMs: 1000,     // 等待空闲
      cap: 20,              // 最大队列深度
      drop: "summarize",    // 溢出策略
    },
  },
  agents: {
    defaults: {
      maxConcurrent: 4,     // 全局最大并发数
    },
  },
}
```

---

### Gateway 配置示例

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    port: 18789,
    auth: { mode: "token", token: "random-32-char-token" },
  },

  session: {
    dmScope: "per-channel-peer", // 安全隔离
    reset: { mode: "daily", idleMinutes: 120 },
    maintenance: { mode: "enforce", pruneAfter: "30d" },
  },

  messages: {
    queue: { mode: "collect", debounceMs: 1000 },
  },

  agents: {
    defaults: {
      heartbeat: { every: "30m", target: "none" },
      maxConcurrent: 4,
    },
  },

  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
  },
}
```

------

# 🤖 L3：Agent（智能体层）

------

## 职责

- **LLM 推理**：调用模型生成回复
- **上下文组装**：system prompt + bootstrap + history + tools
- **记忆管理**：`memory_search` + 自动/手动写入
- **工具决策**：解析模型输出，调用工具，处理结果
- **工作区管理**：文件系统操作（受沙箱限制）

------

## 执行模型

```
Agent.run() = 单次推理循环
```

不是常驻进程 ❗

------

## 核心组件

### Model Runtime模型选择

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      fallbacks: ["sonnet-4-5", "gpt-5.4"],
      imageModel: { primary: "openai/dall-e-3" },
    },
  },
}
```



### 上下文组装

```
System Prompt
+ Bootstrap 文件
+ 历史消息
+ Memory
+ Tool schema
```



### Memory System

**三层架构**：

```
┌─────────────────────────────────────┐
│   Agent Tools (memory_search/get)   │
└──────────────┬──────────────────────┘
               │ 调用
┌──────────────▼──────────────────────┐
│     Search Backend (SQLite/QMD)     │
│  Vector + BM25 + Reranking          │
└──────────────┬──────────────────────┘
               │ 查询
┌──────────────▼──────────────────────┐
│    Storage (Markdown files)         │
│  MEMORY.md + memory/YYYY-MM-DD.md  │
└─────────────────────────────────────┘
```

**关键特性**：
- **显式写入**：Agent 必须主动调用 `write`/`edit`
- **语义搜索**：向量 + 关键词混合
- **高级排序**：MMR（多样性）+ Temporal decay（时间衰减）
- **本地优先**：QMD 后端完全离线运行

---

### Workspace（工作区）

**目录结构**：

```
<workspace>/
├── MEMORY.md              # 长期记忆（仅 DM 注入）
├── memory/
│   ├── 2026-03-20.md      # 今日日志
│   └── ...
├── AGENTS.md              # Agent 元描述
├── SOUL.md                # 性格/行为准则
├── TOOLS.md               # 本地工具配置
├── IDENTITY.md            # 身份信息
├── USER.md                # 用户信息
├── HEARTBEAT.md           # 心跳检查清单（可选）
├── skills/                # 技能目录
│   ├── weather/
│   └── ...
└── sessions/              # 会话存储（被子进程读写）
    ├── sessions.json
    └── <sessionId>.jsonl
```

**Bootstrap 注入**（启动时）：

默认注入（除非 `lightContext: true`）：
- `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`

**会话注入**：
- DM：当日 + 前一日 `memory/` 文件（自动）
- 群组：仅 `HEARTBEAT.md`（隐私保护）

---

### Tool Execution（工具调用）

**流程**：



```
1. LLM 输出: { tool_calls: [{ name: "web_search", arguments: {...} }] }
2. Agent 验证: 工具是否在 allowlist? 会话是否允许?
3. 转发到 Gateway → Execution 层
4. 执行完成，结果返回 Agent
5. Agent 注入结果到上下文，继续推理
```


**工具策略**（多层过滤）：

1. Tool profile (`tools.profile`)
2. Global deny (`tools.deny`)
3. Agent deny (`agents.list[].tools.deny`)
4. Sandbox policy (`tools.sandbox.tools`)

**deny 优先级高于 allow**。

---

## Agent 配置示例

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        default: true,
        name: "Personal Assistant",
        workspace: "~/.openclaw/workspace-personal",
        model: { primary: "anthropic/claude-opus-4-6" },
        sandbox: { mode: "off" }, // 无沙箱（完全信任）
        tools: {
          profile: "coding", // coding/messaging/minimal
        },
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        model: { primary: "anthropic/claude-sonnet-4-5" },
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "none", // 沙箱独立工作区
        },
        tools: {
          allow: ["read", "sessions_list", "sessions_send"],
          deny: ["exec", "write", "edit", "browser"],
        },
      },
    ],
  },
}
```



# ⚙️ L4：Execution（执行层）

------

## 职责

实际执行工具调用，提供**隔离**和**安全**边界。

## 执行模式

| 模式                 | 运行位置                | 隔离性 | 启用条件                         | 特点             |
| -------------------- | ----------------------- | ------ | -------------------------------- | ---------------- |
| **Host**             | Gateway 主机进程        | 无     | `tools.elevated` 或 sandbox off  | 无隔离（高权限） |
| **Sandbox (Docker)** | 容器                    | 高     | `agents.*.sandbox.mode != "off"` | 强隔离（推荐）   |
| **Node (远程)**      | 配对设备（iOS/Android） | 中     | 设备已配对 + 权限                | 远程设备         |
| **Browser**          | 本地 Chrome 或容器      | 中     | `browser` 工具被调用             | 自动化           |

------

### Host 执行

**适用**：个人代理，完全信任环境

**风险**：工具可直接访问主机文件系统、网络、进程

**保护措施**：
- `tools.elevated` 需要显式 allowlist 发送者
- `tools.fs.workspaceOnly` 限制路径（可选）
- 文件权限（`~/.openclaw` 700）

---

### Sandbox (Docker)

**Docker 容器配置**：

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "session", // session | agent | shared
        workspaceAccess: "none", // none | ro | rw

        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none", // 默认无网络
          user: "1000:1000",
          pidsLimit: 256,
          memory: "1g",
          cpu: 1,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl",
          binds: [ // 额外挂载
            "/data/shared:/data:ro"
          ],
        },

        prune: {
          idleHours: 24,   // 空闲 24h 删除容器
          maxAgeDays: 7,   // 最大年龄 7 天
        },

        browser: {
          enabled: false,
          autoStart: true,
          network: "openclaw-sandbox-browser", // 专用网络
          cdpSourceRange: ["172.21.0.1/32"], // CDP 源限制
        },
      },
    },
  },
}
```

**构建镜像**：

```bash
scripts/sandbox-setup.sh              # 基础镜像
scripts/sandbox-common-setup.sh       # 带常用工具
scripts/sandbox-browser-setup.sh      # 浏览器镜像
```

---

### Remote Node（远程设备）

**配对流程**：
1. 设备（iOS/Android）安装 OpenClaw App
2. 在 App 中启用 Node 模式，扫描配对码
3. Gateway 批准 pairing 请求
4. 设备作为远程执行节点

**可用能力**（需权限）：

- `nodes.camera` - 拍照
- `nodes.screen` - 录屏
- `nodes.system.run` - 执行命令
- `nodes.notification` - 发送通知
- `nodes.contacts` - 读取联系人
- `nodes.calendar` - 日历事件

**Node 权限模型**（设备端）：

```yaml
# 在 OpenClaw App 的 Exec Approvals 设置
security: "ask" | "allowlist" | "deny"
allowlist: ["system.run", "nodes.camera", ...]
```

---

### Browser Control

**两种模式**：

1. **本地 Chrome**（`profile: "user"`）
   - 使用用户已登录的 Chrome
   - 需人工 attach tab
   - 风险：继承用户登录状态

2. **容器 Chrome**（沙箱模式）
   - 独立 profile（`openclaw`）
   - 无持久化登录
   - 更安全，推荐

**SSRF 策略**：

```json5
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false, // 默认 true（信任模型）
      hostnameAllowlist: ["*.example.com"],
      allowedHostnames: ["localhost"], // 白名单
    },
  },
}
```



## 安全模型（三层防御）

```
Gateway → Policy
Agent   → allow/deny
Execution → sandbox
```

------





# 4️⃣ 完整执行时序（核心）

```
1. User 发送消息
2. Channel → InboundEvent
3. Gateway：
   - Auth
   - Router
   - Session
   - Enqueue

4. Queue 调度：
   → Agent.run()

5. Agent：
   - 推理
   - 决定 tool_call

6. Execution：
   - 执行工具
   - 返回结果

7. Agent：
   - 继续推理
   - 生成回复

8. Channel：
   - 发送消息
```

------



场景：用户查询咖啡偏好为例

```
┌─────────────────────────────────────────────────────────────┐
│  用户 (WhatsApp)                                            │
│  "我的咖啡偏好是什么？"                                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L1: Channel (WhatsApp 适配器)                              │
│  - 接收消息                                                   │
│  - 标准化: {channel:"whatsapp", peer:+1555..., text:"..."} │
└─────────────────────────────┬───────────────────────────────┘
                              │ WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L2: Gateway                                                │
│  1. Auth: token 验证通过                                     │
│  2. Router: bindings 匹配 → agentId = "personal"           │
│  3. Session: sessionKey = "agent:personal:whatsapp:direct:+1555..." │
│  4. Queue: enqueue (lane: session:personal:whatsapp:direct) │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L3: Agent (personal)                                       │
│  1. 上下文组装:                                              │
│     - System prompt (工具列表)                              │
│     - Bootstrap (AGENTS.md, SOUL.md, ...)                   │
│     - History (最近 20 条消息)                              │
│  2. LLM 推理:                                               │
│     用户问咖啡 → 决定调用 memory_search                     │
│  3. 工具调用: memory_search({query:"咖啡"})                │
└─────────────────────────────┬───────────────────────────────┘
                              │ 工具调用
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L4: Execution (Host 或 Sandbox)                            │
│  - 验证: memory_search 在 allowlist                         │
│  - 执行: 查询记忆索引 (SQLite/QMD)                          │
│  - 返回: {text:"咖啡: 黑咖啡, 过敏: 花生", score:0.92}     │
└─────────────────────────────┬───────────────────────────────┘
                              │ 工具结果
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L3: Agent (继续)                                           │
│  - 接收工具结果，注入上下文                                 │
│  - 继续推理 → 生成回复                                      │
│  - 调用 message 工具发送                                    │
└─────────────────────────────┬───────────────────────────────┘
                              │ 发送请求
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L4: Execution (发送)                                       │
│  - message 工具 → Channel 适配器 → WhatsApp API            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  L1: Channel (WhatsApp)                                     │
│  - 发送消息到用户                                            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  用户 (WhatsApp)                                            │
│  "根据记忆，您喜欢黑咖啡，对花生过敏。"                      │
└─────────────────────────────────────────────────────────────┘
```

# 5️⃣ 系统本质模型

------

## 🧠 抽象表达

```
System =
Event-driven
+ Tool-augmented
+ Session-isolated
+ Gateway-orchestrated
```

------

## 🔁 更底层表达

```
for event in system:
    session = resolve(event)
    enqueue(session)

worker:
    while queue:
        run_agent(session)
```

------

# 6️⃣ 设计原则（架构哲学）

------

##  单一职责

每层只做一件事

## 控制反转

- Agent 不执行
- Execution 不决策
- Gateway 控制一切

------

## 状态隔离

```
state ∈ session
```

------

## 副作用集中

```
side effects → tools only
```

## 配置外置

行为由配置驱动，无需修改代码即可调整策略。

## 安全性纵深

- Gateway: auth + dmPolicy + groupPolicy
- Agent: tools.allow/deny + sandbox
- Execution: Docker isolation + SSRF policy

------

# 7️⃣ 五大常见误区（极重要）

------

## ❌ 误区 1：Agent 是长期运行的

✔️ 实际：

```
Agent = 短生命周期函数
```

------

## ❌ 误区 2：Memory 自动写入

✔️ 实际：

```
必须 tool 调用 write
```

------

## ❌ 误区 3：Cron 直接执行 Agent

✔️ 实际：

```
cron → event → queue → agent
```

------

## ❌ 误区 4：Sandbox 就是安全

✔️ 实际：

```
安全 = Gateway + Agent + Execution
```

------

## ❌ 误区 5：并发是 Agent 级

✔️ 实际：

```
并发 = session 级
```

------

# 8️⃣ 部署拓扑

------

## 🧑‍💻单机部署（个人）

```
┌─────────────────────────────────────────────┐
│   Mac mini (Gateway + Agent 全在 host)      │
│  - Gateway: 18789 (localhost)               │
│  - Agent: personal (sandbox: off)           │
│  - Channels: WhatsApp (个人号)              │
└─────────────────────────────────────────────┘
```

---

### 容器化部署（团队）

```
┌────────────────────────────────────────────────────┐
│   VPS (Docker)                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ Gateway 容器 (openclaw:latest)              │ │
│  │  - port 18789 (Tailscale Funnel)            │ │
│  │  - agents: personal, family, public         │ │
│  └──────────────────────────────────────────────┘ │
│                                                      │
│  ┌──────────────────────────────────────────────┐ │
│  │ Sandbox 容器 (按需创建)                       │ │
│  │  - family (agent 级沙箱)                     │ │
│  │  - public (session 级沙箱)                   │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
                              │
                              ▼
                    iOS/Android 设备（Node 配对）
```

---



------

# 9️⃣ 一句话终极理解

------

> OpenClaw 不是聊天机器人框架
> 而是一个：

```
类操作系统的 Agent 执行平台
```

