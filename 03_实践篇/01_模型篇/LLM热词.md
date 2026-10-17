# 模型相关

> **出处标注说明**：本文优先列出原始论文、正式标准和厂商官方技术博客。能够确认首次提出或首次发布的技术，会明确标注“提出”；没有公认单一出处的工程概念，则列出奠基工作或代表性资料，不将“代表性工作”等同于“首创”。

## Token

文本生成模型和嵌入模型都以一种称为 **Token** 的文本片段为基本单位处理文本。Token 通常对应文本中频繁出现的字符组合。

例如，字符串“ tokenization”可能会被拆分为“ token”和“ization”两个 Token；而像“ the”这样简短且常见的单词，通常会被视为一个完整的 Token。需要注意的是，在英文句子中，每个单词对应的第一个 Token 通常会包含单词前面的空格。

你可以把 Token 理解为“模型的阅读单位”。我们人类读中文是一个字一个字地看，读英文是一个词一个词地看。但模型既不按字、也不按词——它用一套自己的“拆字规则”（叫 Tokenizer）把文本切成大小不等的碎片，每个碎片就是一个 Token。

为什么不直接按字或按词切？因为模型需要在“词表大小”和“序列长度”之间取平衡：

- 每个汉字都是一个 Token，词表小、但序列长（模型要“补”更多步）。
- 每个词都是一个 Token，序列短、但词表会爆炸（中文词组太多了）。

所以实际用的是折中方案——**子词切分算法**（如 BPE、Unigram），高频词保留为整体，低频词拆成更小片段。

你可以把 Token 想象成乐高积木。常用的“积木块”比较大（比如“你好”可能是一个 Token），不常用的词会被拆成更小的基础块拼起来。

Token 不是“一个字”或“一个词”的严格等价物：

- 英文可能一个单词被拆成多个 Token。
- 中文可能一个词被拆成多个 Token，也可能多个字合并成一个 Token（取决于词频与词表）。

工程上通常用**经验估算**做容量规划，用**实际 API 返回的 usage**做精确计费与监控。

**Token、BPE 与 Unigram 的出处**

Token 是语言学、编译原理和自然语言处理长期使用的基础概念，并非由大语言模型或某一篇论文首次提出。现代 LLM 常用的子词 Tokenization，主要建立在以下工作之上：

