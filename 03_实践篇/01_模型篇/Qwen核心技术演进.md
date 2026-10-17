# Qwen 核心技术演进

> 从 Qwen、Qwen1.5、Qwen2、Qwen2.5、Qwen3、Qwen3-Next，到 2026 年 Qwen3.5，以及 Coder / VL / Omni / Agent 专项路线

---

# 第一篇：主模型与技术全景

## 一、先看全景：Qwen 到底在解决什么问题？

Qwen 的特点与 DeepSeek、Kimi、GLM 有些不同：

> **Qwen 从一开始就是“通用基座 + 专项模型 + 多模态 + Agent 工具链”并行发展的模型家族。**

因此不能简单画成：

```text
Qwen → Qwen2 → Qwen3 → Qwen3.5
```

更准确的是：

```text
                           Qwen Family
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
    General LLM             Specialized             Multimodal
        │                       │                       │
 Qwen → Qwen2              Math / Coder           VL / Audio
        │                       │                       │
     Qwen2.5                   QwQ                  Qwen2.5-VL
        │                       │                       │
      Qwen3                Qwen3-Coder            Qwen2.5-Omni
        │                                               │
   Qwen3-Next                                      Qwen3-VL
        │                                               │
      Qwen3.5 ◀─────────────────────────────────────────┘
        │
 Native Multimodal Agent
        │
   Qwen Code / CUA
```

---

## 二、Qwen 核心问题地图

| 核心问题 | Qwen 技术 / 模型 | 一句话理解 |
| --- | --- | --- |
| **通用模型怎么做强？** | Qwen → Qwen2 → Qwen2.5 | 数据、模型规模、训练配方持续 Scaling |
| **KV Cache 怎么降？** | Qwen2 GQA | 多个 Q Head 共享 KV Head |
| **长上下文怎么扩？** | Qwen2.5-Turbo → Qwen3-Next → Qwen3.5 | 1M、Hybrid Attention、Linear Attention |
| **模型怎么做大又省计算？** | Qwen1.5-MoE → Qwen3 MoE → Qwen3-Next | 越来越稀疏的 MoE |
| **Reasoning 怎么统一？** | QwQ → Qwen3 | Thinking + Non-thinking Unified |
| **推理预算怎么控制？** | Qwen3 | Thinking Budget |
| **Attention 怎么进一步少算？** | Qwen3-Next / Qwen3.5 | Gated DeltaNet + Gated Attention Hybrid |
| **生成怎么更快？** | Qwen3-Next | Multi-Token Prediction |
| **多模态怎么统一？** | Qwen-VL → Qwen2.5-Omni → Qwen3.5 | Vision → Audio/Video → Native Multimodal |
| **视觉怎么保留原始分辨率？** | Qwen2-VL / Qwen2.5-VL | Naive Dynamic Resolution |
| **视频时间怎么建模？** | MRoPE / TMRoPE | 统一空间与时间位置编码 |
| **代码怎么走向 Agent？** | Qwen3-Coder | Agentic Coding |
| **怎么操作电脑？** | Qwen-CUA | Screenshot → Mouse / Keyboard Native Computer Use |
| **怎么形成 Agent 工具链？** | Qwen Code | Skills、Sub-agent、Agent Team、Review |

---

# 第二篇：通用语言模型主线

# 三、Qwen：模型家族起点

## 3.1 技术报告

**Qwen Technical Report**

https://arxiv.org/abs/2309.16609

Qwen 第一代已经形成：

```text
Base Model
   │
   ├─ Qwen
   └─ Qwen-Chat
```

其中：

```text
Qwen
Pre-training
Next Token Prediction

Qwen-Chat
SFT
+
RLHF
```

同时开始出现专项模型：

```text
Code-Qwen
Math-Qwen
Qwen-VL
Qwen-Audio
```

因此 Qwen 很早就不是“一个模型”，而是：

> **Foundation Model Family。**

---

# 四、Qwen1.5：工程生态与 MoE 开始成熟

Qwen1.5 于 2024 年初发布。

模型覆盖：

```text
0.5B
1.8B
4B
7B
14B
32B
72B
110B
+
MoE
```

这一代的重要意义之一是：

> **模型代码正式进入 Hugging Face Transformers 主线，不再依赖 trust_remote_code。**

同时提供：

```text
GPTQ
AWQ
GGUF
```

等量化版本。

一句话：

> **Qwen1.5：模型能力继续扩展，同时把部署和开发体验做成成熟开源生态。**

---

# 五、Qwen2：GQA + 更强多语言

## 5.1 技术报告

**Qwen2 Technical Report**

https://arxiv.org/abs/2407.10671

Qwen2 模型规模：

```text
0.5B → 72B
Dense
+
MoE
```

支持约：

```text
30 Languages
```

---

## 5.2 GQA

Qwen2 一个值得单独讲的架构变化是：

# GQA

**Grouped Query Attention**

传统 MHA：

```text
Q1 → K1 V1
Q2 → K2 V2
Q3 → K3 V3
...
```

GQA：

