# Kimi 核心技术演进

> 从 Mooncake、MoBA、Kimi k1.5、Kimi-VL、Kimi K2、Kimi Linear、Kimi K2.5，到最新 Kimi K3

------------------------------------------------------------------------

# 第一篇：主模型与技术全景

## 一、先看全景：Kimi 到底在解决什么问题？

Kimi 的技术演进不能简单理解成：

``` text
K1 → K2 → K2.5 → K3
```

更准确地说，Kimi 围绕 **长上下文、训练扩展、Reasoning、多模态、Agent、Serving** 多条路线并行演进：

| 核心问题                        | Kimi 技术              | 一句话理解                                  |
|:--------------------------------|:-----------------------|:--------------------------------------------|
| **长上下文怎么服务？**          | Mooncake               | Prefill / Decode 分离 + 分布式 KV Cache     |
| **长上下文怎么算得省？**        | MoBA                   | 按 Block 动态挑重点看                       |
| **Reasoning 怎么练？**          | Kimi k1.5              | Scaling RL + Long2Short                     |
| **多模态怎么看得清？**          | Kimi-VL / MoonViT      | Native Resolution Vision                    |
| **大模型怎么训得稳？**          | MuonClip               | Muon + QK-Clip                              |
| **模型怎么做大？**              | MoE → Stable LatentMoE | 大容量、低激活、稳定训练                    |
| **KV Cache 怎么进一步降？**     | MLA → KDA + Gated MLA  | 从压缩 KV 走向固定状态 + 少量全局 Attention |
| **1M Context 怎么实现？**       | Kimi Linear → K3       | KDA 为主、Gated MLA 补全局                  |
| **模型深了怎么传信息？**        | Attention Residuals    | 沿深度动态检索历史层表示                    |
| **怎么从 Agent 到并行 Agent？** | Agent Swarm            | 自动拆任务并行执行                          |
| **怎么形成原生多模态 Agent？**  | K2.5 → K3              | Text + Vision + RL + Agent                  |
| **3T 级模型怎么稳定扩展？**     | Stable LatentMoE       | 896 Experts / Top-16 + 稳定化设计           |

可以把 Kimi 的主线理解为：

``` text
长上下文服务
Mooncake
    ↓
长上下文少算
MoBA
    ↓
Reasoning
Kimi k1.5
    ↓
原生视觉
Kimi-VL
    ↓
Agentic Intelligence
Kimi K2
    ↓
Linear / Recurrent Attention
Kimi Linear
    ↓
Visual Agentic Intelligence
Kimi K2.5
    ↓
1M Context + Frontier Agent
Kimi K3
```

但需要特别强调：

> **这不是严格的”架构替代链”。**

Mooncake 属于 Serving Infra；MoBA 属于 Sparse Attention；MLA 属于 KV 压缩；KDA 属于 Linear / Recurrent Attention；K2.5 重点是多模态与 Agent，而 K3 才真正把 KDA 大规模引入主干。

------------------------------------------------------------------------

## 二、Kimi 关键论文 / 技术报告时间线

| 时间    | 模型 / 技术     | 类型               | 论文 / 技术报告                                                          | 核心技术                                              |
|:--------|:----------------|:-------------------|:-------------------------------------------------------------------------|:------------------------------------------------------|
| 2024.06 | **Mooncake**    | Serving Infra      | *Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving* | P/D 分离、Distributed KV Cache                        |
| 2025.01 | **Kimi k1.5**   | Reasoning / RL     | *Kimi k1.5: Scaling Reinforcement Learning with LLMs*                    | Scaling RL、Long Context、Long2Short                  |
| 2025.02 | **MoBA**        | Attention Research | *MoBA: Mixture of Block Attention for Long-Context LLMs*                 | Block-level Sparse Attention                          |
| 2025.04 | **Kimi-VL**     | Multimodal         | *Kimi-VL Technical Report*                                               | MoonViT、128K、Multimodal Reasoning                   |
| 2025.07 | **Kimi K2**     | 主模型             | *Kimi K2: Open Agentic Intelligence*                                     | 1T MoE、MLA、MuonClip、Agentic RL                     |
| 2025.10 | **Kimi Linear** | Attention Research | *Kimi Linear: An Expressive, Efficient Attention Architecture*           | **KDA + MLA Hybrid**                                  |
| 2026.02 | **Kimi K2.5**   | 主模型             | *Kimi K2.5: Visual Agentic Intelligence*                                 | Native Multimodal、Agent Swarm、Joint RL              |
| 2026.07 | **Kimi K3**     | 最新主模型         | *Kimi K3: Open Frontier Intelligence*                                    | **KDA + Gated MLA + AttnRes + Stable LatentMoE + 1M** |

------------------------------------------------------------------------

# 第二篇：长上下文技术演进

# 三、Mooncake：先解决”长上下文怎么服务”

