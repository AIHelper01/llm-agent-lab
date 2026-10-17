# 第一章 OpenClaw：从对话到执行的 AI 革命

> ChatGPT 给你建议。OpenClaw 帮你做完。

2026 年初，[OpenClaw](https://github.com/openclaw/openclaw) 两个月斩获 247,000 GitHub 星标，超越 Linux 成为史上增长最快的开源项目。13 家国内大厂跟进，掀起"[百虾大战](#百虾大战)"。

它不是又一个聊天机器人。它是一个**住在你电脑里、真正能干活的 AI 员工**——而这背后，是 AI 交互范式的一次根本跃迁。

从教 AI "怎么问"的提示词工程（Prompt Engineering），到教 AI "喂什么"的上下文工程（Context Engineering），再到今天的[**驾驭工程（Harness Engineering）**](https://openai.com/index/harness-engineering)——**把 AI 真正套上缰绳，让它持续、自主地替你干活**。OpenClaw 就是这根缰绳。

---

## 不是聊天，是干活

你可能习惯了这样的 AI：

```
你：帮我整理一下收件箱里的邮件
ChatGPT：我可以给你一些整理邮件的建议...
```

OpenClaw 不一样：

```
你：帮我整理一下收件箱里的邮件
OpenClaw：[正在连接 Gmail API...]
         [已读取 127 封未读邮件...]
         [按主题分类完成，生成摘要...]
         完成！已将邮件分为 5 类，重要邮件 3 封已标记。
```

**一个给建议，一个做事情。** 这就是本质区别。

OpenClaw（龙虾）能读写文件、执行命令、控制浏览器、收发消息、定时巡检——所有数据都在你自己的设备上。你可以让它每天早上推送新闻简报，自动回复邮件，甚至写代码、提 PR、跑测试。

## OpenClaw 的本质：自主式 AI Agent

OpenClaw 是一个开源的自主式 AI Agent 执行引擎，由开发者 Peter Steinberger 创建。根据 [Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) 的介绍，它是一个免费开源的自主人工智能代理项目，以消息平台（WhatsApp、Telegram、Discord、Slack 等）作为主要用户界面。

核心特征：

- **本地运行**：数据完全由你掌控，不送到别人的服务器
- **真正执行**：不只生成代码，而是直接运行、验证、修复
- **自主决策**：能分解任务、选择工具、自我检查、迭代优化
- **多平台集成**：通过 Telegram、Discord、Slack、飞书等随时随地控制

## 发展历程：从 Clawdbot 到 OpenClaw

- **2025.11**：以 Clawdbot 名称首次发布
- **短暂更名**：因 Anthropic 商标问题改为 Moltbot
- **2026.01**：正式定名 OpenClaw
- **2026.02**：病毒式传播，成为 GitHub 历史上增长最快的项目
- **2026.02.14**：开发者宣布加入 OpenAI，项目转移到开源基金会

---

## 龙虾为什么这么火？

和2025年 DeepSeek 的爆火一样——**把一小撮人已经在享受的能力，第一次推到了更广泛的人群面前**。

| 设计决策                    | 为什么有效                                          | trade-off                |
| --------------------------- | --------------------------------------------------- | ------------------------ |
| **聊天界面作为入口**        | 复用微信/飞书/WhatsApp 等现有习惯，学习成本几乎为零 | 线性对话，过程不可观测   |
| **统一上下文 + 持久化记忆** | 跨平台、跨会话记住你的一切，"它真的懂我"            | 记忆是黑盒，跨项目易污染 |
| **丰富的 Skills 生态**      | 16,000+ 技能可组合，AI 还能自己写新技能             | 12% 第三方技能含恶意代码 |

三者形成**飞轮效应**：记忆带来数据复利，技能带来自我进化，易用性带来使用频率——越转越快，越用越强。

## 百虾大战

国内大厂跟进 OpenClaw 全景图：

![国内大厂 OpenClaw 生态全景](../assets/openclaw-landscape.jpg)

图片来源：[TheBlockBeats]

**类 Claw 方案对比与选型指南**

OpenClaw 的爆发催生了一个庞大的"龙虾生态"——从开源框架到商业托管、从桌面客户端到嵌入式设备、从个人助手到企业级多智能体平台。本附录系统梳理所有主流类 Claw 方案，帮你根据自身需求快速选型。

类 Claw 方案可分为五大类：

| 分类           | 代表产品                                      | 适合谁                             |
| -------------- | --------------------------------------------- | ---------------------------------- |
| **桌面客户端** | AutoClaw、ClawX、OneClaw、LobsterAI、EasyClaw | 想要 GUI 体验、不想碰终端的用户    |
| **托管服务**   | ArkClaw、Kimi Claw、MaxClaw、WorkBuddy        | 只想用、不想管服务器的用户         |
| **云厂商部署** | 腾讯云、阿里云、华为云、百度智能云等          | 想要独立服务器但省去安装步骤的用户 |
| **开源自建**   | OpenClaw、IronClaw、CoPaw、NanoClaw 等        | 想完全掌控、愿意折腾的技术用户     |
| **移动端/IoT** | Xiaomi miclaw、MimiClaw、droidclaw            | 手机端或嵌入式硬件场景             |

换个角度看——选 AI 就像买车，你得先知道自己是要越野、通勤、还是拉货：

| 阵营                               | 定位                         | 代表选手                                                     | 适合谁                                     |
| ---------------------------------- | ---------------------------- | ------------------------------------------------------------ | ------------------------------------------ |
| **第一阵营：本地桌面与一键安装**   | 开箱即用，注重隐私           | [LobsterAI](https://lobsterai.youdao.com)（网易有道）、[AutoClaw](https://autoglm.zhipuai.cn/autoclaw)（智谱）、[EasyClaw](https://easyclaw.cn)（猎豹）、[ClawX](https://clawx.com.cn)、[OneClaw](https://oneclaw.cn)、[WorkBuddy](https://workbuddy.tencent.com)（腾讯） | 打工人写日报、做 PPT，装在自己电脑里最踏实 |
| **第二阵营：公有云原生与一键部署** | 高扩展，企业级               | [阿里云](https://www.aliyun.com/benefit/scene/moltbot)、[腾讯云](https://cloud.tencent.com/act/pro/openclaw)、[火山引擎](https://www.volcengine.com/activity/codingplan)、[华为云](https://activity.huaweicloud.com/openclaw.html)、[百度智能云](https://cloud.baidu.com/doc/qianfan/s/tmlhtdwyj)、[京东云](https://www.ithome.com/0/927/614.htm) | 企业大规模应用协同                         |
| **第三阵营：云端托管与移动跨端**   | 跨平台便捷，免除本地算力烦恼 | [MaxClaw](https://maxclaw.ai/)（MiniMax）、[Kimi Claw](https://kimi.com)（月之暗面）、[ArkClaw](https://www.volcengine.com/experience/ark?mode=claw)（字节） | 只想用、不想管服务器                       |
| **第四阵营：专业定制与极客硬件**   | 进阶领域与低功耗场景         | [PicoClaw](https://github.com/sipeed/picoclaw)（树莓派）、[IronClaw](https://www.ironclaw.com)（安全重写）、[HiClaw](https://hiclaw.org/)（多智能体）、[MimiClaw](https://github.com/memovai/mimiclaw)（ESP32） | 极客玩家、安全敏感、多智能体协作           |



**自建 vs 托管决策框架**

选好场景后，下一步是决定**怎么部署**。以下框架帮你在四种部署模式之间做出选择：

| 维度         | 自建部署（本教程主线） | 桌面客户端       | 云厂商一键部署         | 全托管 SaaS         |
| ------------ | ---------------------- | ---------------- | ---------------------- | ------------------- |
| **代表**     | OpenClaw 手动安装      | AutoClaw / ClawX | 腾讯云/阿里云等        | ArkClaw / Kimi Claw |
| **控制权**   | ★★★★★ 完全掌控         | ★★★★☆ 大部分     | ★★★★☆ 大部分           | ★★☆☆☆ 受限          |
| **运维成本** | 需自行维护             | 几乎无           | 半托管                 | 零运维              |
| **月费**     | 仅电费/VPS             | 免费/按需买积分  | ¥10-100/月             | ¥10-300/月          |
| **数据主权** | 完全本地               | 本地             | 云端（可控）           | 云端（受限）        |
| **灵活性**   | ★★★★★ 最高             | ★★★☆☆ 中等       | ★★★★☆ 较高             | ★★☆☆☆ 最低          |
| **上手难度** | ★★★☆☆ 需终端           | ★☆☆☆☆ 下载即用   | ★★☆☆☆ 买了就能用       | ★☆☆☆☆ 注册即用      |
| **适合谁**   | 想深入学习的技术用户   | 零基础用户       | 想省事但保留控制的用户 | 只想用不想管的用户  |

**决策建议：**

> - 🎯 **新手首选**：AutoClaw（零门槛）→ 熟悉后迁移到 OpenClaw（完全掌控）
> - 💰 **预算最低**：ClawX 或 OneClaw + StepFun 免费模型（零成本）
> - 🔒 **安全优先**：IronClaw 自建（WASM 沙盒 + 零遥测）
> - 🏢 **企业用途**：WorkBuddy（微信生态）/ ArkClaw（飞书生态）
> - 🤖 **多智能体**：HiClaw（Manager-Worker 架构）

---


## 领养四步法：像雇员工一样养龙虾

领养一只龙虾，本质上和雇一个员工一样——准备四样东西就行：

![养一只龙虾需要做的4件事情](../assets/龙虾套装.png)

| 步骤           | 类比             | 你要做的                                   |
| -------------- | ---------------- | ------------------------------------------ |
| **租房子**     | 给员工一个工位   | 安装 OpenClaw（本地电脑或云服务器）        |
| **买粮食**     | 给员工发工资     | 配置模型 API Key（Token 就是龙虾的"口粮"） |
| **给联系方式** | 让客户能找到员工 | 接入聊天平台（QQ / 飞书 / Telegram）       |
| **培训上岗**   | 教员工怎么干活   | 配置智能体、工具、定时任务                 |

> 前两步（租房子 + 买粮食）是**最低要求**——装好 OpenClaw、配好一个模型 API Key，龙虾就能在终端里跟你对话了。后两步让它从"能说话"变成"能干活"。



# 第二章 OpenClaw 快速安装

> 本章结束时，你将在电脑上运行一个真正的 AI 助手——可以在终端对话，也可以通过浏览器控制面板管理它。全程大约 10 分钟。

## 支持的平台

OpenClaw 可以运行在所有主流操作系统上。

| 平台        | Gateway 支持          | 配套应用                            |
| ----------- | --------------------- | ----------------------------------- |
| **macOS**   | 原生支持              | 菜单栏应用 + 语音唤醒（Voice Wake） |
| **Windows** | 支持（强烈推荐 WSL2） | 计划中                              |
| **Linux**   | 原生支持              | 计划中                              |

##  系统要求

- **[Node 24（推荐）](https://docs.openclaw.ai/install/node)**（出于兼容性考虑，仍支持 Node 22 LTS，目前为 `22.16+`；如果缺失，[安装脚本](https://docs.openclaw.ai/zh-CN/install#install-methods) 会安装 Node 24）
- macOS、Linux 或 Windows
- 仅当你从源码构建时需要 `pnpm`

## 安装步骤

**官方推荐方式**是使用一键安装脚本——它会自动检测 Node.js、安装 CLI、并启动配置向导，一步到位。

<details>
<summary>什么是终端（Terminal）？</summary>
终端是一个文字界面，你输入命令，电脑执行。打开方式：

- **Windows**：按 `Win + X`，选择"终端管理员"或"PowerShell"
- **macOS**：按 `Cmd + 空格`，搜索"Terminal"
- **Linux**：按 `Ctrl + Alt + T`

![Windows PowerShell 终端](../assets/windows-powershell.png)

### macOS / Linux / WSL2

**方式一：安装脚本** （推荐）

安装 OpenClaw 的推荐方式。它会一步完成 Node 检测、安装和新手引导。

下载 CLI，通过 npm 全局安装，并启动设置向导。

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

就这样脚本会处理 Node 检测、安装和新手引导。如果要跳过新手引导，只安装二进制文件：

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

所有标志、环境变量以及 CI/自动化选项，请参阅 [Installer internals](https://docs.openclaw.ai/install/installer)。

**方式二：npm / pnpm**

如果你已经自行管理 Node，我们推荐使用 Node 24。出于兼容性考虑，OpenClaw 仍支持 Node 22 LTS，目前为 `22.16+`：

```
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**方式三：从源码**

适用于贡献者或任何想从本地检出运行的人。

克隆并构建：克隆 [OpenClaw 仓库](https://github.com/openclaw/openclaw) 并构建：

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
```

链接 CLI：让 `openclaw` 命令在全局可用：

```
pnpm link --global
```

或者，你也可以跳过链接，直接在仓库内通过 `pnpm openclaw ...` 运行命令。

运行新手引导

```
openclaw onboard --install-daemon
```



### Windows（PowerShell）

安装脚本

下载 CLI，通过 npm 全局安装，并启动设置向导。

```shell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iwr -useb https://openclaw.ai/install.ps1 | iex
```

就这样脚本会处理 Node 检测、安装和新手引导。如果要跳过新手引导，只安装二进制文件：

```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

所有标志、环境变量以及 CI/自动化选项，请参阅 [Installer internals](https://docs.openclaw.ai/install/installer)。

> **Q: Windows 上运行 `openclaw` 提示"命令未找到"？**
>
> A: PowerShell 默认禁止执行脚本。以管理员身份运行：Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

然后重新打开终端。

**方式二：npm / pnpm**

如果你已经自行管理 Node，我们推荐使用 Node 24。出于兼容性考虑，OpenClaw 仍支持 Node 22 LTS，目前为 `22.16+`：

打开 PowerShell（管理员模式），运行：

```powershell
# npm
npm install -g openclaw@latest
openclaw onboard --install-daemon

# pnpm
pnpm add -g openclaw@latest
pnpm approve-builds -g        # 批准 openclaw、node-llama-cpp、sharp 等
openclaw onboard --install-daemon
```

### 验证安装

```bash
openclaw --version
```

<details>
<summary>查看验证截图</summary>


![openclaw --version 终端输出](../assets/openclaw-version.png)

<details>
<summary>什么是 Node.js？</summary>


OpenClaw 需要 Node.js 22+ 运行环境。Node.js 让用 JavaScript 编写的 OpenClaw 能在你的电脑上运行。你不需要学 JavaScript——安装脚本会自动处理。如果你已经装过 Node.js 22+，脚本会跳过这一步。

<details>
<summary>Windows 用户：什么是 WSL2？如何安装？</summary>


WSL2（Windows Subsystem for Linux 2）让你在 Windows 上运行完整的 Linux 环境。**如果你不想折腾，直接用 PowerShell 即可，跳过此步骤。**

1. 以管理员身份打开 PowerShell
2. 运行：`wsl --install`
3. 重启电脑，按提示设置用户名和密码

之后在开始菜单搜索"Ubuntu"即可打开 WSL2 终端，使用上面 macOS / Linux 的安装脚本。

> OpenClaw 官方建议：在 Windows 上，**强烈推荐使用 WSL2** 运行 OpenClaw，兼容性和稳定性更好。


## 配置 AI 模型

OpenClaw 本身不包含 AI 大脑，需要连接一个"模型提供商"来获得智能。如果安装脚本已启动了配置向导，按下方说明填写即可；如果跳过了向导，手动运行：

```bash
openclaw onboard --install-daemon
```

![openclaw onboard 配置向导界面](../assets/openclaw-onboard.png)

向导会引导你完成所有配置。

关键步骤：

**安全确认** → 选 **Yes**
**配置模式** → 选 **QuickStart**
**模型提供商** → 选 **Custom Provider**

初次使用，推荐推荐 OpenRouter 或者 硅基流动 的免费体验模型

**OpenRouter**——注册即可使用免费模型（如 Step 3.5 Flash），无需充值，零成本完成全部教程练习。

然后输入以下信息（以 OpenRouter 免费模型为例）：

```
◇  API Base URL
│  https://openrouter.ai/api/v1

◇  API Key
│  sk-or-v1-你的密钥

◇  Endpoint compatibility
│  OpenAI-compatible

◇  Model ID
│  stepfun/step-3.5-flash:free
```

然后输入以下信息（以  硅基流动 免费模型为例）：

```
◇  API Base URL
│  https://api.siliconflow.cn/v1

◇  API Key
│  sk-你的密钥

◇  Model ID
│  deepseek-ai/DeepSeek-V3
```



## 验证安装

安装配置完成后，验证运行状态：

```bash
openclaw status
```

<details>
<summary>查看 status 输出截图</summary>
![openclaw status 输出](../assets/openclaw-status.png)

## 首次对话

**方式一：命令行终端界面**

一切正常后，开始你的第一次对话：

```bash
openclaw tui
```

试着输入：`你好，请介绍一下你自己` —— 如果龙虾回复了，恭喜你，安装成功！

**单次 Agent 调用**

不需要交互界面，发一条消息就走：

```bash
openclaw agent --list

openclaw agent --agent main --message "你好，请介绍一下你自己"                       # 本地执行
openclaw agent --agent main --message "你好，请介绍一下你自己"  --thinking high      # 使用深度思考
```

**方式二：Web 图形化界面**

打开 Web 控制面板，可视化管理你的龙虾：

```bash
openclaw dashboard
```

浏览器会自动打开控制面板 `http://localhost:18789`：

![Web 控制面板浏览器界面](../assets/openclaw-dashboard-browser.png)

## 更新

OpenClaw 发展迅速（尚未到”1.0”）。将更新视为发布基础设施：更新 → 运行检查 → 重启（或使用会重启的 `openclaw update`）→ 验证。

### 更新前准备

升级前建议备份你的定制内容：配置文件、凭证 `~/.openclaw/credentials/`、工作区 `~/.openclaw/workspace/`。

```
配置：~/.openclaw/openclaw.json
凭证：~/.openclaw/credentials/
工作区：~/.openclaw/workspace
```

### 推荐：重新运行网站安装程序（原地升级）

**首选**的更新路径是重新运行网站上的安装程序。它会检测现有安装、原地升级，并在需要时运行 `openclaw doctor`。

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

说明：

- 如果你不想再次运行新手引导向导，添加 `--no-onboard`。

- 对于源码安装，使用：

  ```
  curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
  ```

  安装程序仅在仓库干净时才会执行 `git pull --rebase`

- 对于**全局安装**，脚本底层使用 `npm install -g openclaw@latest`。

### 回滚指定版本

```bash
# 安装指定版本
npm i -g openclaw@<version>
openclaw doctor
openclaw gateway restart
```

源码安装按日期回滚：

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
pnpm install && pnpm build
openclaw gateway restart
```

---

## 卸载

卸载前建议先备份 `~/.openclaw/workspace`（包含对话历史和记忆文件）。

```bash
openclaw uninstall
```

<details>
<summary>需要手动卸载，或 CLI 已删除但服务仍在运行？</summary>
**手动完整卸载：**

```bash
openclaw gateway stop
openclaw gateway uninstall
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
npm rm -g openclaw
# 或 pnpm remove -g openclaw

# macOS 应用（如有）
rm -rf /Applications/OpenClaw.app
```

> 使用了 `--profile` 时，对每个 `~/.openclaw-<profile>` 重复删除步骤。

**服务残留手动清理：**

macOS：

```bash
launchctl bootout gui/$UID/bot.molt.gateway
rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist
```

Linux：

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

Windows：

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```



---

## 迁移到新机器

<details>
<summary>换电脑了，怎么把龙虾完整搬过去？</summary>
核心思路：**复制状态目录 + 工作区 → 安装 → doctor → 重启**。无需重新进行新手引导。

**要迁移什么：**

| 项目         | 默认路径                 | 包含内容                                             |
| ------------ | ------------------------ | ---------------------------------------------------- |
| **状态目录** | `~/.openclaw/`           | 配置、凭证、API 密钥、OAuth 令牌、会话历史、渠道状态 |
| **工作区**   | `~/.openclaw/workspace/` | MEMORY.md、USER.md、Skills 笔记等智能体文件          |

两者都复制 = 完整迁移。只复制工作区 = 不保留会话和凭证。

**步骤 0 — 旧机器备份：**

```bash
openclaw gateway stop
cd ~
tar -czf openclaw-state.tgz .openclaw
```

**步骤 1 — 新机器安装：**

按[第 1 步](#_1-安装)安装 CLI，然后用 `scp` 或外部驱动器把 `openclaw-state.tgz` 复制过来并解压，覆盖新生成的 `~/.openclaw/`。

**步骤 2 — 运行 doctor + 重启：**

```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

**验证：**

- [ ] `openclaw status` 显示 Gateway 正在运行
- [ ] 渠道仍然连接（WhatsApp 不需要重新配对）
- [ ] Dashboard 显示现有会话
- [ ] 工作区文件存在

**常见陷阱：**

- **只复制了配置文件**：不够，必须迁移整个 `~/.openclaw/` 文件夹（凭证存在 `credentials/` 子目录）
- **权限问题**：确保状态目录由运行 Gateway 的用户拥有，不要用 root 复制
- **备份安全**：`~/.openclaw/` 含 API 密钥等敏感信息，加密存储，勿通过不安全渠道传输



# 第三章 初始配置向导

## 0. 两条路径，选一条

**Onboarding（配置向导）** 帮你告诉龙虾三件事：用哪个模型、通过哪个渠道联系你、在哪里工作。OpenClaw 提供两条路径：

![OpenClaw Onboarding](../assets/OpenClaw-Onboarding.png)

```mermaid
flowchart TB

subgraph OB["OpenClaw Onboarding 路径"]

subgraph CLI["CLI 配置向导（跨平台）"]
A1["openclaw onboard"]
A2["终端交互式配置"]
A3["支持脚本化 / 非交互"]
A1 --> A2 --> A3
end

subgraph MAC["macOS 应用引导（仅 macOS）"]
B1["OpenClaw.app 启动"]
B2["图形化分步引导"]
B3["自动申请系统权限"]
B1 --> B2 --> B3
end

end

A3 --> C
B3 --> C

C["Gateway 启动
龙虾就绪 ✅"]
```

| 路径               | 适用场景                                  | 平台                           |
| ------------------ | ----------------------------------------- | ------------------------------ |
| **CLI 配置向导**   | 需要完全控制、远程服务器、自动化脚本      | macOS / Linux / Windows (WSL2) |
| **macOS 应用引导** | 希望图形化引导、需要语音/摄像头等原生权限 | 仅 macOS                       |

> **已经在第二章跑过 `openclaw onboard` 了？** 基本配置已完成！本章帮你理解每一步做了什么，以及如何微调。

---

## 1. CLI 配置向导（所有平台）

### 1.1 启动向导

```bash
openclaw onboard
```

> **想同时安装后台服务？** 加 `--install-daemon` 一步到位：
>
> ```bash
> openclaw onboard --install-daemon
> ```

### 1.2 QuickStart vs Advanced

向导启动后会问你第一个问题：**QuickStart（快速开始）** 还是 **Advanced（高级模式）**？

| 选项           | 自动配置内容                                                 | 适合谁                                |
| -------------- | ------------------------------------------------------------ | ------------------------------------- |
| **QuickStart** | 本地 Gateway + 默认工作区 + 端口 18789 + Token 认证 + coding 工具策略 | 第一次用，想尽快聊天                  |
| **Advanced**   | 所有选项都可自定义                                           | 需要远程部署、Tailscale、特殊安全策略 |

<details>
<summary>QuickStart 默认配置一览</summary>
QuickStart 模式自动应用以下默认值：
| 配置项               | 默认值                                | 说明                     |
| -------------------- | ------------------------------------- | ------------------------ |
| Gateway 位置         | 本机（loopback）                      | 仅本机可访问             |
| 工作区               | `~/.openclaw/workspace/`              | 或使用已有工作区         |
| Gateway 端口         | 18789                                 | 标准端口                 |
| 认证方式             | Token（自动生成）                     | 即使本地也需认证         |
| 工具策略             | `tools.profile: "coding"`             | 保留文件系统和运行时工具 |
| DM 隔离              | `session.dmScope: "per-channel-peer"` | 每个渠道独立会话         |
| Tailscale            | 关闭                                  | 不暴露到 Tailnet         |
| Telegram/WhatsApp DM | 白名单模式                            | 会提示输入你的手机号     |

> 已有自定义 `tools.profile` 的用户不会被覆盖——向导尊重现有配置。

### 1.3 向导的六个步骤

#### 步骤一：模型与认证

**场景一：**选择模型提供商，粘贴 API Key。

**场景二：**自定义模型提供商（Custom Provider）

向导列表里没有你的提供商？选 **Custom Provider**，依次填写：

| 步骤                | 内容                                                         | 示例                           |
| ------------------- | ------------------------------------------------------------ | ------------------------------ |
| 1. 选择兼容类型     | OpenAI-compatible / Anthropic-compatible / Unknown（自动检测） | OpenAI-compatible              |
| 2. 输入 Base URL    | 提供商的 API 地址                                            | `https://api.mycompany.com/v1` |
| 3. 输入 API Key     | 如果需要的话                                                 | `sk-custom-...`                |
| 4. 填写 Model ID    | 模型标识符                                                   | `gpt-4o`                       |
| 5. 设置别名（可选） | 方便记忆的短名称                                             | `company-gpt`                  |
| 6. 设置 Endpoint ID | 区分多个自定义端点                                           | `mycompany`                    |

<details>
<summary>多个自定义端点共存</summary>
每个 Custom Provider 通过 **Endpoint ID** 区分，所以你可以同时配置多个自定义端点：

```json
// 配置示例
{
  "models": {
    "providers": {
      "custom-company-a": {
        "type": "openai",
        "baseUrl": "https://api.company-a.com/v1",
        "apiKey": "sk-a-..."
      },
      "custom-company-b": {
        "type": "anthropic",
        "baseUrl": "https://api.company-b.com/v1",
        "apiKey": "sk-b-..."
      }
    }
  }
}
```

#### 步骤二：工作区

设置龙虾的工作目录（默认 `~/.openclaw/workspace/`），存放 IDENTITY.md、MEMORY.md 等文件。已有工作区文件会被保留。

#### 步骤三：Gateway 配置

设置端口（默认 18789）、绑定地址（默认仅本机）和认证方式。

<details>
<summary>Gateway Token 与 SecretRef</summary>

在交互式 Token 模式下，你可以选择：

- **明文 Token**（默认）：存储在配置文件中
- **SecretRef**：通过环境变量或外部程序管理 Token

非交互模式下使用 SecretRef：

```bash
openclaw onboard --gateway-token-ref-env GATEWAY_TOKEN --non-interactive
```

注意：如果同时配置了 `gateway.auth.token` 和 `gateway.auth.password` 但未设置 `gateway.auth.mode`，后台服务安装会被阻止，直到你明确选择一种模式。



#### 步骤四：渠道接入

选择要连接的聊天平台（WhatsApp、Telegram、Discord 等）。可以跳过，后续用 `openclaw channels add` 随时添加。

#### 步骤五：后台服务

安装后台服务，开机自动启动 Gateway。macOS 用 LaunchAgent，Linux/WSL2 用 systemd。

<details>
<summary>后台服务与 SecretRef 的注意事项</summary>
- 如果 Token 认证使用 SecretRef，后台服务安装时会验证引用有效性，但**不会**将解析后的 Token 持久化到服务环境中
- 如果配置的 SecretRef 无法解析，后台服务安装会被阻止，并给出修复建议
- 使用 `openclaw doctor` 可以自动检测和修复服务问题



#### 步骤六：健康检查与技能安装

启动 Gateway、验证运行状态，安装推荐技能。

## 2. 重新配置与维护

### 2.1 重新运行向导

```bash
openclaw configure
```

> `configure` 修改现有配置，`onboard` 用于首次设置；前者不会重新安装后台服务。

### 2.2 重置配置

```bash
# 默认重置：配置、凭证、会话
openclaw onboard --reset

# 完整重置：包括工作区
openclaw onboard --reset --reset-scope full
```

> ⚠️ `--reset` 会清除现有配置。只想改某项设置，用 `openclaw configure` 更安全。

### 2.3 配置异常处理

配置文件损坏时，运行 `openclaw doctor` 自动诊断并修复。



## 3. 多智能体配置

OpenClaw 支持在同一实例下运行多个独立智能体，每个智能体有自己的工作区、会话和渠道绑定。

### 3.1 添加智能体

```bash
openclaw agents add <name>
```

### 3.2 智能体配置项

| 配置项                    | 说明                                                 |
| ------------------------- | ---------------------------------------------------- |
| `agents.list[].name`      | 智能体名称                                           |
| `agents.list[].workspace` | 工作区路径（默认 `~/.openclaw/workspace-<agentId>`） |
| `agents.list[].agentDir`  | 智能体配置目录                                       |

<details>
<summary>非交互模式与消息路由</summary>
**非交互模式标志**：


```bash
openclaw agents add worker-bot \
  --model "openrouter/stepfun/step-3.5-flash:free" \
  --agent-dir ~/.openclaw/agents/worker \
  --bind "telegram:chat:12345" \
  --non-interactive
```

**消息路由**：通过 `--bind` 参数将特定渠道/对话绑定到某个智能体。向导也会引导你完成绑定配置。

这样你可以让不同的龙虾负责不同的聊天群或任务类型。

也可以直接修改`openclaw.json`配置文件，以绑定飞书为例： 

```
openclaw agents add 001HR \ 
  --workspace /Users/will/.openclaw/workspace-001 

openclaw config set --json bindings '[
  {
    "agentId": "001HR",
    "match": {
      "channel": "feishu",
      "peer": {
        "kind": "group",
        "id": "oc_066af8418969975894edf72d74630d28"
      }
    }
  }
]'
```



# 第四章 Gateway网关运维

Gateway 是龙虾的神经中枢。本章教你管理它——启动、监控、排障。

## 0. Gateway 是什么？

Gateway 是 OpenClaw 的核心后台进程，负责连接聊天平台、调度 AI 模型、管理会话与工具。一台机器通常只运行一个 Gateway，默认监听 `ws://127.0.0.1:18789`，仅本机可访问。

```
用户消息 → [飞书/QQ/Telegram] → Gateway → AI 模型 → 用户
                                    ↕
                              控制面板 / CLI
```

<details>
<summary>Gateway 架构详解（连接协议、节点系统）</summary>




![OpenClaw Gateway 架构](E:/hello-claw - yw/docs/cn/adopt/chapter6/images/OpenClaw-Gateway.png)

```mermaid
flowchart LR

A["飞书"]
B["QQ"]
C["Telegram"]
D["Web 面板"]
E["CLI"]

G["Gateway（网关）
统一消息入口"]

R["Agent 运行时"]

M["AI 模型"]

WS["WebSocket API"]

A --> G
B --> G
C --> G
D --> G
E --> G

G --> R
R --> M

G <---> WS
```

**核心职责**：

- 维护与各聊天平台的长连接
- 将消息路由给对应 Agent
- 为客户端提供 WebSocket API
- 执行 Cron 定时任务

**连接协议**：Gateway 使用 WebSocket，默认监听 `127.0.0.1:18789`（仅本机）。

- 请求：`{type:"req", id, method, params}` → 响应：`{type:"res", id, ok, payload}`
- 事件（服务器推送）：`{type:"event", event, payload}`

**安全认证**：

- 设置了 `OPENCLAW_GATEWAY_TOKEN` 后，连接时必须提供匹配的 token
- 新设备需要配对审批；本地连接自动批准，远程连接需显式审批

**远程访问**：推荐 Tailscale 或 VPN；备选 SSH 隧道：

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

**节点（Node）系统**：物理设备（手机、平板）以 `role: node` 身份接入，可提供拍照（`camera.*`）、录屏（`screen.record`）、位置（`location.get`）、画布（`canvas.*`）等能力。



## 1. 启动与管理

```bash
# 启动
openclaw gateway --port 18789

# 查看状态
openclaw gateway status    # 显示 "Runtime: running" + "RPC probe: ok" = 正常
openclaw status            # 整体状态

# 实时日志
openclaw logs --follow
```

注册为系统服务后开机自启、崩溃自动重启：

```bash
openclaw gateway install   # 安装服务
openclaw gateway restart   # 重启（应用配置变更）
openclaw gateway stop      # 停止
```

- **macOS**：LaunchAgent（`ai.openclaw.gateway`），路径：`~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- **Linux / WSL2**：systemd 用户服务（`openclaw-gateway.service`）

## 2. 配置管理

配置文件为 JSON5 格式（支持注释和尾逗号）。

| 编辑方式           | 命令/操作                           |
| ------------------ | ----------------------------------- |
| 配置向导           | `openclaw onboard`                  |
| CLI                | `openclaw config set <key> <value>` |
| Web 控制面板       | `openclaw dashboard`                |
| 直接编辑（不推荐） | 手动改 JSON 容易出错                |

**配置写错会怎样**：Gateway 拒绝启动，运行 `openclaw doctor` 查看原因，`openclaw doctor --fix` 自动修复。

**配置热更新**

通过 CLI 修改配置后**大部分设置自动生效，无需重启**。只有 `gateway.*`（端口、绑定、认证、TLS）和 `discovery`、`plugins` 等基础设施字段需要重启。

<details>
<summary>热更新 vs 需要重启：完整对照表</summary>
| 类别           | 字段                                          | 需要重启？ |
| -------------- | --------------------------------------------- | ---------- |
| 渠道           | `channels.*`、`web`                           | 否         |
| Agent 与模型   | `agent`、`agents`、`models`、`routing`        | 否         |
| 自动化         | `hooks`、`cron`、`agent.heartbeat`            | 否         |
| 会话与消息     | `session`、`messages`                         | 否         |
| 工具与媒体     | `tools`、`browser`、`skills`、`audio`、`talk` | 否         |
| UI 与杂项      | `ui`、`logging`、`identity`、`bindings`       | 否         |
| Gateway 服务器 | `gateway.*`（端口、绑定、认证、TLS、HTTP）    | **是**     |
| 基础设施       | `discovery`、`canvasHost`、`plugins`          | **是**     |

> `gateway.reload` 和 `gateway.remote` 是例外——修改它们不会触发重启。

<details>
<summary>环境变量</summary>
OpenClaw 读取环境变量的优先级：

1. 父进程传入的环境变量
2. 当前工作目录的 `.env` 文件
3. `~/.openclaw/.env`（全局兜底）

`.env` 文件不会覆盖已有的环境变量。你也可以在配置文件中内联设置：

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

如果 Gateway 运行在 systemd/launchd 下，建议把 API Key 放在 `~/.openclaw/.env` 中，确保守护进程能读取。

<details>
<summary>配置 RPC（程序化更新）</summary>
控制面板写操作（`config.apply`、`config.patch`、`update.run`）有速率限制：每 60 秒最多 3 次请求（按 deviceId + clientIp 计算）。超限时返回 `UNAVAILABLE` 和 `retryAfterMs`。

<details>
<summary>常用配置模板</summary>
**推荐起步配置**：

```json5
{
  identity: {
    name: "Clawd",
    theme: "helpful assistant",
    emoji: "🦞",
  },
  agent: {
    workspace: "~/.openclaw/workspace",
    model: { primary: "anthropic/claude-sonnet-4-5" },
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

**多平台配置**：

```json5
{
  agent: { workspace: "~/.openclaw/workspace" },
  channels: {
    whatsapp: { allowFrom: ["+15555550123"] },
    telegram: {
      enabled: true,
      botToken: "YOUR_TOKEN",
      allowFrom: ["123456789"],
    },
    discord: {
      enabled: true,
      token: "YOUR_TOKEN",
      dm: { allowFrom: ["123456789012345678"] },
    },
  },
}
```

**纯本地模型**：

```json5
{
  agent: {
    workspace: "~/.openclaw/workspace",
    model: { primary: "lmstudio/minimax-m2.5-gs32" },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## 3. 认证与安全

Gateway 默认只监听本机（`127.0.0.1`）。**如需从外部访问（LAN、Tailnet），必须配置认证**，否则 Gateway 拒绝启动。

```json5
{
  gateway: {
    bind: "loopback",  // loopback | lan | tailnet | custom
    auth: { mode: "token", token: "你的网关密码" },
  },
}
```

**模型 API Key**

推荐放在 `~/.openclaw/.env`（守护进程场景必须放这里）：

```bash
cat >> ~/.openclaw/.env <<'EOF'
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
EOF

openclaw models status   # 验证
```

<details>
<summary>密钥管理（SecretRef）</summary>
对于生产环境，OpenClaw 支持 **SecretRef**——不需要把密钥明文写在配置文件中。支持三种来源：

**环境变量引用**：

```json5
{ source: "env", provider: "default", id: "OPENAI_API_KEY" }
```

**文件引用**：

```json5
{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }
```

**外部命令引用**（支持 1Password、HashiCorp Vault、sops 等）：

```json5
{ source: "exec", provider: "vault", id: "providers/openai/apiKey" }
```

配置密钥提供者：

```json5
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json",
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        args: ["--profile", "prod"],
        passEnv: ["PATH", "VAULT_ADDR"],
      },
    },
  },
}
```

密钥管理命令：

```bash
openclaw secrets audit --check    # 检查明文密钥
openclaw secrets configure        # 交互式配置 SecretRef
openclaw secrets reload           # 刷新密钥快照
```

SecretRef 解析是**启动时一次性完成**的（不是每次请求时），解析失败会阻止 Gateway 启动。运行时使用内存中的快照，避免密钥提供者故障影响请求路径。

**1Password 集成示例**：

```json5
{
  secrets: {
    providers: {
      onepassword_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/op",
        allowSymlinkCommand: true,
        trustedDirs: ["/opt/homebrew"],
        args: ["read", "op://Personal/OpenClaw QA API Key/password"],
        passEnv: ["HOME"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "onepassword_openai", id: "value" },
      },
    },
  },
}
```

<details>
<summary>反向代理认证（Trusted Proxy）</summary>
如果 OpenClaw 运行在身份感知代理（Pomerium、Caddy + OAuth、nginx + oauth2-proxy）后面，可以使用 `trusted-proxy` 模式：

```json5
{
  gateway: {
    bind: "loopback",
    trustedProxies: ["10.0.0.1"],
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user",
        allowUsers: ["nick@example.com"],
      },
    },
  },
}
```

**nginx + oauth2-proxy 示例**：

```nginx
location / {
    auth_request /oauth2/auth;
    auth_request_set $user $upstream_http_x_auth_request_email;

    proxy_pass http://openclaw:18789;
    proxy_set_header X-Auth-Request-Email $user;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

> **安全警告**：此模式将认证完全委托给代理。必须确保：代理是唯一入口、`trustedProxies` 最小化、代理会覆盖（而非追加）转发头。启用后 `openclaw security audit` 会标记为 critical——这是故意的提醒。



<details>
<summary>安全审计与安全模型</summary>
定期运行安全审计（特别是修改配置或暴露网络后）：

```bash
openclaw security audit           # 基本审计
openclaw security audit --deep    # 深度审计
openclaw security audit --fix     # 自动修复
```

它会检查：Gateway 认证暴露、浏览器控制暴露、提权 allowlist、文件权限等常见问题。

**核心安全原则**：OpenClaw 采用**个人助理信任模型**——每个 Gateway 一个可信操作者。它不是敌对多租户安全边界。如果需要多用户隔离，应分开 Gateway + 凭证（最好分开操作系统用户/主机）。

## 4. 日志与健康检查

### 查看日志

```bash
openclaw logs --follow          # 实时
openclaw logs --limit 100       # 最近 100 条
openclaw logs --limit 100 --json  # JSON 格式
```

日志文件默认在 `/tmp/openclaw/openclaw-YYYY-MM-DD.log`。`--verbose` 只影响控制台输出；要在文件日志中捕获详细信息，设置 `logging.level: "debug"`。

<details>
<summary>日志级别配置</summary>
```json5
{
  logging: {
    level: "info",           // 文件日志级别
    consoleLevel: "info",    // 控制台日志级别
    consoleStyle: "pretty",  // pretty | compact | json
    redactSensitive: "tools",
  },
}
```

### 健康检查

```bash
openclaw status          # 总体状态（Gateway、渠道、会话）
openclaw status --deep   # 深度检查（含渠道探测）
openclaw health --json   # JSON 格式快照
```

### Doctor 自动诊断

遇到任何问题，先跑 `openclaw doctor`——它会自动检测并修复大多数常见问题。

```bash
openclaw doctor          # 交互式诊断
openclaw doctor --fix    # 自动修复
openclaw doctor --deep   # 扫描多余 Gateway 安装
```

<details>
<summary>Doctor 检查项完整列表</summary>
1. **可选更新**（git 安装时可选拉取最新代码）
2. **UI 协议刷新**（Protocol Schema 更新时重建控制面板 UI）
3. **健康检查 + 重启提示**
4. **技能状态摘要**（可用/缺失/阻塞）
5. **配置规范化**（遗留值格式迁移）
6. **OpenCode 提供商覆盖警告**
7. **遗留磁盘布局迁移**（会话、Agent 目录、WhatsApp 认证）
8. **遗留 Cron 存储迁移**
9. **状态完整性检查**（目录缺失、权限、云同步警告）
10. **模型认证健康**（OAuth 过期、冷却/禁用状态）
11. **Hooks 模型验证**
12. **沙箱镜像修复**
13. **Gateway 服务迁移和清理**
14. **安全警告**
15. **systemd linger 检查**（Linux）
16. **技能状态**
17. **Gateway 认证检查**
18. **运行时与端口诊断**
19. **运行时最佳实践**（Node vs Bun 检查）

## 5. Heartbeat 心跳机制

心跳让龙虾定时主动检查——不是被动等消息，而是主动巡逻。每次心跳都是完整的 Agent 对话轮，**间隔越短越烧 Token**。

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",   // 每 30 分钟一次
        target: "last", // 发送到最近联系的渠道
      },
    },
  },
}
```

在工作区创建 `~/.openclaw/workspace/HEARTBEAT.md` 告诉龙虾检查什么。没有需要关注的事情时，龙虾回复 `HEARTBEAT_OK` 并静默；有重要事项才发送提醒。

```markdown
# 心跳检查清单

- 快速扫描：收件箱有紧急邮件吗？
- 如果某个任务被阻塞，在下次对话时提醒我
```

> 省钱：保持 `HEARTBEAT.md` 简短，或设置 `target: "none"` 只内部运行不发消息。

<details>
<summary>心跳高级配置</summary>
**活跃时段**（避免深夜打扰）：

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
        activeHours: {
          start: "09:00",
          end: "22:00",
          timezone: "Asia/Shanghai",
        },
      },
    },
  },
}
```

**多 Agent 独立心跳**：

```json5
{
  agents: {
    defaults: {
      heartbeat: { every: "30m", target: "last" },
    },
    list: [
      { id: "main", default: true },
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "telegram",
          to: "12345678",
          prompt: "检查服务器状态，如果一切正常回复 HEARTBEAT_OK。",
        },
      },
    ],
  },
}
```

**可见性控制**（按渠道定制）：

- `showOk: false`（默认）：静默吞掉 `HEARTBEAT_OK`
- `showAlerts: true`（默认）：发送告警内容
- `useIndicator: true`（默认）：发出指示器事件

**手动触发心跳**：

```bash
openclaw system event --text "检查紧急跟进事项" --mode now
```

**轻量上下文模式**：

设置 `lightContext: true` 让心跳只注入 `HEARTBEAT.md`，减少上下文大小和 Token 消耗。

**推理过程透传**：

设置 `includeReasoning: true` 额外发送 `Reasoning:` 前缀的推理过程消息，方便了解龙虾为什么决定通知你。建议在群聊中关闭此选项。

## 6.常用命令速查表

### ⭐ 日常管理

```bash
openclaw gateway status              # 查看网关是否在运行
openclaw gateway start               # 启动网关服务
openclaw gateway stop                # 停止网关服务
openclaw gateway restart             # 重启（修改配置后需要重启生效）
```

### 启动选项

需要自定义启动方式时使用：

```bash
openclaw gateway --port 18789 --verbose     # 前台运行（调试模式，日志直接输出）
openclaw gateway --bind loopback            # 仅本机访问（默认，最安全）
openclaw gateway --bind lan                 # 局域网访问
openclaw gateway --bind tailnet             # Tailscale 网络访问
openclaw gateway --auth token --token <t>   # Token 认证
openclaw gateway --auth password --password <p>  # 密码认证
openclaw gateway --tailscale serve|funnel   # 通过 Tailscale 暴露服务
openclaw gateway --dev                      # 开发模式
```

### 服务安装

```bash
openclaw gateway install             # 安装为系统服务（开机自启）
openclaw gateway uninstall           # 卸载系统服务
```

### 健康检查

```bash
openclaw health                      # 🔧 网关健康状态
openclaw health --json               # JSON 格式输出（适合脚本解析）
openclaw health --verbose            # 详细信息
openclaw gateway call <method> --params '<json>'  # 🔧 直接调用网关 RPC 方法
```

> 详见[第 8 章 Gateway 运维与管理](/cn/adopt/chapter8/)。

# 第五章 聊天平台接入

> 完成本章内容，你就能在手机上跟龙虾对话了。

## 0. 支持哪些聊天平台？

OpenClaw 支持几乎所有主流聊天软件，文字消息全渠道可用。

| 渠道                | 说明                                    | 安装方式 |
| ------------------- | --------------------------------------- | -------- |
| **飞书 / Lark**     | WebSocket 长连接；企业协作首选          | 内置     |
| **微信**            | WorkBuddy 桥接；个人号/企业微信         | 插件     |
| **QQ**              | QQ 开放平台 Bot API                     | 插件     |
| **WhatsApp**        | 全球最流行；Baileys 库，需 QR 配对      | 内置     |
| **Telegram**        | Bot API（grammY）；支持群聊，API 最开放 | 内置     |
| **Discord**         | Bot API + Gateway；服务器、频道、私信   | 内置     |
| **Slack**           | Bolt SDK；工作区应用                    | 内置     |
| **Signal**          | signal-cli；注重隐私                    | 内置     |
| **Google Chat**     | Google Chat API；HTTP webhook           | 内置     |
| **iMessage**        | BlueBubbles（推荐）或旧版 imsg CLI      | 内置     |
| **IRC**             | 经典 IRC 服务器；频道 + 私信            | 内置     |
| **WebChat**         | Gateway 内置 Web 聊天界面               | 内置     |
| **LINE**            | LINE Messaging API                      | 插件     |
| **Matrix**          | Matrix 开放协议                         | 插件     |
| **Mattermost**      | Bot API + WebSocket                     | 插件     |
| **Microsoft Teams** | Bot Framework；企业支持                 | 插件     |
| **Nostr**           | 去中心化协议 NIP-04                     | 插件     |
| **Twitch**          | IRC 连接                                | 插件     |
| **Zalo**            | Zalo Bot API（越南）                    | 插件     |

> 多个平台可以同时接入吗？
> 可以。OpenClaw 会按来源自动路由消息，飞书处理工作、Telegram 做个人助理，共享同一个 AI 大脑。

本章以**飞书**为例——国内办公场景首选，深度集成文档、日历、多维表格，Telegram 配置更简单但国内需代理。

## 1. 创建飞书应用

### 第一步：登录飞书开放平台

访问 [飞书开放平台](https://open.feishu.cn/app)，使用飞书账号登录。

![飞书开放平台首页](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark.png)

### 第二步：创建企业自建应用

点击"创建企业自建应用"，填写名称（如"OpenClaw 助理"）和描述，点击"创建"。

### 第三步：获取应用凭证

进入"凭证与基础信息"，复制 **App ID**（格式 `cli_xxx`）和 **App Secret**，妥善保存。

![飞书应用凭证页面](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark-credential.png)

### 第四步：启用机器人能力

进入"添加应用能力" → "机器人"，点击"添加"。

![添加应用能力页面](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark-app.png)

> **必须先做这步**：否则下一步导入权限时，消息相关权限无法开通。

### 第五步：配置权限

进入"权限管理"，点击"批量导入"，粘贴下方 JSON：

![飞书权限管理页面](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark-authentication.png)

```json
{
  "scopes": {
    "tenant": [
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:read",
      "cardkit:card:write",
      "contact:contact.base:readonly",
      "contact:user.employee_id:readonly",
      "docs:document.content:read",
      "docx:document:readonly",
      "event:ip_list",
      "im:chat",
      "im:chat.members:bot_access",
      "im:chat:read",
      "im:chat:update",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.group_msg",
      "im:message.p2p_msg:readonly",
      "im:message.pins:read",
      "im:message.pins:write_only",
      "im:message.reactions:read",
      "im:message.reactions:write_only",
      "im:message:readonly",
      "im:message:recall",
      "im:message:send_as_bot",
      "im:message:send_multi_users",
      "im:message:send_sys_msg",
      "im:message:update",
      "im:resource",
      "sheets:spreadsheet",
      "wiki:wiki:readonly"
    ],
    "user": [
      "base:app:copy",
      "base:app:create",
      "base:app:read",
      "base:app:update",
      "base:field:create",
      "base:field:delete",
      "base:field:read",
      "base:field:update",
      "base:record:create",
      "base:record:delete",
      "base:record:retrieve",
      "base:record:update",
      "base:table:create",
      "base:table:delete",
      "base:table:read",
      "base:table:update",
      "base:view:read",
      "base:view:write_only",
      "board:whiteboard:node:create",
      "board:whiteboard:node:read",
      "calendar:calendar.event:create",
      "calendar:calendar.event:delete",
      "calendar:calendar.event:read",
      "calendar:calendar.event:reply",
      "calendar:calendar.event:update",
      "calendar:calendar.free_busy:read",
      "calendar:calendar:read",
      "contact:contact.base:readonly",
      "contact:user.base:readonly",
      "contact:user.employee_id:readonly",
      "contact:user:search",
      "docs:document.comment:create",
      "docs:document.comment:read",
      "docs:document.comment:update",
      "docs:document.media:download",
      "docs:document:copy",
      "docx:document:create",
      "docx:document:readonly",
      "docx:document:write_only",
      "drive:drive.metadata:readonly",
      "drive:file:download",
      "drive:file:upload",
      "im:chat.members:read",
      "im:chat:read",
      "im:message",
      "im:message.group_msg:get_as_user",
      "im:message.p2p_msg:get_as_user",
      "im:message:readonly",
      "offline_access",
      "search:docs:read",
      "search:message",
      "space:document:delete",
      "space:document:move",
      "space:document:retrieve",
      "task:comment:read",
      "task:comment:write",
      "task:task:read",
      "task:task:write",
      "task:task:writeonly",
      "task:tasklist:read",
      "task:tasklist:write",
      "wiki:node:copy",
      "wiki:node:create",
      "wiki:node:move",
      "wiki:node:read",
      "wiki:node:retrieve",
      "wiki:space:read",
      "wiki:space:retrieve",
      "wiki:space:write_only"
    ]
  }
}
```

> 这一包权限涵盖消息收发、云文档、多维表格、日历、任务等完整能力。

<details>
<summary>这些权限分别做什么？</summary>

| 权限类别                     | 代表权限                                                     | 用途                       |
| ---------------------------- | ------------------------------------------------------------ | -------------------------- |
| **应用管理（application:）** | `application:application:self_manage`、`application:bot.menu:write` | 应用自管理、机器人菜单配置 |
| **消息卡片（cardkit:）**     | `cardkit:card:read`、`cardkit:card:write`                    | 读写消息卡片               |
| **消息（im:）**              | `im:message`、`im:message:send_as_bot`、`im:resource`        | 收发消息、图片、文件       |
| **群聊（im:chat）**          | `im:chat`、`im:chat.members:bot_access`                      | 群聊管理、成员访问         |
| **联系人（contact:）**       | `contact:user.base:readonly`、`contact:user.employee_id:readonly` | 获取用户基础信息           |
| **云文档（docx:/docs:）**    | `docx:document:create`、`docs:document.content:read`         | 创建和读取飞书文档         |
| **电子表格（sheets:）**      | `sheets:spreadsheet`                                         | 操作飞书电子表格           |
| **多维表格（base:）**        | `base:record:create`、`base:table:read`                      | 操作多维表格数据           |
| **日历（calendar:）**        | `calendar:calendar.event:create`、`calendar:calendar.event:read` | 管理日程                   |
| **任务（task:）**            | `task:task:read`、`task:task:write`                          | 创建和管理飞书任务         |
| **知识库（wiki:）**          | `wiki:node:read`、`wiki:wiki:readonly`                       | 读写飞书知识库             |
| **云空间（drive:/space:）**  | `drive:file:upload`、`drive:file:download`                   | 上传下载文件               |
| **白板（board:）**           | `board:whiteboard:node:create`、`board:whiteboard:node:read` | 读写飞书白板               |
| **搜索（search:）**          | `search:docs:read`、`search:message`                         | 搜索文档和消息             |
| **事件（event:）**           | `event:ip_list`                                              | 事件推送 IP 白名单         |

如果你只需要基础聊天功能，最少只需 `im:message`、`im:message.p2p_msg:readonly`、`im:message.group_at_msg:readonly`、`im:message:send_as_bot`、`im:resource` 这几个消息相关权限即可。但建议导入完整权限以获得最佳体验。

导入后点击"申请开通"确认。

### 第六步：发布应用

进入"版本管理与发布"，点击"创建版本"，填写版本号后提交发布申请。管理员审批通过即生效（你本人是管理员可直接通过）。

![版本管理与发布页面](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark-version.png)

## 2. 在 OpenClaw 中添加飞书渠道

回到终端，运行：

```bash
openclaw channels add
```

选择"Feishu/Lark（飞书）"，输入 App ID 和 App Secret，其余保持默认。

添加后重启网关：

```bash
openclaw gateway restart
openclaw gateway status
```

确认 feishu 渠道状态为 **connected**：

```
openclaw status

Channels
┌──────────┬─────────┬────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Channel  │ Enabled │ State  │ Detail                                                                                                                                   │
├──────────┼─────────┼────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Feishu   │ ON      │ OK     │ configured                                                                                                                               │
└──────────┴─────────┴────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

不想用交互式向导？也可以一行 CLI 命令搞定：

```bash
openclaw channels add \
    --channel feishu \
    --token "cli_xxx:你的App Secret"

openclaw gateway restart
```

> **不推荐**直接编辑配置文件——手动改 JSON 容易漏逗号或括号导致配置解析失败。始终优先使用 CLI 命令。


## 3. 配置事件订阅

> 此步必须在上一步（添加渠道 + 启动网关）之后进行。飞书在保存长连接配置时会实时检测 WebSocket 连接——如果 OpenClaw 网关未运行，飞书会报"未检测到应用连接信息"错误，无法保存。

回到飞书开放平台，进入"事件与回调" → "事件配置"：

![事件与回调页面](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark-event.png)

1. 选择"**使用长连接接收事件**"
2. 添加事件：`im.message.receive_v1`

<details>
<summary>为什么用长连接而不是 Webhook？</summary>

Webhook 需要公网 IP，长连接（WebSocket）由 OpenClaw 主动连飞书——不需要公网 IP、不需要域名、家用网络就能用。

## 4. 配对与首次对话

在飞书中找到你的机器人，发送"你好"。机器人会回复一个 **8 位配对码**：

![飞书配对码提示界面](E:/hello-claw - yw/docs/cn/adopt/chapter4/images/lark-pairing.jpg)

<details>
<summary>为什么要配对？</summary>

防止陌生人滥用你的机器人——每次对话都消耗你的 API 额度。新用户第一次发消息时会收到配对码，只有你批准后才能正常对话。配对码 1 小时过期。



在终端批准：

```bash
openclaw pairing approve feishu <配对码>
```

例如：`openclaw pairing approve feishu 6KKG7C7K`。也可在 Web 控制面板（`openclaw dashboard`）中点击批准。

配对成功后，飞书里的龙虾就能回你了。试试：

```
你好，请介绍一下你自己
```

## 5. 群聊中使用

把机器人拉进飞书群，**@机器人** 触发回复。

<details>
<summary>群聊访问控制</summary>

OpenClaw 通过 `groupPolicy` 控制群聊行为：

| 策略          | 行为                           |
| ------------- | ------------------------------ |
| `"open"`      | 允许所有群聊，仍需 @提及才回复 |
| `"allowlist"` | 仅允许白名单中的群（默认）     |
| `"disabled"`  | 禁用所有群聊消息               |

配置示例：

```bash
# 允许所有群聊
openclaw config set channels.feishu.groupPolicy "open"


```

群聊中每个群拥有独立的会话——群里的对话不会影响你和机器人的私聊记录。



<details>
<summary>私聊访问策略（dmPolicy）</summary>

`dmPolicy` 控制谁能通过私聊使用你的机器人：

| 策略          | 行为                                        |
| ------------- | ------------------------------------------- |
| `"pairing"`   | 默认。新用户需配对码批准                    |
| `"allowlist"` | 仅允许 `allowFrom` 列表中的用户             |
| `"open"`      | 允许所有人（需在 `allowFrom` 中设置 `"*"`） |
| `"disabled"`  | 禁用私聊                                    |



**设置某个群不需要@就回复**

Agent绑定到飞书，这样就有多个数字员工，每个员工一个独立对话框，（但实际是一个群聊，需要解决群聊每次都要@的这问题）
群聊不需要@： 

方法一：CLI

```
openclaw config set channels.feishu.groups.<群ID>.requireMention false
```

方法二：

Dashbord: http://192.168.0.166:18789/  -> 配置 -> Channels -> Require Mention   开一次 再关一次 ，这样配置文件里多了一行： requireMention: false,

方法三： 
修改配置文件 `~/.openclaw/openclaw.json`

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

## 6.常用命令速查表

### ⭐ 添加渠道

```bash
openclaw channels add                # 交互式添加（推荐，有引导）

# 非交互式添加示例：
openclaw channels add \
  --channel telegram \
  --account alerts \
  --name "Alerts Bot" \
  --token $TELEGRAM_BOT_TOKEN

openclaw channels add \
  --channel discord \
  --account work \
  --name "Work Bot" \
  --token $DISCORD_BOT_TOKEN
```

### 查看状态

```bash
openclaw channels list               # ⭐ 列出所有已添加渠道
openclaw channels list --json        # JSON 格式
openclaw channels status             # 查看各渠道连接状态
openclaw channels status --probe     # 主动探测连接（更准确）
openclaw channels logs               # 查看渠道日志
openclaw channels logs --channel <name> --limit 200  # 指定渠道、限制条数
```

### 移除渠道

```bash
openclaw channels remove --channel <channel> --account <id>
openclaw channels remove --channel <channel> --account <id> --delete  # 同时删除数据
```

### 登录 / 登出（WhatsApp 等需要扫码的平台）

```bash
openclaw channels login              # 打开扫码登录
openclaw channels login --channel whatsapp --account <id> --verbose
openclaw channels logout             # 登出
openclaw channels logout --channel <channel> --account <id>
```

### ⭐ 配对管理

配对是 OpenClaw 的安全机制——新用户首次对话时需要审批。

```bash
openclaw pairing list                # 查看待审批配对请求
openclaw pairing approve <channel> <code>           # 批准配对
openclaw pairing approve --channel <channel> <code> --notify  # 批准并通知对方
```

> 详见[第 4 章 Chat Provider 配置](/cn/adopt/chapter4/)。



# 第六章 模型管理篇

> 学完本章，你的龙虾就能换上任何你想要的 AI 大脑——免费的、最强的、本地的，甚至在一个挂掉时自动切换到另一个。

---

## 0. 先搞清楚：模型和提供商是什么？

OpenClaw 本身没有 AI 大脑，你选哪个大脑，它就用哪个。

模型标识格式是 `提供商/模型名`，比如：

| 标识                                     | 含义                    |
| ---------------------------------------- | ----------------------- |
| `openrouter/stepfun/step-3.5-flash:free` | OpenRouter 上的免费模型 |
| `anthropic/claude-opus-4-6`              | Anthropic 的旗舰模型    |
| `openai/gpt-5.1-codex`                   | OpenAI 的编程专用模型   |
| `ollama/llama3.3`                        | 你电脑上本地运行的模型  |

模型提供商可分为四大类：

| 分类         | 代表                                    | 适合谁                                 |
| ------------ | --------------------------------------- | -------------------------------------- |
| **聚合网关** | OpenRouter、硅基流动                    | 一个 Key 用多家模型，入门首选          |
| **国内直连** | DeepSeek、Qwen、GLM、Kimi、豆包、混元等 | 国内网络直连、支付宝付款、低延迟       |
| **国际直连** | OpenAI、Anthropic、Google、xAI、Mistral | 追求最强模型能力，需科学上网或海外节点 |
| **本地部署** | Ollama、LM Studio                       | 完全离线、零成本、数据不出本机         |



## 1. 配置模型

查看模型清单：`openclaw models list `

```
openclaw models list 

🦞 OpenClaw 2026.3.13 (61d171a) — Hot reload for config, cold sweat for deploys.

Model                                      Input      Ctx      Local Auth  Tags
openrouter/auto                            text+image 195k     no    yes   default,configured,alias:OpenRouter
custom-api-siliconflow-cn/Qwen/Qwen3-8B    text       16k      no    yes   fallback#1,configured
minimax-cn/MiniMax-M2.5                    text       195k     no    yes   fallback#2,configured,alias:Minimax
kimi-coding/k2p5                           text+image 256k     no    yes   fallback#3,configured,alias:Kimi for Coding
```

配置模型： `openclaw onboard`

```
(base) will@MacMini-Will extensions % openclaw onboard

🦞 OpenClaw 2026.3.13 (61d171a) — Your personal assistant, minus the passive-aggressive calendar reminders.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞                    
 
│
◇  Model/auth provider
│  OpenRouter
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
└  Onboarding complete. Dashboard opened; keep that tab to control OpenClaw.
```



###  聚合网关（推荐入门）

不想注册一堆账号？聚合网关让你用**一个 API Key 访问多家模型**，还能在模型之间自由切换。

**聚合网关对比**

|                   | OpenRouter              | 硅基流动            |
| ----------------- | ----------------------- | ------------------- |
| **模型数量**      | 300+                    | 200+                |
| **免费模型**      | ✅ 多个                  | ✅ 部分              |
| **新用户福利**    | —                       | ¥16 免费额度        |
| **国内直连**      | 部分地区                | ✅                   |
| **支付宝**        | ❌                       | ✅                   |
| **OpenClaw 集成** | ✅ 原生支持              | ✅ 原生支持          |
| **适合谁**        | 海外用户 / 想用免费模型 | 国内用户 / 付费首选 |



#### OpenRouter

[OpenRouter](https://openrouter.ai) 是全球最大的模型聚合网关，接入 300+ 模型，包括 OpenAI、Anthropic、Google、Meta、Mistral、DeepSeek 等几乎所有主流提供商。

**核心优势：**

- **有免费模型**：`stepfun/step-3.5-flash:free`、`google/gemma-3-4b-it:free` 等，零成本入门
- **一个 Key 用所有模型**：注册后生成一个 API Key，通过 `provider/model-name` 格式切换模型
- **透明定价**：在每个模型页面直接显示价格，按用量付费，无月费
- **中国可访问**：部分地区可直连，或通过硅基流动等国内代理访问

**定价模式：**

- 免费模型：$0（有速率限制）
- 付费模型：按各提供商原价 + 小幅加价（通常 5-15%）
- 支付方式：国际信用卡、Crypto

**Openclaw onboard配置：**

```
(base) will@MacMini-Will extensions % openclaw onboard

🦞 OpenClaw 2026.3.13 (61d171a) — Less clicking, more shipping, fewer "where did that file go" moments.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞                    
 
┌  OpenClaw onboarding
│

◇  Model/auth provider
│  OpenRouter
│
◇  Model configured ─────────────────────╮
│                                        │
│  Default model set to openrouter/auto  │
│                                        │
├────────────────────────────────────────╯
18:43:48 [agents/model-providers] Failed to discover vLLM models: TypeError: fetch failed
│
◇  Default model
│  openrouter/stepfun/step-3.5-flash:free
18:43:57 [agents/model-providers] Failed to discover vLLM models: TypeError: fetch failed
[info]: [ 'client ready' ]
```



**CLI配置：**

```bash
# 环境变量
export OPENROUTER_API_KEY="sk-or-v1-..."

# 设置模型
openclaw models set openrouter/stepfun/step-3.5-flash:free
```



####  SiliconFlow

[硅基流动](https://cloud.siliconflow.cn) 是国内领先的模型聚合平台，提供 200+ 开源和商用模型的统一 API 接口。

**核心优势：**

- **新用户送 ¥16**：注册即送，足够体验数天
- **国内直连**：无需科学上网，低延迟
- **支付宝付款**：对国内用户最友好
- **模型丰富**：DeepSeek、Qwen、GLM、Llama、Mistral 等全覆盖
- **有免费模型**：部分开源模型提供免费推理额度

**定价模式：**

- 新用户：¥16 免费额度
- 按量付费：不同模型价格不同，通常比直连略高
- 充值方式：支付宝、微信支付

**OpenClaw 配置：**

参考： https://docs.siliconflow.cn/cn/usercases/use-siliconcloud-in-OpenClaw

```bash
(base) will@MacMini-Will extensions % openclaw onboard


▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞                    
 
┌  OpenClaw onboarding
│
◇  Model/auth provider
│  Custom Provider
│
◇  API Base URL
│  https://api.siliconflow.cn/v1
│
◇  How do you want to provide this API key?
│  Paste API key now
│
◇  API Key (leave blank if not required)
│  YOUR_API_KEY
│
◇  Endpoint compatibility
│  OpenAI-compatible
│
◇  Model ID
│  Qwen/Qwen3-8B
│
◇  Verification successful.
│
◇  Endpoint ID
│  custom-api-siliconflow-cn
│
◇  Model alias (optional)
│  s-qwen3-8b
Configured custom provider: custom-api-siliconflow-cn/Qwen/Qwen3-8B
18:38:26 [agents/model-providers] Failed to discover vLLM models: TypeError: fetch failed
[info]: [ 'client ready' ]
```

或者修改配置文件`~/.openclaw/openclaw.json`

```
"models": {
    "providers": {
      "siliconflow": {
        "baseUrl": "https://api.siliconflow.cn/v1",
        "apiKey": "您的_SILICONFLOW_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "Qwen/Qwen3-8B",
            "name": "s-qwen3-8b",
            "reasoning": false,
            "input": [
              "text"
            ],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      },
```


---

### 国内模型提供商

国内提供商的共同优势：**直连无需科学上网**、**支付宝/微信支付**、**中文优化好**。

**一键对比**

| 提供商       | 旗舰模型        | 输入价格 (¥/百万token) | 输出价格 (¥/百万token) | 免费额度        | 上下文 | 特色                   |
| ------------ | --------------- | ---------------------- | ---------------------- | --------------- | ------ | ---------------------- |
| **DeepSeek** | DeepSeek V3     | 1                      | 2                      | 新用户送额度    | 128K   | 性价比之王，推理能力强 |
| **DeepSeek** | DeepSeek R1     | 4                      | 16                     | —               | 128K   | 深度推理，数学/编程    |
| **通义千问** | Qwen3.5-plus    | 2                      | 6                      | 有免费额度      | 128K   | 阿里系，中文理解好     |
| **智谱**     | GLM-5           | 5                      | 5                      | 新用户送额度    | 128K   | 学术背景，工具调用强   |
| **月之暗面** | Kimi K2.5       | 8                      | 8                      | 有限免费        | 256K   | 超长上下文             |
| **豆包**     | Doubao-Seed-2.0 | 0.3                    | 0.6                    | Coding Plan 含  | 128K   | 字节系，极致低价       |
| **混元**     | hunyuan-lite    | **免费**               | **免费**               | **无限量**      | 32K    | 腾讯免费模型           |
| **混元**     | hunyuan-pro     | 15                     | 50                     | —               | 128K   | 腾讯旗舰               |
| **MiniMax**  | MiniMax-M2.5    | 1                      | 4                      | 欢迎积分        | 200K+  | MoE 架构，多模态       |
| **阶跃星辰** | Step-3.5-flash  | 免费(via OR)           | 免费(via OR)           | OpenRouter 免费 | 128K   | 通过 OpenRouter 免费用 |
| **文心**     | ERNIE-4.5-turbo | 4                      | 12                     | 有免费额度      | 128K   | 百度系                 |

> **价格说明**：以上为 API 直连价格（2026 年 3 月），通过聚合网关（硅基流动/OpenRouter）使用时价格可能略有不同。

### 国际模型提供商

国际提供商通常提供最前沿的模型能力，但**需要科学上网**且**需国际信用卡支付**。如果你在国内且不方便直连，可以通过 [OpenRouter](#_3-1-openrouter) 或 [硅基流动](#_3-2-硅基流动-siliconflow) 间接使用这些模型。

**一键对比**

| 提供商         | 旗舰模型          | 输入价格 ($/百万token) | 输出价格 ($/百万token) | 免费额度   | 上下文 | 特色                  |
| -------------- | ----------------- | ---------------------- | ---------------------- | ---------- | ------ | --------------------- |
| **OpenAI**     | GPT-5             | ~30                    | ~60                    | ❌          | 128K   | 综合最强，生态最完善  |
| **OpenAI**     | GPT-4o            | ~2.5                   | ~10                    | ❌          | 128K   | 高性价比多模态        |
| **OpenAI**     | o3                | ~15                    | ~60                    | ❌          | 200K   | 深度推理              |
| **Anthropic**  | Claude Opus 4.5   | ~15                    | ~75                    | ❌          | 200K   | 编程最强，超长输出    |
| **Anthropic**  | Claude Sonnet 4.5 | ~3                     | ~15                    | ❌          | 200K   | 性价比编程            |
| **Google**     | Gemini 2.5 Pro    | ~1.25                  | ~10                    | ✅ 免费层   | **1M** | 超长上下文之王        |
| **Google**     | Gemini 2.5 Flash  | ~0.15                  | ~0.6                   | ✅ 免费层   | 1M     | 极致性价比            |
| **xAI**        | Grok 4            | ~5                     | ~15                    | ✅ 免费积分 | 128K   | 实时信息（X/Twitter） |
| **Mistral**    | Mistral Large     | ~2                     | ~6                     | ✅ 免费层   | 128K   | 欧洲开源领军          |
| **Mistral**    | Codestral         | ~0.3                   | ~0.9                   | ✅ 免费层   | 256K   | 代码专用，FIM 支持    |
| **Perplexity** | Sonar Pro         | ~3                     | ~15                    | ❌          | 128K   | 搜索增强，带引用      |

> **价格说明**：以上为 2026 年 3 月参考价格，实际价格请以各提供商官网为准。OpenAI/Anthropic 价格波动较频繁。

### 本地部署

不想把数据发送到云端？本地部署让模型完全在你的电脑上运行——**零成本、零延迟、完全隐私**。代价是需要足够的硬件资源，且模型能力通常弱于云端旗舰。

对比 **Ollama**、**vLLM** 和 **Xinference** 这三个主流推理引擎。这三者在定位上有本质区别：**Ollama** 主打轻量和易用（本地玩具），**vLLM** 主打性能和吞吐（云端利器），而 **Xinference** 主打功能和灵活性（企业级全能）。

**📊 核心对比一览表**

| 维度         | **Ollama**                   | **vLLM**                               | **Xinference**                            |
| ------------ | ---------------------------- | -------------------------------------- | ----------------------------------------- |
| **定位**     | **本地开发 & 个人玩具**      | **高性能推理 & API服务**               | **企业级多功能引擎**                      |
| **核心技术** | llama.cpp (量化/CPU友好)     | **PagedAttention** (显存复用)          | PyTorch / 分布式调度                      |
| **部署难度** | ⭐ (极简，一键安装)           | ⭐⭐⭐⭐ (依赖CUDA/Python环境)             | ⭐⭐⭐ (Python依赖，自带UI)                  |
| **硬件门槛** | **极低** (CPU/Mac M芯片友好) | **极高** (依赖高端GPU，显存杀手)       | **中等** (支持CPU/GPU混合部署)            |
| **模型支持** | GGUF格式为主                 | HuggingFace格式为主                    | **全模态支持** (文本/图像/音频/Embedding) |
| **适用场景** | 本地调试、原型验证、个人助理 | **高并发API服务**、云端推理、Agent后端 | RAG系统、企业私有化部署、多模态应用       |

#### Ollama

先拉取模型，再配置：

```bash
ollama pull qwen3.5:0.8b
```

```json5
(base) will@MacMini-Will extensions % ollama launch openclaw
This will modify your OpenClaw configuration:
  /Users/will/.openclaw/openclaw.json
Backups will be saved to /var/folders/4f/lx3tlt3d6fz2bys8ct46fzxh0000gn/T/ollama-backups/

Added qwen3.5:0.8b to OpenClaw

Launching OpenClaw with qwen3.5:0.8b...

Security

  OpenClaw can read files and run actions when tools are enabled.
  A bad prompt can trick it into doing unsafe things.

  Learn more: https://docs.openclaw.ai/gateway/security


Preparing your assistant — this may take a moment...

Starting gateway...

✓ OpenClaw is running

  Open the Web UI:
    http://localhost:18789/#token=536eb0bbb905eb6ad8b965fc32e5d3174b208743e201f5ff
```

Ollama 在 `http://127.0.0.1:11434/v1` 运行时会被自动发现，无需额外配置。

#### vLLM

推荐 `openclaw onboard`：

``` 
(base) will@MacMini-Will extensions % openclaw onboard

🦞 OpenClaw 2026.3.13 (61d171a) — iMessage green bubble energy, but for everyone.

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░██░▄▄░██░▄▄▄██░▀██░██░▄▄▀██░████░▄▄▀██░███░██
██░███░██░▀▀░██░▄▄▄██░█░█░██░█████░████░▀▀░██░█░█░██
██░▀▀▀░██░█████░▀▀▀██░██▄░██░▀▀▄██░▀▀░█░██░██▄▀▄▀▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                  🦞 OPENCLAW 🦞                    
 
┌  OpenClaw onboarding
│
│
◇  Model/auth provider
│  vLLM
│
◇  vLLM base URL
│  http://127.0.0.1:8000/v1
│
◇  vLLM API key
│  sk-
│
◇  vLLM model
│  my-qwen3-4b
│
◇  Model configured ──────────────────────╮
│                                         │
│  Default model set to vllm/my-qwen3-4b  │
│                                         │
├─────────────────────────────────────────╯
│
◇  Default model
│  Keep current (vllm/my-qwen3-4b)
[info]: [ 'client ready' ]
```



也可以配置文件配置

高性能本地推理服务器

```bash
export VLLM_API_KEY="vllm-local"
```

```json5
{
  agents: {
    defaults: { model: { primary: "vllm/your-model-id" } }
  }
}
```

默认连接 `http://127.0.0.1:8000/v1`。







### 自定义

任何 OpenAI 或 Anthropic 兼容的 API 都可以通过 `models.providers` 接入：

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.5-gs32" },
      models: { "lmstudio/minimax-m2.5-gs32": { alias: "Minimax" } },
    }
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "LMSTUDIO_KEY",
        api: "openai-completions",
        models: [{
          id: "minimax-m2.5-gs32",
          name: "MiniMax M2.5",
          contextWindow: 200000,
          maxTokens: 8192,
        }]
      }
    }
  }
}
```

<details>
<summary>自定义提供商的可选字段</summary>


在 `models` 数组中，每个模型对象支持以下字段（均可省略）：

| 字段            | 默认值     | 说明                                       |
| --------------- | ---------- | ------------------------------------------ |
| `reasoning`     | `false`    | 是否支持推理/思考链                        |
| `input`         | `["text"]` | 支持的输入类型                             |
| `cost`          | 全为 0     | `{ input, output, cacheRead, cacheWrite }` |
| `contextWindow` | `200000`   | 上下文窗口大小                             |
| `maxTokens`     | `8192`     | 最大输出 Token 数                          |

建议设置与你的代理/模型实际限制匹配的值。

**API 兼容模式**（`api` 字段）：

- `openai-completions`：OpenAI Chat Completions 兼容
- `anthropic-messages`：Anthropic Messages 兼容

<details>
<summary>models.json 注册表机制</summary>


自定义提供商配置会写入 `~/.openclaw/agents/<agentId>/models.json`。默认使用 `merge` 模式（与内置目录合并），也可设置 `models.mode: "replace"` 完全替换。

合并优先级规则：

- 已有的非空 `baseUrl` 优先
- 非 SecretRef 管理的 `apiKey` 优先
- SecretRef 管理的 Key 会从源标记（环境变量名等）刷新，不直接存储明文
- 其他字段从配置和标准目录刷新

## 2.切换默认模型

`openclaw models set xxx `

`openclaw config set agents.defaults.model.primary "xxx"`

```bash
(base) will@MacMini-Will extensions % openclaw models list 

