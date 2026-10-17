# GLM 核心技术演进

> 从 GLM、GLM-130B、ChatGLM、GLM-4，到 GLM-4.5、GLM-5、GLM-5.2 与最新 GLM-5.3

---

# 第一篇：主模型与技术全景

## 一、先看全景：GLM 到底在解决什么问题？

GLM 的演进跨度很长。它并不是从 ChatGLM 才开始，而是可以追溯到 2021 年的 **General Language Model（GLM）**。

如果只看产品名，容易得到：

```text
ChatGLM
  ↓
ChatGLM2
  ↓
ChatGLM3
  ↓
GLM-4
  ↓
GLM-4.5
  ↓
GLM-5
```

但从技术角度，更准确的路线是：

```text
GLM Pretraining
      ↓
GLM-130B
大规模双语预训练
      ↓
ChatGLM
对话 / 指令对齐
      ↓
ChatGLM2 / 3
长上下文 + Tool Use
      ↓
GLM-4
128K / 1M + All Tools
      ↓
GLM-4.5
MoE + ARC
Agentic / Reasoning / Coding
      ↓
GLM-5
DSA + Async RL
      ↓
GLM-5.1
Long-Horizon Agent
      ↓
GLM-5.2
1M + IndexShare + MTP + Long-Horizon RL
      ↓
GLM-5.3
Scaling Post-training
Frontier Coding + Long-Horizon Agent
```

---

## 二、GLM 核心问题地图

| 核心问题 | GLM 技术 / 模型 | 一句话理解 |
| --- | --- | --- |
| **预训练目标怎么统一？** | GLM | Autoregressive Blank Infilling |
| **百亿 / 千亿模型怎么稳定训练？** | GLM-130B | 大规模双语预训练 + 稳定性工程 |
| **怎么变成聊天模型？** | ChatGLM | Instruction / Dialogue Alignment |
| **怎么支持长上下文？** | ChatGLM2 → GLM-4 → GLM-5.2 | 32K → 128K / 1M → Solid 1M |
| **怎么使用工具？** | ChatGLM3 → GLM-4 All Tools | Function Call → Autonomous Tool Use |
| **模型怎么做大又控制计算？** | GLM-4.5 / GLM-5 | MoE |
| **长上下文 Attention 怎么少算？** | GLM-5 | DSA |
| **1M Context 怎么进一步降成本？** | GLM-5.2 | IndexShare for DSA |
| **生成怎么更快？** | GLM-5.2 | Improved MTP + Speculative Decoding |
| **Reasoning / Coding / Agent 怎么统一？** | GLM-4.5 | ARC Foundation Model |
| **RL 怎么扩到复杂 Agent？** | GLM-5 | slime + Asynchronous Agent RL |
| **怎么做长时程 Agent？** | GLM-5.1 → 5.2 → 5.3 | 8h Execution → 1M Context → Scaling Post-training |
| **多模态怎么推理？** | CogVLM → GLM-4V → GLM-4.1V / 4.5V → GLM-5V | Visual Expert → Scalable Multimodal RL |

---

## 三、关键论文 / 技术报告时间线

| 时间 | 模型 / 技术 | 类型 | 论文 / 技术报告 | 核心技术 |
| --- | --- | --- | --- | --- |
| 2021.03 | **GLM** | Pretraining | *GLM: General Language Model Pretraining with Autoregressive Blank Infilling* | Autoregressive Blank Infilling、2D Position Encoding |
| 2022.10 | **GLM-130B** | 基座模型 | *GLM-130B: An Open Bilingual Pre-trained Model* | 130B、Bilingual、Training Stability、INT4 |
| 2023 | **ChatGLM / 2 / 3** | Chat / Tool | ChatGLM Family | Dialogue Alignment、Long Context、Tool Use |
| 2024.06 | **GLM-4** | 主模型 | *ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools* | 10T Tokens、128K / 1M、All Tools |
| 2025.07 | **GLM-4.1V-Thinking** | Multimodal Reasoning | *GLM-4.1V-Thinking and GLM-4.5V* | Scalable RL、Multimodal Reasoning |
| 2025.08 | **GLM-4.5** | 主模型 | *GLM-4.5: Agentic, Reasoning, and Coding Foundation Models* | MoE、355B / 32B Active、ARC、Hybrid Reasoning |
| 2025.09 | **GLM-4.6** | 主模型迭代 | 官方技术发布 | 200K、Coding、Reasoning、Agent |
| 2026.02 | **GLM-5** | 主模型 | *GLM-5: from Vibe Coding to Agentic Engineering* | 744B / 40B Active、DSA、slime、Async Agent RL |
| 2026.04 | **GLM-5.1** | 主模型迭代 | 官方技术发布 | Long-Horizon Agent、8h Autonomous Execution |
| 2026.06 | **GLM-5.2** | 主模型迭代 | 官方技术发布 | **1M Context、IndexShare、MTP、Long-Horizon RL** |
| 2026.08 | **GLM-5.3** | 最新主模型 | 官方技术发布 | **Scaling Post-training、Frontier Coding、Long-Horizon Agent** |