```text
Q1 ─┐
Q2 ─┼→ K1 V1

Q3 ─┐
Q4 ─┼→ K2 V2
```

即：

> **多个 Query Head 共用一组 KV Head。**

作用：

```text
KV Heads ↓
   ↓
KV Cache ↓
   ↓
Memory Bandwidth ↓
   ↓
Decode Efficiency ↑
```

一句话：

> **GQA：少存 KV，但保留多 Query Head 的表达能力。**

---

# 六、Qwen2.5：从 7T 扩到 18T Tokens

## 6.1 技术报告

**Qwen2.5 Technical Report**

https://arxiv.org/abs/2412.15115

Qwen2.5 的核心不是一次激进的 Attention 架构重构。

而是：

# Data + Post-training Scaling

预训练数据：

```text
Qwen2
约 7T Tokens
    ↓
Qwen2.5
约 18T Tokens
```

Post-training：

```text
> 1M SFT Samples
+
Multi-stage RL
```

重点提升：

```text
Knowledge
Reasoning
Math
Coding
Instruction Following
Long-form Generation
Structured Data
```

一句话：

> **Qwen2.5：先把传统 Transformer 路线的数据和后训练做到很强。**

---

# 七、Qwen2.5-Turbo：1M Context 探索

Qwen2.5-Turbo 将上下文扩展到：

# 1M Tokens

这一阶段说明 Qwen 已经开始进入 Million-token Context。

但官方也明确指出：

> “能输入 1M”并不意味着所有真实长序列任务都已经解决。

仍然存在：

```text
Long-context Stability
+
Inference Cost
+
Long-sequence Alignment
```

等问题。

这也为后续：

```text
Qwen3-Next
   ↓
Qwen3.5
```

重新设计 Attention Architecture 埋下伏笔。

---

# 第三篇：Reasoning 演进

# 八、QwQ：专门的 Reasoning Model

QwQ 是 Qwen 的推理模型分支。

代表模型：

# QwQ-32B

官方技术文章：

**QwQ-32B: Embracing the Power of Reinforcement Learning**

https://qwenlm.github.io/blog/qwq-32b/

核心思想：

```text
Base Model
    ↓
Reinforcement Learning
    ↓
Long Reasoning
    ↓
Math / Coding / Planning
```

QwQ 的意义是：

> **Qwen 开始把 Test-time Reasoning 与 RL 单独作为核心能力扩展。**

但此时：

```text
普通 Chat Model
和
Reasoning Model
```

仍然是相对分离的。

---

# 九、Qwen3：Thinking 与 Non-thinking 正式统一

## 9.1 技术报告

**Qwen3 Technical Report**

https://arxiv.org/abs/2505.09388

Qwen3 最大的能力创新之一：

# Hybrid Thinking

一个模型同时支持：

```text
Thinking Mode
+
Non-thinking Mode
```

传统：

```text
Chat Model
负责快速回答

Reasoning Model
负责深度思考
```

Qwen3：

```text
                    Qwen3
                      │
            ┌─────────┴─────────┐
            │                   │
        Thinking            Non-thinking
            │                   │
      Complex Task           Simple Task
```

一句话：

> **Qwen3：不再需要在 Chat Model 和 Reasoning Model 之间切换。**

---

# 十、Thinking Budget

Qwen3 进一步提出：

# Thinking Budget

即：

> **用户可以控制模型愿意花多少推理计算。**

概念上：

```text
Simple Task
   ↓
Small Thinking Budget
   ↓
Fast Response

Complex Task
   ↓
Large Thinking Budget
   ↓
Deep Reasoning
```

这意味着推理能力开始从：

```text
Think / Don't Think
```

变成：

```text
How Much to Think
```

一句话：

> **Thinking Budget：把推理计算本身变成可调资源。**

---

# 十一、Qwen3 的 Pre-training Scaling

Qwen3 数据进一步扩大：

```text
Qwen2
约 7T

↓

Qwen2.5
约 18T

↓

Qwen3
约 36T
```

语言 / 方言：

```text
Qwen2.5
约 29

↓

Qwen3
119
```

Qwen3 的 Pre-training 大致分为：

```text
Stage 1
General Pre-training
>30T Tokens
4K Context

↓

Stage 2
Knowledge-intensive
STEM / Coding / Reasoning
约 5T

↓

Stage 3
Long-context
32K
```

一句话：

> **Qwen3：数据量继续翻倍，同时提高 STEM、Coding、Reasoning 数据比例。**

---

# 十二、Qwen3：Dense + MoE 双路线

Qwen3 同时提供：

```text
Dense Models
+
MoE Models
```

典型：

| 模型 | 总参数 | 激活参数 | 架构 |
| --- | ---: | ---: | --- |
| Qwen3-32B | 32B | 32B | Dense |
| Qwen3-30B-A3B | 30B | 3B | MoE |
| Qwen3-235B-A22B | 235B | 22B | MoE |

MoE：

```text
Token
  ↓
Router
  ↓
128 Experts
  ↓
Activate 8
```

一句话：

> **Qwen3：用 MoE 把模型容量与每 Token 计算量解耦。**