🦞 OpenClaw 2026.3.13 (61d171a) — I can run local, remote, or purely on vibes—results may vary with DNS.

Model                                      Input      Ctx      Local Auth  Tags
openrouter/stepfun/step-3.5-flash:free     text       250k     no    yes   default,configured
custom-api-siliconflow-cn/Qwen/Qwen3-8B    text       16k      no    yes   fallback#1,configured,alias:s-qwen3-8b
minimax-cn/MiniMax-M2.5                    text       195k     no    yes   fallback#2,configured,alias:Minimax
kimi-coding/k2p5                           text+image 256k     no    yes   fallback#3,configured,alias:Kimi for Coding
ollama/qwen3.5:0.8b                        text+image 256k     yes   yes   configured
openrouter/auto                            text+image 195k     no    yes   configured,alias:OpenRouter


(base) will@MacMini-Will extensions % openclaw models set kimi-coding/k2p5

🦞 OpenClaw 2026.3.13 (61d171a) — One CLI to rule them all, and one more restart because you changed the port.

Config overwrite: /Users/will/.openclaw/openclaw.json (sha256 bd04fdcb2363b6a47ae3b03414777ded52c7320714f006f7f78e4b8276d5bf33 -> 0c6fb20af260b98ee6beb11fa7b566a13617e58d2c8f0ccdd918194b12084a2a, backup=/Users/will/.openclaw/openclaw.json.bak)
Updated ~/.openclaw/openclaw.json
Default model: kimi-coding/k2p5