---

# 第二篇：GLM 基础架构演进

# 四、GLM：从 GPT / BERT 二分法走向统一预训练

## 4.1 论文

**GLM: General Language Model Pretraining with Autoregressive Blank Infilling**

https://arxiv.org/abs/2103.10360

早期 NLP 预训练大致分成：

```text
BERT
Autoencoding
擅长理解

GPT
Autoregressive
擅长生成

T5
Encoder-Decoder
擅长条件生成
```

GLM 希望用一个统一框架覆盖：

```text
NLU
+
Conditional Generation
+
Unconditional Generation
```

核心：

# Autoregressive Blank Infilling

概念上：

```text
原文：

The quick brown fox jumps over the lazy dog.

↓

挖掉 Span：

The [MASK] fox jumps over [MASK].

↓

模型自回归生成：

quick brown
+
the lazy dog
```

与普通 Masked Language Modeling 不同：

> GLM 不是独立预测每个 Mask，而是以自回归方式生成被遮住的 Span。

---

## 4.2 2D Positional Encoding

GLM 还使用二维位置编码，让模型同时知道：

```text
这个 Span 在原文哪里
        +
Span 内当前生成到哪里
```

一句话：

> **GLM：把“填空”和“自回归生成”统一起来。**

这是整个 GLM 家族名字的真正技术起点。

---

# 五、GLM-130B：把 GLM 扩到千亿参数

## 5.1 论文

**GLM-130B: An Open Bilingual Pre-trained Model**

https://arxiv.org/abs/2210.02414

模型规模：

```text
130B Parameters
Chinese + English
```

GLM-130B 的意义不只是“大”。

它重点解决了：

```text
100B+ Training
     │
     ├─ Loss Spike
     ├─ Divergence
     ├─ Training Stability
     └─ Engineering Efficiency
```

论文还展示了 GLM-130B 的量化能力，包括 INT4 推理。

一句话：

> **GLM-130B：把 GLM 从预训练方法真正扩展成百亿 / 千亿级基础模型。**

---

# 六、ChatGLM：从 Foundation Model 到 Chat Model

ChatGLM 将 GLM 基座进一步转向：

```text
Foundation Model
       ↓
Instruction Alignment
       ↓
Dialogue Alignment
       ↓
Chat Model
```

早期路线：

```text
GLM-130B
   ↓
ChatGLM-6B
   ↓
ChatGLM2
   ↓
ChatGLM3
```

可以把三个阶段简单理解为：

| 模型 | 重点 |
| --- | --- |
| **ChatGLM** | 中文 / 英文对话能力 |
| **ChatGLM2** | 更强性能 + 更长 Context |
| **ChatGLM3** | Tool Use / Function Call / Agent 能力 |

---

# 七、GLM-4：从 Chat 走向 All Tools

## 7.1 技术报告

**ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools**

https://arxiv.org/abs/2406.12793

GLM-4 系列预训练规模达到约：

```text
10T Tokens
```

并覆盖：

```text
Chinese
English
+
24 Languages
```

长上下文能力进入：

```text
128K
+
1M Variant
```

---

## 7.2 GLM-4 All Tools

GLM-4 一个非常重要的变化是：

> 模型开始自己判断什么时候使用工具，以及使用什么工具。

工具包括：

```text
Web Browser
Python Interpreter
Text-to-Image
User-defined Functions
```

路线：

```text
ChatGLM
会聊天
   ↓
ChatGLM3
会 Function Call
   ↓
GLM-4 All Tools
会自主选择工具
```

一句话：

> **GLM-4：从“会回答”走向“会调用工具完成任务”。**

---

# 第三篇：ARC——Agentic、Reasoning、Coding

# 八、GLM-4.5：ARC Foundation Model

## 8.1 论文

**GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models**

https://arxiv.org/abs/2508.06471

GLM-4.5 是 GLM 技术路线的重要分水岭。

它把三种能力统一成：

# ARC

```text
A = Agentic
R = Reasoning
C = Coding
```

即：

```text
                    GLM-4.5
                       │
          ┌────────────┼────────────┐
          │            │            │
       Agentic      Reasoning      Coding
```

---

## 8.2 GLM-4.5 的 MoE

GLM-4.5：

```text
355B Total Parameters
32B Active Parameters
```

同时还有：

```text
GLM-4.5-Air
106B Total
```

这意味着 GLM 正式进入大规模 MoE 路线：