---

# 第四篇：Qwen3-Next——架构真正开始重构

# 十三、Qwen3-Next：Towards Ultimate Training & Inference Efficiency

官方技术文章：

**Qwen3-Next: Towards Ultimate Training & Inference Efficiency**

https://qwen.ai/blog?id=qwen3-next

Qwen3-Next 是理解 Qwen3.5 最关键的架构前置。

它主要引入：

```text
Hybrid Attention
+
Ultra-Sparse MoE
+
Training Stability Designs
+
MTP
```

代表模型：

```text
Qwen3-Next-80B-A3B
```

即：

```text
80B Total
3B Active
```

---

# 十四、Hybrid Attention：Linear Attention + Standard Attention

Qwen3-Next 不再让所有层都使用传统 Attention。

而是引入：

# Gated DeltaNet

属于 Linear / Recurrent Attention 路线。

概念：

```text
Token 1
   ↓
State
   ↓
Token 2
   ↓
Update State
   ↓
Token 3
   ↓
Update State
```

历史信息被写入固定状态，而不是所有层都持续保存完整 KV。

但纯 Linear Attention 存在：

> **精确访问很久以前具体 Token 的能力有限。**

所以 Qwen3-Next 采用 Hybrid：

```text
Gated DeltaNet
Gated DeltaNet
Gated DeltaNet
Gated Attention
Gated DeltaNet
...
```

一句话：

> **大部分层高效“记”，少量传统 Attention 层负责精确“找”。**

---

# 十五、Ultra-Sparse MoE

Qwen3：

```text
128 Experts
Activate 8
```

Qwen3-Next：

```text
512 Experts
10 Routed
+
1 Shared
```

代表模型：

```text
80B Total
3B Active
```

激活比例约：

```text
3.7%
```

所以：

> **Qwen3-Next 把 MoE 做得更稀疏。**

一句话：

> **专家更多，但每个 Token 仍然只用很少专家。**

---

# 十六、Training Stability

高稀疏 MoE + Linear Attention 会带来新的训练稳定性问题。

Qwen3-Next 引入：

```text
Attention Output Gating
+
Zero-Centered RMSNorm
+
Router Initialization Normalization
```

用于缓解：

```text
Attention Sink
Massive Activation
Norm Weight Growth
Router Bias
```

一句话：

> **Qwen3-Next：架构更激进，所以同时把稳定性设计直接写进架构。**

---

# 十七、MTP：Multi-Token Prediction

Qwen3-Next 引入：

# Multi-Token Prediction

传统：

```text
Token t
  ↓
Predict t+1
```

MTP：

```text
Token t
  ↓
Predict
t+1
t+2
t+3
...
```

作用：

```text
Training Signal ↑
+
Speculative Decoding
+
Decode Speed ↑
```

一句话：

> **MTP：训练时预测更多未来 Token，推理时还能作为 Speculative Decoding 的 Draft。**

---

# 十八、Qwen3-Next 的效率意义

官方实验中：

```text
Qwen3-Next-80B-A3B
```

只激活约 3B 参数。

相比 Qwen3-32B：

```text
4K Context
Prefill ~7× throughput

>32K
Prefill / Decode
>10× throughput
```

并且训练成本显著降低。

所以：

> **Qwen3-Next 是 Qwen 从“传统 Transformer Scaling”转向“Architecture Efficiency Scaling”的关键节点。**

---

---

# 第五篇：Qwen3.5 → Qwen3.8：Hybrid Architecture 成为主干

# 十九、Qwen3.5：Qwen3-Next 架构正式进入主模型

Qwen3-Next 的角色非常关键：

```text
Qwen3
传统 Transformer / GQA + MoE
        ↓
Qwen3-Next
架构实验与验证
        ↓
Qwen3.5
Hybrid Architecture 正式进入主模型系列
```

Qwen 官方在后续 Qwen3.8-Flash-Next 发布说明中明确回顾：

> Qwen3-Next 引入的 **Gated DeltaNet + Gated Attention** Hybrid Design，随后被用于 Qwen3.5、Qwen3.6、Qwen3.7 和 Qwen3.8 系列。

因此，理解 2026 年 Qwen 的核心，不应只看模型编号，而应该看这条架构主线：

```text
GQA
 ↓
Gated DeltaNet
+
Gated Attention
 ↓
Hybrid Attention
 ↓
Qwen3.5 / 3.6 / 3.7 / 3.8
```

一句话：

> **Qwen3-Next 是架构试验场，Qwen3.5 之后是这套 Hybrid Architecture 的规模化落地。**

---

# 二十、Qwen3.6：Agentic Coding 与多模态继续增强

Qwen3.6 延续 Qwen3.5 的 Hybrid Architecture，并继续强化：

```text
Coding
+
Agent
+
Multimodal Reasoning
```

代表开放模型包括：

```text
Qwen3.6-35B-A3B
Qwen3.6-27B
```

其中 Qwen3.6-27B 是 Dense 27B 多模态模型。

这一阶段非常值得注意：

