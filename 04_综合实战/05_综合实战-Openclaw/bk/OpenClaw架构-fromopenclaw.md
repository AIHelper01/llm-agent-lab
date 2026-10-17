# OpenClaw 四层架构详解

> 理解系统的分层设计、职责边界和数据流

---

## 一、架构总览

OpenClaw 采用**四层架构**，实现清晰的分层解耦：

```
┌─────────────────────────────────────────────────────────────┐
│                    L1: Channel (接入层)                      │
│   WhatsApp  Telegram  Discord  iMessage  Slack  ...         │
└─────────────────────────────┬───────────────────────────────┘
                              │ 标准化事件
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   L2: Gateway (网关层)                       │
│  路由 · 认证 · 会话 · 调度 · 策略 · 队列                     │
└─────────────────────────────┬───────────────────────────────┘
                              │ agentId + sessionKey
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    L3: Agent (智能体层)                      │
│  LLM 推理 · 记忆检索 · 工具决策 · 工作区管理                 │
└─────────────────────────────┬───────────────────────────────┘
                              │ 工具调用
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 L4: Execution (执行层)                       │
│  沙箱 Docker · 主机命令 · 浏览器控制 · 远程 Nodes           │
└─────────────────────────────────────────────────────────────┘
```

**核心思想**：
- **每层只做一件事**，通过明确的接口通信
- **层间隔离**：下层变化不影响上层
- **可插拔**：Channel 可扩展、Agent 可多实例、Execution 可切换模式

---

## 二、第一层：Channel（接入层）

### 2.1 职责

- **协议适配**：对接各聊天平台的 API/协议
- **消息标准化**：将平台特定格式转为 OpenClaw 内部事件格式
- **发送消息**：将 Agent 输出转为平台特定格式发送
- **媒体处理**：图片、音频、文件的上传下载
- **Mention 检测**：识别群组中的 @提及
- **连接管理**：保持长连接（WebSocket/polling）

### 2.2 内部事件格式

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

### 2.3 适配器实现

| 渠道     | 技术栈                             | 特点                               |
| -------- | ---------------------------------- | ---------------------------------- |
| WhatsApp | `@whiskeysockets/baileys`          | 需 QR 登录，支持群组               |
| Telegram | `grammY` + `node-telegram-bot-api` | Bot token，支持论坛主题            |
| Discord  | `discord.js`                       | OAuth2，支持 guild/channel         |
| iMessage | `imessage-tools` (macOS 节点)      | 需 macOS 节点配对                  |
| Slack    | `@slack/bolt`                      | Bot token，支持 workspace          |
| Signal   | `signal-cli` (Rest API)            | 需 paired device                   |
| Feishu   | `@larksuiteoapi/node-sdk`          | App 凭证认证，支持群聊/机器人/审批 |

### 2.4 配置示例

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

---

## 三、第二层：Gateway（网关层）

### 3.1 核心职责

Gateway 是 OpenClaw 的**大脑中枢**，负责：

1. **路由**（Router）：决定消息去哪个 Agent
2. **认证**（Auth）：保护 WebSocket API
3. **会话管理**（Session）：会话生命周期
4. **调度**（Scheduler）：Heartbeat + Cron
5. **策略执行**（Policy）：工具权限、DM/群组规则
6. **队列管理**（Queue）：串行化 Agent 执行
7. **插件系统**（Plugins）：扩展能力

### 3.2 关键子系统

#### 3.2.1 Router（路由）

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

#### 3.2.2 Auth（认证）

**目标**：防止未授权访问 Gateway API

**模式**：

| 模式 | 配置 | 适用场景 |
|------|------|----------|
| `token` | `gateway.auth.token: "random-string"` | 本地/私有网络 |
| `password` | `gateway.auth.password: "..."` 或 `OPENCLAW_GATEWAY_PASSWORD` | 本地/简单共享 |
| `trusted-proxy` | 信任反向代理的身份头 | 公网 + 反向代理 |

**默认行为**：
- 本地（`bind: "loopback"`）允许无 auth（但建议设置）
- 非本地绑定**必须**配置 auth，否则拒绝启动

**设备配对**（Device Pairing）：
- Control UI、CLI 需先"配对"（类似 OAuth）
- 配对请求通过 WebSocket 发送，需人工 approve
- 配对后使用 device token 认证

---

#### 3.2.3 Session Manager（会话管理）

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