## 3.1 论文

**Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving**

https://arxiv.org/abs/2407.00079

Mooncake 不是模型 Attention 架构，而是 Kimi 的 Serving Infrastructure。

核心：

``` text
Request
   │
   ├──────────────┐
   ▼              ▼
Prefill Cluster  Decode Cluster
   │              │
   └──────┬───────┘
          ▼
 Distributed KV Cache
 CPU / DRAM / SSD / GPU
```

主要思想：

1.  **Prefill / Decode 分离**
2.  **KVCache-centric Scheduling**
3.  利用 CPU、DRAM、SSD 等构建分布式 KV Cache Pool
4.  通过调度优化长上下文吞吐与 SLO

一句话：

> **Mooncake：把长上下文推理的 KV Cache 从单卡问题升级成整个集群的存储与调度问题。**

因此它应该归类为：

``` text
Inference / Serving
      │
      ├─ 存得住
      └─ 扛得多
```

而不是 Attention Architecture。

------------------------------------------------------------------------

# 四、MoBA：从”全部 Token 看”到”挑重要 Block 看”

## 4.1 论文

**MoBA: Mixture of Block Attention for Long-Context LLMs**

https://arxiv.org/abs/2502.13189

MoBA：

**Mixture of Block Attention**

核心思想是把 MoE 的 Routing 思想应用到 Attention。

传统 Full Attention：

``` text
Query
  ↓
所有历史 Token
  ↓
Attention
```

MoBA：

``` text
Long Context
     ↓
Split into Blocks
     ↓
Block Router
     ↓
Top-K Relevant Blocks
     ↓
Attention
```

一句话：

> **MoBA：不是每个历史 Token 都看，而是先挑重要 Block。**

它与固定 Sliding Window 不同：

``` text
SWA
只看附近窗口

MoBA
模型自己决定看哪些 Block
```

因此可以记成：

> **SWA：附近看。**
>
> **MoBA：挑 Block 看。**

MoBA 已被用于 Kimi 的长上下文请求，但它更适合作为一条 Sparse Attention 研究与工程路线，而不是 K2/K3 的严格版本替代链。

------------------------------------------------------------------------

# 五、MLA：Kimi K2 的 KV 压缩路线

Kimi K2 的文本主干采用 MLA。

MLA：

**Multi-head Latent Attention**

核心思想：

``` text
K / V
 │
 ▼
Low-Rank Compression
 │
 ▼
Latent KV
 │
 ▼
KV Cache
```

一句话：

> **MLA：压缩 KV，让长上下文”存得更省”。**

因此 MoBA 与 MLA 解决的并不是同一个问题：

``` text
                    长上下文成本
                         │
             ┌───────────┴───────────┐
             │                       │
       KV Cache 太大            Attention 太贵
             │                       │
             ▼                       ▼
            MLA                     MoBA
             │                       │
           少存                    少算
```

------------------------------------------------------------------------

# 六、Kimi Linear：KDA 正式出现

## 6.1 论文

**Kimi Linear: An Expressive, Efficient Attention Architecture**

https://arxiv.org/abs/2510.26692

这是理解 Kimi K3 最关键的前置论文。

Kimi Linear 提出：

# KDA

**Kimi Delta Attention**

KDA 是一种 Linear / Recurrent Attention。

其核心不是：

> 从历史 Token 中挑少数 Token。

而是：

> **把历史信息持续写入固定大小的 recurrent state。**

概念上：

``` text
传统 Attention

Token 1 ─┐
Token 2 ─┤
Token 3 ─┤──→ KV Cache 随序列增长
...      │
Token N ─┘
```

KDA：

``` text
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
   ↓
...
```

因此：

> **KDA 的历史状态大小不随序列长度线性增长。**

一句话：

> **KDA：不是把所有历史 Token 存下来，而是把历史持续”写进状态”。**

------------------------------------------------------------------------

## 6.2 KDA 从哪里来？

KDA 在 Gated DeltaNet 的基础上进一步改进。

Kimi Linear 的关键变化之一是：

> **更细粒度的 Channel-wise Gating。**

这样不同特征通道可以具有不同的：

``` text
Remember
Forget
Update
```

行为。

可以直观理解：

``` text
历史信息
   ↓
Channel-wise Gate
   │
   ├─ 这个信息继续记
   ├─ 这个信息减弱
   └─ 这个信息更新
   ↓
Recurrent State
```

------------------------------------------------------------------------

## 6.3 为什么 KDA 仍然需要 MLA？

Linear / Recurrent Attention 的优势：

``` text
固定状态
低 KV Cache
长序列效率高
```

但它也存在一个天然问题：

> 历史被压缩进有限状态之后，如何精确重新访问很久以前的具体信息？

因此 Kimi Linear 并没有全部使用 KDA。

而是：