```text
Dense / Earlier GLM
       ↓
GLM-4.5 MoE
355B / 32B Active
       ↓
GLM-5 MoE
744B / 40B Active
```

一句话：

> **模型容量大幅增加，但每个 Token 只激活少量参数。**

---

## 8.3 Hybrid Reasoning

GLM-4.5 支持：

```text
Thinking Mode
+
Direct Response Mode
```

也就是：

```text
复杂任务
   ↓
Thinking
   ↓
Long Reasoning

简单任务
   ↓
Direct Response
```

一句话：

> **需要思考时深度推理，不需要时直接回答。**

---

## 8.4 Multi-stage Training

GLM-4.5 使用约：

```text
23T Pre-training Tokens
```

然后通过：

```text
Pre-training
     ↓
SFT
     ↓
Expert Model Iteration
     ↓
Reinforcement Learning
```

强化：

```text
Agent
Reasoning
Coding
```

因此 GLM-4.5 的定位不是普通 Chat Model，而是：

> **面向 Agentic / Reasoning / Coding 的 Foundation Model。**

---

# 九、GLM-4.6：Context 与 Agent 继续增强

GLM-4.6 把上下文从：

```text
128K
 ↓
200K
```

同时继续强化：

```text
Coding
+
Reasoning
+
Tool Use
+
Search Agent
```

它更像 GLM-4.5 ARC 路线的强化版本，而不是一次基础架构大换代。

---

# 第四篇：GLM-5——从 Vibe Coding 到 Agentic Engineering

# 十、GLM-5：规模再次扩大

## 10.1 技术报告

**GLM-5: from Vibe Coding to Agentic Engineering**

https://arxiv.org/abs/2602.15763

GLM-5：

```text
744B Total Parameters
40B Active Parameters
28.5T Pre-training Tokens
```

对比 GLM-4.5：

| 模型 | 总参数 | 激活参数 | Pre-training Tokens |
| --- | ---: | ---: | ---: |
| GLM-4.5 | 355B | 32B | 23T |
| GLM-5 | 744B | 40B | 28.5T |

可以看到：

```text
Model Capacity ↑↑
Active Compute ↑
Training Data ↑
```

---

# 十一、GLM-5：正式引入 DSA

GLM-5 一个非常重要的架构变化：

# DSA

**DeepSeek Sparse Attention**

需要特别说明：

> **DSA 不是 GLM 原创，而是 GLM-5 集成采用的 Sparse Attention 技术。**

传统 Dense Attention：

```text
Query
  ↓
所有历史 Token
  ↓
Attention
```

DSA：

```text
Query
  ↓
Indexer
  ↓
Top-K Relevant Tokens
  ↓
Sparse Attention
```

一句话：

> **DSA：先找重要 Token，再真正做 Attention。**

作用：

```text
Long Context
    ↓
Attention FLOPs ↓
    ↓
Training / Inference Cost ↓
```

因此：

> **GLM-5 用 DSA 解决长上下文 Attention 计算成本。**

---

# 十二、GLM-5：slime 异步 RL 基础设施

GLM-5 的另一条核心路线不是模型 Architecture，而是：

# RL Infrastructure

GLM 团队开发：

**slime**

其核心是：

> Generation 与 Training 解耦。

传统同步 RL：

```text
Generate
   ↓
Wait
   ↓
Train
   ↓
Wait
   ↓
Generate
```

异步 RL：

```text
Generation Workers ─────┐
Generation Workers ─────┤
                        ▼
                    Experience
                        │
                        ▼
                   RL Training
                        │
                        └──持续更新
```

目标：

```text
GPU Utilization ↑
RL Throughput ↑
Iteration Speed ↑
```

一句话：

> **slime：让 Agent RL 不必“生成完再等训练”，而是异步流水起来。**

---

# 十三、Asynchronous Agent RL

GLM-5 进一步提出面向 Agent 的异步 RL 方法。

因为 Agent 任务具有：

```text
Long Horizon
+
Different Trajectory Length
+
Tool Interaction
+
Environment Feedback
```

不同 Rollout 的执行时间差异很大。

如果全部同步：

```text
短任务做完
   ↓
等待最长任务
   ↓
GPU / Worker 空转
```

异步方式：

```text
Agent A ──完成──→ Training
Agent B ─────完成────→ Training
Agent C ───────────完成────→ Training
```

一句话：

> **异步 Agent RL：谁先跑完谁先进入训练，不必所有 Agent 一起等。**

---

# 第五篇：Long-Horizon Agent

# 十四、GLM-5.1：从 Agent 到 8 小时持续执行

GLM-5.1 的重点不是再次扩大 Context。

其 Context 仍为：

```text
200K
```

真正的重点是：

# Long-Horizon Task

官方定位：

> 单次任务可以持续自主工作最长约 8 小时。

能力从：