> **模型演进已经不只是继续增加参数，而是在不同参数规模上强化 Agentic Coding。**

所以 Qwen3.6 更适合放在：

```text
Architecture 延续
        +
Post-training / Agent Capability Scaling
```

这条线上理解。

---

# 二十一、Qwen3.7：承接 Hybrid Architecture

Qwen 官方在 Qwen3.8-Flash-Next 的架构说明中明确把：

```text
Qwen3.5
Qwen3.6
Qwen3.7
Qwen3.8
```

归入 Qwen3-Next 所引入的：

```text
Gated DeltaNet
+
Gated Attention
```

Hybrid Design 的后续模型系列。

因此 Qwen3.7 在这份“核心算法演进”文档中不必人为制造一个新的 Attention 世代。

更合适的定位是：

> **Qwen3.5 → 3.8 属于同一代 Hybrid Architecture 的持续 Scaling 与能力增强。**

---

# 二十二、Qwen3.8：2026 年最新主模型世代

到 Qwen3.8，Qwen 已经形成多个规模与定位的模型。

公开信息中包括：

```text
Qwen3.8-Max
2.4T-scale flagship

Qwen3.8-27B
Dense model

Qwen3.8-Flash-Next
New Architecture Preview
```

这里需要特别区分：

```text
Qwen3.8
= 当前模型世代

Qwen3.8-Flash-Next
= 新架构试验模型
  同时预览 Qwen4 Architecture
```

因此不能写成：

```text
Qwen3.8
 ↓
Qwen4 已发布
```

更准确的是：

```text
Qwen3.8
   │
   └──────────────┐
                  ▼
        Qwen3.8-Flash-Next
                  │
          Architecture Preview
                  │
                  ▼
               Qwen4
             （未来主模型）
```

---

# 第六篇：Qwen3.8-Flash-Next——Qwen4 架构预览

# 二十三、为什么 Qwen3.8-Flash-Next 特别重要？

发布时间：

```text
2026-08-26
```

官方定位：

> **Qwen3.8-Flash-Next 是一个 Multimodal MoE Model，同时也是 Qwen4 所使用架构的 Early Preview。**

它与上一代的关系非常像：

```text
Qwen3-Next
    ↓
预览 Qwen3.5 架构

Qwen3.8-Flash-Next
    ↓
预览 Qwen4 架构
```

所以在技术课程中，Qwen3.8-Flash-Next 的重要性甚至高于单纯比较 Qwen3.8 的 Benchmark。

因为它回答的是：

> **下一代 Qwen 的基础架构准备怎么变？**

---

# 二十四、四个核心架构升级

Qwen3.8-Flash-Next 官方把变化总结为四条：

| 维度 | 核心技术 | 主要目标 |
| --- | --- | --- |
| **Attention** | **GDN + QSA** | 长上下文少算，同时保留精确检索 |
| **Residual** | **Gated Residual（GR）** | 加强跨层信息流与训练稳定性 |
| **Embedding** | **N-gram Embedding** | 用低计算成本增加模型容量 |
| **Optimization** | **Muon** | 提升超大模型优化效率与稳定性 |

这四条可以对应成：

```text
Token 之间怎么交流？
→ GDN + QSA

Layer 之间怎么交流？
→ Gated Residual

模型容量怎么继续做大？
→ N-gram Embedding

这么大的模型怎么训？
→ Muon
```

---

# 二十五、Attention：GDN + QSA

这是最新 Qwen 架构最值得讲的一条线。

## 25.1 GDN：压缩历史

GDN：

# Gated DeltaNet

核心思想仍然是：

```text
历史 Token
   ↓
不断更新
   ↓
Compact State
```

而不是每一层都对完整历史做 Dense Attention。

可以理解为：

> **把大量历史信息压缩进一个持续更新的状态。**

优点：

```text
Long Sequence
     ↓
Attention Cost ↓
KV / Memory Pressure ↓
```

但问题也很明显：

> 压缩状态适合“记住整体”，却不一定擅长精确找回某个很久以前的细节。

因此需要第二部分：

# QSA

---

## 25.2 QSA：Qwen Sparse Attention

QSA：

# Qwen Sparse Attention

核心流程：

```text
Long Context
     ↓
Micro-block
     ↓
Compressed Lightweight Indexer
     ↓
Importance Selection
     ↓
Relevant Context
     ↓
Sparse Attention
```

与 Dense Attention：

```text
Query
 ↓
看全部历史 Token
```

相比，QSA：

```text
Query
 ↓
先通过轻量 Indexer 找重点
 ↓
只对重要 Context 做 Attention
```

一句话：

> **QSA：先用便宜的 Indexer 找重要上下文，再把昂贵 Attention 用在真正值得看的地方。**

---

# 二十六、为什么 GDN 和 QSA 要一起用？

两者解决的问题不同。

| 技术 | 主要作用 | 直观理解 |
| --- | --- | --- |
| **GDN** | 压缩历史 | 把过去“记”进 State |
| **QSA** | 精确检索 | 从长历史里“找”重点 |
| **GDN + QSA** | Hybrid Long Context | 既能高效记，又能精确找 |