``` text
KDA
KDA
KDA
MLA
KDA
KDA
KDA
MLA
...
```

也就是：

> **KDA 负责高效持续记忆，MLA 负责显式全局检索。**

这成为 K3 的直接架构基础。

------------------------------------------------------------------------

## 6.4 Kimi Linear 的效率意义

论文报告，在其测试设置中：

- KV Cache 最多降低约 **75%**
- 1M Context 下 Decode Throughput 最多提升约 **6×**

因此 Kimi 的长上下文路线开始发生根本变化：

``` text
过去：
如何减少 KV Cache？

↓

现在：
能不能让大部分层根本不需要随 Token 增长的 KV Cache？
```

------------------------------------------------------------------------

# 七、Kimi K3：KDA + Gated MLA 正式进入 2.8T 主模型

## 7.1 技术报告

**Kimi K3: Open Frontier Intelligence**

https://arxiv.org/abs/2607.24653

K3 是截至 2026 年 7 月 Kimi 架构路线最重要的一次升级。

核心规格：

| 项目              | Kimi K3                   |
|:------------------|:--------------------------|
| 总参数            | **2.8T**                  |
| 激活参数          | **104B**                  |
| 主干层数          | **93**                    |
| KDA Layers        | **69**                    |
| Gated MLA Layers  | **24**                    |
| Routed Experts    | **896**                   |
| 每 Token 激活专家 | **16**                    |
| Shared Experts    | **2**                     |
| Context           | **1,048,576 Tokens**      |
| Vision Encoder    | **MoonViT-V2**            |
| 模型形态          | **Native Multimodal MoE** |

------------------------------------------------------------------------

## 7.2 K3 Attention 结构

K3 的 93 层中：

``` text
69 KDA
+
24 Gated MLA
```

整体大致采用：

``` text
KDA
 ↓
KDA
 ↓
KDA
 ↓
Gated MLA
 ↓
KDA
 ↓
KDA
 ↓
KDA
 ↓
Gated MLA
 ↓
...
```

即：

> **约 3 KDA : 1 Gated MLA。**

最终还保留额外的 MLA 层用于全局信息处理。

所以 K3 不是：

``` text
Pure Linear Attention
```

而是：

# Hybrid Attention

``` text
KDA
+
Gated MLA
```

------------------------------------------------------------------------

## 7.3 两种 Attention 的分工

### KDA

负责：

``` text
长序列持续建模
+
固定大小 Recurrent State
+
降低 KV Cache
```

一句话：

> **KDA：高效记住历史。**

### Gated MLA

负责：

``` text
显式 Global Attention
+
精确访问历史 Token
+
补偿有限状态的信息压缩
```

一句话：

> **Gated MLA：需要的时候重新全局找。**

所以：

``` text
KDA
负责「持续记」

+

Gated MLA
负责「精确找」
```

------------------------------------------------------------------------

# 八、Kimi 长上下文技术线应该怎么画？

不建议画成：

``` text
MoBA → MLA → KDA
```

因为三者解决的问题不同。

更准确的是三条路线：

``` text
                 Kimi Long Context

        ┌────────────┼────────────┐
        │            │            │
   Sparse Attention  KV Compression  Linear / Recurrent
        │            │            │
       MoBA         MLA          KDA
        │            │            │
    少看 Block      少存 KV      固定状态记忆
                                  │
                                  ▼
                           KDA + Gated MLA
                                  │
                                  ▼
                              Kimi K3
                                  │
                                  ▼
                              1M Context
```

再加一条 Infra：

``` text
Mooncake
   │
   ▼
KVCache-centric Serving
```

因此：

> **Mooncake：怎么服务长上下文。**
>
> **MoBA：怎么少算 Attention。**
>
> **MLA：怎么少存 KV。**
>
> **KDA：怎么改变历史信息的存储方式。**

------------------------------------------------------------------------

# 第三篇：模型规模与训练技术

# 九、Kimi K2：Open Agentic Intelligence

## 9.1 技术报告

**Kimi K2: Open Agentic Intelligence**

https://arxiv.org/abs/2507.20534

K2 是 Kimi 从长上下文模型向 Agentic Model 转型的重要节点。

核心规格：

``` text
1T Total Parameters
32B Active Parameters
MoE
MLA
```

但 K2 最值得关注的不只是模型规模，而是：

``` text
MuonClip
+
Large-Scale Agentic Data Synthesis
+
Joint Reinforcement Learning
```

------------------------------------------------------------------------

# 十、MuonClip：让 Muon 在超大模型上更稳定

K2 提出：

# MuonClip

其基础是 Muon Optimizer。

Muon 的优势是较好的 Token Efficiency，但大规模训练时可能出现 Attention Logit 爆炸等稳定性问题。

K2 加入：

> **QK-Clip**

形成：

``` text
Muon
  ↓
QK-Clip
  ↓
MuonClip
```

