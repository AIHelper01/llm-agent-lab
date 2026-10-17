# 📚 **AI News Radar 记忆系统详细说明** (v2.0)



## 双源记忆架构

OpenClaw 的记忆系统采用了一个**双源记忆架构**的设计，其将记忆整体分为了两类：每日日志（动态记忆）和长期记忆（静态记忆）。

| **记忆类型** | **存储格式**  | **存储路径**                                   | **产生方式**        |
| ------------ | ------------- | ---------------------------------------------- | ------------------- |
| 动态记忆     | JSONL 文件    | ~/.openclaw/agents/{agentId}/sessions/*.jsonl  | 自动记录            |
| 静态记忆     | Markdown 文件 | ~/.openclaw/workspace/MEMORY.md 和 memory/*.md | 手动创建 + 自动生成 |

从直觉上看，这是符合人类大脑的记忆机制的，人的记忆也是由一个个重点片段组成的，我们能记住的也只是某个特定的时刻、某件具体的事件，把这些片段串联起来才形成了人类所谓的记忆，至于每天发生的琐事，终究会随着时间而被淡忘。因此，此种记忆机制也可以说是实现了工程学和生物学上的高度统一。



###  **动态记忆的产生**

每次用户与 Agent 交互时，系统会自动将对话内容追加到 JSONL 格式的会话日志文件中，这是最原始的、未经处理过的记忆，存储位置如下：



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr7kNaPyp6LnzKjL0BOiaf5BHa7NPIsdV48G7CB8IiaHobm1icPA77mtKknasEM0p6HQoMPoyQo35Xib4MlNOUibQ9iaEh4rtAFdoI04o/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)



动态记忆的 JOSNL 格式示例如下：

```
{"type":"message","message":{"role":"user","content":"帮我写一个 Python 爬虫"}}{"type":"message","message":{"role":"assistant","content":"好的，我来帮你写..."}}{"type":"tool_call","tool":"bash","input":{"command":"python crawler.py"}}
```



代码实现方式如下：

```
export async function buildSessionEntry(absPath: string): Promise<SessionFileEntry | null> {
  // 读取 JSONL 文件
  const raw = await fs.readFile(absPath, "utf-8");
  const lines = raw.split("\n");
  const collected: string[] = [];

  for (const line of lines) {
    if (!line.trim()) continue; // 跳过空行
    
    const record = JSON.parse(line);
    // 假设记录结构中有 messages 数组
    for (const message of record.messages) {
      // 只提取 user 和 assistant 的消息
      if (message.role === "user" || message.role === "assistant") {
        const label = message.role === "user" ? "User" : "Assistant";
        collected.push(`${label}: ${message.text}`);
      }
    }
  }

  const content = collected.join("\n");
  return {
    path: sessionPathForFile(absPath),
    hash: hashText(content),
    content, // "User: 帮我写... \n Assistant: 好的..."
  };
}
```



###  **静态记忆的产生**



静态记忆是整个系统的长期记忆，可以理解成是在短期的琐碎记忆中提炼出来的需要系统重点记住的内容，比如用户的性格、身份信息、回答偏好等，其文件存储结构如下：



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr4cIxSIpKXqVQ8omuLnpIhkicfp4xic6gkEwIjYxKeX86VBbCM0PEQzPaSnjG7DsIgpbptnUgSeicKAvZR20MySlBeOF5maI8WkRg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)



静态记忆的产生途径分为以下三种：

- 途径一：用户手动创建。用户可以直接编辑 MEMORY.md 文件，写入需要 Agent 长期记住的信息，比如：“你要称呼我为老板”、“我喜欢简洁的回复”等。；
- 途径二：session-memory Hook 自动转换。当用户执行 /new 命令重置会话时，系统会触发 session-memory Hook，自动将上一个会话的关键内容转换为 Markdown 文件。大致的流程为：
  - 读取会话日志：从 JSONL 文件中提取最近 N 条（默认 15 条）user/assistant 消息；
- 生成语义化文件名：使用 LLM 根据对话内容生成描述性 slug（如 api-design、bug-fix）；
- 写入 Markdown 文件：生成 memory/YYYY-MM-DD-{slug}.md 文件。
- 途径三：Memory Flush 自动写入（类似于记忆刷新）。这是一个非常关键的自动化机制，当会话上下文接近 token 限制时，系统会在压缩（compaction）前触发一个特殊的 Agent 回合，在该回合中，Agent 被明确指示：将需要持久保存的重要信息写入 memory/YYYY-MM-DD.md 文件。



| **特性**       | **MEMORY.md**                  | **memory/\*.md**       |
| -------------- | ------------------------------ | ---------------------- |
| **用途**       | 核心长期记忆                   | 按时间组织的会话记忆   |
| **内容类型**   | 用户偏好、重要信息、工作流程等 | 具体会话的摘要和细节   |
| **更新方式**   | 用户手动维护为主               | 系统自动生成为主       |
| **命名规则**   | 固定为 MEMORY.md               | YYYY-MM-DD(-{slug}).md |
| **检索优先级** | 平等，由向量相似度决定         |                        |



整个静态记忆系统的设计核心在于途径三，往往“健忘”的问题就出在这一步，即如何进行历史对话信息的压缩。其实此处OpenClaw 的处理方法比较粗暴，是使用 LLM 直接对历史对话信息进行处理。



首先，通过 Memory Flush 进行一次记忆筛选，让 Agent 自己判断什么是"durable memories"（持久记忆），代码如下：

```
export const DEFAULT_MEMORY_FLUSH_PROMPT = [
  "Pre-compaction memory flush.",
  "Store durable memories now (use memory/YYYY-MM-DD.md; create memory/ if needed).",
  `If nothing to store, reply with ${SILENT_REPLY_TOKEN}.`,
].join(" ");
```



然后，最终压缩就是再使用 LLM 对历史消息进行有损摘要，这里的默认指令只要求保留 “decisions, TODOs, open questions, constraints”，不保留具体数值、时间点等细节，代码如下：

```
const MERGE_SUMMARIES_INSTRUCTIONS = 
  "Merge these partial summaries into a single cohesive summary. Preserve decisions, " +
  "TODOs, open questions, and any constraints.";
```



这正是 OpenClaw 在记忆上的平衡，通过把历史会话记录（JSONL 格式）压缩成记忆（Markdown 格式），来避免上下文溢出的问题，赋予系统记忆的能力，但与此同时带来的问题也显而易见，在进行压缩时难免会有信息的流失，这在大多数场景下是合理的，但对于"具体几点"这类精确信息确实是弱点。但并这不是 bug，而是在"长期记忆完整性"和"系统效率/成本"之间的设计取舍。用户如果有重要的精确信息，可以主动要求 Agent 记录到长期记忆中。



好了，现在解释了第一个问题，OpenClaw 到底记住的是什么信息，下面我们来看这些所谓的“记忆”是怎么在需要的时候被“记起来”的。







## **记忆信息的检索与调用**



当产生并保存一个记忆文件（.md）时，后台会自动触发如下的索引构建流程，并在需要时进行检索：



![图片](https://mmbiz.qpic.cn/mmbiz_png/ZRhjO8xAWr7bcFQibRuTSrnqtxuLRZMBpDmmtYLfTQe9mT9Q2ACmweibEIE0ncmZReWia9zKu86xic5pS5G0jQOukc6lS1zlu26D1HH6iaiaMbtH4/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)



###   **索引构建**



默认情况下，只有 Markdown 文件会被索引，而 JSONL 会话日志不会被索引。Markdown 文件首先被分块（默认每个块包含 400 tokens，相邻块重叠 80 tokens），而后每个块同时生成向量 Embedding（支持三种，OpenAI、Gemini、本地） 和文本 Token，分别存入 sqlite-vec 和 FTS5 索引，这两个都是 SQLite 扩展，意味着整个系统只依赖一个轻量级数据库文件，不需要部署 ES 或者 Milvus。SQLite 数据库的核心 Schema 如下所示：

```
-- 文件元数据
CREATE TABLE files (
  path TEXT PRIMARY KEY,      -- 'memory/projects.md'
  source TEXT NOT NULL,       -- 'memory' | 'sessions'
  hash TEXT NOT NULL,         -- SHA256 用于增量更新
  mtime INTEGER NOT NULL,
  size INTEGER NOT NULL
);

-- 文本块（带 embedding）
CREATE TABLE chunks (
  id TEXT PRIMARY KEY,        -- UUID
  path TEXT NOT NULL,         -- 来源文件
  source TEXT NOT NULL,       -- 'memory' | 'sessions'
  start_line INTEGER,
  end_line INTEGER,
  hash TEXT NOT NULL,
  model TEXT NOT NULL,        -- 'text-embedding-3-small'
  text TEXT NOT NULL,         -- 原文
  embedding TEXT NOT NULL,    -- JSON 数组 [0.1, 0.2, ...]
  updated_at INTEGER
);

-- 向量索引（sqlite-vec 扩展）
CREATE VIRTUAL TABLE chunks_vec USING vec0(...);

-- 全文索引（FTS5）
CREATE VIRTUAL TABLE chunks_fts USING fts5(
  path,
  source, 
  model,
  text,
  tokenize='porter unicode61'
);
```



对于具体的记忆索引实现流程，在附录一中进行了详细阐述。



###   **记忆搜索**



OpenClaw 采用关键词 + 向量的混合加权搜索，结合了两者的优势。当 Agent 需要搜索记忆时，系统会启动两个搜索引擎：

- 向量搜索：基于语义相似度。把之前向量化之后的内容通过计算余弦相似度找到意思相近的内容，这个直接依赖 sqlite-vec 的扩展实现，无需外部向量数据库；
- BM25 关键词搜索：基于词频统计。使用 SQLite 内置的 FTS5 全文检索引擎，找到包含精确关键词的内容。



混合检索的代码实现方式如下：

```
async search(query: string, opts?: { maxResults?: number; minScore?: number }) {
  const cleaned = this.cleanQuery(query);
  const maxResults = opts?.maxResults ?? 20;
  const minScore = opts?.minScore ?? 0.2;
  const hybrid = { enabled: true };

  // 获取候选片段
  const candidates = await this.getCandidates(cleaned);

  // 1. 关键词搜索 (BM25)
  const keywordResults = hybrid.enabled
    ? await this.searchKeyword(cleaned, candidates)
    : [];

  // 2. 向量搜索
  const queryVec = await this.embedQueryWithTimeout(cleaned);
  const vectorResults = await this.searchVector(queryVec, candidates);

  // 3. 混合排序
  if (!hybrid.enabled) {
    return vectorResults
      .filter(r => r.score >= minScore)
      .slice(0, maxResults);
  }

  const merged = this.mergeHybridResults({
    vector: vectorResults,
    keyword: keywordResults,
    vectorWeight: 0.7,  // 向量权重
    textWeight: 0.3,    // 关键词权重
  });

  return merged
    .filter(r => r.score >= minScore)
    .slice(0, maxResults);
}
```



###   **加权融合**



两个引擎的搜索结果按照 70:30 的权重合并，最终得分 = 0.7 向量相似度 + 0.3 BM25 得分，且只有得分超过 0.35 的结果才会被返回。混合排序实现方式如下所示：



```
const merged = Array.from(byId.values()).map((entry) => {
  // 最终得分 = 向量权重 × 向量相似度 + 关键词权重 × BM25 得分
  const score = vectorWeight * entry.vectorScore + textWeight * entry.textScore;
  return {
    path: entry.path,
    startLine: entry.startLine,
    endLine: entry.endLine,
    score,
    snippet: entry.snippet,
    source: entry.source
  };
});

return merged.sort((a, b) => b.score - a.score);
```



系统默认的 70% 和 30% 的比例来自与内部测试的结果，在其模拟进行的 1000 次复杂查询测试中，纯向量搜索的召回率为 76%，纯 BM25 搜索的召回率为 68%，而 70/30 的混合策略召回率达到 89%。



##   **Agent 交互**



基于上述介绍的记忆系统架构，在实际使用时，AI Agent 则是通过两个接口实现与整个记忆系统的交互。



### **两个核心工具**



- memory_search：语义搜索

此工具用来调用上述的记忆检索功能，工具的定义如下：

```
return {
  label: "Memory Search",
  name: "memory_search",
  description: "Mandatory recall step: semantically search MEMORY.md + memory/*.md (and optional session transcripts) before answering questions about prior work, decisions, dates, people, preferences, or todos; returns top snippets with path + lines.",
  parameters: MemorySearchSchema,
  execute: async (_toolCallId, params) => {
    // 搜索查询文本（必填）
    const query = readStringParam(params, "query", { required: true });
    // 返回结果数量（默认 6）
    const maxResults = readNumberParam(params, "maxResults") ?? 6;
    // 最低相关度阈值（默认 0.35）
    const minScore = readNumberParam(params, "minScore") ?? 0.35;
    
    const { manager, error } = await getMemorySearchManager({
      cfg,
      agentId,
    });
    
    if (error) {
      return errorResult(error);
    }
    
    // 执行搜索
    const results = await manager.search(query, {
      maxResults,
      minScore,
      sessionKey: options?.agentSessionKey,
    });
    
    return jsonResult({
      results,
      provider: status.provider,
      model: status.model,
      fallback: status.fallback,
    });
  },
};
```



返回格式如下：

```
{
  "results": [
    {
      "path": "memory/2026-01-10.md",
      "startLine": 15,
      "endLine": 20,
      "score": 0.85,
      "snippet": "用户提到喜欢蓝色，特别是天空蓝...",
      "source": "memory"
    },
    {
      "path": "MEMORY.md",
      "startLine": 5,
      "endLine": 8,
      "score": 0.72,
      "snippet": "颜色偏好：蓝色系...",
      "source": "memory"
    }
  ],
  "provider": "openai",
  "model": "text-embedding-3-small"
}
```



- memory_get：精确读取

此工具用来精准读取记忆文件，工具的定义如下：

```
return {
  label: "Memory Get",
  name: "memory_get",
  description: "Safe snippet read from MEMORY.md, memory/*.md, or configured memorySearch.extraPaths with optional from/lines; use after memory_search to pull only the needed lines and keep context small.",
  parameters: MemoryGetSchema,
  execute: async (_toolCallId, params) => {
    // 文件相对路径（如 memory/2026-01-10.md）
    const relPath = readStringParam(params, "path", { required: true });
    // 起始行号
    const from = readNumberParam(params, "from", { integer: true });
    // 读取行数
    const lines = readNumberParam(params, "lines", { integer: true });
    
    const { manager, error } = await getMemorySearchManager({
      cfg,
      agentId,
    });
    
    if (error) {
      return errorResult(error);
    }
    
    // 读取文件
    const result = await manager.readFile({
      relPath,
      from: from ?? undefined,
      lines: lines ?? undefined,
    });
    
    return jsonResult(result);
  },
};
```



返回的格式如下：

```
{
  "text": "用户提到喜欢蓝色，特别是天空蓝。\n在选择UI时偏好冷色调。\n...",
  "path": "memory/2026-01-10.md"
}
```



### **Agent 记忆交互的指令约束**



Agent 被明确指示必须在特定场景下使用记忆工具：

```
return [
  "## Memory Recall",
  "Before answering anything about prior work, decisions, dates, people, preferences, or todos: run memory_search on MEMORY.md + memory/*.md; then use memory_get to pull only the needed lines. If low confidence after search, say you checked.",
  "",
];
```



### **Agent 主动写入记忆**



在 OpenClaw 的交互中，Agent 也可以主动写入记忆文件，使用标准的文件操作工具。比如，当 Agent 判断需要记住某些信息时，会使用 exec 或 write 工具写入对应的 memory/YYYY-MM-DD.md 文件，例如：

```
exec(command = "echo '## 用户偏好\n- 喜欢蓝色' >> memory/2026-02-05.md");
write(path = "memory/2026-02-05.md", content = "用户喜欢蓝色");
```



而后 `MemoryIndexManager` 检测到文件变更 (fs.watch)，会触发增量同步和更新 SQLite 索引，这在上文提到的 Memory Flush 场景中特别重要。



### **交互的安全边界**



为了保证整个系统的安全边界，对 memory_get 制定了严格的路径限制，规定其只能读取到特定位置的文件：

```
async readFile(params: {
  relPath: string;
  from?: number;
  lines?: number;
}): Promise<{ text: string; path: string }> {
  // 路径验证
  const inWorkspace = 
    relPath.length > 0 && 
    !relPath.startsWith("..") && 
    !path.isAbsolute(relPath);
  const allowedWorkspace = inWorkspace && isMemoryPath(relPath);
  
  // 只允许读取：
  // 1. MEMORY.md / memory.md
  // 2. memory/*.md
  // 3. 配置的 extraPaths 中的 .md 文件
  if (!allowedWorkspace && !allowedAdditional) {
    throw new Error("path required");  // 安全限制
  }
  
  if (!absPath.endsWith(".md")) {
    throw new Error("path required");  // 只允许 .md 文件
  }
  
  // 文件读取逻辑...
}
```







## **一个典型的记忆系统交互流程**



场景：用户询问 "我之前说过喜欢什么颜色？"



![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ZRhjO8xAWr450JfaE4FhpHE0WnjS4V12qpnfVk22aibDHDkqttLicLPnWiacAKMGfhx6kBiakAMxjXSZHiaasNGMUUrYGYNFmGT4T1oJ9KibdGicJg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)



不难看出，类似 OpenClaw 类型的个人助手，使用体验大大依赖于所选用的基础大模型的性能，如果选择某些开源的轻量化模型，很容易陷入复杂工具调用的死循环，而选择更优性能的闭源模型又会带来不可避免的成本开销，那么问题来了：C 端用户到底需不需要更高性能的模型？







## 记忆索引的实现流程



此部分，将结合具体的例子，详细整理记忆索引的完整流程。



首先我们假设一个场景，用户在 1 月 10 日与 Agent 进行了一次对话，讨论了需要 Agent 设置提醒的事项，在用户执行 /new 命令后，session-memory 会自动将该对话进行提取并转化为 Markdown 文件如下：



文件路径：

```
~/.openclaw/memory/2026-01-10-reminders.md
```



文件内容：

```
# Session: 2026-01-10 08:00:15 UTC ## Summary用户请求设置每日提醒，讨论了健身计划安排。 ## Key Points- 用户想要每天下午3点收到健身提醒- 健身计划包括：周一胸肌、周三背部、周五腿部- 用户偏好使用 Telegram 接收提醒通知 ## Conversation HighlightsUser: 帮我设置一个每日提醒，下午3点提醒我去健身Assistant: 好的，我已经为你设置了每日下午3点的健身提醒。 User: 对了，我的健身计划是周一练胸，周三练背，周五练腿Assistant: 明白了，我已记录你的健身计划安排。 ## Action Items- [x] 设置每日 15:00 健身提醒- [ ] 后续可添加具体训练动作细节 
```



  **6.1 Step 1: 文件发现与变更检测**

当存入了新的记忆文件，会调用 sync() 方法，系统首先会扫描记忆目录，检测哪些文件需要索引，如果发现记忆文件没有变化，那么也就不需要重新构建一次索引。

- 列出所有记忆文件：

找到所有和记忆有关的文件，为下一步的判重做准备：

```
const files = await listMemoryFiles(this.workspaceDir, this.settings.extraPaths);// 结果: ["~/.openclaw/MEMORY.md", "~/.openclaw/memory/2026-01-10-reminders.md", ...]
```



- 构建文件元信息：

对每个文件调用 buildfileEntry()，只读取文件并计算整体 hash，不做分块等处理。

```
// buildFileEntry 实现const stat = await fs.stat(absPath);const content = await fs.readFile(absPath, "utf-8");  // 读取整个文件const hash = hashText(content);                        // 计算整个文件的 hashreturn {  path: "memory/2026-01-10-reminders.md",  absPath: "/Users/xxx/.openclaw/memory/2026-01-10-reminders.md",  mtimeMs: 1736496015000,  size: 847,  hash: "e4d909c290d0fb1ca068ffaddf22cbd0"  // 整个文件内容的 MD5};
```



- 判断是否需要重新索引：

结合上述文件的 hash 就可以判断出新产生的记忆文件是否与原有的文件相同，如果相同就说明记忆没有变化，省去了重新索引这一步。



```
const record = this.db  .prepare(`SELECT hash FROM files WHERE path = ? AND source = ?`)  .get(entry.path, "memory"); // 情况A: 数据库中无记录，或 hash 不匹配 → 需要索引// 情况B: hash 匹配 → 跳过，无需重新索引if (!params.needsFullReindex && record?.hash === entry.hash) {  return;  // 跳过}await this.indexFile(entry, { source: "memory" });  // 需要索引
```



这个情境中我们假设记忆是新的，那么此时会输出结果：

```
[需要索引] memory/2026-01-10-reminders.md (hash: e4d909c290d0fb1ca068ffaddf22cbd0)
```



  **6.2 Step 2: 文本分块**



经过上一步，只有确定需要索引的文件，才会使用 indexFile() 方法进行分块处理。调用的分块函数如下：

```
const content = await fs.readFile(entry.absPath, "utf-8");const chunks = chunkMarkdown(content, this.settings.chunking);// 默认配置: { tokens: 400, overlap: 80 } export function chunkMarkdown(  content: string,  chunking: { tokens: number; overlap: number },): MemoryChunk[] {  const lines = content.split("\n");  const maxChars = Math.max(32, chunking.tokens * 4);  // 1600 chars  const overlapChars = Math.max(0, chunking.overlap * 4);  // 320 chars  const chunks: MemoryChunk[] = [];   let current: Array<{ line: string; lineNo: number }> = [];  let currentChars = 0;   const flush = () => {    // 将当前累积的行打包成一个 chunk    const text = current.map((entry) => entry.line).join("\n");    const startLine = firstEntry.lineNo;    const endLine = lastEntry.lineNo;    chunks.push({      startLine,      endLine,      text,      hash: hashText(text),  // SHA-256(chunk文本)    });  };   const carryOverlap = () => {    // 保留最后 overlapChars 个字符到下一个 chunk（滑动窗口）    // ...  };   for (let i = 0; i < lines.length; i += 1) {    // 逐行累积，超过 maxChars 就 flush    if (currentChars + lineSize > maxChars && current.length > 0) {      flush();      carryOverlap();  // 保留重叠部分    }    current.push({ line: segment, lineNo });    currentChars += lineSize;  }  flush();  // 最后一批  return chunks;}
```



上述步骤中的分块算法按照以下规则切分文本：

1. 按行遍历，累积字符数（默认约为 tokens * 4 个字符）；
2. 遇到 Markdown 标题（#）时优先断开，保持语义完整；
3. 块之间有重叠（默认约 overlap * 4 个字符），确保跨块检索的连续性。



按照实例文件，分块之后可能会被切分为 2 个块：

| Chunk # | startLine | endLine | text（摘要）                                                 | hash      |
| ------- | --------- | ------- | ------------------------------------------------------------ | --------- |
| Chunk 0 | 1         | 12      | # Session: 2026-01-10...<br>## Summary<br>## Key Points<br>- 用户想要每天下午3点... | 7a8b9c... |
| Chunk 1 | 10        | 22      | - 用户偏好使用 Telegram...<br>## Conversation Highlights<br>## Action Items | 3d4e5f... |



  **6.3 Step 3: 向量化（Embedding）**



上述每个 Chunk 的文本需要转化为向量，用于进行语义搜索。首先系统会先查询已有的 embedding_cache 表，看是否已经有相同文本的向量缓存：

```
const cached = this.loadEmbeddingCache(chunks.map(chunk => chunk.hash));// 如果 chunk.hash 在缓存中命中，直接复用向量，跳过 API 调用
```



对于缓存未命中的 Chunk，调用配置好的 embedding provider（如 OpenAI），返回向量化后的结果。

```
// 批量请求 embeddingconst batchEmbeddings = await this.provider.embedBatch([  "# Session: 2026-01-10 08:00:15 UTC\n\n## Summary\n用户请求设置每日提醒...",  "- 用户偏好使用 Telegram...\n\n## Conversation Highlights..."]); // 返回结果（1536维向量，text-embedding-3-small）// Chunk 0: [0.0234, -0.0567, 0.0891, ..., -0.0123]  (1536个浮点数)// Chunk 1: [0.0345, -0.0678, 0.0902, ..., -0.0234]  (1536个浮点数)
```



而后更新向量缓存：

```
this.upsertEmbeddingCache([  { hash: "7a8b9c...", embedding: [0.0234, -0.0567, ...] },  { hash: "3d4e5f...", embedding: [0.0345, -0.0678, ...] }]); 
```



  **6.4 Step 4: 持久化存储**



向量化完成后，系统会将上述数据写入 SQLite 数据库中的三张表。



- 生成 Chunk ID：

首先，需要先为每个 chunk 生成唯一的标识，其是由多个因素组合 hash 生成。

```
const id = hashText(  `${source}:${path}:${startLine}:${endLine}:${chunkHash}:${model}`); // Chunk 0 的 id 计算:// hashText("memory:memory/2026-01-10-reminders.md:1:12:7a8b9c...:text-embedding-3-small")// → "a1b2c3d4e5f6..." // Chunk 1 的 id 计算:// hashText("memory:memory/2026-01-10-reminders.md:10:22:3d4e5f...:text-embedding-3-small")// → "g7h8i9j0k1l2..."
```



- 写入 chunks 主表：

主表中会存储每一个 chunk 所包含的/相关的完整元数据和向量（JSONL 字符串格式），比如在该例子中，存入主表的一条信息如下：

```
this.db.prepare(`  INSERT INTO chunks (id, path, source, start_line, end_line, hash, model, text, embedding, updated_at)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).run(  "a1b2c3d4e5f6...",                    // id  "memory/2026-01-10-reminders.md",     // path  "memory",                              // source  1,                                     // start_line  12,                                    // end_line  "7a8b9c...",                          // chunk hash  "text-embedding-3-small",             // model  "# Session: 2026-01-10...",           // 原始文本  "[0.0234, -0.0567, ...]",             // 向量 (JSON 字符串)  1736496100000                          // updated_at);
```



- 写入 chunks_vec 向量表：

此处的 sqlite_vec 为虚拟表，专门用于向量相似度（语义相似度）的搜索，表中存储的内容示例如下：

```
this.db.prepare(`INSERT INTO chunks_vec (id, embedding) VALUES (?, ?)`)  .run(    "a1b2c3d4e5f6...",           // 与 chunks 表相同的 id    vectorToBlob([0.0234, ...])  // 转换为二进制 BLOB 格式  );
```



- 写入 chunks_fts 全文搜索表：

此处的 FTS5 也是虚拟表，而且 SQLite FTS5 会自动对 text 字段进行分词，不需要手动进行分词处理。

```
this.db.prepare(`  INSERT INTO chunks_fts (text, id, path, source, model, start_line, end_line)  VALUES (?, ?, ?, ?, ?, ?, ?)`).run(  "# Session: 2026-01-10...",           // text (FTS5 自动分词)  "a1b2c3d4e5f6...",                    // id (UNINDEXED，不分词)  "memory/2026-01-10-reminders.md",     // path (UNINDEXED)  "memory",                              // source (UNINDEXED)  "text-embedding-3-small",             // model (UNINDEXED)  1,                                     // start_line (UNINDEXED)  12                                     // end_line (UNINDEXED));
```



上述有些字段标记为 UNINDEXED，意味着不会参与全文搜索索引，只是作为元数据进行存储，方便后续 JOIN 查询和过滤，只有 text 字段会被 FTS5 分词和建立倒排索引。



- 更新 files 表：

上述存储完成后，会再次记录文件级别的元信息，用于下次进行变更检测。

```
this.db.prepare(`  INSERT INTO files (path, source, hash, mtime, size) VALUES (?, ?, ?, ?, ?)  ON CONFLICT(path) DO UPDATE SET hash=excluded.hash, mtime=excluded.mtime, size=excluded.size`).run(  "memory/2026-01-10-reminders.md",  "memory",  "e4d909c290d0fb1ca068ffaddf22cbd0",  // 整个文件的 hash  1736496015000,  847);
```



  **6.5 Step 5: 最终数据库状态**



1、  files 表：



| **path**                       | **source** | **hash**                         | **mtime**     | **size** |
| ------------------------------ | ---------- | -------------------------------- | ------------- | -------- |
| memory/2026-01-10-reminders.md | memory     | e4d909c290d0fb1ca068ffaddf22cbd0 | 1736496015000 | 847      |



2、 chunks 表（主表）：



| **id**       | **path**                       | **source** | **start_line** | **end_line** | **hash**  | **model**              | **text**                                                     | **embedding**        |
| ------------ | ------------------------------ | ---------- | -------------- | ------------ | --------- | ---------------------- | ------------------------------------------------------------ | -------------------- |
| a1b2c3d4e5f6 | memory/2026-01-10-reminders.md | memory     | 1              | 12           | 7a8b9c... | text-embedding-3-small | # Session: 2026-01-10 08:00:15 UTC<br>## Summary<br>用户请求设置每日提醒... | [0.0234,-0.0567,...] |
| g7h8i9j0k1l2 | memory/2026-01-10-reminders.md | memory     | 10             | 22           | 3d4e5f... | text-embedding-3-small | - 用户偏好使用 Telegram...<br>## Conversation Highlights<br>## Action Items | [0.0345,-0.0678,...] |



3、 chunks_vec 表（sqlite-vec 向量表）：



| id              | embedding (BLOB)                      |
| --------------- | ------------------------------------- |
| a1b2c3d4e5f6... | <binary: 1536 × float32 = 6144 bytes> |
| g7h8i9j0k1l2... | <binary: 1536 × float32 = 6144 bytes> |



4、 chunks_fts 表（FTS5 全文索引表）：



| text                       | id           | path                           | source | model                  | start_line | end_line |
| -------------------------- | ------------ | ------------------------------ | ------ | ---------------------- | ---------- | -------- |
| # Session: 2026-01-10...   | a1b2c3d4e5f6 | memory/2026-01-10-reminders.md | memory | text-embedding-3-small | 1          | 12       |
| - 用户偏好使用 Telegram... | g7h8i9j0k1l2 | memory/2026-01-10-reminders.md | memory | text-embedding-3-small | 10         | 22       |



注：在FTS5 内部会自动为 text 列建立倒排索引，如：

```
> - "健身" → [a1b2c3d4e5f6..., g7h8i9j0k1l2...]> - "提醒" → [a1b2c3d4e5f6...]> - "Telegram" → [g7h8i9j0k1l2...]
```



# 动态记忆总体架构与工作流程







# 静态记忆总体架构与工作流程

## 一、总体流程图

```markdown
┌────────────────────────────────────────────────────┐
│               OpenClaw Agent Runtime               │
├────────────────────────────────────────────────────┤
│                                                    │
│   ┌─────────────┐         ┌─────────────┐          │
│   │  Markdown   │ ──────► │   SQLite    │          │
│   │  文件系统    │ 索引     │  向量数据库  │           │
│   │ (人类可读)   │ ◄─────  │  (语义检索)  │           │
│   └─────────────┘         └─────────────┘          │
│         ▲                        ▲                 │
│         │ 监听变化                │ 向量化检索        │
│         └────────────────────────┘                 │
│                                                    │
└────────────────────────────────────────────────────┘
```

**核心理念**：

- ✅ **人类优先**：Markdown是唯一事实来源
- ✅ **机器辅助**：SQLite只为快速检索
- ✅ **自动同步**：文件变化→索引更新（无感）

**执行流程：**

```
┌─────────────────────────────────────────────────────────────┐
│                     OpenClaw Gateway                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ memory-core 插件 (文件 → 向量索引)                    │  │
│  │  • 监视 workspace 下 memory/*.md                     │  │
│  │  • 分块 (~400 tokens)                                │  │
│  │  • Embedding → SQLite + sqlite-vec                   │  │
│  │  • FTS 全文索引                                      │  │
│  └──────────────────────────────┬───────────────────────┘  │
└──────────────────────────────────┼──────────────────────────┘
                                   │
      ┌────────────────────────────┼──────────────────────────┐
      │                            ▼                          │
┌─────┴──────────────────────────────────────────────────────┐
│               Agent Sessions (002newsanchor)              │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Tools                                               │ │
│  │  • memory_search(query, top_k=10) → 混合检索         │ │
│  │  • memory_get(path, start_line, end_line) → 读取     │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**工作流程图**

```
┌──────────────────────────────────────────────────────────────────┐
│                          典型交互流程                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  用户: "南京今天天气"                                             │
│     │                                                            │
│     ▼                                                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 1. 会话启动                                                │  │
│  │    - 加载 SOUL.md, USER.md                                 │  │
│  │    - 加载 memory/今天.md, 昨天.md                          │  │
│  │    - 【群聊】跳过 MEMORY.md                                 │  │
│  └────────────────────────────────────────────────────────────┘  │
│     │                                                            │
│     ▼                                                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 2. 意图识别                                                │  │
│  │    - 识别为天气查询意图                                    │  │
│  │    - 触发 weather 工具                                     │  │
│  └────────────────────────────────────────────────────────────┘  │
│     │                                                            │
│     ▼                                                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 3. 数据获取                                                │  │
│  │    - curl wttr.in/Nanjing?format=j1                        │  │
│  │    - 解析 JSON 响应                                        │  │
│  └────────────────────────────────────────────────────────────┘  │
│     │                                                            │
│     ▼                                                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 4. 格式化输出                                              │  │
│  │    - 提取温度、天气、风力、湿度等                          │  │
│  │    - 生成建议                                              │  │
│  │    - 添加 Model/Tokens/Skill 页脚 (SOUL.md 规范)          │  │
│  └────────────────────────────────────────────────────────────┘  │
│     │                                                            │
│     ▼                                                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 5. 记忆写入（宽松模式）                                    │  │
│  │    - 追加到 memory/2026-03-18.md                           │  │
│  │    - 添加 [WEATHER] 标签                                   │  │
│  │    - 自动更新 SQLite 索引（向量化）                        │  │
│  └────────────────────────────────────────────────────────────┘  │
│     │                                                            │
│     ▼                                                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ 6. 响应用户                                                │  │
│  │    - 发送格式化天气信息                                    │  │
│  │    - 包含分隔线和元数据页脚                                │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```


---

## 二、Markdown文件文件系统

### 2.1 工作空间布局

```
/Users/will/.openclaw/workspace-002/
├── memory/                      ← 索引源目录（唯一）
│   ├── 2026-03-15.md           ← 每日记忆文件
│   ├── 2026-03-16.md
│   ├── 2026-03-17.md
│   └── 2026-03-18.md           ← 当前，持续追加
├── memory/TAGS.md              ← 标签规范 (可选)   
├── HEARTBEAT.md                ← 心跳任务定义
├── ARCHIVE/                    ← 备份（可选）
│   ├── 2026-03-15.md
│   └── ...
└── scripts/                   ← 辅助脚本
    ├── memory_health.py       ← 健康检查
    ├── memory_summarize.py    ← 自动摘要
    └── tag_migrate.py         ← 标签迁移（一次性）
```

**文件职责**：

| 文件                   | 内容                                 | 更新频率                 | 标签要求          |
| ---------------------- | ------------------------------------ | ------------------------ | ----------------- |
| `memory/YYYY-MM-DD.md` | 原始日志：所有heartbeat、任务、对话  | 每次heartbeat/任务后追加 | 每条记录需标签    |
| `MEMORY.md`            | 精选总结：用户偏好、趋势洞察、工作流 | 定期手动或自动整理       | `[CONFIG][TREND]` |
| `memory/TAGS.md`       | 标签规范文档                         | 静态                     | -                 |

### 2.2 记忆文件格式`memory/YYYY-MM-DD.md`

每个 `YYYY-MM-DD.md` 包含：

```markdown
# 2026-03-18 记忆日志

### [NEWS] | [PREF] | [CHAT] | [CONFIG] | [TREND]  ← 多标签

**时间**: 04:21 UTC
**来源**: Tavily Search

- 重要事件描述 1
- 重要事件描述 2
- ...

### [NEWS] 另一条新闻

**时间**: 13:11 (Asia/Shanghai)
**来源**: Yahoo Finance

具体内容...
```

**标签规范** (参考 `memory/TAGS.md`)：

- `[NEWS]` - 新闻动态
- `[PREF]` - 用户偏好
- `[CHAT]` - 对话记录
- `[CONFIG]` - 系统配置
- `[TREND]` - 趋势观察
- `[ERROR]` - 异常事件
- `[TODO]` - 待办事项

---

## 三、SQLite向量数据库-数据流与同步机制

### 1. 写入流程 (我执行)

```javascript
// 示例：记录用户偏好
write("memory/2026-03-18.md", `
### [PREF] 用户偏好记录
**用户声明**: "我最感兴趣的是英伟达的新闻"
**记录**: 已同步至 MEMORY.md 和数据库
`);

// 结果：
// 1. 文件立即更新 (+N 行)
// 2. OpenClaw 后台监听器检测到变化
// 3. 触发索引任务（异步，通常<2分钟）
```

---

### 2. 索引流程 (OpenClaw后台)

```
┌─────────────┐
│   FsWatch   │ 监听文件变化
└──────┬──────┘
       │ 检测到修改事件
       ▼
┌─────────────┐
│   Chunker   │ 智能分块
│             │ • 按段落/标题边界
│             │ • chunk_size=400 tokens
│             │ • overlap=80 tokens
└──────┬──────┘
       │ [(start, end, text), ...]
       ▼
┌─────────────┐
│  Embedding  │ 向量化
│             │ model: qwen3-embedding:0.6b
│             │ → [0.123, -0.456, ...] × 1024
└──────┬──────┘
       │ {chunks + embeddings}
       ▼
┌─────────────┐
│   SQLite    │ 存储
│             │ • 更新 files 表 (hash, mtime)
│             │ • 插入 chunks (text, embedding)
│             │ • 重建 HNSW 索引（增量）
└─────────────┘
```

**关键特性**：

- 🔄 **增量索引**：只处理修改的文件
- 🔄 **去重**：内容hash相同则跳过
- 🔄 **失败安全**：索引失败不影响文件写入

---

## 四、SQLite向量数据库-索引机制 (memory-core)

### 3.1 索引触发

| 触发方式     | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| **自动监视** | memory-core 监听 `workspace-002/memory/*.md` 文件修改时间 (mtime) |
| **手动命令** | `openclaw memory index` 强制重建所有文件                     |
| **守护进程** | OpenClaw Gateway 后台任务自动处理 `dirty` 状态               |

### 3.2 索引流程

```
File Change Detected
        ↓
Read File (UTF-8)
        ↓
Chunking (≈400 tokens / chunk, 按段落边界)
        ↓
For each chunk:
  ├─ Generate embedding (Ollama qwen3-embedding:0.6b)
  ├─ Store in SQLite chunks table
  ├─ Build FTS (Full-Text Search) index
  └─ Update files table (hash, mtime, size)
        ↓
Update DB metadata (status=clean)
```

### 3.3 数据库结构

**位置**: `~/.openclaw/memory/002newsanchor.sqlite`

**核心表结构**：

#### `files` - 文件元数据

```sql
CREATE TABLE files (
  path TEXT PRIMARY KEY,   -- "memory/2026-03-18.md"
  hash TEXT,               -- SHA256 (去重)
  mtime INTEGER,           -- 修改时间戳
  size INTEGER             -- 文件大小
);
```

#### `chunks` - 分块内容 + 向量

```sql
CREATE TABLE chunks (
  id TEXT PRIMARY KEY,          -- 内容hash (SHA256)
  path TEXT NOT NULL,           -- 源文件路径
  source TEXT DEFAULT 'memory', -- 数据源
  start_line INTEGER,           -- 起始行号
  end_line INTEGER,             -- 结束行号
  hash TEXT NOT NULL,           -- 内容hash
  model TEXT NOT NULL,          -- "qwen3-embedding:0.6b"
  text TEXT NOT NULL,           -- 文本内容 (~400 tokens)
  embedding TEXT NOT NULL,      -- 向量 (JSON array, 1024 dims)
  updated_at INTEGER NOT NULL   -- 更新时间戳 (ms)
);
```

**索引**：

- `idx_chunks_path` - B-tree on path
- `chunks_fts*` - SQLite FTS5 全文搜索
- `chunks_vec*` - HNSW 向量检索索引

---

## 四、SQLite向量数据库-检索机制

### 4.1 混合检索配置

在 `openclaw.json` 中配置：

```json
"memorySearch": {
  "provider": "openai",
  "remote": {
    "baseUrl": "http://127.0.0.1:11434/v1/",
    "apiKey": "ollama"
  },
  "model": "qwen3-embedding:0.6b",
  "query": {
    "hybrid": {
      "enabled": true,
      "vectorWeight": 0.7,       // 70% 语义匹配
      "textWeight": 0.3,         // 30% 关键词匹配
      "mmr": {
        "enabled": true,
        "lambda": 0.7            // 相关性 vs 多样性平衡
      },
      "temporalDecay": {
        "enabled": true,
        "halfLifeDays": 30       // 30天后权重减半
      }
    }
  }
}
```

### 4.2 检索流程

```python
# 调用示例
results = memory_search("NVIDIA GTC", top_k=10)

# 内部流程
1. 向量化查询: embedding = ollama.embed("NVIDIA GTC")
2. 并行搜索:
   ├─ 向量搜索: cosine_similarity(embedding, chunk_embedding) × 0.7
   ├─ 全文搜索: bm25_score("NVIDIA GTC", chunk_text) × 0.3
   └─ 时间衰减: e^(-Δt / 30d) (如果启用)
3. MMR 重排序: λ=0.7 平衡相关性与多样性
4. 返回 top_k 结果，每个包含:
   - path: "memory/2026-03-18.md"
   - start_line, end_line
   - text: 片段内容
   - score: 综合得分 (0-1)
```

**评分公式**:

```
final_score =
  0.70 * cosine_similarity(query_vector, chunk_vector) +
  0.30 * BM25/text_match_score(query, chunk_text) +
  [MMR重排序: λ=0.7, 平衡相关性与多样性] +
  [时间衰减: e^(-Δt/30d), 30天半衰期]
```

**混合检索权重解释**

**总得分** = 0.7 × 语义相似度 + 0.3 × 文本匹配 + 时间衰减 + MMR

| 参数                         | 当前值 | 调优建议                            |
| ---------------------------- | ------ | ----------------------------------- |
| `vectorWeight`               | 0.7    | 侧重语义，适合新闻抽象查询          |
| `textWeight`                 | 0.3    | 确保精确词匹配                      |
| `mmr.lambda`                 | 0.7    | 偏向相关性 (1.0=纯相关, 0.0=纯多样) |
| `temporalDecay.halfLifeDays` | 30     | 旧新闻权重渐减，适合动态领域        |



### 4.3 `memory_get` 工具

```python
# 根据检索结果读取完整上下文
content = memory_get(
  path="memory/2026-03-18.md",
  start_line=1,
  end_line=82
)
# 返回文件片段，用于 AI 生成回复
```

---



## 五、Heartbeat 任务机制

### 5.1 心跳定义 (HEARTBEAT.md)

- **间隔**: 4 小时 (例如)
- **触发**: OpenClaw 定时调度
- **目标**: 主动维护记忆系统，执行新闻任务

### 5.2 心跳检查清单

每次心跳必须检查：

1. ✅ **未完成任务** - 是否有挂起的任务？
2. ✅ **新文件/日志** - 是否有需要归档的内容？
3. ✅ **记忆更新** - 今日记忆文件是否存在？
4. ✅ **新闻任务** - 是否执行 Tavily 搜索（1小时 + 24小时）？
5. ✅ **记忆整理** - 是否需要 Trend 总结？

### 5.3 新闻播报流程

```yaml
Heartbeat Triggered
    ↓
1. 检查 memory/YYYY-MM-DD.md 存在
    ↓ (不存在则创建)
2. 执行 Tavily Search
   ├─ Query 1: "breaking tech news last hour"
   ├─ Query 2: "major tech news past 24h"
   └─ Filters: topic=news, time_range=hour/day
    ↓
3. 解析结果 (去重、筛选、评估时效性)
    ↓
4. 生成简报
   ├─ 格式: 每条 2-3 句
   ├─ 风格: 国际化、简洁、客观
   ├─ 标签: [NEWS] / [TREND]
   └─ 包含: 时间、来源、要点
    ↓
5. 追加写入 memory/YYYY-MM-DD.md
    ↓
6. 触发索引更新 (touch + openclaw memory index)
    ↓
7. 可选: 外部投递 (Feishu 群聊)
    ↓
8. 退出 (直到下次心跳)
```

### 5.4 强制记忆写入规则

**任何任务执行后**必须：

1. 读取 `memory/YYYY-MM-DD.md`
2. 追加新记录，包含 **有效标签**
3. 保存文件 (UTF-8 编码)
4. ✅ OpenClaw 自动检测变化并更新索引

**禁止**: 跳过记忆写入、不添加标签、使用错误编码

---

## 六、配置与管理

### 关键配置文件

| 文件               | 用途                          |
| ------------------ | ----------------------------- |
| `openclaw.json`    | Agent 配置、memorySearch 参数 |
| `HEARTBEAT.md`     | 心跳任务定义                  |
| `memory/TAGS.md`   | 标签规范                      |
| `MEMORY_SYSTEM.md` | 架构文档                      |

---

## 七、使用示例

### 7.1 基本检索

```python
# 在你的 agent 代码中
results = memory_search("NVIDIA GTC", top_k=10)

for r in results:
  print(f"{r['path']}:{r['start_line']}-{r['end_line']}")
  print(f"Score: {r['score']:.3f}")
  print(f"Text: {r['text'][:100]}...")
```

### 7.2 写入新记忆

```python
# 直接追加到当日文件
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")

with open(f"memory/{today}.md", "a") as f:
  f.write(f"\n\n### [NEWS] 标题\n")
  f.write(f"**时间**: {datetime.now().strftime('%H:%M')}\n")
  f.write(f"**来源**: Source Name\n\n")
  f.write("- 要点 1\n")
  f.write("- 要点 2\n")

# 触发索引
import subprocess
subprocess.run(["touch", f"memory/{today}.md"])
subprocess.run(["openclaw", "memory", "index"])
```

