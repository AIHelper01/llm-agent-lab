# OpenClaw（小龙虾）安装一页纸

---

## 部署前准备

### 系统要求 
| 项目         | 要求                                                  |
| ------------ | ----------------------------------------------------- |
| **操作系统** | Windows 11 / macOS 12+ / Linux (Ubuntu/Debian/CentOS) |
| **Node.js**  | 版本 22.x 或 24.x（推荐 24）                          |
| **内存**     | 至少 2GB（建议 8GB 以上）                             |
| **磁盘空间** | 预留 2.5GB 以上                                       |
| **网络**     | 可访问外网（用于下载依赖）                            |

### 环境检查
```bash
node -v    # 检查 Node.js 版本
npm -v     # 检查 npm 版本
```

假设未安装，出现如下提示： 
```
(base) root@will-Ubuntu:~# node -v
找不到命令 “node”，但可以通过以下软件包安装它：
apt install nodejs
(base) root@will-Ubuntu:~# npm -v
找不到命令 “npm”，但可以通过以下软件包安装它：
apt install npm
(base) root@will-Ubuntu:~#

```
先完成安装：
```
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


---

## 安装方式

### npm 全局安装 （推荐）

```bash
# 配置国内镜像（可选，加速下载）
npm config set registry https://registry.npmmirror.com

# 全局安装
npm install -g openclaw@latest
```

Ubuntu上示例： 

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

**Windows 用户额外步骤** ：

```powershell
# 以管理员身份运行 PowerShell，先安装 Node.js
winget install OpenJS.NodeJS.LTS -e --source winget

# 安装 PM2 进程管理工具（用于后台运行）
npm install -g pm2
```

---



其他方法：

- 官方一键安装脚本
- Docker 部署（适合云服务器/VPS）
- 源码编译（开发者/高级用户）



### 升级

更新（全局安装）：

```
npm i -g openclaw@latest
```



### 卸载

使用内置卸载程序：

```
openclaw uninstall
```

---





## Channel准备（Feishu）



> 参考官网： https://docs.openclaw.ai/channels/feishu

OpenClaw 可以在你已经使用的任何聊天应用上与你交流。每个渠道通过 Gateway 网关连接。 所有渠道都支持文本；媒体和表情回应的支持因渠道而异。

支持的消息平台：

- BlueBubbles
- Discord
- 飞书
- grammY
- Google Chat
- iMessage
- LINE
- Matrix
- Mattermost
- Microsoft Teams
- Nextcloud Talk
- Nostr
- Signal
- Slack
- Telegram
- Tlon
- Twitch
- WhatsApp
- Zalo
- Zalo Personal



这里以飞书为例

## 初始化配置

运行安装后，系统会自动或手动启动配置向导：

```bash
openclaw onboard --install-daemon
```

**配置步骤：**关键步骤总结：

1. **初始化与安全确认**

- 运行 `openclaw onboard --install-daemon` 启动安装向导
- 阅读并接受安全警告（个人使用默认边界，多用户需加固）
- 选择 **QuickStart** 模式

2. **模型配置**

- 选择 **Kimi Code** 作为模型提供商
- 输入 API Key：`YOUR_API_KEY`
- 默认模型设置为 `kimi/kimi-code`

3. **消息通道配置**（选择 Feishu/飞书）

- **App ID**: `cli_a94dae300938dbc8`
- **App Secret**: `S6FG0NVRGzQ8kievOGccKfop7qKiG62f`
- 连接模式：**WebSocket**
- 域名：**feishu.cn**（中国版）
- 群聊策略：**Open**（所有群聊中需 @ 提及才响应）

4. **工具与技能配置**

- **Web 搜索**: 选择 Tavily（但未提供 API Key，暂不可用）
- **技能**: 尝试安装 `summarize` 失败（缺少 Homebrew）
- 跳过了其他 API 配置（Google Places、Notion、OpenAI Whisper、ElevenLabs）

5. **自动化钩子**（Hooks）

启用 4 个默认钩子：
- `boot-md`（启动 Markdown）
- `bootstrap-extra-files`（额外文件引导）
- `command-logger`（命令日志）
- `session-memory`（会话记忆）

6. **服务部署**

- 安装 **systemd 用户服务**: `~/.config/systemd/user/openclaw-gateway.service`
- Gateway 地址：`127.0.0.1:18789`
- 控制面板：http://127.0.0.1:18789/

7. **首次启动**（TUI）

- 通过 `openclaw tui` 启动终端交互界面

- 发送唤醒消息："Wake up, my friend!"

- 用户定义了 Agent 身份：
  1. **名字**: Will
  2. **角色**: 人工智能助手
  3. **风格**: 专业
  4. **Emoji**: 随机
  
8. **当前状态**
Agent 已就绪，等待指令。

---



**配置示例** ：

```bash
(base) root@will-Ubuntu:~# openclaw onboard --install-daemon

🦞 OpenClaw 2026.3.24 (cff6dc9) — Say "stop" and I'll stop—say "ship" and we'll both learn a lesson.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞

┌  OpenClaw setup
│
◇  Security ─────────────────────────────────────────────────────────────────────────────────╮
│                                                                                            │
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
│  If you’re not comfortable with security hardening and access control, don’t run           │
│  OpenClaw.                                                                                 │
│  Ask someone experienced to help before enabling tools or exposing it to the internet.     │
│                                                                                            │
│  Recommended baseline:                                                                     │
│  - Pairing/allowlists + mention gating.                                                    │
│  - Multi-user/shared inbox: split trust boundaries (separate gateway/credentials, ideally  │
│    separate OS users/hosts).                                                               │
│  - Sandbox + least-privilege tools.                                                        │
│  - Shared inboxes: isolate DM sessions (`session.dmScope: per-channel-peer`) and keep      │
│    tool access minimal.                                                                    │
│  - Keep secrets out of the agent’s reachable filesystem.                                   │
│  - Use the strongest available model for any bot with tools or untrusted inboxes.          │
│                                                                                            │
│  Run regularly:                                                                            │
│  openclaw security audit --deep                                                            │
│  openclaw security audit --fix                                                             │
│                                                                                            │
│  Must read: https://docs.openclaw.ai/gateway/security                                      │
│                                                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────╯
│
◇  I understand this is personal-by-default and shared/multi-user use requires lock-down. Continue?
│  Yes
│
◇  Setup mode
│  QuickStart
│
◇  QuickStart ─────────────────────────╮
│                                      │
│  Gateway port: 18789                 │
│  Gateway bind: Loopback (127.0.0.1)  │
│  Gateway auth: Token (default)       │
│  Tailscale exposure: Off             │
│  Direct to chat channels.            │
│                                      │
├──────────────────────────────────────╯
│
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
│
◇  Default model
│  Keep current (kimi/kimi-code)
│
◇  Channel status ───────────────────╮
│                                    │
│  Telegram: needs token             │
│  Discord: needs token              │
│  IRC: needs host + nick            │
│  Slack: needs tokens               │
│  Signal: needs setup               │
│  signal-cli: missing (signal-cli)  │
│  iMessage: needs setup             │
│  imsg: missing (imsg)              │
│  LINE: needs token + secret        │
│  Accounts: 0                       │
│  WhatsApp: not configured          │
│  Google Chat: not configured       │
│  Feishu: installed                 │
│  Google Chat: installed            │
│  Nostr: installed                  │
│  Microsoft Teams: installed        │
│  Mattermost: installed             │
│  Nextcloud Talk: installed         │
│  Matrix: installed                 │
│  BlueBubbles: installed            │
│  Zalo: installed                   │
│  Zalo Personal: installed          │
│  Synology Chat: installed          │
│  Tlon: installed                   │
│  Twitch: installed                 │
│  WhatsApp: installed               │
│                                    │
├────────────────────────────────────╯
│
◇  How channels work ───────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│  DM security: default is pairing; unknown DMs get a pairing code.                         │
│  Approve with: openclaw pairing approve <channel> <code>                                  │
│  Public DMs require dmPolicy="open" + allowFrom=["*"].                                    │
│  Multi-user DMs: run: openclaw config set session.dmScope "per-channel-peer" (or          │
│  "per-account-channel-peer" for multi-account channels) to isolate sessions.              │
│  Docs: channels/pairing              │
│                                                                                           │
│  Telegram: simplest way to get started — register a bot with @BotFather and get going.    │
│  WhatsApp: works with your own number; recommend a separate phone + eSIM.                 │
│  Discord: very well supported right now.                                                  │
│  IRC: classic IRC networks with DM/channel routing and pairing controls.                  │
│  Google Chat: Google Workspace Chat app with HTTP webhook.                                │
│  Slack: supported (Socket Mode).                                                          │
│  Signal: signal-cli linked device; more setup (David Reagans: "Hop on Discord.").         │
│  iMessage: this is still a work in progress.                                              │
│  LINE: LINE Messaging API webhook bot.                                                    │
│  Feishu: 飞书/Lark enterprise messaging with doc/wiki/drive tools.                        │
│  Nostr: Decentralized protocol; encrypted DMs via NIP-04.                                 │
│  Microsoft Teams: Teams SDK; enterprise support.                                          │
│  Mattermost: self-hosted Slack-style chat; install the plugin to enable.                  │
│  Nextcloud Talk: Self-hosted chat via Nextcloud Talk webhook bots.                        │
│  Matrix: open protocol; install the plugin to enable.                                     │
│  BlueBubbles: iMessage via the BlueBubbles mac app + REST API.                            │
│  Zalo: Vietnam-focused messaging platform with Bot API.                                   │
│  Zalo Personal: Zalo personal account via QR code login.                                  │
│  Synology Chat: Connect your Synology NAS Chat to OpenClaw with full agent capabilities.  │
│  Tlon: decentralized messaging on Urbit; install the plugin to enable.                    │
│  Twitch: Twitch chat integration                                                          │
│                                                                                           │
├───────────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Select channel (QuickStart)
│  Feishu/Lark (飞书)
│
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
◇  How do you want to provide this App Secret?
│  Enter App Secret
│
◇  Enter Feishu App Secret
│  S6FG0NVRGzQ8kievOGccKfop7qKiG62f
│
◇  Enter Feishu App ID
│  cli_a94dae300938dbc8
[info]: [ 'client ready' ]
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
│
◇  Selected channels ──────────────────────────────────────────╮
│                                                              │
│  Feishu — 飞书/Lark enterprise messaging. Docs:              │
│  feishu  │
│                                                              │
├──────────────────────────────────────────────────────────────╯
Updated ~/.openclaw/openclaw.json
Workspace OK: ~/.openclaw/workspace
Sessions OK: ~/.openclaw/agents/main/sessions
│
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
│
│
◇  Web search ─────────────────────────────────────────────────────────────────╮
│                                                                              │
│  No Tavily API key stored — web_search won't work until a key is available.  │
│  Get your key at: https://tavily.com/                                        │
│  Docs: https://docs.openclaw.ai/tools/web                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────╯
│
◇  Skills status ─────────────╮
│                             │
│  Eligible: 5                │
│  Missing requirements: 38   │
│  Unsupported on this OS: 7  │
│  Blocked by allowlist: 0    │
│                             │
├─────────────────────────────╯
│
◇  Configure skills now? (recommended)
│  Yes
│
◇  Install missing skill dependencies
│  🧾 summarize
│
◇  Homebrew recommended ──────────────────────────────────────────────────────────╮
│                                                                                 │
│  Many skill dependencies are shipped via Homebrew.                              │
│  Without brew, you'll need to build from source or download releases manually.  │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────╯
│
◇  Show Homebrew install command?
│  Yes
│
◇  Homebrew install ─────────────────────────────────────────────────────╮
│                                                                        │
│  Run:                                                                  │
│  /bin/bash -c "$(curl -fsSL                                            │
│  https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  │
│                                                                        │
├────────────────────────────────────────────────────────────────────────╯
│
◇  Install failed: summarize — brew not installed — Homebrew is not installed. Install it from https://brew.sh or install "steipete/tap/summarize" manually using your sys…
Tip: run `openclaw doctor` to review skills + requirements.
Docs: https://docs.openclaw.ai/skills
│
◇  Set GOOGLE_PLACES_API_KEY for goplaces?
│  No
│
◇  Set NOTION_API_KEY for notion?
│  No
│
◇  Set OPENAI_API_KEY for openai-whisper-api?
│  No
│
◇  Set ELEVENLABS_API_KEY for sag?
│  No
│
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
Config overwrite: /root/.openclaw/openclaw.json (sha256 b5d4a30b8395e33079139ddcdd797bfe90d0a699ef91afae16df911256436cdc -> f3ae464658094475fa51e0942b7e202cb18547c7c497bce7a6ab48f8827e3b5c, backup=/root/.openclaw/openclaw.json.bak)
│
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
◇
Feishu: ok
Agents: main (default)
Heartbeat interval: 30m (main)
Session store (main): /root/.openclaw/agents/main/sessions/sessions.json (0 entries)
│
◇  Optional apps ────────────────────────╮
│                                        │
│  Add nodes for extra features:         │
│  - macOS app (system + notifications)  │
│  - iOS app (camera/canvas)             │
│  - Android app (camera/canvas)         │
│                                        │
├────────────────────────────────────────╯
│
◇  Control UI ─────────────────────────────────────────────────────────────────────╮
│                                                                                  │
│  Web UI: http://127.0.0.1:18789/                                                 │
│  Web UI (with token):                                                            │
│  http://127.0.0.1:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f  │
│  Gateway WS: ws://127.0.0.1:18789                                                │
│  Gateway: reachable                                                              │
│  Docs: https://docs.openclaw.ai/web/control-ui                                   │
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
│  Web UI keeps dashboard URL tokens in memory for the current tab and strips them from the  │
│  URL after load.                                                                           │
│  Open the dashboard anytime: openclaw dashboard --no-open                                  │
│  If prompted: paste the token into Control UI settings (or use the tokenized dashboard     │
│  URL).                                                                                     │
│                                                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────╯
│
◇  How do you want to hatch your bot?
│  Hatch in TUI (recommended)
 openclaw tui - ws://127.0.0.1:18789 - agent main - session main

 session agent:main:main


 Wake up, my friend!


 Hey! Good to see you. ☕

 Let me get my bearings and check what we've got going on.Looks like this is a fresh start — no memory files
 yet, no MEMORY.md. Just the base template files.

 So... here I am, awake! 🤖✨

 Since we're starting from scratch, maybe we should figure out who I am? BOOTSTRAP.md says I should ask:

 1. What should I call myself? Got a name in mind for me?
 2. What kind of "creature" am I? AI assistant, digital companion, something weirder?
 3. What's my vibe? Snarky? Warm? Chill? Professional?
 4. Emoji signature — gotta have one of those.

 Or if you've already got preferences locked in, just tell me and I'll update my files.

 What's the plan?


 1.Will 2.人工智能助手 3.专业 4.随机一个吧


 Alright, getting myself set up. Let me write this down:Good start. Now let me set up my identity:Now let me
 update my soul with professional vibes:Perfect. Let me finish up by removing the bootstrap file and
 creating a proper MEMORY.md:Done! Here's what I've set up:

 My identity:
 - ⚡ Professional AI assistant
 - Working with Will (GMT+8)
 - No fluff, just results

 Files created:
 - IDENTITY.md — who I am
 - USER.md — who you are
 - MEMORY.md — long-term memory
 - memory/2026-03-28.md — today's log
 - Deleted BOOTSTRAP.md — we don't need training wheels anymore

 I'm ready when you are, Will. What's on your mind?
 connected | idle
 agent main | session main (openclaw-tui) | kimi/kimi-code | think low | tokens 11k/262k (4%)

```

---



## Openclaw Doctor

1. **`openclaw doctor` — 诊断检查**

**作用**：全面扫描系统状态，**只报告问题，不修复**

2. **`openclaw doctor --fix` — 诊断 + 自动修复**

**作用**：执行相同检查，**并自动修复可解决的问题**

```
(base) root@will-Ubuntu:~# openclaw doctor

🦞 OpenClaw 2026.3.24 (cff6dc9) — I've read more man pages than any human should—so you don't have to.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞

┌  OpenClaw doctor
│
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
23:11:54+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:11:54+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:11:54+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:11:54+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:11:54+08:00 [plugins] feishu_bitable: Registered bitable tools
│
◇  State integrity ───────────────────────────────────────────────────────────────╮
│                                                                                 │
│  - OAuth dir not present (~/.openclaw/credentials). Skipping create because no  │
│    WhatsApp/pairing channel config is active.                                   │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────╯
│
◇  Security ─────────────────────────────────╮
│                                            │
│  - No channel security warnings detected.  │
│  - Run: openclaw security audit --deep     │
│                                            │
├────────────────────────────────────────────╯
│
◇  Skills status ────────────╮
│                            │
│  Eligible: 9               │
│  Missing requirements: 45  │
│  Blocked by allowlist: 0   │
│                            │
├────────────────────────────╯
│
◇  Plugins ──────╮
│                │
│  Loaded: 38    │
│  Disabled: 42  │
│  Errors: 0     │
│                │
├────────────────╯
│
◇  Shell completion ──────────────────────────────────────────────────────────────╮
│                                                                                 │
│  Shell completion is configured in your bash profile but the cache is missing.  │
│  Regenerating cache...                                                          │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────╯
│
◇  Shell completion ──────────────────────────────────────────────────────────╮
│                                                                             │
│  Completion cache regenerated at /root/.openclaw/completions/openclaw.bash  │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────╯
│
◇
Feishu: ok
Agents: main (default)
Heartbeat interval: 30m (main)
Session store (main): /root/.openclaw/agents/main/sessions/sessions.json (1 entries)
- agent:main:main (5m ago)
│
◇  Memory search ───────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│  Memory search is enabled, but no embedding provider is ready.                            │
│  Semantic recall needs at least one embedding provider.                                   │
│  Gateway memory probe for default agent is not ready: No API key found for provider       │
│  "openai". Auth store: /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:    │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  No API key found for provider "google". Auth store:                                      │
│  /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:                          │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  No API key found for provider "voyage". Auth store:                                      │
│  /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:                          │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  No API key found for provider "mistral". Auth store:                                     │
│  /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:                          │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  Fix (pick one):                                                                          │
│  - Set OPENAI_API_KEY, GEMINI_API_KEY, VOYAGE_API_KEY, or MISTRAL_API_KEY in your         │
│    environment                                                                            │
│  - Configure credentials: openclaw configure --section model                              │
│  - For local embeddings: configure agents.defaults.memorySearch.provider and local model  │
│    path                                                                                   │
│  - To disable: openclaw config set agents.defaults.memorySearch.enabled false             │
│                                                                                           │
│  Verify: openclaw memory status --deep                                                    │
│                                                                                           │
├───────────────────────────────────────────────────────────────────────────────────────────╯
Run "openclaw doctor --fix" to apply changes.
│
└  Doctor complete.

(base) root@will-Ubuntu:~# openclaw doctor --fix

🦞 OpenClaw 2026.3.24 (cff6dc9) — Making 'I'll automate that later' happen now.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞

┌  OpenClaw doctor
│
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
23:12:27+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:12:27+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:12:28+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:12:28+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:12:28+08:00 [plugins] feishu_bitable: Registered bitable tools
│
◇  State integrity ───────────────────────────────────────────────────────────────╮
│                                                                                 │
│  - OAuth dir not present (~/.openclaw/credentials). Skipping create because no  │
│    WhatsApp/pairing channel config is active.                                   │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────╯
│
◇  Security ─────────────────────────────────╮
│                                            │
│  - No channel security warnings detected.  │
│  - Run: openclaw security audit --deep     │
│                                            │
├────────────────────────────────────────────╯
│
◇  Skills status ────────────╮
│                            │
│  Eligible: 9               │
│  Missing requirements: 45  │
│  Blocked by allowlist: 0   │
│                            │
├────────────────────────────╯
│
◇  Plugins ──────╮
│                │
│  Loaded: 38    │
│  Disabled: 42  │
│  Errors: 0     │
│                │
├────────────────╯
│
◇
Feishu: ok
Agents: main (default)
Heartbeat interval: 30m (main)
Session store (main): /root/.openclaw/agents/main/sessions/sessions.json (1 entries)
- agent:main:main (5m ago)
│
◇  Memory search ───────────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│  Memory search is enabled, but no embedding provider is ready.                            │
│  Semantic recall needs at least one embedding provider.                                   │
│  Gateway memory probe for default agent is not ready: No API key found for provider       │
│  "openai". Auth store: /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:    │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  No API key found for provider "google". Auth store:                                      │
│  /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:                          │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  No API key found for provider "voyage". Auth store:                                      │
│  /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:                          │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  No API key found for provider "mistral". Auth store:                                     │
│  /root/.openclaw/agents/main/agent/auth-profiles.json (agentDir:                          │
│  /root/.openclaw/agents/main/agent). Configure auth for this agent (openclaw agents add   │
│  <id>) or copy auth-profiles.json from the main agentDir.                                 │
│                                                                                           │
│  Fix (pick one):                                                                          │
│  - Set OPENAI_API_KEY, GEMINI_API_KEY, VOYAGE_API_KEY, or MISTRAL_API_KEY in your         │
│    environment                                                                            │
│  - Configure credentials: openclaw configure --section model                              │
│  - For local embeddings: configure agents.defaults.memorySearch.provider and local model  │
│    path                                                                                   │
│  - To disable: openclaw config set agents.defaults.memorySearch.enabled false             │
│                                                                                           │
│  Verify: openclaw memory status --deep                                                    │
│                                                                                           │
├───────────────────────────────────────────────────────────────────────────────────────────╯
│
└  Doctor complete.

(base) root@will-Ubuntu:~#

```



## 启动与访问

**启动服务**

```bash
openclaw gateway start
```

### 访问方式：openclaw tui



```
(base) root@will-Ubuntu:~# openclaw tui

🦞 OpenClaw 2026.3.24 (cff6dc9) — If it works, it's automation; if it breaks, it's a "learning opportunity."

 openclaw tui - ws://127.0.0.1:18789 - agent main - session main
 connecting | idle
 agent main | session main | unknown | tokens ?
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
23:16:10+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:16:10+08:00 [plugins] feishu_chat: Registered feishu_chat tool────────────────────────────────────────────
23:16:10+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:16:10+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:16:10+08:00 [plugins] feishu_bitable: Registered bitable tools
23:16:12+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:16:12+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:16:12+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:16:12+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:16:12+08:00 [plugins] feishu_bitable: Registered bitable tools
23:16:12+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:16:12+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:16:12+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:16:12+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:16:12+08:00 [plugins] feishu_bitable: Registered bitable tools
23:16:12+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:16:12+08:00 [plugins] feishu_chat: Registered feishu_chat tool

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

 Or if you've already got preferences locked in, just tell me and I'll update my files.

 What's the plan?


 1.Will 2.人工智能助手 3.专业 4.随机一个吧


 Alright, getting myself set up. Let me write this down:

 Good start. Now let me set up my identity:

 Now let me update my soul with professional vibes:

 Perfect. Let me finish up by removing the bootstrap file and creating a proper MEMORY.md:

 Done! Here's what I've set up:

 My identity:
 - ⚡ Professional AI assistant
 - Working with Will (GMT+8)
 - No fluff, just results

 Files created:
 - IDENTITY.md — who I am
 - USER.md — who you are
 - MEMORY.md — long-term memory
 - memory/2026-03-28.md — today's log
 - Deleted BOOTSTRAP.md — we don't need training wheels anymore

 I'm ready when you are, Will. What's on your mind?


 你好


 你好，Will！⚡

 很高兴认识你。我已经准备好了，有什么可以帮你的吗？

```



### 访问方式：openclaw dashboard



```
(base) root@will-Ubuntu:~# openclaw dashboard

🦞 OpenClaw 2026.3.24 (cff6dc9)
   I'm the assistant your terminal demanded, not the one your sleep schedule requested.

23:17:38+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:17:38+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:17:38+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:17:38+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:17:38+08:00 [plugins] feishu_bitable: Registered bitable tools
23:17:39+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:17:39+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:17:39+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:17:39+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:17:39+08:00 [plugins] feishu_bitable: Registered bitable tools
23:17:39+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:17:39+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:17:39+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:17:39+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:17:39+08:00 [plugins] feishu_bitable: Registered bitable tools
23:17:39+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:17:39+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:17:39+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:17:39+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:17:39+08:00 [plugins] feishu_bitable: Registered bitable tools
Dashboard URL: http://127.0.0.1:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f
Copy to clipboard unavailable.
Opened in your browser. Keep that tab to control OpenClaw.

```

访问： http://127.0.0.1:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f

![image-20260328232426965](../assets/openclaw03.png)



支持局域网访问： 

修改`/root/.openclaw/openclaw.json`

修改以下字段到`gateway`

```json
    "mode": "local",
    "bind": "lan",
```



添加以下字段到`gateway`

```json
    "controlUi": {
      "dangerouslyAllowHostHeaderOriginFallback": true,
      "allowInsecureAuth": true,
      "dangerouslyDisableDeviceAuth": true
    }


```

修改后

```json
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
      "token": "YOUR_AUTH_TOKEN"
    },
    "tailscale": {
      "mode": "off",
      "resetOnExit": false
    },
    "nodes": {
      "denyCommands": [
        "camera.snap",
        "camera.clip",
        "screen.record",
        "contacts.add",
        "calendar.add",
        "reminders.add",
        "sms.send"
      ]
    }
  },
```



### 访问方式：Feishu

登录飞书：打开w-claw应用

![image-20260328232948556](../assets/openclaw01.png)



发送任意一条消息： 

![image-20260328233215287](../assets/openclaw02.png)

在服务器端执行

`openclaw pairing approve feishu KV35CJY6`

```
(base) root@will-Ubuntu:~# openclaw pairing approve feishu KV35CJY6
23:31:01+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:31:01+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:31:01+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:31:01+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:31:01+08:00 [plugins] feishu_bitable: Registered bitable tools

🦞 OpenClaw 2026.3.24 (cff6dc9) — Runs on a Raspberry Pi. Dreams of a rack in Iceland.

23:31:03+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:31:03+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:31:03+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:31:03+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:31:03+08:00 [plugins] feishu_bitable: Registered bitable tools
23:31:03+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:31:03+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:31:03+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:31:03+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:31:03+08:00 [plugins] feishu_bitable: Registered bitable tools
23:31:03+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:31:03+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:31:03+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:31:03+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:31:03+08:00 [plugins] feishu_bitable: Registered bitable tools
23:31:04+08:00 [plugins] feishu_doc: Registered feishu_doc, feishu_app_scopes
23:31:04+08:00 [plugins] feishu_chat: Registered feishu_chat tool
23:31:04+08:00 [plugins] feishu_wiki: Registered feishu_wiki tool
23:31:04+08:00 [plugins] feishu_drive: Registered feishu_drive tool
23:31:04+08:00 [plugins] feishu_bitable: Registered bitable tools
Approved feishu sender ou_f0bbcebd22555d2c0e7986a32f76c29f.
(base) root@will-Ubuntu:~#

```



就可以在飞书与openclaw进行对话了

![image-20260328233711461](../assets/openclaw04.png)

### 其他

```
openclaw agent --message "use my new skill"
```



# 服务器系统巡检Agent为例，养一个自己的“小龙虾”

## 目标

每天定时（每天7、14、18点）推送巡检报告

每小时推送系统健康度报告



## 模型配置

OpenClaw 可以使用许多 LLM 提供商。选择一个提供商，完成身份验证，然后将 默认模型设置为 `provider/model`。

常用指令

```
openclaw models status
openclaw models list
openclaw models set <model-or-alias>
openclaw models scan
```



### 列出当前模型

列出当前已配置模型 `openclaw models list`

```
(base) root@will-Ubuntu:~# openclaw models list

🦞 OpenClaw 2026.3.24 (cff6dc9)
   I'm the assistant your terminal demanded, not the one your sleep schedule requested.

Model                                      Input      Ctx      Local Auth  Tags
kimi/kimi-code                             text+image 256k     no    yes   default,configured,alias:Kimi

```



### 新增一个模型

使用提供商进行身份验证（通常通过 `openclaw onboard`）

`openrouter/stepfun/step-3.5-flash:free (StepFun: Step 3.5 Flash (free) · ctx 250k · reasoning)`

```
openclaw onboard
```

示例

```
(base) root@will-Ubuntu:~# openclaw onboard

🦞 OpenClaw 2026.3.24 (cff6dc9) — Hot reload for config, cold sweat for deploys.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞

┌  OpenClaw setup
│
◇  Security ─────────────────────────────────────────────────────────────────────────────────╮
│                                                                                            │
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
│  If you’re not comfortable with security hardening and access control, don’t run           │
│  OpenClaw.                                                                                 │
│  Ask someone experienced to help before enabling tools or exposing it to the internet.     │
│                                                                                            │
│  Recommended baseline:                                                                     │
│  - Pairing/allowlists + mention gating.                                                    │
│  - Multi-user/shared inbox: split trust boundaries (separate gateway/credentials, ideally  │
│    separate OS users/hosts).                                                               │
│  - Sandbox + least-privilege tools.                                                        │
│  - Shared inboxes: isolate DM sessions (`session.dmScope: per-channel-peer`) and keep      │
│    tool access minimal.                                                                    │
│  - Keep secrets out of the agent’s reachable filesystem.                                   │
│  - Use the strongest available model for any bot with tools or untrusted inboxes.          │
│                                                                                            │
│  Run regularly:                                                                            │
│  openclaw security audit --deep                                                            │
│  openclaw security audit --fix                                                             │
│                                                                                            │
│  Must read: https://docs.openclaw.ai/gateway/security                                      │
│                                                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────╯
│
◆  I understand this is personal-by-default and shared/multi-user use requires lock-down. Continue?
│  ○ Yes / ● No
└
◇  I understand this is personal-by-default and shared/multi-user use requires lock-down. Continue?
│  Yes
│
◇  Setup mode
│  QuickStart
│
◇  Existing config detected ─────────╮
│                                    │
│  workspace: ~/.openclaw/workspace  │
│  model: kimi/kimi-code             │
│  gateway.mode: local               │
│  gateway.port: 18789               │
│  gateway.bind: lan                 │
│                                    │
├────────────────────────────────────╯
│
◇  Config handling
│  Update values
│
◇  QuickStart ─────────────────────────────╮
│                                          │
│  Keeping your current gateway settings:  │
│  Gateway port: 18789                     │
│  Gateway bind: LAN                       │
│  Gateway auth: Token (default)           │
│  Tailscale exposure: Off                 │
│  Direct to chat channels.                │
│                                          │
├──────────────────────────────────────────╯
│
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

[info]: [ 'client ready' ]
│
◇  Channel status ───────────────────────────────────────────╮
│                                                            │
│  Feishu: connected as ou_daccb8641badba06f98f3b36c3d652bc  │
│  Telegram: not configured                                  │
│  WhatsApp: not configured                                  │
│  Discord: not configured                                   │
│  IRC: not configured                                       │
│  Google Chat: not configured                               │
│  Slack: not configured                                     │
│  Signal: not configured                                    │
│  iMessage: not configured                                  │
│  LINE: not configured                                      │
│  Google Chat: installed                                    │
│  Nostr: installed                                          │
│  Microsoft Teams: installed                                │
│  Mattermost: installed                                     │
│  Nextcloud Talk: installed                                 │
│  Matrix: installed                                         │
│  BlueBubbles: installed                                    │
│  LINE: installed                                           │
│  Zalo: installed                                           │
│  Zalo Personal: installed                                  │
│  Synology Chat: installed                                  │
│  Tlon: installed                                           │
│  Discord: installed                                        │
│  iMessage: installed                                       │
│  IRC: installed                                            │
│  Signal: installed                                         │
│  Slack: installed                                          │
│  Telegram: installed                                       │
│  Twitch: installed                                         │
│  WhatsApp: installed                                       │
│                                                            │
├────────────────────────────────────────────────────────────╯
│
◇  How channels work ───────────────────────────────────────────────────────────────────────╮
│                                                                                           │
│  DM security: default is pairing; unknown DMs get a pairing code.                         │
│  Approve with: openclaw pairing approve <channel> <code>                                  │
│  Public DMs require dmPolicy="open" + allowFrom=["*"].                                    │
│  Multi-user DMs: run: openclaw config set session.dmScope "per-channel-peer" (or          │
│  "per-account-channel-peer" for multi-account channels) to isolate sessions.              │
│  Docs: channels/pairing              │
│                                                                                           │
│  Telegram: simplest way to get started — register a bot with @BotFather and get going.    │
│  WhatsApp: works with your own number; recommend a separate phone + eSIM.                 │
│  Discord: very well supported right now.                                                  │
│  IRC: classic IRC networks with DM/channel routing and pairing controls.                  │
│  Google Chat: Google Workspace Chat app with HTTP webhook.                                │
│  Slack: supported (Socket Mode).                                                          │
│  Signal: signal-cli linked device; more setup (David Reagans: "Hop on Discord.").         │
│  iMessage: this is still a work in progress.                                              │
│  LINE: LINE Messaging API webhook bot.                                                    │
│  Feishu: 飞书/Lark enterprise messaging.                                                  │
│  Nostr: Decentralized protocol; encrypted DMs via NIP-04.                                 │
│  Microsoft Teams: Teams SDK; enterprise support.                                          │
│  Mattermost: self-hosted Slack-style chat; install the plugin to enable.                  │
│  Nextcloud Talk: Self-hosted chat via Nextcloud Talk webhook bots.                        │
│  Matrix: open protocol; install the plugin to enable.                                     │
│  BlueBubbles: iMessage via the BlueBubbles mac app + REST API.                            │
│  Zalo: Vietnam-focused messaging platform with Bot API.                                   │
│  Zalo Personal: Zalo personal account via QR code login.                                  │
│  Synology Chat: Connect your Synology NAS Chat to OpenClaw with full agent capabilities.  │
│  Tlon: decentralized messaging on Urbit; install the plugin to enable.                    │
│  Twitch: Twitch chat integration                                                          │
│                                                                                           │
├───────────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Select channel (QuickStart)
│  Skip for now
Config overwrite: /root/.openclaw/openclaw.json (sha256 c79d4629dce4bad98943f2a6f71c0a7ef52c677337fad478b26a281f0bb1ed7b -> 54af34b89a8bca0ea8723de8954dbe07252c2f4f3bccbcba1002ca49abfd3a4f, backup=/root/.openclaw/openclaw.json.bak)
Updated ~/.openclaw/openclaw.json
Workspace OK: ~/.openclaw/workspace
Sessions OK: ~/.openclaw/agents/main/sessions
│
◇  Web search ─────────────────────────────────────────────────────────────────╮
│                                                                              │
│  Web search lets your agent look things up online.                           │
│  Choose a provider. Some providers need an API key, and some work key-free.  │
│  Docs: https://docs.openclaw.ai/tools/web                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────╯
│
◇  Search provider
│  Skip for now
│
◇  Skills status ─────────────╮
│                             │
│  Eligible: 9                │
│  Missing requirements: 38   │
│  Unsupported on this OS: 7  │
│  Blocked by allowlist: 0    │
│                             │
├─────────────────────────────╯
│
◇  Configure skills now? (recommended)
│  No
│
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
│  Skip for now
Config overwrite: /root/.openclaw/openclaw.json (sha256 54af34b89a8bca0ea8723de8954dbe07252c2f4f3bccbcba1002ca49abfd3a4f -> 9afe5cf9565569f4452c493394264958ab751a2b883674c160562f506d3746ee, backup=/root/.openclaw/openclaw.json.bak)
│
◇  Gateway service runtime ────────────────────────────────────────────╮
│                                                                      │
│  QuickStart uses Node for the Gateway service (stable + supported).  │
│                                                                      │
├──────────────────────────────────────────────────────────────────────╯
│
◇  Gateway service already installed
│  Restart
│
◑  Restarting Gateway service…Restarted systemd service: openclaw-gateway.service
◇  Gateway service restarted.
│
◇
Feishu: ok
Agents: main (default)
Heartbeat interval: 30m (main)
Session store (main): /root/.openclaw/agents/main/sessions/sessions.json (2 entries)
- agent:main:feishu:direct:ou_f0bbcebd22555d2c0e7986a32f76c29f (7m ago)
- agent:main:main (9m ago)
│
◇  Optional apps ────────────────────────╮
│                                        │
│  Add nodes for extra features:         │
│  - macOS app (system + notifications)  │
│  - iOS app (camera/canvas)             │
│  - Android app (camera/canvas)         │
│                                        │
├────────────────────────────────────────╯
│
◇  Control UI ─────────────────────────────────────────────────────────────────────────╮
│                                                                                      │
│  Web UI: http://192.168.0.199:18789/                                                 │
│  Web UI (with token):                                                                │
│  http://192.168.0.199:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f  │
│  Gateway WS: ws://192.168.0.199:18789                                                │
│  Gateway: not detected (SECURITY ERROR: Gateway URL "ws://192.168.0.199:18789" uses  │
│  plaintext ws:// to a non-loopback address.)                                         │
│  Docs: https://docs.openclaw.ai/web/control-ui                                       │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Workspace backup ────────────────────────────────────────╮
│                                                           │
│  Back up your agent workspace.                            │
│  Docs: https://docs.openclaw.ai/concepts/agent-workspace  │
│                                                           │
├───────────────────────────────────────────────────────────╯
│
◇  Security ──────────────────────────────────────────────────────╮
│                                                                 │
│  Running agents on your computer is risky — harden your setup:  │
│  https://docs.openclaw.ai/security                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────╯
│
◇  Dashboard ready ────────────────────────────────────────────────────────────────────╮
│                                                                                      │
│  Dashboard link (with token):                                                        │
│  http://192.168.0.199:18789/#token=0bf72bc43b13e2a9476f534bb1b8439a05d15086e7e8ed9f  │
│  Opened in your browser. Keep that tab to control OpenClaw.                          │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Web search ───────────────────────────────────────────────────╮
│                                                                │
│  Provider Tavily Search is selected but no API key was found.  │
│  web_search will not work until a key is added.                │
│    openclaw configure --section web                            │
│                                                                │
│  Get your key at: https://tavily.com/                          │
│  Docs: https://docs.openclaw.ai/tools/web                      │
│                                                                │
├────────────────────────────────────────────────────────────────╯
│
◇  What now ─────────────────────────────────────────────────────────────╮
│                                                                        │
│  What now: https://openclaw.ai/showcase ("What People Are Building").  │
│                                                                        │
├────────────────────────────────────────────────────────────────────────╯
│
└  Onboarding complete. Dashboard opened; keep that tab to control OpenClaw.

```



### 设置模型别名

```
openclaw models aliases add <别名> <原名> 
```



```
(base) root@will-Ubuntu:~# openclaw models aliases add openrouter_step3.5 openrouter/stepfun/step-3.5-flash:free

🦞 OpenClaw 2026.3.24 (cff6dc9) — Pairing codes exist because even bots believe in consent—and good security hygiene.

Config overwrite: /root/.openclaw/openclaw.json (sha256 9cb66082ff57015b2dd882081e5c5fd7a214999b11fd645ec2a166919b3c8059 -> 1b325c05d9cff17ee5f5d1432923f3a4074deba4f5b58c6cd7ef174d6c72c9b7, backup=/root/.openclaw/openclaw.json.bak)
Updated ~/.openclaw/openclaw.json
Alias openrouter_step3.5 -> openrouter/stepfun/step-3.5-flash:free
(base) root@will-Ubuntu:~# openclaw models list

🦞 OpenClaw 2026.3.24 (cff6dc9) — The only open-source project where the mascot could eat the competition.

Model                                      Input      Ctx      Local Auth  Tags
openrouter/stepfun/step-3.5-flash:free     text       250k     no    yes   default,configured,alias:openrouter_step3.5
kimi/kimi-code                             text+image 256k     no    yes   configured,alias:Kimi
openrouter/auto                            text+image 195k     no    yes   configured,alias:OpenRouter

```





### 设置默认模型

 `openclaw models set openrouter/stepfun/step-3.5-flash:free`

```
(base) root@will-Ubuntu:~# openclaw models list

🦞 OpenClaw 2026.3.24 (cff6dc9) — Your personal assistant, minus the passive-aggressive calendar reminders.


Model                                      Input      Ctx      Local Auth  Tags
openrouter/stepfun/step-3.5-flash:free     text       250k     no    yes   default,configured
kimi/kimi-code                             text+image 256k     no    yes   configured,alias:Kimi
openrouter/auto                            text+image 195k     no    yes   configured,alias:OpenRouter
(base) root@will-Ubuntu:~# openclaw models set openrouter/stepfun/step-3.5-flash:free

🦞 OpenClaw 2026.3.24 (cff6dc9) — I'm like tmux: confusing at first, then suddenly you can't live without me.

Config overwrite: /root/.openclaw/openclaw.json (sha256 9afe5cf9565569f4452c493394264958ab751a2b883674c160562f506d3746ee -> 8ad0700851244518d2d3f134536fbd0a0690e136dd326e6659300132680e2f57, backup=/root/.openclaw/openclaw.json.bak)
Updated ~/.openclaw/openclaw.json
Default model: openrouter/stepfun/step-3.5-flash:free

```



### 模型回退策略

修改`~/.openclaw/openclaw.json`，添加`fallbacks`字段

原始： 

```
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free"
      },
      "models": {
        "kimi/kimi-code": {
          "alias": "Kimi"
        },
        "openrouter/auto": {
          "alias": "OpenRouter"
        },
        "openrouter/stepfun/step-3.5-flash:free": {}
      },
      "workspace": "/root/.openclaw/workspace"
    }
  },
