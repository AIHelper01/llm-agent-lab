# Heartbeat 与 Cron 深度分析

> 理解 OpenClaw 的两大调度系统及其协同机制

---

## 一、核心概念对比

| 维度 | Heartbeat | Cron |
|------|-----------|------|
| **本质** | 周期性 Agent Turn（主会话） | 调度器 + 可配置执行 |
| **触发** | 定时器（每 N 分钟） | 定时器 + 条件（cron 表达式） |
| **会话** | 主会话（`agent:<id>:main`） | 主会话 或 隔离会话（`cron:<jobId>`） |
| **上下文** | 完整主会话历史 | 主会话 或 全新（isolated） |
| **交付** | 可配置（target + directPolicy） | announce/webhook/none |
| **用途** | 周期性检查、监控、轻量提醒 | 精确调度、批量任务、一次性事件 |

---

## 二、Heartbeat 详解

### 2.1 工作机制

```
Gateway Scheduler (每 30min)
    ↓
读取 HEARTBEAT.md（如果存在）
    ↓
注入主会话上下文
    ↓
运行 Agent Turn
    ↓
检查输出：
  - 纯 HEARTBEAT_OK + ≤300char → 丢弃（不发送）
  - 其他内容 → 根据 target 配置发送
```

### 2.2 关键配置

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",                    // 间隔（默认 30min 或 Anthropic OAuth 1h）
        target: "last",                  // 发送目标：none（默认）/ last / <channel>
        directPolicy: "allow",           // DM 发送：allow（默认）/ block
        activeHours: {                   // 活跃时间窗口（可选）
          start: "08:00",
          end: "22:00",
          timezone: "Asia/Shanghai"
        },
        lightContext: false,             // 轻量上下文（仅 HEARTBEAT.md）
        includeReasoning: false,         // 是否发送 Reasoning 消息
        ackMaxChars: 300,                // HEARTBEAT_OK 后允许的最大字符
        prompt: "默认提示词...",          // 可自定义
        session: "main",                 // 会话 key（默认主会话）
        model: "...",                    // 可覆盖模型（可选）
        suppressToolErrorWarnings: false // 抑制工具错误警告
      },
    },
  },
}
```

### 2.3 执行流程

1. **时间检查**：
   - 间隔是否已过？
   - 是否在 `activeHours` 内？
   - 主队列是否空闲（通过 Command Queue）？

2. **上下文准备**：
   - 正常模式：注入所有 Bootstrap 文件（AGENTS.md, SOUL.md, TOOLS.md 等）
   - `lightContext: true`：仅注入 `HEARTBEAT.md`

3. **Agent 运行**：
   - Prompt = ` heartbeat.prompt + HEARTBEAT.md 内容`
   - 主会话历史 + 近期工具结果（已 prune）
   - 模型生成回复

4. **响应处理**：
   - 检测 `HEARTBEAT_OK`：
     - 出现于开头或结尾 → 视为 ack，可能丢弃
     - 纯 ack（剩余 ≤ `ackMaxChars`）→ 不发送
   - 非 ack 内容 → 正常发送（通过 target 路由）

5. **会话状态**：
   - 心跳**不更新**会话 `updatedAt`（不影响 idle reset）
   - 仅当实际发送消息时才保持活跃

### 2.4 发送控制

```yaml
# 按渠道控制可见性
channels:
  defaults:
    heartbeat:
      showOk: false      # 默认隐藏 HEARTBEAT_OK
      showAlerts: true   # 默认显示告警
      useIndicator: true # 发送 UI 指示器
  telegram:
    heartbeat:
      showOk: true       # Telegram 显示 OK
  whatsapp:
    accounts:
      personal:
        heartbeat:
          showAlerts: false  # 个人账号不发送告警
```

---

## 三、Cron 详解

### 3.1 核心架构

```
Gateway Scheduler
    ├─ 检查 job 调度（cron 表达式/interval/at）
    ├─ 决定执行模式：
    │   ├─ Main Session (systemEvent)
    │   │   └─ 注入主会话队列 → 在下次心跳运行
    │   └─ Isolated Session (agentTurn)
    │       └─ 创建独立会话 cron:<jobId> → 立即运行（不等待心跳）
    └─ 交付处理：
        ├─ announce → 直接发送到目标频道
        ├─ webhook → HTTP POST
        └─ none → 静默