```text
Prompt
  ↓
Answer
```

变成：

```text
Goal
 ↓
Plan
 ↓
Execute
 ↓
Test
 ↓
Analyze
 ↓
Fix
 ↓
Optimize
 ↓
Repeat
 ↓
Deliver
```

一句话：

> **GLM-5.1：衡量 Agent 的标准开始从“单轮多聪明”变成“能稳定工作多久”。**

---

# 十五、GLM-5.2：Solid 1M Context

2026 年 6 月，GLM-5.2 把 Context 从：

```text
200K
  ↓
1M
```

但官方特别强调：

> 重点不是“能够输入 1M”，而是 **Solid 1M Context**。

也就是：

```text
1M Input
   +
Long-Horizon Training
   +
Coding-Agent Trajectory
   +
Stable Execution
```

一句话：

> **不是窗口标称 1M，而是让 1M 真正能支撑长时程 Agent 工作。**

---

# 十六、IndexShare：GLM-5.2 的关键长上下文创新

GLM-5 使用 DSA：

```text
Layer 1 → Indexer → Top-K
Layer 2 → Indexer → Top-K
Layer 3 → Indexer → Top-K
Layer 4 → Indexer → Top-K
```

问题：

> 每层都运行 Indexer，本身也有计算成本。

GLM-5.2 提出：

# IndexShare

```text
Layer 1
  ↓
Indexer
  ↓
Top-K Indices
  │
  ├────→ Layer 1
  ├────→ Layer 2
  ├────→ Layer 3
  └────→ Layer 4
```

即：

> **每 4 个 Sparse Attention Layers 共用一个 Indexer。**

官方报告：

> 在 1M Context 下，IndexShare 可将相关 per-token FLOPs 降低约 2.9×。

一句话：

> **DSA 是“挑重要 Token”，IndexShare 是“挑一次，四层一起用”。**

---

# 十七、GLM-5.2：MTP 继续优化

GLM-5.2 还进一步优化：

# MTP

**Multi-Token Prediction**

用于：

```text
Speculative Decoding
```

其优化包括：

```text
IndexShare
+
KVShare
+
Rejection Sampling
+
End-to-End TV Loss
```

并共享不同 MTP Step 的参数。

概念：

```text
Main Model
    ↓
MTP Draft
    ↓
一次提出多个候选 Token
    ↓
Main Model Verify
    ↓
一次接受多个 Token
```

官方实验中，最终方案相对 baseline 的 Acceptance Length 提升约：

```text
20%
```

一句话：

> **MTP：让模型一次“猜”更多 Token，通过验证后批量接受。**

---

# 十八、GLM-5.2：长时程 RL 的变化

超长 Agent Trajectory 带来一个问题：

```text
同一个 Prompt
   ↓
不同 Rollout
   ↓
长度完全不同
   ↓
Compaction 后子轨迹数量也不同
```

因此 GLM-5.2 的长时程训练进一步采用：

```text
Critic-based PPO
+
Single-rollout Optimization
+
Token-level Advantage / Loss
```

这里非常值得注意：

> **GLM-5.2 并不是简单沿用 Group-relative RL。**

在超长 Agent 轨迹场景下，它重新引入 Critic-based PPO，以适配长度不一的单 Rollout 与 Compaction。

一句话：

> **短推理可以组内比较，超长 Agent 更需要对每条轨迹单独估值。**

---

# 十九、GLM-5.2 长上下文技术线

```text
GLM-4
128K / 1M Variant
     │
     ▼
GLM-4.5
128K
     │
     ▼
GLM-4.6 / GLM-5 / GLM-5.1
200K
     │
     ▼
GLM-5
DSA
「少算」
     │
     ▼
GLM-5.2
DSA + IndexShare
「挑一次，多层共享」
     │
     ▼
Solid 1M Context
```

---

# 二十、GLM-5.3：最新路线——只 Scaling Post-training

2026 年 8 月 14 日发布：

# GLM-5.3

官方给出的一个非常重要的信息：

> **GLM-5.3 与 GLM-5.2 使用同一个 Base Model。**

也就是说：

```text
GLM-5.2 Base
     │
     ├─ IndexShare
     ├─ 1M Context
     ├─ Long-Horizon RL Stack
     └─ slime
     │
     ▼
继续扩大 Post-training
     │
     ├─ More Environments
     ├─ More Diverse Tasks
     └─ More RL Compute
     │
     ▼
GLM-5.3
```

所以 GLM-5.3 的核心不是：

```text
New Attention
New MoE
New Base Architecture
```

而是：

# Scaling Post-training

一句话：

> **GLM-5.3：底座不变，把环境、任务和 RL Compute 继续做大。**

这很重要，因为它说明 Frontier Model 的 Scaling 已经从：