(base) will@MacMini-Will extensions % openclaw models list                

🦞 OpenClaw 2026.3.13 (61d171a) — Claws out, commit in—let's ship something mildly responsible.

Model                                      Input      Ctx      Local Auth  Tags
kimi-coding/k2p5                           text+image 256k     no    yes   default,fallback#3,configured,alias:Kimi for Coding
custom-api-siliconflow-cn/Qwen/Qwen3-8B    text       16k      no    yes   fallback#1,configured,alias:s-qwen3-8b
minimax-cn/MiniMax-M2.5                    text       195k     no    yes   fallback#2,configured,alias:Minimax
openrouter/stepfun/step-3.5-flash:free     text       250k     no    yes   configured
ollama/qwen3.5:0.8b                        text+image 256k     yes   yes   configured
openrouter/auto                            text+image 195k     no    yes   configured,alias:OpenRouter
```



## 3.删除模型

查看配置文件：

```
(base) will@MacMini-Will extensions % openclaw config get agents.defaults.models

🦞 OpenClaw 2026.3.13 (61d171a) — Pairing codes exist because even bots believe in consent—and good security hygiene.

{
  "custom-api-siliconflow-cn/Qwen/Qwen3-8B": {
    "alias": "s-qwen3-8b"
  },
  "kimi-coding/k2p5": {
    "alias": "Kimi for Coding"
  },
  "minimax-cn/MiniMax-M2.5": {
    "alias": "Minimax"
  },
  "openrouter/stepfun/step-3.5-flash:free": {},
  "ollama/qwen3.5:0.8b": {},
  "openrouter/auto": {
    "alias": "OpenRouter"
  }
}
```

CLI：

```
openclaw models list
openclaw config unset 'agents.defaults.models.[模型ID]'
openclaw config unset 'agents.defaults.models.openrouter/stepfun/step-3.5-flash:free'
```

修改配置文件： 

```