```

### 3.2 执行模式对比

| 特性 | Main Session (systemEvent) | Isolated Session (agentTurn) |
|------|---------------------------|----------------------------|
| 会话 key | `agent:<id>:main` | `cron:<jobId>`（新会话） |
| 历史 | 共享主会话历史 | 每次 fresh（无历史） |
| 上下文 | 完整主会话 | 仅 bootstrap（可轻量） |
| 模型 | 主会话模型（可覆盖） | 可独立覆盖 |
| Thinking | 主会话级别 | 可独立覆盖 |
| 交付 | 等待心跳发送（`wakeMode`） | 立即 announce（默认）或 webhook |
| 历史污染 | 是（加入主历史） | 否（独立会话） |
| 用途 | 轻量事件、提醒 | 重量任务、报告、后台作业 |

### 3.3 调度类型

#### 一次性（`at`）
```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-03-20T14:00:00Z" \
  --session main \
  --system-event "Meeting in 10 min" \
  --wake now \
  --delete-after-run  # 默认 true
```
- ISO 8601 时间戳（默认 UTC）
- 默认执行后删除（`deleteAfterRun: true`）
- 失败重试：最多 3 次，指数退避（30s → 1m → 5m）

#### 间隔（`every`）
```bash
openclaw cron add \
  --name "Health check" \
  --every "4h" \
  --session isolated \
  --message "Check system health" \
  --announce
```
- 固定间隔（毫秒或人类可读：`4h`, `30m`, `1h`）
- 永久运行，失败后退避（30s → 1m → 5m → 15m → 60m）

#### Cron 表达式（`cron`）
```bash
openclaw cron add \
  --name "Daily report" \
  --cron "0 7 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Send daily report" \
  --announce
```
- 5 字段（分时日月周）或 6 字段（含秒）
- 可选 `tz`（IANA 时区）
- 自动 stagger：整点任务随机偏移 0-5 分钟（避免负载峰值）
- 可关闭 stagger：`--exact` 或 `--stagger 0`

### 3.4 交付模式

#### Announce（默认，isolated）
- 直接通过渠道发送结果
- 不使用消息工具（避免循环）
- 主会话收到简短摘要（可选）
- `delivery.bestEffort: true` 忽略发送失败

#### Webhook
```json5
{
  delivery: {
    mode: "webhook",
    to: "https://example.com/webhook",
  }
}
```
- POST finished event JSON 到 URL
- 可选 `cron.webhookToken` 提供 Bearer 认证
- 主会话不收到摘要

#### None
```json5
{
  delivery: { mode: "none" }
}
```
- 无外送，仅内部记录
- 适合纯数据收集任务

### 3.5 模型与上下文控制

```bash
# 使用更便宜的模型
openclaw cron add ... --model "sonnet"

# 深度思考（仅支持 GPT-5.2 / Codex）
openclaw cron add ... --thinking high

# 轻量上下文（不注入工作区文件）
openclaw cron add ... --light-context
```

---

## 四、协同机制

### 4.1 队列层级

```
┌─────────────────────────────────────────────┐
│          Command Queue (Lane-aware)         │
├─────────────────────────────────────────────┤
│  Lane: session:<key> (per-session lock)    │
│  Lane: main (global inbound + heartbeats)  │
│  Lane: cron (cron jobs, isolated)          │
│  Lane: subagent (subagent runs)            │
└─────────────────────────────────────────────┘
```

**关键点**：
- Heartbeat 和 Cron (isolated) 使用**不同 lane** → 可并行
- Cron (main) 通过 `systemEvent` 加入 main session queue → 与 inbound 消息竞争
- 默认 `agents.defaults.maxConcurrent: 4`（全局并发限制）

### 4.2 触发链路

#### 场景 1: Heartbeat 周期触发

```
Timer (every 30m)
    ↓
Heartbeat Runner
    ↓
读取 HEARTBEAT.md
    ↓
Enqueue to main lane (session:agent:main:main)
    ↓