目标：

> **既保留 Muon 的训练效率，又提高超大规模训练稳定性。**

K2 报告指出，其 1T 模型在约 15.5T Token 预训练过程中实现 zero loss spike。

一句话：

> **MuonClip：给 Muon 加一道 QK 稳定器。**

------------------------------------------------------------------------

# 十一、Stable LatentMoE：K3 的宽度扩展路线

K3 把模型扩大到：

``` text
2.8T Total
104B Active
```

其 MoE 结构：

``` text
896 Routed Experts
      │
      ▼
Top-16 / Token
      +
2 Shared Experts
```

但 K3 的重点不只是”更多专家”。

而是：

# Stable LatentMoE

可以从三个关键词理解：

``` text
Latent Projection
+
Extreme Expert Sparsity
+
Stable Routing / Activation
```

K3 把 Hidden Representation 先投影到较低维的 Latent MoE Space，再进行 Expert Computation。

概念上：

``` text
Hidden State
7168
  ↓
Latent Projection
3584
  ↓
Router
  ↓
16 / 896 Experts
  ↓
Output
```

这让 K3 能够在保持巨大模型容量的同时控制每 Token 的激活计算。

一句话：

> **Stable LatentMoE：先进入更紧凑的专家空间，再从 896 个专家里激活 16 个。**

------------------------------------------------------------------------

# 十二、K2 → K3：MoE 如何扩展

``` text
Kimi K2
1T Total
32B Active
     │
     ▼
Kimi K3
2.8T Total
104B Active
     │
     ├─ 896 Routed Experts
     ├─ Top-16
     ├─ 2 Shared Experts
     └─ Stable LatentMoE
```

K3 技术报告称，结合 KDA、Attention Residuals、Stable LatentMoE 与新的训练配方后，整体 Scaling Efficiency 相比 K2 提升约 **2.5×**。

------------------------------------------------------------------------

# 十三、K3 的低精度路线

K3 官方模型配置还引入：

``` text
MXFP4 Weights
+
MXFP8 Activations
+
Quantization-Aware Training
```

需要注意：

> 这不是简单的部署后 PTQ。

而是模型训练过程中考虑量化行为的 QAT 路线。

一句话：

> **K3：在 2.8T 规模上把低精度直接纳入模型训练与部署设计。**

------------------------------------------------------------------------

# 第四篇：Depth Scaling

# 十四、Attention Residuals：不仅扩 Sequence，也扩 Depth

K3 一个非常重要但容易被 KDA 抢走注意力的创新是：

# Attention Residuals

简称：

**AttnRes**

传统 Transformer Residual：

``` text
Layer 1
  ↓
Layer 2
  ↓
Layer 3
  ↓
Layer 4
```

信息主要沿层逐层累积。

AttnRes 的思路是：

> 当前层可以对历史层表示进行动态加权组合。

概念上：

``` text
Layer 1 ───────┐
Layer 2 ───────┤
Layer 3 ───────┤
Layer 4 ───────┤
               ▼
        Attention over
        Historical Layers
               │
               ▼
          Current Layer
```

因此它处理的是：

``` text
KDA / MLA
Token ↔ Token

AttnRes
Layer ↔ Layer
```

------------------------------------------------------------------------

## 14.1 Sequence Scaling vs Depth Scaling

K3 很适合用下面这个框架理解：

``` text
                   Kimi K3 Scaling

              ┌──────────┴──────────┐
              │                     │
       Sequence Length          Model Depth
              │                     │
              ▼                     ▼
      KDA + Gated MLA             AttnRes
              │                     │
        Token ↔ Token           Layer ↔ Layer
```

一句话：

> **KDA 解决序列方向的信息流，AttnRes 解决深度方向的信息流。**

这与 K3 技术报告对两项技术的定位是一致的。

------------------------------------------------------------------------

# 第五篇：Reasoning 与 RL

# 十五、Kimi k1.5：Scaling Reinforcement Learning

## 15.1 论文

**Kimi k1.5: Scaling Reinforcement Learning with LLMs**

https://arxiv.org/abs/2501.12599

Kimi k1.5 是 Kimi Reasoning 路线的重要节点。

核心不是提出复杂的新 RL 算法，而是强调：

> **Scaling RL 本身就是新的 Scaling Axis。**

主要技术包括：

``` text
Long Context Scaling
+
Improved Policy Optimization
+
Long-CoT RL
+
Long2Short
```

------------------------------------------------------------------------

## 15.2 Long2Short

Kimi k1.5 的一个重要思想：

> 用 Long-CoT 模型的能力改善 Short-CoT 模型。

概念上：

``` text
Long Reasoning
      │
      ▼
Strong Long-CoT Policy
      │
      ▼
Long2Short
      │
      ▼
Shorter Reasoning
+
Strong Performance
```