```text
Pre-training Scaling
参数 / 数据 / 算力
```

进一步扩展到：

```text
Post-training Scaling
环境 / 任务 / Rollout / RL Compute
```

---

# 第六篇：GLM 技术主线拆解

# 二十一、Attention / 长上下文技术线

建议这样理解：

```text
GLM / ChatGLM
短上下文
    ↓
ChatGLM2 / 3
Long Context
    ↓
GLM-4
128K / 1M
    ↓
GLM-4.6
200K
    ↓
GLM-5
DSA
    │
    │ 挑重要 Token
    ▼
GLM-5.2
DSA + IndexShare
    │
    │ 多层共享 Index
    ▼
Solid 1M Context
```

最容易记忆：

```text
DSA
挑重要 Token

↓

IndexShare
挑一次，多层一起用
```

---

# 二十二、MoE / Model Scaling 技术线

```text
GLM-130B
Dense 130B
    ↓
GLM-4.x
Scaling Foundation Model
    ↓
GLM-4.5
355B Total
32B Active
    ↓
GLM-5
744B Total
40B Active
```

核心变化：

> **总模型容量接近翻倍，但激活参数增长远小于总参数增长。**

因此：

```text
Model Capacity ↑↑
       +
Per-token Compute 可控
```

一句话：

> **MoE：模型知识容量继续扩展，但每个 Token 不必计算全部参数。**

---

# 二十三、Training Scaling 技术线

```text
GLM-130B
Training Stability
      ↓
GLM-4
10T Tokens
      ↓
GLM-4.5
23T Tokens
      ↓
GLM-5
28.5T Tokens
      ↓
GLM-5.3
Post-training Scaling
```

可以看到 Scaling 的重点发生变化：

```text
早期：

Parameter Scaling
+
Data Scaling

↓

现在：

Pre-training Scaling
+
Post-training Scaling
+
Environment Scaling
+
RL Compute Scaling
```

---

# 二十四、Reasoning / RL 技术线

```text
GLM-4
SFT + Human Feedback
      ↓
GLM-4.5
Hybrid Reasoning
+
Multi-stage RL
      ↓
GLM-5
slime
+
Asynchronous Agent RL
      ↓
GLM-5.2
Long-Horizon RL
+
Critic-based PPO
      ↓
GLM-5.3
Scaling Post-training
```

一句话：

> **GLM 的 RL 路线从“让回答更好”逐渐转向“让 Agent 在复杂环境中长期工作”。**

---

# 二十五、Agent 技术线

```text
ChatGLM
会聊天
   ↓
ChatGLM3
会 Function Call
   ↓
GLM-4 All Tools
会自主选择工具
   ↓
GLM-4.5
Agentic Foundation Model
   ↓
GLM-5
Agentic Engineering
   ↓
GLM-5.1
8h Long-Horizon Execution
   ↓
GLM-5.2
1M Context Long-Horizon Agent
   ↓
GLM-5.3
Scaling Agent Post-training
```

这条线非常清晰：

> **Chat → Tool → Agent → Engineering Agent → Long-Horizon Agent**

---

# 第七篇：多模态技术线

# 二十六、CogVLM：Visual Expert

## 26.1 论文

**CogVLM: Visual Expert for Pretrained Language Models**

https://arxiv.org/abs/2311.03079

CogVLM 的关键思想：

# Visual Expert

传统：

```text
Vision Encoder
    ↓
Projection
    ↓
LLM
```

CogVLM：

```text
Vision Encoder
     ↓
LLM Layers
     │
     ├─ Language Path
     └─ Visual Expert
```

即在：

```text
Attention
+
FFN
```

内部加入可训练的视觉专家。

一句话：

> **CogVLM：不是只在入口把图片映射成 Token，而是在 LLM 内部加入视觉专家。**

---

# 二十七、GLM-4V：多模态进入 GLM 主模型家族

GLM-4V 将：

```text
Image
+
Text
```

纳入 GLM-4 系列。

这标志着多模态不再只是 CogVLM 独立路线，而开始进入：

> **GLM 主模型体系。**

---

# 二十八、GLM-4.1V-Thinking：多模态也开始 Reasoning

## 28.1 论文

**GLM-4.1V-Thinking and GLM-4.5V: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning**

https://arxiv.org/abs/2507.01006

核心变化：

```text
Multimodal Understanding
        ↓
Multimodal Reasoning
        ↓
Scalable Reinforcement Learning
```

模型不再只是：

```text
看图
 ↓
回答
```

而是：

```text
看图
 ↓
Reasoning
 ↓
Verification
 ↓
Answer / Action
```

一句话：

> **GLM-4.1V-Thinking：把 RL Reasoning 扩展到视觉任务。**

---

# 二十九、GLM-4.5V → GLM-5V

多模态继续向：

