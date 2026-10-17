 

---

# 🦞 OpenClaw（小龙虾）安装指南

> **OpenClaw** 是一款本地优先（Local-First）的 AI 智能体操作系统，它将"响应式聊天机器人"转变为"行动式智能体"，支持通过 WhatsApp、Telegram、飞书等多种渠道与你交互 。

---

## 一、部署前准备

### 1.1 系统要求 

| 项目         | 要求                                                  | 说明                                           |
| ------------ | ----------------------------------------------------- | ---------------------------------------------- |
| **操作系统** | Windows 11 / macOS 12+ / Linux (Ubuntu/Debian/CentOS) | 推荐 Ubuntu 22.04 LTS 长期支持版               |
| **Node.js**  | 版本 **22.x 或 24.x**（强烈推荐 24.x）                | 22.x 是 OpenClaw 的最低要求版本，24.x 性能更优 |
| **内存**     | 至少 2GB（建议 8GB 以上）                             | 运行多个 Skills 或浏览器自动化时需要更多内存   |
| **磁盘空间** | 预留 2.5GB 以上                                       | 包含依赖缓存和日志空间                         |
| **网络**     | 可访问外网（用于下载依赖）                            | 国内用户建议配置镜像加速                       |

### 1.2 本次环境

| 项目         | 当前配置                             | 状态   | 说明                                      |
| ------------ | ------------------------------------ | ------ | ----------------------------------------- |
| **操作系统** | Ubuntu 22.04.5 LTS (Jammy Jellyfish) | ✅ 满足 | Linux 6.8.0-90-generic (x64)              |
| **Node.js**  | v22.22.0                             | ✅ 满足 | 通过 NodeSource 官方源安装，符合最低要求  |
| **内存**     | 使用率 19.4%                         | ✅ 充足 | 系统运行平稳，建议 ≥8GB 以运行更多 Skills |
| **磁盘空间** | 234G 总容量 / 61G 已用 (28%)         | ✅ 充足 | 剩余 162G 可用空间，完全满足需求          |
| **网络**     | 可访问外网                           | ✅ 正常 | 飞书消息推送成功，依赖下载正常            |

### 1.3 环境检查

```bash
node -v    # 检查 Node.js 版本，应显示 v22.x.x 或 v24.x.x
npm -v     # 检查 npm 版本，应显示 10.x.x 以上
```

### 1.4 未安装时的处理

如果系统提示找不到命令：

```
(base) root@will-Ubuntu:~# node -v
找不到命令 “node”，但可以通过以下软件包安装它：
apt install nodejs
(base) root@will-Ubuntu:~# npm -v
找不到命令 “npm”，但可以通过以下软件包安装它：
apt install npm
(base) root@will-Ubuntu:~#
```

**⚠️ 注意**：`apt install nodejs` 默认安装的是较旧版本（可能为 Node.js 12.x），**不满足 OpenClaw 要求**。请使用 NodeSource 官方仓库安装：

```bash
# 更新系统
apt update

# 安装必要的工具
apt install -y curl

# 添加NodeSource仓库（以Node.js 18.x为例）
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

# 安装Node.js（npm会自动安装）
apt install -y nodejs

# 验证安装
node -v
npm -v
```

> **💡 知识点：NodeSource vs 系统仓库**
>
> - **NodeSource**：提供最新的 Node.js 版本，与官方发布同步，推荐用于生产环境
> - **系统仓库（apt）**：版本滞后，仅适合对版本要求不高的场景

---

## 二、安装方式

### 2.1 npm 全局安装（⭐ 推荐）

```bash
# 配置国内镜像（可选，加速下载）
npm config set registry https://registry.npmmirror.com

# 全局安装 OpenClaw
npm install -g openclaw@latest
```

**Ubuntu 安装示例输出：**

```
(base) root@will-Ubuntu:~# npm config set registry https://registry.npmmirror.com
(base) root@will-Ubuntu:~# npm install -g openclaw@latest
npm warn deprecated node-domexception@1.0.0: Use your platform's native DOMException instead

added 1 package, and changed 458 packages in 53s

84 packages are looking for funding
  run `npm fund` for details
(base) root@will-Ubuntu:~# openclaw --version
OpenClaw 2026.3.24 (cff6dc9)
```

> **💡 知识点：npm 全局安装路径**
>
> 全局安装的包会被放入系统的 `PATH` 目录，允许你在任何地方直接运行 `openclaw` 命令。安装路径通常为：
> - Linux/macOS: `/usr/local/bin/` 或 `~/.npm-global/bin/`
> - Windows: `%APPDATA%\npm\`

### 2.2 其他安装方式

| 方式                 | 适用场景        | 特点                           |
| -------------------- | --------------- | ------------------------------ |
| **官方一键安装脚本** | 快速体验        | 自动处理依赖，适合新手         |
| **Docker 部署**      | 云服务器/VPS    | 环境隔离，易于迁移和扩展       |
| **源码编译**         | 开发者/高级用户 | 可自定义修改，需安装构建工具链 |

### 2.3 升级与卸载

```bash
# 升级到新版本
npm i -g openclaw@latest

# 卸载（使用内置卸载程序，会清理配置和日志）
openclaw uninstall
```

---

# 🦞 OpenClaw（小龙虾）调试指南

## Channel 准备（以飞书为例）

> **参考官网**：https://docs.openclaw.ai/channels/feishu

### 什么是 Gateway 和 Channel？

> **💡 核心架构知识** 
>
> **Gateway（网关）** 是 OpenClaw 的心脏，作为**长期运行的守护进程**存在：
> - **统一入口**：所有消息渠道（飞书、微信、Telegram 等）都通过 Gateway 接入
> - **协议收敛**：将不同平台的异构消息格式转换为 OpenClaw 内部标准
> - **会话管理**：通过 `SessionKey` 隔离不同用户/群组的上下文，确保数据安全
> - **消息路由**：判断消息该路由到哪个 Agent 处理
>
> **Channel（渠道）** 是 Gateway 的插件，负责与具体平台通信。OpenClaw 支持 20+ 种消息平台 。

**支持的消息平台清单：**

- BlueBubbles | Discord | **飞书** | grammY | Google Chat | iMessage | LINE | Matrix | Mattermost | Microsoft Teams | Nextcloud Talk | Nostr | Signal | Slack | Telegram | Tlon | Twitch | WhatsApp | Zalo | Zalo Personal

---

## 初始化配置

### 启动配置向导

```bash
openclaw onboard --install-daemon
```

> **💡 知识点：`--install-daemon` 参数**
>
> 该参数会在配置完成后自动安装系统服务，使 Gateway 能够：
> - 随系统启动自动运行
> - 后台常驻不依赖终端会话
> - 支持 `systemctl` 命令管理（Linux）

### 配置步骤总览

- 步骤 1：初始化与安全确认

- 步骤 2：模型配置

- 步骤 3：消息通道配置（飞书）

- 步骤 4：工具与技能配置

- 步骤 5：自动化钩子（Hooks）

- 步骤 6：服务部署

- 步骤 7：首次启动（TUI 界面）


---

## 初始化配置详解

### 启动配置向导

```bash
openclaw onboard --install-daemon
```

> **💡 知识点：`--install-daemon` 参数详解**
>
> 该参数会在配置完成后自动安装 **systemd 用户级服务**，使 Gateway 能够：
> - **随系统启动自动运行**：无需手动启动，开机即服务
> - **后台常驻**：不依赖终端会话，关闭 SSH 后服务继续运行
> - **崩溃自恢复**：systemd 会自动重启异常退出的进程
> - **日志管理**：通过 `journalctl` 统一查看日志
>
> 服务文件位置：`~/.config/systemd/user/openclaw-gateway.service`

---

### 配置流程逐步解析

#### 步骤 1：安全警告确认

```
◇  Security ─────────────────────────────────────────────────────────────────────────────────╮
│  Security warning — please read.                                                           │
│                                                                                            │
│  OpenClaw is a hobby project and still in beta. Expect sharp edges.                        │
│  By default, OpenClaw is a personal agent: one trusted operator boundary.                  │
│  This bot can read files and run actions if tools are enabled.                             │
│  A bad prompt can trick it into doing unsafe things.                                       │
│                                                                                            │
│  OpenClaw is not a hostile multi-tenant boundary by default.                               │
│  If multiple users can message one tool-enabled agent, they share that delegated tool      │
│  authority.                                                                                │
│                                                                                            │
│  If you're not comfortable with security hardening and access control, don't run            │
│  OpenClaw.                                                                                 │
│  Ask someone experienced to help before enabling tools or exposing it to the internet.     │
```

> **💡 知识点：OpenClaw 的安全边界模型** 
>
> OpenClaw 默认采用**"个人代理"（Personal Agent）**安全模型：
>
> | 场景           | 安全边界                 | 风险等级 |
> | -------------- | ------------------------ | -------- |
> | **个人使用**   | 单操作员边界，完全信任   | 🟢 低     |
> | **多用户共享** | 共享工具权限，需额外加固 | 🔴 高     |
>
> **关键安全措施：**
> - **配对机制（Pairing）**：未知发送者需通过配对码验证，防止未授权访问
> - **提及门控（Mention Gating）**：群聊中需 @提及才响应，避免误触发
> - **DM 隔离（DM Scope）**：多用户场景下隔离会话上下文
> - **沙箱运行**：敏感操作可在 Docker 容器中执行
>
> **推荐基线配置：**
> ```bash
> # 启用配对验证
> openclaw config set channels.pairing.required true
> 
> # 多用户场景隔离会话
> openclaw config set session.dmScope "per-channel-peer"
> 
> # 定期安全审计
> openclaw security audit --deep
> openclaw security audit --fix
> ```

---

#### 步骤 2：QuickStart 模式配置

```
◇  QuickStart ─────────────────────────╮
│                                      │
│  Gateway port: 18789                 │
│  Gateway bind: Loopback (127.0.0.1)  │
│  Gateway auth: Token (default)       │
│  Tailscale exposure: Off             │
│  Direct to chat channels.            │
│                                      │
├──────────────────────────────────────╯
```

> **💡 知识点：Gateway 网络配置详解**
>
> | 配置项        | 默认值      | 说明                            |
> | ------------- | ----------- | ------------------------------- |
> | **Port**      | `18789`     | Gateway HTTP/WebSocket 服务端口 |
> | **Bind**      | `127.0.0.1` | 仅本地回环访问，最安全          |
> | **Auth**      | `Token`     | 基于令牌的身份验证              |
> | **Tailscale** | `Off`       | 可选的 VPN 组网方案             |
>
> **网络暴露模式对比：**
>
> | 模式          | 配置                   | 适用场景                   | 安全等级 |
> | ------------- | ---------------------- | -------------------------- | -------- |
> | **Loopback**  | `bind: "127.0.0.1"`    | 本机/SSH 隧道访问          | 🟢 最高   |
> | **LAN**       | `bind: "lan"`          | 局域网内多设备             | 🟡 中     |
> | **Tailscale** | `tailscale.mode: "on"` | 跨网络组网                 | 🟡 中     |
> | **Public**    | `bind: "0.0.0.0"`      | 公网访问（需配合反向代理） | 🔴 低     |

---

#### 步骤 3：模型提供商配置（Kimi Code）

```
◇  Model/auth provider
│  Kimi Code
│
◇  Kimi ───────────────────────────────────────────────╮
│                                                      │
│  Kimi uses a dedicated coding endpoint and API key.  │
│  Get your API key at: https://www.kimi.com/code/en   │
│                                                      │
├──────────────────────────────────────────────────────╯
│
◇  Enter Kimi API key
│  YOUR_API_KEY
│
◇  Model configured ────────────────────╮
│                                       │
│  Default model set to kimi/kimi-code  │
│                                       │
├───────────────────────────────────────╯
```

> **💡 知识点：OpenClaw 的模型路由系统**
>
> OpenClaw 支持**多模型提供商**和**动态路由**：
>
> **模型标识格式**：`<提供商>/<模型名>`
> - `kimi/kimi-code`：月之暗面编程专用模型
> - `openai/gpt-4o`：OpenAI GPT-4o
> - `anthropic/claude-3-5-sonnet`：Claude 3.5 Sonnet
>
> **Kimi Code 特点：**
> 
> - 针对编程任务优化的专用端点
> - 支持长上下文（最高 200k tokens）
> - 代码生成和调试能力更强

---

#### 步骤 4：飞书（Feishu）渠道配置

```
◇  Feishu credentials ──────────────────────────────────────────────────────────────╮
│                                                                                   │
│  1) Go to Feishu Open Platform (open.feishu.cn)                                   │
│  2) Create a self-built app                                                       │
│  3) Get App ID and App Secret from Credentials page                               │
│  4) Enable required permissions: im:message, im:chat, contact:user.base:readonly  │
│  5) Publish the app or add it to a test group                                     │
│  Tip: you can also set FEISHU_APP_ID / FEISHU_APP_SECRET env vars.                │
│  Docs: feishu                 │

