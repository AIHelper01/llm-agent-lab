# DeepSeek 核心技术演进

> 从 DeepSeekMoE、MLA、FP8、MTP、GRPO，到 DSA、mHC、DeepSeek-V4 与 Agentic Intelligence

---

# 第一篇：主模型演进

## 一、先看全景：DeepSeek 到底在解决什么问题？

DeepSeek 的技术演进，并不是简单的：

```text
V1 → V2 → V3 → R1 → V3.2 → V4
```

更准确地说，是围绕几个核心问题持续优化：

| 核心问题 | DeepSeek 技术 | 一句话理解 |
| --- | --- | --- |
| **模型怎么做大？** | DeepSeekMoE | 总参数做大，每个 Token 少激活 |
| **KV 怎么存得下？** | MLA | 压缩 KV |
| **长上下文怎么算得动？** | NSA → DSA → CSA/HCA | 从全部算走向选择、压缩与稀疏计算 |
| **超大模型怎么训得省？** | FP8 → FP4 QAT | 更低精度训练 |
| **MoE 怎么训得稳？** | Aux-loss-free Load Balancing | 专家负载均衡但少干扰主任务 |
| **生成怎么更高效？** | MTP | 同时预测多个未来 Token |
| **推理能力怎么练出来？** | GRPO → R1-Zero → R1 | 用 RL 激发 Reasoning |
| **怎么从 Reasoning 到 Agent？** | V3.2 Agentic RL | Reasoning + Tool Use |
| **深层网络怎么传信息？** | mHC | 升级 Residual Connection |
| **百万上下文怎么落地？** | V4 Hybrid Attention | Compression + Sparse + Dense |

可以把整条路线理解为：

```text
做得大
  ↓
存得住
  ↓
算得动
  ↓
训得省
  ↓
训得稳
  ↓
会推理
  ↓
会用工具
  ↓
支持 1M Context
```

---

## 二、DeepSeek 主模型时间线

这一条只保留“正式主模型”，不把 NSA、mHC、Muon 等独立研究论文混入版本线。

```text
2024.01
DeepSeek LLM
Scaling Law
     │
     ▼
2024.05
DeepSeek-V2
DeepSeekMoE + MLA
「少激活 + 少存 KV」
     │
     ▼
2024.12
DeepSeek-V3
MLA + MoE
FP8 + MTP + Aux-loss-free
「训得省 + 训得稳」
     │
     ├───────────────┐
     │               │
     │               ▼
     │          2025.01
     │        DeepSeek-R1
     │        GRPO + RL
     │         「会推理」
     │               │
     └───────┬───────┘
             ▼
          2025.12
       DeepSeek-V3.2
             │
            DSA
      Scalable RL
   Agentic Task Synthesis
             │
       「长上下文 +
       Reasoning Agent」
             │
             ▼
          2026
       DeepSeek-V4
             │
        CSA + HCA
           mHC
          Muon
        FP4 QAT
             │
             ▼
        1M Context
```

---

## 三、关键论文 / 技术报告时间线