| 策略 | 行为 | 适用 |
|------|------|------|
| `main` | 所有 DM → `agent:<id>:main` | 单用户，跨设备连续 |
| `per-peer` | 按发送者隔离 | 多用户，防止交叉 |
| `per-channel-peer` | 按渠道+发送者 | 多账号场景 |
| `per-account-channel-peer` | 按账号+渠道+发送者 | 复杂多账号 |

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

#### 3.2.4 Scheduler（调度器）

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

#### 3.2.5 Command Queue（命令队列）

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

### 3.3 Gateway 配置示例

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

---

## 四、第三层：Agent（智能体层）

### 4.1 职责

- **LLM 推理**：调用模型生成回复
- **上下文组装**：system prompt + bootstrap + history + tools
- **记忆管理**：`memory_search` + 自动/手动写入
- **工具决策**：解析模型输出，调用工具，处理结果
- **工作区管理**：文件系统操作（受沙箱限制）

### 4.2 核心组件

#### 4.2.1 Model Runtime

**模型选择**：

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

**上下文窗口管理**：
- 自动裁剪旧工具结果（pruning）
- 自动压缩早期消息（compaction）
- 预留 tokens（`reserveTokens`）

---

#### 4.2.2 Memory System

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

#### 4.2.3 Workspace（工作区）

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

#### 4.2.4 Tool Execution（工具调用）

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

### 4.3 Agent 配置示例

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

---

## 五、第四层：Execution（执行层）

### 5.1 职责

实际执行工具调用，提供**隔离**和**安全**边界。

### 5.2 执行模式

| 模式 | 运行位置 | 隔离性 | 启用条件 |
|------|----------|--------|----------|
| **Host** | Gateway 主机进程 | 无 | `tools.elevated` 或 sandbox off |
| **Sandbox (Docker)** | 容器 | 高 | `agents.*.sandbox.mode != "off"` |
| **Node (远程)** | 配对设备（iOS/Android） | 中 | 设备已配对 + 权限 |
| **Browser** | 本地 Chrome 或容器 | 中 | `browser` 工具被调用 |

---

#### 5.2.1 Host 执行

**适用**：个人代理，完全信任环境

**风险**：工具可直接访问主机文件系统、网络、进程

**保护措施**：
- `tools.elevated` 需要显式 allowlist 发送者
- `tools.fs.workspaceOnly` 限制路径（可选）
- 文件权限（`~/.openclaw` 700）

---

#### 5.2.2 Sandbox (Docker)

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

#### 5.2.3 Remote Node（远程设备）

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

#### 5.2.4 Browser Control

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

---

## 六、完整数据流示例

### 场景：用户查询咖啡偏好

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

---

## 七、层间接口总结

### L1 ↔ L2

**接口**: WebSocket + REST (HTTP)

**L1 → L2**: 规范化事件（JSON）
**L2 → L1**: 发送指令（`{channel, to, content}`）

---

### L2 ↔ L3

**接口**: Embedded Agent Runtime（`runEmbeddedPiAgent`）

**L2 → L3**:
```typescript
{
  agentId: string;
  sessionKey: string;
  message: string;          // 用户消息或系统事件
  tools: ToolCall[],        // 继续工具调用（如果中断）
  context: ContextAssembler  // 上下文配置
}
```

**L3 → L2**: 工具调用请求（WebSocket RPC 或 direct function call）

---

### L3 ↔ L4

**接口**: Tool Invocation（工具调用协议）

**L3 → L4**:
```json
{
  "tool": "exec",
  "params": { "command": "ls -la", "timeout": 30000 }
}
```

**L4 → L3**: 工具结果（JSON）
```json
{
  "success": true,
  "output": "total 0\n...",
  "error": null
}
```

---

## 八、关键设计原则

### 1. 单一职责

每层只做一件明确的事，避免交叉耦合。

### 2. 接口隔离

层间通过明确定义的接口通信，内部实现可替换。

### 3. 依赖方向

依赖始终向内（上层依赖下层抽象，而非相反）。

### 4. 配置外置

行为由配置驱动，无需修改代码即可调整策略。

### 5. 安全性纵深

- Gateway: auth + dmPolicy + groupPolicy
- Agent: tools.allow/deny + sandbox
- Execution: Docker isolation + SSRF policy

---

## 九、典型部署拓扑

### 单机部署（个人）

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