Agent 执行（完整上下文）
    ↓
发送结果（根据 target）
```

#### 场景 2: Cron（isolated）精确触发

```
Timer (cron 0 7 * * *)
    ↓
Cron Scheduler
    ↓
创建独立会话：cron:<jobId>
    ↓
Enqueue to cron lane (session:cron:<jobId>)
    ↓
Agent 执行（轻量/可配置上下文）
    ↓
直接 announce 发送（不等待心跳）
```

#### 场景 3: Cron（main）配合 Heartbeat

```
Cron Job (systemEvent, wakeMode: "now")
    ↓
Enqueue system event to main session queue
    ↓
下一个可用心跳处理该事件（与其他 inbound 竞争）
    ↓
Heartbeat 运行（包含系统事件）
    ↓
发送结果
```

**这意味着**：
- `systemEvent` cron 不直接执行 Agent turn，只是注入事件
- 实际执行依赖下一个 heartbeat（或手工 `openclaw system event --mode now`）
- 此时 main session 上下文已包含事件内容

#### 场景 4: Mix 实际例子

```yaml
# 配置
heartbeat:
  every: 30m
  target: none  # 不发送，仅内部检查

cron:
  - name: "Daily report"
    schedule: "0 7 * * *"
    session: isolated
    delivery:
      mode: announce
      channel: whatsapp
      to: "+1555..."
  - name: "Reminder"
    schedule: "at: 2026-03-20T14:00:00Z"
    session: main
    payload: systemEvent
    wakeMode: now
```

**时间线**（3月20日）：

| 时间 | 事件 | 执行者 | 说明 |
|------|------|--------|------|
| 13:30 | Heartbeat 触发 | main session | 检查 inbox/calendar，无大事 → `HEARTBEAT_OK`（不发送） |
| 14:00 | Cron (at) 触发 | systemEvent → 加入 main queue | 提醒事件入队 |
| 14:00 | Heartbeat 被唤醒 | main session | 处理 reminder 事件 |
| 14:00 | 发送 "Reminder: ..." | WhatsApp | 发送提醒 |
| 07:00 (次日) | Cron (daily) 触发 | isolated session | 独立运行，生成报告 |
| 07:00 | 直接 announce | WhatsApp | 发送日报 |

**观察**：
- 心跳每 30min 周期运行（但实际发送仅当有内容）
- Cron isolated 不依赖心跳，独立执行
- Cron main 通过 system event 调用心跳

### 4.3 资源竞争与并发

**队列规则**：
1. 同一 session key 的 turn 串行化（`session:<key>` lane）
2. 全局 lane `main` 受 `maxConcurrent` 限制（默认 4）
3. Heartbeat 和 Cron (isolated) 使用**不同 lane**（`main` vs `cron`）→ 可同时运行

**潜在冲突**：
- 如果 inbound 消息很多，main lane 繁忙 → heartbeat 可能延迟或跳过（检测到 busy 后 skip）
- 若 cron 太多，cron lane 串行化 → 任务排队（可调整 `cron.maxConcurrentRuns`）

---

## 五、配置与调优

### 5.1 典型双轨配置

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "none",      // 默认为检查，不发送
        activeHours: { start: "08:00", end: "23:00", timezone: "Asia/Shanghai" },
      },
    },
  },

  cron: {
    enabled: true,
    maxConcurrentRuns: 2,  // 允许并行运行 2 个 cron job
    sessionRetention: "24h",
    runLog: { maxBytes: "2mb", keepLines: 2000 },
  },
}
```

### 5.2 成本优化

| 策略 | 配置 | 效果 |
|------|------|------|
| 仅检查，不发送 | `heartbeat.target: "none"` | 只在有告警时发送 |
| 轻量上下文 | `heartbeat.lightContext: true` | 减少 token 使用 |
| 批量 cron | 将多个定时任务合并为一个 isolated job | 减少独立 Agent turn 数量 |
| 任务分离 | heartbeat 只检查，cron 做重任务 | 避免主会话历史膨胀 |

### 5.3 可见性与调试