```text
Image
Video
Document
GUI
Coding
Tool Use
```

扩展。

到 GLM-5V 系列，视觉能力进一步与：

```text
Agent
+
Coding
+
GUI Interaction
+
Skills
```

结合。

因此多模态路线可以概括为：

```text
CogVLM
Visual Expert
   ↓
GLM-4V
Multimodal GLM
   ↓
GLM-4.1V-Thinking
Multimodal Reasoning
   ↓
GLM-4.5V
Versatile Multimodal
   ↓
GLM-5V
Visual Agent
```

---

# 三十、CogVideoX：生成式多模态分支

## 30.1 技术报告

**CogVideoX: Text-to-Video Diffusion Models with an Expert Transformer**

https://arxiv.org/abs/2408.06072

CogVideoX 属于：

> **Multimodal Generation**

而不是 GLM-V 的理解路线。

核心：

```text
Text
 ↓
Expert Transformer
 ↓
Diffusion Transformer
 ↓
3D VAE
 ↓
Video
```

关键技术：

```text
3D VAE
+
Expert Transformer
+
Progressive Training
+
Text-Video Data Pipeline
```

因此 GLM 多模态最好拆成两条：

```text
                 GLM Multimodal
                       │
          ┌────────────┴────────────┐
          │                         │
   Understanding / Agent        Generation
          │                         │
       CogVLM                  CogVideoX
          ↓
       GLM-V
          ↓
  Multimodal Reasoning
          ↓
     Visual Agent
```

---

# 第八篇：GLM-5.2 / 5.3 最新技术全景

# 三十一、GLM-5.2 的三层优化

GLM-5.2 最适合从三层理解：

| 层次 | 技术 | 解决的问题 |
| --- | --- | --- |
| **Architecture** | DSA + IndexShare | 1M Context Attention 成本 |
| **Inference** | MTP + IndexShare + KVShare | Decode 加速 |
| **Post-training** | Long-Horizon RL + Critic PPO | 超长 Agent Trajectory |

整体：

```text
                    GLM-5.2
                       │
          ┌────────────┼────────────┐
          │            │            │
    Architecture    Inference       RL
          │            │            │
      IndexShare       MTP      Long-Horizon
       for DSA       Improved        PPO
          │            │            │
          └────────────┼────────────┘
                       ▼
                  Solid 1M
                       +
               Long-Horizon Agent
```

---

# 三十二、GLM-5.3 为什么值得单独讲？

因为它代表一种新的 Scaling 思路。

过去：

```text
GPT-3 / GLM-130B
Parameter Scaling
```

后来：

```text
GLM-4 / GLM-4.5 / GLM-5
Parameter
+
Data
+
Architecture
```

GLM-5.3：

```text
Same Base Model
      ↓
More Environments
      +
More Diverse Tasks
      +
More RL Compute
      ↓
Better Coding / Agent
```

因此：

> **GLM-5.3 把“Post-training Scaling”从辅助阶段提升成 Frontier Capability 的主要增长来源之一。**

---

# 第九篇：完整技术树

# 三十三、GLM 完整技术树

```text
                                  GLM
                                   │
                     GLM Pretraining · 2021
                                   │
                     Autoregressive Blank Infilling
                                   │
                                   ▼
                              GLM-130B
                                   │
                         130B Bilingual LLM
                                   │
                                   ▼
                              ChatGLM
                                   │
                     Instruction / Dialogue
                                   │
                                   ▼
                      ChatGLM2 → ChatGLM3
                                   │
                        Long Context + Tools
                                   │
                                   ▼
                                GLM-4
                                   │
                      128K / 1M + All Tools
                                   │
                                   ▼
                               GLM-4.5
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                MoE            Reasoning           Agent
                 │                 │                 │
           355B / 32B          Hybrid Mode        ARC Model
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   ▼
                                GLM-5
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                DSA              slime          Async Agent RL
                 │                 │                 │
              少算             RL Infra          长时程交互
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   ▼
                              GLM-5.1
                                   │
                          8h Long-Horizon
                                   │
                                   ▼
                              GLM-5.2
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
           IndexShare             MTP          Long-Horizon PPO
                │                  │                  │
          DSA 多层共享        Spec Decode       Agent Training
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                              Solid 1M
                                   │
                                   ▼
                              GLM-5.3
                                   │
                         Same Base Model
                                   │
                         Scaling Post-training
                                   │
                    More Environments / Tasks /
                             RL Compute
                                   │
                                   ▼
                    Frontier Coding + Agent
```

---

# 三十四、按能力重新总结