| 时间 | 模型 / 技术 | 类型 | 论文 / 技术报告 | arXiv | 核心技术 |
| --- | --- | --- | --- | --- | --- |
| 2024.01 | **DeepSeek LLM** | 主模型 | *DeepSeek LLM: Scaling Open-Source Language Models with Longtermism* | [2401.02954](https://arxiv.org/abs/2401.02954) | Scaling Law、SFT、DPO |
| 2024.01 | **DeepSeekMoE** | 独立技术论文 | *DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models* | [2401.06066](https://arxiv.org/abs/2401.06066) | Fine-Grained Experts、Shared Experts |
| 2024.02 | **DeepSeekMath** | 数学 / RL | *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models* | [2402.03300](https://arxiv.org/abs/2402.03300) | **GRPO** |
| 2024.05 | **DeepSeek-V2** | 主模型 | *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model* | [2405.04434](https://arxiv.org/abs/2405.04434) | **MLA + DeepSeekMoE + 128K** |
| 2024.12 | **DeepSeek-V3** | 主模型 | *DeepSeek-V3 Technical Report* | [2412.19437](https://arxiv.org/abs/2412.19437) | **MTP、FP8、Aux-loss-free、MLA、MoE** |
| 2025.01 | **DeepSeek-R1** | Reasoning / RL | *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning* | [2501.12948](https://arxiv.org/abs/2501.12948) | **R1-Zero、GRPO、Cold Start、Multi-stage RL** |
| 2025.02 | **NSA** | 独立研究论文 | *Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention* | [2502.11089](https://arxiv.org/abs/2502.11089) | Compression + Selection + Local Attention |
| 2025.09 | **V3.2-Exp** | 主模型实验版 | DeepSeek 官方技术发布 | — | **DSA 首次公开** |
| 2025.12 | **DeepSeek-V3.2** | 主模型 | *DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models* | [2512.02556](https://arxiv.org/abs/2512.02556) | **DSA、Scalable RL、Agentic Task Synthesis** |
| 2025.12 | **mHC** | 独立架构论文 | *mHC: Manifold-Constrained Hyper-Connections* | [2512.24880](https://arxiv.org/abs/2512.24880) | **深层信息流 / Residual 升级** |
| 2026.06 | **DeepSeek-V4** | 主模型 | *DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence* | [2606.19348](https://arxiv.org/abs/2606.19348) | **CSA + HCA、mHC、Muon、FP4 QAT、1M Context** |

---

## 四、DeepSeek LLM：建立 Scaling 方法论

### 4.1 论文

**DeepSeek LLM: Scaling Open-Source Language Models with Longtermism**

https://arxiv.org/abs/2401.02954

这一阶段的重点不是 MLA、DSA，而是建立基础模型扩展方法：

```text
Scaling Law
    +
Data Scaling
    +
7B / 67B
    +
SFT
    +
DPO
```

一句话：

> **DeepSeek LLM：先解决模型应该怎么扩展、怎么训练。**

---

## 五、DeepSeek-V2：DeepSeek 主干架构成型

### 5.1 论文

**DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model**

https://arxiv.org/abs/2405.04434

V2 的两个核心关键词：

```text
                 DeepSeek-V2
                      │
            ┌─────────┴─────────┐
            │                   │
           MLA             DeepSeekMoE
            │                   │
         少存 KV              少激活参数
```

模型规模：

```text
236B Total Parameters
21B Active Parameters
128K Context
```

从这一代开始，DeepSeek 后续主干架构可以概括为：

> **MLA + DeepSeekMoE**

---

## 六、DeepSeek-V3：从架构创新走向系统级效率优化

### 6.1 技术报告

**DeepSeek-V3 Technical Report**

https://arxiv.org/abs/2412.19437

V3 继续使用：

```text
MLA
+
DeepSeekMoE
```

同时加入：

```text
                   DeepSeek-V3
                        │
          ┌─────────────┼─────────────┐
          │             │             │
         FP8           MTP      Aux-loss-free
          │             │       Load Balancing
          │             │             │
        训得省        学得更多        训得稳
```

模型规模：

```text
671B Total
37B Active
```

---

## 七、DeepSeek-R1：重点从 Architecture 转向 Reasoning

### 7.1 论文

**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**

https://arxiv.org/abs/2501.12948

R1 的创新重点不是重新设计 Attention，而是：

> **Reasoning Capability 怎么通过强化学习训练出来。**

核心路线：

```text
DeepSeekMath
     │
    GRPO
     ▼
R1-Zero
     │
   Pure RL
     ▼
Reasoning Emergence
     │
     ▼
DeepSeek-R1
     │
Cold Start
+
Multi-stage RL
```

一句话：

> **R1 改变的不是 Transformer 怎么算，而是模型怎么学会推理。**

---

## 八、DeepSeek-V3.2：长上下文 + Agent

### 8.1 技术报告

**DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models**

https://arxiv.org/abs/2512.02556

V3.2 的三项核心突破：

```text
                    DeepSeek-V3.2
                          │
            ┌─────────────┼──────────────┐
            │             │              │
           DSA       Scalable RL   Agentic Task
            │             │          Synthesis
            │             │              │
          效率         Reasoning        Agent
```

它把 DeepSeek 的主线从：

```text
Reasoning
   ↓
Answer
```

推进到：

```text
Reasoning
   ↓
Tool Call
   ↓
Observation
   ↓
Reasoning
   ↓
Action
```

一句话：

> **V3.2：既解决长上下文计算效率，也把 Reasoning 推向 Agent。**

---

## 九、DeepSeek-V4：百万上下文架构升级

### 9.1 技术报告

**DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence**

https://arxiv.org/abs/2606.19348

V4 的重点不是单纯把 Context Window 拉到 1M，而是重新设计长上下文成本结构：

```text
DeepSeek-V4
     │
 ┌───┼───────────────┐
 │   │               │
CSA HCA             mHC
 │   │               │
 └─Hybrid Attention──┘
         │
        Muon
         │
      FP4 QAT
         │
         ▼
     1M Context
```

V4 的核心思想可以概括为：

> **先减少序列表示，再组合 Sparse 与 Dense Attention。**

---

# 第二篇：核心技术专项

# 十、MoE：模型怎么「做得大、算得省」

## 10.1 DeepSeekMoE 原始论文

**DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models**

https://arxiv.org/abs/2401.06066

核心创新有两个：

```text
Fine-Grained Expert Segmentation
+
Shared Expert Isolation
```

---

## 10.2 Fine-Grained Expert Segmentation

传统 MoE：

```text
Expert 1         Expert 2         Expert 3
████████         ████████         ████████
```

DeepSeekMoE：

```text
E1  E2  E3  E4    E5  E6  E7  E8
██  ██  ██  ██    ██  ██  ██  ██
```

把较大的专家拆成更多细粒度专家，让 Router 可以形成更灵活的组合。

一句话：

> **专家拆得更细，专业分工更明确。**

---

## 10.3 Shared Expert Isolation

```text
                   MoE
                    │
            ┌───────┴───────┐
            │               │
      Shared Experts   Routed Experts
            │               │
         公共知识          专业知识
```

一句话：

> **DeepSeekMoE = 专家拆细 + 公共专家独立。**

---

## 10.4 MoE 技术演进

```text
普通 MoE
   │
   ▼
DeepSeekMoE
   │
   ├─ Fine-Grained Experts
   └─ Shared Experts
   │
   ▼
DeepSeek-V2
236B / 21B Active
   │
   ▼
DeepSeek-V3
671B / 37B Active
   │
   ├─ Auxiliary-Loss-Free
   └─ Node-Limited Routing
   │
   ▼
DeepSeek-V4
更大规模 MoE
```

核心逻辑一直没有变化：

> **总参数越来越大，但一个 Token 实际只激活其中一部分参数。**

---

# 十一、Attention：长上下文怎么演进

这是 DeepSeek 技术体系里最重要的一条线。

```text
                DeepSeek 长上下文演进

MHA
 │
 │ 全部存 + 全部算
 ▼
MLA · DeepSeek-V2
 │
 │ 压缩 KV
 ▼
「少存」
 │
 ▼
NSA · Research
 │
 │ Compression
 │ Selection
 │ Sliding Window
 ▼
Sparse Attention 探索
 │
 ▼
DSA · DeepSeek-V3.2
 │
 │ Lightning Indexer
 │ Top-K
 ▼
「少算」
 │
 ▼
CSA + HCA · DeepSeek-V4
 │
 ├─────────────┐
 │             │
 ▼             ▼
CSA           HCA
 │             │
压缩+Sparse   强压缩+Dense
 │             │
 └──────┬──────┘
        ▼
Hybrid Attention
        │
        ▼
    1M Context
```

---

## 11.1 MLA：解决 KV Cache 太大

MLA：

**Multi-head Latent Attention**

出处：

**DeepSeek-V2**

https://arxiv.org/abs/2405.04434

传统 MHA：

```text
Token
 │
 ├──────── K ─────────→ KV Cache
 │
 └──────── V ─────────→ KV Cache
```

MLA：

```text
K / V
 │
 ▼
Low-Rank Compression
 │
 ▼
Latent Representation
 │
 ▼
KV Cache
```

一句话：

> **MLA：不是少看，而是少存。**

需要特别区分：

```text
MLA ≠ KV Cache Quantization
```

MLA 是：

> 架构级低维表示压缩。

KV Quantization 是：

```text
FP16 → FP8 → INT8 → INT4
```

属于数值精度压缩。

---

## 11.2 NSA：Sparse Attention 的研究探索

论文：

**Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention**

https://arxiv.org/abs/2502.11089

核心结构：

```text
                     Query
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
   Compression      Selection    Sliding Window
         │             │             │
     全局压缩         重点选择        局部信息
         │             │             │
         └─────────────┼─────────────┘
                       ▼
                Sparse Attention
```

一句话：

> **NSA：全局压缩着看 + 重点挑着看 + 附近直接看。**

需要注意：

```text
NSA ≠ DSA
```

NSA 更适合定位为：

> **DeepSeek 在 Sparse Attention 方向的重要独立研究探索。**

而不是主模型版本链中的一个“替代节点”。

---

## 11.3 DSA：解决 Attention 计算太多

DSA：

**DeepSeek Sparse Attention**

正式出处：

**DeepSeek-V3.2**

https://arxiv.org/abs/2512.02556

核心：

```text
Query
  ↓
Lightning Indexer
  ↓
Token Importance Score
  ↓
Top-K
  ↓
Sparse Attention
```

一句话：

> **DSA：挑重要 Token 看。**

---

## 11.4 MLA 与 DSA 的关系

这是最容易混淆的地方。

```text
                    长上下文成本
                         │
            ┌────────────┴────────────┐
            │                         │
       KV Cache 太大             Attention 太贵
            │                         │
            ▼                         ▼
           MLA                       DSA
            │                         │
          少存                      少算
```

所以：

> **MLA 解决“存多少”，DSA 解决“算多少”。**

两者不是替代关系，而是协同关系。

---

## 11.5 CSA：先压缩，再挑重点

CSA：

**Compressed Sparse Attention**

出处：

**DeepSeek-V4**

https://arxiv.org/abs/2606.19348

可以理解为：

```text
1M Tokens
    ↓
Sequence / Token Compression
    ↓
Compressed Representation
    ↓
Sparse Selection
    ↓
DSA
    ↓
Attention
```

一句话：

> **CSA：先压缩，再挑着看。**

---

## 11.6 HCA：压得更狠，然后全局看

HCA：

**Heavily Compressed Attention**

```text
Original Sequence
      ↓
Heavy Compression
      ↓
Short Global Representation
      ↓
Dense Attention
```

所以：

```text
CSA
压缩
 ↓
Sparse


HCA
强压缩
 ↓
Dense
```

一句话：

> **HCA：压得更狠，然后全部看。**

---

## 11.7 为什么 V4 要 Hybrid Attention？

如果全部 Sparse：

```text
Sparse
Sparse
Sparse
Sparse
```

效率高，但可能损失部分全局信息。

如果全部 Dense：

```text
Dense
Dense
Dense
Dense
```

全局信息完整，但 1M Context 计算过于昂贵。

所以 V4 采用：

```text
CSA
 │
CSA
 │
HCA
 │
CSA
 │
CSA
 │
HCA
 │
...
```

核心思想：

> **大多数层追求效率，同时保留全局信息通道。**

---

## 11.8 Attention 演进一句话总结

```text
MHA
全部存、全部看

↓

MLA
压缩着存、仍然看

↓

DSA
压缩着存、挑重点看

↓

CSA / HCA
先压缩序列，
再决定挑着看还是全局看
```

---

# 十二、Training：模型怎么训得更省

训练效率线建议与 mHC 分开，因为 mHC 属于网络连接架构，而不是 Optimizer / Precision 技术。

---

## 12.1 FP8：低精度训练

主要出处：

**DeepSeek-V3 Technical Report**

https://arxiv.org/abs/2412.19437

精度演进：

```text
FP32
 ↓
BF16 / FP16
 ↓
FP8
```

目标：

```text
显存 ↓
带宽 ↓
通信 ↓
计算成本 ↓
```

一句话：

> **FP8：让超大模型用更低成本训练。**

---

## 12.2 Auxiliary-Loss-Free Load Balancing

MoE 很容易出现专家负载不均：

```text
Expert 1 ███████████████
Expert 2 ██
Expert 3 █
Expert 4 █████
```

传统方法：

```text
Main Loss
   +
Auxiliary Balance Loss
```

问题：

> Auxiliary Loss 太强可能干扰模型主任务。

DeepSeek-V3 提出：

**Auxiliary-Loss-Free Load Balancing**

一句话：

> **让 Expert 吃得均匀，但尽量不干扰模型本身学习。**

---

## 12.3 Muon：优化器升级

DeepSeek-V4 使用 Muon。

但需要强调：

> **Muon 不是 DeepSeek 首创。**

代表论文之一：

**Muon is Scalable for LLM Training**

https://arxiv.org/abs/2502.16982

路线：

```text
AdamW
  ↓
Muon
  ↓
DeepSeek-V4
```

一句话：

> **Muon：通过更适合矩阵参数的更新方式改善大模型训练效率。**

---

## 12.4 FP8 → FP4 QAT

DeepSeek 的低精度路线：

```text
BF16
 │
 ▼
DeepSeek-V3
FP8 Training
 │
 ▼
DeepSeek-V4
FP4 QAT
```

需要避免错误表述：

> “V4 整个模型全部使用 FP4 训练。”

更准确的理解是：

> **V4 将 FP4 Quantization-Aware Training 引入适合低精度化的关键路径或权重。**

---

# 十三、Prediction：模型怎么生成得更高效

## 13.1 MTP

MTP：

**Multi-Token Prediction**

出处：

**DeepSeek-V3 Technical Report**

https://arxiv.org/abs/2412.19437

传统：

```text
Token N
  ↓
预测 N+1
```

MTP：

```text
Token N
  │
  ├── N+1
  ├── N+2
  └── ...
```

它首先是：

> **训练目标。**

作用：

```text
Next-Token Prediction
        ↓
Multi-Token Prediction
        ↓
更丰富训练信号
        +
可服务 Speculative Decoding
```

一句话：

> **MTP：一次学习预测多个未来 Token。**

---

# 十四、Depth Scaling：模型深了以后怎么传信息

这一条建议独立出来。

```text
                模型规模扩展

          ┌──────────┴──────────┐
          │                     │
 Sequence Length             Model Depth
          │                     │
          ▼                     ▼
 MLA / DSA / CSA-HCA           mHC
          │                     │
  Token ↔ Token             Layer ↔ Layer
```

---

## 14.1 mHC

论文：

**mHC: Manifold-Constrained Hyper-Connections**

https://arxiv.org/abs/2512.24880

演进：

```text
Residual Connection
       ↓
Hyper-Connections
       ↓
Manifold Constraint
       ↓
mHC
```

它解决的是：

> Hyper-Connections 扩大跨层信息流之后，如何保持稳定 Identity Mapping 与训练稳定性。

一句话：

> **mHC：升级 Layer 与 Layer 之间的信息高速公路。**

---

# 十五、Reasoning：推理能力怎么练出来

```text
DeepSeekMath
2024
 │
GRPO
 │
 ▼
DeepSeek-R1-Zero
 │
Pure RL
 │
 ▼
Reasoning Emergence
 │
 ▼
DeepSeek-R1
 │
Cold Start
+
Multi-stage RL
 │
 ▼
DeepSeek-V3.2
 │
Scalable RL
```

---

## 15.1 GRPO

原始出处：

**DeepSeekMath**

https://arxiv.org/abs/2402.03300

而不是 DeepSeek-R1。

GRPO：

**Group Relative Policy Optimization**

传统 PPO：

```text
Policy Model
     +
Reward Model
     +
Critic / Value Model
```

GRPO：

```text
                    Question
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Response 1   Response 2   Response 3
          │            │            │
        Reward       Reward       Reward
          │            │            │
          └────────────┼────────────┘
                       ▼
               Group Relative
                  Advantage
```

一句话：

> **同一道题多生成几个答案，在组内比较谁更好。**

---

## 15.2 R1-Zero：Pure RL

```text
Base Model
    ↓
Large-Scale RL
    ↓
Reasoning
```

训练过程中出现：

```text
Long Reasoning
     │
     ├── Reflection
     ├── Verification
     ├── Error Correction
     └── Strategy Change
```

即：

> **Reasoning Emergence**

但同时存在：

- 可读性差
- 语言混杂
- 输出结构不稳定

---

## 15.3 R1：Cold Start + Multi-stage RL

```text
Base Model
    ↓
Cold Start Data
    ↓
Reasoning RL
    ↓
Rejection Sampling
    ↓
SFT
    ↓
RL
    ↓
DeepSeek-R1
```

一句话：

> **Cold Start + RL，让推理能力从“能涌现”变成“更稳定可用”。**

---

# 十六、Agent：从会推理到会做事

不要重复再讲一遍 R1，只强调能力边界的变化。

```text
Reasoning
DeepSeek-R1
    │
    ▼
Reasoning + Tool Use
DeepSeek-V3.2
    │
    ▼
Agentic Intelligence
DeepSeek-V4
```

能力变化：

```text
R1：

Reasoning
   ↓
Answer
```

变成：

```text
V3.2 / V4：

Reasoning
   ↓
Tool
   ↓
Observation
   ↓
Reasoning
   ↓
Action
```

V3.2 的：

**Large-Scale Agentic Task Synthesis Pipeline**

可以抽象成：

```text
Environment
+
Tools
+
Goal
+
Multi-step Interaction
```

一句话：

> **从“会想”进一步进入“边想边做”。**

---

# 第三篇：专项模型与分支

# 十七、Code 分支

## 17.1 DeepSeek-Coder

论文：

**DeepSeek-Coder: When the Large Language Model Meets Programming — The Rise of Code Intelligence**

https://arxiv.org/abs/2401.14196

特点：

- 1.3B–33B
- 2T Tokens
- Project-Level Code Corpus
- Fill-in-the-Middle
- 16K Context

---

## 17.2 DeepSeek-Coder-V2

论文：

**DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence**

https://arxiv.org/abs/2406.11931

Coder-V2 建立在 DeepSeek-V2 架构基础上，因此继承：

```text
DeepSeekMoE
+
MLA
```

同时：

```text
Programming Languages
86
 ↓
338

Context
16K
 ↓
128K
```

Code 路线：

```text
DeepSeek-Coder
      ↓
DeepSeek-Coder-V2
      ↓
Reasoning Coding
      ↓
Agentic Coding
```

---

# 十八、Math / Formal Reasoning 分支

## 18.1 DeepSeekMath

论文：

**DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models**

https://arxiv.org/abs/2402.03300

核心：

> **GRPO**

---

## 18.2 DeepSeek-Prover

论文：

**DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale Synthetic Data**

https://arxiv.org/abs/2405.14333

关键词：

> **Lean 4 + 大规模合成证明数据**

---

## 18.3 DeepSeek-Prover-V1.5

论文：

**DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search**

https://arxiv.org/abs/2408.08152

核心：

```text
Proof Assistant Feedback
+
Reinforcement Learning
+
Monte-Carlo Tree Search
```

---

## 18.4 DeepSeek-Prover-V2

论文：

**DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition**

https://arxiv.org/abs/2504.21801

核心：

```text
Complex Theorem
      ↓
Subgoal Decomposition
      ↓
Goal 1 / Goal 2 / Goal 3
      ↓
RL
      ↓
Formal Proof
```

整个数学路线：

```text
DeepSeekMath
     │
    GRPO
     │
     ├────────────→ DeepSeek-R1
     │
     └────────────→ DeepSeek-Prover
                        ↓
                  Prover-V1.5
                   RL + MCTS
                        ↓
                  Prover-V2
             Subgoal Decomposition
                      + RL
```

---

# 十九、多模态分支

DeepSeek 的多模态可以分为两条：

```text
               DeepSeek Multimodal
                       │
            ┌──────────┴──────────┐
            │                     │
           VL                   Janus
            │                     │
        理解为主              理解 + 生成
```

---

## 19.1 DeepSeek-VL

论文：

**DeepSeek-VL: Towards Real-World Vision-Language Understanding**

https://arxiv.org/abs/2403.05525

核心：

**Hybrid Vision Encoder**

主要面向：

```text
OCR
PDF
Chart
Screenshot
Natural Image
Document
```

目标：

```text
High-Resolution Details
+
Semantic Information
```

一句话：

> **既看清细节，又理解语义。**

---

## 19.2 DeepSeek-VL2

论文：

**DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for Advanced Multimodal Understanding**

https://arxiv.org/abs/2412.10302

视觉侧：

```text
Dynamic Tiling
```

语言侧：

```text
DeepSeekMoE
+
MLA
```

一句话：

> **DeepSeek 文本模型中的 MoE 与 MLA 开始迁移到多模态。**

---

## 19.3 Janus

论文：

**Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation**

https://arxiv.org/abs/2410.13848

传统统一多模态：

```text
Same Visual Encoder
       │
       ├─ Understanding
       └─ Generation
```

Janus：

```text
                 Unified Transformer
                       ▲
             ┌─────────┴─────────┐
             │                   │
      Understanding          Generation
         Encoder               Encoder
```

一句话：

> **理解和生成使用不同视觉编码路径，再统一进入 Transformer。**

---

## 19.4 Janus-Pro

论文：

**Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling**

https://arxiv.org/abs/2501.17811

核心：

```text
Better Training Strategy
+
More Data
+
Model Scaling
```

同时强化：

```text
Image Understanding
+
Image Generation
```

---

# 第四篇：总结与论文索引

# 二十、DeepSeek 完整技术树

```text
                               DeepSeek
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
     Model                    Reasoning                  Specialist
       │                          │                          │
DeepSeek LLM               DeepSeekMath                    │
       │                      GRPO                          │
       ▼                          │                          │
DeepSeekMoE                     ▼                          │
       │                  DeepSeek-R1                      │
       │                          │                          │
       ▼                          │                          │
DeepSeek-V2                      │                          │
       │                          │                          │
   MLA + MoE                     │                          │
       │                          │                          │
       ▼                          │                          │
DeepSeek-V3                      │                          │
       │                          │                          │
FP8 + MTP + Aux-free            │                          │
       │                          │                          │
       └──────────────┬───────────┘                          │
                      ▼                                      │
               DeepSeek-V3.2                                │
                      │                                      │
          ┌───────────┼─────────────┐                        │
          │           │             │                        │
         DSA      Scalable RL   Agentic Data                 │
          │           │             │                        │
          └───────────┼─────────────┘                        │
                      ▼                                      │
                 Reasoning Agent                             │
                      │                                      │
                      ▼                                      │
                DeepSeek-V4                                  │
                      │                                      │
            ┌─────────┼─────────┐                            │
            │         │         │                            │
           CSA       HCA       mHC                           │
            │         │         │                            │
            └──Hybrid Attn──────┘                            │
                      │                                      │
                 Muon + FP4                                  │
                      │                                      │
                  1M Context                                  │
                      │                                      │
                 Agentic Coding                               │
                                                             │
            ┌────────────────────┬────────────────────────────┤
            │                    │                            │
          Code                 Math                       Multimodal
            │                    │                            │
     DeepSeek-Coder       DeepSeek-Prover               DeepSeek-VL
            │                    │                            │
        Coder-V2           Prover-V1.5                      VL2
                                 │
                             Prover-V2

Multimodal Generation Branch:

Janus
  ↓
Janus-Pro
```

---

# 二十一、按能力重新总结

| 能力 | 技术 | 一句话 |
| --- | --- | --- |
| **做得大** | DeepSeekMoE | 专家拆细 + Shared Expert |
| **存得住** | MLA | 压缩 KV |
| **算得快** | DSA | 挑重要 Token 看 |
| **看得远** | CSA + HCA | 序列压缩 + Hybrid Attention |
| **训得省** | FP8 / FP4 QAT | 更低精度训练 |
| **训得稳** | Aux-loss-free | 专家负载均衡 |
| **深层传得稳** | mHC | 升级跨层信息流 |
| **学得更多** | MTP | 多 Token 预测 |
| **会推理** | GRPO + R1 | RL 激发 Reasoning |
| **会做事** | Agentic RL | Reasoning + Tool Use |

---

# 二十二、关键技术一句话总结

## DeepSeekMoE

> **专家拆细 + 公共专家共享。**

## MLA

> **不是少看，而是少存。**

## FP8

> **用更低精度把超大模型训得更省。**

## Auxiliary-Loss-Free

> **让 Expert 吃得均匀，又尽量不干扰主任务。**

## MTP

> **一次学习预测多个未来 Token。**

## GRPO

> **同一道题多生成几个答案，在组内比较谁更好。**

## R1

> **通过大规模 RL 把 Reasoning 能力练出来。**

## NSA

> **全局压缩看 + 重点挑着看 + 附近直接看。**

## DSA

> **挑重要 Token 看。**

## mHC

> **升级 Layer 与 Layer 之间的信息高速公路。**

## CSA

> **先压缩，再挑重点看。**

## HCA

> **压得更狠，再全局看。**

## DeepSeek-V4

> **压缩 + Sparse + Dense Hybrid，让百万上下文更经济。**

---

# 二十三、论文 / 技术报告完整索引

## A. 主模型与核心架构

| 时间 | 论文 / 技术报告 | 核心技术 |
| --- | --- | --- |
| 2024.01 | [DeepSeek LLM](https://arxiv.org/abs/2401.02954) | Scaling Law、SFT、DPO |
| 2024.01 | [DeepSeekMoE](https://arxiv.org/abs/2401.06066) | Fine-Grained Experts、Shared Experts |
| 2024.05 | [DeepSeek-V2](https://arxiv.org/abs/2405.04434) | MLA + DeepSeekMoE |
| 2024.12 | [DeepSeek-V3](https://arxiv.org/abs/2412.19437) | FP8 + MTP + Aux-loss-free |
| 2025.01 | [DeepSeek-R1](https://arxiv.org/abs/2501.12948) | GRPO + Pure RL + Cold Start |
| 2025.02 | [Native Sparse Attention](https://arxiv.org/abs/2502.11089) | NSA |
| 2025.12 | [DeepSeek-V3.2](https://arxiv.org/abs/2512.02556) | DSA + Scalable RL + Agentic Task Synthesis |
| 2025.12 | [mHC](https://arxiv.org/abs/2512.24880) | Hyper-Connections / Depth Scaling |
| 2026.06 | [DeepSeek-V4](https://arxiv.org/abs/2606.19348) | CSA + HCA + mHC + Muon + FP4 QAT + 1M |

---

## B. Reasoning / Math

| 时间 | 论文 | 核心技术 |
| --- | --- | --- |
| 2024.02 | [DeepSeekMath](https://arxiv.org/abs/2402.03300) | GRPO |
| 2024.05 | [DeepSeek-Prover](https://arxiv.org/abs/2405.14333) | Synthetic Formal Proof Data |
| 2024.08 | [DeepSeek-Prover-V1.5](https://arxiv.org/abs/2408.08152) | RL + Proof Assistant + MCTS |
| 2025.04 | [DeepSeek-Prover-V2](https://arxiv.org/abs/2504.21801) | Subgoal Decomposition + RL |

---

## C. Code

| 时间 | 论文 | 核心技术 |
| --- | --- | --- |
| 2024.01 | [DeepSeek-Coder](https://arxiv.org/abs/2401.14196) | Project-Level Code Corpus、FIM |
| 2024.06 | [DeepSeek-Coder-V2](https://arxiv.org/abs/2406.11931) | MoE + MLA + 128K |

---

## D. Multimodal

| 时间 | 论文 | 核心技术 |
| --- | --- | --- |
| 2024.03 | [DeepSeek-VL](https://arxiv.org/abs/2403.05525) | Hybrid Vision Encoder |
| 2024.10 | [Janus](https://arxiv.org/abs/2410.13848) | Decoupled Visual Encoding |
| 2024.12 | [DeepSeek-VL2](https://arxiv.org/abs/2412.10302) | Dynamic Tiling + MoE + MLA |
| 2025.01 | [Janus-Pro](https://arxiv.org/abs/2501.17811) | Unified Understanding + Generation |

---

## E. Optimizer / Infrastructure

| 时间 | 论文 | 核心技术 |
| --- | --- | --- |
| 2025.02 | [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982) | Muon Scaling |
| 2025.05 | [Insights into DeepSeek-V3](https://arxiv.org/abs/2505.09343) | MLA、MoE、FP8、硬件协同设计、网络拓扑 |

---

# 二十四、课程推荐：论文分三级

## A 级：主干必讲

1. **DeepSeekMoE**
2. **DeepSeekMath**
3. **DeepSeek-V2**
4. **DeepSeek-V3**
5. **DeepSeek-R1**
6. **Native Sparse Attention**
7. **DeepSeek-V3.2**
8. **mHC**
9. **DeepSeek-V4**

这些论文基本构成 DeepSeek 的核心技术骨架。

---

## B 级：专题课程讲

- DeepSeek-Coder
- DeepSeek-Coder-V2
- DeepSeek-Prover
- DeepSeek-Prover-V1.5
- DeepSeek-Prover-V2
- DeepSeek-VL
- DeepSeek-VL2
- Janus
- Janus-Pro

---

## C 级：背景补充

- DeepSeek LLM
- Muon is Scalable for LLM Training
- Insights into DeepSeek-V3

这些更适合作为 Scaling、优化器、Infrastructure 等背景资料。

---

# 二十五、最终总结

DeepSeek 的技术演进可以浓缩成：

```text
做得大
DeepSeekMoE
     ↓
存得住
MLA
     ↓
训得省
FP8
     ↓
训得稳
Aux-loss-free
     ↓
学得更多 / 推得快
MTP
     ↓
会推理
GRPO + R1
     ↓
长上下文算得动
DSA
     ↓
百万上下文更经济
CSA + HCA
     ↓
深层模型信息传得更稳
mHC
     ↓
会思考、会调用工具、会执行任务
Agentic RL + DeepSeek-V4
```

所以 DeepSeek 真正的演进并不是简单：

```text
V1 → V2 → V3 → V4
```

而是几条互相协同的技术路线：

```text
MoE：
DeepSeekMoE → V2 → V3 → V4

Attention：
MLA → DSA → CSA / HCA
        ↑
      NSA Research

Training：
FP8 → Muon / FP4 QAT

Depth Scaling：
Residual → Hyper-Connections → mHC

Reasoning：
GRPO → R1-Zero → R1 → Scalable RL

Agent：
Reasoning → Tool Use → Agentic Task Synthesis

Code：
Coder → Coder-V2 → Agentic Coding

Math：
DeepSeekMath → Prover → R1

Multimodal：
VL → VL2
Janus → Janus-Pro
```

最终可以用一句话概括：

> **DeepSeekMoE 解决“模型太大算不起”；MLA 解决“KV 太大存不下”；FP8 与 Auxiliary-Loss-Free 解决“超大 MoE 难训练”；MTP 增加未来 Token 学习并可辅助推理加速；GRPO 与 R1 解决“Reasoning 怎么练出来”；DSA 解决“超长上下文 Attention 算不动”；CSA/HCA 进一步通过序列压缩与 Sparse/Dense Hybrid，把百万 Token 的计算与 KV 成本继续压低；mHC 则从模型深度方向改善跨层信息传递，最终让 DeepSeek 从大语言模型进一步走向长上下文 Reasoning Agent。**