一句话：

> **先学会想得很长，再学会想得更短。**

------------------------------------------------------------------------

# 十六、K2：Agentic RL

K2 的 Post-training 不再只针对：

``` text
Math
Reasoning
```

而是开始大量加入：

``` text
Real Environment
+
Synthetic Environment
+
Tool Interaction
+
Agentic Data
```

核心：

``` text
Large-Scale Agentic
Data Synthesis
      +
Joint RL
```

因此 Kimi 的 RL 演进可以概括为：

``` text
Kimi k1.5
Scaling RL
    ↓
Reasoning
    ↓
Kimi K2
Agentic Data + Joint RL
    ↓
Agentic Intelligence
```

------------------------------------------------------------------------

# 十七、K3：General + Agentic + Coding RL

K3 进一步把 RL 扩展到多个领域：

``` text
General
   +
Agentic
   +
Coding
```

并支持：

``` text
Multiple Reasoning Effort Levels
```

即：

> 模型可以根据任务复杂度使用不同推理预算。

同时 K3 还针对：

> **Long-Horizon Agent Execution**

进行了大规模训练与 Infra 优化。

所以：

``` text
k1.5
会长思考
   ↓
K2
会使用环境 / 工具
   ↓
K2.5
会看 + 会做 + 多 Agent
   ↓
K3
长上下文 + 长时程 Agent
```

------------------------------------------------------------------------

# 第六篇：多模态演进

# 十八、Kimi-VL：Native Resolution Vision

## 18.1 技术报告

**Kimi-VL Technical Report**

https://arxiv.org/abs/2504.07491

Kimi-VL 是 Kimi 多模态路线的重要节点。

核心：

# MoonViT

Native-Resolution Vision Encoder

它不要求所有图片简单 Resize 到固定低分辨率。

主要面向：

``` text
High Resolution Image
Document
OCR
Screenshot
Chart
Video
```

Kimi-VL 支持：

``` text
128K Context
+
Native Resolution
+
Multimodal Reasoning
+
Agent
```

一句话：

> **MoonViT：尽量保持原图细节，而不是先把高分辨率信息压没。**

------------------------------------------------------------------------

# 十九、Kimi K2.5：Visual Agentic Intelligence

## 19.1 技术报告

**Kimi K2.5: Visual Agentic Intelligence**

https://arxiv.org/abs/2602.02276

K2.5 的重点不是 KDA。

这一点需要特别注意：

> **K2.5 仍属于 K2 / MLA 架构世代。**

它真正的重点是：

# Native Multimodal + Agent

训练路线：

``` text
Joint Text-Vision Pre-training
        ↓
Zero-Vision SFT
        ↓
Joint Text-Vision RL
        ↓
Visual Agentic Intelligence
```

核心思想：

> **不是把视觉模型外挂到文本模型，而是让 Text 与 Vision 从训练阶段就共同优化。**

------------------------------------------------------------------------

# 二十、Agent Swarm：从单 Agent 到并行 Agent

K2.5 还提出：

# Agent Swarm

传统单 Agent：

``` text
Task
 ↓
Agent
 ↓
Step 1
 ↓
Step 2
 ↓
Step 3
```

Agent Swarm：

``` text
                  Complex Task
                       │
                       ▼
                 Task Decompose
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Agent A         Agent B         Agent C
        │              │              │
     Subtask A       Subtask B       Subtask C
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                    Merge
```

一句话：

> **Agent Swarm：复杂任务自动拆分，然后多个 Agent 并行执行。**

论文报告在其测试设置下，Agent Swarm 相比单 Agent 基线最高可降低约 **4.5× latency**。

------------------------------------------------------------------------

# 二十一、K3：原生多模态进一步进入主干

K3 不再把多模态视为单独分支，而是：

> **Native Multimodal Frontier Model**

K3 使用：

# MoonViT-V2

视觉能力与：

``` text
Text
Vision
Reasoning
Coding
Agent
```

共同进入统一模型。

所以多模态路线可以写成：

``` text
Kimi-VL
   │
MoonViT
Native Resolution
   │
   ▼
Kimi K2.5
   │
Joint Text-Vision Training
+
Joint RL
+
Agent Swarm
   │
   ▼
Kimi K3
   │
MoonViT-V2
+
Native Multimodal
+
Long-Horizon Agent
```

------------------------------------------------------------------------

# 第七篇：Kimi K3 架构全景

# 二十二、K3 的三个 Scaling 维度

理解 K3 最好的方法不是背技术名，而是看它同时重构了三个方向的信息流。

``` text
                         Kimi K3
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
 Sequence Dimension    Depth Dimension      Width Dimension
       │                    │                    │
       ▼                    ▼                    ▼
 KDA + Gated MLA          AttnRes        Stable LatentMoE
       │                    │                    │
 Token ↔ Token          Layer ↔ Layer      Expert Routing
       │                    │                    │
 长上下文效率            深层信息流             模型容量
```