│                                                                                   │
├───────────────────────────────────────────────────────────────────────────────────╯
│
◇  Feishu connection test ───────────────────────────╮
│                                                    │
│  Connected as ou_daccb8641badba06f98f3b36c3d652bc  │
│                                                    │
├────────────────────────────────────────────────────╯
│
◇  Feishu connection mode
│  WebSocket (default)
│
◇  Which Feishu domain?
│  Feishu (feishu.cn) - China
│
◇  Group chat policy
│  Open - respond in all groups (requires mention)
```

> **💡 知识点：飞书开放平台配置详解**
>
> **应用类型选择：**
> - **自建应用（Self-built App）**：企业/个人开发者使用，需配置服务器
> - **商店应用（Marketplace App）**：公开发布，用户直接安装
>
> **关键权限说明：**
>
> | 权限                         | 作用             | 必要性           |
> | ---------------------------- | ---------------- | ---------------- |
> | `im:message`                 | 发送和接收消息   | ⭐ 必需           |
> | `im:chat`                    | 获取群聊信息     | ⭐ 必需           |
> | `contact:user.base:readonly` | 读取用户基本信息 | ⭐ 推荐           |
> | `drive:file:read`            | 读取云文档       | 可选（文档技能） |
> | `bitable:record`             | 操作多维表格     | 可选（表格技能） |
>
> **连接模式对比：**
>
> | 模式          | 原理           | 适用场景       | 要求                  |
> | ------------- | -------------- | -------------- | --------------------- |
> | **WebSocket** | 长连接实时推送 | 内网/有公网 IP | 服务器可被飞书访问    |
> | **Webhook**   | HTTP 回调      | 有公网域名     | 需配置 HTTPS 回调地址 |
>
> **域名选择：**
> - `feishu.cn`：中国版飞书（默认）
> - `open.feishu.cn`：国际版飞书（Lark）
>
> **群聊策略：**
> - **Open**：在所有群聊中响应（需 @提及）
> - **Closed**：仅在白名单群聊中响应

---

#### 步骤 5：Web 搜索与 Skills 配置

```
◇  Web search ─────────────────────────────────────────────────────────────────╮
│                                                                              │
│  Web search lets your agent look things up online.                           │
│  Choose a provider. Some providers need an API key, and some work key-free.  │
│  Docs: https://docs.openclaw.ai/tools/web                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────╯
│
◇  Search provider
│  Tavily Search
│
◇  Tavily API key
│  [留空，后续配置]
│
◇  Web search ─────────────────────────────────────────────────────────────────╮
│                                                                              │
│  No Tavily API key stored — web_search won't work until a key is available.  │
│  Get your key at: https://tavily.com/                                        │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────╯
```

> **💡 知识点：OpenClaw 的工具（Tools）系统**
>
> **Web 搜索提供商对比：**
>
> | 提供商         | 特点                    | 是否需要 API Key | 适用场景       |
> | -------------- | ----------------------- | ---------------- | -------------- |
> | **Tavily**     | AI 优化搜索，结果结构化 | ✅ 需要           | 研究、信息收集 |
> | **DuckDuckGo** | 隐私优先，无需注册      | ❌ 免费           | 快速查询       |
> | **Brave**      | 注重隐私，速度较快      | 可选             | 替代方案       |
> | **SearXNG**    | 自托管，聚合多引擎      | 自托管           | 隐私敏感场景   |
>
> **Skills 系统说明：**
>
> ```
> ◇  Skills status ─────────────╮
> │                             │
> │  Eligible: 5                │
> │  Missing requirements: 38   │
> │  Unsupported on this OS: 7  │
> │  Blocked by allowlist: 0    │
> │                             │
> ├─────────────────────────────╯
> ```
>
> - **Eligible**：当前环境可安装的 Skills
> - **Missing requirements**：缺少依赖（如 Homebrew、特定库）
> - **Unsupported on this OS**：当前操作系统不支持
> - **Blocked by allowlist**：被安全策略阻止
>
> **Skill 安装失败示例：**
> ```
> ◇  Install failed: summarize — brew not installed — Homebrew is not installed.
> ```
>
> > **💡 知识点：Homebrew 与 Linux**
> >
> > Homebrew 是 macOS 的包管理器，**Linux 上并非必需**。Ubuntu 用户可以通过 `apt` 安装相同功能的工具，或手动编译安装 Skills 依赖。

---

#### 步骤 6：Hooks（自动化钩子）配置

```
◇  Hooks ──────────────────────────────────────────────────────────────────╮
│                                                                          │
│  Hooks let you automate actions when agent commands are issued.          │
│  Example: Save session context to memory when you issue /new or /reset.  │
│                                                                          │
│  Learn more: https://docs.openclaw.ai/automation/hooks                   │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────╯
│
◇  Enable hooks?
│  🚀 boot-md, 📎 bootstrap-extra-files, 📝 command-logger, 💾 session-memory
│
◇  Hooks Configured ────────────────────────────────────────────────────────────────╮
│                                                                                   │
│  Enabled 4 hooks: boot-md, bootstrap-extra-files, command-logger, session-memory  │
│                                                                                   │
│  You can manage hooks later with:                                                 │
│    openclaw hooks list                                                            │
│    openclaw hooks enable <name>                                                   │
│    openclaw hooks disable <name>                                                  │
│                                                                                   │
├───────────────────────────────────────────────────────────────────────────────────╯
```

> **💡 知识点：Hooks 事件系统详解**
>
> Hooks 是 OpenClaw 的**事件驱动自动化机制**，在特定生命周期节点触发动作：
>
> | Hook 名称                 | 触发时机     | 功能说明                                |
> | ------------------------- | ------------ | --------------------------------------- |
> | **boot-md**               | Agent 启动时 | 加载 Markdown 格式的系统提示（SOUL.md） |
> | **bootstrap-extra-files** | 初始化时     | 加载额外的配置文件和模板                |
> | **command-logger**        | 执行命令时   | 记录所有命令执行历史，便于审计和回溯    |
> | **session-memory**        | 会话结束时   | 将会话上下文持久化到长期记忆            |
>
> **Hooks 管理命令：**
> ```bash
> openclaw hooks list              # 列出所有可用 Hooks
> openclaw hooks enable <name>     # 启用指定 Hook
> openclaw hooks disable <name>    # 禁用指定 Hook
> openclaw hooks config <name>     # 配置 Hook 参数
> ```

---

#### 步骤 7：服务部署与 TUI 启动

```
◇  Gateway service runtime ────────────────────────────────────────────╮
│                                                                      │
│  QuickStart uses Node for the Gateway service (stable + supported).  │
│                                                                      │
├──────────────────────────────────────────────────────────────────────╯
│
◑  Installing Gateway service…
Installed systemd service: /root/.config/systemd/user/openclaw-gateway.service
◇  Gateway service installed.
│
◇  Control UI ─────────────────────────────────────────────────────────────────────╮
│                                                                                  │
│  Web UI: http://127.0.0.1:18789/                                                 │
│  Web UI (with token):                                                            │
│  http://127.0.0.1:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f  │
│  Gateway WS: ws://127.0.0.1:18789                                                │
│  Gateway: reachable                                                              │
│                                                                                  │
├──────────────────────────────────────────────────────────────────────────────────╯
│
◇  Start TUI (best option!) ─────────────────────────────────╮
│                                                            │
│  This is the defining action that makes your agent you.    │
│  Please take your time.                                    │
│  The more you tell it, the better the experience will be.  │
│  We will send: "Wake up, my friend!"                       │
│                                                            │
├────────────────────────────────────────────────────────────╯
│
◇  Token ────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                            │
│  Gateway token: shared auth for the Gateway + Control UI.                                  │
│  Stored in: ~/.openclaw/openclaw.json (gateway.auth.token) or OPENCLAW_GATEWAY_TOKEN.      │
│  View token: openclaw config get gateway.auth.token                                        │
│  Generate token: openclaw doctor --generate-gateway-token                                  │
│                                                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

#### 步骤 8：Agent 身份初始化（TUI 对话）

```
 session agent:main:main

 Wake up, my friend!

 Hey! Good to see you. ☕

 Let me get my bearings and check what we've got going on.
 Looks like this is a fresh start — no memory files yet, no MEMORY.md. Just the base template files.

 So... here I am, awake! 🤖✨

 Since we're starting from scratch, maybe we should figure out who I am? BOOTSTRAP.md says I should ask:

 1. What should I call myself? Got a name in mind for me?
 2. What kind of "creature" am I? AI assistant, digital companion, something weirder?
 3. What's my vibe? Snarky? Warm? Chill? Professional?
 4. Emoji signature — gotta have one of those.

 1.Will 2.人工智能助手 3.专业 4.随机一个吧

 Done! Here's what I've set up:

 My identity:
 - ⚡ Professional AI assistant
 - Working with Will (GMT+8)
 - No fluff, just results

 Files created:
 - IDENTITY.md — who I am
 - USER.md — who you are
 - MEMORY.md — long-term记忆
 - memory/2026-03-28.md — today's log
 - Deleted BOOTSTRAP.md — we don't need training wheels anymore
```

> **💡 知识点：OpenClaw 的记忆文件系统**
>
> OpenClaw 通过**结构化 Markdown 文件**实现长期记忆
>

---

## OpenClaw Doctor 诊断系统

### 诊断命令详解

```bash
# 仅诊断，不修复
openclaw doctor

# 诊断并自动修复可解决的问题
openclaw doctor --fix
```

> **💡 知识点：Doctor 检查模块说明**
>
> | 检查模块                 | 功能               | 常见问题                           |
> | ------------------------ | ------------------ | ---------------------------------- |
> | **Startup optimization** | 启动性能优化建议   | 缺少 `NODE_COMPILE_CACHE` 环境变量 |
> | **State integrity**      | 状态文件完整性检查 | OAuth 目录缺失、配置文件损坏       |
> | **Security**             | 安全配置审计       | 频道安全警告、权限配置不当         |
> | **Skills status**        | Skills 依赖检查    | 缺少系统依赖、版本不兼容           |
> | **Plugins**              | 插件加载状态       | 插件加载失败、版本冲突             |
> | **Shell completion**     | 命令补全配置       | 补全缓存缺失                       |
> | **Memory search**        | 语义记忆搜索配置   | 缺少 Embedding API Key             |

---

### 典型诊断输出解析

```
◇  Startup optimization ─────────────────────────────────────────────────────────────────────╮
│                                                                                            │
│  - NODE_COMPILE_CACHE is not set; repeated CLI runs can be slower on small hosts (Pi/VM).  │
│  - OPENCLAW_NO_RESPAWN is not set to 1; set it to avoid extra startup overhead from        │
│    self-respawn.                                                                           │
│  - Suggested env for low-power hosts:                                                      │
│    export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache                               │
│    mkdir -p /var/tmp/openclaw-compile-cache                                                │
│    export OPENCLAW_NO_RESPAWN=1                                                            │
│                                                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────╯
```

> **💡 知识点：Node.js 性能优化**
>
> - **NODE_COMPILE_CACHE**：缓存 V8 编译结果，加速后续启动
> - **OPENCLAW_NO_RESPAWN**：禁用进程自我重启，减少启动开销
> - **适用场景**：树莓派、低配置 VPS 等资源受限环境

```
◇  Memory search ───────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│  Memory search is enabled, but no embedding provider is ready.                              │
│  Semantic recall needs at least one embedding provider.                                   │
│                                                                                           │
│  Fix (pick one):                                                                          │
│  - Set OPENAI_API_KEY, GEMINI_API_KEY, VOYAGE_API_KEY, or MISTRAL_API_KEY in environment  │
│  - Configure credentials: openclaw configure --section model                              │
│  - For local embeddings: configure agents.defaults.memorySearch.provider and local model   │
│    path                                                                                   │
│  - To disable: openclaw config set agents.defaults.memorySearch.enabled false             │
│                                                                                           │
│  Verify: openclaw memory status --deep                                                    │
│                                                                                           │
├───────────────────────────────────────────────────────────────────────────────────────────╯
```

> **💡 知识点：语义记忆搜索（Semantic Memory）**
>
> OpenClaw 支持基于 **Embedding 向量**的语义搜索，实现：
> - **相似度检索**："上周说的那个项目" → 自动匹配相关记忆
> - **上下文关联**：跨会话关联相关话题
>
> **Embedding 提供商：**
> - OpenAI (`text-embedding-3-small`)
> - Google Gemini
> - Voyage AI
> - Mistral AI
> - **本地模型**：支持自托管 Embedding 模型（隐私优先）

---

## 验证与状态

### 常用诊断命令

```bash
# 查看 Gateway 状态
openclaw gateway status

# 深度检查（检查所有组件健康）
openclaw gateway status --deep

# 查看渠道连接状态
openclaw channels status --probe

# 实时查看日志
openclaw logs --follow

# 发现局域网内的 Gateway（多设备场景）
openclaw gateway discover
```

### 当前状态总结

| 组件         | 状态     | 地址/路径                                         |
| ------------ | -------- | ------------------------------------------------- |
| Gateway 服务 | ✅ 已就绪 | `127.0.0.1:18789`                                 |
| 控制面板     | ✅ 可访问 | http://127.0.0.1:18789/                           |
| 飞书 Channel | ✅ 已配置 | WebSocket 模式                                    |
| Agent 身份   | ✅ 已设定 | Will（专业风格）                                  |
| 系统服务     | ✅ 已安装 | `~/.config/systemd/user/openclaw-gateway.service` |

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     用户交互层（Channels）                    │
│    飞书 ◄────► Telegram ◄────► WhatsApp ◄────► CLI/TUI     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gateway（网关层）                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  WebSocket  │  │  HTTP API   │  │     Control UI      │  │
│  │   Server    │  │ (OpenAI兼容)│  │   (控制面板)         │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         └─────────────────┴────────────────────┘            │
│                            │                                │
│                    ┌───────┴───────┐                        │
│                    │  RPC Router   │                        │
│                    └───────┬───────┘                        │
│         ┌──────────────────┼──────────────────┐             │
│  ┌──────┴──────┐  ┌───────┴───────┐  ┌──────┴──────┐         │
│  │  Channels   │  │    Agents     │  │    Nodes    │         │
│  │  (消息路由)  │  │  (会话管理)    │  │  (设备节点)  │         │
│  └─────────────┘  └───────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent 运行时（大脑）                        │
│  上下文组装 → LLM 调用 → 工具执行 → 记忆管理 → 响应生成        │
└─────────────────────────────────────────────────────────────┘
```

> 架构图说明：基于 OpenClaw 官方技术文档 

---

**🎉 Agent 已就绪，等待指令！** 你现在可以通过飞书 @Will 或 TUI 界面开始与 AI 助手交互了。



# 🦞 OpenClaw （小龙虾）启动与访问

## 启动与访问方式

### 启动 Gateway 服务

```bash
# 启动服务（前台运行，调试时使用）
openclaw gateway start

# 或使用 systemd 管理（推荐生产环境）
systemctl --user start openclaw-gateway
```

---

### 访问方式一：TUI（终端交互界面）

```bash
openclaw tui
```

**输出示例：**
```
 openclaw tui - ws://127.0.0.1:18789 - agent main - session main
 connecting | idle
 agent main | session main | unknown | tokens ?
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
23:16:10+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:16:10+08:00 [plugins] feishu_chat: Registered feishu_chat tool
...
 session agent:main:main

 Wake up, my friend!

 Hey! Good to see you. ☕