```

## 4.主模型、备用模型、图片模型

每次对话，OpenClaw 按这个顺序选模型：

```
主模型（primary）
  ↓ 挂了或限流
备用模型列表（fallbacks），依次尝试
  ↓ 每个模型内部
同提供商的多个 API Key 之间轮换
```

**配置建议**：主模型选你用得到的最强的；备用模型做兜底或省钱。

发图片时，如果主模型不支持图片输入，OpenClaw 会自动切到 `imageModel`：

```json5
{
  agents: {
    defaults: {
      imageModel: {
        primary: "openai/gpt-5.1-codex",
        fallbacks: ["google/gemini-3-pro-preview"]
      }
    }
  }
}
```

<details>
<summary>想限制只能用哪些模型？</summary>
设置 `agents.defaults.models` 就启用了**白名单**，只有列表里的模型才能使用。同时还能给模型起别名，方便聊天中快速切换：

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-sonnet-4-5" },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "anthropic/claude-opus-4-6": { alias: "Opus" },
      }
    }
  }
}
```

设置后，聊天中 `/model Sonnet` 就能直接切换，不用记完整 ID。不设置 `models` 则无限制，自由切换任意模型。

---

## 5.聊天中切换模型

无需重启，随时切换：

| 命令                    | 效果                   |
| ----------------------- | ---------------------- |
| `/model`                | 打开模型列表，用数字选 |
| `/model 3`              | 直接选第 3 个          |
| `/model openai/gpt-5.2` | 直接指定模型 ID        |
| `/model status`         | 查看当前模型和认证状态 |