这可以说是 K3 最核心的架构框架。

------------------------------------------------------------------------

# 二十三、Sequence：KDA + Gated MLA

``` text
93 Layers
   │
   ├─ 69 KDA
   │
   └─ 24 Gated MLA
```

大致：

``` text
[KDA → KDA → KDA → Gated MLA] × N
                     +
                Final MLA
```

作用：

``` text
KDA
固定状态
高效持续记忆

+

Gated MLA
显式全局 Attention
精确检索
```

------------------------------------------------------------------------

# 二十四、Depth：Attention Residuals

传统：

``` text
Layer N
只直接接收上一层累积表示
```

AttnRes：

``` text
Historical Layers
       ↓
Depth Attention
       ↓
Dynamic Weighted Retrieval
       ↓
Current Layer
```

作用：

> **让深层模型能够更灵活地访问浅层与中间层表示。**

------------------------------------------------------------------------

# 二十五、Width：Stable LatentMoE

``` text
Hidden State
    ↓
Latent Space
    ↓
Router
    ↓
16 / 896 Experts
    +
2 Shared Experts
```

作用：

> **让 2.8T 模型保持巨大容量，同时控制每 Token 激活计算并提高训练稳定性。**

------------------------------------------------------------------------

# 二十六、K3 为什么能支持 1M Context？

不是靠单一技术。

而是：

``` text
                       1M Context
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
       KDA             Gated MLA          Infra
        │                  │                  │
固定状态记忆           全局精确检索      KDA Kernel /
降低 KV 增长         少量层保留 KV       Serving Co-design
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                   Million-Token Model
```

因此：

> **1M Context 是 Architecture + Training + Infra Co-design 的结果。**

------------------------------------------------------------------------

# 第八篇：Kimi 完整技术树

# 二十七、完整技术树

``` text
                              Kimi / Moonshot
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   Long Context                  Reasoning                 Multimodal
         │                          │                          │
      Mooncake                  Kimi k1.5                  Kimi-VL
         │                          │                          │
 Serving / KV Cache             Scaling RL                 MoonViT
         │                          │                          │
         ▼                          ▼                          ▼
       MoBA                    Long2Short                 Kimi K2.5
         │                          │                          │
 Sparse Block Attn                 │                 Joint Text-Vision
         │                          │                    + Agent Swarm
         │                          │                          │
         └──────────────┐           │                          │
                        │           │                          │
                        ▼           ▼                          │
                       Kimi K2                                 │
                          │                                   │
                  1T MoE + MLA                                │
                  MuonClip                                    │
                  Agentic RL                                  │
                          │                                   │
              ┌───────────┴───────────┐                       │
              │                       │                       │
              ▼                       ▼                       │
        Kimi Linear               Kimi K2.5 ◀─────────────────┘
              │                       │
             KDA                Visual Agentic
        + Hybrid MLA             Intelligence
              │                       │
              └───────────┬───────────┘
                          ▼
                       Kimi K3
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
 KDA + Gated MLA        AttnRes       Stable LatentMoE
       │                  │                  │
Sequence Scaling     Depth Scaling      Width Scaling
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                    MoonViT-V2
                          │
                    1M Context
                          │
               General / Coding /
                  Agentic RL
                          │
                          ▼
                Open Frontier Intelligence
```

------------------------------------------------------------------------

# 二十八、按能力重新总结

| 能力             | Kimi 技术                   | 一句话                          |
|:-----------------|:----------------------------|:--------------------------------|
| **服务长上下文** | Mooncake                    | P/D 分离 + Distributed KV Cache |
| **少算**         | MoBA                        | 挑重要 Block 看                 |
| **少存**         | MLA                         | 压缩 KV                         |
| **固定状态记忆** | KDA                         | 历史持续写进 recurrent state    |
| **全局找信息**   | Gated MLA                   | 少量层执行显式全局检索          |
| **看得远**       | KDA + Gated MLA             | 1M Context Hybrid Attention     |
| **模型做得大**   | Stable LatentMoE            | 2.8T / 104B Active              |
| **训得稳**       | MuonClip / Stable LatentMoE | 控制超大规模训练稳定性          |
| **深层传得好**   | AttnRes                     | Layer ↔ Layer 动态检索          |
| **会推理**       | k1.5 Scaling RL             | Long-CoT + Long2Short           |
| **会做事**       | K2 Agentic RL               | 环境交互 + Tool Use             |
| **会并行做事**   | Agent Swarm                 | 多 Agent 自动拆解并行执行       |
| **看得清**       | MoonViT                     | Native Resolution Vision        |
| **原生多模态**   | K2.5 / K3                   | Text + Vision Joint Training    |
| **长时程 Agent** | K3                          | 1M Context + Agentic RL         |