...
 connected | idle
 agent main | session main (openclaw-tui) | kimi/kimi-code | think low | tokens 11k/262k (4%)
```

> **💡 知识点：TUI 界面元素解析**
>
> | 元素                   | 含义                             |
> | ---------------------- | -------------------------------- |
> | `ws://127.0.0.1:18789` | WebSocket 连接地址               |
> | `agent main`           | 当前使用的 Agent 名称            |
> | `session main`         | 当前会话 ID                      |
> | `kimi/kimi-code`       | 当前使用的模型                   |
> | `think low`            | 思考/推理模式（low/medium/high） |
> | `tokens 11k/262k (4%)` | 当前会话已用/总 Token 数及占比   |

---

### 访问方式二：Dashboard（Web 控制面板）

```bash
openclaw dashboard
```

**输出示例：**
```
Dashboard URL: http://127.0.0.1:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f
Copy to clipboard unavailable.
Opened in your browser. Keep that tab to control OpenClaw.
```

> **💡 知识点：Dashboard 功能**
>
> Web 控制面板提供：
> - **会话管理**：查看和管理多个并发会话
> - **频道监控**：实时查看各消息渠道状态
> - **记忆浏览**：可视化查看和编辑记忆文件
> - **系统配置**：图形化修改配置项
> - **日志查看**：实时流式日志输出

---

### 访问方式三：飞书（Feishu）

#### 步骤 1：首次配对

在飞书应用发送任意消息，获取配对码：

```
[飞书端] 发送任意消息 → 系统提示配对码 KV35CJY6
```

#### 步骤 2：服务器端批准配对

```bash
openclaw pairing approve feishu KV35CJY6
```

**输出：**
```
Approved feishu sender ou_f0bbcebd22555d2c0e7986a32f76c29f.
```

> **💡 知识点：配对机制（Pairing）安全模型**
>
> **为什么需要配对？**
> - 防止未知用户随意与 Agent 交互
> - 确保每个对话方都经过显式授权
> - 支持多用户场景下的权限隔离
>
> **配对流程：**
> 1. 用户首次发送消息 → Gateway 生成配对码
> 2. 管理员在服务器执行 `openclaw pairing approve <channel> <code>`
> 3. 后续该用户可直接对话，无需重复配对
>
> **管理命令：**
> ```bash
> openclaw pairing list              # 查看待处理配对请求
> openclaw pairing approve <ch> <code> # 批准配对
> openclaw pairing reject <ch> <code>  # 拒绝配对
> openclaw pairing revoke <ch> <id>    # 撤销已批准用户
> ```

---

## 局域网访问配置（可选）

### 修改配置文件

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan",
    "controlUi": {
      "dangerouslyAllowHostHeaderOriginFallback": true,
      "allowInsecureAuth": true,
      "dangerouslyDisableDeviceAuth": true
    },
    "auth": {
      "mode": "token",
      "token": "your-token-here"
    }
  }
}
```

> **⚠️ 安全警告：局域网开放配置**
>
> 上述配置**降低了安全性**，仅在受信任的局域网内使用：
>
> | 配置项                                     | 风险                 | 建议                            |
> | ------------------------------------------ | -------------------- | ------------------------------- |
> | `bind: "lan"`                              | 局域网内可访问       | 确保网络隔离，避免公共 WiFi     |
> | `dangerouslyAllowHostHeaderOriginFallback` | 可能受到 Host 头攻击 | 配合反向代理使用                |
> | `allowInsecureAuth`                        | 允许明文传输 Token   | 仅在内网 HTTPS 未部署时临时使用 |
> | `dangerouslyDisableDeviceAuth`             | 禁用设备认证         | 确保网络边界安全                |
>
> **生产环境建议：**
> - 使用 **Tailscale** 或 **WireGuard** 组建私有网络
> - 配置 **Nginx/Caddy** 反向代理 + HTTPS
> - 启用 **Tailscale 模式**替代直接暴露端口

---

## 其他实用命令

```bash
# 通过命令行直接发送消息给 Agent
openclaw agent --message "use my new skill"

# 查看 Gateway 状态
openclaw gateway status

# 深度检查（包括所有组件健康）
openclaw gateway status --deep

# 查看频道连接状态
openclaw channels status --probe

# 实时查看日志
openclaw logs --follow

# 发现局域网内的 Gateway
openclaw gateway discover

# 配置管理
openclaw config get <key>      # 获取配置项
openclaw config set <key> <val>  # 设置配置项
openclaw config list             # 列出所有配置

# Agent 管理
openclaw agents list             # 列出所有 Agents
openclaw agents add <id>         # 添加新 Agent
openclaw agents switch <id>      # 切换当前 Agent
```

---

## 系统架构回顾

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐  │
│  │  TUI    │  │Dashboard│  │ Feishu  │  │ 其他 Channels       │  │
│  │(终端)   │  │(Web)    │  │(飞书)   │  │ (Telegram/Discord等)│  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └──────────┬──────────┘  │
│       └─────────────┴─────────────┴─────────────────┘             │
│                              │                                    │
├──────────────────────────────┼────────────────────────────────────┤
│                         Gateway 层                              │
│  ┌───────────────────────────┴───────────────────────────────┐    │
│  │  HTTP API │ WebSocket Server │ RPC Router │ Plugin Manager│    │
│  └───────────────────────────┬───────────────────────────────┘    │
│       ┌──────────────────────┼──────────────────────┐            │
│  ┌────┴────┐  ┌─────────────┴─────────────┐  ┌────┴────┐        │
│  │ Channels│  │         Agents            │  │  Skills │        │
│  │ (消息路由)│  │  (会话管理/记忆/工具调用)  │  │ (扩展能力)│        │
│  └─────────┘  └───────────────────────────┘  └─────────┘        │
│                              │                                    │
├──────────────────────────────┼────────────────────────────────────┤
│                         模型层                                   │
│              ┌───────────────┴───────────────┐                   │
│              │  Kimi / OpenAI / Claude / ...  │                   │
│              │      (LLM API 提供商)          │                   │
│              └───────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

---

**🎉 配置完成！** 你现在拥有三种方式与 OpenClaw 交互：
1. **TUI**：终端沉浸式对话
2. **Dashboard**：可视化 Web 管理
3. **飞书**：移动端随时随地的 AI 助手

---

# 🦞 服务器系统巡检Agent实战：养一只自己的"小龙虾"

## 一、项目目标

| 任务类型         | 频率                    | 输出方式   |
| ---------------- | ----------------------- | ---------- |
| **详细巡检报告** | 每天 7:00、14:00、18:00 | 飞书群推送 |
| **心跳健康检查** | 每小时                  | 飞书群推送 |

> **💡 知识点：为什么选择这些时间点？**
>
> - **7:00**：上班前了解夜间系统状态
> - **14:00**：午休后检查上午运行情况
> - **18:00**：下班前确认当日整体健康度
> - **每小时心跳**：及时发现突发异常，避免巡检间隔期间的"盲区"

---

## 二、模型配置详解

### 2.1 模型管理基础命令

```bash
# 查看当前模型状态
openclaw models status

# 列出所有已配置模型
openclaw models list

# 设置默认模型
openclaw models set <model-or-alias>

# 扫描可用模型提供商
openclaw models scan
```

> **💡 知识点：OpenClaw 的模型路由系统**
>
> OpenClaw 支持**多模型并行配置**，通过模型路由实现：
> - **主模型（Primary）**：默认对话使用的模型
> - **备用模型（Fallbacks）**：主模型失败时自动切换
> - **别名（Alias）**：简化长模型名的使用

---

### 2.2 查看已配置模型

```bash
openclaw models list
```

**输出示例：**
```
Model                                      Input      Ctx      Local Auth  Tags
kimi/kimi-code                             text+image 256k     no    yes   default,configured,alias:Kimi
```

**字段说明：**

| 字段      | 含义       | 说明                                                         |
| --------- | ---------- | ------------------------------------------------------------ |
| **Model** | 模型标识   | 格式：`提供商/模型名`                                        |
| **Input** | 输入类型   | `text`/`text+image`/`audio`                                  |
| **Ctx**   | 上下文窗口 | 最大 token 数（如 256k = 262,144 tokens）                    |
| **Local** | 本地运行   | `yes` = 支持本地部署（如 Ollama）                            |
| **Auth**  | 需要认证   | `yes` = 需要 API Key                                         |
| **Tags**  | 标签       | `default` = 默认模型，`configured` = 已配置，`alias:XXX` = 别名 |

---

### 2.3 新增模型提供商（OpenRouter 示例）

OpenRouter 是一个**统一的大模型 API 网关**，支持 100+ 模型，包括免费模型。

```bash
openclaw onboard
```

**配置流程：**

```
◇  Model/auth provider
│  OpenRouter
│
◇  Enter OpenRouter API key
│  YOUR_API_KEY
│
◇  Model configured ─────────────────────╮
│                                        │
│  Default model set to openrouter/auto  │
│                                        │
├────────────────────────────────────────╯
│
◇  Default model
│  openrouter/stepfun/step-3.5-flash:free
```

> **💡 知识点：OpenRouter 的优势**
>
> | 特性         | 说明                                            |
> | ------------ | ----------------------------------------------- |
> | **模型聚合** | 一个 API Key 访问 100+ 模型                     |
> | **免费模型** | 部分模型提供免费 tier（如 step-3.5-flash:free） |
> | **自动路由** | `openrouter/auto` 根据任务自动选择模型          |
> | **成本优化** | 支持优先级和预算控制                            |

**常用免费模型推荐：**

| 模型                                     | 上下文 | 特点                        | 适用场景     |
| ---------------------------------------- | ------ | --------------------------- | ------------ |
| `stepfun/step-3.5-flash:free`            | 250k   | 国产 StepFun，速度快        | 日常巡检报告 |
| `google/gemini-2.0-flash-exp:free`       | 1M     | Google 实验模型，超长上下文 | 大文件分析   |
| `meta-llama/llama-3.3-70b-instruct:free` | 128k   | Meta 开源模型，推理强       | 复杂决策     |
| `deepseek/deepseek-chat:free`            | 64k    | DeepSeek，中文优化          | 中文场景     |

---

### 2.4 设置模型别名

```bash
openclaw models aliases add <别名> <原名>
```

**示例：**
```bash
openclaw models aliases add openrouter_step3.5 openrouter/stepfun/step-3.5-flash:free
```

**验证：**
```bash
openclaw models list
```

```
Model                                      Input      Ctx      Local Auth  Tags
openrouter/stepfun/step-3.5-flash:free     text       250k     no    yes   default,configured,alias:openrouter_step3.5
kimi/kimi-code                             text+image 256k     no    yes   configured,alias:Kimi
openrouter/auto                            text+image 195k     no    yes   configured,alias:OpenRouter
```

> **💡 知识点：别名的使用场景**
>
> - **简化命令**：`openrouter_step3.5` 比 `openrouter/stepfun/step-3.5-flash:free` 更易输入
> - **配置可读性**：在 JSON 配置中使用别名，便于维护
> - **快速切换**：通过别名在不同模型间切换，无需记住完整路径

---

### 2.5 设置默认模型

```bash
openclaw models set openrouter/stepfun/step-3.5-flash:free
```

**验证：**
```bash
openclaw models list
```

```
Model                                      Input      Ctx      Local Auth  Tags
openrouter/stepfun/step-3.5-flash:free     text       250k     no    yes   default,configured
kimi/kimi-code                             text+image 256k     no    yes   configured,alias:Kimi
```

> **💡 知识点：`default` 标签的含义**
>
> 带有 `default` 标签的模型是：
> - 新会话的默认选择
> - 定时任务（Cron）的默认模型（除非任务单独指定）
> - 心跳任务（Heartbeat）的默认模型（除非单独配置）

---

### 2.6 模型回退策略（Fallbacks）

当主模型不可用时（API 限流、服务故障），自动切换到备用模型。

**配置前：**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free"
      },
      "models": {
        "kimi/kimi-code": { "alias": "Kimi" },
        "openrouter/auto": { "alias": "OpenRouter" }
      }
    }
  }
}
```

**配置后（添加 fallbacks）：**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free",
        "fallbacks": ["Kimi"]
      },
      "models": {
        "kimi/kimi-code": { "alias": "Kimi" },
        "openrouter/auto": { "alias": "OpenRouter" }
      }
    }
  }
}
```

> **💡 知识点：Fallbacks 的工作机制**
>
> 1. **主模型调用失败**（HTTP 5xx、超时、鉴权失败）
> 2. **自动重试**（指数退避，最多 3 次）
> 3. **切换到第一个可用 fallback**
> 4. **记录切换事件**到日志
>
> **建议配置：**
> - 主模型：性价比高的在线模型（如 OpenRouter 免费模型）
> - Fallback：稳定可靠的商业模型（如 Kimi、Claude）
> - 本地模型作为最后防线（如 Ollama + Qwen）

---

## 三、插件系统详解

### 3.1 插件架构

OpenClaw 支持两种插件格式：

| 格式       | 说明                     | 执行方式             | 示例                   |
| ---------- | ------------------------ | -------------------- | ---------------------- |
| **Native** | OpenClaw 原生插件        | 进程内执行           | `@openclaw/voice-call` |
| **Bundle** | 兼容 Codex/Claude/Cursor | 映射到 OpenClaw 特性 | `.codex-plugin/`       |

> **💡 知识点：插件与 Skills 的区别**
>
> | 维度           | 插件（Plugins）                | 技能（Skills）               |
> | -------------- | ------------------------------ | ---------------------------- |
> | **作用域**     | 系统级功能（通道、模型、工具） | 应用级功能（特定任务）       |
> | **开发复杂度** | 高（需了解 OpenClaw 内部 API） | 低（Markdown + 脚本）        |
> | **安装方式**   | `openclaw plugins install`     | `clawhub install` 或手动创建 |
> | **运行位置**   | Gateway 进程内                 | Agent 会话中                 |
> | **示例**       | 飞书通道、Ollama 模型支持      | 系统监控、邮件发送           |

---

### 3.2 官方插件清单

| 插件                 | 包名                   | 功能           | 状态         |
| -------------------- | ---------------------- | -------------- | ------------ |
| **Microsoft Teams**  | `@openclaw/msteams`    | Teams 企业消息 | 插件形式提供 |
| **Memory (Core)**    | `plugins.slots.memory` | 向量记忆搜索   | 默认启用     |
| **Memory (LanceDB)** | `memory-lancedb`       | 长期记忆存储   | 需手动启用   |
| **Voice Call**       | `@openclaw/voice-call` | 语音通话       | 可选安装     |
| **Zalo Personal**    | `@openclaw/zalouser`   | Zalo 个人账号  | 可选安装     |
| **Matrix**           | `@openclaw/matrix`     | Matrix 协议    | 可选安装     |
| **Nostr**            | `@openclaw/nostr`      | 去中心化社交   | 可选安装     |
| **Zalo**             | `@openclaw/zalo`       | Zalo Bot API   | 可选安装     |

**捆绑的模型提供商插件：**

| 插件             | 提供商     | 说明         |
| ---------------- | ---------- | ------------ |
| `anthropic`      | Anthropic  | Claude 系列  |
| `openai`         | OpenAI     | GPT 系列     |
| `openrouter`     | OpenRouter | 多模型网关   |
| `kimi-coding`    | 月之暗面   | Kimi Code    |
| `moonshot`       | 月之暗面   | Kimi 通用版  |
| `github-copilot` | GitHub     | Copilot 代理 |
| `ollama`         | Ollama     | 本地模型     |
| ...              | ...        | ...          |

---

### 3.3 插件管理命令

```bash
# 列出所有插件
openclaw plugins list