> 模型 ID 中的第一个 `/` 分隔提供商和模型名。OpenRouter 上的模型名本身含 `/`，必须带提供商前缀：`/model openrouter/moonshotai/kimi-k2`。


---

## 6. 进阶：多 Key 轮换与故障转移

日常使用不需要关心这些——OpenClaw 出错时会自动处理。但如果你想精确控制，展开看详情。

<details>
<summary>多个 API Key 自动轮换</summary>
有多个 API Key 时，遇到限流（429）会自动切换到下一个。通过环境变量配置：

```bash
# 方式一：逗号分隔
OPENAI_API_KEYS="sk-key1,sk-key2,sk-key3"

# 方式二：编号列表
OPENAI_API_KEY_1="sk-key1"
OPENAI_API_KEY_2="sk-key2"

# 方式三：实时热切（最高优先级）
OPENCLAW_LIVE_OPENAI_KEY="sk-hot-key"
```

优先级：`OPENCLAW_LIVE_*` > `_API_KEYS`（逗号列表）> `_API_KEY`（单个）> `_API_KEY_*`（编号）

轮换只在限流错误时触发；非限流错误直接失败，不尝试下一个 Key。

<details>
<summary>模型故障转移（Failover）</summary>
故障转移分两阶段：先在同提供商的多个 Key 之间轮换，全部失败后切换到 `fallbacks` 列表中的下一个模型。

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: [
          "openai/gpt-5.1-codex",
          "google/gemini-3-pro-preview"
        ]
      }
    }
  }
}
```

Anthropic 全部失败 → 自动切 OpenAI；OpenAI 也失败 → 切 Google。用户无感。

**冷却机制**：Key 出错后进入冷却，使用指数退避：

| 失败次数 | 冷却时间       |
| -------- | -------------- |
| 第 1 次  | 1 分钟         |
| 第 2 次  | 5 分钟         |
| 第 3 次  | 25 分钟        |
| 第 4 次+ | 1 小时（上限） |

余额不足则触发长期禁用（起始 5 小时，每次翻倍，上限 24 小时）。建议 OpenRouter 用户开启 Auto Top Up。

**会话粘性**：同一会话内 OpenClaw 会固定使用选中的认证配置，不会每次请求都轮换（有利于缓存命中）。想锁定特定配置，聊天中用 `/model …@<profileId>`。

## 7.常用命令速查表

### 常用命令

```bash
openclaw models status                          # 查看当前主模型 + 备用 + 认证概览
openclaw models list                            # 查看已配置的模型
openclaw models list --all                      # 查看全部可用模型
openclaw models set openai/gpt-5.1-codex        # 设置主模型
openclaw models set-image google/gemini-3-pro-preview  # 设置图片模型
```

### 别名（让切换更方便）

```bash
openclaw models aliases add Sonnet anthropic/claude-sonnet-4-5
openclaw models aliases add Opus anthropic/claude-opus-4-6
openclaw models aliases list
openclaw models aliases remove Sonnet
```

### 备用模型

```bash
openclaw models fallbacks list
openclaw models fallbacks add openai/gpt-5.2
openclaw models fallbacks add google/gemini-3-pro-preview
openclaw models fallbacks remove openai/gpt-5.2
openclaw models fallbacks clear
```

<details>
<summary>models status 有哪些输出标志？</summary>

- `--plain`：只输出当前主模型名（适合脚本）
- `--json`：机器可读 JSON
- `--check`：自动化检查（缺失/过期返回 exit 1，即将过期返回 exit 2）

输出内容包括：当前主模型和备用模型、每个提供商的认证状态、24 小时内即将过期的 OAuth Token 警告。



<details>
<summary>想找 OpenRouter 上最好的免费模型？</summary>



```bash
openclaw models scan              # 自动探测并排序免费模型
openclaw models scan --no-probe   # 只看列表，不探测
openclaw models scan --set-default  # 扫完直接设为默认
```

排名依据：图片支持 → 工具调用延迟 → 上下文窗口 → 参数量。需要 `OPENROUTER_API_KEY`。



# 第七章 智能体管理

这章教你调教龙虾——让它知道自己是谁、记住你的偏好、按你的规矩干活。

## 0. 什么是 Agent？

**Agent（智能体）就是你的龙虾本身**——有自己的性格（人设文件）、记忆（工作区文件）和能力（工具）。

默认情况下 OpenClaw 运行一个 Agent（id 为 `main`）。工作区就是龙虾的"家"，存放它的一切：

```
~/.openclaw/workspace/
```

> **Windows 用户**：`~/.openclaw/workspace` 即 `C:\Users\你的用户名\.openclaw\workspace`。



## 1. Agent 工作区

工作区（Workspace）是龙虾的"家"——它的身份、性格、记忆、技能全都存放在这里。

### 1.1 默认位置

```
~/.openclaw/workspace/
```

查看默认workspace

```
(base) will@MacMini-Will learn-llm-agent-easily % openclaw config get agents.defaults.workspace

🦞 OpenClaw 2026.3.13 (61d171a) — One CLI to rule them all, and one more restart because you changed the port.

/Users/will/.openclaw/workspace
```

修改默认工作区

```
(base) will@MacMini-Will learn-llm-agent-easily % openclaw config set agents.defaults.workspace /Users/will/.openclaw/workspace-001

🦞 OpenClaw 2026.3.13 (61d171a) — Gateway online—please keep hands, feet, and appendages inside the shell at all times.

Config overwrite: /Users/will/.openclaw/openclaw.json (sha256 58af7fec368d32df40dab066cf50df2bedbb6f456bdcb5822af0200108f9d4d9 -> 890080c3355e767d69eaa356f5548d8581087c6001c049bb89cab2fbad25cacd, backup=/Users/will/.openclaw/openclaw.json.bak)
Updated agents.defaults.workspace. Restart the gateway to apply.
```



### 1.2 工作区文件一览

| 文件                   | 用途                                         | 加载时机       |
| ---------------------- | -------------------------------------------- | -------------- |
| `AGENTS.md`            | 操作指令：告诉龙虾"怎么做事"和如何使用记忆   | 每次会话开始   |
| `SOUL.md`              | 人设：性格、语气、边界                       | 每次会话开始   |
| `USER.md`              | 用户资料：你是谁、怎么称呼你                 | 每次会话开始   |
| `IDENTITY.md`          | 龙虾身份：名字、风格、表情符号               | 每次会话开始   |
| `TOOLS.md`             | 工具使用备注（不控制工具开关，只是使用建议） | 每次会话开始   |
| `HEARTBEAT.md`         | 心跳任务清单（可选，保持简短）               | 心跳运行时     |
| `BOOT.md`              | 启动清单（可选，Gateway 重启时执行）         | Gateway 启动时 |
| `BOOTSTRAP.md`         | 首次引导仪式（完成后删除）                   | 仅首次运行     |
| `MEMORY.md`            | 长期记忆（可选）                             | 仅主会话       |
| `memory/YYYY-MM-DD.md` | 每日记忆日志                                 | 按需读取       |
| `skills/`              | 工作区级技能（可选）                         | 按需加载       |

> **重要**：这些文件在每次对话时都会注入到 AI 模型的上下文窗口中，**会消耗 Token**。保持文件简洁，尤其是 `MEMORY.md`——它会随时间增长，导致上下文使用量增大和更频繁的压缩。

> `memory/YYYY-MM-DD.md` 每日文件**不会**自动注入，而是通过 `memory_search` 和 `memory_get` 工具按需访问，不占用上下文窗口。

<details>
<summary>工作区文件注入规则</summary>

- 空文件会被跳过
- 大文件会被截断并标注 `[truncated]`
  - 单文件上限：`agents.defaults.bootstrapMaxChars`（默认 20,000 字符）
  - 所有文件总上限：`agents.defaults.bootstrapTotalMaxChars`（默认 150,000 字符）
- 缺失的文件会注入一行 "missing file" 标记
- 子 Agent 会话只注入 `AGENTS.md` 和 `TOOLS.md`（其他文件被过滤以保持子 Agent 上下文精简）
- 截断时可注入警告，通过 `agents.defaults.bootstrapPromptTruncationWarning` 控制（`off` / `once` / `always`，默认 `once`）

运行 `/context list` 或 `/context detail` 可以查看每个文件的原始大小 vs 注入大小、是否被截断。

<details>
<summary>工作区的安全边界</summary>

工作区是默认的工作目录（`cwd`），**但不是硬沙盒**。工具解析相对路径时会基于工作区，但绝对路径仍然可以访问主机上的其他位置。

如果你需要严格隔离，使用沙盒模式：

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",
        "scope": "agent"
      }
    }
  }
}
```

启用沙盒后，工具会在 `~/.openclaw/sandboxes` 下的隔离目录中操作，而非主机工作区。

<details>
<summary>工作区 Git 备份（推荐）</summary>

建议将工作区放入私有 Git 仓库备份：

```bash
# 初始化
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"

# 添加远程仓库（GitHub CLI）
gh repo create openclaw-workspace --private --source . --remote origin --push

# 日常更新
git add .
git commit -m "Update memory"
git push
```

**不要提交**：API 密钥、OAuth 令牌、`~/.openclaw/` 下的任何内容。

建议的 `.gitignore`：

```
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

### 1.3 工作区文件配置指南

每个文件都是纯 Markdown，直接用文本编辑器编辑即可。9 个文件看起来不少，但它们各司其职，可以分为四组来理解：

| 分组           | 文件                                  | 一句话说明                     |
| -------------- | ------------------------------------- | ------------------------------ |
| **身份三件套** | IDENTITY.md / SOUL.md / USER.md       | 龙虾是谁、什么性格、服务谁     |
| **行为指南**   | AGENTS.md / TOOLS.md                  | 怎么做事、怎么用工具           |
| **记忆系统**   | MEMORY.md                             | 跨会话记住什么                 |
| **生命周期**   | BOOTSTRAP.md / BOOT.md / HEARTBEAT.md | 首次启动 → 每次重启 → 定期巡检 |

> **建议阅读顺序**：先配好身份三件套（让龙虾认识你），再写 AGENTS.md（教它做事），其余按需添加。

---

#### **身份三件套：让龙虾认识你和自己**

这三个文件定义了"谁是谁"——龙虾的身份、性格和用户资料。它们在每次会话开始时自动加载，是龙虾"记忆"的起点。

##### IDENTITY.md —— 龙虾的身份证

定义龙虾的名字、风格和表情偏好。龙虾会按照这里的设定来介绍自己。

```markdown
# 身份

- 名字：阿虾
- 称呼用户：老板
- 语言：中文为主，技术术语保留英文
- 表情符号：适度使用 🦞🔥✅❌
- 签名风格：回复末尾不加落款
```

<details>
<summary>📋 IDENTITY.md 配置模板参考</summary>

上面的简化示例只展示了基本字段。实际使用中，你可以根据场景定制得更丰富：

```markdown
# 身份

- 名字：阿虾
- 物种：一只住在电脑里的龙虾 🦞
- 称呼用户：老板
- 气质：温暖但不啰嗦，偶尔毒舌
- 语言：中文为主，技术术语保留英文
- 表情符号：🦞（签名）、✅❌（判断）、🔥（重要）、💡（建议）
- 头像：avatars/lobster.png
- 签名风格：回复末尾不加落款，不用"祝好"之类的客套
- 自我介绍：当被问到"你是谁"时，回答"我是阿虾，你的私人助理"
```

**每个字段的作用：**

| 字段     | 影响                           | 不写会怎样     |
| -------- | ------------------------------ | -------------- |
| 名字     | 龙虾怎么称呼自己               | 默认用"我"     |
| 物种     | 自我认知的基调（严肃 or 有趣） | 默认"AI 助手"  |
| 称呼用户 | 对你的称呼方式                 | 默认用"你"     |
| 气质     | 整体回复风格                   | 取决于 SOUL.md |
| 语言     | 回复语言                       | 跟随用户语言   |
| 表情符号 | 回复中使用的表情               | 不主动使用     |
| 头像     | 在聊天平台显示的头像           | 使用默认头像   |

> 安装后的初始模板是一份空白问卷，引导龙虾在首次对话中通过问答来填写。你也可以跳过引导，直接按上面的格式手动编辑。

##### SOUL.md —— 龙虾的性格

定义性格、语气和行为边界。这是龙虾"怎么说话"的指南。

```markdown
# 人设

## 性格
- 专业但不刻板，偶尔幽默
- 遇到不确定的问题，诚实说"我不确定"而非编造答案
- 主动提供建议，但不越权执行

## 语气
- 日常对话：轻松简洁
- 技术讨论：严谨准确
- 出错时：坦诚道歉，给出修复方案

## 边界
- 不讨论政治、宗教等敏感话题
- 不执行未经确认的破坏性操作（删除文件、清空数据等）
- 涉及金钱交易时，必须二次确认
```

<details>
<summary>📋 SOUL.md 配置模板参考</summary>

上面的简化示例覆盖了基本维度。实际使用中，你可以按场景细化到更具体的行为指导：

```markdown
# 人设

## 核心信条
- 真正有用，不要表演式有用——别说"好问题！"，直接帮忙
- 有自己的观点，可以不同意、可以有偏好
- 先自己想办法，搞不定再问——带着答案回来，不是带着问题
- 对外部操作（发邮件、发消息）谨慎，对内部操作（阅读、整理）大胆

## 性格
- 专业但不刻板，偶尔幽默
- 遇到不确定的问题，诚实说"我不确定"而非编造答案
- 主动提供建议，但不越权执行
- 犯错时坦诚道歉，直接给修复方案，不找借口

## 语气（按场景调整）
- 日常对话：轻松简洁，像朋友聊天
- 正式文档：严谨准确，用书面语
- 出错时：坦诚 + 方案，不啰嗦
- 催促时：不急不躁，先确认优先级

## 边界
- 隐私的事情就是隐私，没有例外
- 不讨论政治、宗教等敏感话题
- 不执行未经确认的破坏性操作（删除文件、清空数据等）
- 涉及金钱交易时，必须二次确认
- 绝不往聊天平台发半成品回复
- 在群聊中谨慎发言——你不是用户的代言人

## 延续性
- 每次会话你都是全新醒来的，工作区文件就是你的记忆
- 重要的事情写进文件，不要"心里记着"
- 如果你修改了这个文件，告诉用户——这是你的灵魂，他们应该知道
```

**SOUL.md vs AGENTS.md 的区别：**

| 维度     | SOUL.md                      | AGENTS.md                    |
| -------- | ---------------------------- | ---------------------------- |
| 管什么   | "怎么说话"——性格、语气、边界 | "怎么做事"——流程、规则、记忆 |
| 类比     | 一个人的性格                 | 一个人的工作手册             |
| 修改频率 | 很少改——定型后基本不动       | 经常改——随工作流程调整       |

> 官方初始模板的核心理念是：**做一个有个性、有能力、有边界的助手**，而不是唯唯诺诺的聊天机器人。上面的参考配置将这一理念具体化为可操作的规则。

##### USER.md —— 用户档案

告诉龙虾"你是谁"，让它更好地理解你的需求。

```markdown
# 用户信息

- 称呼：虾哥
- 角色：产品经理
- 日常工作：写需求文档、竞品分析、数据报表
- 偏好：喜欢简洁清晰的表达，讨厌冗长废话
- 时区：Asia/Shanghai
- 工作语言：中文
```

<details>
<summary>📋 USER.md 配置模板参考</summary>

上面的简化示例只列了基础信息。实际使用中，写得越详细，龙虾就越能"懂你"：

```markdown
# 用户信息

## 基本资料
- 称呼：虾哥
- 角色：产品经理
- 公司/团队：XX 科技 产品部
- 时区：Asia/Shanghai
- 工作语言：中文
- 工作时间：周一至周五 9:00-18:00

## 日常工作
- 写需求文档、竞品分析、数据报表
- 经常需要整理会议纪要
- 每周给领导汇报项目进展

## 沟通偏好
- 喜欢简洁清晰的表达，讨厌冗长废话
- 回复消息时先说结论，再说原因
- 不需要"您好""祝好"之类的客套
- 提建议时直接给方案，不要只说问题

## 技能水平
- 熟练使用飞书、Excel、PPT
- 了解基本的数据分析（SQL 能看懂，写不太行）
- 对技术概念有基本理解，但不需要看代码

## 个人喜好
- 喜欢简约设计风格
- 喜欢用清单和表格整理信息
- 不喜欢被追问"你确定吗？"——说了就是确定了
```

**写多少合适？** USER.md 会在每次会话开始时注入上下文，所以不宜过长。建议控制在 **30 行以内**，把变化频繁的细节（当前项目、最近任务）放到 MEMORY.md 中。

> 安装后的初始模板是一份空白问卷，龙虾会在引导仪式中通过对话帮你填写，之后在日常使用中持续补充。你也可以跳过引导，直接按上面的格式手动编辑。

---

#### **行为指南：教龙虾怎么做事**

身份确定了，接下来告诉龙虾"该怎么工作"。AGENTS.md 是核心操作手册，TOOLS.md 是工具使用的补充备注。

##### AGENTS.md —— 操作手册

这是最重要的文件——告诉龙虾"怎么做事"。所有行为规则、工作流程、记忆使用方式都写在这里。

```markdown
# 操作指令

## 通用规则
- 收到任务后，先确认理解再执行
- 每完成一个步骤，主动汇报进度
- 遇到错误先尝试自行解决，解决不了再告知用户

## 记忆使用
- 用户说"记住这个"时，立即写入 memory/YYYY-MM-DD.md
- 重要的长期信息（偏好、项目规范）写入 MEMORY.md
- 每次会话结束前，主动总结关键决策写入记忆
```

<details>
<summary>📋 AGENTS.md 配置模板参考</summary>

上面的简化示例只展示了通用规则和记忆使用。实际的 AGENTS.md 应该覆盖更多维度——以下是一个完整的参考配置：

```markdown
# 操作指令

## 会话启动
每次会话开始前，依次执行（不需要请示）：
1. 读取 `SOUL.md` —— 了解自己是谁
2. 读取 `USER.md` —— 了解服务对象
3. 读取 `memory/YYYY-MM-DD.md`（今天 + 昨天）获取近期上下文
4. **仅在主会话中**：读取 `MEMORY.md`

## 通用规则
- 收到任务后，先确认理解再执行
- 每完成一个步骤，主动汇报进度
- 遇到错误先尝试自行解决，解决不了再告知用户
- 回复要简洁，不需要"好的，我来帮你"之类的开场白

## 记忆
龙虾每次会话都是全新的，记忆文件是唯一的"前世今生"：
- **每日日志：** `memory/YYYY-MM-DD.md` —— 当天发生了什么
- **长期记忆：** `MEMORY.md` —— 精炼后的持久知识（仅主会话加载）

### 记忆规则
- 用户说"记住这个"时，立即写入 memory/YYYY-MM-DD.md
- 重要的长期信息写入 MEMORY.md
- 每次会话结束前，主动总结关键决策写入记忆
- 一定要写进文件——"心里记着"熬不过会话重启

### 安全设计
- MEMORY.md **不在群聊中加载**——防止个人上下文泄露给陌生人
- 这是刻意的隐私保护，不要手动在群聊中读取 MEMORY.md

## 红线
- 绝不外泄用户隐私数据
- 执行破坏性命令前必须确认
- `trash` 优于 `rm`（可恢复胜过彻底删除）
- 拿不准的事，先问再做

## 群聊礼仪
**该回复时：**
- 被直接 @ 或被提问
- 能提供有价值的信息、见解或帮助

**该沉默时（回复 HEARTBEAT_OK）：**
- 只是人类之间的闲聊
- 已经有人回答了问题
- 对话流畅，不需要你插嘴

人类法则：人在群聊里也不会每条消息都回。龙虾也不应该。