------------------------------------------------------------------------

# 二十九、关键技术一句话总结

## Mooncake

> **把 KV Cache 做成集群级基础设施。**

## MoBA

> **挑重要 Block 看。**

## MLA

> **不是少看，而是少存。**

## Kimi k1.5

> **把 RL 本身当成新的 Scaling Axis。**

## Long2Short

> **先学会想得长，再学会想得短。**

## MoonViT

> **尽量保留原始分辨率，让模型看清细节。**

## MuonClip

> **给 Muon 加 QK 稳定器。**

## Kimi K2

> **从大模型走向 Agentic Intelligence。**

## KDA

> **不是把历史 Token 全存下来，而是持续写进固定大小状态。**

## Gated MLA

> **在少量关键层重新做全局精确检索。**

## Attention Residuals

> **让当前层可以动态回看历史层表示。**

## Stable LatentMoE

> **在更紧凑的 Latent Space 中进行极稀疏专家计算。**

## Agent Swarm

> **复杂任务自动拆分，多 Agent 并行执行。**

## Kimi K3

> **KDA 管序列、AttnRes 管深度、Stable LatentMoE 管宽度，再叠加原生多模态和 Agentic RL。**

------------------------------------------------------------------------

# 三十、Kimi 与传统 Transformer 的变化

传统 Transformer：

``` text
Sequence：
Full Attention

Depth：
Residual Connection

Width：
Dense FFN / Conventional MoE
```

Kimi K3：

``` text
Sequence：
KDA + Gated MLA

Depth：
Attention Residuals

Width：
Stable LatentMoE
```

因此 K3 可以理解成：

> **同时重构 Transformer 的序列、深度和宽度三个信息流维度。**

------------------------------------------------------------------------

# 三十一、Kimi 长上下文路线最终总结

最容易记忆的版本：

``` text
Mooncake
解决「怎么服务」
    ↓
MoBA
解决「怎么少看」
    ↓
MLA
解决「怎么少存」
    ↓
Kimi Linear / KDA
解决「能不能不随 Token 增长存 KV」
    ↓
KDA + Gated MLA
解决「高效记忆 + 精确全局检索」
    ↓
Kimi K3
1M Context
```

但技术上更严谨的表达是：

``` text
Serving Infra：
Mooncake

Sparse Attention：
MoBA

KV Compression：
MLA

Linear / Recurrent Attention：
KDA

Hybrid Long Context：
KDA + Gated MLA
```

------------------------------------------------------------------------

# 三十二、K2、K2.5、K3 的区别

| 模型          | 核心定位                    | Attention           | 关键创新                                                | Context |
|:--------------|:----------------------------|:--------------------|:--------------------------------------------------------|:--------|
| **Kimi K2**   | Open Agentic Intelligence   | MLA                 | 1T MoE、MuonClip、Agentic RL                            | 128K    |
| **Kimi K2.5** | Visual Agentic Intelligence | MLA 世代            | Joint Text-Vision、Agent Swarm                          | 256K    |
| **Kimi K3**   | Open Frontier Intelligence  | **KDA + Gated MLA** | AttnRes、Stable LatentMoE、Native Vision、1M Agentic RL | **1M**  |

最重要的区别：

``` text
K2
重点：MoE + Agent

↓

K2.5
重点：Vision + Agent Swarm

↓

K3
重点：
Architecture Scaling
+
1M Context
+
Native Multimodal
+
Long-Horizon Agent
```

------------------------------------------------------------------------

# 三十三、论文 / 技术报告完整索引

## A. 长上下文 / Attention / Serving