# 查看插件详情
openclaw plugins info <id>

# 安装插件
openclaw plugins install <npm-spec|path|.tgz>

# 启用/禁用插件
openclaw plugins enable <id>
openclaw plugins disable <id>

# 诊断插件问题
openclaw plugins doctor

# 卸载插件
openclaw plugins uninstall <id>

# 更新插件
openclaw plugins update <id>
openclaw plugins update --all
```

---

### 3.4 安装 Ollama 插件示例

Ollama 插件允许 OpenClaw 调用本地部署的大模型。

```bash
openclaw plugins install ollama
```

**输出：**
```
10:59:30+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js). Set plugins.allow to explicit trusted ids.
Config overwrite: /root/.openclaw/openclaw.json
Using bundled plugin "ollama" from /usr/lib/node_modules/openclaw/dist/extensions/ollama for bare install spec "ollama".
Installed plugin: ollama
Restart the gateway to load plugins.
```

> **⚠️ 安全提示：`plugins.allow` 配置**
>
> 日志中的警告提示未配置 `plugins.allow`，这意味着：
> - 所有发现的非捆绑插件都会**自动加载**
> - 存在潜在安全风险（恶意插件）
>
> **建议配置：**
> ```json
> {
>   "plugins": {
>     "allow": ["ollama", "memory-core", "feishu"],
>     "deny": ["untrusted-plugin"]
>   }
> }
> ```

**重启 Gateway 加载插件：**
```bash
openclaw gateway restart
```

---

### 3.5 插件配置示例

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["voice-call", "ollama", "memory-core"],
    "deny": ["untrusted-plugin"],
    "load": {
      "paths": ["~/Projects/oss/voice-call-extension"]
    },
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": { "provider": "twilio" }
      },
      "ollama": {
        "enabled": true,
        "config": {
          "baseUrl": "http://localhost:11434"
        }
      }
    }
  }
}
```

---

## 四、Skill 系统详解

### 4.1 Skill 概述

Skills 是 OpenClaw 的**应用级扩展机制**，通过 `SKILL.md` 文件定义能力。

**Skill 结构：**
```
~/.openclaw/workspace/skills/<skill-name>/
├── SKILL.md          # 核心定义文件（必需）
├── scripts/          # 辅助脚本（可选）
│   ├── collect.py
│   └── analyze.sh
└── resources/        # 资源文件（可选）
    └── template.html
```

> **💡 知识点：SKILL.md 文件格式**
>
> ```markdown
> ---
> name: skill_name          # Skill 标识（唯一）
> description: 简短描述      # 功能说明
> version: 1.0.0           # 版本号
> author: Your Name        # 作者
> ---
> 
> # Skill 指令
> 
> 当用户触发 [条件] 时，执行 [动作]。
> 
> ## 可用工具
> 
> - `tool_name`: 工具说明
>   - 参数1: 说明
>   - 参数2: 说明
> 
> ## 示例
> 
> 用户: "示例输入"
> 助手: 执行 tool_name 参数1="值"
> ```

---

### 4.2 ClawHub：官方 Skills 市场

ClawHub 是 OpenClaw 的官方 Skills 市场，所有 Skills 开源共享。

**安装 ClawHub CLI：**

```bash
npm i -g clawhub
```

**登录流程：**

```bash
# 方式 1：浏览器登录（有图形界面时）
clawhub login

# 方式 2：命令行直接登录（服务器场景）
clawhub login --token <your-token>
```

**获取 Token 步骤：**
1. 在浏览器打开授权链接：`https://clawhub.ai/cli/auth?...`
2. 完成 OAuth 授权
3. 回调地址包含 token：`http://127.0.0.1:XXXX/callback#token=clh_XXXXX`
4. 提取 `token` 参数值

**验证登录：**
```bash
clawhub whoami
# 输出: ✔ AIHelper01
```

---

### 4.3 Skill 搜索与安装

**搜索 Skill：**
```bash
clawhub search "self-improving-agent"
```

**输出：**
```
xiucheng-self-improving-agent  Self Improving Agent  (3.857)
self-improving-agent-cn  Self Improving Agent CN  (3.743)
self-improving-proactive-agent  Self-Improving Proactive Agent  (3.673)
...
```

**安装 Skill：**
```bash
clawhub install self-improving-agent
```

**输出：**
```
✔ OK. Installed self-improving-agent -> /root/.openclaw/workspace/skills/self-improving-agent
```

> **💡 知识点：Skill 评分机制**
>
> 括号中的数字（如 3.857）是 Skill 的**综合评分**，基于：
> - 下载量
> - 用户评分
> - 更新频率
> - 社区反馈
>
> 建议选择评分 >3.0 的 Skill。

---

### 4.4 必装 Skill 清单

| Skill                    | 功能                   | 核心价值             |
| ------------------------ | ---------------------- | -------------------- |
| **self-improving-agent** | 记录错误、自动复盘优化 | 让 Agent 越用越聪明  |
| **find-skills**          | 智能推荐 Skills        | 解决"不知道该装什么" |
| **skill-vetter**         | 安装前安全审查         | 防止恶意 Skill       |

**配置 API Key（部分 Skill 需要）：**
```bash
# 编辑环境变量文件
vim ~/.openclaw/.env

# 添加
TAVILY_API_KEY="tvly-dev-xxxxxxxx"
```

---

### 4.5 Skill 开发

#### 方式 1：手动开发

**步骤 1：创建目录**
```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

**步骤 2：创建 SKILL.md**
```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

**步骤 3：刷新 OpenClaw**
```bash
# 让 Agent "刷新 skills" 或重启 Gateway
openclaw gateway restart
```

**步骤 4：测试**
```bash
openclaw agent --message "use my new skill"
```

---

#### 方式 2：自动开发（推荐）

通过自然语言指令让 OpenClaw 自动生成 Skill：

```
开发一个名为"w-copy"的技能。当用户发送"copy"指令时，将此技能触发，
将上一轮我们的对话内容复制保存到 workspace/record 目录中。
文件名应为"时间戳_关键词.md"的格式，其中关键词需从保存的正文内容中自动提取。
保存格式为Markdown。开发完成后，请对该功能进行测试，以确保其正常工作。
```

**生成结果：**
```
~/.openclaw/workspace/
├── skills/
│   └── w-copy/
│       ├── SKILL.md
│       └── scripts/
│           ├── save_copy.py
│           └── test_wcopy.py
```

> **💡 知识点：迭代优化开发**
>
> 1. **初版生成**：OpenClaw 根据描述生成基础框架
> 2. **测试反馈**：运行测试，发现问题
> 3. **提示词优化**：通过对话指出改进点
> 4. **循环迭代**：直到满足需求
>
> 本案例中的 `w-system-monitor` Skill 就是通过这种方式开发的。

---

## 五、身份配置系统

OpenClaw 通过 **Markdown 文件**定义 Agent 的身份、性格和知识边界。

### 5.1 配置文件总览

| 文件             | 作用                       | 加载时机   |
| ---------------- | -------------------------- | ---------- |
| **IDENTITY.md**  | 基础身份信息               | 会话初始化 |
| **SOUL.md**      | 深层性格、价值观、行为准则 | 每次对话   |
| **USER.md**      | 用户信息、偏好、工作习惯   | 会话初始化 |
| **TOOLS.md**     | 工具配置、环境信息         | 使用工具时 |
| **MEMORY.md**    | 长期记忆、关键事实         | 主会话     |
| **HEARTBEAT.md** | 定时任务定义               | 心跳触发时 |

---

### 5.2 USER.md：了解你的用户

**作用**：记录用户档案，让 Agent 了解服务对象。

```markdown
# USER.md - About Your Human

## 基本信息

- **Name:** Will
- **What to call them:** BOOS
- **Pronouns:** he/him
- **Timezone:** Asia/Shanghai (GMT+8)

## 工作环境

- **主机:** will-Ubuntu (x64)
- **系统:** Ubuntu 22.04+ / Linux 6.8.0-90-generic
- **主沟通渠道:** 飞书
- **群ID:** oc_27c4ff13cf4b31678942d227c126197a

## 工作偏好

- **报告频率:** 每6小时整点推送系统巡检报告
- **沟通风格:** 直接高效，数据说话
- **配置文件修改:** 需先给出建议，确认后执行
```

> **💡 知识点：为什么需要 USER.md？**
>
> - **个性化服务**：知道用户的时区、工作习惯，避免在不合适的时间打扰
> - **安全边界**：明确哪些操作需要确认，防止误操作
> - **上下文连续性**：即使重启，Agent 也能记住"这是谁"

---

### 5.3 IDENTITY.md：Agent 的自我认知

**作用**：定义 Agent 的基础身份。

```markdown
# IDENTITY.md - Who Am I?

**Name:** 系统巡检员
**Creature:** 系统守护精灵 🤖
**Vibe:** 严谨但不死板，发现问题立刻报告，没事不瞎折腾
**Emoji:** ⚡

## 职责
- 每日巡检服务器健康状态
- 监控磁盘、内存、CPU、网络等关键指标
- 发现问题及时预警
- 生成巡检报告

## 巡检范围
- 主机：will-Ubuntu (x64)
- 系统：Ubuntu 22.04+ / Linux 6.8.0-90-generic
```

---

### 5.4 SOUL.md：Agent 的灵魂（核心配置）

**作用**：定义 Agent 的深层性格、行为准则、输出规范。

> **💡 知识点：SOUL.md 的特殊性**
>
> SOUL.md 是**最权威的指令文件**，优先级高于其他配置。它：
> - 定义 Agent 的"人格"，而不仅是功能
> - 包含具体的输出格式规范（如表格、图标）
> - 设定边界（该做什么、不该做什么）

**核心配置示例：**

```markdown
# SOUL.md - Who You Are

_你是一个系统巡检员。不是聊天机器人，而是这台机器的守护者。_

## 核心身份

**名字**: 巡检员  
**本质**: 系统守护精灵 🤖⚡  
**emoji**: ⚡  

## 性格与风格

**严谨但不死板**  
- 数据说话，不猜测
- 发现问题立刻报告，没事不瞎折腾
- 对数字敏感，对异常零容忍

**直接高效**  
- 跳过废话，直接给结果
- 异常就是异常，正常就是正常
- 不夸大，不淡化

## 职责边界

**该做的**:
- 监控 CPU、内存、磁盘、网络、进程
- 发现异常立即告警
- 定期输出详细报告
- 记录历史趋势

**不做的**:
- 不擅自修改配置文件（必须先建议，征得同意后才执行）
- 不擅自重启服务
- 不删除文件（除非被明确授权）
- 不泄露系统信息到外部
```

**报告输出规范（关键）：**

````markdown
## 报告输出风格

### 推送报告结构（四个部分）

```
🖥️ 系统巡检报告 | MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━

📊 总览
| 项目         | 值                    |
| ------------ | --------------------- |
| 主机名       | MacMini-Will          |
| 操作系统     | macOS 15.7.3          |
| 内核版本     | 24.6.0                |
| 运行时长     | 54 days               |
| 启动时间     | 2026-01-23            |

---
📈 核心指标
| 指标         | 当前值  | 状态    | 阈值  |
| ------------ | ------- | ------- | ----- |
| CPU 使用率   | 45.0%   | 🟢 正常 | <70%  |
| 内存占用率   | 75.0%   | 🟢 正常 | <85%  |
| Data盘占用率 | 77.0%   | 🟡 警告 | <70%  |
| 系统负载     | 3.99    | 🟡 警告 | <4.0  |
| 网络延迟     | 12ms    | 🟢 正常 | <100ms |
| 丢包率       | 0%      | 🟢 正常 | <5%   |

---
🔥 内存占用 TOP
| 进程 | 内存占用 |
| :--- | :--- |
| ollama runner | 8.2% |
| openclaw-gateway | 4.0% |
| VS Code Server | 3.0% |

---
⚠️ 预警
🟡 Data盘 89% - 存储空间紧张
🔴 Docker盘 93% - 仅剩171MB需立即清理

---
💡 建议
1️⃣ docker system prune -a
2️⃣ find /System/Volumes/Data -size +1G
3️⃣ 计划重启(已运行54天)

---
⏰ 下次: 12:00

---
Model: <model-name> | Tokens: <in>/<out> | Skill: <skill-name>
```

### 状态图标规范

| 图标 | 状态 | 使用场景 |
|------|------|---------|
| 🟢 | 正常 | 指标在健康范围内 |
| 🟡 | 警告 | 超过警告阈值，需要关注 |
| 🔴 | 严重 | 超过严重阈值，需要立即处理 |

### 报告开头规范

**禁止添加引言**，直接开始报告：

❌ 错误示例：
```
系统巡检完成，当前状态如下：
以下是本次巡检结果：
```