```bash
# 查看心跳状态
openclaw status | grep heartbeat

# 查看 cron 作业列表
openclaw cron list

# 查看最近运行
openclaw cron runs --id <jobId> --limit 20

# 查看主队列深度（verbose 日志启用）
tail -f ~/.openclaw/logs/gateway.log | grep "queued for"

# 强制立即心跳（不等待时间）
openclaw system event --mode now --text "Forced heartbeat"

# 手动运行 cron
openclaw cron run <jobId>
```

### 5.4 常见问题排查

#### 1. Heartbeat 不执行

- `heartbeat.every` 是否为 0？（0 表示禁用）
- 是否在 `activeHours` 窗口外？
- 主队列是否持续繁忙？（大量 inbound 消息）
- 检查日志：`grep "heartbeat" ~/.openclaw/logs/gateway.log`

#### 2. Cron 不触发

- `cron.enabled: true` 了吗？
- Gateway 进程是否持续运行？（cron 在内存中调度）
- 时区是否正确？`--tz` 或使用本地时区
- 查看调度器状态：`openclaw cron status`

#### 3. 消息延迟

- 检查 `messages.queue` 模式（`collect` 模式会累积然后批量处理）
- `debounceMs` 导致的延迟（默认 1s）
- 队列深度：`openclaw sessions list` 查看未处理消息数

#### 4. 会话混乱

- 确认 `sessionTarget` 选择正确
- `main` vs `isolated` 的上下文隔离
- 查看 `sessions.json` 区分 `agent:main:main` 与 `cron:<jobId>`

---

## 六、设计模式与最佳实践

### 6.1 推荐组合

**个人助理**：
- Heartbeat：每 30min 检查 inbox/calendar/reminders
- Cron：日报（早 8 点）、周报（周一 9 点）、一次性提醒

**团队 bot**：
- Heartbeat：监控项目频道（每 1h，静默检查）
- Cron：每日站会通知（工作日 9:00）、每周回顾（周五 17:00）

**监控代理**：
- Heartbeat：每 15min 系统健康检查（轻量）
- Cron：每小时深度分析（isolated，使用强模型）

### 6.2 避免反模式

❌ **不要** 用 heartbeat 做精确定时任务（时间不保证）  
❌ **不要** 在 `HEARTBEAT.md` 放长列表（token 浪费）  
❌ **不要** 创建大量 cron 高频任务（可能队列阻塞）  
❌ **不要** 混合 main/isolated 模式导致上下文混淆  
❌ **不要** 忽视 `activeHours`（夜间不必要的开销）

### 6.3 高级技巧

#### 动态调整心跳间隔

```json5
// 工作时间密集，非工作稀疏
agents:
  list:
    - id: "main"
      heartbeat:
        every: "15m"  # 工作时间
        activeHours:
          start: "09:00"
          end: "18:00"
        # 非工作时间自动回落到默认间隔（或可设另一个 less frequent）
```

#### 条件化 cron 执行

在 `agentTurn` prompt 中添加逻辑：

```
如果今天是周末，跳过日报生成。
否则，生成日报。
```

#### 链式任务（cron 触发 cron）

cron job A 完成后，调用 `cron.add` 创建 job B（通过工具）。

### 6.4 监控与告警

```bash
# 检查心跳是否在运行（日志中有 heartbeat 条目）
grep -q "heartbeat" ~/.openclaw/logs/gateway.log && echo "OK"

# 检查 cron 最近执行
openclaw cron runs --id <jobId> --limit 5 | jq '.[] | {time: .finishedAt, success: .success}'

# 查看队列深度
openclaw sessions list --json | jq '.sessions | length'
```

设置一个 cron 监控另一个 cron：

```bash
openclaw cron add \
  --name "Cron monitor" \
  --every "1h" \
  --session isolated \
  --message "检查以下 cron 是否在过去 2h 运行过：daily-report, weekly-review" \
  --announce
```

---

## 七、底层实现参考

### 7.1 Scheduler 生命周期

Gateway 启动时：
1. 加载 `cron/jobs.json`
2. 启动定时器（`setInterval`，精度约 1min）
3. 每次 tick 检查到期 job
4. 执行（enqueue 或立即运行 isolated）

Heartbeat：
- 在 Agent 运行时检查时间间隔
- 每次心跳后重置计时器
- 如果 `target: "last"`，记录最后外送渠道