## 心跳 —— 主动巡检
**定期检查（轮流进行，每天 2-4 次）：**
- 邮件 —— 有没有紧急未读？
- 日历 —— 未来 24-48 小时有什么安排？
- 天气 —— 用户可能出门吗？

**该主动汇报时：** 收到重要邮件、日历事件即将到来（< 2 小时）
**该保持安静时：** 深夜时段（23:00-08:00）、上次检查后没有新消息

## 场景处理 —— 遇到特定需求怎么办

龙虾不是只会聊天，很多用户会提出操作性需求。
提前定义好处理流程，龙虾就能自主完成，不需要你手把手教。

### 日程与提醒类需求
当用户提出涉及日程、提醒的任务时：
1. 确认时间、地点、参与人等关键信息
2. 检查是否与现有日程冲突
3. 创建/修改日程后，汇报确认结果
4. 临近时间主动提醒

### 信息查询类需求
当用户提出"帮我查一下""看看有没有"类需求时：
1. 优先使用已有工具（搜索、API 调用）获取信息
2. 结果要结构化呈现（表格、列表），不要大段文字
3. 标注信息来源和时效性

### 文件与内容类需求
当用户提出涉及文件整理、文案撰写的任务时：
1. 确认具体要求（格式、风格、长度）
2. 先给出大纲或草稿，确认方向无误再完善
3. 完成后列出要点摘要，方便用户快速检查

> **按需扩展**：以上只是常见场景的示例。你可以根据自己的使用习惯，添加更多场景处理规则，比如"翻译类需求""购物比价类需求""旅行规划类需求"等。场景越具体，龙虾的执行越精准。进阶用户还可以添加"代码与 PR 类需求"等开发场景。
```

**AGENTS.md 的七大模块及其作用：**

| 模块     | 作用                         | 不写会怎样                                       |
| -------- | ---------------------------- | ------------------------------------------------ |
| 会话启动 | 定义每次对话前的准备动作     | 龙虾不会主动读取记忆文件                         |
| 通用规则 | 控制任务执行的基本行为       | 龙虾按默认习惯行事，可能不符合你的预期           |
| 记忆     | 规定什么时候写记忆、写到哪里 | 龙虾不会主动记录，重要信息可能丢失               |
| 红线     | 设定不可逾越的安全边界       | 龙虾可能执行你不想要的操作                       |
| 群聊礼仪 | 控制在群聊中的发言策略       | 龙虾可能对每条消息都回复，造成刷屏               |
| 心跳     | 定义主动巡检的内容和频率     | 龙虾不会主动检查邮件、日历等                     |
| 场景处理 | 预定义特定需求的处理流程     | 龙虾遇到操作性需求时凭直觉行事，可能遗漏关键步骤 |

##### TOOLS.md —— 工具使用备注

给龙虾补充工具使用的注意事项（不控制工具开关，只是建议）。

```markdown
# 工具使用备注

## exec（命令执行）
- 执行破坏性命令前必须确认（删除文件、清空目录等）
- 长时间运行的命令加 timeout

## browser（浏览器）
- 优先使用搜索工具而非浏览器访问
- 访问需要登录的网站时，提前告知用户

## write / edit（文件操作）
- 修改重要文件前先备份
- 批量修改前先展示变更内容让用户确认
```

<details>
<summary>📋 TOOLS.md 配置模板参考</summary>

上面的简化示例按工具类型组织。实际使用中，你还可以加入环境专属信息——龙虾用工具时就会参考这些备忘：

```markdown
# 工具使用备注

## exec（命令执行）
- 执行破坏性命令前必须确认（删除文件、清空目录等）
- 长时间运行的命令加 timeout
- `trash` 优于 `rm`（可恢复胜过彻底删除）

## browser（浏览器）
- 优先使用搜索工具而非浏览器访问
- 访问需要登录的网站时，提前告知用户
- 不要自动点击"同意 Cookie"之类的弹窗

## write / edit（文件操作）
- 修改重要文件前先备份
- 批量修改前先展示变更内容让用户确认
- 文件名用中文或拼音，不要用纯英文

## 我的环境信息
- 智能音箱：客厅小爱同学、卧室天猫精灵
- 打印机：书房 HP LaserJet（Wi-Fi 直连，IP 192.168.1.50）
- NAS：群晖 DS220+（IP 192.168.1.100，用户名 admin）
- 常用网站：飞书（feishu.cn）、语雀（yuque.com）
```

**TOOLS.md vs CLI 配置的区别：**

| 维度     | TOOLS.md                 | CLI 配置（`openclaw config set`）        |
| -------- | ------------------------ | ---------------------------------------- |
| 控制什么 | 使用建议和环境备忘       | 工具的开关和权限                         |
| 谁读     | 龙虾（AI 模型）          | Gateway（程序）                          |
| 效果     | 软性引导，龙虾"尽量"遵守 | 硬性限制，不给就用不了                   |
| 例子     | "删除前先确认"           | `openclaw config set tools.profile full` |

> TOOLS.md 是龙虾的"速查小抄"——技能定义了工具怎么用，这个文件记录你的环境怎么配。两者分开存放，更新技能不会丢失你的备忘，分享技能也不会泄露你的环境信息。


---

#### **记忆系统：让龙虾记住重要的事**

AGENTS.md 里提到了"记忆使用"规则，而 MEMORY.md 就是龙虾的长期记忆载体——跨会话保存的持久信息。

##### MEMORY.md —— 长期记忆核心文件

存放跨会话的持久信息。龙虾每次主会话都会读取这个文件，所以**保持精简**。这是你与龙虾协作的基础配置文件，记录的是你最不希望重复说明的核心信息。

```markdown
# 长期记忆

## 日常事务
- 每周一上午有团队周会，需要提前准备议题
- 每月 25 号提交月度报表给领导

## 偏好
- 邮件回复尽量简短，不超过三段
- 文档用中文写，关键术语保留英文
- 不喜欢冗长的开场白，直奔主题

## 重要决策
- 2026-03-10：决定用飞书作为主要沟通渠道，微信仅用于非工作场景
```

<details>
<summary>📋 MEMORY.md 配置模板参考</summary>

OpenClaw 安装后不会自动生成 MEMORY.md，需要你自己创建（或让龙虾在对话中帮你写入）。以下是一个完整的模板参考：

```markdown
# 长期记忆

> 这个文件每次会话都会加载，请保持精简。细节放到 memory/ 目录的日志文件中。

## 关于我
- 称呼：虾哥
- 习惯：早起型，通常 7 点前在线
- 沟通风格：喜欢直奔主题，不需要寒暄

## 日常事务
- 每周一上午 9:30 团队周会，需要提前准备议题
- 每月 25 号提交月度报表给领导
- 每周五下午整理下周计划

## 重要联系人
- 李总：直属领导，喜欢看数据说话
- 小王：设计同事，配合最多
- 张姐：财务，报销找她

## 偏好与习惯
- 邮件回复尽量简短，不超过三段
- 文档用中文写，关键术语保留英文
- 不喜欢冗长的开场白，直奔主题
- 讨厌被问"你确定吗？"——说了就是确定了

## 常用工具与账号
- 主要沟通：飞书（工作）、微信（私人）
- 文档协作：飞书文档
- 项目管理：飞书多维表格
- 日历：飞书日历（以飞书日历为准）

## 重要决策记录
- 2026-03-10：决定用飞书作为主要沟通渠道，微信仅用于非工作场景
- 2026-03-05：月度报表改用新模板，数据来源切换到新系统

## 注意事项
- 周三下午尽量不安排会议（留给专注工作）
- 给领导的文件必须检查错别字
- 涉及预算的事必须邮件确认，不接受口头承诺
```

> 这个模板比上面的简化示例更完整，涵盖了个人信息、日常事务、联系人、偏好、工具、决策记录等方面。你不需要一次性填满所有内容——可以先写最重要的几条，让龙虾在日常对话中逐步补充。记住：**MEMORY.md 仅在主会话加载**，群聊中不会泄露这些内容。



⚠️ `MEMORY.md` 会随时间增长。定期清理过时内容，或将细节移入 `memory/` 目录的日志文件中。

##### memory/ 目录 —— 记忆档案馆

存放详细的对话历史、完整记录和过时信息。龙虾不会自动加载这里的内容，但当你需要回顾时可以随时查阅。

```
memory/
├── 2026-03-10-决策讨论.md     # 详细记录当天决策的前因后果
├── 2026-03-15-周会记录.md     # 完整的会议纪要和待办事项
└── 2025/                      # 可按年月归档旧文件
    └── 2025-12-31-年度总结.md
```

##### 两者的核心区别

| 维度         | MEMORY.md                | memory/ 目录                   |
| ------------ | ------------------------ | ------------------------------ |
| **性质**     | 核心配置文件             | 历史档案馆                     |
| **加载方式** | 每次主会话自动读取       | 需主动调取或查阅               |
| **内容特点** | 精简、高频使用、当前有效 | 详细、历史记录、可过时         |
| **维护原则** | 保持简洁，定期清理       | 按需归档，保留完整             |
| **典型内容** | 偏好、联系人、日常事务   | 会议记录、长决策过程、历史版本 |

---

#### **生命周期：从出生到日常巡检**

最后三个文件控制龙虾在不同阶段的行为——首次启动时做什么、每次重启时做什么、日常定期做什么。按时间线排列：

```
BOOTSTRAP.md（首次启动，完成后删除）
    → BOOT.md（每次 Gateway 重启时执行）
        → HEARTBEAT.md（运行期间定期执行）
```

##### BOOTSTRAP.md —— 首次引导仪式（一次性）

首次运行时的引导脚本——龙虾通过一次轻松对话认识你和自己。**完成后会自动删除**。

```markdown
# 引导仪式

1. 你叫什么名字？
2. 你是什么"物种"？
3. 你的风格是什么？
4. 用户怎么称呼？
```

<details>
<summary>📋 BOOTSTRAP.md 配置模板参考</summary>

上面的简化示例只列了四个问题。实际的引导仪式可以设计得更丰富，让龙虾的"出生体验"更完整：

```markdown
# 引导仪式

## 第一步：认识自己
通过对话确认以下信息，写入 IDENTITY.md：
1. 你叫什么名字？（比如：阿虾、Lobster、小龙）
2. 你是什么"物种"？（AI 助手？电子龙虾？数字精灵？）
3. 你的气质是什么？（温暖？犀利？幽默？沉稳？）
4. 选一个专属表情符号（比如 🦞）

## 第二步：认识主人
通过对话确认以下信息，写入 USER.md：
1. 怎么称呼你？（名字或昵称）
2. 你的时区是？
3. 你平时做什么工作？
4. 你喜欢什么样的沟通方式？（简洁 or 详细？正式 or 随意？）

## 第三步：定性格
打开 SOUL.md，一起聊聊：
- 什么话题不该碰？（政治？宗教？其他？）
- 什么操作必须先问？（删除文件？发送消息？花钱？）
- 出错了怎么处理？（直接道歉还是解释原因？）

## 第四步：连接渠道（可选）
问问用户想怎么联系你：
- 仅网页聊天
- 飞书 / QQ / Telegram / WhatsApp
引导用户完成渠道配置（详见第四章）。

## 完成后
- 确认 IDENTITY.md、USER.md、SOUL.md 都已写入
- 删除这个文件——你不再需要引导脚本了
```

**引导仪式的设计原则：**

| 原则               | 说明                                        |
| ------------------ | ------------------------------------------- |
| 对话式，不是问卷式 | 像朋友聊天，不像填表格                      |
| 龙虾主导           | 龙虾主动提问和建议，用户只需回答            |
| 允许跳过           | 用户不想回答的问题可以跳过，以后再补        |
| 写入文件           | 每个环节的结果立即写入对应的 .md 文件       |
| 一次性             | 完成后自动删除 BOOTSTRAP.md，确保只运行一次 |

> 如果你不想走引导仪式，运行 `openclaw config set agent.skipBootstrap true`，然后直接手动编辑 IDENTITY.md、USER.md 和 SOUL.md 即可。


##### BOOT.md —— 启动任务

Gateway 重启时自动执行的一次性任务。适合做环境检查。

```markdown
# 启动任务

Gateway 重启时自动执行以下检查（每次启动只执行一次）。

## 环境检查
- 确认网络连接正常
- 检查工作区文件完整性（AGENTS.md、SOUL.md、USER.md 是否存在）

## 问候
- 如果在工作时间（08:00-22:00），给用户发一条简短的上线通知
```

<details>
<summary>📋 BOOT.md 配置模板参考</summary>

OpenClaw 安装后不会自动生成 BOOT.md，需要你自己创建。以下是一个实用的模板参考：

```markdown
# 启动任务

Gateway 重启时自动执行以下检查（每次启动只执行一次）。

## 环境检查
- 确认网络连接正常
- 检查工作区文件完整性（AGENTS.md、SOUL.md、USER.md 是否存在）
- 检查 memory/ 目录是否可读写

## 状态恢复
- 读取昨天的记忆日志，了解最近上下文
- 如果有未完成的任务，列出待办清单

## 问候
- 如果在工作时间（08:00-22:00），给用户发一条简短的上线通知
- 如果不在工作时间，保持安静
```

> BOOT.md 适合放"每次启动都要做一遍"的事情，比如环境自检和状态恢复。与 HEARTBEAT.md（定期重复执行）和 BOOTSTRAP.md（仅首次执行）不同，BOOT.md 在每次 Gateway 重启时执行一次。保持简短，避免启动时消耗过多 Token。


##### HEARTBEAT.md —— 心跳任务

心跳是龙虾的"定期自检"——每隔一段时间自动执行的轻量任务。保持简短，避免消耗过多 Token。

```markdown
# 心跳任务

- 检查 memory/ 目录，清理超过 30 天的日志
- 如果今天还没写日记，提醒用户
```

> 心跳间隔通过 `openclaw config set agents.defaults.heartbeat.every "30m"` 配置，不在这里设置。

<details>
<summary>📋 HEARTBEAT.md 配置模板参考</summary>

上面的简化示例只列了两个任务。实际使用中，你可以根据龙虾接入的工具和服务来定制巡检清单：

```markdown
# 心跳任务

## 信息检查（轮流进行，每天 2-4 次）
- 邮件 —— 有没有紧急未读？摘要汇报
- 日历 —— 未来 24-48 小时有什么安排？提前提醒
- 天气 —— 明天需要带伞吗？有极端天气吗？

## 主动汇报规则
- 收到重要邮件 → 立即通知
- 日历事件 < 2 小时 → 提醒
- 天气预警 → 当天第一次心跳时通知

## 静默规则
- 深夜时段（23:00-08:00）不打扰，除非紧急
- 上次检查后没有新消息 → 不汇报
- 周末减少频率，只检查邮件

## 维护任务
- 检查 memory/ 目录，清理超过 30 天的日志
- 如果今天还没写日记，提醒用户
- 检查 MEMORY.md 大小，超过 200 行时建议精简
```

**心跳的成本意识：** 每次心跳都会消耗 Token（调用 AI 模型执行任务清单）。任务越多，消耗越大。建议：

| 心跳频率  | 适用场景              | 每日大约消耗 |
| --------- | --------------------- | ------------ |
| 每 6 小时 | 轻度使用，只检查邮件  | 较低         |
| 每 3 小时 | 日常使用，邮件 + 日历 | 中等         |
| 每 1 小时 | 重度使用，多项检查    | 较高         |

> 安装后的初始模板是空的——**留空就不会触发心跳 API 调用**，不消耗任何 Token。等你确定了需要定期检查的事项，再按上面的格式添加任务。心跳间隔通过 CLI 配置：`openclaw config set agents.defaults.heartbeat.every "30m"`。

**Heartbeat vs Cron 选择指南：**

| 场景                   | 推荐方式       | 原因                                    |
| ---------------------- | -------------- | --------------------------------------- |
| 批量检查邮件+日历+通知 | Heartbeat      | 多个检查合并在一次心跳中，减少 API 调用 |
| 每周一早 9 点发周报    | Cron           | 需要精确时间触发                        |
| 20 分钟后提醒我开会    | Cron（`--at`） | 一次性定时任务                          |
| 定期清理旧记忆文件     | Heartbeat      | 时间不敏感，可顺带完成                  |

> AGENTS.md 是工作区中**最重要也最长的文件**。建议从上面的参考配置开始，用一段时间后根据实际体验逐步调整。记住：**这只是起点，加入你自己的风格和规则。**


### 2.4 工作区外的文件配置

以下内容存储在 `~/.openclaw/` 下，不在工作区中：

| 路径                                | 内容                                              |
| ----------------------------------- | ------------------------------------------------- |
| `~/.openclaw/` 配置文件             | 全局配置（详见[附录 G](/cn/appendix/appendix-g)） |
| `~/.openclaw/credentials/`          | OAuth 令牌、API 密钥                              |
| `~/.openclaw/agents/<id>/sessions/` | 会话记录                                          |
| `~/.openclaw/skills/`               | 共享级技能                                        |

> 如果你需要迁移到新机器，配置和会话需要单独复制。

## 2. 首次启动：引导仪式

首次运行 Agent 时，OpenClaw 会执行一个**引导仪式（Bootstrapping）**——一个简短的问答过程，帮助龙虾了解"它是谁"和"你是谁"。

### 引导过程

1. 在工作区中创建 `AGENTS.md`、`BOOTSTRAP.md`、`IDENTITY.md`、`USER.md`
2. 运行一轮简短的问答（每次一个问题）
3. 将你的回答写入 `IDENTITY.md`、`USER.md`、`SOUL.md`
4. 完成后自动删除 `BOOTSTRAP.md`（确保只运行一次）

如果你已经自行管理工作区文件（比如从另一台机器迁移过来），可以跳过引导：

```bash
openclaw config set agent.skipBootstrap true
```

也可以随时运行 `openclaw setup` 重建缺失的默认文件（不会覆盖已有文件）。

## 3. Agent 循环与上下文

发送消息后，龙虾会依次：路由 → 排队 → 组装上下文 → 调用 AI 模型 → 执行工具 → 回复。

**同一会话内的消息串行处理**（不并行）。发送 `/stop` 可随时中止。

查看上下文使用情况：

| 命令              | 作用                               |
| ----------------- | ---------------------------------- |
| `/status`         | 快速查看上下文使用率               |
| `/context list`   | 查看注入的文件列表                 |
| `/context detail` | 详细分解每个文件/工具的 Token 占用 |
| `/usage tokens`   | 每次回复后追加 Token 用量          |

> **上下文 ≠ 记忆**。上下文是模型当前窗口内容；记忆存在磁盘上，跨会话加载。

<details>
<summary>Agent 循环详解（运行步骤、系统提示词、钩子系统）</summary>

### Agent 循环流程

```markdown
你的消息
  → 路由（找到对应的 Agent 和会话）
  → 排队（如果正在处理另一条消息）
  → Agent 运行
      → 组装上下文（系统提示词 + 历史消息 + 工具列表）
      → 发送给 AI 模型
      → 模型思考并决定下一步
      → 执行工具调用（搜索、读写文件等）
      → 流式输出回复
  → 回复发送到聊天平台
```

不同会话（比如不同群聊）之间是并行的，通过 `agents.defaults.maxConcurrent`（默认 4）控制最大并行数。Agent 运行超时默认 600 秒。

### 系统提示词构成

每次 Agent 运行时，OpenClaw 构建一个系统提示词，包含：

| 部分     | 内容                                   |
| -------- | -------------------------------------- |
| 工具列表 | 当前可用工具 + 简短描述                |
| 安全守则 | 避免越权行为的提醒（建议性，非硬限制） |
| 技能列表 | 可用技能的名称、描述和路径             |
| 工作区   | 工作目录路径                           |
| 日期时间 | 用户时区                               |
| 引导文件 | AGENTS.md、SOUL.md 等文件内容          |

真正的硬限制来自工具策略、exec 审批、沙盒和渠道白名单。

上下文的两大隐形成本：**技能列表**（每条技能占用提示词空间）和**工具 Schema**（JSON 格式，不可见但占用 Token，如 `browser` 工具约 2,500 Token）。

提示词模式由运行时自动设置：`full`（默认）/ `minimal`（子 Agent）/ `none`（最小化）。

### 钩子系统（Hooks）

OpenClaw 的钩子系统（Hooks）是一个**事件驱动**的自动化机制。它允许你在特定事件（如启动、收到消息、执行命令）发生时，自动运行自定义脚本，而无需修改核心代码。

简单来说，钩子就是**“当……发生时就做……”**的自动化规则。

**1. 核心概念：事件驱动**

钩子监听系统内部的事件，一旦事件触发，对应的脚本就会执行。常见的事件包括：

- **`command:new`**：当你输入 `/new`命令开始新会话时。
- **`message:received`**：当系统收到用户消息时。
- **`gateway:startup`**：当 OpenClaw 网关启动时。

**2. 内置钩子示例**

OpenClaw 自带了一些开箱即用的钩子，你可以直接启用：

| 钩子名称             | 作用                     | 触发事件          |
| -------------------- | ------------------------ | ----------------- |
| **`session-memory`** | 保存会话上下文到记忆     | `command:new`     |
| **`command-logger`** | 记录所有命令到审计日志   | 所有命令事件      |
| **`boot-md`**        | 网关启动时运行 `boot.md` | `gateway:startup` |

**3. 如何使用钩子？**

通过 CLI 命令管理钩子非常简单：

```bash
# 1. 列出所有可用的钩子
openclaw hooks list