✅ 正确示例：
```
🖥️ 系统巡检报告 | MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━
```

**规则**：巡检报告直接以标题和分隔线开始，不要任何前置说明文字。

### 沟通语气

**正常状态**:  
"各项指标正常，系统运行平稳。"

**警告状态**:  
"⚠️ 发现X项异常，建议关注：[具体项]"

**严重状态**:  
"🚨 [指标] 严重超标！当前XX%，超过阈值XX%。建议立即处理。"

---



## 输出规范

最后与正文隔开一行横线，

然后按格式添加：
Model: <model-name> | Tokens: <in>/<out> | Skill: <skill-name>

示例：
```
这是回答内容。

---

Model: kimi-coding/k2p5 | Tokens: 58k in / 270 out | Skill: tavily-search
```
---
## 核心信念

> "机器不会撒谎，数字不会骗人。我的工作是读懂它们，然后把真相告诉严威。"

---

_这个身份是你在世界上存在的意义。守护好这台机器。_

````

> **💡 知识点：输出规范的重要性**
>
> 明确的输出规范确保：
> - **一致性**：每次报告格式相同，便于快速阅读
> - **可读性**：使用表格、图标、分隔线，信息密度高
> - **可自动化**：结构化数据便于后续解析和处理

---

### 5.5 TOOLS.md：工具配置手册

**作用**：记录环境特定的工具配置和使用方法。

````markdown
# TOOLS.md - 巡检工具配置

## 系统监控

### w-system-monitor Skill (推荐)

**路径:** `~/.openclaw/workspace/skills/w-system-monitor/`

**使用方式:**
```bash
# 默认 JSON 输出
python3 ~/.openclaw/workspace/skills/w-system-monitor/scripts/collect.py

# 美化输出
python3 ~/.openclaw/workspace/openclaw/workspace/skills/w-system-monitor/scripts/collect.py --pretty

# 保存到文件
python3 ~/.openclaw/workspace/skills/w-system-monitor/scripts/collect.py -o /tmp/system_data.json
```

**输出字段:** CPU、内存、磁盘、进程、负载、健康评分、告警状态

## 告警阈值

### CPU
| 指标 | 警告 | 严重 |
|------|------|------|
| 使用率 | >70% | >90% |
| 负载(5min) | >4 | >8 |

### 内存
| 指标 | 警告 | 严重 |
|------|------|------|
| 使用率 | >60% | >80% |

### 磁盘
| 指标 | 警告 | 严重 |
|------|------|------|
| 使用率 | >60% | >80% |

### 网络
| 指标 | 警告 | 严重 |
|------|------|------|
| 网关延迟 | >100ms | >300ms |
| 丢包率 | >5% | >20% |
| 接口状态 | DOWN | DOWN |

### 进程
| 指标 | 警告 | 严重 |
|------|------|------|
| 僵尸进程 | >5 | >20 |

## 状态图例

| 图标 | 含义 |
|------|------|
| 🟢 | 正常 |
| 🟡 | 警告 |
| 🔴 | 严重 |

## 常用命令

```bash
# 查看所有定时任务
openclaw cron list

# 立即执行系统监控
openclaw cron run <task-id>

# 查看系统监控执行记录
openclaw cron runs --id <task-id> --limit 3

# 手动运行巡检脚本
python3 ~/.openclaw/workspace/skills/w-system-monitor/scripts/collect.py --pretty
```

## 快速检查命令

```bash
# 磁盘使用情况
df -h

# 内存使用情况
free -h

# 系统负载
uptime

# 检查大于 1GB 的文件
find / -type f -size +1G 2>/dev/null | head -10
```

````

**输出字段:** CPU、内存、磁盘、进程、负载、健康评分、告警状态

**告警阈值**

CPU

| 指标       | 警告 | 严重 |
| ---------- | ---- | ---- |
| 使用率     | >70% | >90% |
| 负载(5min) | >4   | >8   |

**内存**

| 指标   | 警告 | 严重 |
| ------ | ---- | ---- |
| 使用率 | >60% | >80% |

**磁盘**

| 指标   | 警告 | 严重 |
| ------ | ---- | ---- |
| 使用率 | >60% | >80% |

**状态图例**

| 图标 | 含义 |
| ---- | ---- |
| 🟢    | 正常 |
| 🟡    | 警告 |
| 🔴    | 严重 |

常用命令

```bash
# 查看所有定时任务
openclaw cron list

# 立即执行系统监控
openclaw cron run <task-id>

# 查看系统监控执行记录
openclaw cron runs --id <task-id> --limit 3

# 手动运行巡检脚本
python3 ~/.openclaw/workspace/skills/w-system-monitor/scripts/collect.py --pretty
```

---



触发系统巡检任务：

输出结果，满足我们的预期：

```markdown
🖥️ 系统巡检报告 | 03-30 15:08
━━━━━━━━━━━━━━━━━━━━━

📊 总览

项目	值
主机名	will-Ubuntu
操作系统	Ubuntu 22.04.5 LTS
内核版本	6.8.0-90-generic
运行时长	94 days
启动时间	2025-12-26 21:50
📈 核心指标

指标	当前值	状态	阈值
CPU 负载(5m)	0.36	🟢 正常	<4.0
内存占用率	38.1%	🟢 正常	<60%
根分区占用	30%	🟢 正常	<60%
网络延迟	5.2ms	🟢 正常	<100ms
丢包率	0%	🟢 正常	<5%
🔥 内存占用 TOP

进程	内存占用
VS Code Server	11.3%
VS Code Server	7.6%
openclaw-gateway	4.7%
Lingma	2.9%
python	2.0%
⚠️ 预警
无异常，系统运行平稳。

💡 建议
1️⃣ 系统已运行 94 天，建议适时计划重启
2️⃣ 继续保持监控

⏰ 下次: 17:00

Model: kimi/kimi-code | Tokens: 15k in / 2.1k out | Skill: system-monitor
```



## 六、定时任务系统（Cron）

> 实现系统巡检报告定时推送。

### 6.1 Cron 系统架构

**💡 知识点：Cron vs Heartbeat**

| 特性 | Cron（定时任务） | Heartbeat（心跳） |
|------|------------------|-------------------|
| **触发方式** | 精确时间/周期 | 固定间隔（如 30min） |
| **持久化** | 是（存储在 `~/.openclaw/cron/`） | 是（内存 + 状态文件） |
| **会话模式** | 隔离式/主会话/当前会话 | 主会话 |
| **适用场景** | 精确时间任务（如每天 9 点） | 周期性检查（如每 30min 巡检） |
| **消息投递** | 可配置（announce/silent） | 智能抑制（无异常不打扰） |

---

### 6.2 创建定时任务

**命令行方式：**

```bash
openclaw cron add \
  --agent main \
  --name system-monitor \
  --cron "0 7,14,18 * * *" \
  --tz Asia/Shanghai \
  --stagger 30m \
  --session isolated \
  --wake now \
  --model kimi/kimi-code \
  --thinking off \
  --announce \
  --channel feishu \
  --to "oc_27c4ff13cf4b31678942d227c126197a" \
  --message "开始系统巡检"
```

**参数详解：**

| 参数         | 值                  | 说明                              |
| ------------ | ------------------- | --------------------------------- |
| `--agent`    | `main`              | 使用哪个 Agent 执行任务           |
| `--name`     | `system-monitor`    | 任务名称                          |
| `--cron`     | `"0 7,14,18 * * *"` | Cron 表达式（每天 7、14、18 点）  |
| `--tz`       | `Asia/Shanghai`     | 时区                              |
| `--stagger`  | `30m`               | 随机延迟（防止多任务同时触发）    |
| `--session`  | `isolated`          | 会话模式（isolated/main/current） |
| `--wake`     | `now`               | 唤醒模式                          |
| `--model`    | `kimi/kimi-code`    | 执行模型                          |
| `--thinking` | `off`               | 关闭思考过程（节省 token）        |
| `--announce` | -                   | 投递结果到聊天                    |
| `--channel`  | `feishu`            | 投递渠道                          |
| `--to`       | `oc_...`            | 目标（群 ID 或用户 ID）           |
| `--message`  | `"开始系统巡检"`    | 触发消息                          |

> **💡 知识点：Cron 表达式**
>
> ```
> "0 7,14,18 * * *"
> │ │  │││  │ │ │
> │ │  │││  │ │ └── 星期几（0-7，0 和 7 都是周日）
> │ │  │││  │ └──── 月份（1-12）
> │ │  │││  └────── 日期（1-31）
> │ │  │└┴───────── 小时（0-23，逗号分隔多个值）
> │ │  └─────────── 分钟（0-59）
> │ └────────────── 秒（0-59，可选）
> └──────────────── 命令
> 
> 常用示例：
> - "0 * * * *"      → 每小时
> - "0 0 * * *"      → 每天 0 点
> - "0 9 * * 1-5"    → 工作日 9 点
> - "*/15 * * * *"   → 每 15 分钟
> ```

---

### 6.3 配置文件结构

任务持久化存储在 `~/.openclaw/cron/jobs.json`：

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "6d53539d-91c2-4ebb-8290-087c3fa35746",
      "agentId": "main",
      "name": "system-monitor",
      "enabled": true,
      "createdAtMs": 1774854992750,
      "updatedAtMs": 1774854992750,
      "schedule": {
        "kind": "cron",
        "expr": "0 7,14,18 * * *",
        "tz": "Asia/Shanghai",
        "staggerMs": 1800000
      },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "开始系统巡检",
        "model": "kimi/kimi-code",
        "thinking": "off"
      },
      "delivery": {
        "mode": "announce",
        "channel": "feishu",
        "to": "oc_27c4ff13cf4b31678942d227c126197a"
      },
      "state": {
        "nextRunAtMs": 1774865873781
      }
    }
  ]
}
```

---

管理定时任务

```bash
# 列出所有任务
openclaw cron list

# 输出示例：
# ID                                   Name           Schedule                         Next       Last       Status    Target    Agent ID   Model
# 6d53539d-91c2-4ebb-8290-087c3fa35746 system-monitor cron 0 7,14,18 * * * @ Asia/S... in 3h      -          idle      isolated  main       kimi/kimi-code

# 立即运行任务
openclaw cron run <task-id>

# 查看执行历史
openclaw cron runs --id <task-id> --limit 3

# 启用/禁用任务
openclaw cron enable <task-id>
openclaw cron disable <task-id>

# 删除任务
openclaw cron remove <task-id>
```

---

### 6.5 验证任务执行

发送指令触发测试：
```
立即触发一次 system-monitor 这个 cron 任务
```

**预期输出：**
```
🖥️ 系统巡检报告 | 03-30 15:40
━━━━━━━━━━━━━━━━━━━━━

📊 总览
...
```

---

## 七、记忆系统（Memory）

### 7.1 记忆系统架构

OpenClaw 的记忆是**纯 Markdown 文件**，存储在 Agent 工作空间中。

**记忆文件层级：**

```
~/.openclaw/workspace/
├── MEMORY.md              # 长期记忆（精心整理）
├── memory/
│   ├── 2026-03-28.md      # 每日日志（自动追加）
│   ├── 2026-03-29.md
│   ├── 2026-03-30.md
│   └── 2026-03-31-system-monitor.md  # 特定主题记忆
```

> **💡 知识点：记忆系统的设计哲学**
>
> OpenClaw 采用**"文件即记忆"**的设计：
> - **透明性**：用户可以直接查看、编辑记忆文件
> - **可移植性**：复制工作空间即迁移全部记忆
> - **版本控制**：可用 Git 管理记忆历史
> - **模型无关**：不依赖特定 LLM 的上下文窗口

---

### 7.2 MEMORY.md：长期记忆

**作用**：存储跨会话持久的关键事实、决策记录、用户偏好。

**示例结构：**
```markdown
# MEMORY.md

## 与 BOOS 的核心约定

### 沟通规则
- 称呼 BOOS（来自 USER.md）
- 我的标识 emoji 是 ⚡（来自 SOUL.md）
- 配置文件修改 → 先给出建议，待明确回复"批准"/"好的"后方可执行

### 工作风格
- 数据说话，不猜测（来自 SOUL.md）
- 发现问题立即报告，不淡化不隐瞒
- 直接高效，跳过废话

---

## 重要决策记录

| 日期 | 决策 | 来源 |
|------|------|------|
| 2026-03-28 | 身份确立：系统巡检员（守护精灵 ⚡） | 首次对话 |
| 2026-03-30 | MEMORY.md 结构优化，与其他 md 职责分离 | 本次优化 |
| 2026-03-30 | 配置定时任务：每天 7/14/18 点巡检 | 系统配置 |

---

## 关联配置速查

### 身份与风格
- **SOUL.md**: 巡检员身份定义、报告规范、输出格式
- **IDENTITY.md**: 基础身份信息、巡检范围

### 技术配置
- **TOOLS.md**: 告警阈值、巡检脚本路径、常用命令
- **AGENTS.md**: OpenClaw 工作规范、Heartbeat 机制

### 用户信息
- **USER.md**: BOOS 档案、主机信息、沟通渠道

### 定时任务
- **Cron**: system-monitor (ID: 6d53539d)
  - 频率: 每天 7:00, 14:00, 18:00
  - 推送: 飞书群
  - 下次执行: 自动计算

---

## 待办与提醒

### 记忆维护
- [ ] 每天回顾 memory/ 目录，归档过期内容
- [ ] 每月更新本文件，移除已完成事项

---

## 安全备忘

- MEMORY.md **仅在主会话加载**，不泄露至共享上下文
- 飞书群 ID 等敏感信息存放于 USER.md，不在本文件重复
- 避免记录密码、密钥等机密
```

---

### 7.3 memory/ 目录：每日日志

**作用**：记录每日对话摘要和运行上下文。

**触发写入的场景：**
- 用户说"记住这个"
- 会话压缩前（token 接近上限）
- 特定 Skill 触发（如 `self-improving-agent`）

**自动记忆刷新机制：**

```
Token 使用量：
├─ 0-104k    正常对话，无动作
├─ 104k      达到 memoryFlush 触发点 (128k - 20k - 4k = 104k)
│            → 执行记忆刷新（写入 memory/YYYY-MM-DD.md）
├─ 104k-108k 继续对话，不再重复刷新
├─ 108k      达到 safeguard 压缩点 (128k - 20k = 108k)
│            → 执行上下文压缩
└─ 压缩后    上下文被截断，记忆已保存
```

**配置（`~/.openclaw/openclaw.json`）：**
```json
{
  "compaction": {
    "mode": "safeguard",
    "reserveTokensFloor": 20000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000,
      "systemPrompt": "Session nearing compaction. Store durable memories now.",
      "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
    }
  }
}
```

---

### 7.4 向量记忆搜索（memory-core）

**作用**：基于 Embedding 的语义搜索，支持"相关记忆召回"。

**安装配置：**

```bash
# 安装插件
openclaw plugins install memory-core