因此：

```text
                 Long Context
                      │
          ┌───────────┴───────────┐
          │                       │
         GDN                     QSA
          │                       │
   Compress History        Select Context
          │                       │
     高效“记”                 精确“找”
          │                       │
          └───────────┬───────────┘
                      ▼
               Hybrid Attention
```

一句话：

> **GDN 负责“记”，QSA 负责“找”。**

---

# 二十七、QSA 与 DSA 有什么关系？

从思想层面，两者都属于：

```text
Sparse Attention
```

都在解决：

> **长上下文中没有必要让每个 Query 看所有历史 Token。**

但实现不能简单写成“QSA = DSA”。

可以这样区分：

| 技术 | 模型路线 | 选择粒度 / 机制 | 核心目标 |
| --- | --- | --- | --- |
| **DSA** | DeepSeek / GLM 采用路线 | Indexer → Top-K Relevant Tokens | Token Sparse Attention |
| **QSA** | Qwen3.8-Flash-Next | Compressed Indexer → Micro-block Selection | 降低 Attention + Indexing Cost |

一句话：

```text
DSA
挑重要 Token

QSA
压缩索引后，按 Micro-block 挑重要 Context
```

---

# 二十八、Residual：Gated Residual（GR）

传统 Transformer：

```text
x
│
├──────────────┐
│              ▼
│          Attention
│              │
└────── + ◀────┘
       ↓
      x'
```

核心是：

# Residual Connection

但随着模型越来越深：

```text
Layer 1
 ↓
Layer 2
 ↓
...
 ↓
Layer N
```

跨层信息流也成为 Scaling 问题。

Qwen3.8-Flash-Next 引入：

# Gated Residual（GR）

官方描述：

```text
Residual Stream
      ↓
Widen to 4 Branches
      ↓
Dynamic Gate
      ↓
Control Read / Write
```

即：

> **把 Residual Stream 扩展成 4 条分支，并通过数据相关的动态 Gate 控制信息读写。**

作用：

```text
Cross-layer Information Flow ↑
Training Stability ↑
```

一句话：

> **Attention 解决 Token 怎么交流，GR 解决 Layer 之间的信息怎么更好流动。**

---

# 二十九、Embedding：N-gram Embedding

Qwen3.8-Flash-Next 的另一个很有意思的变化：

# N-gram Embedding

传统 Token Embedding：

```text
Token
 ↓
Embedding Table
 ↓
Vector
```

N-gram Embedding：

```text
Local Context
Token_{t-n} ... Token_t
        ↓
N-gram Address
        ↓
Lookup Table
        ↓
Additional Representation
```

它的关键价值不是复杂计算，而是：

> **通过 Lookup Memory 增加模型容量。**

官方给出的模型规模：

```text
Main Model
125B

+

N-gram Embedding
51B

=

Large Capacity
```

但每 Token 激活：

```text
6B Parameters
```

并且 N-gram Embedding 可以：

```text
Offload to Host Memory
        +
Asynchronous Prefetch
        +
Overlap with Model Compute
```

一句话：

> **N-gram Embedding：用“查表”而不是大规模矩阵计算来扩模型容量。**

---

# 三十、Optimization：Muon

Qwen3.8-Flash-Next 使用：

# Muon Optimizer

但这里要注意：

> **Muon 不是 Qwen 原创。**

Qwen 在新架构中对 Muon 的使用重点优化了：

```text
Orthogonalization Accuracy
+
Muon / AdamW Parameter Assignment
+
Fused Parameter Splitting
+
Architecture-specific Scaling Law
```

因此不能简单写：

```text
AdamW
 ↓
Muon
```

更准确是：

```text
Different Parameter Types
        │
        ├─ Muon
        │
        └─ AdamW
```

一句话：

> **Qwen 把 Muon 与 AdamW 分工使用，并针对新架构重新拟合 Scaling Law。**

---

# 三十一、Qwen3.8-Flash-Next 模型规格

| 项目 | Qwen3.8-Flash-Next |
| --- | --- |
| 模型类型 | Multimodal MoE |
| Main Model Parameters | **125B** |
| N-gram Embedding Parameters | **51B** |
| Activated Parameters / Token | **6B** |
| Native Context | **262,144 Tokens** |
| Extended Context | **1,000,000 Tokens with YaRN** |
| Attention | **GDN + QSA** |
| Residual | **Gated Residual** |
| Embedding | **N-gram Embedding** |
| Optimizer | **Muon + AdamW 分工** |
| 下一代意义 | **Qwen4 Architecture Early Preview** |

注意：

> 51B N-gram Embedding 参数通过确定性 Lookup 访问，不进入常规 per-token Matrix Multiplication Budget。

---

# 三十二、训练与推理效率

官方对比 Qwen3.7-Plus：

```text
Qwen3.7-Plus
397B Total
17B Active

vs

Qwen3.8-Flash-Next
125B Main
+ 51B N-gram
6B Active
```

官方报告：