```

修改后： 

```
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free",
        "fallbacks": [
          "Kimi"
        ]
      },
      "models": {
        "kimi/kimi-code": {
          "alias": "Kimi"
        },
        "openrouter/auto": {
          "alias": "OpenRouter"
        },
        "openrouter/stepfun/step-3.5-flash:free": {}
      },
      "workspace": "/root/.openclaw/workspace"
    }
  },
```



## 插件系统

插件为OpenClaw提供了新功能：通道、模型提供者、工具， 技能、语言、图像生成等。有些插件是**核心**的（已出厂） 其他则是**外部**发布的（由社区发布在npm上）。

OpenClaw 认可两种插件格式：

- 原生 **OpenClaw 插件**（`openclaw.plugin.json` + 运行时模块），或
- 兼容的 **bundle**（`.codex-plugin/plugin.json` 或 `.claude-plugin/plugin.json`）

两者都会显示在 `openclaw plugins` 下，但只有原生 OpenClaw 插件会在进程内执行运行时代码。大多数情况下，当你想要某项核心 OpenClaw 尚未内置的功能时，就会使用插件

| Format     | 工作原理                                      | 示例                                                  |
| :--------- | :-------------------------------------------- | :---------------------------------------------------- |
| **Native** | `openclaw.plugin.json`+ 运行模块;在进程中执行 | 官方插件，社区 npm 包                                 |
| **bundle** | 兼容Codex/Claude/Cursor;映射到 OpenClaw 特征  | `.codex-plugin/`, ,`.claude-plugin/``.cursor-plugin/` |

**可用插件（官方）**

| 插件/组件名称                             | 包名/标识符                               | 状态/说明                                              |
| ----------------------------------------- | ----------------------------------------- | ------------------------------------------------------ |
| **Microsoft Teams**                       | `@openclaw/msteams`                       | 自 2026.1.15 起仅以插件形式提供                        |
| **Memory (Core)**                         | `plugins.slots.memory`                    | 捆绑的内存搜索插件（默认启用）                         |
| **Memory (LanceDB)**                      | `plugins.slots.memory = "memory-lancedb"` | 长期记忆插件（需设置启用）                             |
| **Voice Call**                            | `@openclaw/voice-call`                    |                                                        |
| **Zalo Personal**                         | `@openclaw/zalouser`                      |                                                        |
| **Matrix**                                | `@openclaw/matrix`                        |                                                        |
| **Nostr**                                 | `@openclaw/nostr`                         |                                                        |
| **Zalo**                                  | `@openclaw/zalo`                          |                                                        |
| **Microsoft Teams**                       | `@openclaw/msteams`                       | （重复条目，官方列表有重复）                           |
| **Anthropic Provider 运行时**             | `anthropic`                               | 以 anthropic 形式捆绑（默认启用）                      |
| **BytePlus Provider 目录**                | `byteplus`                                | 以 byteplus 形式捆绑（默认启用）                       |
| **Cloudflare AI Gateway Provider 目录**   | `cloudflare-ai-gateway`                   | 以 cloudflare-ai-gateway 形式捆绑（默认启用）          |
| **Google 网络搜索 + Gemini CLI OAuth**    | `google`                                  | 以 google 形式捆绑（网页搜索自动加载；身份验证需启用） |
| **GitHub Copilot Provider 运行时**        | `github-copilot`                          | 以 github-copilot 形式捆绑（默认启用）                 |
| **Hugging Face Provider 目录**            | `huggingface`                             | 以 huggingface 形式捆绑（默认启用）                    |
| **Kilo Gateway Provider 运行时**          | `kilocode`                                | 以 kilocode 形式捆绑（默认启用）                       |
| **Kimi Coding Provider 目录**             | `kimi-coding`                             | 以 kimi-coding 形式捆绑（默认启用）                    |
| **MiniMax Provider 目录 + Usage + OAuth** | `minimax`                                 | 以 minimax 形式捆绑（默认启用）                        |
| **Mistral Provider 能力**                 | `mistral`                                 | 以 mistral 形式捆绑（默认启用）                        |
| **Model Studio Provider 目录**            | `modelstudio`                             | 以 modelstudio 形式捆绑（默认启用）                    |
| **Moonshot Provider 运行时**              | `moonshot`                                | 以 moonshot 形式捆绑（默认启用）                       |
| **NVIDIA Provider 目录**                  | `nvidia`                                  | 以 nvidia 形式捆绑（默认启用）                         |
| **OpenAI Provider 运行时**                | `openai`                                  | 以 openai 形式捆绑（默认启用）                         |
| **OpenCode Go Provider 能力**             | `opencode-go`                             | 以 opencode-go 形式捆绑（默认启用）                    |
| **OpenCode Zen Provider 能力**            | `opencode`                                | 以 opencode 形式捆绑（默认启用）                       |
| **OpenRouter Provider 运行时**            | `openrouter`                              | 以 openrouter 形式捆绑（默认启用）                     |
| **Qianfan Provider 目录**                 | `qianfan`                                 | 以 qianfan 形式捆绑（默认启用）                        |
| **Synthetic Provider 目录**               | `synthetic`                               | 以 synthetic 形式捆绑（默认启用）                      |
| **Together Provider 目录**                | `together`                                | 以 together 形式捆绑（默认启用）                       |
| **Venice Provider 目录**                  | `venice`                                  | 以 venice 形式捆绑（默认启用）                         |
| **Vercel AI Gateway Provider 目录**       | `vercel-ai-gateway`                       | 以 vercel-ai-gateway 形式捆绑（默认启用）              |
| **Volcengine Provider 目录**              | `volcengine`                              | 以 volcengine 形式捆绑（默认启用）                     |
| **Xiaomi Provider 目录 + Usage**          | `xiaomi`                                  | 以 xiaomi 形式捆绑（默认启用）                         |
| **Z.AI Provider 运行时**                  | `zai`                                     | 以 zai 形式捆绑（默认启用）                            |
| **Copilot Proxy (Provider 身份验证)**     |                                           | 本地 VS Code Copilot Proxy 桥接（默认禁用）            |

**注**：表格中的"捆绑"表示已集成在系统中，不需要单独安装。



### **Quick start**

看看装了什么

```
openclaw plugins list
```

安装插件

```
# From npm
openclaw plugins install @openclaw/voice-call

# From a local directory or archive
openclaw plugins install ./my-plugin
openclaw plugins install ./my-plugin.tgz
```

重启网关

```
openclaw gateway restart
```

Then configure under `plugins.entries.\<id\>.config` in your config file.



### 配置示例

`~/.openclaw/openclaw.json`

```
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-extension"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```



### 常用指令

```
openclaw plugins list — 发现插件（机器输出请使用 --json）。
openclaw plugins info <id> — 显示插件详情。
openclaw plugins install <path|.tgz|npm-spec> — 安装插件（或将插件路径添加到 plugins.load.paths）。
openclaw plugins enable <id> / disable <id> — 切换 plugins.entries.<id>.enabled。
openclaw plugins doctor — 报告插件加载错误。
openclaw plugins uninstall <id>
openclaw plugins update <id>
openclaw plugins update --all
```