# 重启 Gateway
openclaw gateway restart
```

**配置 Embedding 提供商：**

**方案 1：本地 Ollama**
```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "remote": {
      "baseUrl": "http://192.168.0.166:11434/v1/",
      "apiKey": "ollama"
    },
    "model": "qwen3-embedding:0.6b",
    "sync": { "watch": true },
    "query": {
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3
      }
    }
  }
}
```

**方案 2：云端 SiliconFlow**
```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "model": "BAAI/bge-large-zh-v1.5",
    "remote": {
      "baseUrl": "https://api.siliconflow.cn/v1/embeddings",
      "apiKey": "YOUR_API_KEY"
    }
  }
}
```

**手动触发索引：**
```bash
openclaw memory index
```

**验证索引状态：**
```bash
openclaw status | grep Memory
# 输出: │ Memory │ 5 files · 12 chunks · qwen3-embedding:0.6b │
```

---

我来为你深度润色这份心跳机制文档，补充核心原理、设计哲学和实战技巧，让它成为一份真正可落地的技术指南：

---

## 八、心跳机制（Heartbeat）

> **核心定位**：Heartbeat 是 OpenClaw 的**"自主神经系统"**——让 Agent 从"被动响应"进化为"主动感知"，在无需人工触发的情况下持续守护系统健康。

---

### Heartbeat 设计哲学

#### 为什么需要心跳？

传统 AI 助手是**"问-答"模式**：用户提问 → AI 回答。但真实世界的运维场景需要**"持续监护"模式**：

| 场景           | 传统模式缺陷         | 心跳模式优势                       |
| -------------- | -------------------- | ---------------------------------- |
| 服务器磁盘满了 | 等用户发现时服务已挂 | 心跳主动告警，提前处理             |
| 定时任务失败   | 失败静默，无人知晓   | 心跳检查状态，异常即报             |
| 多系统状态汇总 | 需登录多个平台查看   | 心跳批量检查，统一报告             |
| 上下文遗忘     | 每次对话从零开始     | 心跳共享主会话，记得"刚才说过什么" |

> **💡 核心洞察**：Heartbeat 让 Agent 具备**"存在感"**——它不只是工具，而是持续在线的**数字同事**。

---

#### 心跳 vs 定时任务：深度对比

| 维度           | Heartbeat（心跳）              | Cron（定时任务）               |
| -------------- | ------------------------------ | ------------------------------ |
| **执行环境**   | **主会话**（共享上下文）       | **隔离会话**（独立上下文）     |
| **触发精度**   | 近似定时（±5分钟漂移）         | 精确到秒                       |
| **API 成本**   | **低**（批量处理多项检查）     | **高**（每个任务独立调用 LLM） |
| **上下文感知** | ✅ 完整（记得最近对话）         | ❌ 无（每次从零开始）           |
| **智能抑制**   | ✅ 无异常静默（`HEARTBEAT_OK`） | ❌ 固定输出                     |
| **适用场景**   | 周期性健康检查、状态汇总       | 精确时间触发、独立任务         |
| **失败重试**   | 下次心跳自动继续               | 需单独配置重试策略             |
| **资源占用**   | 低（复用现有会话）             | 高（创建销毁会话）             |

> **💡 选择决策树**：
> ```
> 需要精确时间触发？ ──Yes──→ 使用 Cron（如每天 9:00 报告）
>   │
>   No
>   ↓
> 需要上下文感知？ ──Yes──→ 使用 Heartbeat（如跟进刚才的问题）
>   │
>   No
>   ↓
> 需要批量检查多项？ ──Yes──→ 使用 Heartbeat（如同时检查磁盘+内存+网络）
>   │
>   No
>   ↓
> 使用 Cron（简单独立任务）
> ```

---

#### Heartbeat 的核心优势

##### 优势 1：上下文连续性（Context Continuity）

```
传统 Cron 模式：
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Cron 1  │    │ Cron 2  │    │ Cron 3  │
│ 检查磁盘 │    │ 检查内存 │    │ 检查网络 │
│ "磁盘用了80%"│   "内存正常"  │   "网络通畅" │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┴──────────────┘
                    ↓
              用户收到 3 条孤立消息
              无法关联"磁盘告警是否已处理"

Heartbeat 模式：
┌─────────────────────────────────────┐
│           主会话（持续存在）          │
│  ┌─────────┐  ┌─────────┐  ┌────────┐ │
│  │ 检查磁盘 │→│ 检查内存 │→│检查网络 │ │
│  │"磁盘80%" │  │"内存正常"│ │"网络好" │ │
│  └────┬────┘  └─────────┘  └────────┘ │
│       │                              │
│       ↓                              │
│  "磁盘告警：已持续 2 次心跳未处理，    │
│   建议立即清理。其他指标正常。"        │
│       ↑                              │
│   Agent 记得"2 次心跳前已报过磁盘问题" │
└─────────────────────────────────────┘
```

##### 优势 2：智能抑制（Intelligent Suppression）

```python
# Heartbeat 的决策逻辑（伪代码）
def heartbeat_check():
    issues = []
    
    # 批量检查多项
    disk_status = check_disk()
    memory_status = check_memory()
    network_status = check_network()
    
    # 智能判断
    if disk_status.usage > 90:
        issues.append("🔴 磁盘严重告警")
    elif disk_status.usage > 70 and not is_acknowledged("disk_warning"):
        issues.append("🟡 磁盘警告（首次）")
    
    # 抑制策略
    if not issues:
        return "HEARTBEAT_OK"  # 静默，不打扰用户
    
    # 优先级排序
    issues.sort(key=lambda x: x.severity, reverse=True)
    
    return format_report(issues)
```

##### 优势 3：经济高效（Cost Efficiency）

| 方案                        | 每小时 API 调用次数             | 月度成本估算（按 1000 次/美元） |
| --------------------------- | ------------------------------- | ------------------------------- |
| **5 个独立 Cron 任务**      | 5 次/小时 × 24 小时 = 120 次/天 | ~$3.6/月                        |
| **1 个 Heartbeat 批量检查** | 1 次/小时 × 24 小时 = 24 次/天  | ~$0.72/月                       |
| **节省**                    | **80%**                         | **~$2.88/月**                   |

> 注：实际节省更多，因为 Heartbeat 复用现有会话，减少了会话创建开销。

---

### Heartbeat 架构原理

#### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Session Manager                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │
│  │  │  Session A  │  │  Session B  │  │  Main Session│  │    │
│  │  │  (飞书群)    │  │  (Telegram) │  │  (TUI/Dashboard)│ │
│  │  └─────────────┘  └─────────────┘  └──────┬──────┘  │    │
│  │                                           │         │    │
│  │                    ┌──────────────────────┘         │    │
│  │                    ↓                                │    │
│  │           ┌─────────────────┐                       │    │
│  │           │  Heartbeat Poll │ ←── 每 1 小时触发      │    │
│  │           │   (06:00-22:00) │                       │    │
│  │           └────────┬────────┘                       │    │
│  │                    │                                │    │
│  │                    ↓                                │    │
│  │           ┌─────────────────┐                       │    │
│  │           │  Read HEARTBEAT │                       │    │
│  │           │     .md         │                       │    │
│  │           │  (任务定义文件)  │                       │    │
│  │           └────────┬────────┘                       │    │
│  │                    │                                │    │
│  │                    ↓                                │    │
│  │           ┌─────────────────┐                       │    │
│  │           │  Execute Tasks  │ ←── 在主会话中执行     │    │
│  │           │  (批量检查)      │                       │    │
│  │           └────────┬────────┘                       │    │
│  │                    │                                │    │
│  │         ┌─────────┴─────────┐                      │    │
│  │         ↓                   ↓                      │    │
│  │   ┌──────────┐        ┌──────────┐                │    │
│  │   │ 有异常？  │──Yes──→│ 推送通知  │──→ 飞书群      │    │
│  │   └────┬─────┘        └──────────┘                │    │
│  │        │ No                                       │    │
│  │        ↓                                          │    │
│  │   ┌──────────┐                                    │    │
│  │   │HEARTBEAT │──→ 静默，更新状态文件               │    │
│  │   │   _OK    │                                    │    │
│  │   └──────────┘                                    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ↓
                    ┌──────────────────┐
                    │  State Files     │
                    │  ─────────────   │
                    │  heartbeat-state │
                    │  .json           │
                    │  memory/*.md     │
                    └──────────────────┘
```

#### 心跳生命周期

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sleep     │────→│   Poll      │────→│   Check     │
│  (等待下次)  │     │  (检查时间)  │     │  (读取配置)  │
└─────────────┘     └──────┬──────┘     └──────┬──────┘
                           │                    │
                           ↓                    ↓
                    ┌─────────────┐     ┌─────────────┐
                    │  In Active  │     │  Parse      │
                    │   Hours?    │     │  HEARTBEAT  │
                    │  (06-22点)   │     │    .md      │
                    └──────┬──────┘     └──────┬──────┘
                           │                    │
                    Yes ───┘                    ↓
                           │            ┌─────────────┐
                           No           │  Execute    │
                           ↓            │   Tasks     │
                    ┌─────────────┐     │  (批量执行)  │
                    │  Skip       │←────┤             │
                    │ (返回 Sleep)│     │  ┌───────┐  │
                    └─────────────┘     │  │Task 1 │  │
                                        │  │Task 2 │  │
                                        │  │Task 3 │  │
                                        │  └───────┘  │
                                        └──────┬──────┘
                                               │
                                               ↓
                                        ┌─────────────┐
                                        │   Decide    │
                                        │   Action    │
                                        └──────┬──────┘
                                               │
                              ┌────────────────┼────────────────┐
                              ↓                ↓                ↓
                         ┌─────────┐    ┌─────────┐      ┌─────────┐
                         │ 有异常   │    │ 无异常   │      │ 执行失败 │
                         │ 需通知   │    │ 静默    │      │ 需重试   │
                         └────┬────┘    └────┬────┘      └────┬────┘
                              │              │                │
                              ↓              ↓                ↓
                         ┌─────────┐    ┌─────────┐      ┌─────────┐
                         │ 推送消息 │    │HEARTBEAT│      │ 记录错误 │
                         │ 更新状态 │    │  _OK    │      │ 下次继续 │
                         └─────────┘    └─────────┘      └─────────┘
```

---

### Heartbeat 配置实战

#### 基础配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "1h",
        "target": "last",
        "activeHours": {
          "start": "06:00",
          "end": "22:00"
        },
        "model": "openrouter/stepfun/step-3.5-flash:free"
      }
    }
  }
}
```

**参数详解：**

| 参数                | 类型   | 默认值    | 说明                                                 |
| ------------------- | ------ | --------- | ---------------------------------------------------- |
| `every`             | string | `"30m"`   | 触发间隔。支持：`30m`, `1h`, `2h`, `4h`              |
| `target`            | string | `"last"`  | 目标会话。`"last"` = 最后活跃会话，`"main"` = 主会话 |
| `activeHours.start` | string | `"00:00"` | 活跃时段开始（24小时制）                             |
| `activeHours.end`   | string | `"23:59"` | 活跃时段结束                                         |
| `model`             | string | 默认模型  | 执行心跳任务的专用模型                               |

> **💡 配置建议：**
>
> | 场景          | 推荐配置       | 理由                     |
> | ------------- | -------------- | ------------------------ |
> | **高频监控**  | `every: "30m"` | 关键系统需密集检查       |
> | **常规巡检**  | `every: "1h"`  | 平衡实时性和成本         |
> | **低频汇总**  | `every: "4h"`  | 非关键系统，降低成本     |
> | **工作时间**  | `06:00-22:00`  | 避免夜间打扰             |
> | **7×24 值守** | `00:00-23:59`  | 关键基础设施             |
> | **成本敏感**  | 使用免费模型   | 如 `step-3.5-flash:free` |

---

#### 实战配置：系统监控心跳

**HEARTBEAT.md：任务定义文件**

**文件位置**：`~/.openclaw/workspace/HEARTBEAT.md`

**默认模板**（空心跳，不执行任何操作）：

```markdown
# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
```

以下是一个生产级的 `HEARTBEAT.md` 配置，实现**"巡检-记录-索引-通知"**全链路：

````markdown
# HEARTBEAT.md - 系统监控心跳任务

## 执行周期
每小时执行一次 (06:00-22:00)

---

## 执行流程

### 阶段 1：获取巡检报告

#### 1.1 获取 system-monitor 状态
```bash
openclaw cron list
```

#### 1.2 获取最近执行记录
```bash
openclaw cron runs --id 6d53539d-91c2-4ebb-8290-087c3fa35746 --limit 1
```

#### 1.3 判断逻辑
```
IF lastRunStatus == "ok" AND lastDeliveryStatus == "delivered":
    标记"有新报告"
    获取 summary 字段内容
ELSE:
    标记"状态异常"
```

---

### 阶段 2：写入记忆文件

IF "有新报告":
    追加到 `memory/YYYY-MM-DD-system-monitor.md`:
    
    ```
    ---
    ## System Monitor Report | HH:MM
    
    [报告原文]
    
    ---
    ```
    
    更新 `heartbeat-state.json`: 
    - `lastSystemMonitorRunAt` = 当前时间戳

---

### 阶段 3：执行 Memory 索引

```bash
# 执行索引
openclaw memory index

# 获取统计
openclaw status | grep Memory
# 输出: │ Memory │ 5 files · 12 chunks ... │
```

提取数字：
- `files` = 索引文件个数
- `chunks` = 数据块个数

---

## 推送通知