# 2. 查看某个钩子的详细信息
openclaw hooks info session-memory

# 3. 启用钩子（例如启用会话记忆）
openclaw hooks enable session-memory

# 4. 检查钩子状态
openclaw hooks check
```

**4. 实际应用场景**

- **自动备份**：启用 `session-memory`后，每次你输入 `/new`开始新对话，系统会自动将上一个会话的关键信息保存下来，实现跨会话记忆。
- **审计日志**：启用 `command-logger`后，系统会记录你所有的操作，方便排查问题。
- **自定义自动化**：你可以编写自己的钩子，比如在收到消息时自动调用外部 API，或者在会话结束时发送通知。

**内部钩子（Gateway Hooks）**：

- `agent:bootstrap`：引导文件构建前，可修改/替换引导上下文
- 命令钩子：`/new`、`/reset`、`/stop` 等命令事件

**插件钩子**：

- `before_model_resolve`：在模型解析前覆盖 provider/model
- `before_prompt_build`：在提交前注入额外上下文或系统提示
- `agent_end`：运行完成后检查消息列表和元数据
- `before_tool_call` / `after_tool_call`：拦截工具参数/结果
- `message_received` / `message_sending` / `message_sent`：消息生命周期
- `session_start` / `session_end`：会话边界
- `gateway_start` / `gateway_stop`：网关生命周期

配置时区：`agents.defaults.userTimezone`，时间格式：`agents.defaults.timeFormat`（`auto` / `12` / `24`）。



## 5. 会话管理

会话（Session）是龙虾与你（或一个群聊）之间的对话记录。每个群独立会话，私聊默认共享一个。

**修改工作区文件后**，发送 `/new` 开始新会话才能生效。`/new Opus` 还可以同时切换模型。

### 多人场景下的隐私隔离

> **安全警告**：默认所有私聊共享同一会话。如果多个人都能私聊你的龙虾，Alice 的内容可能被 Bob 看到。

多人使用时，用 CLI 设置会话隔离：

```bash
openclaw config set session.dmScope per-channel-peer
```

| 模式               | 适用场景           |
| ------------------ | ------------------ |
| `main`（默认）     | 只有你一个人使用   |
| `per-channel-peer` | **推荐**——多人使用 |

> 运行 `openclaw security audit` 可以检查你的 DM 安全设置。

<details>
<summary>会话管理进阶（生命周期、存储维护、跨会话通信、身份关联）</summary>

### 会话生命周期

默认每天凌晨 4:00 自动重置（Gateway 所在机器本地时间）：

```json
{
  "session": {
    "reset": {
      "mode": "daily",
      "atHour": 4,
      "idleMinutes": 120
    }
  }
}
```

按类型/渠道自定义重置策略：

```json
{
  "session": {
    "resetByType": {
      "direct": { "mode": "idle", "idleMinutes": 240 },
      "group": { "mode": "idle", "idleMinutes": 120 },
      "thread": { "mode": "daily", "atHour": 4 }
    },
    "resetByChannel": {
      "discord": { "mode": "idle", "idleMinutes": 10080 }
    }
  }
}
```

`resetByChannel` 优先级高于 `reset` / `resetByType`。

### 会话存储与维护

会话记录存储为 JSONL 文件：`~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

| 配置项                            | 默认值 | 说明                              |
| --------------------------------- | ------ | --------------------------------- |
| `session.maintenance.mode`        | `warn` | `warn` 仅报告，`enforce` 自动清理 |
| `session.maintenance.pruneAfter`  | `30d`  | 清理超过 30 天的旧会话            |
| `session.maintenance.maxEntries`  | `500`  | 最多保留 500 个会话条目           |
| `session.maintenance.rotateBytes` | `10mb` | sessions.json 超过此大小时轮转    |

```bash
openclaw sessions cleanup --dry-run   # 预览清理效果
openclaw sessions cleanup --enforce   # 执行清理
```

大规模部署示例：

```json
{
  "session": {
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "14d",
      "maxEntries": 2000,
      "rotateBytes": "25mb",
      "maxDiskBytes": "2gb",
      "highWaterBytes": "1.6gb"
    }
  }
}
```

### 会话键格式

| 来源         | 会话键格式                        |
| ------------ | --------------------------------- |
| 私聊（默认） | `agent:main:main`                 |
| 群聊         | `agent:main:<channel>:group:<id>` |
| Cron 任务    | `cron:<job.id>`                   |
| 子 Agent     | `agent:main:subagent:<uuid>`      |

### 身份关联（identityLinks）

同一个人在多个平台联系龙虾时，可以合并为同一会话：

```json
{
  "session": {
    "dmScope": "per-channel-peer",
    "identityLinks": {
      "alice": ["telegram:123456789", "discord:987654321012345678"]
    }
  }
}
```

### 跨会话通信工具

| 工具               | 功能                                 |
| ------------------ | ------------------------------------ |
| `sessions_list`    | 列出所有会话                         |
| `sessions_history` | 获取某个会话的对话记录               |
| `sessions_send`    | 向另一个会话发送消息（支持等待回复） |
| `sessions_spawn`   | 派生子 Agent 执行隔离任务            |

`sessions_send`：`timeoutSeconds = 0` 异步发出；`timeoutSeconds > 0` 等待回复；超时返回 `timeout`。发送后触发乒乓循环，最多 `maxPingPongTurns`（默认 5）轮，回复 `REPLY_SKIP` 终止。

`sessions_spawn` 派生子 Agent 参数：`task`（必填）、`label`、`model`、`thinking`、`runTimeoutSeconds`、`thread`、`cleanup`（delete/keep）、`sandbox`（inherit/require）、`attachments`。子 Agent 不含会话工具，不允许嵌套派生，完成后默认 60 分钟后自动归档。

## 6. 记忆系统

OpenClaw 的记忆是**纯 Markdown 文件**——文件就是唯一真相来源，模型只"记住"被写到磁盘上的内容。

| 文件                   | 用途                             |
| ---------------------- | -------------------------------- |
| `MEMORY.md`            | 精选长期记忆（每次会话加载）     |
| `memory/YYYY-MM-DD.md` | 每日日志（按需读取，不占上下文） |

写记忆的原则：说了"记住这个"，龙虾必须立即写入文件——"脑子里记着"熬不过会话重启。

搜索工具：`memory_search`（语义搜索）和 `memory_get`（读取指定文件）。

<details>
<summary>记忆系统进阶（向量搜索、混合搜索、时间衰减、QMD 后端）</summary>

### 自动记忆刷新

会话接近压缩上限时，OpenClaw 自动触发静默记忆刷新，提醒模型将重要信息写入磁盘：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

### 向量记忆搜索

默认启用，自动监控记忆文件变化，通过语义相似度搜索（即使措辞不同也能匹配）。

嵌入提供商自动检测顺序：本地模型 → OpenAI → Gemini → Voyage/Mistral → Ollama。

配置示例（使用 Gemini 嵌入模型）：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "gemini",
        "model": "gemini-embedding-001",
        "remote": {
          "apiKey": "你的 Gemini API Key"
        }
      }
    }
  }
}
```

配置示例（使用本地部署的嵌入模型）：

```json
{
    "agents": {
        "defaults": {
            "memorySearch": {
                "provider": "openai",
                "remote": {
                    "baseUrl": "http://127.0.0.1:11434/v1/",
                    "apiKey": "ollama"
                },
                "model": "qwen3-embedding:0.6b"
            }
        }
    }
}
```

### 混合搜索（BM25 + 向量）

结合语义匹配和关键词匹配（精确 ID、代码符号、错误信息）：

```json
{
    "agents": {
        "defaults": {
            "memorySearch": {
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
            }
        }
    }
}
```

**MMR 去重**（减少重复结果，`lambda`：0=最大多样性，1=最大相关性，默认 0.7）：

```json
{ "hybrid": { "mmr": { "enabled": true, "lambda": 0.7 } } }
```

**时间衰减**（优先近期记忆，半衰期 30 天：今天 100%、30 天前 50%、90 天前 12.5%）：

```json
{ "hybrid": { "temporalDecay": { "enabled": true, "halfLifeDays": 30 } } }
```

`MEMORY.md` 和非日期命名文件不受衰减影响。

**额外记忆路径**：

```json
{ "memorySearch": { "extraPaths": ["../team-docs", "/srv/shared-notes/overview.md"] } }
```



## 7. 上下文压缩与会话修剪

对话越来越长时，OpenClaw 会自动压缩旧对话（总结成摘要），保持上下文窗口可用。

手动压缩：`/compact Focus on decisions and open questions`（可附带指令引导重点）。

<details>
<summary>压缩与修剪详细配置</summary>

### 上下文压缩（Compaction）

自动压缩默认开启。`/status` 可查看压缩次数。

压缩后结构：`压缩摘要 + 最近消息 + 当前提问`

配置（可指定不同模型做压缩总结）：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "openrouter/anthropic/claude-sonnet-4-5",
        "identifierPolicy": "strict"
      }
    }
  }
}
```

`identifierPolicy`：`strict`（默认，保留标识符）/ `off` / `custom`

### 会话修剪（Session Pruning）

修剪只临时裁剪发送给模型的内容，不修改磁盘记录。

| 对比   | 压缩           | 修剪            |
| ------ | -------------- | --------------- |
| 作用   | 总结旧对话     | 裁剪旧工具结果  |
| 持久化 | 写入 JSONL     | 仅内存中        |
| 触发   | 接近上下文上限 | 每次 LLM 调用前 |

修剪默认关闭。启用（`cache-ttl` 模式）：

```json
{
  "agents": {
    "defaults": {
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "5m"
      }
    }
  }
}
```

修剪规则：只修剪 `toolResult` 消息；保护最近 3 条助手消息后的工具结果；含图片的不修剪；软裁剪（保留头尾加 `...`）或硬清除（替换为 `[Old tool result content cleared]`）。

默认参数：`ttl` 5 分钟，`keepLastAssistants` 3，`softTrimRatio` 0.3，`hardClearRatio` 0.5，`minPrunableToolChars` 50,000。

## 8. 多 Agent 路由

需要多 Agent 的场景：多人使用（各有独立记忆）、多场景（日常用快速模型/深度工作用 Opus）、多渠道分离、安全隔离（限制公开群组权限）。

```bash
openclaw agents add work             # 创建新 Agent
openclaw agents list --bindings      # 查看所有 Agent 和路由绑定
```

每个 Agent 获得独立工作区（`~/.openclaw/workspace-<id>`）和会话存储。

路由绑定配置：

```json
{
  "agents": {
    "list": [
      { "id": "chat", "name": "Everyday", "workspace": "~/.openclaw/workspace-chat" },
      { "id": "opus", "name": "Deep Work", "workspace": "~/.openclaw/workspace-opus" }
    ]
  },
  "bindings": [
    { "agentId": "chat", "match": { "channel": "whatsapp" } },
    { "agentId": "opus", "match": { "channel": "telegram" } }
  ]
}
```

## 9.常用命令速查表

### 查看 Agent

```bash
openclaw agents list                 # ⭐ 列出所有 Agent
openclaw agents list --json          # JSON 格式
openclaw agents list --bindings      # 显示各 Agent 绑定了哪些渠道
```

### 添加 Agent

```bash
openclaw agents add                  # ⭐ 交互式添加（推荐）
openclaw agents add [name]           # 指定名称

# 非交互式（自动化部署用）：
openclaw agents add my-agent \
  --workspace ~/.openclaw/workspace-my-agent \
  --model anthropic/claude-sonnet-4-5 \
  --bind whatsapp:personal \
  --non-interactive
```

### 绑定渠道

一个 Agent 可以绑定多个渠道，一个渠道也可以被多个 Agent 共享。

```bash
openclaw agents bindings                              # 查看所有绑定关系
openclaw agents bindings --agent <id>                  # 查看指定 Agent 的绑定
openclaw agents bind --agent <id> --bind <channel[:accountId]>    # 添加绑定
openclaw agents unbind --agent <id> --bind <channel[:accountId]>  # 移除绑定
openclaw agents unbind --agent <id> --all              # 移除全部绑定
```

### 运行 Agent（手动触发）

```bash
openclaw agent --message "Hello" --to <dest>           # 发送一条消息
openclaw agent --message "Hello" --session-id <id>     # 在指定会话中发送
openclaw agent --message "Hello" --thinking high       # 使用深度思考
openclaw agent --message "Hello" --local               # 本地模式（不经网关）
openclaw agent --message "Hello" --channel whatsapp --deliver  # 发送并投递到渠道
```

### 删除 Agent

```bash
openclaw agents delete <id>          # 删除 Agent
openclaw agents delete <id> --force  # 强制删除（跳过确认）
```



# 第八章 工具与定时任务

学完本章，你的龙虾就能自己找工具干活、定时执行任务了——搜网页、操浏览器、每天早上自动发天气，一个不落。

## 0. 工具 vs 技能

龙虾的"大脑"是模型，**工具（Tools）是它的"双手"**——没有工具只能聊天，有了工具才能干实事。

对比工具和技能，一句话：**Tools 是手脚，Skills 是招式。**

|              | Tools（工具）                          | Skills（技能）                   |
| ------------ | -------------------------------------- | -------------------------------- |
| **是什么**   | OpenClaw 内置的底层能力                | 社区或用户编写的高层指令         |
| **举例**     | 执行命令、读写文件、搜索网页           | "每天早上发晨间简报"、"总结网页" |
| **谁提供**   | OpenClaw 核心代码                      | ClawHub 技能市场 / 用户自己编写  |
| **如何管理** | `openclaw config set tools.*` CLI 命令 | `clawhub` CLI 安装/卸载          |

## 1. 工具配置档（Tool Profiles）

Tool Profile 控制龙虾"能做什么"。

| 配置档      | 能力范围                           | 适用场景                     |
| ----------- | ---------------------------------- | ---------------------------- |
| `full`      | 无限制，所有工具可用               | **推荐**——个人电脑全能助手   |
| `coding`    | 文件读写、命令执行、记忆、图片分析 | 开发者专用，不含消息和浏览器 |
| `messaging` | 消息收发、会话浏览、状态查看       | 纯聊天机器人                 |
| `minimal`   | 仅状态查看                         | 最小权限                     |

```bash
# 查看当前配置
openclaw config get tools.profile

# 设置为 full（推荐）
openclaw config set tools.profile full
openclaw gateway restart
```

配置文件`openclaw.json`

```json
  "tools": {
    "profile": "full"
  },
```

> 如果龙虾只给建议、不执行操作，多半是配置档停在了旧版默认值 `messaging`——跑一遍上面的命令就好。
> `full` 模式下 OpenClaw 可在你的电脑上执行任意命令、读写任意文件。个人电脑上使用没问题，但**不要在生产服务器上使用 `full` 模式**。

<details>
<summary>为特定 Agent 单独设置配置档</summary>
如果你运行多个 Agent（如一个全能助手 + 一个客服机器人），可以为每个 Agent 设置不同的配置档：

让默认 Agent 拥有全部工具，而 `support` Agent 只能收发消息和使用 Slack。

```json
{
  "tools": { "profile": "full" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

## 2. 内置工具一览

不需要逐个记住——龙虾会自动选工具，你只要确保配置档是 `full`。

| 分类         | 工具                                | 说明                                   |
| ------------ | ----------------------------------- | -------------------------------------- |
| **文件操作** | `read` `write` `edit` `apply_patch` | 读写文件，批量打补丁                   |
| **命令执行** | `exec` `process`                    | 运行 Shell 命令、管理后台进程          |
| **网页**     | `web_search` `web_fetch`            | 搜索引擎查询、抓取网页内容             |
| **浏览器**   | `browser`                           | 完整的浏览器自动化（点击、输入、截图） |
| **消息**     | `message`                           | 跨渠道收发消息（飞书/QQ/Telegram 等）  |
| **定时任务** | `cron`                              | 创建和管理定时 / 周期性任务            |
| **画布**     | `canvas`                            | 驱动配套 App 的画布功能                |
| **设备**     | `nodes`                             | 发现配套设备、拍照、录屏、获取位置     |
| **图片/PDF** | `image` `pdf`                       | 分析图片内容、解析 PDF 文档            |
| **网关**     | `gateway`                           | 重启网关、查看和修改配置               |
| **会话**     | `sessions_*` `agents_list`          | 管理对话会话、生成子 Agent             |

工具组（快捷分组）速查表
OpenClaw 提供预定义的工具组，方便在配置中批量引用：

| 工具组             | 包含的工具                                             |
| ------------------ | ------------------------------------------------------ |
| `group:fs`         | read, write, edit, apply_patch                         |
| `group:runtime`    | exec, bash, process                                    |
| `group:web`        | web_search, web_fetch                                  |
| `group:ui`         | browser, canvas                                        |
| `group:sessions`   | sessions_list / history / send / spawn, session_status |
| `group:memory`     | memory_search, memory_get                              |
| `group:automation` | cron, gateway                                          |
| `group:messaging`  | message                                                |
| `group:nodes`      | nodes                                                  |
| `group:openclaw`   | 所有内置工具（不含插件）                               |

在后续的权限管理中会用到这些组名。

## 3. 联网搜索工具

想让龙虾告诉你今天的新闻或最新股价？配置联网搜索就行。

一行命令启动向导：

```bash
openclaw configure --section web
```

向导会让你选搜索引擎、填 API Key，完成后龙虾就能实时查网了。

配置完成后直接在对话里问：

```
今天有什么科技新闻？
帮我搜索"OpenClaw 最新版本"的更新内容
```

龙虾自动判断要不要联网，不用你指定。

> `web_fetch` 工具还能直接抓取指定网址的内容并转成文字。JavaScript 渲染的动态网页建议用下一节的浏览器工具。

支持哪些搜索引擎？
| 搜索引擎       | 说明                                 |
| -------------- | ------------------------------------ |
| **Brave**      | 隐私友好，免费额度充足，推荐入门使用 |
| **Perplexity** | AI 增强搜索，结果质量高              |
| **Kimi**       | 国内可用，中文搜索优化               |
| **Gemini**     | Google 搜索能力                      |
| **Grok**       | xAI 提供的搜索                       |
## 4. 浏览器自动化工具

想让龙虾帮你填表单、截图、点按钮？浏览器工具默认已启用，直接说就行：

```
帮我打开百度搜索"今日天气"，截图给我看
打开 https://example.com，找到登录按钮并点击
```

龙虾会自动启动 Chrome、打开页面、识别元素、执行操作，最后截图给你确认。

> 前提：系统需要安装 Chrome 或 Chromium。

如果浏览器未启用，运行：

```bash
openclaw config set browser.enabled true
openclaw gateway restart
```

浏览器支持哪些操作？
| 操作                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| `status`                   | 查看浏览器是否运行                                           |
| `start` / `stop`           | 启动 / 关闭浏览器                                            |
| `open`                     | 打开指定 URL                                                 |
| `tabs` / `focus` / `close` | 标签页管理                                                   |
| `snapshot`                 | 获取页面快照（识别可操作元素）                               |
| `screenshot`               | 截取当前页面图片                                             |
| `act`                      | 交互操作：click / type / press / hover / drag / fill / resize / wait |
| `navigate`                 | 前进 / 后退 / 刷新                                           |
| `console`                  | 查看浏览器控制台日志                                         |
| `pdf`                      | 将当前页面导出为 PDF                                         |
| `upload`                   | 上传文件                                                     |
`snapshot` 有两种模式：`ai`（默认，Playwright 分析页面结构）和 `aria`（返回无障碍树）。`act` 操作需要引用 `snapshot` 返回的元素编号。



需要同时登录多个账号怎么办？
创建多个浏览器 Profile，每个有独立的 Cookie 和登录状态：

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "chrome",
    "profiles": {
      "chrome": { "port": 18800 },
      "work": { "port": 18801 }
    }
  }
}
```