| 技术 | 出处或代表资料 | 说明 |
| --- | --- | --- |
| BPE 原始算法 | Philip Gage，[*A New Algorithm for Data Compression*](https://www.derczynski.com/papers/archive/BPE_Gage.pdf)，1994 | 最初是数据压缩算法，并非为 NLP 提出 |
| BPE 子词切分 | Sennrich 等，[《Neural Machine Translation of Rare Words with Subword Units》](https://aclanthology.org/P16-1162/)，ACL 2016 | 将 BPE 系统用于神经机器翻译中的子词切分，推动其在 NLP 中普及 |
| Unigram 子词模型 | Taku Kudo，[《Subword Regularization》](https://aclanthology.org/P18-1007/)，ACL 2018 | 提出基于 Unigram Language Model 的子词切分与子词正则化 |
| SentencePiece | Kudo、Richardson，[《SentencePiece》](https://aclanthology.org/D18-2012/)，EMNLP 2018 | 从原始文本训练、与语言无关的子词 Tokenizer |

**Token 化过程示例**：

- 原文：`你好，我是小 G。`
- 切分：`[你好]` `[，]` `[我是]` `[小 G]` `[。]`
- 统计：原文 9 字符 → Token 数 5 个 → 压缩比约 1.8 倍

![Token 化过程示例](https://oss.javaguide.cn/github/javaguide/ai/llm/llm-token-process.png)

注意：实际 Token 切分由模型供应商的 Tokenizer 实现，不同供应商对相同文本可能产生不同的 Token 序列。

以openai的为例：

OpenAI 的大语言模型以 **Token** 为基本单位处理文本。Token 是从大量文本中归纳出的常见字符组合。模型通过学习 Token 之间的统计关系来理解语言，并根据已有的 Token 序列预测下一个 Token。[了解更多](https://platform.openai.com/docs/concepts#tokens)。

你可以使用下方工具，查看一段文本可能会被语言模型如何拆分为 Token，以及这段文本包含的 Token 总数。

![image-20260901094743532](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901094743532.png)

![image-20260901094759876](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901094759876.png)

## Embedding（嵌入向量）

Embedding（嵌入向量）是将概念转换为一组数字序列后得到的数值表示，使计算机能够更容易地理解不同概念之间的关系。我们的 Embedding 模型在三项标准基准测试中的表现均优于当时的领先模型，其中代码搜索性能相对提升了 20%。

Embedding 特别适合处理自然语言和代码。生成的向量可以方便地输入其他机器学习模型和算法，用于聚类、搜索等任务。

![image-20260901120253466](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901120253466.png)

数值上越相近的 Embedding，通常在语义上也越相似。例如，“canine companions say”（犬类伙伴会说）的嵌入向量，与“woof”（汪汪）的嵌入向量更加接近，而与“meow”（喵喵）的嵌入向量相距更远。

![image-20260901120353106](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901120353106.png)

embedding的可视化：[https://projector.tensorflow.org/](https://projector.tensorflow.org/)

**Embedding 的出处与代表工作**

Embedding/分布式表示不是由单一论文首次提出的。现代神经语言模型中的词向量通常追溯到以下工作：

| 技术 | 出处或代表资料 | 说明 |
| --- | --- | --- |
| 神经语言模型中的分布式词表示 | Bengio 等，[《A Neural Probabilistic Language Model》](https://www.jmlr.org/papers/v3/bengio03a.html)，JMLR 2003 | 在神经语言模型中联合学习词的连续向量表示 |
| Word2Vec | Mikolov 等，[《Efficient Estimation of Word Representations in Vector Space》](https://arxiv.org/abs/1301.3781)，2013 | 以 CBOW 和 Skip-gram 推动词向量大规模应用 |
| Sentence-BERT | Reimers、Gurevych，[《Sentence-BERT》](https://arxiv.org/abs/1908.10084)，EMNLP 2019 | 用孪生网络生成适合语义相似度与检索的句向量 |
| OpenAI Embeddings API | OpenAI，[《Introducing text and code embeddings》](https://openai.com/index/introducing-text-and-code-embeddings/)，2022 | 本节图片和示例文字的直接来源，也是 OpenAI Embeddings 产品发布页 |





## 采样参数

模型每一步会给词表中**每个**候选 Token 打一个分数（内部叫 **logits**），分数越高说明模型越觉得这个词应该出现在这里。

举个例子，假设模型正在补全“今天天气真__”，它可能给出这样的分数：

| 候选 Token | 原始分数（logit） |
| ---------- | ----------------- |
| 好         | 5.0               |
| 不错       | 3.2               |
| 棒         | 2.1               |
| 糟糕       | 0.5               |
| 紫色       | -8.0              |

原始分数不是概率，需要经过 **softmax** 才能得到概率分布。假设候选集合只有表中的五项，计算结果约为：

| 候选 Token | 概率     |
| ---------- | -------- |
| 好         | 81.21%   |
| 不错       | 13.42%   |
| 棒         | 4.47%    |
| 糟糕       | 0.90%    |
| 紫色       | < 0.001% |

最后，模型按这个概率分布“抽签”（采样），决定输出哪个 Token。

解码参数（Temperature、Top-p、Top-k 等）就是在这个“打分 → 概率 → 抽签”的过程中施加控制：

- Temperature：调整概率分布的“形状”，让高分选项更突出，或者让各选项更均匀。
- Top-p / Top-k：直接砍掉不靠谱的候选项，缩小“抽签池”。
- Penalty 系列：对已经出现过的词降分，防止“复读机”。

![Temperature 参数：控制模型输出的随机性](https://oss.javaguide.cn/github/javaguide/ai/llm/llm-temperature-params.png)

**采样策略的出处与代表工作**

Softmax 和 Temperature 早于 LLM 时代，属于概率建模中的通用方法；现代文本生成中较明确的代表性工作如下：

| 技术 | 出处或代表资料 | 说明 |
| --- | --- | --- |
| Softmax 概率建模 | Bengio 等，[《A Neural Probabilistic Language Model》](https://www.jmlr.org/papers/v3/bengio03a.html)，2003 | 神经语言模型中使用 Softmax 计算下一词概率的代表性早期工作 |
| Top-k Sampling | Fan 等，[《Hierarchical Neural Story Generation》](https://arxiv.org/abs/1805.04833)，2018 | 文本生成中系统使用 Top-k 随机采样的代表性工作 |
| Top-p / Nucleus Sampling | Holtzman 等，[《The Curious Case of Neural Text Degeneration》](https://arxiv.org/abs/1904.09751)，2019 | 提出 Nucleus Sampling，即今天常说的 Top-p |
| Temperature、Top-p、Penalty 参数 | [OpenAI API Reference](https://developers.openai.com/api/reference/resources/completions/methods/create/) | API 参数的官方定义；Presence/Frequency Penalty 属于产品级解码控制，并无公认的单一首篇论文 |

## Function Calling

目标：让模型能够使用新的功能和数据，从而更好地遵循指令并响应用户请求。

**函数调用（Function Calling）**，也称为**工具调用（Tool Calling）**，为 OpenAI 模型连接外部系统、访问训练数据之外的信息提供了一种强大且灵活的方式。

本指南将介绍如何把模型与你的应用程序所提供的数据和操作连接起来，包括：

- 使用通过 JSON Schema 定义的函数工具；
- 使用支持自由格式文本输入和输出的自定义工具。

**工具调用流程**

工具调用是应用程序与模型之间通过 OpenAI API 完成的一种多步骤交互过程。整个工具调用流程可以概括为五个主要步骤：

1. 向模型发送请求，并提供模型可以调用的工具；
2. 接收模型返回的工具调用请求；
3. 应用程序根据工具调用提供的参数，在本地执行相应代码；
4. 将工具的执行结果再次发送给模型；
5. 接收模型生成的最终回答，或者继续处理模型发起的新一轮工具调用。

![Function Calling 流程图](https://cdn.openai.com/API/docs/images/function-calling-diagram-steps.png)

**Function Calling 的出处**

OpenAI 于 **2023 年 6 月 13 日**正式发布名为 Function Calling 的 API 能力：[《Function calling and other API updates》](https://openai.com/index/function-calling-and-other-api-updates/)。当前官方文档将 Function Calling 也称为 Tool Calling：[Function Calling Guide](https://developers.openai.com/api/docs/guides/function-calling)。

需要区分的是，“让语言模型调用外部模块”的思想更早已经出现，例如 [MRKL Systems](https://arxiv.org/abs/2205.00445)（2022）和 [Toolformer](https://arxiv.org/abs/2302.04761)（2023）；但 **Function Calling 这一 API 名称及 JSON Schema 接口形式，通常追溯到 OpenAI 2023 年的产品发布**。

# 三个工程

## Prompt&Prompt Engineering

Prompt 是提供给大语言模型（LLM）的输入指令，可以包含任务、背景、约束和输出格式。

LLM 会根据当前上下文生成后续 Token。输入没有说明任务边界、所需信息和结果形式时，模型只能自行补全这些条件，输出便更容易偏题或编造。Prompt 的作用是把这部分条件交代清楚。

简单来说，Prompt 就是我们输入给大语言模型（LLM）的指令。从生成机制看，LLM 会基于上下文生成后续 Token；从应用效果看，它能表现出一定的语义理解和指令跟随能力。但这种能力依赖输入上下文，边界不清时就容易偏题或编造。

Prompt 要做的事，就是缩小模型的搜索范围。

指令越模糊，模型越容易乱猜。指令越结构化，输出就越容易被控制。

Prompt 写得好不好，不看长度，看它有没有把任务说清楚。

一个合格的 Prompt，通常要交代四件事：Role、Task、Context、Format。

**Prompt Engineering 的出处与代表工作**

Prompt Engineering 是随着预训练语言模型和 In-context Learning 逐步形成的工程方向，没有公认的单一发明者。

| 工作 | 出处 | 贡献 |
| --- | --- | --- |
| GPT-3 / In-context Learning | Brown 等，[《Language Models are Few-Shot Learners》](https://arxiv.org/abs/2005.14165)，NeurIPS 2020 | 展示通过自然语言指令和少量示例在上下文中完成新任务 |
| Prompt Programming | Reynolds、McDonell，[《Prompt Programming for Large Language Models》](https://arxiv.org/abs/2102.07350)，2021 | 较早系统讨论如何利用自然语言 Prompt 控制大模型 |
| Prompt-based Learning 综述 | Liu 等，[《Pre-train, Prompt, and Predict》](https://arxiv.org/abs/2107.13586)，2021/2023 | 系统整理 Prompt 模板、答案映射和 Prompt 学习方法 |
| Chain-of-Thought | Wei 等，[《Chain-of-Thought Prompting Elicits Reasoning in Large Language Models》](https://arxiv.org/abs/2201.11903)，NeurIPS 2022 | 提出通过中间推理步骤提升复杂推理任务表现 |

![image-20260901120427565](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901120427565.png)

| 要素              | 作用                             | 常见表述                                        |
| ----------------- | -------------------------------- | ----------------------------------------------- |
| Role（角色）      | 告诉模型该用哪个领域的知识和语气 | “你是一位 10 年经验的 Java 架构师”              |
| Task（任务）      | 说明要完成什么动作               | “请评审以下代码的性能问题”                      |
| Context（上下文） | 补充和任务相关的背景             | “当前线上 QPS 2000，响应时间超 500ms”           |
| Format（格式）    | 规定输出长什么样                 | “输出 JSON，包含 bottleneck、solution 两个字段” |



## 上下文窗口&上下文工程(Context Engineering)

**上下文窗口**是 LLM 的“工作记忆”（Working Memory）。它决定了模型在任何时刻可以处理或“记住”的文本量（以 Token 为单位）。

- 对话连续性：决定模型能进行多长的多轮对话而不遗忘早期细节。
- 单次处理能力：决定模型一次性能够处理的最大文档、代码库或数据样本。

“模型支持 128K/200K/1M”指的是一次调用里能放进模型的总 Token 上限。大多数模型的上下文窗口包含输入与输出的总和，但部分供应商（如 Google Gemini）对输入和输出分别设限，使用前请查阅具体 API 文档。

上下文窗口往往被隐形成本占用：

![上下文窗口（Context Window）= LLM 的「工作记忆」](https://oss.javaguide.cn/github/javaguide/ai/llm/llm-context-window.png)

- System Prompt：调节模型行为的系统指令（对用户隐藏，但占用窗口）。
- User Prompt：业务数据与指令。
- 多轮对话历史：过往的消息记录。
- RAG 检索片段：从外部知识库检索到的补充信息。
- 工具调用 Schema：函数定义与参数结构。
- 格式开销：特殊字符、换行符、Markdown 标记等。
- 模型生成的输出 Token：**输出也占用上下文窗口**。

因此，你真正能塞进 Prompt 的“有效业务内容”往往远小于标称上限。

**上下文工程(Context Engineering)**

上下文窗口能装下更多资料，不代表 Agent 会稳定利用这些资料。一次调用里混入过期状态、无关日志或几十个相似工具描述后，模型仍可能漏掉真正影响决策的条件。

Context Engineering 处理的就是调用前的信息组装：哪些规则进入消息，哪些证据按需检索，哪些工具在当前阶段可见，历史何时压缩，原始结果如何保留引用。长任务还要处理跨窗口的状态交接，避免摘要后丢失约束、版本号和未完成事项。

**同样的 Agent，为什么表现差这么多？**

![以电商售后为例图解同样的 Agent，为什么表现差这么多](https://oss.javaguide.cn/github/javaguide/ai/context-engineering/why-the-same-agent-performs-so-differently.png)

这里以电商售后为例。

G 友发来一句话： “MD，我上周买的耳机右耳没声音了，怎么处理？”

如果 Agent 拿到的上下文很少，它大概率会这么回：“抱歉给您带来不便。请问您购买的是哪款耳机？订单号是多少？能否描述一下具体故障表现？”

这句答话也问题不大，但对一个售后场景很让人恼火。它只会套流程问答，并不去主动整理信息。

我们换一个上文充足的改写看看效果。

在调用 LLM 之前，系统先把能查的信息都查出来：

- 查订单系统，定位到上周购买记录：索尼 WH-1000XM5，3 月 25 日下单
- 查保修状态，发现还在 7 天无理由退换期内
- 查历史工单，发现用户是老客户，之前没有售后纠纷
- 挂载 `create_return_order` 和 `check_inventory` 工具

那么 Agent 就可以这么回复：“您好，查到您 3 月 25 日购买的索尼 WH-1000XM5，目前还在退换期内。我这边直接帮您发起换货申请，仓库显示同款有库存，预计 2-3 天寄出新品。需要我帮你操作吗？”

这差距一下就出来了，后面这个回复是真的在解决问题，不是继续去反问用户。

当然，Agent 的很多失败确实和上下文有关，但上下文不是唯一原因。工具设计、任务拆解、状态管理、验证机制，这些通常要一起看。

不过有一点很确定：**上下文不够的时候，模型再强也只能靠猜；上下文给对了，中等水平的模型也能把任务做下去。**

**Context Engineering 到底在做什么？**

Context Engineering 做的事情，就是在有限 Token 窗口里，把最有用的信息喂给模型，把噪声挡在外面。它很容易和 Prompt Engineering 混在一起。

Prompt Engineering 更偏提示词怎么写，Context Engineering 管得更宽，包括规则、记忆、工具描述、会话状态、外部观察结果、Token 预算。

![Context Engineering 和 Prompt Engineering 差别](https://oss.javaguide.cn/github/javaguide/ai/context-engineering/context-engineering-vs-context-engineering-dimension-comparison.png)

**上下文窗口与 Context Engineering 的出处**

“上下文窗口”是序列模型可处理输入范围的通用概念，并非某家公司或某篇论文独创。Transformer 及 GPT 系列让它成为大模型的重要规格：[《Attention Is All You Need》](https://arxiv.org/abs/1706.03762)（2017）和 [《Language Models are Few-Shot Learners》](https://arxiv.org/abs/2005.14165)（2020）是代表性基础论文。

Context Engineering 是业界逐步形成的工程概念，没有公认的单一首篇论文。2025 年该术语在 Agent 工程中被广泛系统化，代表资料包括：

- LangChain：[《The rise of “context engineering”》](https://www.langchain.com/blog/the-rise-of-context-engineering)，2025 年 6 月；
- LangChain：[《Context Engineering for Agents》](https://www.langchain.com/blog/context-engineering-for-agents)，2025 年 7 月；
- Anthropic：[《Effective context engineering for AI agents》](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，2025 年 9 月。



## Harness Engineering

可以先用一个粗暴但好记的说法：Agent = Model + Harness。你不是模型，那你做的东西大概率就是 Harness。

这个说法有点绝对，但抓住了重点。Harness 指的是模型之外的整套系统：系统提示词、工具调用、文件系统、沙箱环境、编排逻辑、钩子中间件、反馈回路、约束机制。模型只提供推理和生成能力，Harness 把状态、工具、反馈、执行环境和安全边界串起来，Agent 才能真正开始干活。

LangChain 的 Vivek Trivedi 写过一篇《The Anatomy of an Agent Harness》，里面有个思路很值得记：先分清模型负责什么，再看剩下的系统该补什么。用这条线一切，很多 Agent 问题就不再是“模型行不行”，而是“系统有没有把模型需要的东西准备好”。

可以把模型想成 CPU，把 Harness 想成操作系统。CPU 再强，OS 如果天天崩，体验也不会好。你买了最新的 M5 芯片，但系统卡死、驱动乱飞，实际体验可能还不如旧芯片配一个稳定系统。

![Agent = Model + Harness](https://oss.javaguide.cn/github/javaguide/ai/harness/harness-agent-equals-model-harness-arch.png)

Prompt Engineering、Context Engineering、Harness Engineering 不太适合放在同一层比较。它们更像一层套一层，处理的问题范围越来越大。

![Harness 和 Prompt/Context Engineering 的关系](https://oss.javaguide.cn/github/javaguide/ai/harness/harness-engineering-layers-arch.png)

**Harness Engineering 的出处**

Harness 是软件工程中的既有词汇，Agent Harness/Agent Harness Engineering 也是在智能体产品实践中逐渐形成的工程术语，**目前没有公认的首篇学术论文或唯一提出者**。本节所采用的“Agent = Model + Harness”以及“模型之外的系统构成 Harness”的直接来源是 LangChain 的 Vivek Trivedi：[《The Anatomy of an Agent Harness》](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)。

因此课程中更适合表述为“LangChain 对 Agent Harness 的代表性工程总结”，而不是“LangChain 首次发明了 Harness”。

# RAG

## 什么是 RAG？

**RAG 的出处**

**RAG（Retrieval-Augmented Generation，检索增强生成）**这一术语来源于 Patrick Lewis 等人在 2020 年发表的论文：

> **《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》**
>  面向知识密集型 NLP 任务的检索增强生成

- 作者：Patrick Lewis、Ethan Perez、Aleksandra Piktus、Douwe Kiela 等
- 研究机构：以 Facebook AI Research（现 Meta AI）为主
- 首次提交：2020 年 5 月 22 日
- 正式发表：NeurIPS 2020
- [arXiv 论文页面](https://arxiv.org/abs/2005.11401)
- [论文 PDF](https://arxiv.org/pdf/2005.11401)
- [NeurIPS 官方页面](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)

在 RAG 论文之前，检索增强语言模型已有相关探索，例如 Google 的 [《REALM: Retrieval-Augmented Language Model Pre-Training》](https://arxiv.org/abs/2002.08909)（2020）。但 **Retrieval-Augmented Generation（RAG）这一名称及 RAG-Sequence、RAG-Token 两种建模方式，来自 Lewis 等人的 2020 年论文**。

**RAG（Retrieval-Augmented Generation，检索增强生成）** 就是把信息检索和大语言模型绑在一起用。系统先从知识库里检索出和当前问题相关的片段，知识库可以是数据库、文档集合，也可以是企业内部系统。然后把这些片段和原始问题一起喂给 LLM，让模型基于检索内容回答，而不是只靠训练时记住的知识。

![RAG 示意图](https://oss.javaguide.cn/github/javaguide/ai/rag/rag-simplified-architecture-diagram.jpeg)

LLM 训练数据再大，也绕不开几个问题。RAG 正好可以在这些地方进行弥补。

**第一是知识时效性。**

预训练模型的知识会停在训练数据截止时间点。训练后发生的新事件、新政策、新产品文档，模型默认是不知道的，除非通过联网、工具调用或外部知识注入来补。RAG 的做法是动态检索外部知识源，把最新的相关内容直接送给 LLM，让它不用只依赖参数里的旧知识。

**第二是私有数据访问。**

企业内部的产品文档、知识库、客户数据，不可能让公开 LLM 随便访问。RAG 在用户提问时只提取和问题相关的片段给 LLM，不需要暴露全部数据，模型也能基于企业自己的知识回答。

**第三是幻觉问题。**

LLM 编造事实这件事大家都遇到过。RAG 通过提供明确参考文本，让模型尽量基于证据回答，确实能降低幻觉概率。但别指望它彻底消除幻觉。检索错误、上下文噪声、引用错配、模型不遵循指令，都可能导致错误答案。生产级 RAG 通常还要配引用校验、答案评估、拒答机制和人工反馈闭环。

## 向量检索与向量数据库

RAG 的检索流程里，最基础的一步是：把用户问题和文档都变成向量，再用相似度搜索找到最相关的文档片段。

可以把它理解成这样：

1. 文档进入知识库后，先被切成 Chunk。
2. 每个 Chunk 通过 Embedding 模型转成一个向量。
3. 向量和原文、元数据一起写入向量数据库。
4. 用户提问时，问题也会被转成查询向量。
5. 向量数据库检索出最相似的 Top-K 文档向量。
6. 系统把这些文档片段放进 Prompt，交给 LLM 生成答案。

![Embedding 和向量检索是什么关系？](https://oss.javaguide.cn/github/javaguide/ai/rag/rag-embedding-vector-retrieval.png)

Embedding 负责把文本变成可比较的向量，向量检索据此查找语义接近的内容。向量检索只是 RAG 的一种实现；RAG 还可以使用 BM25、SQL、知识图谱、搜索 API 或其他业务查询来取得外部证据。

在小规模 Demo 里，几千条文档向量可以直接放在内存里暴力搜索。但真实 RAG 系统里，文档量很快会到百万级、千万级，甚至更大。

向量数据库解决的不是“存一个数组”这么简单，而是几个工程问题：

**向量检索与向量数据库的出处和代表工作**

“向量数据库”是多种向量表示、相似度计算和近似最近邻索引技术工程化集成后的产品形态，并没有一篇公认的“向量数据库起源论文”。相关技术主线如下：

| 技术 | 出处或代表资料 | 贡献 |
| --- | --- | --- |
| 稠密语义检索 DPR | Karpukhin 等，[《Dense Passage Retrieval for Open-Domain Question Answering》](https://arxiv.org/abs/2004.04906)，EMNLP 2020 | 使用双编码器生成问题和文档向量，是现代 RAG 稠密检索的重要基础 |
| BM25 | Robertson 等，《Okapi at TREC-3》，1994；综述见 [《The Probabilistic Relevance Framework: BM25 and Beyond》](https://dl.acm.org/doi/10.1561/1500000019)，2009 | 经典稀疏关键词检索方法 |
| HNSW | Malkov、Yashunin，[《Efficient and Robust Approximate Nearest Neighbor Search Using HNSW》](https://arxiv.org/abs/1603.09320)，2016/2018 | 多层图结构的近似最近邻检索，广泛用于向量数据库索引 |
| FAISS | Johnson、Douze、Jégou，[《Billion-scale Similarity Search with GPUs》](https://arxiv.org/abs/1702.08734)，2017 | 推动十亿级向量相似度搜索和 GPU 加速 |
| RAG 中的检索—生成结合 | Lewis 等，[《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》](https://arxiv.org/abs/2005.11401)，2020 | 将稠密向量检索器与生成模型端到端结合 |

![RAG 场景为什么需要向量数据库？](https://oss.javaguide.cn/github/javaguide/ai/rag/rag-why-need-vector-store.png)

# Agent

## 什么是 Agent？

如果你看过 LangChain 的 Agent 源码，会发现它的核心并不神秘，很多时候就是一个 while 循环。

AI Agent 可以理解为一个能感知环境、做决策、执行动作的软件系统。LLM 负责理解和决策，工具负责执行，记忆负责保存上下文和历史经验。

它和普通聊天机器人的差别在于：Agent 不只是回复消息，它会在动态环境里持续观察、判断、执行，直到任务结束。

一般可以用这个公式概括：**Agent = LLM + Planning + Memory + Tools** 。

![AI Agent 核心架构](https://oss.javaguide.cn/github/javaguide/ai/agent/agent-core-arch.png)

**AI Agent 与 LLM Agent 的出处**

Agent 是人工智能中的经典研究方向，远早于大语言模型。现代 LLM Agent 则在 2022—2023 年由多项工作共同推动形成，并不存在唯一的“LLM Agent 首篇论文”。

| 阶段 | 出处或代表资料 | 贡献 |
| --- | --- | --- |
| 经典智能体理论 | Wooldridge、Jennings，[《Intelligent Agents: Theory and Practice》](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95.pdf)，1995 | 系统讨论 Agent 的自主性、反应性、主动性和社会能力 |
| LLM 连接外部模块 | Karpas 等，[《MRKL Systems》](https://arxiv.org/abs/2205.00445)，2022 | 将 LLM 与外部知识、计算和离散推理模块组合 |
| 推理—行动闭环 | Yao 等，[《ReAct》](https://arxiv.org/abs/2210.03629)，2022/ICLR 2023 | 建立 Reasoning、Acting 和 Observation 交替运行的核心范式 |
| 记忆—反思—规划 | Park 等，[《Generative Agents》](https://arxiv.org/abs/2304.03442)，2023 | 构建包含记忆检索、反思和规划的生成式智能体架构 |
| 工程架构总结 | Lilian Weng，[《LLM Powered Autonomous Agents》](https://lilianweng.github.io/posts/2023-06-23-agent/)，2023 | 将 LLM Agent 系统概括为 LLM、Planning、Memory 和 Tool Use |
| 领域系统化 | Wang 等，[《A Survey on Large Language Model based Autonomous Agents》](https://arxiv.org/abs/2308.11432)，2023 | 系统梳理 LLM 自主智能体的构建、应用与评测 |

**推理与规划（Reasoning / Planning）**：用 LLM 分析当前任务状态，拆目标，决定下一步怎么做。Chain-of-Thought（CoT）提示技术可以让模型逐步推理，减少直接拍脑袋给答案的概率。

记忆分两层。短期记忆通常是上下文历史，用来保持对话连续性；长期记忆一般是外部知识库，比如向量数据库或知识图谱。短期记忆解决“刚才说过什么”，长期记忆解决“过去积累了什么”。

**Tools（工具）**：让 LLM 能真正操作外部世界，比如查数据、调 API、读文件、执行代码。没有工具，Agent 很多时候只能停留在“建议你怎么做”。

工具执行后会返回结果，Agent 把这些结果放回上下文，再进入下一轮推理。这个反馈闭环就是 Observation（观察），也是 Agent Loop 能转起来的关键。



## Agent Loop

Agent Loop 是 Agent 真正跑起来的地方。

它每一轮大概做三件事：让 LLM 推理，调用工具，把工具结果写回上下文。一直循环，直到任务完成或者触发停止条件。

![Agent Loop 工作流程](https://oss.javaguide.cn/github/javaguide/ai/agent/agent-loop-flow.png)

流程大概是这样：

1. 初始化时加载 System Prompt、可用工具列表、用户初始请求
2. 循环迭代——读取上下文，LLM 推理决定下一步（调用工具还是直接回复），触发并执行工具，捕获返回结果追加到上下文
3. LLM 判断任务完成，不再调用工具时退出循环
4. 安全兜底——防止死循环，设置最大迭代轮次上限（一般 10 到 20 轮）或 Token 消耗阈值

工程难点不在 while 循环本身，而在上下文管理。

任务越跑越久，上下文会越来越长。关键信息被稀释后，模型就容易跑偏。这也是 Context Engineering 要解决的问题。

LangChain、LlamaIndex、Spring AI 这些框架都对 Agent Loop 做了封装，但底层思路差不多。

**Agent Loop 的出处**

“感知—决策—行动”的循环来自经典 Agent 理论，而现代 LLM Agent 中“模型生成动作—环境返回观察—模型继续决策”的闭环，最具代表性的直接来源是 [《ReAct: Synergizing Reasoning and Acting in Language Models》](https://arxiv.org/abs/2210.03629)（2022）。论文将推理轨迹与面向环境的动作交替生成，并利用 Observation 更新后续决策。

因此，Agent Loop 不是 LangChain 等框架发明的；这些框架主要把这一循环工程化，补上停止条件、工具执行、异常处理和状态管理。

## ReAct

ReAct 是 Reasoning + Acting，由 Shunyu Yao 等人在 2022 年提出，论文是[《ReAct: Synergizing Reasoning and Acting in Language Models》](https://react-lm.github.io/)。

**ReAct 的正式出处**

- 论文：[《ReAct: Synergizing Reasoning and Acting in Language Models》](https://arxiv.org/abs/2210.03629)；
- 首次提交：2022 年 10 月；
- 正式发表：ICLR 2023；
- 作者项目页：[ReAct Project](https://react-lm.github.io/)；
- Google Research 解读：[ReAct: Synergizing Reasoning and Acting in Language Models](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)。

LangChain、LlamaIndex、AgentScope 这类框架里的 Agent 模块，很多都能看到这个范式的影子。

它的思路很直观：模型先推理一步，拿到外部环境反馈，再推理下一步，交替进行。

LLM 自己容易缺少实时信息，也容易幻觉。ReAct 就让它“走一步看一步”，每一步都根据工具返回结果继续判断。

![ReAct-LLM](https://oss.javaguide.cn/github/javaguide/ai/agent/ReAct-LLM.png)

ReAct 落地时一般需要这几个组件配合：

1. 历史上下文，保存推理步骤、执行动作、反馈观察
2. 实时环境输入，比如系统告警、用户反馈等外部变量
3. LLM 推理模块：负责逻辑分析和下一步规划
4. 工具集与技能库，包括原子工具和 Skills
5. 反馈观察机制，采集工具响应并追加回上下文

![ReAct 模式流程](https://oss.javaguide.cn/github/javaguide/ai/agent/agent-react-flow.png)

ReAct 的好处是能减少幻觉，复杂任务成功率更高，也比较容易解释每一步为什么这么做。

代价也明显：多轮迭代会增加响应延迟，效果还很依赖工具和 Skills 的质量。

## Memory

![image-20260901120506917](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901120506917.png)

记忆系统通常分两层：短期记忆和长期记忆。短期记忆是 Session 级的，服务当前任务；长期记忆是跨 Session 的，负责把用户偏好、历史决策、过往经验沉淀下来。两者在物理和逻辑上都应该分开，不要混成一锅。

![AI Agent 记忆系统架构](https://oss.javaguide.cn/github/javaguide/ai/agent/agent-memory-arch.png)

按功能目的看，Agent 记忆可以分成三类。

| 功能类型 | 核心问题           | 存储内容                     | 典型场景               |
| -------- | ------------------ | ---------------------------- | ---------------------- |
| 事实记忆 | 智能体知道什么     | 用户偏好、环境状态、显式事实 | 记住用户的技术栈偏好   |
| 经验记忆 | 智能体如何改进     | 过往轨迹、成败教训、策略知识 | 从失败的代码审查中学习 |
| 工作记忆 | 智能体当前思考什么 | 当前推理上下文、任务进展     | 多步推理中的中间状态   |

长期记忆和 RAG 技术上很像，都会用向量库和语义检索。但它们服务的对象不一样。

RAG 挂载的是可检索知识源，比如公司规章、产品文档、实时数据库查询结果。它既可以服务共享知识库，也可以根据用户、租户、角色和会话执行权限过滤或个性化检索。RAG 与长期记忆的主要区别在数据来源和生命周期：前者检索外部知识，后者保存交互中形成、需要跨会话复用的信息。

长期记忆管理的是 Agent 与特定用户交互中动态沉淀的个性化经验，比如用户偏好、习惯、历史决策、专属背景。它高度个性化，因人而异。

![image-20260901120519315](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901120519315.png)

**Agent Memory 的出处与代表工作**

短期记忆、工作记忆和长期记忆首先是认知心理学与经典计算机体系中的既有概念；LLM Agent Memory 没有唯一的起源论文。以下工作对现代 Agent 记忆架构影响较大：

| 工作 | 出处 | 贡献 |
| --- | --- | --- |
| Generative Agents | Park 等，[《Generative Agents: Interactive Simulacra of Human Behavior》](https://arxiv.org/abs/2304.03442)，2023 | 提出 Memory Stream，并通过相关性、时近性和重要性检索记忆，支持反思和规划 |
| CoALA | Sumers 等，[《Cognitive Architectures for Language Agents》](https://arxiv.org/abs/2309.02427)，2023 | 从工作记忆、情景记忆、语义记忆和程序记忆等角度统一分析语言智能体 |
| MemGPT | Packer 等，[《MemGPT: Towards LLMs as Operating Systems》](https://arxiv.org/abs/2310.08560)，2023 | 用分层存储和上下文换入换出管理有限上下文窗口 |

本文“事实记忆、经验记忆、工作记忆”的三分法属于面向课程理解的**功能性归纳**，并非直接照搬某一篇论文中的标准分类。若需要论文框架，应优先引用 CoALA 的记忆分类。

## MCP

MCP 全称是 Model Context Protocol，中文一般叫“模型上下文协议”。

把 MCP 的全称拆开来看，其实就很清晰了：

- Model：面向大模型应用；
- Context：把外部上下文、工具和数据源带给模型；
- Protocol：用一套标准协议把交互方式定下来。

不过，也不要把 MCP 理解成给模型加插件这么简单。之前在星球群里看大家讨论 MCP 的时候，有不少同学都是这样认为的。

更准确一点说，MCP 是 **MCP Client 和 MCP Server 之间的通信协议**。Host 负责承载用户交互和模型调用，Client 负责和 Server 说话，Server 负责把具体能力暴露出来。

![MCP 图解](https://oss.javaguide.cn/github/javaguide/ai/skills/mcp-simple-diagram.png)

不少读者朋友第一次了解 MCP，都会将它和 Function Calling、Agent、Skills 混在一起。

这几个确实经常一起出现，但不在同一层。

Function Calling 解决的是：**模型怎么表达自己想调工具。**

MCP 解决的是：**这个工具从哪里来，怎么被宿主发现，怎么真正连到后端服务。**

Agent 再往上一层，关注的是：**任务怎么一步步做完。**

![FC/MCP/Agent 三层关系图](https://oss.javaguide.cn/github/javaguide/ai/skills/mcp-fc-agent-layer.png)

**MCP 的出处**

MCP 由 Anthropic 于 **2024 年 11 月 25 日**正式提出并开源：

- 官方发布：[《Introducing the Model Context Protocol》](https://www.anthropic.com/news/model-context-protocol)；
- 官方规范：[Model Context Protocol Specification](https://modelcontextprotocol.io/specification/latest)；
- 官方文档：[Model Context Protocol Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)。

因此可以准确表述为：**MCP 是 Anthropic 提出的一套连接 AI 应用与外部数据源、工具和工作流的开放协议。**

## Skills

Agent Skills 是一种轻量级的开放格式，用于通过专业知识和工作流程扩展 AI 智能体的能力。

从结构上看，一个 Skill 本质上是一个包含 **`SKILL.md`** 文件的文件夹。该文件至少要包含 **`name`** 和 **`description`** 等元数据，以及指导智能体如何完成特定任务的操作说明。

Skill 还可以包含脚本、参考资料、模板及其他相关资源。

```text
my-skill/
├── SKILL.md          # 必需：元数据和操作说明
├── scripts/          # 可选：可执行代码
├── references/       # 可选：参考文档
├── assets/           # 可选：模板和资源
└── ...               # 其他文件或目录
```

为什么需要 Agent Skills？

智能体的能力正在不断增强，但在执行实际任务时，往往缺少可靠完成工作所需的专业知识、操作流程和具体上下文。

Skills 将操作性知识，以及企业、团队和用户特有的上下文，封装成可移植、可进行版本管理的文件夹，并由智能体在需要时按需加载。它可以为智能体带来以下能力：

- **领域专业知识**：将法律审查流程、数据分析管线、演示文稿排版规范等专业知识，沉淀为可重复使用的操作说明和配套资源。
- **可重复的工作流程**：将复杂的多步骤任务转化为一致、规范且可审计的执行流程。
- **跨产品复用**：一个 Skill 只需编写一次，便可在任何兼容 Agent Skills 的智能体产品中使用。

Agent Skills 如何工作？

智能体通过**渐进式披露（Progressive Disclosure）**机制加载 Skills，整个过程分为三个阶段：

1. **发现（Discovery）**
   智能体启动时，只加载每个 Skill 的名称和描述。这些信息足以帮助智能体判断某个 Skill 可能在什么情况下适用。
2. **激活（Activation）**
   当用户任务与某个 Skill 的描述相匹配时，智能体会读取完整的 **`SKILL.md`** 文件，并将其中的操作说明加载到上下文中。
3. **执行（Execution）**
   智能体按照 Skill 中的说明执行任务，并根据需要运行其中附带的代码，或者加载其引用的文件和资料。

只有在任务确实需要某个 Skill 时，完整的操作说明才会被加载。因此，智能体可以同时配置大量 Skills，而只占用较少的上下文空间。放在一个真实链路里，大概是这样：

![image-20260901120534221](C:\Users\KeychronK3\AppData\Roaming\Typora\typora-user-images\image-20260901120534221.png)

1. 用户提出任务（Prompt）
2. 宿主把可用 Skills 的简短描述放进上下文（Skill 元数据）
3. 模型判断当前任务命中了某个 Skill（Skill 路由）
4. 宿主再把完整 `SKILL.md` 加载进来（延迟加载）
5. 模型按照 Skill 里的流程去调工具、读资料、写结果（执行）

**Agent Skills 的出处**

Agent Skills 最早由 Anthropic 在 Claude 产品体系中推出，后来开放为跨平台标准：

| 时间 | 出处 | 事件 |
| --- | --- | --- |
| 2025 年 10 月 16 日 | Anthropic，[《Introducing Agent Skills》](https://www.anthropic.com/news/skills) | 正式发布 Agent Skills；Skill 以包含说明、脚本和资源的文件夹形式扩展 Claude |
| 2025 年 12 月 18 日 | [Agent Skills 开放标准](https://agentskills.io/home) | Anthropic 将 Agent Skills 发布为跨平台开放标准 |
| 后续采用 | [OpenAI Skills API](https://developers.openai.com/api/docs/guides/tools-skills) | OpenAI 等平台采用与开放 Agent Skills 标准兼容的 Skill 机制 |

Skill 的格式规范见 [Agent Skills Specification](https://agentskills.io/specification)。其中 `SKILL.md`、`name`、`description` 以及渐进式披露机制均可在官方规范和 Anthropic 发布文章中找到依据。