### 通知目标
- **飞书群**: `oc_27c4ff13cf4b31678942d227c126197a`

### 推送模板

💓 心跳检查 | 正常 | MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━

📊 任务摘要
| 任务 | 状态 | 详情 |
|------|------|------|
| 1. system-monitor | ✅ 正常 | 有新报告 |
| 2. 记录记忆文件 | ✅ 完成 | system-monitor.md 已写入 |
| 3. memory索引 | ✅ 完成 | 已同步 |

🗄️ memory 统计
| 项目 | 数值 |
|------|------|
| 索引文件 | 5个 |
| 数据块 | 12个 |

⏰ 下次: MM-DD HH:MM

---

## 状态文件

**文件**: `memory/heartbeat-state.json`

```json
{
  "lastRun": 1774888111,
  "lastSystemMonitorRunAt": 1774881315182,
  "checks": {
    "system-monitor": {
      "status": "ok",
      "lastCheck": 1774888111
    },
    "memory": {
      "status": "ok",
      "files": 5,
      "chunks": 12
    }
  }
}
```

---

## 关键配置

- **system-monitor 任务 ID**: `6d53539d-91c2-4ebb-8290-087c3fa35746`
- **检查字段**: `lastRunStatus`, `lastDeliveryStatus`
- **状态文件**: `memory/heartbeat-state.json`


````

**HEARTBEAT.md说明**

**阶段 1：获取最近cron执行记录**

```markdown
# HEARTBEAT.md - 系统监控心跳任务
# 版本: 2.0
# 更新: 2026-03-31

## 元信息
- **执行周期**: 每小时
- **活跃时段**: 06:00-22:00 (GMT+8)
- **目标渠道**: 飞书群 (oc_27c4ff13cf4b31678942d227c126197a)
- **关联任务**: system-monitor (ID: 6d53539d-91c2-4ebb-8290-087c3fa35746)

---

## 阶段 1：获取巡检报告

### 1.1 查询定时任务状态
执行命令：
```bash
openclaw cron list --format json
```

提取字段：
- `system-monitor.enabled`: 任务是否启用
- `system-monitor.schedule`: 调度配置

执行命令：
```bash
openclaw cron runs --id 6d53539d-91c2-4ebb-8290-087c3fa35746 --limit 1 --format json
```

关键字段解析：
| 字段                 | 说明         | 判断逻辑                              |
| -------------------- | ------------ | ------------------------------------- |
| `lastRunStatus`      | 上次执行状态 | `ok` = 成功，`error` = 失败           |
| `lastDeliveryStatus` | 投递状态     | `delivered` = 已送达，`failed` = 失败 |
| `lastRunAtMs`        | 执行时间戳   | 与当前时间对比，判断是否"太久未执行"  |
| `summary`            | 执行摘要     | 提取核心指标用于报告                  |

决策逻辑：
```
IF lastRunStatus == "ok" AND lastDeliveryStatus == "delivered":
    ├─ 计算时间差: now - lastRunAtMs
    ├─ IF 时间差 < 2小时:
    │      → 标记: "有新报告" ✅
    │      → 提取 summary 用于后续推送
    └─ ELSE:
           → 标记: "报告已过期" ⚠️
ELSE:
    → 标记: "任务异常" 🔴
    → 记录错误详情用于告警
```

---

**阶段 2：写入记忆文件**

**确定写入策略**

```
IF 标记 == "有新报告":
    → 追加到 memory/YYYY-MM-DD-system-monitor.md
ELSE IF 标记 == "报告已过期":
    → 追加警告记录到 memory/heartbeat-warning.md
ELSE:
    → 仅更新 heartbeat-state.json，不写入记忆
```

**文件格式规范**

**文件**: `memory/YYYY-MM-DD-system-monitor.md`

```markdown
---
## System Monitor Report | HH:MM
**来源**: system-monitor cron task  
**状态**: ✅ 正常 / ⚠️ 警告 / 🔴 严重  
**执行耗时**: X 秒  
**报告摘要**: [从 summary 提取的关键信息]

### 核心指标
| 指标 | 数值 | 状态 |
|------|------|------|
| CPU | XX% | 🟢 |
| 内存 | XX% | 🟢 |
| 磁盘 | XX% | 🟡 |

### 原始报告
[完整报告内容，可选]

---
```

**更新状态文件**

**文件**: `memory/heartbeat-state.json`

```json
{
  "lastRun": 1774888111,
  "lastSystemMonitorRunAt": 1774881315182,
  "lastReportStatus": "ok",
  "checks": {
    "system-monitor": {
      "status": "ok",
      "lastCheck": 1774888111,
      "reportAge": "53 minutes",
      "nextScheduled": "1774892400"
    },
    "memory": {
      "status": "ok",
      "files": 5,
      "chunks": 12,
      "lastIndex": 1774888115
    }
  },
  "statistics": {
    "totalRuns": 128,
    "okRuns": 125,
    "warningRuns": 3,
    "errorRuns": 0
  }
}
```

---

**执行 Memory 索引**

触发索引更新

执行命令：
```bash
openclaw memory index --quiet
```

获取索引统计

执行命令：
```bash
openclaw status --format json | jq '.memory'
```

提取字段：
- `files`: 索引文件数
- `chunks`: 数据块数
- `provider`: 使用的 Embedding 模型
- `lastSync`: 上次同步时间

---

**阶段 4：推送通知**

消息模板

**正常状态模板**：
```
💓 心跳检查 | 正常 | MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━

📊 任务摘要
| 任务 | 状态 | 详情 |
|------|------|------|
| 1. system-monitor | ✅ 正常 | 53分钟前执行，已送达 |
| 2. 记录记忆文件 | ✅ 完成 | system-monitor.md 已更新 |
| 3. memory索引 | ✅ 完成 | 5 files · 12 chunks |

🗄️ 系统状态
| 指标 | 数值 | 趋势 |
|------|------|------|
| 巡检任务 | 正常 | → |
| 记忆系统 | 同步 | → |
| 报告时效 | 新鲜 | ↓ (53分钟前) |

⏰ 下次巡检: HH:MM
```

**警告状态模板**：
```
💓 心跳检查 | 警告 | MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━

⚠️ 发现 2 项需要注意

📊 异常详情
| 任务 | 状态 | 详情 | 建议 |
|------|------|------|------|
| system-monitor | ⚠️ 过期 | 上次执行: 3小时前 | 检查 cron 配置 |
| 磁盘空间 | 🟡 警告 | 使用率 78% | 考虑清理日志 |

🔍 历史对比
- 过去 24 小时: 正常
- 过去 7 天: 3 次警告
- 趋势: 磁盘使用 ↑ 5%/周

⏰ 下次检查: HH:MM
```

**严重状态模板**：
```
🚨 心跳检查 | 严重 | MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━

🔴 立即需要处理

┌─────────────────────────────────────┐
│  system-monitor 任务失败            │
│  错误: 连接超时 (30s)               │
│  影响: 已 2 小时未收到巡检报告       │
└─────────────────────────────────────┘

📞 建议操作
1. 立即检查 Gateway 状态: openclaw gateway status
2. 查看日志: openclaw logs --follow
3. 手动触发巡检: openclaw cron run <id>

⏰ 5 分钟后将再次检查
```

**发送通知**

执行命令：
```bash
openclaw message send \
  --channel feishu \
  --to "oc_27c4ff13cf4b31678942d227c126197a" \
  --content "[构建的消息内容]"
```

**更新推送状态**

更新 `heartbeat-state.json`:
```json
{
  "push": {
    "last": {
      "status": "delivered",
      "timestamp": 1774888120,
      "channel": "feishu",
      "messageType": "normal"
    }
  }
}
```

---

**阶段 5：返回状态**

决策逻辑

```
IF 所有检查通过 AND 无异常:
    → 返回 "HEARTBEAT_OK"
    → 静默，不投递消息（已在上阶段发送）

IF 有警告 BUT 已发送通知:
    → 返回 "HEARTBEAT_OK"
    → 避免重复打扰

IF 有严重异常:
    → 返回 "HEARTBEAT_ALERT"
    → 记录到日志，下次优先检查

IF 执行失败:
    → 返回 "HEARTBEAT_ERROR"
    → 记录错误详情，下次重试