对话中指定用哪个：

```
用 work 浏览器打开飞书文档
```

Profile 命名：小写字母 + 数字 + 短横线，最长 64 字符。端口范围 18800–18899。

## 5. 定时任务（Cron）工具

想让龙虾每天早上给你推新闻？那就需要定时任务。

定时任务配置文件路径： `~/.openclaw/cron/jobs.json`

文件示例： 

```
{
  "version": 1,
  "jobs": [
    {
      "id": "669c0ffd-417e-4dfc-8819-88750558c953",
      "name": "新闻定时推送",
      "enabled": true,
      "createdAtMs": 1773154875569,
      "updatedAtMs": 1773657727534,
      "schedule": {
        "kind": "cron",
        "expr": "0 8,14,18 * * *",
        "staggerMs": 300000
      },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "开始工作。",
        "thinking": "medium",
        "model": "kimi-coding/k2p5"
      },
      "delivery": {
        "mode": "announce",
        "channel": "feishu",
        "to": "oc_927cfcc0ed18dbfb99b4c414963045fb",
        "bestEffort": true
      },
      "state": {
        "nextRunAtMs": 1773705778091,
        "lastRunAtMs": 1773655378096,
        "lastRunStatus": "ok",
        "lastStatus": "ok",
        "lastDurationMs": 12756,
        "lastDeliveryStatus": "delivered",
        "consecutiveErrors": 0,
        "lastDelivered": true
      },
      "deleteAfterRun": false,
      "agentId": "002newsanchor"
    },
    {
      "id": "e447bf7d-d7ec-43ce-a254-66618a075760",
      "name": "南京天气预报",
      "enabled": true,
      "createdAtMs": 1773658088036,
      "updatedAtMs": 1773658088036,
      "schedule": {
        "kind": "cron",
        "expr": "0 8 * * *"
      },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "查询中国江苏省南京市今天的天气，包括温度、天气状况、降雨概率，并给出简单穿衣建议，然后发送到群里。"
      },
      "delivery": {
        "mode": "announce",
        "channel": "feishu",
        "to": "chat:oc_066af8418969975894edf72d74630d28"
      },
      "state": {
        "nextRunAtMs": 1773705600000
      }
    }
  ]
}
```



先做简单测试：

```markdown
openclaw cron add \
  --name "测试消息" \
  --at 1s \
  --delete-after-run \
  --session isolated \
  --wake now \
  --channel feishu \
  --to "chat:oc_066af8418969975894edf72d74630d28" \
  --message "测试消息"
```

飞书群正常： 

```markdown
收到来自 cron 的测试消息。
任务状态： ✅ 成功送达
Cron ID: f6ae3bb7-5bd6-4356-8cee-d62115a8264d
内容: 测试消息
时间: 2026-03-16 18:45 (Asia/Shanghai)
定时任务系统运行正常。
```

最简单的例子：每天早上 8 点发江苏省南京市的天气预报：

```bash
openclaw cron add \
  --name "南京天气预报" \
  --cron "0 8 * * *" \
  --session isolated \
  --channel feishu \
  --to "chat:oc_066af8418969975894edf72d74630d28" \
  --message "查询中国江苏省南京市今天的天气，包括温度、天气状况、降雨概率，并给出简单穿衣建议，然后发送到群里。"
```

三种调度方式按需选：

```bash
# 固定周期：每 30 分钟执行一次
openclaw cron add --name "定期检查" --every 30m \
  --message "检查有没有需要我处理的事情"

# 一次性延时：20 分钟后提醒
openclaw cron add --name "提醒" --at 20m \
  --message "提醒：该休息一下了！"
```

管理任务：

```bash
openclaw cron list                   # 查看所有任务
openclaw cron run 天气预报           # 手动触发一次
openclaw cron runs --id <taskID>     # 查看执行历史
openclaw cron disable 天气预报       # 暂停
openclaw cron enable 天气预报        # 恢复
openclaw cron edit <jobId>           # 编辑
openclaw cron rm <jobId>             # 删除
```

<details>
<summary>Cron 表达式速查（`分 时 日 月 周`）</summary>

| 表达式         | 含义                          |
| -------------- | ----------------------------- |
| `0 8 * * *`    | 每天早上 8:00                 |
| `0 9 * * 1-5`  | 工作日（周一到周五）上午 9:00 |
| `*/30 * * * *` | 每 30 分钟                    |
| `0 20 * * 5`   | 每周五晚上 8:00               |
| `0 0 1 * *`    | 每月 1 日零点                 |



## 6. 命令执行（Exec）工具

`exec` 是龙虾"干活"的核心——安装软件、处理文件、运行脚本都靠它。直接说需求就行：

```
帮我创建一个文件叫 hello.txt，写上今天的日期和"Hello from OpenClaw!"
用 Python 写一个猜数字小游戏，保存为 game.py 并运行它
```

每次执行前龙虾都会请求你确认。

<details>
<summary>exec 参数与后台进程管理</summary>

| 参数         | 说明                     | 默认值          |
| ------------ | ------------------------ | --------------- |
| `command`    | 要执行的命令（必填）     | —               |
| `timeout`    | 超时秒数，超时后终止     | 1800（30 分钟） |
| `background` | 立即后台运行             | false           |
| `yieldMs`    | 超过该毫秒数后自动切后台 | 10000（10 秒）  |
| `pty`        | 是否需要真实终端         | false           |

后台运行的命令通过 `process` 工具管理：

| 操作               | 说明                 |
| ------------------ | -------------------- |
| `list`             | 列出所有后台进程     |
| `poll`             | 获取新输出和退出状态 |
| `log`              | 查看输出日志         |
| `write`            | 向进程写入输入       |
| `kill`             | 终止进程             |
| `clear` / `remove` | 清理已完成的进程     |

<details>
<summary>exec 安全策略</summary>

exec 工具有三种安全级别：

| 级别        | 说明                           |
| ----------- | ------------------------------ |
| `deny`      | 完全禁止执行命令               |
| `allowlist` | 仅允许白名单中的命令           |
| `full`      | 允许执行任何命令（需用户确认） |

如果你需要限制龙虾可以执行的命令范围，通过 `openclaw config set tools.exec.security allowlist` 配置安全级别。

## 7. 工具权限管理

需要限制龙虾的能力？用 `tools.allow` 和 `tools.deny` 精确控制：
`deny` 优先于 `allow`，匹配不区分大小写，支持 `*` 通配符。

```bash
# 禁止浏览器
openclaw config set tools.deny '["browser"]'
# 结果：
  "tools": {
    "profile": "full",
    "deny": [
      "browser"
    ]
  },

# 只允许文件操作和搜索
openclaw config set tools.allow '["group:fs", "group:web"]'
# 结果：
  "tools": {
    "profile": "full",
    "allow": [
      "group:fs",
      "group:web"
    ],
    "deny": [
      "browser"
    ]
  },
```

按模型提供商限制工具
通过 `tools.byProvider` 为不同提供商设置不同权限：

```json
{
  "tools": {
    "profile": "coding",
    "byProvider": {
      "google-antigravity": { "profile": "minimal" }
    }
  }
}
```

`byProvider` 只能**收窄**权限，不能超出全局配置档的范围。支持 `provider`（如 `siliconflow`）或 `provider/model`（如 `openai/gpt-5.2`）两种粒度。

那么

龙虾卡住反复做同一件事怎么办？
启用工具循环检测：

```json
{
  "tools": {
    "loopDetection": {
      "enabled": true,
      "warningThreshold": 10,
      "criticalThreshold": 20,
      "globalCircuitBreakerThreshold": 30
    }
  }
}
```

检测器识别三种循环模式：相同工具反复调用、轮询无进展、两个工具乒乓交替。默认关闭。 

## 8. 插件工具

内置工具不够用？OpenClaw 支持插件扩展：

| 插件              | 说明                                                     |
| ----------------- | -------------------------------------------------------- |
| **Lobster**       | 工作流运行时，支持多步骤任务和可恢复的审批流程           |
| **LLM Task**      | JSON 格式的 LLM 调用，用于结构化输出（可选 Schema 校验） |
| **Diffs**         | 文件差异查看器，支持 PNG / PDF 渲染                      |
| **Voice Call**    | 语音通话插件                                             |
| **Zalo Personal** | Zalo 个人账号插件                                        |

安装和配置详见[附录 G 配置文件详解](/cn/appendix/appendix-g)。

<details>
<summary>工具是怎么让 AI 模型"看见"的？</summary>

OpenClaw 通过两个通道让模型感知工具：

1. **系统提示词**：人类可读的工具列表 + 使用指南
2. **工具 Schema**：结构化的函数定义，发送到模型 API

被 `tools.deny` 禁止的工具不会出现在这两个通道里，模型自然无从调用。



## 插件管理指令

```bash
openclaw plugins list                # 列出已安装插件
openclaw plugins list --json         # JSON 格式
openclaw plugins info <id>           # 查看插件详情
openclaw plugins install <path|.tgz|npm-spec>  # 安装插件
openclaw plugins enable <id>         # 启用插件
openclaw plugins disable <id>        # 禁用插件
openclaw plugins doctor              # 插件诊断
```



# 第八章： Skills



## 1. 技能是什么？

### Skills vs Tools

先分清两个概念：

|          | Tools（工具）                  | Skills（技能）               |
| -------- | ------------------------------ | ---------------------------- |
| **比喻** | 手脚和权限开关                 | 小程序 / 插件                |
| **作用** | 决定 Agent 能不能做某类动作    | 给 Agent 增加特定能力        |
| **例子** | 文件读写、Shell 执行、网络请求 | 网络搜索、天气查询、代码审查 |

简单说：Tools 是"能力通道"，Skills 是"装进通道里的具体能力"。

### 技能三级加载

OpenClaw 按优先级从高到低加载技能：

| 优先级 | 类型         | 位置                            | 说明                         |
| :----: | ------------ | ------------------------------- | ---------------------------- |
|   1    | 工作空间技能 | `~/.openclaw/workspace/skills/` | 当前工作空间专属，优先级最高 |
|   2    | 托管技能     | `~/.openclaw/skills/`           | 通过 ClawHub 安装的共享技能  |
|   3    | 内置技能     | 随 OpenClaw 安装                | 官方捆绑，优先级最低         |

同名技能按优先级覆盖，采用懒加载策略（用到时才读取 SKILL.md 正文）。

---

## 2. 技能的结构

每个技能是一个文件夹，核心是 `SKILL.md`：

```
my-skill/
├── SKILL.md           # 必需：技能定义文件（YAML frontmatter + Markdown 指令）
├── scripts/           # 可选：可执行脚本（搜索、API 调用等）
├── references/        # 可选：参考文档（按需加载，不占常驻上下文）
└── assets/            # 可选：模板、图标等静态资源
```

### SKILL.md 格式

`SKILL.md` 由两部分组成：**YAML frontmatter**（元数据）+ **Markdown 正文**（指令）。

````markdown
---
name: my-skill
description: 技能描述（最重要的字段——AI 根据它决定何时调用此技能）
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    requires:
      env:
        - MY_API_KEY
      bins:
        - node
---

# 技能指令

这里用 Markdown 写清楚 AI 应该怎么使用这个技能。

可以用 `{baseDir}` 引用技能所在目录，OpenClaw 运行时会自动替换为实际路径。
````

### Frontmatter 字段说明

| 字段                                | 必填 | 说明                                                         |
| ----------------------------------- | :--: | ------------------------------------------------------------ |
| `name`                              |  是  | 技能标识符，小写字母 + 连字符（如 `my-awesome-skill`）       |
| `description`                       |  是  | **决定 AI 何时调用此技能**——写清楚"做什么"和"什么时候用"     |
| `user-invocable`                    |  否  | 是否可通过斜杠命令手动调用（默认 `true`）                    |
| `disable-model-invocation`          |  否  | 设为 `true` 则 AI 不会自动触发，只能手动调用（默认 `false`） |
| `homepage`                          |  否  | 技能或服务的官网链接                                         |
| `metadata.openclaw.requires.env`    |  否  | 需要的环境变量（未设置时技能标记为"不可用"）                 |
| `metadata.openclaw.requires.bins`   |  否  | 需要的系统命令（如 `node`、`python`、`curl`）                |
| `metadata.openclaw.requires.config` |  否  | 需要的配置路径                                               |

### 三级加载机制

技能内容按需逐级加载，节省上下文窗口：

| 级别 | 内容                   | 何时加载         | 建议大小 |
| :--: | ---------------------- | ---------------- | -------- |
|  1   | `name` + `description` | 始终在上下文中   | ~100 词  |
|  2   | SKILL.md 正文          | 技能被触发时     | <500 行  |
|  3   | `references/` 中的文件 | 正文中指示读取时 | 不限     |

> **写作建议**：SKILL.md 正文控制在 500 行以内。如果内容较多，将详细文档放到 `references/` 目录，在正文中用"如需了解 X，请读取 `{baseDir}/references/x.md`"指引。

## 3. 你的第一个 Skill

### 1. 创建目录

Skills 位于你的工作区中，通常是 `~/.openclaw/workspace/skills/`。为你的 Skill 创建一个新文件夹：

```
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### 2. 定义 `SKILL.md`

在该目录中创建一个 `SKILL.md` 文件。此文件使用 YAML frontmatter 作为元数据，使用 Markdown 作为指令。

```
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

### 3. 添加工具（可选）

你可以在 frontmatter 中定义自定义工具，或指示智能体使用现有的系统工具（如 `bash` 或 `browser`）。

### 4. 刷新 OpenClaw

让你的智能体”刷新 skills”或重启 Gateway 网关。OpenClaw 将发现新目录并索引 `SKILL.md`。

### 5.最佳实践

- **简洁明了**：指示模型*做什么*，而不是如何成为一个 AI。
- **安全第一**：如果你的 Skill 使用 `bash`，确保提示词不允许来自不受信任用户输入的任意命令注入。
- **本地测试**：使用 `openclaw agent --message "use my new skill"` 进行测试。

## Skills 配置

所有 Skills 相关配置都位于 `~/.openclaw/openclaw.json` 中的 `skills` 下。

```json
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun（Gateway 网关运行时仍为 Node；不推荐 bun）
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

**字段说明**

- `allowBundled`：可选的仅用于**内置** Skills 的白名单。设置后，只有列表中的内置 Skills 才有资格（托管/工作区 Skills 不受影响）。
- `load.extraDirs`：要扫描的附加 Skills 目录（最低优先级）。
- `load.watch`：监视 Skills 文件夹并刷新 Skills 快照（默认：true）。
- `load.watchDebounceMs`：Skills 监视器事件的防抖时间（毫秒）（默认：250）。
- `install.preferBrew`：在可用时优先使用 brew 安装器（默认：true）。
- `install.nodeManager`：node 安装器偏好（`npm` | `pnpm` | `yarn` | `bun`，默认：npm）。这仅影响 **Skills 安装**；Gateway 网关运行时应仍为 Node（不推荐 Bun 用于 WhatsApp/Telegram）。
- `entries.<skillKey>`：单 Skills 覆盖。

单 Skills 字段：

- `enabled`：设置为 `false` 以禁用某个 Skills，即使它是内置/已安装的。
- `env`：为智能体运行注入的环境变量（仅在尚未设置时）。
- `apiKey`：可选的便捷字段，用于声明主环境变量的 Skills。



## 位置和优先级

Skills 从**三个**位置加载：

1. **内置 Skills**：随安装包一起发布（npm 包或 OpenClaw.app）
2. **托管/本地 Skills**：`~/.openclaw/skills`
3. **工作区 Skills**：`<workspace>/skills`

如果 Skills 名称冲突，优先级为：`<workspace>/skills`（最高）→ `~/.openclaw/skills` → 内置 Skills（最低）此外，你可以通过 `~/.openclaw/openclaw.json` 中的 `skills.load.extraDirs` 配置额外的 Skills 文件夹（最低优先级）。

## 单智能体 vs 共享 Skills

在**多智能体**设置中，每个智能体有自己的工作区。这意味着：

- **单智能体 Skills** 位于 `<workspace>/skills` 中，仅供该智能体使用。
- **共享 Skills** 位于 `~/.openclaw/skills`（托管/本地），对同一机器上的**所有智能体**可见。
- 如果你想要多个智能体使用一个通用的 Skills 包，也可以通过 `skills.load.extraDirs`（最低优先级）添加**共享文件夹**。

如果同一个 Skills 名称存在于多个位置，将应用通常的优先级规则：工作区优先，然后是托管/本地，最后是内置。

## 插件 + Skills

插件可以通过在 `openclaw.plugin.json` 中列出 `skills` 目录（相对于插件根目录的路径）来发布自己的 Skills。插件 Skills 在插件启用时加载，并参与正常的 Skills 优先级规则。你可以通过插件配置条目上的 `metadata.openclaw.requires.config` 对它们进行门控。参见[插件](https://docs.openclaw.ai/tools/plugin)了解发现/配置，以及[工具](https://docs.openclaw.ai/tools)了解这些 Skills 所教授的工具接口。

## ClawHub

ClawHub 是 **OpenClaw 的公共 Skills 注册中心**。它是一项免费服务：所有 Skills 都是公开的、开放的，所有人都可以查看、共享和复用。Skills 就是一个包含 `SKILL.md` 文件（以及辅助文本文件）的文件夹。你可以在网页应用中浏览 Skills，也可以使用 CLI 来搜索、安装、更新和发布 Skills。网站：[clawhub.com](https://clawhub.com/)

**ClawHub使用流程：**

- 安装安装 CLI

  ```
  npm i -g clawhub
  pnpm add -g clawhub
  ```
  
- 登陆

  ```
  clawhub login
  clawhub whoami
  ```

- 搜索你需要的skills

  ```
  clawhub search "calendar"
  
  (base) will@MacMini-Will extensions % clawhub search "calendar"
  calendar  Calendar  (3.722)
  gcalcli-calendar  Google Calendar (via gcalcli)  (3.660)
  feishu-calendar  feishu-calendar  (3.639)
  lark-calendar  Lark Calendar & Tasks  (3.593)
  macos-calendar  macOS Calendar  (3.574)
  gog-calendar  Google Calendar (via gogcli)  (3.572)
  brainz-calendar  Calendar  (3.518)
  calendar-manager  Calendar Manager  (3.488)
  dingtalk-calendar  Dingtalk Calendar  (3.469)
  yandex-calendar  yandex-calendar  (3.465)
  ```

- 将 Skills 安装到你的工作区：

  ```
  clawhub install <skill-slug>
  ```

- 更新所有已安装的 Skills：

  ```
  clawhub update --all
  ```

- 同步（扫描 + 发布更新）：

  ```
  clawhub sync --all
  ```

注意：

默认情况下，CLI 会将 Skills 安装到当前工作目录下的 `./skills`。如果已配置 OpenClaw 工作区，`clawhub` 会回退到该工作区，除非你通过 `--workdir`（或 `CLAWHUB_WORKDIR`）进行覆盖。OpenClaw 从 `<workspace>/skills` 加载工作区 Skills，并会在**下一个**会话中生效。如果你已经在使用 `~/.openclaw/skills` 或内置 Skills，工作区 Skills 优先级更高。



## SkillHub



SkillHub 是腾讯推出的专为中国用户优化的 AI Skills 社区，专为解决国内用户使用官方 ClawHub 时遭遇的下载慢、搜索不友好、全英文界面等痛点。平台依托腾讯云国内节点提供高速镜像，收录超过 1.3 万个 Skills，并从中精选 Top 50 优质榜单，每个上榜 Skill 均经过安全审核与多维度评估。提供全中文界面、中文友好搜索引擎和 8 大分类体系，帮助用户高效发现所需工具。



在终端中执行以下命令，即可安装 SkillHub CLI

```
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash -s -- --no-skills
```

在终端中执行以下命令，即可安装 SkillHub CLI，并且优先采用 SkillHub 加速安装技能

```curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash
```

添加环境变量
```
vim ~/.zshrc
export PATH="/Users/will/.local/bin:$PATH"
```
```
source ~/.zshrc
```
安装完 CLI 后，安装技能

```
skillhub install self-improving-agent
```