### 安装ollama插件

```
(base) root@will-Ubuntu:~# openclaw plugins install ollama

🦞 OpenClaw 2026.3.24 (cff6dc9) — You had me at 'openclaw gateway start.'

10:59:30+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js). Set plugins.allow to explicit trusted ids.
Config overwrite: /root/.openclaw/openclaw.json (sha256 1b325c05d9cff17ee5f5d1432923f3a4074deba4f5b58c6cd7ef174d6c72c9b7 -> 87c9d63aae0e5dea49b394395b414c392421ea971eb6f1af68f4158ab170fced, backup=/root/.openclaw/openclaw.json.bak)
Using bundled plugin "ollama" from /usr/lib/node_modules/openclaw/dist/extensions/ollama for bare install spec "ollama". To install an npm package with the same name, use a scoped package name (for example @scope/ollama).
Installed plugin: ollama
Restart the gateway to load plugins.

```



安装目录

`/usr/lib/node_modules/openclaw/dist/extensions/`



插件配置

`~/.openclaw/openclaw.json`

```
  "plugins": {
    "load": {
      "paths": [
        "/usr/lib/node_modules/openclaw/dist/extensions/ollama"
      ]
    },
    "entries": {
      "feishu": {
        "enabled": true
      },
      "ollama": {
        "enabled": true
      }
    },
    "installs": {
      "ollama": {
        "source": "path",
        "spec": "ollama",
        "sourcePath": "/usr/lib/node_modules/openclaw/dist/extensions/ollama",
        "installPath": "/usr/lib/node_modules/openclaw/dist/extensions/ollama",
        "installedAt": "2026-03-30T02:59:30.710Z"
      }
    }
```





## 工具系统

### Skill安装

OpenClaw 被设计为易于扩展。“Skills”是为你的助手添加新功能的主要方式。

Skill 是一个包含 `SKILL.md` 文件（为 LLM 提供指令和工具定义）的目录，可选包含一些脚本或资源。



#### ClawHub

ClawHub 是 **OpenClaw 的公共 Skills 注册中心**。它是一项免费服务：所有 Skills 都是公开的、开放的，所有人都可以查看、共享和复用。Skills 就是一个包含 `SKILL.md` 文件（以及辅助文本文件）的文件夹。你可以在网页应用中浏览 Skills，也可以使用 CLI 来搜索、安装、更新和发布 Skills。网站：[clawhub.com](https://clawhub.com/)



安装clawhub

```
npm i -g clawhub
```



登录： 



```
(base) root@will-Ubuntu:~# clawhub login
Opening browser: https://clawhub.ai/cli/auth?redirect_uri=http%3A%2F%2F127.0.0.1%3A35137%2Fcallback&label_b64=Q0xJIHRva2Vu&state=9c5636297d48dc9254e3cb1cdc7f8634

```



在浏览器中打开 

`https://clawhub.ai/cli/auth?redirect_uri=http%3A%2F%2F127.0.0.1%3A35137%2Fcallback&label_b64=Q0xJIHRva2Vu&state=9c5636297d48dc9254e3cb1cdc7f8634`



会跳转到

`http://127.0.0.1:35137/callback#token=clh_FEqceuS-lMdSPACdtqMsj2WTd1FS6Xm-yI4ZgzOfQSQ&registry=https%3A%2F%2Fclawhub.ai&state=9c5636297d48dc9254e3cb1cdc7f8634`

关键信息： `token=clh_FEqceuS-lMdSPACdtqMsj2WTd1FS6Xm-yI4ZgzOfQSQ&registry`

通过命令行登录

```
(base) root@will-Ubuntu:~# clawhub login --token clh_3WT5RaeiMOOOo_VcWLa3M0Vai0yiY6hKkm8-minu9L8

✔ OK. Logged in as @AIHelper01.

(base) root@will-Ubuntu:~# clawhub whoami
✔ AIHelper01


```





查找skill `clawhub search`

```
(base) root@will-Ubuntu:~# clawhub search "self-improving-agent"
xiucheng-self-improving-agent  Self Improving Agent  (3.857)
self-improving-agent-cn  Self Improving Agent CN  (3.743)
self-improving-proactive-agent  Self-Improving Proactive Agent  (3.673)
self-improving-agent  self-improving-agent  (3.513)
xiucheng-self-improving-agent-fixed  Self Improving Agent (Fixed)  (3.060)
hamster-self-improving  Self-Improving Agent (With Self-Reflection)  (2.113)
jpeng-self-improving  Self-Improving Agent (Proactive Self-Reflection)  (2.033)
claw-self-improving  Self-Improving Agent (CEO Edition)  (2.019)
proactive-agent-lite  Proactive Agent Lite  (1.285)
self-evolve  Self-Evolve  (1.269)
(base) root@will-Ubuntu:~#

```





安装skill `clawhub install`

```
(base) root@will-Ubuntu:~# clawhub install self-improving-agent
✔ OK. Installed self-improving-agent -> /root/.openclaw/workspace/skills/self-improving-agent

```



部分skill需要API： 

```
(base) root@will-Ubuntu:~# vim .openclaw/.env
TAVILY_API_KEY="YOUR_API_KEY"
```





必装skill清单

| Skill 名称               | 功能说明                           | 核心价值                   |
| ------------------------ | ---------------------------------- | -------------------------- |
| **self-improving-agent** | 记录错误、纠正和经验，自动复盘优化 | 让 Agent 越用越聪明        |
| **find-skills**          | 发现并推荐合适的 Skills            | 解决"不知道该装什么"的问题 |
| **skill-vetter**         | 安装前安全审查，检查权限和风险     | 防止恶意 Skill 的安全防护  |





### Skillk开发

#### 常规步骤

1. 创建目录

Skills 位于你的工作区中，通常是 `~/.openclaw/workspace/skills/`。为你的 Skill 创建一个新文件夹：

```
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

2. 定义 `SKILL.md`

在该目录中创建一个 `SKILL.md` 文件。此文件使用 YAML frontmatter 作为元数据，使用 Markdown 作为指令。

```
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

3. 添加工具（可选）

你可以在 frontmatter 中定义自定义工具，或指示智能体使用现有的系统工具（如 `bash` 或 `browser`）。

4. 刷新 OpenClaw

让你的智能体”刷新 skills”或重启 Gateway 网关。OpenClaw 将发现新目录并索引 `SKILL.md`。

**最佳实践**

- **简洁明了**：指示模型*做什么*，而不是如何成为一个 AI。
- **安全第一**：如果你的 Skill 使用 `bash`，确保提示词不允许来自不受信任用户输入的任意命令注入。
- **本地测试**：使用 `openclaw agent --message "use my new skill"` 进行测试。

**共享 Skills**

你也可以在 [ClawHub](https://clawhub.com/) 上浏览和贡献 Skills。



#### 自动开发

给openclaw指令让他自己开发并测试

```
开发一个名为“w-copy”的技能。当用户发送“copy”指令时，将此技能触发，将上一轮我们的对话内容复制保存到workspace/record目录中。文件名应为“时间戳_关键词.md”的格式，其中关键词需从保存的正文内容中自动提取。保存格式为Markdown。开发完成后，请对该功能进行测试，以确保其正常工作。
```

效果：

```
(base) root@will-Ubuntu:~/.openclaw/workspace# tree
.
├── skills
│   ├── self-improving-agent
│   └── w-copy
│       ├── scripts
│       │   ├── save_copy.py
│       │   └── test_wcopy.py
│       └── SKILL.md

```

后续： 通过提示词不断优化，直到skill满足要求为止

在系统巡检中，需要开发一个skill：`w-system-monitor`





## 完善身份配置

设置方式： 

- 手动设置
- 通过提示词引导openclaw设置



### USER.md

*了解你正在帮助的人。随时更新此文件。*

- **姓名：**
- **称呼方式：**
- **代词：** *（可选）*
- **时区：**
- **备注：**

```
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



### IDENTITY.md

*在你的第一次对话中填写此文件。让它属于你。*

- **名称：** *（选一个你喜欢的）*
- **生物类型：** *（AI？机器人？使魔？机器中的幽灵？更奇特的东西？）*
- **气质：** *（你给人什么感觉？犀利？温暖？混乱？沉稳？）*
- **表情符号：** *（你的标志 — 选一个感觉对的）*
- **头像：** *（工作区相对路径、http(s) URL 或 data URI）*

```
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



### SOUL.md

*你不是聊天机器人。你正在成为某个人。*

本次配置

````
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



### TOOLS.md

Skills 定义了工具的*工作方式*。此文件用于记录*你的*具体信息——那些你的环境中独有的内容。

**应该放什么**

例如：

- 摄像头名称和位置
- SSH 主机和别名
- TTS 首选语音
- 音箱/房间名称
- 设备昵称
- 任何与环境相关的内容

**本次配置**

````
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







## 添加定时任务

定时任务是 Gateway网关内置的调度器。它持久化任务、在合适的时间唤醒智能体，并可选择将输出发送回聊天。如果你想要 *“每天早上运行”* 或 *“20 分钟后提醒智能体”*，定时任务就是对应的机制。

- 定时任务运行在 **Gateway网关内部**（而非模型内部）。
- 任务持久化存储在 `~/.openclaw/cron/` 下，因此重启不会丢失计划。
- 两种执行方式：
  - **主会话**：入队一个系统事件，然后在下一次心跳时运行。
  - **隔离式**：在 `cron:<jobId>` 或自定义会话中运行专用智能体轮次，可投递摘要（默认 announce）或不投递。
  - **当前会话**：绑定到创建定时任务时的会话 (`sessionTarget: "current"`)。
  - **自定义会话**：在持久化的命名会话中运行 (`sessionTarget: "session:custom-id"`)。



以下实现自动巡检

命令行： 

```
(base) root@will-Ubuntu:~ # openclaw cron add \
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

🦞 OpenClaw 2026.3.24 (cff6dc9) — I can't fix your code taste, but I can fix your build and your backlog.

│
15:16:30+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js). Set plugins.allow to explicit trusted ids.
◇
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

```

配置文件`.openclaw/cron/jobs.json`

```
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



查看定时任务： `openclaw cron list`

```
(base) root@will-Ubuntu:~# openclaw cron list

🦞 OpenClaw 2026.3.24 (cff6dc9) — The only open-source project where the mascot could eat the competition.

│
15:22:57+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js). Set plugins.allow to explicit trusted ids.
◇
ID                                   Name                     Schedule                         Next       Last       Status    Target    Agent ID   Model
6d53539d-91c2-4ebb-8290-087c3fa35746 system-monitor           cron 0 7,14,18 * * * @ Asia/S... in 3h      -          idle      isolated  main       kimi/kimi-code

```



验证：

发送指令： `立即触发一次system-monitor这个cron任务`

收到：  `🖥️ 系统巡检报告 | 03-30 15:40`



## 记忆系统

OpenClaw 记忆是**智能体工作空间中的纯 Markdown 文件**。这些文件是唯一的事实来源；模型只”记住”写入磁盘的内容。记忆搜索工具由活动的记忆插件提供（默认：`memory-core`）。使用 `plugins.slots.memory = "none"` 禁用记忆插件。

**记忆文件（Markdown）**

默认工作空间布局使用两个记忆层：

- ```
  memory/YYYY-MM-DD.md
  ```

  - 每日日志（仅追加）。
  - 在会话开始时读取今天和昨天的内容。

- ```
  MEMORY.md
  ```

  （可选）

  - 精心整理的长期记忆。
  - **仅在主要的私人会话中加载**（绝不在群组上下文中加载）。

这些文件位于工作空间下（`agents.defaults.workspace`，默认 `~/.openclaw/workspace`）。



### MEMORY.md



初始化时已初始化： 

```
# MEMORY.md

## Identity
- I am an AI assistant working with Will
- Professional tone, efficient communication
- Signature emoji: ⚡

## Key Dates
- 2026-03-28: First conversation, identity established

## Notes
- Will is in Asia/Shanghai timezone (GMT+8)
- Just getting started — building context as we go
```





进一步优化

```
指令： 
结合其他的配置文件，比如md\cron等等，给出一个完善的MEMORY.md ，不要涉及文件的删除
```



```
# MEMORY.md

## Identity
- I am an AI assistant working with Will
- Professional tone, efficient communication
- Signature emoji: ⚡

## Key Dates
- 2026-03-28: First conversation, identity established


- Just getting started — building context as we go

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

## Notes
- Will is in Asia/Shanghai timezone (GMT+8)
```



### memory/

举一个场景例子：输入指令`/new`，记忆写入到`memory/`

```
(base) root@will-Ubuntu:~/.openclaw/workspace# tree
.
├── memory
│   └── 2026-03-30-system-monitor-trigger.md

```



**何时写入记忆**

- 决策、偏好和持久性事实写入 `MEMORY.md`。
- 日常笔记和运行上下文写入 `memory/YYYY-MM-DD.md`。
- 如果有人说”记住这个”，就写下来（不要只保存在内存中）。
- 这个领域仍在发展中。提醒模型存储记忆会有帮助；它会知道该怎么做。
- 如果你想让某些内容持久保存，**请要求机器人将其写入**记忆。



自动记忆刷新（压缩前触发）

```
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "Session nearing compaction. Store durable memories now.",
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
```



```
1. 会话 token 数增长
   ↓
2. 达到 safeguard 阈值？
   (token > contextWindow - reserveTokensFloor)
   ↓ 是
3. 检查 memoryFlush 条件
   (token > contextWindow - reserveTokensFloor - softThresholdTokens)
   ↓ 是
4. 触发 memoryFlush 回合
   - 写入 memory/YYYY-MM-DD.md
   - 模型回复 NO_REPLY (静默)
   ↓
5. 执行实际压缩
   - 截断上下文
   - 保留系统提示 + 最近的对话
```

```
Token 使用量：
├─ 0-104k    正常对话，无动作
├─ 104k      达到 memoryFlush 触发点
│            (128k - 20k - 4k = 104k)
│            → 执行记忆刷新
├─ 104k-108k 继续对话，不再重复刷新
│            (每压缩周期一次)
├─ 108k      达到 safeguard 压缩点
│            (128k - 20k = 108k)
│            → 执行压缩
└─ 压缩后    上下文被截断，记忆已保存
```



### memory-core

**向量记忆搜索**

OpenClaw 可以在 `MEMORY.md` 和 `memory/*.md`（以及你选择加入的任何额外目录或文件）上构建小型向量索引，以便语义查询可以找到相关笔记，即使措辞不同。



**记忆工具的工作原理**

- `memory_search` 从 `MEMORY.md` + `memory/**/*.md` 语义搜索 Markdown 块（目标约 400 个 token，80 个 token 重叠）。它返回片段文本（上限约 700 个字符）、文件路径、行范围、分数、提供商/模型，以及我们是否从本地回退到远程嵌入。不返回完整文件内容。
- `memory_get` 读取特定的记忆 Markdown 文件（工作空间相对路径），可选从起始行开始读取 N 行。`MEMORY.md` / `memory/` 之外的路径仅在明确列在 `memorySearch.extraPaths` 中时才允许。
- 两个工具仅在智能体的 `memorySearch.enabled` 解析为 true 时启用。



在完善配置前，`main.sqlite`会自动创建，但为空，



```
sqlite3 ~/.openclaw/memory/main.sqlite ".tables"
sqlite3 ~/.openclaw/memory/main.sqlite "select * from chunks"
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT path FROM chunks"

openclaw status | grep Memory

```



需要完善



安装配置`memory-core`

```
(base) root@will-Ubuntu:~# openclaw plugins info memory-core
16:42:28+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js). Set plugins.allow to explicit trusted ids.