| 能力 | GLM 技术 | 一句话 |
| --- | --- | --- |
| **统一预训练** | GLM | 自回归填空 |
| **做得大** | GLM-130B → MoE | 从 130B Dense 到 744B MoE |
| **长上下文** | GLM-4 → GLM-5.2 | 128K / 1M → Solid 1M |
| **算得快** | DSA | 挑重要 Token 看 |
| **进一步少算** | IndexShare | 一次索引，多层共享 |
| **吐得快** | MTP | 多 Token Speculative Decoding |
| **会推理** | GLM-4.5 Hybrid Reasoning | Thinking / Direct |
| **会用工具** | GLM-4 All Tools | 自主选择工具 |
| **会做工程** | GLM-5 | Agentic Engineering |
| **能持续工作** | GLM-5.1 | 8 小时 Long-Horizon Agent |
| **能处理超长轨迹** | GLM-5.2 | 1M + Long-Horizon PPO |
| **Post-training 扩展** | GLM-5.3 | 环境 + 任务 + RL Compute Scaling |
| **看得懂图** | CogVLM / GLM-V | Visual Expert |
| **视觉也会推理** | GLM-4.1V-Thinking | Multimodal RL |
| **生成视频** | CogVideoX | 3D VAE + Expert DiT |

---

# 三十五、关键技术一句话总结

## GLM

> **把填空理解任务和自回归生成统一起来。**

## GLM-130B

> **把 GLM 扩展到 130B 双语大模型，并解决超大规模训练稳定性。**

## ChatGLM

> **把 GLM 变成真正面向用户的对话模型。**

## GLM-4 All Tools

> **不只是会 Function Call，而是会判断什么时候该用什么工具。**

## GLM-4.5

> **把 Agentic、Reasoning、Coding 统一成 ARC Foundation Model。**

## MoE

> **模型容量做大，但每个 Token 少激活。**

## DSA

> **挑重要 Token 看。**

## slime

> **让 RL 的生成和训练异步流水起来。**

## GLM-5

> **从 Vibe Coding 走向 Agentic Engineering。**

## GLM-5.1

> **Agent 的能力不只看单轮分数，还看能不能连续稳定工作 8 小时。**

## IndexShare

> **DSA 挑一次重要 Token，让连续多层一起复用。**

## MTP

> **一次提出多个 Token，通过验证后批量接受。**

## GLM-5.2

> **DSA + IndexShare + MTP + Long-Horizon RL，把 1M Context 变成可工作的 Agent 基础。**

## GLM-5.3

> **底座不变，继续扩大环境、任务和 RL Compute，把能力增长转向 Post-training Scaling。**

## CogVLM

> **在 LLM 内部加入视觉专家，而不是只在入口做视觉映射。**

## GLM-V

> **从多模态理解进一步走向多模态 Reasoning 与 Visual Agent。**

---

# 第十篇：论文 / 技术报告索引

# 三十六、主模型 / 基础架构