> Qwen3.8-Flash-Next 的训练成本约为 Qwen3.7-Plus 的 **1/9**，同时在 Coding 和 Office Tasks 上表现更强。

这反映 Qwen 新一代 Scaling 思路：

```text
以前：
Parameter Count ↑
Compute ↑

现在：
Architecture Efficiency ↑
Sparse Compute ↑
Lookup Memory ↑
Active Parameters ↓
```

一句话：

> **不再只追求“模型更大”，而是追求“容量更大、激活更少、训练更省”。**

---

# 第七篇：Qwen Attention 完整演进

# 三十三、从 MHA 到 GDN + QSA

```text
Qwen
MHA
 │
 ▼
Qwen2
GQA
 │
 │ 多个 Q 共享 KV
 │ 少存
 ▼
Qwen2.5
GQA + Long Context
 │
 ▼
Qwen3
GQA / MoE
 │
 ▼
Qwen3-Next
Gated DeltaNet
+
Gated Attention
 │
 │ Linear + Dense Hybrid
 ▼
Qwen3.5 / 3.6 / 3.7 / 3.8
Hybrid Architecture
 │
 ▼
Qwen3.8-Flash-Next
GDN
+
QSA
 │
 │ Linear + Sparse Hybrid
 ▼
Qwen4 Architecture Preview
```

核心变化可以压缩成：

```text
MHA
所有头独立 KV

↓

GQA
共享 KV
解决“少存”

↓

GDN
压缩历史进 State
解决“长序列怎么高效记”

↓

Gated Attention
少量 Dense / Precise Attention
解决“怎么精确找”

↓

QSA
Sparse Context Selection
解决“精确找也不要看全部”
```

---

# 三十四、Qwen 长上下文路线

| 阶段 | 核心技术 | 重点 |
| --- | --- | --- |
| Qwen / Qwen1.5 | MHA / Context Extension | 基础长上下文 |
| Qwen2 | GQA | 降 KV Cache |
| Qwen2.5 | Long Context Scaling | 128K / Million-token 探索 |
| Qwen3 | GQA + Better Training | Reasoning + Long Context |
| Qwen3-Next | GDN + Gated Attention | Linear + Dense Hybrid |
| Qwen3.5–3.8 | Hybrid Architecture | 架构规模化 |
| Qwen3.8-Flash-Next | **GDN + QSA** | **Linear + Sparse Hybrid** |
| Qwen4 | **尚未正式发布** | 使用新架构的未来完整模型家族 |

---

# 第八篇：MoE / Capacity Scaling

# 三十五、MoE 路线

```text
Qwen1.5
MoE Exploration
    ↓
Qwen2
Dense + MoE
    ↓
Qwen3
235B-A22B
30B-A3B
    ↓
Qwen3-Next
80B-A3B
Ultra-Sparse MoE
    ↓
Qwen3.5+
Hybrid Attention + Sparse MoE
    ↓
Qwen3.8-Flash-Next
125B Main
6B Active
+
51B N-gram Lookup Capacity
```

这一阶段最大的变化是：

> **模型容量不再只来自 Transformer Parameter。**

开始出现：

```text
Compute Parameters
      +
Sparse Experts
      +
Lookup Memory
```

三种容量来源。

---

# 三十六、Capacity Scaling 新思路

| 路线 | 增加容量方式 | 计算成本 |
| --- | --- | --- |
| Dense | 增加所有参数 | 高 |
| MoE | 增加 Experts，只激活少量 | 中低 |
| N-gram Embedding | 增加 Lookup Table | 很低的额外矩阵计算 |

所以：

```text
Dense Scaling
     ↓
Sparse MoE Scaling
     ↓
MoE + Lookup Memory Scaling
```

可能成为理解 Qwen4 的重要背景。

---

# 第九篇：Depth Scaling

# 三十七、Gated Residual 应该放在哪里？

不要把 GR 放进 Attention 章节后就结束。

它实际属于另一条 Scaling 线：

# Depth Scaling

```text
Sequence Scaling
Token 越来越多
    ↓
GDN + QSA

Model Capacity Scaling
参数越来越多
    ↓
MoE + N-gram Embedding

Depth Scaling
网络越来越深
    ↓
Gated Residual
```

最适合课程记忆的一句话：

> **Attention 解决 Token 怎么交流，Residual 解决 Layer 怎么交流。**

---

# 第十篇：Training Scaling

# 三十八、从 AdamW 到 Muon + AdamW 分工

Qwen 的训练技术不要简单画成：

```text
AdamW → Muon
```

而应该理解成：

```text
Large Model Parameters
        │
        ├─ Suitable Matrices
        │       ↓
        │     Muon
        │
        └─ Other Parameters
                ↓
              AdamW
```

Qwen3.8-Flash-Next 进一步针对：

```text
Orthogonalization
Parameter Assignment
Fused Matrix Splitting
Scaling Law
```

做联合优化。

这体现：

> **Optimizer 也开始与 Architecture Co-design。**

---

# 第十一篇：Reasoning / Multimodal / Agent 主线

# 三十九、Reasoning