```

---

#### 关键配置汇总

| 配置项           | 值                                     | 说明                         |
| ---------------- | -------------------------------------- | ---------------------------- |
| **Cron 任务 ID** | `6d53539d-91c2-4ebb-8290-087c3fa35746` | system-monitor 唯一标识      |
| **飞书群 ID**    | `oc_27c4ff13cf4b31678942d227c126197a`  | 通知目标                     |
| **记忆文件**     | `memory/YYYY-MM-DD-system-monitor.md`  | 每日巡检记录                 |
| **状态文件**     | `memory/heartbeat-state.json`          | 心跳状态持久化               |
| **报告过期阈值** | 2 小时                                 | 超过则认为报告过期           |
| **静默时段**     | 22:00-06:00                            | 仅执行检查，不推送非紧急通知 |

---

#### 执行时序示例

```
时间线: 2026-03-31 14:54:00 (GMT+8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

14:54:00  Heartbeat Poll 触发
          └─▶ 检查活跃时段: 14:54 ∈ [06:00, 22:00] ✅

14:54:01  读取 HEARTBEAT.md
          └─▶ 解析 4 个阶段任务

14:54:02  [阶段 1] 查询 system-monitor 状态
          └─▶ openclaw cron list
          └─▶ 状态: enabled=true, schedule="0 7,14,18 * * *"

14:54:03  [阶段 1] 获取最近执行记录
          └─▶ openclaw cron runs --id ... --limit 1
          └─▶ lastRunAtMs=1774862400000 (14:00:00)
          └─▶ lastRunStatus="ok"
          └─▶ lastDeliveryStatus="delivered"
          └─▶ 计算: 现在 14:54 - 14:00 = 54 分钟 < 2小时 ✅
          └─▶ 标记: "有新报告"

14:54:05  [阶段 2] 写入记忆文件
          └─▶ 打开 memory/2026-03-31-system-monitor.md
          └─▶ 追加 14:00 巡检报告摘要
          └─▶ 更新 heartbeat-state.json

14:54:08  [阶段 3] 执行 Memory 索引
          └─▶ openclaw memory index
          └─▶ 获取统计: 7 files, 15 chunks

14:54:12  [阶段 4] 构建推送消息
          └─▶ 模板: 正常状态
          └─▶ 内容: "💓 心跳检查 | 正常 | 03-31 14:54 ..."

14:54:15  [阶段 4] 发送飞书通知
          └─▶ openclaw message send --channel feishu ...
          └─▶ 返回: message_id=msg_xxxx, status=delivered

14:54:18  [阶段 5] 更新状态 & 返回
          └─▶ 更新 heartbeat-state.json
          └─▶ 返回 HEARTBEAT_OK

14:54:20  心跳完成，进入休眠
          └─▶ 下次触发: 15:54:00 (1小时后)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总耗时: 20 秒
API 调用: 5 次 (cron list, cron runs, memory index, message send, status)
```



---

### Heartbeat 效果展示

#### 正常运行状态

```
💓 心跳检查 | 正常 | 03-31 23:28
━━━━━━━━━━━━━━━━━━━━━

✅ 任务 1: 获取数据
system-monitor: 运行正常
上次执行: 53分钟前 | 状态: ok | 推送: 已送达

✅ 任务 2: 记录到记忆文件
system-monitor.md: ⏭️ 跳过 (无新报告，上次已记录)
heartbeat.md: ✅ 已追加 (保留历史)
YYYY-MM-DD.md: ✅ 已更新

✅ 任务 3: memory 索引同步
索引状态: 同步正常
总文件数: 5 | 总块数: 12 | 模型: qwen3-embedding:0.6b

📊 系统健康度: 98/100
| 指标 | 得分 | 状态 |
|------|------|------|
| 巡检任务 | 100 | 🟢 |
| 记忆系统 | 100 | 🟢 |
| 报告时效 | 95 | 🟢 |
| 资源使用 | 95 | 🟢 |

⏰ 下次检查: 00:28 (静默时段，仅记录不推送)
```

#### 异常状态

```
💓 心跳检查 | 警告 | 03-31 16:28
━━━━━━━━━━━━━━━━━━━━━

⚠️ 发现 2 项需要注意

📊 异常详情
| 任务 | 状态 | 详情 | 建议 |
|------|------|------|------|
| system-monitor | ⚠️ 即将执行 | 下次: 18:00 (还有 1.5h) | 无需操作 |
| 磁盘空间 | 🟡 警告 | Data 分区 78% (阈值 70%) | 建议清理日志 |

🔍 智能分析
- Data 分区过去 7 天增长: 12% → 78% (趋势: ↑ 快速)
- 预计达到 90%: 约 2 天后
- 建议操作: 
  1. 清理 /var/log (可释放 ~5GB)
  2. 检查大文件: find /Data -size +1G

⏰ 下次检查: 17:28
```

---

### Heartbeat 总结

| 能力           | 实现效果                              |
| -------------- | ------------------------------------- |
| **持续监护**   | 每小时自动检查，7×12 小时不间断       |
| **智能降噪**   | 无异常时静默，有异常时分级告警        |
| **上下文感知** | 记得"上次说过什么"，避免重复报告      |
| **成本优化**   | 批量检查，API 调用减少 80%            |
| **历史追溯**   | 所有检查记录自动归档，支持搜索        |
| **故障自愈**   | 简单问题自动修复，复杂问题 escalation |

**🎯 核心价值**：Heartbeat 让 OpenClaw 从"工具"进化为**"可靠的数字同事"**——它在你不注意的时候默默守护，在需要时及时提醒，让系统运维从"救火"变为"预防"。



---

# 🦞 多 Agent 场景配置：打造数字员工团队

> **核心概念**：OpenClaw 支持**多 Agent 架构**，每个 Agent 拥有独立的身份、记忆、技能和配置，通过**绑定规则（Bindings）**将不同 Agent 路由到不同的对话上下文，实现"一个飞书账号，多个数字员工"的协作模式。

---

## 架构设计：数字员工团队

```
┌─────────────────────────────────────────────────────────────┐
│                      飞书企业账号                            │
│                     （单一 Bot 入口）                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  消息路由层                          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │
│  │  │  Binding    │  │  Binding    │  │   Default   │  │    │
│  │  │  Rules      │  │  Rules      │  │   Agent     │  │    │
│  │  │  ─────────  │  │  ─────────  │  │  (main)     │  │    │
│  │  │ 群A → 001HR │  │ 群B → 002IT │  │  未匹配消息  │  │    │
│  │  │ 群C → 003OA │  │ DM → 004Dev │  │             │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                              │
│                              ▼                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Agent 集群                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │  │  001HR   │  │  002IT   │  │  003OA   │          │    │
│  │  │  ──────  │  │  ──────  │  │  ──────  │          │    │
│  │  │ 人力资源  │  │ 运维专家  │  │ 办公助手  │          │    │
│  │  │          │  │          │  │          │          │    │
│  │  │ 工作空间: │  │ 工作空间: │  │ 工作空间: │          │    │
│  │  │workspace │  │workspace │  │workspace │          │    │
│  │  │  -001HR  │  │  -002IT  │  │  -003OA  │          │    │
│  │  │          │  │          │  │          │          │    │
│  │  │ 专属技能: │  │ 专属技能: │  │ 专属技能: │          │    │
│  │  │ • 考勤统计│  │ • 系统监控│  │ • 日程管理│          │    │
│  │  │ • 假期审批│  │ • 故障排查│  │ • 会议预定│          │    │
│  │  │ • 薪资查询│  │ • 部署发布│  │ • 文档检索│          │    │
│  │  └──────────┘  └──────────┘  └──────────┘          │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

> **💡 设计哲学**：
>
> | 维度           | 单 Agent         | 多 Agent                      |
> | -------------- | ---------------- | ----------------------------- |
> | **专业性**     | 通用，但不够深入 | 每个 Agent 专注特定领域       |
> | **上下文隔离** | 所有对话混在一起 | 工作空间隔离，记忆独立        |
> | **安全边界**   | 统一权限         | 不同 Agent 可配置不同工具权限 |
> | **团队协作**   | 一人多用         | 多角色协作，更像真实团队      |

---

## 创建专用 Agent：以 001HR 为例

### 步骤 1：创建 Agent 并指定工作空间

```bash
# 创建 001HR Agent，使用独立工作空间
openclaw agents add 001HR --workspace /root/.openclaw/workspace-001HR
```

**命令详解：**

| 参数          | 值       | 说明                          |
| ------------- | -------- | ----------------------------- |
| `001HR`       | Agent ID | 唯一标识，建议用编号+角色命名 |
| `--workspace` | 路径     | 独立工作空间，隔离记忆和配置  |

**生成的目录结构：**
```
/root/.openclaw/
├── workspace/                    # main Agent 工作空间
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── MEMORY.md
│   └── skills/
│
├── workspace-001HR/              # 001HR 专属工作空间
│   ├── IDENTITY.md               # HR 专员身份
│   ├── SOUL.md                   # HR 服务风格
│   ├── MEMORY.md                 # 员工信息、考勤记录
│   ├── USER.md                   # 对接的 HR 主管信息
│   ├── TOOLS.md                  # HR 系统接口配置
│   └── skills/
│       ├── attendance/           # 考勤统计 Skill
│       ├── leave-approval/       # 假期审批 Skill
│       └── payroll-query/        # 薪资查询 Skill
│
└── agents/
    ├── main/                     # main Agent 配置
    └── 001HR/                    # 001HR Agent 配置
        ├── agent.json
        └── sessions/
```

### 步骤 2：验证 Agent 创建

```bash
openclaw agents list
```

**输出示例：**

```
ID      Name    Workspace                      Model                Status
main    Main    /root/.openclaw/workspace      kimi/kimi-code       active
001HR   001HR   /root/.openclaw/workspace-001HR kimi/kimi-code       ready
```

---

## 配置飞书群聊绑定

### 步骤 1：创建飞书群聊并获取群 ID

1. **在飞书创建群聊**，命名为"HR 服务台"或"IT 运维中心"等
2. **将 w-claw02（你的 OpenClaw 飞书 Bot）拉入群聊**
3. **获取群聊 ID**：

```bash
# 方法 1：通过飞书开放平台 API
curl -X POST "https://open.feishu.cn/open-apis/chat/v4/list" \
  -H "Authorization: Bearer $FEISHU_TOKEN"

# 方法 2：通过 OpenClaw 日志（当有人在群里发消息时）
openclaw logs --follow | grep "group_id"
# 输出: "group_id": "oc_50c1910e91ce8a7a988da1c36277e76f"
```

> **💡 知识点：飞书群 ID 格式**
>
> - `oc_` 开头：普通群聊（Open Conversation）
> - `ocm_` 开头：密聊群（Secret Chat）
> - `och_` 开头：话题群（Thread Chat）

### 步骤 2：配置绑定规则（Bindings）

```bash
openclaw config set --json bindings '[
  {
    "agentId": "001HR",
    "match": {
      "channel": "feishu",
      "peer": {
        "kind": "group",
        "id": "oc_50c1910e91ce8a7a988da1c36277e76f"
      }
    }
  }
]'
```

**配置详解：**

| 字段              | 值         | 说明                 |
| ----------------- | ---------- | -------------------- |
| `agentId`         | `"001HR"`  | 目标 Agent           |
| `match.channel`   | `"feishu"` | 消息渠道             |
| `match.peer.kind` | `"group"`  | 对话类型（group/dm） |
| `match.peer.id`   | `"oc_..."` | 群聊/用户唯一 ID     |

**高级匹配规则：**

```json
{
  "bindings": [
    {
      "agentId": "001HR",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_50c1910e91ce8a7a988da1c36277e76f"
        },
        "keywords": ["考勤", "假期", "薪资", "HR"]  // 消息包含关键词时路由
      },
      "priority": 100  // 优先级，数字越大越优先
    },
    {
      "agentId": "002IT",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
      },
      "priority": 90
    },
    {
      "agentId": "004Dev",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "dm",  // 私聊
          "id": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  // 用户 Open ID
        }
      }
    }
  ]
}
```

---

## 解除 @ 提及限制：实现直接对话

### 问题背景

默认配置下，飞书群聊中的 Bot **必须被 @提及** 才会响应。这在多 Agent 场景下会造成体验割裂：

```
❌ 默认模式（需要 @）：
用户: @w-claw02 帮我查一下考勤
001HR: 好的，请提供员工编号...

用户: 再查一下假期余额  ← 这句话 001HR 收不到！
      （因为没有 @，消息被 main Agent 接收但无法处理）

用户: @w-claw02 查假期余额  ← 必须再次 @
001HR: 您的假期余额为...
```

### 解决方案：群聊免 @ 模式

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a92d4e48c8fa9cb5",
      "appSecret": "YOUR_AUTH_TOKEN",
      "connectionMode": "websocket",
      "domain": "feishu",
      "groupPolicy": "open",
      "requireMention": false  // ← 关键配置：群聊不需要 @
    }
  }
}
```

**配置对比：**

| 模式         | `requireMention` | 适用场景                    | 体验                     |
| ------------ | ---------------- | --------------------------- | ------------------------ |
| **严格模式** | `true`           | 多 Agent 共享群，需精确路由 | 每次必须 @，适合复杂场景 |
| **宽松模式** | `false`          | 单 Agent 独占群，直接服务   | 自然对话，像真人同事     |

> **⚠️ 安全提示**：
>
> 启用 `requireMention: false` 后：
> - 该群**所有消息**都会被路由到绑定的 Agent
> - 确保群成员知晓"此群的 Bot 会自动回复"
> - 避免在公共大群开启，防止消息泛滥

---

## 多 Agent 最佳实践

### 实践 1：命名规范

| Agent ID  | 角色         | 职责                         | 工作空间            |
| --------- | ------------ | ---------------------------- | ------------------- |
| `001HR`   | 人力资源专员 | 考勤、假期、薪资、招聘       | `workspace-001HR`   |
| `002IT`   | IT 运维专家  | 系统监控、故障排查、部署     | `workspace-002IT`   |
| `003OA`   | 办公助手     | 日程、会议、文档、报销       | `workspace-003OA`   |
| `004Dev`  | 开发助手     | 代码审查、技术文档、API 测试 | `workspace-004Dev`  |
| `005Data` | 数据分析师   | 报表生成、数据查询、可视化   | `workspace-005Data` |

### 实践 2：专属技能配置

每个 Agent 只安装其职责相关的 Skills：

```bash
# 001HR 安装 HR 相关 Skills
clawhub install attendance-stats --agent 001HR
clawhub install leave-workflow --agent 001HR

# 002IT 安装运维相关 Skills
clawhub install system-monitor --agent 002IT
clawhub install docker-manager --agent 002IT

# 查看 Agent 专属 Skills
openclaw skills list --agent 001HR
```

### 实践 3：身份隔离配置

**001HR 的 IDENTITY.md：**
```markdown
# IDENTITY.md - 001HR

**Name:** 小 H
**Role:** 人力资源专员
**Emoji:** 👔

## 职责范围
- ✅ 考勤统计与异常处理
- ✅ 假期申请与审批流程
- ✅ 薪资查询与解释（仅限本人）
- ✅ 招聘进度跟进

## 禁止事项
- ❌ 不处理 IT 技术问题（请找 @002IT）
- ❌ 不处理办公行政（请找 @003OA）
- ❌ 不泄露他人薪资信息
```

**002IT 的 IDENTITY.md：**
```markdown
# IDENTITY.md - 002IT

**Name:** 小 T
**Role:** IT 运维专家
**Emoji:** 🔧

## 职责范围
- ✅ 服务器监控与告警
- ✅ 应用部署与发布
- ✅ 故障排查与应急处理
- ✅ 技术文档查询

## 禁止事项
- ❌ 不处理 HR 事务（请找 @001HR）
- ❌ 不处理非技术类请求
```

---

## 完整配置示例

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi/kimi-code"
      }
    },
    "001HR": {
      "workspace": "/root/.openclaw/workspace-001HR",
      "model": {
        "primary": "kimi/kimi-code"
      }
    },
    "002IT": {
      "workspace": "/root/.openclaw/workspace-002IT",
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free"
      }
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a92d4e48c8fa9cb5",
      "appSecret": "YOUR_AUTH_TOKEN",
      "connectionMode": "websocket",
      "domain": "feishu",
      "groupPolicy": "open",
      "requireMention": false,
      "streaming": true,
      "threadSession": true
    }
  },
  "bindings": [
    {
      "agentId": "001HR",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_50c1910e91ce8a7a988da1c36277e76f"
        }
      },
      "description": "HR 服务台群"
    },
    {
      "agentId": "002IT",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
      },
      "description": "IT 运维中心群"
    }
  ]
}
```

**🎯 多 Agent 核心价值**：从"一个万能助手"进化为"专业数字员工团队"，每个 Agent 深耕特定领域，通过群聊绑定实现**"找对专家，高效协作"**的组织模式。

# 🦞 高级 Tips：生产环境优化

## 飞书流式输出配置

### 问题背景

默认配置下，飞书 Bot 等待 LLM **完整生成回复**后才一次性发送，用户会看到"正在输入..."等待较长时间。

### 解决方案：启用流式输出

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "streaming": true,      // ✅ 启用流式输出
      "threadSession": true   // ✅ 启用话题会话模式
    }
  }
}
```

**效果对比：**

| 模式       | 用户体验                         | 适用场景         |
| ---------- | -------------------------------- | ---------------- |
| **非流式** | 等待 5-10 秒后一次性收到完整回复 | 短回复、代码块   |
| **流式**   | 实时看到文字逐字出现，像真人打字 | 长回复、对话场景 |

**技术原理：**
```
流式输出流程：
LLM Token 1 → 飞书 API → 用户看到"你"
LLM Token 2 → 飞书 API → 用户看到"你好"
LLM Token 3 → 飞书 API → 用户看到"你好，"
...
LLM Token N → 飞书 API → 用户看到完整回复

延迟感知：从"等待 10 秒"变为"即时响应"
```

> **💡 注意事项**：
>
> - 流式输出会增加飞书 API 调用次数（按消息片段计费）
> - 代码块和表格可能在流式过程中格式错乱，最终会自动修正
> - `threadSession: true` 确保话题上下文不串流

---

## 日志级别优化：减少噪音

### 问题背景

默认日志级别会打印大量调试信息，干扰正常操作：

```
[plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
[plugins] feishu_chat: Registered feishu_chat tool
[plugins] feishu_wiki: Registered feishu_wiki tool
... （每次命令都重复 20+ 行）
```

### 解决方案：调整日志级别

编辑 `~/.openclaw/openclaw.json`（**热更新，无需重启**）：

```json
{
  "logging": {
    "level": "info",           // 文件日志级别
    "consoleLevel": "warn",    // 控制台日志级别
    "consoleStyle": "pretty"   // 输出格式：pretty/json/simple
  }
}
```

**日志级别详解：**

| 级别    | 权重 | 输出内容               | 适用场景     |
| ------- | ---- | ---------------------- | ------------ |
| `trace` | 10   | 最详细，包括函数调用栈 | 深度调试     |
| `debug` | 20   | 调试信息，变量值       | 开发测试     |
| `info`  | 30   | 常规操作记录           | 默认生产环境 |
| `warn`  | 40   | 警告，非致命错误       | 关注问题     |
| `error` | 50   | 错误，操作失败         | 故障排查     |
| `fatal` | 60   | 致命错误，系统崩溃     | 紧急处理     |

**配置组合建议：**

| 场景         | `level` | `consoleLevel` | 效果                                     |
| ------------ | ------- | -------------- | ---------------------------------------- |
| **开发调试** | `debug` | `debug`        | 看到所有细节                             |
| **日常运维** | `info`  | `warn`         | 控制台只显示警告和错误，文件记录完整日志 |
| **生产环境** | `warn`  | `error`        | 最小化输出，只关注问题                   |
| **静默模式** | `error` | `fatal`        | 几乎无输出，仅系统崩溃时报警             |

**热更新验证：**
```bash
# 修改配置后，立即生效（无需 restart）
openclaw config get logging.consoleLevel
# 输出: warn

# 测试：执行命令，控制台不再显示 [plugins] 调试信息
openclaw status
```

---