| 时间 | 论文 / 报告 | 核心技术 |
| --- | --- | --- |
| 2021.03 | [GLM](https://arxiv.org/abs/2103.10360) | Autoregressive Blank Infilling |
| 2022.10 | [GLM-130B](https://arxiv.org/abs/2210.02414) | 130B、Bilingual、Training Stability |
| 2024.06 | [ChatGLM Family / GLM-4](https://arxiv.org/abs/2406.12793) | ChatGLM → GLM-4、All Tools、Long Context |
| 2025.08 | [GLM-4.5](https://arxiv.org/abs/2508.06471) | ARC、MoE、Hybrid Reasoning |
| 2026.02 | [GLM-5](https://arxiv.org/abs/2602.15763) | DSA、slime、Async Agent RL |

---

# 三十七、2026 最新主模型发布

| 时间 | 模型 | 核心变化 | 文献类型 |
| --- | --- | --- | --- |
| 2026.02 | **GLM-5** | 744B / 40B、DSA、Agentic Engineering | Technical Report |
| 2026.04 | **GLM-5.1** | 8h Long-Horizon Agent | 官方技术发布 |
| 2026.06 | **GLM-5.2** | 1M、IndexShare、Improved MTP、Long-Horizon PPO | 官方技术发布 |
| 2026.08 | **GLM-5.3** | Same Base + Scaling Post-training | 官方技术发布 |

官方发布：

- GLM-5: https://z.ai/blog/glm-5
- GLM-5.1: https://docs.z.ai/guides/llm/glm-5.1
- GLM-5.2: https://z.ai/blog/glm-5.2
- GLM-5.3: https://z.ai/blog/glm-5.3

---

# 三十八、多模态论文

| 时间 | 论文 / 模型 | 核心技术 |
| --- | --- | --- |
| 2023.11 | [CogVLM](https://arxiv.org/abs/2311.03079) | Visual Expert |
| 2024.08 | [CogVideoX](https://arxiv.org/abs/2408.06072) | 3D VAE + Expert Transformer |
| 2025.07 | [GLM-4.1V-Thinking / GLM-4.5V](https://arxiv.org/abs/2507.01006) | Multimodal Reasoning + Scalable RL |
| 2026 | **GLM-5V Series** | Visual Coding + GUI / Agent |

---

# 三十九、课程推荐：论文分三级

## A 级：主干必讲

1. **GLM**
2. **GLM-130B**
3. **ChatGLM Family / GLM-4**
4. **GLM-4.5**
5. **GLM-5**
6. **GLM-5.2 官方技术报告 / Blog**
7. **GLM-5.3 官方技术发布**

核心路线：

```text
GLM
 ↓
GLM-130B
 ↓
ChatGLM
 ↓
GLM-4
 ↓
GLM-4.5
 ↓
GLM-5
 ↓
GLM-5.2
 ↓
GLM-5.3
```

---

## B 级：多模态专题

1. **CogVLM**
2. **CogVideoX**
3. **GLM-4.1V-Thinking / GLM-4.5V**
4. **GLM-5V**

---

## C 级：Agent / Infra 专题

建议重点补充：

```text
GLM-4 All Tools
+
slime
+
Asynchronous Agent RL
+
IndexShare
+
MTP
+
Long-Horizon PPO
+
1M Context Serving
```

---

# 四十、GLM 与 DeepSeek / Kimi 的长上下文路线对照

这三家到 2026 年已经形成非常有意思的不同技术路径：

| 厂商 / 模型 | 核心路线 | 主要思想 |
| --- | --- | --- |
| **DeepSeek-V4** | CSA + HCA | 先压缩序列，再 Sparse / Dense Hybrid |
| **Kimi K3** | KDA + Gated MLA | Recurrent State + 少量 Global Attention |
| **GLM-5.2** | DSA + IndexShare | Sparse Attention + 多层共享 Index |

一句话：

```text
DeepSeek
先压缩，再决定怎么看

Kimi
大部分历史写进状态，需要时全局找

GLM
挑重要 Token，而且连续多层共享一次挑选结果
```

三条路线最终都在解决：

```text
1M Context
     │
     ├─ KV Cache
     ├─ Attention FLOPs
     ├─ Decode Speed
     ├─ Training Cost
     └─ Long-Horizon Agent
```

---

# 四十一、最终总结

GLM 的技术演进可以浓缩成六个阶段。

## 第一阶段：统一预训练

```text
GLM
 ↓
Autoregressive Blank Infilling
```

解决：

> **理解与生成能不能用一个统一预训练框架。**

---

## 第二阶段：把模型做大

```text
GLM-130B
 ↓
130B Bilingual
+
Training Stability
```

解决：

> **百亿 / 千亿模型怎么稳定训练。**

---

## 第三阶段：从模型到 Chat + Tool

```text
ChatGLM
   ↓
ChatGLM2
   ↓
ChatGLM3
   ↓
GLM-4 All Tools
```

解决：

> **从会语言，走向会对话、会调用工具。**

---

## 第四阶段：ARC

```text
GLM-4.5
   │
   ├─ Agentic
   ├─ Reasoning
   └─ Coding
```

解决：

> **把 Agent、Reasoning、Coding 统一进一个 Foundation Model。**

---

## 第五阶段：Agentic Engineering

```text
GLM-5
   │
   ├─ 744B / 40B MoE
   ├─ DSA
   ├─ slime
   └─ Async Agent RL
```

解决：

> **从生成代码升级到长期完成复杂工程任务。**

---

## 第六阶段：1M + Long-Horizon + Post-training Scaling

```text
GLM-5.1
8h Agent
    ↓
GLM-5.2
1M Context
+
IndexShare
+
Improved MTP
+
Long-Horizon PPO
    ↓
GLM-5.3
Same Base
+
More Environments
+
More Tasks
+
More RL Compute
```

解决：

> **让 Agent 不仅聪明，而且能在超长上下文和复杂环境里持续稳定工作。**

最终可以用一句话概括：

> **GLM 从 2021 年用 Autoregressive Blank Infilling 统一语言理解与生成开始，经 GLM-130B 解决超大双语模型训练稳定性，再通过 ChatGLM 与 GLM-4 完成从 Chat 到 All Tools 的能力升级；GLM-4.5 用 MoE 与多阶段训练把 Agentic、Reasoning、Coding 统一成 ARC；GLM-5 进一步引入 DSA、slime 与异步 Agent RL，从 Vibe Coding 走向 Agentic Engineering；GLM-5.2 再通过 DSA + IndexShare、改进 MTP 和长时程 RL 把上下文扩展到可实际工作的 1M；最新 GLM-5.3 则保持相同 Base Model，继续扩大环境、任务和 RL Compute，表明 Frontier Model 的 Scaling 正从 Pre-training Scaling 进一步进入 Post-training Scaling。**