```text
Qwen2.5
Strong General Model
    ↓
QwQ
Dedicated RL Reasoning
    ↓
Qwen3
Thinking + Non-thinking
    ↓
Thinking Budget
    ↓
Qwen3.5+
Multimodal Thinking
    ↓
Qwen3.8
Agentic Reasoning
```

---

# 四十、多模态

```text
Qwen-VL
Image + Text
    ↓
Qwen2-VL
Dynamic Resolution + MRoPE
    ↓
Qwen2.5-VL
Visual Agent
    ↓
Qwen2.5-Omni
Thinker-Talker
    ↓
Qwen3-VL
Long Multimodal Context
    ↓
Qwen3.5+
Native Multimodal
    ↓
Qwen3.8-Flash-Next
Multimodal MoE
```

---

# 四十一、Agent / Coding

```text
Qwen-Chat
Tool Use
   ↓
Qwen2.5
Better Tool Calling
   ↓
Qwen3
Agent Capability
   ↓
Qwen3-Coder
Agentic Coding
   ↓
Qwen Code
Agent Harness
   ↓
Qwen3.6 / 3.8
Agentic Coding Scaling
   ↓
Computer Use / Multimodal Agent
```

---

# 第十二篇：最新完整技术树

# 四十二、Qwen 完整技术树

```text
                                  Qwen
                                   │
                             Foundation Model
                                   │
                                   ▼
                               Qwen1.5
                                   │
                         Ecosystem + MoE
                                   │
                                   ▼
                                Qwen2
                                   │
                                  GQA
                              「少存 KV」
                                   │
                                   ▼
                               Qwen2.5
                                   │
                         Data + Post-training
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
                 QwQ            Qwen-VL          Coder
                  │                │                │
             RL Reasoning     Multimodal       Coding
                  │                │                │
                  └────────────────┼────────────────┘
                                   ▼
                                Qwen3
                                   │
                     Thinking + Non-thinking
                         Thinking Budget
                                   │
                                   ▼
                             Qwen3-Next
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
       Gated DeltaNet        Gated Attention       Ultra-Sparse MoE
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   │
                                  MTP
                                   │
                                   ▼
                       Qwen3.5 → 3.6 → 3.7 → 3.8
                                   │
                         Hybrid Architecture
                                   │
                                   ▼
                         Qwen3.8-Flash-Next
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
    Attention                  Residual                   Capacity
        │                          │                          │
   GDN + QSA              Gated Residual            N-gram Embedding
 Linear + Sparse           4 Branches                Lookup Memory
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
                                  Muon
                                   │
                                   ▼
                       Qwen4 Architecture Preview
                                   │
                          （完整 Qwen4 尚未发布）
```

---

# 第十三篇：按能力重新总结

# 四十三、能力地图

| 能力 | Qwen 技术 | 一句话 |
| --- | --- | --- |
| **做得大** | Sparse MoE | 总容量大、激活少 |
| **进一步扩容量** | N-gram Embedding | 用查表增加容量 |
| **存得住** | GQA | 多 Q 共享 KV |
| **看得远** | GDN + QSA + YaRN | 原生 262K，可扩 1M |
| **高效记历史** | GDN | 历史压进 State |
| **精确找历史** | QSA | Micro-block Sparse Selection |
| **层间传得稳** | Gated Residual | 4 分支 + Dynamic Gate |
| **训得省 / 稳** | Muon + AdamW | Optimizer 与架构协同 |
| **吐得快** | MTP | 多 Token Prediction |
| **会推理** | QwQ → Qwen3 | RL → Unified Thinking |
| **控制思考成本** | Thinking Budget | 决定想多久 |
| **看得懂多模态** | Qwen-VL / Omni | Image / Video / Audio |
| **会写工程代码** | Qwen3-Coder / Qwen3.6+ | Agentic Coding |
| **会做事** | Qwen Code / Agent | Tool + Environment |
| **下一代架构** | Qwen3.8-Flash-Next | Qwen4 Early Preview |

---

# 四十四、关键技术一句话总结

## GQA

> **多个 Query Head 共用 KV，核心是“少存”。**

## Gated DeltaNet

> **把长历史持续压缩进固定状态，核心是“高效记”。**

## QSA

> **用轻量压缩 Indexer 按 Micro-block 挑重要 Context，核心是“少看但找得准”。**

## GDN + QSA

> **GDN 负责记，QSA 负责找。**

## Gated Residual

> **把 Residual Stream 扩成多分支，用动态 Gate 控制跨层读写。**

## N-gram Embedding

> **通过 Lookup Memory 增加模型容量，而不是把所有容量都变成矩阵计算。**

## Muon

> **与 AdamW 分工，并针对新架构重新优化正交化、参数划分和 Scaling Law。**

## Qwen3-Next

> **Qwen 从传统 Transformer Scaling 转向 Hybrid Attention + Ultra-Sparse MoE 的关键节点。**

## Qwen3.8-Flash-Next

> **从 Linear + Dense Hybrid 进一步走向 Linear + Sparse Hybrid，并预览 Qwen4 架构。**