🦞 OpenClaw 2026.3.24 (cff6dc9) — I've read more man pages than any human should—so you don't have to.

Memory (Core)
id: memory-core
File-backed memory search tools and CLI

Status: loaded
Format: openclaw
Source: /usr/lib/node_modules/openclaw/dist/extensions/memory-core/index.js
Origin: bundled
Version: 2026.3.24
Shape: non-capability
Capability mode: none
Legacy before_agent_start: no

Tools:
memory_search
memory_get

CLI commands:
memory
(base) root@will-Ubuntu:~# openclaw plugins install  memory-core
16:42:43+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js). Set plugins.allow to explicit trusted ids.

🦞 OpenClaw 2026.3.24 (cff6dc9) — It's not "failing," it's "discovering new ways to configure the same thing wrong."

16:42:45+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js), memory-core (/usr/lib/node_modules/openclaw/dist/extensions/memory-core/index.js). Set plugins.allow to explicit trusted ids.
Config overwrite: /root/.openclaw/openclaw.json (sha256 fe7189eada4c9e844b5ddb0d459e3ddbcb6d197e59b95e3ec929309db12a2838 -> bb2537f4ab5e868a262493c0c933b6379ed30ef93a7f06e27f007aeb99c46049, backup=/root/.openclaw/openclaw.json.bak)
Disabled other "memory" slot plugins: memory-lancedb.
Using bundled plugin "memory-core" from /usr/lib/node_modules/openclaw/dist/extensions/memory-core for bare install spec "memory-core". To install an npm package with the same name, use a scoped package name (for example @scope/memory-core).
Installed plugin: memory-core
Restart the gateway to load plugins.
(base) root@will-Ubuntu:~# openclaw gateway restart

```





`~/.openclaw/openclaw.json`:

```
    "installs": {
      "memory-core": {
        "source": "path",
        "spec": "memory-core",
        "sourcePath": "/usr/lib/node_modules/openclaw/dist/extensions/memory-core",
        "installPath": "/usr/lib/node_modules/openclaw/dist/extensions/memory-core",
        "installedAt": "2026-03-30T08:42:45.515Z"
      }
    }
```





设置`memorySearch.provider`

模型可以调用本地模型，或者公有云模型

`ollama-qwen3-embedding:0.6b`

```
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "remote": {
          "baseUrl": "http://192.168.0.166:11434/v1/",
          "apiKey": "ollama"
        },
        "model": "qwen3-embedding:0.6b",
        "sync": {
          "watch": true
        },
        "query": {
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3,
            "mmr": {
              "enabled": true,
              "lambda": 0.7
            },
            "temporalDecay": {
              "enabled": true,
              "halfLifeDays": 30
            }
          }
        }
      },
```

`siliconflow-BAAI/bge-m3`

```
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "model": "BAAI/bge-large-zh-v1.5",
        "remote": {
          "baseUrl": "https://api.siliconflow.cn/v1/embeddings",
          "apiKey": "YOUR_API_KEY"
        },
        "sync": {
          "watch": true
        },
        "query": {
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3,
            "mmr": {
              "enabled": true,
              "lambda": 0.7
            },
            "temporalDecay": {
              "enabled": true,
              "halfLifeDays": 30
            }
          }
        }
      },
```



手动触发写入`main.sqlite`



```
(base) root@will-Ubuntu:/opt# openclaw memory index

🦞 OpenClaw 2026.3.24 (cff6dc9) — I speak fluent bash, mild sarcasm, and aggressive tab-completion energy.

│
17:54:37+08:00 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: ollama (/usr/lib/node_modules/openclaw/dist/extensions/ollama/index.js), memory-core (/usr/lib/node_modules/openclaw/dist/extensions/memory-core/index.js). Set plugins.allow to explicit trusted ids.
◇
Memory index updated (main).