| 时间    | 论文                                            | 核心技术                                |
|:--------|:------------------------------------------------|:----------------------------------------|
| 2024.06 | [Mooncake](https://arxiv.org/abs/2407.00079)    | KVCache-centric Serving、P/D Separation |
| 2025.02 | [MoBA](https://arxiv.org/abs/2502.13189)        | Mixture of Block Attention              |
| 2025.10 | [Kimi Linear](https://arxiv.org/abs/2510.26692) | KDA + MLA Hybrid                        |
| 2026.07 | [Kimi K3](https://arxiv.org/abs/2607.24653)     | KDA + Gated MLA + 1M                    |

------------------------------------------------------------------------

## B. Reasoning / RL / Agent

| 时间    | 论文                                          | 核心技术                         |
|:--------|:----------------------------------------------|:---------------------------------|
| 2025.01 | [Kimi k1.5](https://arxiv.org/abs/2501.12599) | Scaling RL、Long2Short           |
| 2025.07 | [Kimi K2](https://arxiv.org/abs/2507.20534)   | Agentic Data Synthesis、Joint RL |
| 2026.02 | [Kimi K2.5](https://arxiv.org/abs/2602.02276) | Visual Agent、Agent Swarm        |
| 2026.07 | [Kimi K3](https://arxiv.org/abs/2607.24653)   | General / Agentic / Coding RL    |

------------------------------------------------------------------------

## C. Multimodal

| 时间    | 论文                                          | 核心技术                         |
|:--------|:----------------------------------------------|:---------------------------------|
| 2025.04 | [Kimi-VL](https://arxiv.org/abs/2504.07491)   | MoonViT、Native Resolution、128K |
| 2026.02 | [Kimi K2.5](https://arxiv.org/abs/2602.02276) | Joint Text-Vision Training / RL  |
| 2026.07 | [Kimi K3](https://arxiv.org/abs/2607.24653)   | MoonViT-V2、Native Multimodal    |

------------------------------------------------------------------------

## D. Model Architecture / Training

| 时间    | 论文                                            | 核心技术                            |
|:--------|:------------------------------------------------|:------------------------------------|
| 2025.07 | [Kimi K2](https://arxiv.org/abs/2507.20534)     | 1T MoE、MuonClip                    |
| 2025.10 | [Kimi Linear](https://arxiv.org/abs/2510.26692) | KDA                                 |
| 2026.07 | [Kimi K3](https://arxiv.org/abs/2607.24653)     | Stable LatentMoE、AttnRes、2.8T MoE |

------------------------------------------------------------------------

# 三十四、课程推荐：论文分三级

## A 级：主干必讲

1.  **Mooncake**
2.  **Kimi k1.5**
3.  **MoBA**
4.  **Kimi K2**
5.  **Kimi Linear**
6.  **Kimi K2.5**
7.  **Kimi K3**

其中最关键的架构论文建议重点讲：

``` text
MoBA
   ↓
Kimi Linear
   ↓
Kimi K3
```

但要明确：

> **它们代表 Sparse Attention → Linear Attention → Hybrid Long-Context 的研究演进，不是简单的代码版本替换关系。**

------------------------------------------------------------------------

## B 级：多模态专题

- Kimi-VL
- MoonViT
- Kimi K2.5
- MoonViT-V2

------------------------------------------------------------------------

## C 级：Infra 专题

- Mooncake
- Mooncake Transfer Engine
- Distributed KV Cache
- Prefill / Decode Disaggregation
- KDA Kernel / System Co-design
- Million-token Agentic RL Infrastructure

------------------------------------------------------------------------

# 三十五、最终总结

Kimi 的技术演进可以浓缩成五个阶段。

## 第一阶段：长上下文先从 Infra 突破

``` text
Mooncake
    ↓
P/D Separation
+
Distributed KV Cache
```

解决：

> **长上下文怎么真正服务起来。**

------------------------------------------------------------------------

## 第二阶段：Attention 开始减少无效计算

``` text
MoBA
   ↓
Block Routing
   ↓
Sparse Attention
```

解决：

> **长上下文不是所有 Token 都值得看。**

------------------------------------------------------------------------

## 第三阶段：Reasoning + Agent

``` text
Kimi k1.5
Scaling RL
    ↓
Kimi K2
Agentic RL
```

解决：

> **模型不仅会回答，还要会长思考、会使用环境完成任务。**

------------------------------------------------------------------------

## 第四阶段：Multimodal Agent

``` text
Kimi-VL
MoonViT
    ↓
Kimi K2.5
Joint Text-Vision
+
Agent Swarm
```

解决：

> **Agent 不仅能读文字，还能看屏幕、图片、文档，并进行并行任务执行。**

------------------------------------------------------------------------

## 第五阶段：K3 重构 Transformer 三个 Scaling 维度

``` text
                         Kimi K3
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
    Sequence              Depth                Width
       │                    │                    │
       ▼                    ▼                    ▼
KDA + Gated MLA          AttnRes        Stable LatentMoE
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                       MoonViT-V2
                            │
                      1M Context
                            │
               General / Coding / Agentic RL
                            │
                            ▼
                 Open Frontier Intelligence
```

最终可以用一句话概括 Kimi：

> **Mooncake 解决”长上下文怎么服务”；MoBA 解决”Attention 怎么少算”；MLA 解决”KV 怎么少存”；Kimi k1.5 解决”Reasoning 怎么通过 Scaling RL 做强”；K2 用 MuonClip 与 Agentic RL 把 1T MoE 推向 Agent；K2.5 把视觉与 Agent Swarm 纳入统一体系；Kimi Linear 则通过 KDA 把大部分历史信息从线性增长的 KV Cache 改造成固定大小 recurrent state；最终 K3 用 KDA + Gated MLA 处理序列维度、Attention Residuals 处理深度维度、Stable LatentMoE 处理宽度维度，再叠加 MoonViT-V2 与大规模 Agentic RL，把 Kimi 推向 2.8T 参数、104B 激活、1M Context 的原生多模态 Frontier Agent。**