### 7.2 序列化保证

- 同 session 的 turn 通过 `session:<key>` lane 串行
- Heartbeat 使用主 session lane → 与 inbound 互斥
- Isolated cron 使用独立 lane → 并行
- 默认 `maxConcurrent=4` 允许多 session 并行

### 7.3 错误处理

**Transient**（重试）：
- 429 rate limit
- 5xx 服务器错误
- 网络超时、连接重置

**Permanent**（直接禁用 oneshot，recurring 保持但应用退避）：
- 401/403 鉴权失败
- 配置错误
- 模型不支持

重试退避：
```
第一次失败: wait 30s
第二次失败: wait 1m
第三次失败: wait 5m
后续: 15m → 60m (不断递增)
```
成功后重置退避计时。

---

## 八、FAQ

**Q: Heartbeat 和 Cron 能同时启用吗？**  
A: 可以，它们独立运行。通常组合使用：heartbeat 做检查，cron 做精确任务。

**Q: Heartbeat 会更新会话 idle 计时吗？**  
A: 不会。即使发送了消息，`updatedAt` 保持不变，不影响 `session.reset.idleMinutes`。

**Q: Cron isolated 会话会被维护清理吗？**  
A: 会。`cron.sessionRetention` 控制（默认 24h），超时会归档/删除。

**Q: HEARTBEAT.md 可以动态生成吗？**  
A: 可以。Agent 可以用 `write` 工具更新它。

**Q: 如何让 cron 任务等待 heartbeat 窗口？**  
A: 设置 `wakeMode: "next-heartbeat"`（默认是 `now`）。

**Q: 多个 heartbeat 会并行吗？**  
A: 不会。同一 heartbeat 配置（同 agent）是全局间隔，不会重叠。

**Q: Cron 失败会通知吗？**  
A: 失败日志会记录；如果 `delivery.mode=announce` 且任务有输出，失败信息可能发送（取决于实现）。可增加监控 cron 作业 health 的 cron。

**Q: 可以暂停单个 cron 作业吗？**  
A: `openclaw cron edit <id> --enabled false`。

**Q: Heartbeat 会触发上下文压缩吗？**  
A: 会。正常 Agent turn，token 接近阈值时会触发 compaction。

---

## 九、总结与建议

### 核心差异

| 维度 | Heartbeat | Cron |
|------|-----------|------|
| **精确性** | 近似（受队列影响） | 精确（cron 表达式） |
| **时机** | 周期性（固定间隔） | 时间驱动（表达式） |
| **上下文** | 主会话 | 主会话 或 隔离 |
| **交付** | 可配置（target） | announce/webhook/none |
| **最佳用途** | 批量检查、监控 | 定时报告、一次性事件 |

### 选择策略

- **用 Heartbeat 如果**：
  - 你想 batch 多个周期性检查
  - 任务需要 conversational context
  - 你希望 silent OK 行为
  - 时间灵活性可接受（± few minutes）

- **用 Cron 如果**：
  - 需要精确时间（"9:00 整"）
  - 任务应独立于主上下文
  - 需要不同模型/thinking 级别
  - 一次性 reminder（`--at`）
  - 必须避免污染主会话历史

### 推荐架构

```yaml
heartbeat:
  every: 30m
  target: none
  activeHours: 08:00-23:00

cron:
  - name: "Morning brief"
    cron: "0 7 * * *"
    session: isolated
    delivery: { mode: announce, channel: whatsapp }

  - name: "Weekly review"
    cron: "0 9 * * 1"
    session: isolated
    model: opus
    thinking: high
    delivery: { mode: webhook, to: "https://..." }

  - name: "Meeting reminder"
    at: "2026-03-20T14:00:00Z"
    session: main
    payload: systemEvent
    wakeMode: now
```

### 监控清单

- [ ] Heartbeat 间隔是否合理（避免过频）？
- [ ] CRON 时区是否正确？
- [ ] `HEARTBEAT.md` 是否精简？
- [ ] Isolated cron 会话保留期（`sessionRetention`）是否合适？
- [ ] 队列深度是否健康（无持续积压）？

---