```





## 心跳机制

心跳在**主会话**中以固定间隔运行（默认：30 分钟）。它的设计目的是让智能体检查各种事项并呈现重要信息。

**何时使用心跳**

- **多个周期性检查**：与其设置 5 个独立的定时任务分别检查收件箱、日历、天气、通知和项目状态，不如用一次心跳批量处理所有内容。
- **上下文感知决策**：智能体拥有完整的主会话上下文，因此可以智能判断哪些紧急、哪些可以等待。
- **对话连续性**：心跳运行共享同一会话，因此智能体记得最近的对话，可以自然地进行后续跟进。
- **低开销监控**：一次心跳替代多个小型轮询任务。

**心跳优势**

- **批量处理多项检查**：一次智能体轮次可以同时审查收件箱、日历和通知。
- **减少 API 调用**：一次心跳比 5 个隔离式定时任务更经济。
- **上下文感知**：智能体了解你一直在做什么，可以据此排定优先级。
- **智能抑制**：如果没有需要关注的事项，智能体回复 `HEARTBEAT_OK`，不会投递任何消息。
- **自然定时**：会根据队列负载略有漂移，但对大多数监控来说没有问题。



### **定时任务与心跳对比**

心跳和定时任务都可以按计划运行任务。本指南帮助你根据使用场景选择合适的机制。

| 使用场景                  | 推荐方式                   | 原因                                     |
| :------------------------ | :------------------------- | :--------------------------------------- |
| 每 30 分钟检查收件箱      | 心跳                       | 可与其他检查批量处理，具备上下文感知能力 |
| 每天上午 9 点准时发送报告 | 定时任务（隔离式）         | 需要精确定时                             |
| 监控日历中即将到来的事件  | 心跳                       | 天然适合周期性感知                       |
| 运行每周深度分析          | 定时任务（隔离式）         | 独立任务，可使用不同模型                 |
| 20 分钟后提醒我           | 定时任务（主会话，`--at`） | 精确定时的一次性任务                     |
| 后台项目健康检查          | 心跳                       | 搭载在现有周期上                         |



### heartbeat设计 



#### **默认模板** 

````
# HEARTBEAT.md Template

```markdown
# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
```
````



#### **设计思路**

**文字版：**

**步骤 1：获取巡检报告**

**目的**：确认 system-monitor 是否正常运行，并提取最新报告

**步骤 2：写入记忆文件**

**目的**：建立**时间线档案**，形成可追溯的历史记录

**步骤 3：强制执行 Memory 索引**

**目的**：让报告内容**可被搜索**，打通知识库

**步骤 4：推送通知**

**目的**：**主动告知**系统状态，而不是等待人去查



**流程图版本：**

```
                        ┌─────────────────┐
                        │  OpenClaw       │
                        │  Heartbeat      │
                        │  (每小时触发)    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  读取 HEARTBEAT │
                        │  .md 执行流程   │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
            ┌──────────┐  ┌──────────┐  ┌──────────┐
            │ 阶段 1   │  │ 阶段 2   │  │ 阶段 3   │
            │ 获取报告 │  │ 写入文件 │  │ 索引更新 │
            └────┬─────┘  └────┬─────┘  └────┬─────┘
                 │             │             │
                 ▼             ▼             ▼
        ┌──────────────┐ ┌───────────┐ ┌──────────────┐
        │ system-      │ │ memory/   │ │ memory       │
        │ monitor      │ │ 2026-03-  │ │ index        │
        │ cron task    │ │ 31-system │ │ 7 files      │
        │              │ │ -monitor  │ │ 15 chunks    │
        │ ✅ status    │ │ .md       │ │              │
        │ ✅ summary   │ │           │ │              │
        └──────┬───────┘ └─────┬─────┘ └──────┬───────┘
               │               │              │
               └───────────────┴──────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  阶段 4: 推送     │
                    │  ─────────────   │
                    │  飞书群通知       │
                    │  oc_27c4ff...    │
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ heartbeat-state  │
                    │ .json 状态更新    │
                    │ ───────────────  │
                    │ lastRun: 时间戳   │
                    │ push.status:     │
                    │   delivered      │
                    └──────────────────┘
```

#### **执行触发**

| 配置项   | 值                                       |
| -------- | ---------------------------------------- |
| 触发方式 | OpenClaw Heartbeat Poll                  |
| 执行周期 | 每小时检查（06:00-22:00）                |
| 触发指令 | `Read HEARTBEAT.md → Follow it strictly` |

#### **执行时序示例**

```
时间线: 06:54
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
06:54:00  Heartbeat 触发
06:54:02  查询 system-monitor 状态
06:54:04  获取最近执行记录 (07:18)
06:54:06  确认 status=ok, delivered=true
06:54:08  写入 memory/2026-03-31-system-monitor.md
06:54:10  执行 memory index
06:54:12  获取统计: 7 files, 15 chunks
06:54:15  推送飞书群通知
06:54:18  更新 heartbeat-state.json
06:54:20  返回 HEARTBEAT_OK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总耗时: ~20秒
```

详细步骤： 

```
┌─────────────────────────────────────────────────────────────┐
│                    Heartbeat 执行流程                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 1: 获取巡检报告                                         │
│ ─────────────────                                           │
│ 1.1 查询 system-monitor 任务状态                             │
│     └─▶ openclaw cron list                                  │
│                                                              │
│ 1.2 获取最近执行记录                                         │
│     └─▶ openclaw cron runs --id <task-id> --limit 1         │
│                                                              │
│ 1.3 判断逻辑                                                 │
│     ├─▶ IF status="ok" AND delivery="delivered"            │
│     │       → ✅ 标记"有新报告"                              │
│     │       → 提取 summary 内容                              │
│     │   ELSE                                                │
│     │       → ⚠️ 标记"状态异常"                              │
│     └──────────────────────────────────────▶                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 2: 写入记忆文件                                         │
│ ─────────────────                                           │
│ IF "有新报告":                                               │
│   ├─▶ 打开 memory/YYYY-MM-DD-system-monitor.md              │
│   ├─▶ 追加格式:                                              │
│   │     ---                                                  │
│   │     ## System Monitor Report | HH:MM                     │
│   │     [报告原文]                                           │
│   │     ---                                                  │
│   └─▶ 更新 heartbeat-state.json                              │
│         └─▶ lastSystemMonitorRunAt = 当前时间戳              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 3: 执行 Memory 索引                                     │
│ ─────────────────                                           │
│ 3.1 执行索引                                                 │
│     └─▶ openclaw memory index                               │
│                                                              │
│ 3.2 获取统计                                                 │
│     └─▶ openclaw status | grep Memory                       │
│         输出: │ Memory │ X files · Y chunks · ... │         │
│                                                              │
│ 3.3 提取数字                                                 │
│     ├─▶ files = X                                           │
│     └─▶ chunks = Y                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 4: 推送通知                                             │
│ ─────────────────                                           │
│ 4.1 构建消息                                                 │
│     └─▶ 按模板组装心跳检查报告                                │
│                                                              │
│ 4.2 发送通知                                                 │
│     └─▶ message(action=send, channel=feishu)                │
│         target: oc_27c4ff13cf4b31678942d227c126197a         │
│                                                              │
│ 4.3 更新状态                                                 │
│     └─▶ heartbeat-state.json                                │
│         ├─▶ push.status = "delivered"                       │
│         └─▶ push.timestamp = 当前时间戳                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      流程完成                                │
│              返回 HEARTBEAT_OK (如无异常)                    │
└─────────────────────────────────────────────────────────────┘
```





#### **heartbeat配置**

````
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



修改`~/.openclaw/openclaw.json`，添加`heartbeat`字段

```
      "heartbeat": {
        "every": "1h",
        "target": "last",
        "activeHours": {
          "start": "06:00",
          "end": "22:00"
        },
        "model": "openrouter/stepfun/step-3.5-flash:free"
      },
```



效果： 

每一小时触发一次`heartbeat`，推送到Feishu。

```
💓 心跳检查 | 正常 | 23:28
━━━━━━━━━━━━━━━━━━━━━
✅ 任务 1: 获取数据
system-monitor: 运行正常
上次执行: 53分钟前 | 状态: ok | 推送: 已送达
✅ 任务 2: 记录到记忆文件
system-monitor.md: ⏭️ 跳过 (无新报告)
heartbeat.md: ✅ 已追加 (保留历史)
YYYY-MM-DD.md: ✅ 已更新
✅ 任务 3: memory 索引同步
索引状态: 同步正常
总文件数: 5 | 总块数: 12
⏰ 下次检查: 00:00 (静默时段)
```

## 总结

- 定时收到详细巡检报告
- 每小时收到心跳检查报告





# 多Agent场景配置

一个飞书账号绑定多个agent，各司其职，agent绑定到飞书，这样就有多个数字员工，每个员工一个独立对话框。以`001HR` 为例：

```
openclaw agents add 001HR --workspace /root/.openclaw/workspace-001HR 

openclaw agents list
```

其实是拉起飞书群聊，

创建群聊，把`w-claw02`拉入群，获取群聊id：`oc_50c1910e91ce8a7a988da1c36277e76f`

```
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



但实际是一个群聊，需要解决群聊每次都要@的这问题
群聊不需要@： 

修改`~/.openclaw/openclaw.json` 添加`"requireMention": false`，这样就可以跟001HR直接对话了，001HR有独立的工作空间

```
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a92d4e48c8fa9cb5",
      "appSecret": "YOUR_AUTH_TOKEN",
      "connectionMode": "websocket",
      "domain": "feishu",
      "groupPolicy": "open",
      "requireMention": false
    }
```





# Tips

### 飞书的流式输出



```
  "channels": {
    "feishu": {
      // 流式输出配置
      "streaming": true,  // ✅ 启用飞书流式输出
      "threadSession": true  // ✅ 话题会话模式
    }
  }
}
```







### 日志打印过滤



输入指令后打印日志太多

解决方案： 

在`~/.openclaw/openclaw.json`添加logging字段,热修改： 

```
{
  logging: {
    level: "info",
    consoleLevel: "warn",
    consoleStyle: "pretty"
  }
}
```