---

# 第十四篇：关键论文 / 官方资料索引

# 四十五、主模型与架构

| 时间 | 模型 / 技术 | 资料 | 核心技术 |
| --- | --- | --- | --- |
| 2023 | Qwen | https://arxiv.org/abs/2309.16609 | Foundation Model Family |
| 2024 | Qwen2 | https://arxiv.org/abs/2407.10671 | GQA、Multilingual |
| 2024 | Qwen2.5 | https://arxiv.org/abs/2412.15115 | 18T Tokens、Post-training |
| 2025 | Qwen3 | https://arxiv.org/abs/2505.09388 | Hybrid Thinking、Thinking Budget |
| 2025.09 | Qwen3-Next | https://qwen.ai/blog?id=qwen3-next | GDN + Gated Attention、Ultra-Sparse MoE、MTP |
| 2026.04 | Qwen3.6-27B | https://qwen.ai/blog?id=qwen3.6-27b | Dense Multimodal、Agentic Coding |
| 2026.08 | Qwen3.8-Flash-Next | https://qwen.ai/blog?id=qwen3.8-flash-next | GDN + QSA、GR、N-gram、Muon |
| 2026.08 | Qwen3.8-Flash-Next Repo / Tech Report | https://github.com/QwenLM/Qwen3.8-Flash-Next | Qwen4 Architecture Preview |

---

# 四十六、Qwen3.8-Flash-Next 四大技术出处

| 技术 | 官方描述重点 |
| --- | --- |
| **GDN + QSA** | GDN 压缩历史；QSA 用压缩轻量 Indexer 在 Micro-block 粒度选择重要 Context |
| **Gated Residual** | Residual Stream 扩成 4 分支，Dynamic Gate 控制读写 |
| **N-gram Embedding** | Local Context 查表扩容量，可 Offload 到 Host Memory |
| **Muon** | 优化 Orthogonalization、Muon/AdamW 分工、Fused Parameter Splitting |

---

# 第十五篇：与 DeepSeek / Kimi / GLM 横向对照

# 四十七、2026 长上下文架构路线

| 厂商 / 模型 | 核心路线 | 一句话 |
| --- | --- | --- |
| **DeepSeek** | Compression + Sparse / Hybrid Attention | 先压缩，再减少需要看的内容 |
| **Kimi** | Recurrent / Linear + Global Attention | 大部分历史写进状态，需要时全局找 |
| **GLM** | DSA + Index Sharing | Sparse Attention + 多层复用选择结果 |
| **Qwen3.8-Flash-Next** | **GDN + QSA** | **高效记历史 + Sparse 精确找历史** |

从教学角度可以记成：

```text
DeepSeek
压缩后再看

Kimi
写进状态，需要时找

GLM
挑重要 Token，多层共享

Qwen
GDN 负责记
QSA 负责找
```

---

# 四十八、Qwen 最新架构的四个 Scaling 维度

```text
                     Qwen3.8-Flash-Next
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
       Sequence             Depth              Capacity
          │                   │                   │
      GDN + QSA        Gated Residual      Sparse MoE
          │                   │             + N-gram
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                         Optimization
                              │
                             Muon
```

因此可以总结成：

| Scaling 维度 | 技术 |
| --- | --- |
| **Sequence Scaling** | GDN + QSA |
| **Depth Scaling** | Gated Residual |
| **Width / Capacity Scaling** | Sparse MoE + N-gram Embedding |
| **Optimization Scaling** | Muon + AdamW Co-design |

---

# 第十六篇：最终总结

Qwen 的核心技术演进可以浓缩成七个阶段：

```text
Qwen
Foundation Model Family
        ↓
Qwen2
GQA
「少存 KV」
        ↓
Qwen2.5
Data + Post-training Scaling
        ↓
QwQ → Qwen3
RL Reasoning
Thinking + Non-thinking
        ↓
Qwen3-Next
GDN + Gated Attention
Ultra-Sparse MoE
MTP
        ↓
Qwen3.5 → 3.6 → 3.7 → 3.8
Hybrid Architecture Scale-up
        ↓
Qwen3.8-Flash-Next
GDN + QSA
Gated Residual
N-gram Embedding
Muon
        ↓
Qwen4 Architecture Preview
```

最终可以用一句话概括：

> **Qwen 的主线已经从早期依靠数据、参数和 GQA 的传统 Transformer Scaling，逐步转向 Architecture Scaling：Qwen3-Next 用 Gated DeltaNet + Gated Attention 建立 Linear + Dense Hybrid Attention，并通过 Ultra-Sparse MoE 与 MTP 降低训练和推理成本；这套架构随后贯穿 Qwen3.5、3.6、3.7 与 3.8。最新 Qwen3.8-Flash-Next 又进一步用 QSA 把 Hybrid Attention 从“Linear + Dense”推进到“Linear + Sparse”，同时引入 Gated Residual 强化跨层信息流、N-gram Embedding 以低计算成本扩容量，以及 Muon 优化训练。这四条技术线共同构成 Qwen4 的 Early Architecture Preview。**
